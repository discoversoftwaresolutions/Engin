// fusionx.js

// ✅ Environment-agnostic HTTP client using fetch
// Works in Node.js (via `node-fetch`) and modern browsers

const FUSIONX_BASE_URL = process.env.FUSIONX_API_URL || 'https://api.discoversoftwaresolutions.com/fusionx';

/**
 * Send a task request to FusionX
 * @param {string} userId - Unique user ID or session identifier
 * @param {string} task - Natural language or structured task request
 * @param {object} [context={}] - Optional context for the agent
 * @returns {Promise<object>} - Response from FusionX
 */
async function sendFusionXTask(userId, task, context = {}) {
  try {
    const response = await fetch(`${FUSIONX_BASE_URL}/task`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-User-ID': userId,
      },
      body: JSON.stringify({
        task,
        context,
      }),
    });

    if (!response.ok) {
      throw new Error(`FusionX API error: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('⚠️ FusionX Request Failed:', error.message);
    throw error;
  }
}

/**
 * Retrieve task history for auditing or UI rendering
 * @param {string} userId
 * @returns {Promise<object[]>}
 */
async function getFusionXTaskHistory(userId) {
  try {
    const response = await fetch(`${FUSIONX_BASE_URL}/history/${userId}`, {
      headers: {
        'Content-Type': 'application/json',
        'X-User-ID': userId,
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch history: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('⚠️ FusionX History Error:', error.message);
    throw error;
  }
}

// ✅ Export functions for use in front-end or back-end
module.exports = {
  sendFusionXTask,
  getFusionXTaskHistory,
};
