from __future__ import annotations

import requests
import logging
import json
from sqlalchemy import desc, exc as sql_exceptions
from sqlalchemy.inspection import inspect
import redis
from typing import Any, Literal

from ckan import types
import ckan.model as model
import ckan.plugins.toolkit as tk
from ckan.lib.search.common import (
    is_available as solr_available,
    make_connection as solr_connection,
)
from ckan.lib.search import clear, rebuild, commit
from ckan.lib.redis import connect_to_redis, Redis

from ckanext.selftools import utils, config

log = logging.getLogger(__name__)


def selftools_solr_query(
    context: types.Context, data_dict: dict[str, Any]
) -> dict[str, Any] | Literal[False]:
    tk.check_access("sysadmin", context, data_dict)

    if solr_available():
        solr = solr_connection()
        solr_url = solr.url
        max_limit = config.selftools_get_operations_limit()
        default_search = "q=*:*&rows=" + str(max_limit)

        search = data_dict.get("q", default_search)

        if "rows=" not in search:
            search += "&rows=" + str(max_limit)
        q_response = requests.get(solr_url.rstrip("/") + "/query?" + search)
        q_response.raise_for_status()

        query = q_response.json()

        return query
    return False


def selftools_solr_delete(
    context: types.Context, data_dict: dict[str, Any]
) -> dict[str, Any]:
    tk.check_access("sysadmin", context, data_dict)

    if not utils.selftools_verify_operations_pwd(data_dict.get("selftools_pwd")):
        return {"success": False, "message": "Unauthorized action."}

    pkg = model.Package.get(data_dict.get("id"))
    if not pkg:
        return {"success": False}

    clear(pkg.id)
    return {"success": True}


def selftools_solr_index(
    context: types.Context, data_dict: dict[str, Any]
) -> dict[str, Any]:
    tk.check_access("sysadmin", context, data_dict)
    id = data_dict.get("id")
    ids = data_dict.get("ids")

    if not id and not ids:
        return {
            "success": False,
            "message": "Dataset ID or multiple IDs should be provided.",
        }
    pkg = None
    if id:
        pkg = model.Package.get(id)

    try:
        rebuild(
            package_id=pkg.id if pkg else None,
            force=tk.asbool(data_dict.get("force", "False")),
            package_ids=json.loads(ids) if ids else [],
        )
        commit()
    except Exception:
        return {"success": False, "message": "An Error appeared while indexing."}
    return {"success": True}


def selftools_db_query(
    context: types.Context, data_dict: dict[str, Any]
) -> dict[str, Any] | Literal[False]:
    tk.check_access("sysadmin", context, data_dict)

    q_model = data_dict.get("model")
    limit = data_dict.get("limit")
    field = data_dict.get("field")
    value = data_dict.get("value")
    order = data_dict.get("order")
    order_by = data_dict.get("order_by")
    if q_model:
        model_fields_blacklist = [
            b.strip().split(".") for b in config.selftools_get_model_fields_blacklist()
        ]
        combained_blacklist = [
            *model_fields_blacklist,
            *[["User", "password"], ["User", "apikey"]],
        ]

        def _get_db_row_values(row: Any, columns: Any, model_name: str) -> list[Any]:
            values = []
            for col in columns:
                if [
                    b for b in combained_blacklist if b[0] == model_name and col == b[1]
                ]:
                    value = "SECURE"
                else:
                    value = getattr(row, col, None)

                if value is not None:
                    values.append(value)
                else:
                    values.append("")

            return values

        models = utils.get_db_models()
        curr_model = [m for m in models if m["label"] == q_model]

        if curr_model:
            try:
                model_class = curr_model[0]["model"]
                q = model.Session.query(model_class)

                if field and value:
                    q = q.filter(getattr(model_class, field) == value)

                if order_by and order:
                    if order == "desc":
                        q = q.order_by(desc(order_by))
                    else:
                        q = q.order_by(order_by)

                if limit:
                    q = q.limit(int(limit))

                results = q.all()

                columns = [col.name for col in inspect(model_class).c]

                structured_results = [
                    _get_db_row_values(row, columns, curr_model[0]["label"])
                    for row in results
                ]

                return {
                    "success": True,
                    "results": structured_results,
                    "fields": columns,
                }
            except (AttributeError, sql_exceptions.CompileError) as e:
                return {
                    "success": False,
                    "message": str(e),
                }
    return False


def selftools_db_update(
    context: types.Context, data_dict: dict[str, Any]
) -> dict[str, Any]:
    tk.check_access("sysadmin", context, data_dict)

    if not utils.selftools_verify_operations_pwd(data_dict.get("selftools_pwd")):
        return {"success": False, "message": "Unauthorized action."}

    q_model = data_dict.get("model")
    limit = data_dict.get("limit")
    field = data_dict.get("field")
    value = data_dict.get("value")
    where_field = data_dict.get("where_field")
    where_value = data_dict.get("where_value")
    if q_model:
        models = utils.get_db_models()
        curr_model = [m for m in models if m["label"] == q_model]

        if curr_model:
            try:
                model_class = curr_model[0]["model"]

                primary_key = None
                mapper = model_class.__mapper__
                pk_prop = list(mapper.iterate_properties)
                for prop in pk_prop:
                    if hasattr(prop, "columns") and prop.columns[0].primary_key:
                        primary_key = getattr(model_class, prop.key)
                if not primary_key:
                    return {
                        "success": False,
                        "message": "Cannot extract Primary key for the Model.",
                    }

                # First filter and limit results
                q = model.Session.query(primary_key)

                if where_field and where_value:
                    q = q.filter(getattr(model_class, where_field) == where_value)

                if limit:
                    q = q.limit(int(limit))

                if field and value:
                    ids = [i[0] for i in q.all()]
                    # Update already limited results
                    upd = (
                        model.Session.query(model_class)
                        .filter(primary_key.in_(ids))
                        .update({field: value})
                    )

                    model.Session.commit()

                    return {
                        "success": True,
                        "updated": upd,
                        "effected": ids,
                        "effected_json": json.dumps(ids, indent=2),
                    }
                else:
                    return {"success": False, "message": "Provide the WHERE condition"}
            except AttributeError:
                return {
                    "success": False,
                    "message": f"There no attribute '{field}' in '{curr_model[0]['label']}'",
                }

    return {"success": False}


def selftools_redis_query(
    context: types.Context, data_dict: dict[str, Any]
) -> dict[str, Any] | Literal[False]:
    tk.check_access("sysadmin", context, data_dict)

    def _redis_key_value(redis_conn: Any, key: str):
        key_type = redis_conn.type(key).decode("utf-8")
        val = ""
        try:
            if key_type == "string":
                val = redis_conn.get(key)
            elif key_type == "hash":
                val = redis_conn.hgetall(key)
            else:
                val = f"<Unsupported type: {key_type}>"
        except redis.exceptions.RedisError as e:  # pyright: ignore
            val = f"<Error: {str(e)}>"

        return val

    redis_conn: Redis = connect_to_redis()

    q = data_dict.get("q", "")
    if q:
        keys = redis_conn.keys(f"*{q}*")
        max_limit = config.selftools_get_operations_limit()
        keys = keys[:max_limit]  # pyright: ignore
        redis_results = [
            {
                "key": k.decode("utf-8"),
                "type": redis_conn.type(k).decode("utf-8"),  # pyright: ignore
                "value": str(_redis_key_value(redis_conn, k)),
            }
            for k in keys
        ]

        return {"success": True, "results": redis_results}
    return False


def selftools_redis_update(
    context: types.Context, data_dict: dict[str, Any]
) -> dict[str, Any]:
    tk.check_access("sysadmin", context, data_dict)

    if not utils.selftools_verify_operations_pwd(data_dict.get("selftools_pwd")):
        return {"success": False, "message": "Unauthorized action."}

    key = data_dict.get("redis_key")
    value = data_dict.get("value")
    if key and value:
        redis_conn: Redis = connect_to_redis()
        redis_conn.set(key, value)
        return {"success": True}

    return {"success": False}


def selftools_redis_delete(
    context: types.Context, data_dict: dict[str, Any]
) -> dict[str, Any]:
    tk.check_access("sysadmin", context, data_dict)

    if not utils.selftools_verify_operations_pwd(data_dict.get("selftools_pwd")):
        return {"success": False, "message": "Unauthorized action."}

    key = data_dict.get("redis_key")
    if key:
        redis_conn: Redis = connect_to_redis()

        deleted = redis_conn.delete(key)
        if deleted:
            return {"success": True}
    return {"success": False}


def selftools_config_query(
    context: types.Context, data_dict: dict[str, Any]
) -> dict[str, Any]:
    tk.check_access("sysadmin", context, data_dict)

    if not utils.selftools_verify_operations_pwd(data_dict.get("selftools_pwd")):
        return {"success": False, "message": "Unauthorized action."}

    key = data_dict.get("q")
    if key:
        blacklist = config.selftools_get_config_blacklist()
        default_blacklist = [
            "sqlalchemy.url",
            "ckan.datastore.write_url",
            "ckan.datastore.read_url",
            "solr_url",
            "solr_user",
            "solr_password",
            "ckan.redis.url",
            config.SELFTOOLS_CONFIG_BLACKLIST,
            config.SELFTOOLS_OPERATIONS_PWD,
        ]
        config_keys = tk.config.keys()
        config_keys = [
            k for k in config_keys if k not in [*default_blacklist, *blacklist]
        ]
        config_results = [
            {"key": ck, "value": tk.config.get(ck)} for ck in config_keys if key in ck
        ]
        return {"success": True, "results": config_results}

    return {"success": False}
