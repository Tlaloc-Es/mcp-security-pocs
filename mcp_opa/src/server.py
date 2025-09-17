
import json
import logging
import os
import sqlite3

import httpx
from mcp.server.fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

logging.basicConfig(level=logging.INFO)
ON_DOCKER = os.getenv("RUNNING_IN_DOCKER", "true").lower() == "true"

mcp = FastMCP("Demo", host="0.0.0.0")


conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE bank_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    concept TEXT NOT NULL,
    expense REAL NOT NULL
)
""")
conn.commit()

examples = [
    ("Groceries", 120.50),
    ("Rent", 950.00),
    ("Utilities", 75.20),
    ("Dining Out", 45.30),
    ("Transportation", 60.00)
]

cursor.executemany(
    "INSERT INTO bank_data (concept, expense) VALUES (?, ?)",
    examples
)
conn.commit()

@mcp.tool()
async def last_concept() -> str:
    """Get the last concept from the bank_data table."""
    cursor.execute("SELECT concept FROM bank_data ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    if result:
        return f"The last concept is: {result[0]}"
    else:
        return "No concepts found."

@mcp.tool()
async def add_concept(concept: str, expense: float) -> str:
    """Add a new concept and expense to the bank_data table."""
    cursor.execute(
        "INSERT INTO bank_data (concept, expense) VALUES (?, ?)",
        (concept, expense)
    )
    conn.commit()
    logging.info(f"Added concept: {concept} with expense: {expense}")
    return f"Added concept '{concept}' with expense {expense:.2f}."

app = mcp.streamable_http_app()

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

