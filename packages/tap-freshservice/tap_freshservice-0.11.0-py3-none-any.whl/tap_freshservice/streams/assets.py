"""Stream type classes for tap-freshservice."""

from __future__ import annotations
from singer_sdk import typing as th  # JSON Schema typing helpers
from typing import Optional
import typing as t
from tap_freshservice.client import FreshserviceStream

class AssetsStream(FreshserviceStream):
    name = "assets"
    path = "/assets?workspace_id=0"
    records_jsonpath="$.assets[*]"
    
    def get_url_params(self, context: dict | None, next_page_token) -> dict[str, t.Any] | str:
        parent_params = super().get_url_params(context, next_page_token)
        params = {"include": "type_fields"}
        params.update(parent_params)
        return params
    
    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for the child streams.
        Refer to https://sdk.meltano.com/en/latest/parent_streams.html"""
        return {"display_id": record["display_id"],
                "asset_id": record["id"]
            }
    
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("display_id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("description", th.StringType),
        th.Property("asset_type_id", th.IntegerType),
        th.Property("impact", th.StringType),
        th.Property("usage_type", th.StringType),
        th.Property("asset_tag", th.StringType),
        th.Property("user_id", th.IntegerType),
        th.Property("department_id", th.IntegerType),
        th.Property("location_id", th.IntegerType),
        th.Property("agent_id", th.IntegerType),
        th.Property("group_id", th.IntegerType),
        th.Property("assigned_on", th.DateTimeType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("author_type", th.StringType),
        th.Property("end_of_life", th.DateTimeType),
        th.Property("discovery_enabled", th.BooleanType),
        th.Property("type_fields", th.ObjectType(
            th.Property("code_18000842429", th.StringType),
            th.Property("category_18000842429", th.StringType),
            th.Property("status_18000842429", th.StringType),
            th.Property("url_18000842432", th.StringType)
        ))
    ).to_dict()
