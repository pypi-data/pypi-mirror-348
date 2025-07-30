from collections.abc import AsyncIterator, Generator
from contextlib import asynccontextmanager
from dataclasses import dataclass
import os
from typing import Any, Dict, Optional
import httpx
from fastmcp import FastMCP, Context
import logging

logger = logging.getLogger(__name__)
# API endpoints and constants
ORCA_API_HOST = os.environ.get("ORCA_API_HOST", "https://api.orcasecurity.io")
ORCA_AUTH_TOKEN = os.environ.get("ORCA_AUTH_TOKEN", "")
ORCA_REQUEST_TIMEOUT = float(os.environ.get("ORCA_REQUEST_TIMEOUT", "60.0"))
COMMON_HEADERS: Dict[str, str] = {
    "Content-Type": "application/json",
    "User-Agent": "orca-mcp-server",
}


class TokenAuth(httpx.Auth):
    """Token authentication for httpx."""

    def __init__(self, token: str):
        """Initialize with the token."""
        self.token = token

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        """Add the token to the request."""
        request.headers["Authorization"] = f"Token {self.token}"
        yield request


@dataclass
class AppContext:
    client: httpx.AsyncClient


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context"""
    # Initialize on startup
    client = httpx.AsyncClient(
        headers=COMMON_HEADERS,
        auth=TokenAuth(ORCA_AUTH_TOKEN),
        timeout=ORCA_REQUEST_TIMEOUT,
    )
    try:
        yield AppContext(client=client)
    finally:
        # Cleanup on shutdown
        await client.aclose()


mcp = FastMCP("orca", lifespan=app_lifespan)


@mcp.tool()
async def ask_orca(ctx: Context, question: str) -> Dict[str, Any]:
    """
    Ask Orca Security a question in natural language and get results about security issues in the client's cloud environment.
    The tool can handle simple questions like 'Am I vulnerable to X?' or 'Show me which vms are exposed to the internet.'
    Don't overcomplicate and overuse this tool. Give it as much context as possible.
    This tool will return aggregated results grouped by risk level and asset type, as well as the top 10 raw results.
    """
    app_ctx: AppContext = ctx.request_context.lifespan_context
    client = app_ctx.client
    try:
        # Step 1: Get the base Sonar query from AI Sonar
        ai_sonar_resp = await client.post(
            f"{ORCA_API_HOST}/api/ai_sonar/sonar_schema/query",
            json={"search": question, "target_schema": "serving_layer"},
        )
        ai_sonar_resp.raise_for_status()
        ai_sonar_data: Dict[str, Any] = ai_sonar_resp.json()

        base_query: Optional[str] = ai_sonar_data.get(
            "sonar_optimized_payload", {}
        ).get("query")
        if not base_query:
            return {
                "status": "error",
                "error": "Orca AI Sonar couldn't generate a query for your question.",
                "aggregated_results": None,
                "raw_results": None,
            }

        # Step 2: Fetch aggregated results
        aggregated_results_data = None
        try:
            # use POST /api/serving-layer/query_fields to get the fields
            query_fields_resp = await client.post(
                f"{ORCA_API_HOST}/api/serving-layer/query_fields",
                json={
                    "query": base_query,
                    "group_by_fields": True,
                    "additional_models[]": ["CloudAccount"],
                },
            )
            query_fields_resp.raise_for_status()
            query_fields_data: Dict[str, Any] = query_fields_resp.json()
            query_fields = query_fields_data.get("data", [])
            if not query_fields:
                return {
                    "status": "error",
                    "error": "No query fields found for your query from the serving layer.",
                    "aggregated_results": None,
                    "raw_results": None,
                }

            # Search for fields ending with RiskLevel
            risk_level_fields = [
                field["key"]
                for field in query_fields
                if field["key"].endswith("RiskLevel")
            ]

            # If risk level field found, use the first one, otherwise fallback to CloudAccount.CloudProvider
            sort_field = (
                [risk_level_fields[0]]
                if risk_level_fields
                else ["CloudAccount.CloudProvider"]
            )

            aggregated_query_resp = await client.post(
                f"{ORCA_API_HOST}/api/serving-layer/query",
                json={
                    "query": base_query,
                    "group_by[]": sort_field,
                    "additional_models[]": ["CloudAccount"],
                },
            )
            aggregated_query_resp.raise_for_status()
            aggregated_results_data = aggregated_query_resp.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Error fetching aggregated results: {e}")
        except Exception as e:
            logger.error(f"Generic error fetching aggregated results: {e}")

        # Step 3: Fetch top 10 raw results
        raw_results_data = None
        try:
            raw_query_resp = await client.post(
                f"{ORCA_API_HOST}/api/serving-layer/query",
                json={
                    "query": base_query,
                    "order_by[]": sort_field,
                    "limit": 10,
                    "start_at_index": 0,
                    "get_results_and_count": True,
                },
            )
            raw_query_resp.raise_for_status()
            raw_results_data = raw_query_resp.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Error fetching raw results: {e}")
        except Exception as e:
            logger.error(f"Generic error fetching raw results: {e}")

        if not aggregated_results_data and not raw_results_data:
            return {
                "status": "error",
                "error": "No results found for your query from either aggregated or raw data endpoints.",
                "aggregated_results": None,
                "raw_results": None,
            }

        return {
            "status": "success",
            "aggregated_results": aggregated_results_data,
            "raw_results": raw_results_data,
        }

    except httpx.HTTPStatusError as e:
        # This catches errors from the AI Sonar call or if all sub-calls fail critically
        return {
            "status": "error",
            "error": f"HTTP error during Orca API call: {e.response.status_code} - {e.response.text}",
            "aggregated_results": None,
            "raw_results": None,
        }
    except Exception as e:
        return {
            "status": "error",
            "error": f"Unable to get results from Orca Security: {e}",
            "aggregated_results": None,
            "raw_results": None,
        }


def main():
    mcp.run()
