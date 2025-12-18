#!/bin/bash

# PowerSave Quick Deploy Script
# This script helps you deploy PowerSave to GitHub Pages

set -e

echo "🚀 PowerSave Deployment Script"
echo "================================"
echo ""

# Check if we're in the right directory
if [ ! -f "index.html" ]; then
    echo "❌ Error: Please run this script from the PowerSave root directory"
    exit 1
fi

# Check git status
echo "📊 Checking Git status..."
git status

echo ""
echo "🔍 Latest commits:"
git log --oneline -3

echo ""
echo "================================"
echo ""
echo "📦 Ready to deploy!"
echo ""
echo "Choose deployment option:"
echo "  1) Push to GitHub (required first step)"
echo "  2) View GitHub Pages setup instructions"
echo "  3) Deploy to Netlify"
echo "  4) Cancel"
echo ""

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🚀 Pushing to GitHub..."
        git push origin main
        echo ""
        echo "✅ Pushed to GitHub!"
        echo ""
        echo "📝 Next steps:"
        echo "   1. Go to: https://github.com/nvoskos/powersave/settings/pages"
        echo "   2. Under 'Source', select: main branch"
        echo "   3. Select folder: / (root)"
        echo "   4. Click 'Save'"
        echo "   5. Wait 1-2 minutes"
        echo "   6. Visit: https://nvoskos.github.io/powersave/"
        echo ""
        ;;
    2)
        echo ""
        echo "📖 GitHub Pages Setup Instructions:"
        echo ""
        echo "1. Go to: https://github.com/nvoskos/powersave/settings/pages"
        echo "2. Under 'Source', select: main branch"
        echo "3. Select folder: / (root)"
        echo "4. Click 'Save'"
        echo "5. Wait 1-2 minutes for deployment"
        echo ""
        echo "Your site will be live at:"
        echo "  🌐 https://nvoskos.github.io/powersave/"
        echo ""
        echo "Tool URLs:"
        echo "  🧠 MindMap Agent:     https://nvoskos.github.io/powersave/tools/mindmap-agent-genspark.html"
        echo "  🌐 Knowledge Crawler: https://nvoskos.github.io/powersave/tools/setup-crawler.html"
        echo "  📄 PDF Form Builder:  https://nvoskos.github.io/powersave/tools/chatbot-genspark.html"
        echo "  🔤 OCR & Translation: https://nvoskos.github.io/powersave/tools/ocr-translator-genspark.html"
        echo ""
        ;;
    3)
        echo ""
        echo "🌐 Deploying to Netlify..."
        echo ""
        if ! command -v netlify &> /dev/null; then
            echo "📦 Installing Netlify CLI..."
            npm install -g netlify-cli
        fi
        echo "🚀 Deploying..."
        netlify deploy --prod
        echo ""
        echo "✅ Deployed to Netlify!"
        echo ""
        ;;
    4)
        echo "❌ Deployment cancelled"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment process complete!"
echo ""
echo "📋 Post-Deployment Checklist:"
echo "  ✅ Test all 5 AI tools"
echo "  ✅ Verify GenSpark API key format (gsk-...)"
echo "  ✅ Check mobile responsiveness"
echo "  ✅ Share URLs with team"
echo ""
echo "🔑 GenSpark API Key:"
echo "gsk-eyJjb2dlbl9pZCI6ICIyYjhjY2E4Ny03YzJjLTRhNDMtOWEzMC03ZjA2NzcxYWQwYWUiLCAia2V5X2lkIjogIjU0NzA2OTc1LTU3ZTctNDllOS05ZTU0LTNkY2JiNWM2ZDQ0MiJ9fFEp-1p1MyDUh_StQuOSM4530mHDXxfECbzca5ZkPYHD"
echo ""
echo "📖 Full deployment guide: See DEPLOYMENT.md"
echo ""
