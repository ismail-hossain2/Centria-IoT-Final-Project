# Centria IoT Final Project  
## Smart Temperature Monitoring System (ESP32 + MQTT + Database + Visualization)

Author: Md. Ismail Hossain  
Course: IT00AL54-3006 Internet of Things  
Institution: Centria University of Applied Sciences  
Year: 2026  

---

## 📌 Project Overview

This project demonstrates a complete Internet of Things (IoT) pipeline using an ESP32 microcontroller in Wokwi simulation.

The system simulates a smart temperature monitoring device that:

• Reads sensor data  
• Controls an actuator based on threshold  
• Sends data over the network (MQTT)  
• Stores data in a database  
• Visualizes sensor data as a live time-series graph  

This project fulfills the final project requirements for:
- Sensor + Actuator
- Communication
- Database storage
- Data visualization

---

## 🏗️ System Architecture

Sensor (Potentiometer)  
        ↓  
ESP32 (Wokwi Simulation)  
        ↓ MQTT  
Public MQTT Broker  
        ↓  
Python Application (PC)  
        ↓  
SQLite Database  
        ↓  
Live Data Visualization (Matplotlib)

---

## 🔧 Hardware (Simulated in Wokwi)

Board: ESP32 DevKit v4  
Sensor: Potentiometer (simulated temperature sensor)  
Actuator: LED  

The potentiometer simulates a temperature range between 15°C and 35°C.

If temperature > 28°C → LED turns ON  
If temperature ≤ 28°C → LED turns OFF  

---

## 🌐 Communication

Protocol: MQTT  
Broker: test.mosquitto.org  
Topic: centria/iot/ismail/temperature  

The ESP32 publishes sensor data in JSON format:

```json
{
  "device": "esp32-wokwi",
  "tempC": 27.52,
  "thresholdC": 28.0,
  "ts_ms": 123456
}
