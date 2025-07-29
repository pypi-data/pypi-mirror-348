"""Stream type classes for tap-freshservice."""
from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_freshservice.client import FreshserviceStream

class GroupsStream(FreshserviceStream):
    name = "groups"
    path = "/groups"
    records_jsonpath="$.groups[*]"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("description", th.StringType),
        th.Property("escalate_to", th.IntegerType),
        th.Property("unassigned_for", th.StringType),
        th.Property("business_hours_id", th.IntegerType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("auto_ticket_assign", th.BooleanType),
        th.Property("ocs_schedule_id", th.IntegerType),
        th.Property("members", th.StringType),
    ).to_dict()

