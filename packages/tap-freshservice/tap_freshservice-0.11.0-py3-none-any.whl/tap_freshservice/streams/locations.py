"""Stream type classes for tap-freshservice."""
from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_freshservice.client import FreshserviceStream
from tap_freshservice.streams.assets import AssetsStream

class LocationsStream(FreshserviceStream):
    name = "locations"
    path = "/locations"
    records_jsonpath="$.locations[*]"

    schema = th.PropertiesList(
        th.Property("address", th.StringType),
        th.Property("contact_name", th.StringType),
        th.Property("created_at", th.DateTimeType),
        th.Property("email", th.StringType),
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("parent_location_id", th.IntegerType),
        th.Property("phone", th.StringType),
        th.Property("primary_contact_id", th.IntegerType),
        th.Property("updated_at", th.DateTimeType)
     ).to_dict()