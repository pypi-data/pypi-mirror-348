"""Stream type classes for tap-freshservice."""

from __future__ import annotations

import typing as t
from pathlib import Path
from urllib.parse import urlencode

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_freshservice.client import FreshserviceStream
from tap_freshservice.streams.tickets import TicketsStream

def get_url_params(self, context: dict | None, next_page_token) -> dict[str, t.Any] | str:
        parent_params = super().get_url_params(context, next_page_token)
        return parent_params

class TicketActivitiesStream(FreshserviceStream):
    name = "ticket_activities"
    path = "/tickets/{ticket_id}/activities"
    records_jsonpath="$.activities[*]"

    schema = th.PropertiesList(
        th.Property("ticket_id", th.IntegerType),
        th.Property("created_at", th.DateTimeType),
        th.Property("actor", th.ObjectType(
            th.Property("id", th.IntegerType),
            th.Property("name", th.StringType),
        )),
        th.Property("content", th.StringType),
        th.Property("sub_contents", th.StringType),
    ).to_dict()

    parent_stream_type = TicketsStream
    ignore_parent_replication_key = True