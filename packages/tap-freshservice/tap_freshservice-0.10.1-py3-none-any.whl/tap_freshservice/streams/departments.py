"""Stream type classes for tap-freshservice."""
from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_freshservice.client import FreshserviceStream
from tap_freshservice.streams.assets import AssetsStream

class DepartmentsStream(FreshserviceStream):
    name = "departments"
    path = "/departments"
    records_jsonpath="$.departments[*]"

    schema = th.PropertiesList(
        th.Property("description", th.StringType),
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("head_name", th.StringType),
        th.Property("prime_user_id", th.IntegerType),
        th.Property("prime_user_name", th.StringType),
        th.Property("head_user_id", th.IntegerType),
        th.Property("custom_fields", th.ObjectType(
            th.Property("company_code", th.StringType),
            th.Property("is_active", th.BooleanType),
            th.Property("internal_channel_id", th.StringType),
            th.Property("client_channel_id", th.StringType),
            th.Property("data_crew_group_id", th.StringType)
        )),
        th.Property("domains", th.StringType)
     ).to_dict()