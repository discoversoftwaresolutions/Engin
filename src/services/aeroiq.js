// ✅ Import necessary modules
import { fetchData } from "../utils/apiClient";  // Ensure API client handles backend requests

const API_BASE_URL = "https://enginuity-production.up.railway.app";

// 🔥 Function to fetch supersonic boom calculations
export async function getWavefronts(mach, altitude_ft) {
    return await fetchData(`${API_BASE_URL}/wavefronts`, "POST", { mach, altitude_ft });
}

// 🛰 Function to compute orbital mechanics
export async function getOrbit(semiMajorAxis, eccentricity, inclination) {
    return await fetchData(`${API_BASE_URL}/orbit`, "POST", { semiMajorAxis, eccentricity, inclination });
}

// ♻️ Function to compute Hohmann Transfer
export async function getHohmannTransfer(initialRadius, targetRadius) {
    return await fetchData(`${API_BASE_URL}/hohmann-transfer`, "POST", { r1_km: initialRadius, r2_km: targetRadius });
}
export async function getWavefronts(mach, altitude_ft) {
    try {
        const response = await fetchData(`${API_BASE_URL}/wavefronts`, "POST", { mach, altitude_ft });
        return response;
    } catch (error) {
        console.error("Error fetching wavefronts:", error);
        return { error: "Failed to fetch wavefront data" };
    }
}
