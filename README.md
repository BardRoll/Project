# Setting on Raspberry Pi 3 Model B+
===
## Config ip address for WiFi
```bash
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```
```bash
network={
    ssid="WiFi name"
    psk="WiFi password"
}
```
If you have WiFi more than 1
```bash
network={
    ssid="WiFi name 1"
    psk="WiFi password 1"
    priority=1
}

network={
    ssid="WiFi name 2"
    psk="WiFi password 2"
    priority=2
}
```
---
## Create virtual environment and install libraries for this project
Create virtual environment
```bash
python -m venv venv
```
Start virtual environment
```bash
source venv/bin/activate
```
Install libraries
```bash
pip install django
pip install launchpad
pip install launchpad_py
pip install pygame
```