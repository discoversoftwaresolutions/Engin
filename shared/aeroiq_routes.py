AEROIQ_BACKEND_URL = "http://localhost:8000/api/v1/aeroiq"

ROUTES = {
    "run_task": f"{AEROIQ_BACKEND_URL}/run",
    "validate_design": f"{AEROIQ_BACKEND_URL}/validate",
    "generate_report": f"{AEROIQ_BACKEND_URL}/report",
}
