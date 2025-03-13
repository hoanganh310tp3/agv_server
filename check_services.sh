#!/bin/bash

echo "Checking network connectivity..."

echo "Checking DNS resolution for mosquitto..."
nslookup mosquitto

echo "Checking MQTT port..."
nc -zv mosquitto 1883

echo "Checking PostgreSQL..."
nc -zv db 5432

echo "Checking Redis..."
nc -zv redis 6379 