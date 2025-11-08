#!/usr/bin/env node
/**
 * MCP Proxy Server for PayMCP
 * 
 * This proxy runs locally in STDIO mode (compatible with Claude Desktop)
 * and forwards requests to your hosted PayMCP server via HTTP.
 * 
 * This keeps your API keys secure on the server while maintaining
 * Claude Desktop compatibility.
 */

import * as readline from "readline";

const PAYMCP_URL = process.env.PAYMCP_SERVER_URL || "http://localhost:8000";
const MCP_ENDPOINT = `${PAYMCP_URL}/mcp`;

// Store session ID from the streamable HTTP transport
let sessionId: string | null = null;

// Log to stderr (stdout is for MCP protocol messages)
function log(message: string) {
  console.error(`[Proxy] ${message}`);
}

// Parse SSE response and extract the data
function parseSSE(text: string): any {
  const lines = text.split('\n');
  for (const line of lines) {
    if (line.startsWith('data: ')) {
      const data = line.substring(6);
      return JSON.parse(data);
    }
  }
  throw new Error('No data found in SSE response');
}

// Forward a single JSON-RPC message to the server
async function forwardMessage(message: any): Promise<any> {
  try {
    // Build headers with session ID if we have one
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      "Accept": "application/json, text/event-stream",
    };
    
    if (sessionId) {
      headers["mcp-session-id"] = sessionId;
    }
    
    const response = await fetch(MCP_ENDPOINT, {
      method: "POST",
      headers,
      body: JSON.stringify(message),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`HTTP ${response.status}: ${errorText}`);
    }

    // Check for session ID in response headers
    const newSessionId = response.headers.get('mcp-session-id');
    if (newSessionId && !sessionId) {
      sessionId = newSessionId;
      log(`Session established: ${sessionId.substring(0, 8)}...`);
    }

    const text = await response.text();
    return parseSSE(text);
  } catch (error) {
    log(`Error forwarding message: ${error}`);
    throw error;
  }
}

// Main proxy loop - read from stdin, forward to server, write to stdout
async function main() {
  log(`Starting proxy...`);
  log(`Connecting to: ${MCP_ENDPOINT}`);

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false,
  });

  rl.on("line", async (line) => {
    try {
      // Parse incoming JSON-RPC request
      const request = JSON.parse(line);
      log(`→ ${request.method || 'notification'} ${sessionId ? `(session: ${sessionId.substring(0, 8)}...)` : '(no session)'}`);

      // Forward to PayMCP server
      const response = await forwardMessage(request);
      log(`← Response`);

      // Write response to stdout
      console.log(JSON.stringify(response));
    } catch (error) {
      log(`Error: ${error}`);
      // Send error response
      const errorResponse = {
        jsonrpc: "2.0",
        id: null,
        error: {
          code: -32603,
          message: String(error),
        },
      };
      console.log(JSON.stringify(errorResponse));
    }
  });

  rl.on("close", () => {
    log("Proxy closed");
    process.exit(0);
  });

  log("Proxy ready");
}

main().catch((error) => {
  log(`Fatal error: ${error}`);
  process.exit(1);
});
