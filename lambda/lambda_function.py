"""
CloudAPI - AWS Lambda handler for an API Gateway HTTP API (payload format 2.0).

Routes:
  GET  /
  GET  /hello
  GET  /status
  POST /greet

Runtime: Python 3.12 (standard library only)
"""

import json
from datetime import datetime, timezone


def response(status_code, body):
    """Return an API Gateway Lambda proxy response."""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json; charset=utf-8",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
        },
        "body": json.dumps(body, ensure_ascii=False),
    }


def lambda_handler(event, context):
    """Route an API Gateway HTTP API request to the correct handler."""
    method = (
        event.get("requestContext", {})
        .get("http", {})
        .get("method", event.get("httpMethod", "GET"))
    )
    path = event.get("rawPath") or event.get("path") or "/"

    if method == "OPTIONS":
        return response(200, {"status": "success", "message": "CORS preflight accepted"})

    if method == "GET" and path == "/":
        return response(200, {
            "status": "success",
            "service": "CloudAPI",
            "description": "A serverless REST API powered by AWS Lambda and Amazon API Gateway.",
            "available_endpoints": [
                "GET /",
                "GET /hello",
                "GET /status",
                "POST /greet",
            ],
        })

    if method == "GET" and path == "/hello":
        return response(200, {
            "status": "success",
            "message": "Hello from AWS Lambda!",
        })

    if method == "GET" and path == "/status":
        return response(200, {
            "status": "success",
            "service": "CloudAPI",
            "health": "healthy",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        })

    if method == "POST" and path == "/greet":
        raw_body = event.get("body") or "{}"
        if event.get("isBase64Encoded"):
            return response(400, {
                "status": "error",
                "message": "Base64-encoded request bodies are not supported by this demo API.",
            })
        try:
            payload = json.loads(raw_body)
        except (json.JSONDecodeError, TypeError):
            return response(400, {
                "status": "error",
                "message": "Request body must contain valid JSON.",
            })

        if not isinstance(payload, dict):
            return response(400, {
                "status": "error",
                "message": "JSON request body must be an object.",
            })

        name = payload.get("name")
        if not isinstance(name, str) or not name.strip():
            return response(400, {
                "status": "error",
                "message": "The 'name' field is required and must be a non-empty string.",
            })

        safe_name = name.strip()[:80]
        return response(200, {
            "status": "success",
            "message": f"Hello, {safe_name}!",
            "service": "AWS Lambda",
            "architecture": "Serverless",
        })

    return response(404, {
        "status": "error",
        "message": f"Route not found: {method} {path}",
        "available_endpoints": ["GET /", "GET /hello", "GET /status", "POST /greet"],
    })
