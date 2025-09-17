# MCP Security POCs 🚨

Exploring the security boundaries of **Anthropic's Model Context Protocol (MCP)**.  
This repository hosts **POCs, experiments, and research** around prompt injection, leaks, authentication, OPA policies, and other MCP edge cases.  
All experiments are **educational and safe**, performed in controlled environments.

---

## Table of Contents

- [POCs](#pocs)
- [Disclaimer](#disclaimer)
- [License](#license)

---

## POCs

Here are some of the experiments included in this repo:

| Name                    | Description                                       | Link                                          |
| ----------------------- | ------------------------------------------------- | --------------------------------------------- |
| Prompt Leak Banktools   | Demonstrating potential context leakage scenarios | [View README](./mcp_leak_banktools/README.md) |
| OPA Tool Blocking Proxy | Restricting MCP tool access using OPA policies    | [View README](./mcp_opa_proxy/README.md)      |

_(More POCs will be added over time…)_

---

## Tools Used

This repository leverages the following tools and technologies:

- [**Python**](https://www.python.org/): For scripting and automation of experiments.
- [**Docker**](https://www.docker.com/): Containerization of test environments.
- [**Ollama**](https://ollama.com/): Running and managing local LLMs for testing.
- [**Docker Compose**](https://docs.docker.com/compose/): Orchestrating multi-container environments for complex scenarios.
- [**poethepoet**](https://github.com/nat-n/poethepoet): Task runner for automating scripts and workflows.
- [**uv**](https://github.com/astral-sh/uv): Ultra-fast Python package manager for dependency management and virtual environments.

## Disclaimer

⚠️ These experiments are intended for educational and research purposes only. Do not use them to attack or exploit live systems.

## License

This project is licensed under the [Apache License 2.0](LICENSE).
