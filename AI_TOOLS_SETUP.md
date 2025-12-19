# 🧠 PowerSave AI Tools Setup Guide

## 🎯 Problem: CORS & API Access

Browser-based AI tools cannot directly call GenSpark API due to:
- **CORS restrictions** (Cross-Origin Resource Sharing)
- **Cloudflare protection** blocking direct requests

## ✅ Solution: Backend Proxy Server

We created a simple FastAPI proxy server that:
- ✅ Runs locally on your machine
- ✅ Handles API authentication
- ✅ Bypasses CORS restrictions
- ✅ Works with all AI tools

---

## 🚀 Quick Start (2 Minutes)

### Step 1: Install Dependencies

```bash
cd /path/to/powersave

# Install Python dependencies
pip install -r requirements-ai-proxy.txt
```

### Step 2: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and set your GenSpark API key
# OPENAI_API_KEY=gsk-your-actual-key-here
```

Or use the current working key:
```bash
echo 'OPENAI_API_KEY=gsk-eyJjb2dlbl9pZCI6ICIyYjhjY2E4Ny03YzJjLTRhNDMtOWEzMC03ZjA2NzcxYWQwYWUiLCAia2V5X2lkIjogIjk2NDg4ZWRlLTEzOGYtNDE4Yy05NGVhLThkZjUxNmZkZTBhOSJ9fGu39u0z0M7qd-AbN5e7qZYXn2FRNkekLHwvDbwani-c' >> .env
echo 'OPENAI_BASE_URL=https://www.genspark.ai/api/llm_proxy/v1' >> .env
```

### Step 3: Start the Proxy Server

```bash
python ai_proxy_server.py
```

You should see:
```
============================================================
🚀 PowerSave AI Proxy Server
============================================================
📡 API Base URL: https://www.genspark.ai/api/llm_proxy/v1
🔑 API Key: gsk-eyJjb2dlbl9pZCI...
🌐 Server Port: 8080
🔓 CORS Origins: *
============================================================

✅ Server starting on http://localhost:8080
📖 API Docs: http://localhost:8080/docs
🏥 Health Check: http://localhost:8080/health
💬 Chat Endpoint: http://localhost:8080/api/ai/chat
```

### Step 4: Test the Connection

Open another terminal:

```bash
# Test health endpoint
curl http://localhost:8080/health

# Test AI endpoint
curl -X POST http://localhost:8080/api/ai/test
```

### Step 5: Open AI Tools

Now you can use any AI tool:

```
🧠 MindMap Agent:     http://localhost:8765/powersave/tools/mindmap-agent-genspark.html
📄 PDF Form Builder:  http://localhost:8765/powersave/tools/chatbot-genspark.html
🔤 OCR & Translation: http://localhost:8765/powersave/tools/ocr-translator-genspark.html
🌐 Knowledge Crawler: http://localhost:8765/powersave/tools/knowledge-crawler-genspark.html
```

**All tools will work without CORS issues!** 🎉

---

## 📚 Architecture

```
┌─────────────┐         ┌──────────────────┐         ┌─────────────┐
│   Browser   │────────▶│   AI Proxy       │────────▶│  GenSpark   │
│  (AI Tools) │         │  (Port 8080)     │         │  API        │
└─────────────┘         └──────────────────┘         └─────────────┘
     ✅ No CORS              ✅ Handles Auth             ✅ Real AI
```

---

## 🔧 Configuration

### Environment Variables

**`.env` file:**

```env
# Required
OPENAI_API_KEY=gsk-your-key-here
OPENAI_BASE_URL=https://www.genspark.ai/api/llm_proxy/v1

# Optional
OPENAI_MODEL=gpt-5-mini
AI_PROXY_PORT=8080
AI_PROXY_CORS_ORIGINS=*
```

### Tool Configuration

**`tools/ai-config.js`:**

```javascript
const AI_CONFIG = {
    mode: 'proxy',  // Use 'proxy' mode when server is running
    
    proxy: {
        endpoint: 'http://localhost:8080/api/ai/chat',
        model: 'gpt-5-mini'
    }
};
```

---

## 🧪 Testing

### 1. Test Proxy Server Directly

```bash
# Health check
curl http://localhost:8080/health

# Response:
{
  "status": "healthy",
  "api_configured": true,
  "base_url": "https://www.genspark.ai/api/llm_proxy/v1"
}
```

### 2. Test Chat Endpoint

```bash
curl -X POST http://localhost:8080/api/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-5-mini",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ],
    "max_tokens": 50
  }'
```

### 3. Test from Browser Console

Open any tool and run in console:

```javascript
// Test AI connection
fetch('http://localhost:8080/api/ai/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        model: 'gpt-5-mini',
        messages: [{role: 'user', content: 'Hello!'}],
        max_tokens: 50
    })
})
.then(r => r.json())
.then(d => console.log('✅ AI Response:', d))
.catch(e => console.error('❌ Error:', e));
```

---

## 🐳 Docker Deployment (Optional)

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements-ai-proxy.txt .
RUN pip install -r requirements-ai-proxy.txt

COPY ai_proxy_server.py .
COPY .env .

EXPOSE 8080

CMD ["python", "ai_proxy_server.py"]
```

### Build & Run

```bash
docker build -t powersave-ai-proxy .
docker run -p 8080:8080 --env-file .env powersave-ai-proxy
```

---

## 🔒 Security Notes

### ✅ Good Practices

1. **Never expose API key in frontend code**
   - ✅ Store in backend `.env` file
   - ✅ Access via proxy server
   
2. **Use environment variables**
   - ✅ `.env` for development
   - ✅ System env vars for production
   
3. **Restrict CORS origins in production**
   ```env
   AI_PROXY_CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
   ```

### ❌ Bad Practices

- ❌ Hardcoding API keys in HTML/JS files
- ❌ Committing `.env` to git
- ❌ Using `CORS_ORIGINS=*` in production
- ❌ Exposing proxy server to public internet

---

## 🆘 Troubleshooting

### Problem: "Cannot connect to proxy server"

**Solution:** Make sure `ai_proxy_server.py` is running

```bash
python ai_proxy_server.py
```

### Problem: "API key not configured"

**Solution:** Set `OPENAI_API_KEY` in `.env`

```bash
echo 'OPENAI_API_KEY=gsk-your-key' >> .env
```

### Problem: "CORS error"

**Solution:** Proxy server should handle CORS. Check:
1. Server is running on port 8080
2. Tool is configured to use proxy mode
3. CORS middleware is enabled in `ai_proxy_server.py`

### Problem: "Port 8080 already in use"

**Solution:** Change the port

```bash
# In .env
AI_PROXY_PORT=8081
```

Then update `tools/ai-config.js`:
```javascript
proxy: {
    endpoint: 'http://localhost:8081/api/ai/chat',
    ...
}
```

---

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Server info |
| `/health` | GET | Health check |
| `/api/ai/chat` | POST | Chat completion (main endpoint) |
| `/api/ai/models` | GET | List available models |
| `/api/ai/test` | POST | Test API connection |
| `/docs` | GET | Interactive API documentation |

---

## 🎯 Production Deployment

### Option 1: systemd Service (Linux)

Create `/etc/systemd/system/powersave-ai-proxy.service`:

```ini
[Unit]
Description=PowerSave AI Proxy Server
After=network.target

[Service]
Type=simple
User=powersave
WorkingDirectory=/opt/powersave
EnvironmentFile=/opt/powersave/.env
ExecStart=/usr/bin/python3 /opt/powersave/ai_proxy_server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable powersave-ai-proxy
sudo systemctl start powersave-ai-proxy
sudo systemctl status powersave-ai-proxy
```

### Option 2: Supervisor

```ini
[program:powersave-ai-proxy]
command=/usr/bin/python3 ai_proxy_server.py
directory=/opt/powersave
autostart=true
autorestart=true
user=powersave
environment=OPENAI_API_KEY="gsk-...",OPENAI_BASE_URL="https://..."
```

### Option 3: Docker Compose

```yaml
version: '3.8'

services:
  ai-proxy:
    build: .
    ports:
      - "8080:8080"
    env_file:
      - .env
    restart: unless-stopped
```

---

## 📝 Summary

| Component | Purpose | Status |
|-----------|---------|--------|
| `ai_proxy_server.py` | Backend API proxy | ✅ Created |
| `requirements-ai-proxy.txt` | Python dependencies | ✅ Created |
| `.env.example` | Configuration template | ✅ Updated |
| `tools/ai-config.js` | Frontend config | ✅ Created |
| `AI_TOOLS_SETUP.md` | This guide | ✅ Created |

---

**Next Steps:**
1. Run `python ai_proxy_server.py`
2. Open any AI tool
3. Start creating! 🚀

**Need help?** Check the troubleshooting section or open an issue on GitHub.
