/**
 * GenSpark AI Configuration Helper
 * Automatically detects and configures API keys for all GenSpark tools
 */

class GenSparkConfig {
    constructor() {
        this.apiKey = null;
        this.endpoint = 'https://www.genspark.ai/api/llm_proxy/v1/chat/completions';
        this.model = 'gpt-5-mini';
        this.init();
    }

    init() {
        // Try to get API key from various sources
        this.apiKey = this.detectApiKey();
        
        if (this.apiKey) {
            console.log('✅ GenSpark API key detected and configured');
            this.saveToLocalStorage();
        } else {
            console.warn('⚠️ GenSpark API key not found');
        }
    }

    detectApiKey() {
        // 1. Check localStorage
        const localKey = localStorage.getItem('genspark_api_key');
        if (localKey && localKey.startsWith('gsk-')) {
            return localKey;
        }

        // 2. Check if running in special environment (sandbox)
        // Note: This won't work in browser, but shows the pattern
        try {
            // Check for meta tag with API key
            const metaTag = document.querySelector('meta[name="genspark-api-key"]');
            if (metaTag && metaTag.content) {
                return metaTag.content;
            }
        } catch (e) {
            // Ignore
        }

        // 3. Check URL parameters (for testing only - not secure for production!)
        const urlParams = new URLSearchParams(window.location.search);
        const urlKey = urlParams.get('api_key');
        if (urlKey && urlKey.startsWith('gsk-')) {
            return urlKey;
        }

        return null;
    }

    saveToLocalStorage() {
        if (this.apiKey) {
            localStorage.setItem('genspark_api_key', this.apiKey);
        }
    }

    promptForApiKey() {
        const key = prompt(
            '🔑 GenSpark API Key Required\n\n' +
            'Please enter your GenSpark API key (starts with gsk-...):\n\n' +
            'Get your key from: https://www.genspark.ai/settings\n\n' +
            'Your key will be saved locally for future use.'
        );

        if (key && key.trim().startsWith('gsk-')) {
            this.apiKey = key.trim();
            this.saveToLocalStorage();
            this.showNotification('API key saved successfully! ✅', 'success');
            return true;
        } else if (key) {
            this.showNotification('Invalid API key format. Must start with gsk-', 'error');
            return false;
        }
        return false;
    }

    async testApiKey() {
        if (!this.apiKey) {
            throw new Error('No API key configured');
        }

        try {
            const response = await fetch(this.endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.apiKey}`
                },
                body: JSON.stringify({
                    model: this.model,
                    messages: [
                        { role: 'user', content: 'Test message' }
                    ],
                    max_tokens: 5
                })
            });

            return response.ok;
        } catch (error) {
            console.error('API test failed:', error);
            return false;
        }
    }

    showNotification(message, type = 'info') {
        // Simple notification implementation
        const colors = {
            success: '#10b981',
            error: '#ef4444',
            warning: '#f59e0b',
            info: '#3b82f6'
        };

        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: ${colors[type]};
            color: white;
            padding: 16px 24px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            font-family: 'Inter', sans-serif;
            font-size: 14px;
            font-weight: 500;
            z-index: 10000;
            animation: slideIn 0.3s ease;
        `;
        notification.textContent = message;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateY(20px)';
            notification.style.transition = 'all 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    getConfig() {
        return {
            apiKey: this.apiKey,
            endpoint: this.endpoint,
            model: this.model
        };
    }

    isConfigured() {
        return !!this.apiKey;
    }
}

// Create global instance
window.genSparkConfig = new GenSparkConfig();

// Export for modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = GenSparkConfig;
}
