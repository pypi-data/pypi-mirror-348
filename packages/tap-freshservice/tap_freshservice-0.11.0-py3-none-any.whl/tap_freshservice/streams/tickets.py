"""Stream type classes for tap-freshservice."""

from __future__ import annotations

import typing as t
from pathlib import Path
from urllib.parse import urlencode

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_freshservice.client import FreshserviceIncrementalStream

class TicketsStream(FreshserviceIncrementalStream):
    name = "tickets"
    path = "/tickets"
    records_jsonpath="$.tickets[*]"

    def get_url_params(self, context: dict | None, next_page_token) -> dict[str, t.Any] | str:
        parent_params = super().get_url_params(context, next_page_token)
        params = {"include": "stats,tags"}
        params.update(parent_params)
        return params

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for the child streams.
        Refer to https://sdk.meltano.com/en/latest/parent_streams.html"""
        return {
                "ticket_id": record["id"]
            }
    
    schema = th.PropertiesList(
        th.Property("subject", th.StringType),
        th.Property("group_id", th.IntegerType),
        th.Property("department_id", th.IntegerType),
        th.Property("workspace_id", th.IntegerType),
        th.Property("category", th.StringType),
        th.Property("sub_category", th.StringType),
        th.Property("item_category", th.StringType),
        th.Property("requester_id", th.IntegerType),
        th.Property("responder_id", th.IntegerType),
        th.Property("due_by", th.StringType),
        th.Property("fr_escalated", th.BooleanType),
        th.Property("deleted", th.BooleanType),
        th.Property("spam", th.BooleanType),
        th.Property("email_config_id", th.IntegerType),
        th.Property("fwd_emails", th.StringType),
        th.Property("reply_cc_emails", th.StringType),
        th.Property("cc_emails", th.StringType),
        th.Property("is_escalated", th.BooleanType),
        th.Property("fr_due_by", th.StringType),
        th.Property("id", th.IntegerType),
        th.Property("priority", th.IntegerType),
        th.Property("status", th.IntegerType),
        th.Property("source", th.IntegerType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("requested_for_id", th.IntegerType),
        th.Property("to_emails", th.StringType),
        th.Property("type", th.StringType),
        th.Property("description", th.StringType),
        th.Property("description_text", th.StringType),
        th.Property("custom_fields", th.ObjectType(
            th.Property("credit_hrs", th.StringType),
            th.Property("estimate", th.StringType),
            th.Property("pending_reason", th.StringType),
            th.Property("quote_hrs", th.StringType),
            th.Property("definition_of_done", th.StringType),
            th.Property("company_division", th.StringType)
        )),
        th.Property("stats", th.ObjectType(
            th.Property("created_at", th.DateTimeType),
            th.Property("updated_at", th.DateTimeType),
            th.Property("ticket_id", th.IntegerType),
            th.Property("opened_at", th.DateTimeType),
            th.Property("group_escalated", th.BooleanType),
            th.Property("inbound_count", th.IntegerType),
            th.Property("status_updated_at", th.DateTimeType),
            th.Property("outbound_count", th.IntegerType),
            th.Property("pending_since", th.StringType),
            th.Property("resolved_at", th.DateTimeType),
            th.Property("closed_at", th.DateTimeType),
            th.Property("first_assigned_at", th.DateTimeType),
            th.Property("assigned_at", th.DateTimeType),
            th.Property("agent_responded_at", th.DateTimeType),
            th.Property("requester_responded_at", th.DateTimeType),
            th.Property("first_responded_at", th.DateTimeType),
            th.Property("first_resp_time_in_secs", th.IntegerType),
            th.Property("resolution_time_in_secs", th.IntegerType),
        )),
        th.Property("tags", th.StringType)
    ).to_dict()

