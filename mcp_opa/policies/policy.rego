package mcp

import rego.v1

default allow := true

allow := false if {
  input.name == "add_concept"
}
