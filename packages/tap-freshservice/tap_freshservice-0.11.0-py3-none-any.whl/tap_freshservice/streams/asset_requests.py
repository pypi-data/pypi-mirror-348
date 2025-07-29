"""Stream type classes for tap-freshservice."""
from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_freshservice.client import FreshserviceStream
from tap_freshservice.streams.assets import AssetsStream

class AssetRequestsStream(FreshserviceStream):
    name = "asset_requests"
    path = "/assets/{display_id}/requests"
    records_jsonpath="$.requests[*]"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("request_type", th.StringType),
        th.Property("request_id", th.StringType),
        th.Property("request_details", th.StringType),
        th.Property("request_status", th.StringType),
        th.Property("workspace_id", th.IntegerType),
        th.Property("display_id", th.IntegerType),
        th.Property("asset_id", th.IntegerType)
     ).to_dict()
    
    parent_stream_type = AssetsStream
    ignore_parent_replication_key = True