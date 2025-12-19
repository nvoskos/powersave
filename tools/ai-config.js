/**
 * PowerSave AI Tools Configuration
 * ================================
 * Unified configuration for all AI-powered tools.
 * 
 * This config supports two modes:
 * 1. Direct Mode: Tools call GenSpark API directly (CORS issues in browser)
 * 2. Proxy Mode: Tools call local backend proxy (RECOMMENDED)
 */

const AI_CONFIG = {
    // Mode: 'direct' or 'proxy'
    // Use 'proxy' when running with ai_proxy_server.py
    // Use 'direct' for standalone HTML files (may have CORS issues)
    mode: 'proxy',
    
    // Direct Mode Configuration (GenSpark API)
    direct: {
        endpoint: 'https://www.genspark.ai/api/llm_proxy/v1/chat/completions',
        // Note: API key should be provided by user or stored in localStorage
        apiKey: localStorage.getItem('gensparkApiKey') || '',
        model: 'gpt-5-mini'
    },
    
    // Proxy Mode Configuration (Local Backend)
    proxy: {
        endpoint: 'http://localhost:8080/api/ai/chat',
        // No API key needed - handled by backend
        apiKey: null,
        model: 'gpt-5-mini'
    },
    
    // Default AI parameters
    defaults: {
        temperature: 0.7,
        max_tokens: 2000,
        stream: false
    }
};

/**
 * Get the active configuration based on current mode
 */
function getAIConfig() {
    const config = AI_CONFIG.mode === 'proxy' ? AI_CONFIG.proxy : AI_CONFIG.direct;
    return {
        ...config,
        ...AI_CONFIG.defaults
    };
}

/**
 * Make an AI request using the configured mode
 * @param {Array} messages - Array of message objects {role, content}
 * @param {Object} options - Optional parameters (temperature, max_tokens, etc.)
 * @returns {Promise} Response from AI
 */
async function callAI(messages, options = {}) {
    const config = getAIConfig();
    
    const requestBody = {
        model: options.model || config.model,
        messages: messages,
        temperature: options.temperature || config.temperature,
        max_tokens: options.max_tokens || config.max_tokens,
        stream: options.stream || config.stream
    };
    
    const headers = {
        'Content-Type': 'application/json'
    };
    
    // Add Authorization header only in direct mode
    if (AI_CONFIG.mode === 'direct' && config.apiKey) {
        headers['Authorization'] = `Bearer ${config.apiKey}`;
    }
    
    try {
        const response = await fetch(config.endpoint, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(requestBody)
        });
        
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`AI API Error (${response.status}): ${errorText}`);
        }
        
        const data = await response.json();
        return data;
        
    } catch (error) {
        console.error('AI Request Error:', error);
        
        // Provide helpful error messages
        if (error.message.includes('Failed to fetch')) {
            if (AI_CONFIG.mode === 'proxy') {
                throw new Error(
                    'Cannot connect to AI proxy server. ' +
                    'Make sure ai_proxy_server.py is running on port 8080. ' +
                    'Run: python ai_proxy_server.py'
                );
            } else {
                throw new Error(
                    'Cannot connect to GenSpark API. ' +
                    'This might be a CORS issue. Consider using proxy mode instead.'
                );
            }
        }
        
        throw error;
    }
}

/**
 * Test the AI connection
 * @returns {Promise<boolean>} True if connection works
 */
async function testAIConnection() {
    try {
        const response = await callAI([
            { role: 'user', content: 'Hello!' }
        ], { max_tokens: 10 });
        
        return !!response.choices;
    } catch (error) {
        console.error('AI Connection Test Failed:', error);
        return false;
    }
}

/**
 * Switch between direct and proxy modes
 * @param {string} mode - 'direct' or 'proxy'
 */
function setAIMode(mode) {
    if (mode !== 'direct' && mode !== 'proxy') {
        throw new Error('Mode must be "direct" or "proxy"');
    }
    AI_CONFIG.mode = mode;
    console.log(`AI mode switched to: ${mode}`);
}

/**
 * Set API key for direct mode
 * @param {string} apiKey - GenSpark API key (gsk-...)
 */
function setAPIKey(apiKey) {
    if (!apiKey.startsWith('gsk-')) {
        throw new Error('Invalid API key format. Must start with gsk-');
    }
    AI_CONFIG.direct.apiKey = apiKey;
    localStorage.setItem('gensparkApiKey', apiKey);
    console.log('API key updated');
}

/**
 * Get current AI mode
 * @returns {string} Current mode ('direct' or 'proxy')
 */
function getAIMode() {
    return AI_CONFIG.mode;
}

// Auto-detect if proxy server is available
async function autoDetectMode() {
    try {
        const response = await fetch('http://localhost:8080/health', {
            method: 'GET',
            timeout: 2000
        });
        
        if (response.ok) {
            setAIMode('proxy');
            console.log('✅ AI Proxy server detected. Using proxy mode.');
            return 'proxy';
        }
    } catch (error) {
        // Proxy not available, keep current mode
        console.log('⚠️ AI Proxy server not detected. Using direct mode (may have CORS issues).');
    }
    return AI_CONFIG.mode;
}

// Export for use in tools
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        AI_CONFIG,
        getAIConfig,
        callAI,
        testAIConnection,
        setAIMode,
        setAPIKey,
        getAIMode,
        autoDetectMode
    };
}
