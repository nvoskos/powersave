# 🚀 PowerSave Deployment Guide

## 📦 Quick Deploy Options

### Option 1: GitHub Pages (RECOMMENDED ⭐⭐⭐)

**Deploy Time:** 2 minutes  
**Cost:** FREE  
**URL:** `https://nvoskos.github.io/powersave/`

#### Steps:

1. **Push latest changes:**
   ```bash
   cd /path/to/powersave
   git push origin main
   ```

2. **Enable GitHub Pages:**
   - Go to: https://github.com/nvoskos/powersave/settings/pages
   - Under "Source", select: `main` branch
   - Select folder: `/ (root)`
   - Click **Save**

3. **Wait 1-2 minutes** for deployment

4. **Your live URLs:**
   ```
   Main Site: https://nvoskos.github.io/powersave/
   Tools Hub: https://nvoskos.github.io/powersave/tools/
   Dashboard: https://nvoskos.github.io/powersave/dashboard.html
   ```

#### Tool Direct Links:
```
MindMap Agent:     https://nvoskos.github.io/powersave/tools/mindmap-agent-genspark.html
Knowledge Crawler: https://nvoskos.github.io/powersave/tools/setup-crawler.html
PDF Form Builder:  https://nvoskos.github.io/powersave/tools/chatbot-genspark.html
OCR & Translation: https://nvoskos.github.io/powersave/tools/ocr-translator-genspark.html
```

---

### Option 2: Netlify (Alternative ⭐⭐)

**Deploy Time:** 3 minutes  
**Cost:** FREE  
**URL:** `https://powersave.netlify.app` (or custom)

#### Steps:

1. **Push to GitHub first:**
   ```bash
   git push origin main
   ```

2. **Deploy via Netlify:**
   - Go to: https://app.netlify.com/
   - Click "Add new site" → "Import an existing project"
   - Choose "GitHub" and select `nvoskos/powersave`
   - Build settings:
     - Build command: (leave empty)
     - Publish directory: `/`
   - Click "Deploy site"

3. **Your site will be live at:**
   ```
   https://[random-name].netlify.app
   ```

4. **Optional: Custom domain:**
   - Go to Site settings → Domain management
   - Add custom domain (e.g., `powersave.netlify.app`)

---

### Option 3: Vercel (Alternative ⭐)

**Deploy Time:** 3 minutes  
**Cost:** FREE  
**URL:** `https://powersave.vercel.app`

#### Steps:

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Deploy:**
   ```bash
   cd /path/to/powersave
   vercel --prod
   ```

3. **Follow the prompts** and your site will be live!

---

## 🔑 Post-Deployment Checklist

After deploying, test all tools with GenSpark API key:

### API Key Format:
```
gsk-eyJjb2dlbl9pZCI6ICIyYjhjY2E4Ny03YzJjLTRhNDMtOWEzMC03ZjA2NzcxYWQwYWUiLCAia2V5X2lkIjogIjU0NzA2OTc1LTU3ZTctNDllOS05ZTU0LTNkY2JiNWM2ZDQ0MiJ9fFEp-1p1MyDUh_StQuOSM4530mHDXxfECbzca5ZkPYHD
```

### Test Each Tool:

1. ✅ **MindMap Agent** - Create a mindmap via AI
2. ✅ **Knowledge Crawler** - Extract data from a URL
3. ✅ **PDF Form Builder** - Build a form and export PDF
4. ✅ **OCR & Translation** - Upload an image and translate
5. ✅ **Main Dashboard** - Check energy savings dashboard

---

## 🌐 Custom Domain Setup (Optional)

### For GitHub Pages:

1. **Buy a domain** (e.g., `powersave.cy` from GoDaddy/Namecheap)

2. **Add CNAME record:**
   ```
   Type: CNAME
   Host: www
   Value: nvoskos.github.io
   ```

3. **Add A records:**
   ```
   Type: A
   Host: @
   Value: 185.199.108.153
   Value: 185.199.109.153
   Value: 185.199.110.153
   Value: 185.199.111.153
   ```

4. **In GitHub repo settings:**
   - Go to Settings → Pages
   - Add custom domain: `powersave.cy`
   - Enable HTTPS

---

## 🔄 Continuous Deployment

Once GitHub Pages is enabled:

1. **Make changes locally:**
   ```bash
   git add .
   git commit -m "Update feature X"
   git push origin main
   ```

2. **GitHub Pages auto-deploys** in 1-2 minutes! 🎉

---

## 🛠 Troubleshooting

### Issue: "Site not loading"
- Wait 2-3 minutes after enabling GitHub Pages
- Check build status: https://github.com/nvoskos/powersave/actions

### Issue: "404 Not Found"
- Ensure you selected `/ (root)` folder, not `/docs`
- Check that `index.html` exists in repo root

### Issue: "API Key not working"
- Use correct format: `gsk-` (hyphen, not underscore)
- Check browser console for errors

### Issue: "Tools not loading"
- Verify all files are in `/tools` directory
- Check CORS settings if calling external APIs

---

## 📊 Deployment Status

| Component | Status | URL |
|-----------|--------|-----|
| Main Site | ⏳ Pending | TBD |
| Tools Hub | ⏳ Pending | TBD |
| Dashboard | ⏳ Pending | TBD |
| API Config | ✅ Ready | N/A |

---

## 🎯 Next Steps After Deployment

1. **Share URLs** with stakeholders
2. **Test all 5 AI tools** with real users
3. **Monitor usage** via GitHub insights
4. **Gather feedback** and iterate
5. **Add Google Analytics** (optional)

---

## 📞 Support

For deployment issues:
- GitHub Pages Docs: https://docs.github.com/en/pages
- Netlify Docs: https://docs.netlify.com/
- Repository: https://github.com/nvoskos/powersave

---

**Ready to deploy? Follow Option 1 (GitHub Pages) for the fastest result!** 🚀
