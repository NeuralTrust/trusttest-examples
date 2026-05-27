"""Example testing sequential rate limiting behavior with HttpTarget."""

import asyncio
import time
from typing import List, Tuple

from trusttest.targets import Response
from trusttest.targets.http import HttpTarget, PayloadConfig


async def _shoot_requests(
    target: HttpTarget, message: str, num_requests: int
) -> Tuple[float, List[Response]]:
    """Fire multiple sequential requests and measure elapsed time.

    Args:
        target: Configured HttpTarget with a rate limit.
        message: Message to send for each request.
        num_requests: Number of sequential requests to send.

    Returns:
        A tuple of (elapsed_seconds, responses_list).
    """
    start: float = time.perf_counter()
    responses: List[Response] = []
    for _ in range(num_requests):
        response: Response = await target.async_respond(message)
        responses.append(response)
    end: float = time.perf_counter()
    return end - start, responses


def _expected_min_elapsed(num_requests: int, rate_limit: float) -> float:
    """Compute expected minimum elapsed time given seconds/request limit.

    For a limit of S seconds per request and N sequential requests, at least
    (N - 1) * S seconds are required by the client-side rate limiter.
    """
    return max(0.0, float((num_requests - 1) * rate_limit))


def main() -> None:
    """Run a quick check to verify client-side rate limiting behavior."""
    rate_limit: float = 5  # 0.2 seconds per request (5 requests per second)
    num_requests: int = 20
    message: str = "Hello, how are you?"

    target: HttpTarget = HttpTarget(
        url="https://example.com/api/chat",
        headers={
            "Content-Type": "application/json",
        },
        payload_config=PayloadConfig(
            format={"message": "{{ test }}"},
            rate_limit=rate_limit,
        ),
        concatenate_field="response",
    )

    elapsed: float
    responses: List[Response]
    elapsed, responses = asyncio.run(_shoot_requests(target, message, num_requests))

    expected_min: float = _expected_min_elapsed(num_requests, rate_limit)
    passed: bool = elapsed >= expected_min

    print("Rate limit check")
    print(f"- rate_limit: {rate_limit}s per request")
    print(f"- num_requests: {num_requests}")
    print(f"- expected_min_elapsed: {expected_min:.3f}s")
    print(f"- measured_elapsed: {elapsed:.3f}s")
    print(f"- PASSED: {passed}")

    # Optionally display truncated responses for sanity
    for i, r in enumerate(responses, 1):
        snippet: str = (r.response or "").replace("\n", " ")[:80]
        print(f"  [{i}] {snippet}")


if __name__ == "__main__":
    main()
