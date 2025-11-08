# PayMCP Video Generation Demo

A demonstration of PayMCP integration with Luma AI for paid video generation through Claude Desktop.

## Features

- 💰 **Payment integration** using PayMCP with Walleot
- 🎥 **AI video generation** using Luma AI Dream Machine
- 🔄 **TWO_STEP payment mode** - payment before execution
- 📁 **Auto-save** videos to Downloads folder
- 🤖 **MCP integration** for Claude Desktop

## Prerequisites

- Python 3.10 or higher
- Claude Desktop
- API Keys:
  - [Walleot API Key](https://walleot.com/developers)
  - [Luma AI API Key](https://lumalabs.ai/dream-machine/api/keys)

## Installation

### 1. Clone and Setup

```bash
cd paymcp-video-demo
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file (or set environment variables):

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

### 3. Configure Claude Desktop

Edit your Claude Desktop configuration file:

**Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Add this configuration:

```json
{
  "mcpServers": {
    "paymcp-video-demo": {
      "command": "/absolute/path/to/venv/bin/python",
      "args": [
        "/absolute/path/to/server.py"
      ],
      "env": {
        "VIDEO_PROVIDER": "luma",
        "PRICE_USD": "0.60",
        "PAYMCP_MODE": "TWO_STEP",
        "WALLEOT_API_KEY": "your_walleot_api_key_here",
        "LUMA_API_KEY": "your_luma_api_key_here"
      }
    }
  }
}
```

**Important:** Replace `/absolute/path/to/` with your actual paths!

### 4. Restart Claude Desktop

Completely quit and restart Claude Desktop for it to pick up the new MCP server.

## Usage

### In Claude Desktop

Simply ask Claude to generate a video:

```
"Generate a video of a sunset over the ocean"
```

### Payment Workflow (TWO_STEP Mode)

1. **Request video generation** - Claude calls the `generate` tool
2. **Receive payment link** - You'll get a Walleot payment URL ($0.60)
3. **Complete payment** - Click the link and pay
4. **Confirm payment** - Tell Claude "I paid" or "Payment completed"
5. **Video generation** - Luma AI generates your video (~1-3 minutes)
6. **Download** - Video is automatically saved to your Downloads folder

### Example Response

```
Video generated successfully!
File path: /Users/you/Downloads/video_a1b2c3d4.mp4
File size: 5.23 MB
```

## PayMCP Modes

This demo uses `TWO_STEP` mode by default. You can change modes by setting `PAYMCP_MODE`:

- `TWO_STEP` - Split into two tools: generate + confirm (default)
- `RESUBMIT` - Same tool called twice with payment_id
- `ELICITATION` - Inline payment prompt (requires client support)
- `PROGRESS` - Shows progress while polling for payment
- `DYNAMIC_TOOLS` - Dynamically shows/hides tools

See [PayMCP documentation](https://github.com/PayMCP/paymcp) for more details.

## Architecture

```
Claude Desktop
    ↓
MCP Server (server.py)
    ↓
PayMCP (payment handling)
    ↓
Walleot (payment processing)
    ↓
Luma AI (video generation)
    ↓
Downloads folder (saved video)
```

## Files

- `server.py` - Main MCP server with PayMCP integration
- `providers/luma_client.py` - Luma AI video generation client
- `requirements.txt` - Python dependencies
- `.gitignore` - Excludes sensitive files

## Troubleshooting

### "Could not connect to MCP server"

- Check that all paths in `claude_desktop_config.json` are absolute
- Verify Python virtual environment path is correct
- Check Claude Desktop logs: `~/Library/Logs/Claude/mcp.log`

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
- Claude Desktop may timeout after 5 minutes

## Dependencies

```
fastmcp>=2.13.0      # MCP server framework
paymcp>=0.4.3        # Payment integration
lumaai>=1.18.0       # Luma AI SDK
aiohttp              # HTTP client
python-dotenv        # Environment variables
```

## Development

### Running in HTTP mode (for testing)

```bash
python server.py
# Server runs on http://localhost:8000
```

### Running in STDIO mode (for Claude Desktop)

```bash
echo '{"jsonrpc":"2.0","method":"initialize",...}' | python server.py
```

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

