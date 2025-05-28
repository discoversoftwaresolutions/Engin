import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "https://enginuity-backend.railway.app/api/v1",
  headers: {
    "Content-Type": "application/json"
  }
});

export const runAgentTask = async (module: string, payload: any) => {
  return api.post(`/task/${module}`, payload);
};
