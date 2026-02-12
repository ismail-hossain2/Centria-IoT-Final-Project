#include <WiFi.h>
#include <PubSubClient.h>

// ===== WiFi for Wokwi =====
const char* WIFI_SSID = "Wokwi-GUEST";
const char* WIFI_PASS = "";

// ===== MQTT =====
// Public broker (works often). If it fails, switch to broker.hivemq.com
const char* MQTT_BROKER = "test.mosquitto.org";
const int   MQTT_PORT   = 1883;

// Make your topic unique:
const char* TOPIC_TEMP  = "centria/iot/ismail/temperature";

// ===== Pins =====
const int LED_PIN = 4;      // LED in your diagram
const int SENSOR_PIN = 34;  // Potentiometer SIG -> GPIO34 (ADC input)

// ===== Logic =====
float thresholdC = 28.0;
unsigned long lastSendMs = 0;
const unsigned long sendIntervalMs = 2000;

// ===== Clients =====
WiFiClient espClient;
PubSubClient mqtt(espClient);

void connectWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  Serial.print("Connecting WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(300);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
}

void connectMQTT() {
  mqtt.setServer(MQTT_BROKER, MQTT_PORT);

  Serial.print("Connecting MQTT");
  while (!mqtt.connected()) {
    // client id must be unique-ish
    String clientId = "esp32-ismail-" + String((uint32_t)ESP.getEfuseMac(), HEX);
    if (mqtt.connect(clientId.c_str())) {
      Serial.println("\nMQTT connected!");
    } else {
      Serial.print(".");
      delay(500);
    }
  }
}

float readTempC_fromPot() {
  // ADC on ESP32 returns 0..4095
  int raw = analogRead(SENSOR_PIN);

  // Map to 15..35 °C (nice range for demo)
  float tempC = 15.0 + (raw / 4095.0) * 20.0;
  return tempC;
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);

  connectWiFi();
  connectMQTT();
}

void loop() {
  if (!mqtt.connected()) connectMQTT();
  mqtt.loop();

  unsigned long now = millis();
  if (now - lastSendMs >= sendIntervalMs) {
    lastSendMs = now;

    float tempC = readTempC_fromPot();

    // Actuator logic: LED ON if temp > threshold
    digitalWrite(LED_PIN, (tempC > thresholdC) ? HIGH : LOW);

    // Publish JSON payload (nice for PC parsing)
    char payload[128];
    snprintf(payload, sizeof(payload),
             "{\"device\":\"esp32-wokwi\",\"tempC\":%.2f,\"thresholdC\":%.2f,\"ts_ms\":%lu}",
             tempC, thresholdC, now);

    mqtt.publish(TOPIC_TEMP, payload);

    Serial.print("Published: ");
    Serial.println(payload);
  }
}
