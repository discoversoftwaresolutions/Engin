package com.enginuity.codemotion;

import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;
import org.json.JSONObject;

import java.util.Map;

@RestController
@RequestMapping("/codemotion")
public class CodeMotionController {

    private static final String API_BASE_URL = "https://enginuity-production.up.railway.app";
    private final RestTemplate restTemplate = new RestTemplate();

    // 🛠 Handle File Upload
    @PostMapping("/upload")
    public ResponseEntity<String> handleFileUpload(@RequestParam("file") MultipartFile file) {
        if (file.isEmpty()) {
            return ResponseEntity.badRequest().body("⚠️ No file uploaded.");
        }
        return ResponseEntity.ok("✅ File uploaded: " + file.getOriginalFilename());
    }

    // 🔥 Execute Firmware, ROS2 Composition, or Behavior Simulation Task
    @PostMapping("/execute-task")
    public ResponseEntity<String> executeTask(@RequestParam String taskEndpoint,
                                              @RequestParam String filename,
                                              @RequestParam String platform) {
        try {
            JSONObject payload = new JSONObject();
            payload.put("filename", filename);
            payload.put("platform", platform);

            HttpHeaders headers = new HttpHeaders();
            headers.set("Content-Type", "application/json");

            HttpEntity<String> requestEntity = new HttpEntity<>(payload.toString(), headers);
            ResponseEntity<String> response = restTemplate.exchange(API_BASE_URL + "/" + taskEndpoint, HttpMethod.POST, requestEntity, String.class);

            return ResponseEntity.status(response.getStatusCode()).body(response.getBody());
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("🚨 API Request Failed: " + e.getMessage());
        }
    }

    // 🎯 Get Available Platforms (ESP32, STM32, etc.)
    @GetMapping("/platforms")
    public ResponseEntity<Map<String, String[]>> getPlatforms() {
        return ResponseEntity.ok(Map.of(
            "availablePlatforms", new String[]{"ESP32", "STM32", "Arduino", "Raspberry Pi"}
        ));
    }

    // 📜 Toggle Simulation Logs
    @PostMapping("/toggle-simulation-logs")
    public ResponseEntity<String> toggleSimulationLogs(@RequestParam boolean enableLogs) {
        return ResponseEntity.ok("📜 Simulation Logs: " + (enableLogs ? "Enabled" : "Disabled"));
    }

    // 📊 Toggle Resource Metrics
    @PostMapping("/toggle-resource-metrics")
    public ResponseEntity<String> toggleResourceMetrics(@RequestParam boolean enableMetrics) {
        return ResponseEntity.ok("📊 Resource Metrics: " + (enableMetrics ? "Enabled" : "Disabled"));
    }
}
