#!/usr/bin/python3
def Help():
    # Define color codes
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    # Banner and header
    print(f'\n{YELLOW}{BOLD}╔{"═"*80}╗')
    print(f'║{"COMMAND REFERENCE".center(80)}║')
    print(f'╠{"═"*80}╣{END}')
    
    # Command modules with better formatting
    Modules = {
        "back": "Background the current process",
        "exit": "Exit the C2 console",
        "help": "Show available commands",
        "iflag": "Agent verification flag (differentiates between sockets and agents)",
        "kill": "Kill an Agent process by PID (Usage: kill <PID>)",
        "killall": "Terminate all running listener jobs and agents",
        "jobs": "List all active Agent processes and listeners",
        "lhost": "Set listener host (Usage: set lhost <IP>)",
        "lport": "Set listener port (Usage: set lport <PORT>)",
        "run": "Start the listener with current configuration",
        "select": "Select an Agent session (Usage: select <AgentID>)",
        "set": "Configure options (Usage: set <option> <value>)",
    }
    max_cmd_length = max(len(cmd) for cmd in Modules.keys()) + 2
    print(f'{YELLOW}║ {BOLD}{"Command".ljust(max_cmd_length)}{END}{YELLOW}  {BOLD}Description{" "*(72-max_cmd_length)}║')
    print(f'╠{"═"*max_cmd_length}╦{"═"*(80-max_cmd_length-3)}╣')
    
    for i, (icmd, idesc) in enumerate(Modules.items()):
        cmd_color = CYAN if i % 2 == 0 else GREEN
        print(f'║ {cmd_color}{icmd.ljust(max_cmd_length)}{END}{YELLOW}  {idesc.ljust(80-max_cmd_length-3)}║')
    # Footer
    print(f'╚{"═"*80}╝{END}\n')
    print(f"{YELLOW}Note:{END} Use {GREEN}set{END} command to configure options before {GREEN}run{END}ning the listener")
    print(f"Example: {CYAN}set lhost 0.0.0.0{END} | {CYAN}set lport 8080{END} | {CYAN}set iflag index.html{END}\n")

HelpCommands = ["back", "exit", "help", "kill", "killall", "lhost", "lport", "jobs", "run", "select", "set", "iflag"]
def HelpCommandCompletion(text, state):
    for cmd in HelpCommands:
        if cmd.startswith(text):
            if not state:
                return cmd
            else:
                state -= 1