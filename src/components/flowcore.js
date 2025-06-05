package com.enginuity.flowcore;

import org.springframework.web.bind.annotation.*;
import org.springframework.http.*;
import org.springframework.web.client.RestTemplate;
import org.json.JSONObject;

import java.time.Instant;
import java.util.Map;
import java.util.logging.Logger;

@RestController
@RequestMapping("/flowcore")
public class FlowCoreController {

    private static final String API_BASE_URL = "https://enginuity-production.up.railway.app";
    private final RestTemplate restTemplate = new RestTemplate();
    private static final Logger logger = Logger.getLogger(FlowCoreController.class.getName());

    // 🧭 Get Available FlowCore Tasks
    @GetMapping("/tasks")
    public ResponseEntity<Map<String, String>> getTaskOptions() {
        Map<String, String> taskOptions = Map.of(
            "Sync Digital Twin State", "Synchronize the digital twin with real-world telemetry data.",
            "Track Engineering Changes", "Audit and version control your model state transitions.",
            "Validate Compliance Rules", "Run your twin against real-time or simulated compliance constraints."
        );
        return ResponseEntity.ok(taskOptions);
    }

    // 📌 Execute FlowCore Task
    @PostMapping("/execute-task")
    public ResponseEntity<String> executeTask(@RequestBody Map<String, String> payload) {
        String task = payload.get("task");
        String description = payload.get("description");

        if (task == null || description == null) {
            return ResponseEntity.badRequest().body("Missing 'task' or 'description' in request.");
        }

        String timestamp = Instant.now().toString();
        logger.info("[FlowCore] Task: " + task + " | Description: " + description + " | Timestamp: " + timestamp);

        JSONObject requestBody = new JSONObject();
        requestBody.put("task", task);
        requestBody.put("description", description);
        requestBody.put("timestamp", timestamp);

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        HttpEntity<String> requestEntity = new HttpEntity<>(requestBody.toString(), headers);

        try {
            ResponseEntity<String> response = restTemplate.exchange(
                API_BASE_URL + "/execute-task",
                HttpMethod.POST,
                requestEntity,
                String.class
            );

            if (response.getStatusCode().is2xxSuccessful()) {
                logger.info("✅ FlowCore task executed successfully.");
                return ResponseEntity.ok(response.getBody());
            } else {
                logger.warning("⚠️ FlowCore API error: " + response.getStatusCode());
                return ResponseEntity.status(response.getStatusCode()).body(response.getBody());
            }
        } catch (Exception e) {
            logger.severe("🚨 API request failed: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("API Request Failed: " + e.getMessage());
        }
    }
}
