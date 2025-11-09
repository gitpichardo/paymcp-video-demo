#!/usr/bin/env python3
import inspect
from fastmcp import FastMCP

print("FastMCP.run signature:")
print(inspect.signature(FastMCP.run))
print("\nFastMCP.run source:")
print(inspect.getsource(FastMCP.run))

