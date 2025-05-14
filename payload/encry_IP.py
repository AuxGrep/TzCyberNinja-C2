import time
import sys
from colorama import Fore, Style

# now tutengeneze function ya kuencrypt any string with XOR
def xor_encrypt(input_str, key=0x81):
    return [ord(c) ^ key for c in input_str]

# Format byte array for C/C++ code with specified bytes per line
def format_byte_array(byte_array, bytes_per_line=10):
    lines = []
    for i in range(0, len(byte_array), bytes_per_line):
        line_bytes = byte_array[i:i+bytes_per_line]
        line = ', '.join(f'0x{b:02x}' for b in line_bytes)
        lines.append(line)
    return 'unsigned char ip_part[] = { ' + ',\n                         '.join(lines) + ' };'

# Split IP into parts unyama wa obfuscation
def split_ip(ip):
    parts = ip.split('.')
    return [
        f"{parts[0]}.",
        f"{parts[1]}.",
        f"{parts[2]}.",
        parts[3]
    ]

class IP_Obfuscator:
    @staticmethod
    def obfuscate_ip(ip, port):
        # Encrypt the whole IP
        try:
            encrypted_ip = xor_encrypt(ip)
            print(f"{Fore.GREEN}\n// Encrypted IP as single array:{Style.RESET_ALL}")
            print(format_byte_array(encrypted_ip))

            # Encrypt split IP (for additional obfuscation)
            ip_parts = split_ip(ip)
            print(f"{Fore.GREEN}\n// Encrypted IP split into parts:{Style.RESET_ALL}")
            for i, part in enumerate(ip_parts, 1):
                encrypted_part = xor_encrypt(part)
                print(f"unsigned char ip_part{i}[] = {{ {', '.join(f'0x{b:02x}' for b in encrypted_part)} }};")
            
            # Encrypt port string
            encrypted_port = xor_encrypt(port)
            print(f"{Fore.GREEN}\n// Encrypted port as string:{Style.RESET_ALL}")
            print(format_byte_array(encrypted_port))
            
            # Encrypt port as integer (for htons)
            port_int = int(port)
            encrypted_port_bytes = [(port_int >> 8) ^ 0x81, (port_int & 0xFF) ^ 0x81]
            print(f"{Fore.GREEN}\n// Encrypted port bytes (for htons):{Style.RESET_ALL}")
            print(f"unsigned char port_bytes[] = {{ 0x{encrypted_port_bytes[0]:02x}, 0x{encrypted_port_bytes[1]:02x} }};")
            
            # Generate example code for the main function
            print(f"{Fore.GREEN}\n// Example usage in main function:{Style.RESET_ALL}")
            print(f"""    // Replace this in your main function:
            char part1[] = {{ {', '.join(f'0x{ord(c):02x}' for c in ip_parts[0])} }};
            char part2[] = {{ {', '.join(f'0x{ord(c):02x}' for c in ip_parts[1])} }};
            char part3[] = {{ {', '.join(f'0x{ord(c):02x}' for c in ip_parts[2])} }};
            char part4[] = {{ {', '.join(f'0x{ord(c):02x}' for c in ip_parts[3])} }};
            
            host = (char*)malloc(strlen(part1) + strlen(part2) + strlen(part3) + strlen(part4));
            strcpy(host, part1);
            strcat(host, part2);
            strcat(host, part3);
            strcat(host, part4);
            
            port = {port};""")
        except Exception as e:
            return f'We have an error: {e}'
        