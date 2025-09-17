
import json
import logging
import os

import httpx
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

ON_DOCKER = os.getenv("RUNNING_IN_DOCKER", "true").lower() == "true"

app = FastAPI()

MCP_SERVER_URL = "http://127.0.0.1:8000"
OPA_URL = "http://127.0.0.1:8181/v1/data/mcp"
if ON_DOCKER:
    MCP_SERVER_URL = "http://mcp:8000"
    OPA_URL = "http://opa:8181/v1/data/mcp"


async def check_policy(name: str):
    """Checks with OPA if the action is allowed"""
    payload = {"input": {"name": name}}
    logging.info(f"Consultando OPA con payload: {payload}")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(OPA_URL, json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("result", {}).get("allow", False)
    except httpx.RequestError as e:
        logging.error(f"Network error while querying OPA: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error while querying OPA: {e}")
        return False

@app.middleware("http")
async def opa_middleware(request: Request, call_next):
    logging.info(f"Incoming request: {request.method} {request.url}")
    body = None
    name = None
    if request.method == "POST":
        try:
            body_bytes = await request.body()
            if body_bytes:
                body = json.loads(body_bytes)
        except Exception as e:
            logging.warning(f"Could not parse body: {e}")
            body = None
        if body:
            name = body.get("params", {}).get("name")
    logging.info(f"Request body: {body}")
    allowed = await check_policy(name)
    logging.info(f"OPA policy check for name '{name}': {allowed}")
    if not allowed:
        logging.warning(f"Access denied by OPA for name '{name}'")
        return JSONResponse(status_code=403, content={"detail": "Access denied by OPA"})
    return await call_next(request)

def filter_headers(headers):
    # Elimina headers que FastAPI no permite reenviar
    excluded = {"content-length", "transfer-encoding", "connection"}
    return {k: v for k, v in headers.items() if k.lower() not in excluded}


@app.api_route("/mcp", methods=["POST", "GET"])
async def proxy_streamable_http(request: Request):
    if request.method == "POST":
        try:
            body = await request.body()
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(f"{MCP_SERVER_URL}/mcp", content=body, headers=filter_headers(request.headers))
                logging.info(f"Proxied POST /mcp with status {resp.status_code}")
                return Response(content=resp.content, status_code=resp.status_code, headers=filter_headers(resp.headers))
        except httpx.RequestError as e:
            logging.error(f"Network error while proxying /mcp: {e}")
            return JSONResponse(status_code=502, content={"detail": "Network error while contacting MCP"})
    else:
        return Response(content="Method Not Allowed", status_code=405)
