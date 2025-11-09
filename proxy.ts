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

  // Handle uncaught errors
  process.on('uncaughtException', (error) => {
    log(`Uncaught exception: ${error}`);
    process.exit(1);
  });

  process.on('unhandledRejection', (reason) => {
    log(`Unhandled rejection: ${reason}`);
    process.exit(1);
  });

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false,
  });

  rl.on("line", async (line) => {
    let requestId: string | number | undefined = undefined;
    
    try {
      // Skip empty lines
      if (!line || line.trim() === '') {
        return;
      }
      
      // Parse incoming JSON-RPC request
      const request = JSON.parse(line);
      
      // Extract ID - must be string or number (not null)
      if (request.id !== undefined && request.id !== null) {
        requestId = request.id;
      }
      
      log(`→ ${request.method || 'notification'} (id: ${requestId ?? 'none'}) ${sessionId ? `(session: ${sessionId.substring(0, 8)}...)` : '(no session)'}`);

      // Forward to PayMCP server
      const response = await forwardMessage(request);
      log(`← Response (id: ${response.id ?? 'none'})`);

      // Write response to stdout (only if it's valid)
      if (response && typeof response === 'object') {
        console.log(JSON.stringify(response));
      } else {
        log(`Warning: Invalid response from server: ${response}`);
      }
    } catch (error) {
      log(`Error processing request: ${error}`);
      
      // Only send error response if this was a request (has an id)
      // Notifications (no id) should not receive responses
      if (requestId !== undefined) {
        const errorResponse = {
          jsonrpc: "2.0",
          id: requestId,
          error: {
            code: -32603,
            message: error instanceof Error ? error.message : String(error),
          },
        };
        console.log(JSON.stringify(errorResponse));
      } else {
        log("Notification failed - no error response sent");
      }
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
