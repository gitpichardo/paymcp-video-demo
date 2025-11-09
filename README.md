# PayMCP Video Generation Demo

A demonstration of PayMCP integration with Luma AI for paid video generation, compatible with **Claude Desktop**, **ChatGPT Developer Mode**, and other MCP clients.

## Features

- 💰 **Payment integration** using PayMCP with Walleot
- 🎥 **AI video generation** using Luma AI Dream Machine
- 🔄 **TWO_STEP payment mode** - payment before execution
- 🔗 **URL-based delivery** - returns video download links
- 🌐 **HTTP-based MCP server** - secure hosted deployment
- 🔌 **Multi-client support** - Works with Claude Desktop and ChatGPT
- 🚀 **Railway deployment** - One-click deployment to production

## Architecture

This demo supports **two deployment patterns**:

### For Claude Desktop (Local Proxy)
```
Claude Desktop (STDIO)
    ↓
Local Proxy (proxy.ts) - No API keys
    ↓ HTTP
Hosted PayMCP Server (server.py) - Has API keys
    ↓
Payment & Video Generation
```

### For ChatGPT / Other MCP Clients (Direct HTTP)
```
ChatGPT Developer Mode (HTTP)
    ↓
Hosted PayMCP Server (server.py) - Has API keys
    ↓
Payment & Video Generation
```

**Why this architecture?**
- 🔒 **Security** - API keys stay on the hosted server only
- 🖥️ **Claude Desktop** - Uses local proxy in STDIO mode
- 💬 **ChatGPT** - Connects directly to HTTP server
- 🌐 **Flexible** - Works with any MCP client

## Prerequisites

- **Python 3.10+** (for PayMCP server)
- **Node.js 18+** (for local proxy)
- API Keys:
  - [Walleot API Key](https://walleot.com/developers)
  - [Luma AI API Key](https://lumalabs.ai/dream-machine/api/keys)

## Installation

### Part 1: Setup PayMCP Server (Hosted)

#### 1. Install Python Dependencies

```bash
cd paymcp-video-demo
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 2. Configure Environment Variables

Create a `.env` file:

```bash
# Video Provider
VIDEO_PROVIDER=luma
LUMA_API_KEY=your_luma_api_key_here

# Payment Provider
WALLEOT_API_KEY=your_walleot_api_key_here

# Optional Settings
PAYMCP_MODE=TWO_STEP
PRICE_USD=0.60
```

#### 3. Start the Server

```bash
python server.py
```

The server will start on `http://localhost:8000`.

**For production:** Deploy to a cloud platform (Railway, Fly.io, AWS, etc.) and note your server URL.

### Part 2: Setup Local Proxy (for Claude Desktop)

#### 1. Install Node.js Dependencies

```bash
npm install
```

#### 2. Build the Proxy

```bash
npm run build
```

This compiles `proxy.ts` to `proxy.js`.

#### 3. Configure Claude Desktop

Edit your Claude Desktop configuration:

**Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Add this configuration:

```json
{
  "mcpServers": {
    "paymcp-video-demo": {
      "command": "node",
      "args": ["/absolute/path/to/paymcp-video-demo/proxy.js"],
      "env": {
        "PAYMCP_SERVER_URL": "http://localhost:8000"
      }
    }
  }
}
```

**For production:** Change `PAYMCP_SERVER_URL` to your deployed server URL.

#### 4. Restart Claude Desktop

Completely quit and restart Claude Desktop.

## 🔒 Security Notice

**⚠️ API keys must NEVER be exposed to end users**

This demo uses a **proxy architecture** to maintain security:

- ✅ **Server** (`server.py`) - Hosted, contains API keys
- ✅ **Proxy** (`proxy.ts`) - Local, NO API keys, just forwards requests
- ❌ **Never run server in STDIO mode** with API keys in config

**Deployment models:**
- **Development:** Server on `localhost`, proxy connects locally
- **Production:** Server on cloud (Railway, Fly.io, AWS), proxy connects remotely
- **Team use:** Shared hosted server, each user runs their own proxy

## Usage

### In Claude Desktop

Simply ask Claude to generate a video:

```
"Generate a video of a sunset over the ocean"
```

The proxy will forward your request to the hosted PayMCP server.

### In ChatGPT Developer Mode

**Prerequisites:** Deploy your server first (see [DEPLOYMENT.md](DEPLOYMENT.md))

1. **Enable Developer Mode:**
   - Settings → Connectors → Advanced → Enable "Developer mode"

2. **Add your connector:**
   - Settings → Connectors → Add connector
   - **Name:** PayMCP Video Generator
   - **URL:** `https://your-server.railway.app/mcp`
   - **Protocol:** Streaming HTTP
   - **Authentication:** None

3. **Use in conversations:**
   - Select "Developer mode" from the model picker (⊕ menu)
   - Be explicit: "Use the PayMCP Video Generator connector to generate a video of a cat playing with yarn"
   - Tip: Add "Do not use any other tools" to avoid confusion

4. **Confirm payment:**
   - ChatGPT will show the tool call with payment link
   - Click to pay via Walleot
   - Confirm the `confirm_generate_payment` tool call
   - Wait for video generation (~1-3 minutes)

**Example prompt:**
```
Use the "PayMCP Video Generator" connector's "generate" tool to create 
a video of a sunset over mountains. Do not use built-in image generation.
```

### Payment Workflow (TWO_STEP Mode)

1. **Request video generation** - Client calls the `generate` tool
2. **Receive payment link** - You'll get a Walleot payment URL ($0.60)
3. **Complete payment** - Click the link and pay
4. **Confirm payment** - Use the `confirm_generate_payment` tool with the payment_id
5. **Video generation** - Luma AI generates your video (~1-3 minutes)
6. **Receive URL** - Get a download link for your generated video (valid 24 hours)

### Example Response

```json
{
  "message": "Video generated successfully!",
  "video_url": "https://storage.lumalabs.ai/dream_machine/...",
  "prompt": "a sunset over the ocean",
  "instructions": "Click the video_url to download or view your generated video"
}
```

The video URL is valid for 24 hours and can be downloaded directly.

## PayMCP Modes

This demo uses `TWO_STEP` mode by default. You can change modes by setting `PAYMCP_MODE`:

- `TWO_STEP` - Split into two tools: generate + confirm (default)
- `RESUBMIT` - Same tool called twice with payment_id
- `ELICITATION` - Inline payment prompt (requires client support)
- `PROGRESS` - Shows progress while polling for payment
- `DYNAMIC_TOOLS` - Dynamically shows/hides tools

See [PayMCP documentation](https://github.com/PayMCP/paymcp) for more details.

## Files

**Server (Python):**
- `server.py` - PayMCP server with payment and video generation
- `providers/luma_client.py` - Luma AI integration
- `requirements.txt` - Python dependencies

**Proxy (Node.js/TypeScript):**
- `proxy.ts` - Local STDIO proxy for Claude Desktop
- `package.json` - Node.js dependencies
- `tsconfig.json` - TypeScript configuration

**Configuration:**
- `.env` - Server environment variables (not committed)
- `.gitignore` - Excludes sensitive and generated files

## Troubleshooting

### "Could not connect to MCP server" (Claude Desktop)

**Check the proxy:**
1. Ensure `proxy.js` exists (run `npm run build`)
2. Check absolute path in Claude Desktop config is correct
3. Verify `PAYMCP_SERVER_URL` environment variable is set

**Check the server:**
1. Ensure the server is running: `python server.py`
2. Verify server is accessible at configured URL
3. Check server logs for errors

**Test the flow:**
```bash
# Terminal 1: Start server
python server.py

# Terminal 2: Test server directly
curl http://localhost:8000/

# Terminal 3: Restart Claude Desktop
```

### "Permission denied" errors

- Recreate the virtual environment: `rm -rf venv && python3 -m venv venv`
- Fix permissions: `chmod -R 755 venv`

### "404 Not Found" from Luma API

- Verify your Luma API key is valid
- Check you have credits/quota on your Luma account
- Visit [Luma API Keys](https://lumalabs.ai/dream-machine/api/keys)

### Video generation takes too long

- Video generation typically takes 1-3 minutes
- Check Luma AI dashboard for generation status
- Some MCP clients may have request timeouts - check client settings

## Dependencies

```
fastmcp>=2.13.0      # MCP server framework
paymcp>=0.4.3        # Payment integration
lumaai>=1.18.0       # Luma AI SDK
python-dotenv        # Environment variables
```

## Development

### Running the server

```bash
python server.py
# Server runs on http://localhost:8000
```

### Testing the API

You can test the MCP server using any HTTP client or MCP-compatible application that supports the HTTP transport.

## Contributing

This is a demonstration project for the PayMCP developer community. Feel free to:

- Report issues
- Submit pull requests
- Share improvements
- Create variants for other video providers

## Resources

- [PayMCP Documentation](https://github.com/PayMCP/paymcp)
- [Luma AI API Docs](https://lumalabs.ai/docs)
- [MCP Protocol](https://modelcontextprotocol.io)
- [Claude Desktop MCP Guide](https://docs.anthropic.com/claude/docs/mcp)

## License

MIT

## Support

For PayMCP questions: [PayMCP GitHub](https://github.com/PayMCP/paymcp)

For Luma AI questions: [Luma Labs](https://lumalabs.ai)

---

Built with ❤️ for the PayMCP community

