#!/bin/bash

# Instala Chromium y ChromeDriver
apt-get update && apt-get install -y chromium chromium-driver

# Instala dependencias de Python
pip install -r requirements.txt
