# PowerSave AI Tools - OpenAI Setup Guide

## ✅ Complete OpenAI Integration

PowerSave AI Tools now support **standard OpenAI API** (no GenSpark required)!

---

## 🚀 Quick Start (3 Steps)

### Step 1: Get Your OpenAI API Key

1. Go to: **https://platform.openai.com/api-keys**
2. Click "Create new secret key"
3. Copy your API key (starts with `sk-proj-...` or `sk-...`)

### Step 2: Configure the Proxy Server

```bash
cd /path/to/powersave

# Create .env file from template
cp .env.example .env

# Edit .env and add your API key
nano .env
```

Update these lines in `.env`:

```bash
# Replace with your actual OpenAI API key
OPENAI_API_KEY=sk-proj-your-key-here

# Use standard OpenAI API
OPENAI_BASE_URL=https://api.openai.com/v1

# Default model (gpt-3.5-turbo is fastest and cheapest)
OPENAI_MODEL=gpt-3.5-turbo
```

### Step 3: Start the Proxy Server

```bash
# Install dependencies (first time only)
pip install -r requirements-ai-proxy.txt

# Start the proxy server
python ai_proxy_server.py
```

You should see:

```
============================================================
🚀 PowerSave AI Proxy Server
============================================================
📡 API Base URL: https://api.openai.com/v1
🔑 API Key: sk-proj-...
🌐 Server Port: 8080
============================================================

✅ Server starting on http://localhost:8080
📖 API Docs: http://localhost:8080/docs
```

---

## 🎯 Test Your Setup

Open your browser and test any tool:

- **Chatbot**: `http://localhost:8765/powersave/tools/chatbot-genspark.html`
- **MindMap Agent**: `http://localhost:8765/powersave/tools/mindmap-agent-genspark.html`
- **OCR Translator**: `http://localhost:8765/powersave/tools/ocr-translator-genspark.html`
- **Knowledge Crawler**: `http://localhost:8765/powersave/tools/knowledge-crawler-genspark.html`
- **PDF Form Builder**: `http://localhost:8765/powersave/tools/pdf-form-builder-genspark.html`

All tools will now use **your OpenAI API key** through the proxy!

---

## 🔧 Advanced Configuration

### Available Models

Edit `OPENAI_MODEL` in `.env` to use different models:

| Model | Speed | Cost | Best For |
|-------|-------|------|----------|
| `gpt-3.5-turbo` | ⚡ Fast | 💰 Cheap | General tasks, chat |
| `gpt-4` | 🐢 Slow | 💰💰💰 Expensive | Complex reasoning |
| `gpt-4-turbo` | 🚀 Fast | 💰💰 Medium | Best balance |

### Alternative: Use GenSpark (Optional)

If you still want to use GenSpark instead of OpenAI:

1. Get GenSpark API key from: **https://www.genspark.ai/settings**
2. Edit `.env`:

```bash
# Use GenSpark instead
OPENAI_API_KEY=gsk-your-genspark-key-here
OPENAI_BASE_URL=https://www.genspark.ai/api/llm_proxy/v1
OPENAI_MODEL=gpt-5-mini
```

---

## 📊 Architecture

```
Browser (AI Tools)
      ↓
Proxy Server (localhost:8080)
      ↓
OpenAI API (api.openai.com/v1)
```

**Why use a proxy?**

- ✅ Bypasses CORS restrictions
- ✅ Secures API key (not exposed in browser)
- ✅ Works with all 5 AI tools
- ✅ Easy configuration

---

## ❌ Troubleshooting

### Issue: "Cannot connect to AI proxy server"

**Solution:** Make sure the proxy server is running:

```bash
python ai_proxy_server.py
```

### Issue: "OpenAI API error: 401 Unauthorized"

**Solution:** Check your API key in `.env`:

```bash
cat .env | grep OPENAI_API_KEY
```

Make sure it starts with `sk-` and is valid.

### Issue: "Model not found"

**Solution:** OpenAI models available:
- ✅ `gpt-3.5-turbo`
- ✅ `gpt-4`
- ✅ `gpt-4-turbo`

GenSpark models (if using GenSpark):
- ✅ `gpt-5-mini`
- ✅ `gpt-5`
- ✅ `gpt-5-nano`

### Issue: Tools still not working

**Checklist:**

1. ✅ Proxy server running? (`python ai_proxy_server.py`)
2. ✅ API key valid? (Check on OpenAI dashboard)
3. ✅ `.env` file configured? (`cat .env`)
4. ✅ Port 8080 available? (Not blocked by firewall)

---

## 💰 Cost Estimation

Using OpenAI API:

| Model | Cost (per 1M tokens) | Typical Request Cost |
|-------|---------------------|---------------------|
| `gpt-3.5-turbo` | $0.50 input / $1.50 output | ~$0.001 |
| `gpt-4` | $30 input / $60 output | ~$0.05 |
| `gpt-4-turbo` | $10 input / $30 output | ~$0.02 |

**Example:** 100 chat messages with gpt-3.5-turbo ≈ $0.10

Get $5 free credits when you sign up at OpenAI!

---

## 📦 What's Included

- **ai_proxy_server.py** - Backend proxy server
- **tools/ai-config.js** - Unified AI configuration
- **.env.example** - Configuration template
- **requirements-ai-proxy.txt** - Python dependencies
- **OPENAI_SETUP.md** - This guide

---

## 🆘 Need Help?

1. Check proxy logs: `python ai_proxy_server.py` (see error messages)
2. Test API connection: Open `http://localhost:8080/health`
3. View API docs: Open `http://localhost:8080/docs`

---

## ✅ Success!

Once the proxy is running, **all 5 AI tools** will work automatically with your OpenAI API key!

No more GenSpark, no more CORS issues, no more Cloudflare problems! 🎉
