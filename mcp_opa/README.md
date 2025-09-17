# Proof of Concept: MCP Tool Blocking with OPA (Direct Client-MCP Calls)

## 🎯 Objective

This project demonstrates how to restrict access to specific **tools** of an MCP server using **Open Policy Agent (OPA)** as a policy engine.

Unlike the previous approach with a proxy, the **MCP server** itself queries OPA directly to determine whether a client request should be allowed or denied.

---

## 🚀 Getting Started

To start the environment with MCP and OPA:

```bash
docker compose up --build
```

This will start:

* MCP server
* OPA with the defined policy

The MCP client runs from the **host** (outside Docker) using commands defined in `pyproject.toml`:

```bash
poe question_allowed
poe question_not_allowed
```

---

## 🛠️ Implementation

* **MCP server** with two tools:

  * `last_concept`: retrieves the latest recorded concept.
  * `add_concept`: adds a new concept and expense.
* MCP server queries **OPA** for each client request before executing any tool.
* If OPA allows → the server executes the tool and returns the result.
* If OPA denies → the server returns a 403 error to the client.

---

## 🏗️ Architecture

```mermaid
graph LR
    Client[MCP Client]
    MCP[MCP Server<br/>- last_concept<br/>- add_concept]
    OPA[Open Policy Agent]

    Client --> MCP
    MCP --> OPA
    OPA --> MCP
```

---

## ⚙️ Workflow

1. MCP client requests a tool.
2. MCP server receives the request and queries OPA.
3. OPA responds **allowed** or **denied**.
4. If **allowed**, MCP executes the tool and returns the result.
5. If **denied**, MCP returns a 403 error.

---

## 📌 Usage Example

* Tool `add_concept` → blocked by OPA policy.
* Tool `last_concept` → allowed.

The client can only execute tools permitted by the policy.

---

## 🔐 OPA Policies

Example policy (`policies/policy.rego`):

```rego
package mcp

import rego.v1

default allow := true

allow := false if {
  input.name == "add_concept"
}
```

➡️ With this policy, **only** `add_concept` is denied. All others are allowed by default.

---

## ✅ Results

### Case 1: Allowed tool

```bash
❯ poe question_allowed
...
The last concept is: (server response)
```

### Case 2: Denied tool

```bash
❯ poe question_not_allowed
httpx.HTTPStatusError: Client error '403 Forbidden'
```

---

## 📊 Flow Diagrams

### Allowed tool

```mermaid
sequenceDiagram
  participant Client
  participant MCP
  participant OPA

  Client->>MCP: Request tool
  MCP->>OPA: Check policy
  OPA-->>MCP: Allowed
  MCP-->>Client: Result
```

### Denied tool

```mermaid
sequenceDiagram
  participant Client
  participant MCP
  participant OPA

  Client->>MCP: Request tool
  MCP->>OPA: Check policy
  OPA-->>MCP: Denied
  MCP-->>Client: Error 403
```

---

## 📚 References

* [Open Policy Agent](https://www.openpolicyagent.org/)
* [Model Context Protocol (MCP)](https://github.com/modelcontext/modelcontext-protocol)
