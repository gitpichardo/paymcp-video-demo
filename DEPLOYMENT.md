# Deployment Guide

This guide covers deploying your PayMCP video generation server to Railway for use with Claude Desktop, ChatGPT, and other MCP clients.

## Why Deploy?

- **ChatGPT compatibility** - ChatGPT Developer Mode requires remote HTTP servers
- **Share with others** - Anyone can use your server without exposing API keys
- **Persistent URL** - Stable endpoint that doesn't change
- **Free tier** - Railway offers a generous free tier

## Railway Deployment (Recommended)

### Prerequisites

- Railway account: [Sign up](https://railway.app/)
- Luma AI API key: [Get key](https://lumalabs.ai/dream-machine/api/keys)
- Walleot API key: [Get key](https://walleot.com/developers)

### Option 1: Deploy via Railway CLI

1. **Login to Railway:**
   ```bash
   railway login
   ```

2. **Initialize project:**
   ```bash
   cd /path/to/paymcp-video-demo
   railway init
   ```

3. **Set environment variables:**
   ```bash
   railway variables set VIDEO_PROVIDER=luma
   railway variables set LUMA_API_KEY=your_luma_api_key
   railway variables set WALLEOT_API_KEY=your_walleot_api_key
   railway variables set PAYMCP_MODE=TWO_STEP
   railway variables set PRICE_USD=0.60
   ```

4. **Deploy:**
   ```bash
   railway up
   ```

5. **Get your URL:**
   ```bash
   railway domain
   ```

### Option 2: Deploy via Railway Dashboard

1. **Create new project:**
   - Go to [Railway Dashboard](https://railway.app/dashboard)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your `paymcp-video-demo` repository

2. **Configure environment variables:**
   - In your Railway project, go to "Variables"
   - Add these variables:
     ```
     VIDEO_PROVIDER=luma
     LUMA_API_KEY=your_luma_api_key
     WALLEOT_API_KEY=your_walleot_api_key
     PAYMCP_MODE=TWO_STEP
     PRICE_USD=0.60
     ```

3. **Generate domain:**
   - Go to "Settings" → "Domains"
   - Click "Generate Domain"
   - Copy your URL (e.g., `https://paymcp-video-demo-production.up.railway.app`)

4. **Verify deployment:**
   - Visit `https://your-domain.railway.app/`
   - You should see: "MCP Video Generator is running"

## Using Your Deployed Server

### With Claude Desktop (via Proxy)

Update `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "paymcp-video-demo": {
      "command": "node",
      "args": ["/path/to/paymcp-video-demo/proxy.js"],
      "env": {
        "PAYMCP_SERVER_URL": "https://your-domain.railway.app"
      }
    }
  }
}
```

### With ChatGPT Developer Mode

1. **Enable Developer Mode:**
   - Settings → Connectors → Advanced → Enable "Developer mode"

2. **Add connector:**
   - Settings → Connectors → Add connector
   - **Name:** PayMCP Video Generator
   - **URL:** `https://your-domain.railway.app/mcp`
   - **Protocol:** Streaming HTTP
   - **Authentication:** None

3. **Use in conversations:**
   - Select "Developer mode" from model picker
   - Ask: "Use the PayMCP Video Generator to create a video of a cat playing with yarn"

### With Other MCP Clients

Most MCP clients support HTTP transport. Use:
- **Endpoint:** `https://your-domain.railway.app/mcp`
- **Protocol:** Streamable HTTP

## Monitoring & Logs

### View logs:
```bash
railway logs
```

### Check status:
```bash
railway status
```

### Redeploy:
```bash
railway up
```

## Cost & Limits

**Railway Free Tier:**
- $5 of usage per month
- Perfect for demo/testing
- Automatically sleeps after inactivity

**Usage Costs:**
- **Luma AI:** ~$0.10-0.20 per video (your cost)
- **Your price:** $0.60 per video (user pays)
- **Profit margin:** $0.40-0.50 per video

## Security Best Practices

✅ **DO:**
- Keep API keys in Railway environment variables
- Use HTTPS URLs only
- Monitor usage and costs
- Set rate limits if needed

❌ **DON'T:**
- Commit API keys to GitHub
- Share your Railway admin access
- Expose raw API endpoints without PayMCP

## Troubleshooting

### Server won't start
- Check Railway logs: `railway logs`
- Verify environment variables are set
- Ensure `requirements.txt` is up to date

### ChatGPT can't connect
- Verify URL ends with `/mcp`
- Check server is running: visit your domain
- Ensure Streaming HTTP is selected

### Payment not working
- Verify Walleot API key is correct
- Check Walleot dashboard for payment status
- Ensure `PAYMCP_MODE=TWO_STEP` is set

## Alternative Deployment Platforms

### Fly.io
```bash
fly launch
fly secrets set LUMA_API_KEY=...
fly secrets set WALLEOT_API_KEY=...
fly deploy
```

### Render
- Connect GitHub repo
- Set environment variables in dashboard
- Deploy from main branch

### AWS/GCP/Azure
- Deploy as a containerized app
- Use managed Python runtime
- Set environment variables in platform

## Next Steps

- Add authentication for production use
- Implement rate limiting
- Add monitoring/analytics
- Support multiple payment providers
- Add video customization options

---

Need help? [Open an issue](https://github.com/yourusername/paymcp-video-demo/issues)

