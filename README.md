# MCP Security POCs 🚨

Exploring the **security boundaries** of Anthropic's **Model Context Protocol (MCP)**.
This repository hosts **POCs, experiments, and research** around prompt injection, context leaks, authentication, OPA policies, and other MCP edge cases. All experiments are **educational, safe, and performed in controlled environments**.

---

## 📖 Table of Contents

* [POCs](#pocs)
* [Tools Used](#tools-used)
* [Disclaimer](#disclaimer)
* [License](#license)

---

## 🧪 POCs

Here are some of the experiments included in this repository:

| Name                     | Description                                                           | Link                                          |
| ------------------------ | --------------------------------------------------------------------- | --------------------------------------------- |
| Prompt Leak Banktools    | Demonstrates potential context leakage scenarios                      | [View README](./mcp_leak_banktools/README.md) |
| OPA Tool Blocking Proxy  | Fine-grained MCP tool access control using an OPA policy-driven proxy | [View README](./mcp_opa_proxy/README.md)      |
| OPA Tool Blocking Direct | Restricting MCP tool access using OPA policies without a proxy        | [View README](./mcp_opa/README.md)            |

*More POCs will be added over time…*

---

## 🛠️ Tools Used

This repository leverages the following tools and technologies:

* [**Python**](https://www.python.org/): Scripting and automation of experiments.
* [**Docker**](https://www.docker.com/): Containerization of test environments.
* [**Ollama**](https://ollama.com/): Running and managing local LLMs for testing.
* [**Docker Compose**](https://docs.docker.com/compose/): Orchestrating multi-container environments for complex scenarios.
* [**poethepoet**](https://github.com/nat-n/poethepoet): Task runner for automating scripts and workflows.
* [**uv**](https://github.com/astral-sh/uv): Fast Python package manager for dependencies and virtual environments.
* [**Open Policy Agent (OPA)**](https://www.openpolicyagent.org/): Policy engine used to enforce rules and access control in MCP experiments.

---

## ⚠️ Disclaimer

These experiments are intended **for educational and research purposes only**. Do not use them to attack or exploit live systems.

---

## 📄 License

This project is licensed under the [Apache License 2.0](LICENSE).
