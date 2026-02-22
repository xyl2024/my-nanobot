"""MiniMax usage query module."""

import aiohttp


async def query_minimax_usage(api_key: str) -> str | None:
    """Query MiniMax API usage information.

    Args:
        api_key: MiniMax API key.

    Returns:
        Formatted usage string like "\n\nMinimax已使用：86.67%" or None on failure.
    """
    if not api_key:
        return None

    url = "https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains"
    headers = {
        "authorization": f"Bearer {api_key}",
        "content-type": "application/json",
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status != 200:
                    return None

                data = await response.json()

                # Parse model_remains array (root level, not nested in "data")
                model_remains = data.get("model_remains", [])
                if not model_remains:
                    return None

                # Get first element
                first = model_remains[0]
                total = first.get("current_interval_total_count")
                usage_count = first.get("current_interval_usage_count")

                if total is None or usage_count is None or total == 0:
                    return None

                used_percent = (total - usage_count) / total * 100
                return f"\n\nMinimax已使用：{used_percent:.2f}%"

    except Exception:
        return None
