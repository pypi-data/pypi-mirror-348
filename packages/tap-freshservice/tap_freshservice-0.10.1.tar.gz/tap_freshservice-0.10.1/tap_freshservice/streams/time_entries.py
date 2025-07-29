"""Stream type classes for tap-freshservice."""

from __future__ import annotations

import typing as t
from pathlib import Path
from urllib.parse import urlencode

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_freshservice.client import FreshserviceStream
from tap_freshservice.streams.tickets import TicketsStream

class TimeEntriesStream(FreshserviceStream):
    name = "time_entries"
    path = "/tickets/{ticket_id}/time_entries"
    records_jsonpath="$.time_entries[*]"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("ticket_id", th.IntegerType),
        th.Property("start_time", th.DateTimeType),
        th.Property("timer_running", th.BooleanType),
        th.Property("billable", th.BooleanType),
        th.Property("time_spent", th.StringType),
        th.Property("executed_at", th.DateTimeType),
        th.Property("task_id", th.IntegerType),
        th.Property("workspace_id", th.IntegerType),
        th.Property("note", th.StringType),
        th.Property("agent_id", th.IntegerType),
    ).to_dict()

    parent_stream_type = TicketsStream
    ignore_parent_replication_key = True