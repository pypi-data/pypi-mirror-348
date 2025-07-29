"""REST client handling, including FreshserviceStream base class."""

from __future__ import annotations

from typing import Any, Iterable
from urllib.parse import parse_qsl

import backoff
import requests
from singer_sdk.authenticators import BasicAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator  # noqa: TCH002
from singer_sdk.streams import RESTStream

from tap_freshservice.paginator import FreshservicePaginator

class FreshserviceStream(RESTStream):
    """Freshservice stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config.get('url_base')  

    @property
    def authenticator(self) -> BasicAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return BasicAuthenticator.create_for_stream(
            self,
            username=self.config.get("api_key"),
            password="X",
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        # If not using an authenticator, you may also provide inline auth headers:
        # headers["Private-Token"] = self.config.get("auth_token")  # noqa: ERA001
        return headers


    def backoff_wait_generator(self):
        """Try again every 10 seconds if we hit the 429 rate limit response code"""
        return backoff.constant(interval=10)


    def backoff_max_tries(self) -> int:
        """retry 6 times, because the rate limit is per minute. This will guarantee to not hard fail, because after 60 seconds maximum, the rate limit resets"""
        return 6

    def get_new_paginator(self) -> BaseAPIPaginator:
        """Create a new pagination helper instance.
        Returns:
            A pagination helper instance.
        """
        return FreshservicePaginator()

    def get_url_params(
        self,
        context: dict | None,  # noqa: ARG002
        next_page_token: Any | None,  # noqa: ANN401
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        # 100 is the max page size https://api.freshservice.com/#pagination
        params: dict = {"per_page": "100"}
        if next_page_token:
            params["page"] = dict(parse_qsl(next_page_token.query)).get('page')

        return params



class FreshserviceIncrementalStream(FreshserviceStream):
    replication_key = "updated_at"
    is_sorted = True

    def get_url_params(
        self,
        context: dict | None,  # noqa: ARG002
        next_page_token: Any | None,  # noqa: ANN401
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        if self.replication_key:
            params["order_type"] = "asc"
            params["order_by"] = self.replication_key
            starting_timestamp = self.get_starting_timestamp(context)

            # By default only tickets that have been created within the past 30 days will be returned. For older tickets, use the updated_since filter.
            if starting_timestamp:
                params["updated_since"] = starting_timestamp.isoformat()
            elif self.config.get('updated_since') is not None:
                params["updated_since"] = self.config.get('updated_since')

        params.update(super().get_url_params(context, next_page_token))
        return params