import time
import sys
import os
import time
import subprocess
from colorama import Fore, Style 

class Payload:
    @staticmethod
    def payload_build(payload, out):
        try:
            if os.path.exists(payload):
                print(f"{Fore.GREEN}[*] Payload file found: {payload}{Style.RESET_ALL}")
                time.sleep(2)
                cmd = subprocess.run(
                    ['x86_64-w64-mingw32-gcc', '-m64', payload, '-o', out],
                    check=True,
                    capture_output=True,
                    text=True
                )
                if cmd.returncode == 0:
                    print(f"{Fore.GREEN}Successful build the payload!!{Style.RESET_ALL}")
                    time.sleep(2)
                    print(f"{Fore.GREEN}[+] Payload saved as {os.getcwd()}/{out}{Style.RESET_ALL}")
                else:
                    sys.exit(f"{Fore.RED}[-] Compiler exited with a non-zero status{Style.RESET_ALL}")
            else:
                sys.exit(f"{Fore.RED}[-] Payload source file does not exist{Style.RESET_ALL}") 
                
        except subprocess.CalledProcessError as e:
            sys.exit(f"{Fore.RED}[-] Compilation failed. {e}{Style.RESET_ALL}") 
        except Exception as e:
            sys.exit(f"{Fore.RED}[!] Unexpected error: {e}{Style.RESET_ALL}") 

class SilentDE:
    @staticmethod
    def Silent(payload, out):
        try:
            if os.path.exists(payload):
                print(f"{Fore.GREEN}[*] Payload file found: {payload}{Style.RESET_ALL}")
                time.sleep(2)
                cmd = subprocess.run(
                    ['x86_64-w64-mingw32-gcc', payload, '-o', out, '-lwininet', '-mwindows'],
                    check=True,
                    capture_output=True,
                    text=True
                )
                if cmd.returncode == 0:
                    print(f"{Fore.GREEN}Successful build the payload!!{Style.RESET_ALL}")
                    time.sleep(2)
                    print(f"{Fore.GREEN}[+] Payload saved as {os.getcwd()}/{out}{Style.RESET_ALL}")
                else:
                    sys.exit(f"{Fore.RED}[-] Compiler exited with a non-zero status{Style.RESET_ALL}")
            else:
                sys.exit(f"{Fore.RED}[-] Payload source file does not exist{Style.RESET_ALL}")
        except Exception as e:
            sys.exit(f"{Fore.RED}[!] Unexpected error: {e}{Style.RESET_ALL}")
