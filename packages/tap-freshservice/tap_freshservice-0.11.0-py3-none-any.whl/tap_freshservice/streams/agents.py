"""Stream type classes for tap-freshservice."""
from singer_sdk import typing as th  # JSON Schema typing helpers
from typing import Optional
from tap_freshservice.client import FreshserviceStream

class AgentsStream(FreshserviceStream):
    name = "agents"
    path = "/agents"
    records_jsonpath="$.agents[*]"
    
    schema = th.PropertiesList(
        th.Property("active", th.BooleanType),
        th.Property("address", th.StringType),
        th.Property("background_information", th.StringType),
        th.Property("can_see_all_tickets_from_associated_departments", th.BooleanType),
        th.Property("created_at", th.DateTimeType),
        th.Property("department_ids", th.StringType),
        th.Property("department_names", th.StringType),
        th.Property("email", th.StringType),
        th.Property("first_name", th.StringType),
        th.Property("has_logged_in", th.BooleanType),
        th.Property("id", th.IntegerType),
        th.Property("job_title", th.StringType),
        th.Property("language", th.StringType),
        th.Property("last_active_at", th.DateTimeType),
        th.Property("last_login_at", th.DateTimeType),
        th.Property("last_name", th.StringType),
        th.Property("location_id", th.IntegerType),
        th.Property("location_name", th.StringType),
        th.Property("mobile_phone_number", th.StringType),
        th.Property("occasional", th.BooleanType),
        th.Property("reporting_manager_id", th.IntegerType),
        th.Property("roles", th.StringType),
        th.Property("scoreboard_level_id", th.IntegerType),
        th.Property("time_format", th.StringType),
        th.Property("time_zone", th.StringType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("member_of", th.StringType),
        th.Property("observer_of", th.StringType),
    ).to_dict()
