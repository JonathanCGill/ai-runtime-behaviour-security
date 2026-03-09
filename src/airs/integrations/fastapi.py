"""FastAPI middleware for AIRS security pipeline.

Drop-in middleware that wraps AI endpoints with the three-layer
security architecture. Handles input/output evaluation, circuit
breaking, and PACE state management.

Usage:
    from fastapi import FastAPI
    from airs.integrations.fastapi import AIRSMiddleware
    from airs.runtime import SecurityPipeline, GuardrailChain, RegexGuardrail

    app = FastAPI()
    pipeline = SecurityPipeline(
        guardrails=GuardrailChain([RegexGuardrail()]),
    )
    app.add_middleware(AIRSMiddleware, pipeline=pipeline)
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any, Callable

from airs.core.models import AIRequest, AIResponse, PipelineResult
from airs.runtime.pipeline import SecurityPipeline

logger = logging.getLogger(__name__)

try:
    from fastapi import Request, Response
    from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
    from starlette.responses import JSONResponse

    class AIRSMiddleware(BaseHTTPMiddleware):
        """FastAPI middleware that enforces AIRS security pipeline.

        Intercepts requests to protected AI endpoints, runs input through
        guardrails before the handler, and runs output through guardrails
        + judge after the handler.

        Args:
            app: The FastAPI application.
            pipeline: Configured SecurityPipeline instance.
            protected_paths: URL path prefixes to protect (default: ["/ai", "/chat", "/completion"]).
            input_field: JSON field name containing user input (default: "input").
            output_field: JSON field name containing AI output (default: "output").
        """

        def __init__(
            self,
            app: Any,
            pipeline: SecurityPipeline | None = None,
            protected_paths: list[str] | None = None,
            input_field: str = "input",
            output_field: str = "output",
        ) -> None:
            super().__init__(app)
            self.pipeline = pipeline or SecurityPipeline()
            self.protected_paths = protected_paths or ["/ai", "/chat", "/completion"]
            self.input_field = input_field
            self.output_field = output_field

        async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
        ) -> Response:
            # Only intercept protected paths
            if not any(request.url.path.startswith(p) for p in self.protected_paths):
                return await call_next(request)

            # Only intercept POST requests
            if request.method != "POST":
                return await call_next(request)

            start = time.monotonic()

            # Parse request body
            try:
                body = await request.json()
            except Exception:
                return await call_next(request)

            input_text = body.get(self.input_field, "")
            if not input_text:
                return await call_next(request)

            # Build AIRequest
            ai_request = AIRequest(
                input_text=input_text,
                user_id=request.headers.get("x-user-id", ""),
                session_id=request.headers.get("x-session-id", ""),
                metadata={"path": request.url.path, "method": request.method},
            )

            # Evaluate input
            input_result = await self.pipeline.evaluate_input(ai_request)

            if not input_result.allowed:
                logger.warning(
                    "AIRS blocked input: request_id=%s blocked_by=%s reason=%s",
                    ai_request.request_id,
                    input_result.blocked_by,
                    input_result.layer_results[-1].reason if input_result.layer_results else "",
                )
                return self._blocked_response(input_result)

            # Call the actual handler
            response = await call_next(request)

            # Read response body for output evaluation
            response_body = b""
            async for chunk in response.body_iterator:
                if isinstance(chunk, str):
                    response_body += chunk.encode()
                else:
                    response_body += chunk

            try:
                response_data = json.loads(response_body)
                output_text = response_data.get(self.output_field, "")
            except (json.JSONDecodeError, AttributeError):
                output_text = response_body.decode(errors="replace")

            if output_text:
                ai_response = AIResponse(
                    request_id=ai_request.request_id,
                    output_text=output_text,
                )
                output_result = await self.pipeline.evaluate_output(ai_request, ai_response)

                if not output_result.allowed:
                    logger.warning(
                        "AIRS blocked output: request_id=%s blocked_by=%s",
                        ai_request.request_id,
                        output_result.blocked_by,
                    )
                    return self._blocked_response(output_result)

            # Add AIRS headers to response
            headers = dict(response.headers)
            headers["x-airs-request-id"] = ai_request.request_id
            headers["x-airs-pace-state"] = self.pipeline.pace.state.value
            latency = (time.monotonic() - start) * 1000
            headers["x-airs-latency-ms"] = f"{latency:.1f}"

            return Response(
                content=response_body,
                status_code=response.status_code,
                headers=headers,
                media_type=response.media_type,
            )

        def _blocked_response(self, result: PipelineResult) -> JSONResponse:
            reason = ""
            if result.layer_results:
                reason = result.layer_results[-1].reason

            return JSONResponse(
                status_code=403,
                content={
                    "error": "blocked_by_security",
                    "request_id": result.request_id,
                    "blocked_by": result.blocked_by.value if result.blocked_by else "unknown",
                    "reason": reason,
                    "pace_state": result.pace_state.value,
                    "fallback": self.pipeline.config.fallback_response,
                },
                headers={
                    "x-airs-request-id": result.request_id,
                    "x-airs-blocked": "true",
                    "x-airs-pace-state": result.pace_state.value,
                },
            )

except ImportError:
    # FastAPI not installed — provide helpful error
    class AIRSMiddleware:  # type: ignore[no-redef]
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise ImportError(
                "AIRSMiddleware requires FastAPI. Install with: pip install airs[fastapi]"
            )
