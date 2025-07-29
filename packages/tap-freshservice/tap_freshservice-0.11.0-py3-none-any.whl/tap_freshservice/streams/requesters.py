"""Stream type classes for tap-freshservice."""
from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_freshservice.client import FreshserviceStream

class RequestersStream(FreshserviceStream):
    name = "requesters"
    path = "/requesters"
    records_jsonpath="$.requesters[*]"

    schema = th.PropertiesList(
        th.Property("active", th.BooleanType),
        th.Property("address", th.StringType),
        th.Property("background_information", th.StringType),
        th.Property("can_see_all_changes_from_associated_departments", th.BooleanType),
        th.Property("can_see_all_tickets_from_associated_departments", th.BooleanType),
        th.Property("created_at", th.DateTimeType),
        th.Property("custom_fields", th.StringType),
        th.Property("department_ids", th.StringType),
        th.Property("department_names", th.StringType),
        th.Property("external_id", th.IntegerType),
        th.Property("first_name", th.StringType),
        th.Property("has_logged_in", th.BooleanType),
        th.Property("id", th.IntegerType),
        th.Property("is_agent", th.BooleanType),
        th.Property("language", th.StringType),
        th.Property("last_name", th.StringType),
        th.Property("location_id", th.IntegerType),
        th.Property("location_name", th.StringType),
        th.Property("mobile_phone_number", th.StringType),
        th.Property("primary_email", th.StringType),
        th.Property("reporting_manager_id", th.IntegerType),
        th.Property("secondary_emails", th.StringType),
        th.Property("time_format", th.StringType),
        th.Property("time_zone", th.StringType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("vip_user", th.BooleanType),
        th.Property("work_phone_number", th.StringType)
    ).to_dict()



            