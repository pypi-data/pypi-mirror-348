"""Freshservice tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_freshservice.streams import (agents, assets, asset_types, asset_requests, departments, groups, locations, requesters, tickets, time_entries)


class TapFreshservice(Tap):
    """Freshservice tap class."""

    name = "tap-freshservice"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The Freshservice API key",
        ),
        th.Property(
            "updated_since",
            th.DateTimeType,
            description="The earliest record date to sync. You probably need this! The Freshservice API only returns items less than 30 days old. To override this, you must include an 'updated_since' value in the URL querystring. Providing a value here will ensure this value is used if there is no state (i.e. for a full refresh). ",
            default="2000-01-01T00:00:00Z"
        ),
        th.Property(
            "base_url",
            th.StringType,
            required=True,
            default="https://<replace with your org>.freshservice.com/api/v2",
            description="The url for the Freshservice API",
        ),
    ).to_dict()

    def discover_streams(self) -> list[tickets.FreshserviceStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            agents.AgentsStream(self),
            assets.AssetsStream(self),
            asset_types.AssetTypesStream(self),
            asset_requests.AssetRequestsStream(self),
            departments.DepartmentsStream(self),
            groups.GroupsStream(self),
            locations.LocationsStream(self),
            requesters.RequestersStream(self),
            tickets.TicketsStream(self),
            time_entries.TimeEntriesStream(self),
        ]


if __name__ == "__main__":
    TapFreshservice.cli()
