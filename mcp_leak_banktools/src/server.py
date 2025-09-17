import logging
import sqlite3

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Bank Tools MCP")

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

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    mcp.run(transport="streamable-http")