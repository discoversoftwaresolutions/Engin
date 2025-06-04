const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "https://enginuity-production.up.railway.app";

/**
 * Generic function to make API requests.
 * @param {string} endpoint - The API endpoint (e.g., "/wavefronts").
 * @param {string} method - The HTTP method (GET, POST, etc.).
 * @param {object} body - The request payload (optional).
 * @returns {Promise<object>} - The API response.
 */
export async function fetchData(endpoint, method = "GET", body = null) {
    try {
        const options = {
            method,
            headers: { "Content-Type": "application/json" }
        };

        if (body) options.body = JSON.stringify(body);

        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        if (!response.ok) throw new Error(`❌ API Error ${response.status}: ${await response.text()}`);

        return await response.json();
    } catch (error) {
        console.error("🚨 API Request Failed:", error);
        return { error: error.message };
    }
}
