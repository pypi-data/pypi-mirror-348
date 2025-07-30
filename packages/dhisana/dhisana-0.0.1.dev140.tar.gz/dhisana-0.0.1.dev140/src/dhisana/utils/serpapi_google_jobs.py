import json
import logging
from typing import Any, Dict, List, Optional

import aiohttp

from dhisana.utils.assistant_tool_tag import assistant_tool
from dhisana.utils.cache_output_tools import cache_output, retrieve_output
from dhisana.utils.serpapi_google_search import get_serp_api_access_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _normalise_job_result(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a SerpApi jobs result to a simplified schema."""
    apply_link = ""
    apply_options = raw.get("apply_options") or raw.get("apply_links") or []
    if isinstance(apply_options, list) and apply_options:
        first = apply_options[0]
        if isinstance(first, dict):
            apply_link = first.get("link") or first.get("apply_link") or ""
    if isinstance(apply_options, dict):
        apply_link = apply_options.get("link") or apply_options.get("apply_link") or ""

    return {
        "job_title": raw.get("title", ""),
        "company_name": raw.get("company_name") or raw.get("company", ""),
        "location": raw.get("location", ""),
        "via": raw.get("via", ""),
        "description": raw.get("description", ""),
        "job_posting_url": raw.get("job_highlight_url")
        or raw.get("apply_link")
        or apply_link
        or raw.get("link", ""),
    }


@assistant_tool
async def search_google_jobs_serpapi(
    query: str,
    number_of_results: int = 10,
    offset: int = 0,
    tool_config: Optional[List[Dict]] = None,
    location: Optional[str] = None,
) -> List[str]:
    """Search Google Jobs via SerpApi and return normalised JSON strings."""
    if not query:
        logger.warning("Empty query provided to search_google_jobs_serpapi")
        return []

    cache_key = f"jobs_serpapi_{query}_{number_of_results}_{offset}_{location or ''}"
    cached = retrieve_output("search_google_jobs_serpapi", cache_key)
    if cached is not None:
        return cached

    api_key = get_serp_api_access_token(tool_config)
    page_size = 10
    start_index = offset
    collected: List[Dict[str, Any]] = []

    async with aiohttp.ClientSession() as session:
        while len(collected) < number_of_results:
            to_fetch = min(page_size, number_of_results - len(collected))
            params = {
                "engine": "google_jobs",
                "q": query,
                "api_key": api_key,
                "num": to_fetch,
                "start": start_index,
            }
            if location:
                params["location"] = location
            try:
                async with session.get("https://serpapi.com/search", params=params) as resp:
                    if resp.status != 200:
                        try:
                            err = await resp.json()
                        except Exception:
                            err = await resp.text()
                        logger.warning("SerpApi jobs error: %s", err)
                        return [json.dumps({"error": err})]
                    payload = await resp.json()
            except Exception as exc:
                logger.exception("SerpApi jobs request failed")
                return [json.dumps({"error": str(exc)})]

            jobs = payload.get("jobs_results", [])
            if not jobs:
                break
            collected.extend(jobs)
            start_index += to_fetch

    normalised = [_normalise_job_result(j) for j in collected[:number_of_results]]
    serialised = [json.dumps(item) for item in normalised]
    cache_output("search_google_jobs_serpapi", cache_key, serialised)
    logger.info("Returned %d job results for '%s'", len(serialised), query)
    return serialised
