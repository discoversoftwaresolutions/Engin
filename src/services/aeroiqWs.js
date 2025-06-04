const WebSocket = require("ws");

const API_BASE_URL = "wss://enginuity-production.up.railway.app/aeroiq";

/**
 * Sends a JSON command to an AeroIQ WebSocket endpoint and receives the response.
 * @param {string} uri - WebSocket URI (e.g., "wss://yourserver.com/ws/aeroiq")
 * @param {object} payload - Command payload to send
 * @param {number} timeout - Timeout in milliseconds (default: 10,000 ms)
 * @returns {Promise<object>} - Decoded response from the server
 */
async function sendAeroIQCommand(uri, payload, timeout = 10000) {
    return new Promise((resolve, reject) => {
        const ws = new WebSocket(uri);

        ws.on("open", () => {
            console.log(`🔗 Connected to WebSocket: ${uri}`);
            console.log(`📤 Sending payload:`, payload);
            ws.send(JSON.stringify(payload));
        });

        ws.on("message", (data) => {
            console.log(`📥 Received response:`, data);
            try {
                resolve(JSON.parse(data));
            } catch (error) {
                reject({ error: "Invalid JSON response" });
            }
            ws.close();
        });

        ws.on("error", (error) => {
            console.error("❌ WebSocket error:", error);
            reject({ error: error.message });
        });

        ws.on("close", () => {
            console.log("🔌 WebSocket connection closed.");
        });

        setTimeout(() => {
            reject({ error: "⏱ Timeout while waiting for server response" });
            ws.close();
        }, timeout);
    });
}

// ✅ Example Usage
(async () => {
    try {
        const result = await sendAeroIQCommand(API_BASE_URL, { command: "start_sim" });
        console.log("✅ WebSocket Response:", result);
    } catch (error) {
        console.error("❌ WebSocket Error:", error);
    }
})();
