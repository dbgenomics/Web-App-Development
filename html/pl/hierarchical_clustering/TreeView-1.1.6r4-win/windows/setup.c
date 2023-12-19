#define UNICODE
#define _UNICODE

#include <windows.h>
#include <tchar.h>
#include <shlobj.h>

#include "resources.h"

#define NWINDOWS 5

/*============================================================================*/
/* Helper functions.                                                          */
/*============================================================================*/

static void
ShowError(const TCHAR* const title)
{ TCHAR* buffer;
  DWORD errorcode = GetLastError();
  FormatMessage (
    FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM,
    NULL,
    errorcode,
    0,
    (LPVOID)&buffer,
    0,
    NULL);
  MessageBox(NULL,buffer,title,0);
  LocalFree(buffer);
}

static TCHAR*
GetVersionNumber(void)
{ int n;
  TCHAR path[MAX_PATH];
  TCHAR* start = NULL;
  TCHAR* end = NULL;
  TCHAR* version;
  HINSTANCE hInst = GetModuleHandle(NULL);
  GetModuleFileName(hInst, path, MAX_PATH);
  end = _tcsrchr(path,'\\');
  if(end==NULL) return NULL;
  *end = '\0';
  start = _tcsrchr(path,'\\');
  if(start==NULL) return NULL;
  start++;
  start = _tcschr(start,'-');
  if(start==NULL) return NULL;
  start++;
  end = _tcschr(start,'-');
  if(end==NULL) return NULL;
  *end='\0';
  n = lstrlen(start) + 1;
  version = malloc(n*sizeof(TCHAR));
  wsprintf (version, start);
  return version;
}

static BOOL
CreateDirectoryRecursive (TCHAR* directory)
{ TCHAR* path = directory;
  WIN32_FIND_DATA filedata;
  HANDLE h;
  while ((path = _tcschr(path+1, '\\')))
  { *path = '\0';
    h = FindFirstFile(directory, &filedata);
    if(h==INVALID_HANDLE_VALUE && !CreateDirectory(directory, NULL))
      return FALSE;
    FindClose(h);
    *path = '\\';
  }
  return TRUE;
}

static void
CopyFiles(TCHAR* sourcedir, TCHAR* targetdir, HWND status)
{ HANDLE h;
  WIN32_FIND_DATA filedata;
  TCHAR* source = _tcsrchr(sourcedir,'\0');
  TCHAR* target = _tcsrchr(targetdir,'\0');
  wsprintf(source,TEXT("*"));
  h = FindFirstFile(sourcedir, &filedata);
  if(h==INVALID_HANDLE_VALUE) return;
  CreateDirectoryRecursive(targetdir);
  do
  { TCHAR* filename = filedata.cFileName;
    if (!lstrcmp(TEXT("."), filename) ||
        !lstrcmp(TEXT(".."), filename) ||
        !lstrcmp(TEXT("windows"), filename) ||
        !lstrcmp(TEXT("setup.exe"), filename)) continue;
    if (filedata.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)
    { wsprintf(source, TEXT("%s\\"), filename);
      wsprintf(target, TEXT("%s\\"), filename);
      CopyFiles(sourcedir, targetdir, status);
      *source = '\0';
      *target = '\0';
    }
    else
    { TCHAR* buffer;
      TCHAR message[] = TEXT("Copying %s to %s");
      int size = lstrlen(message) - 3; /* Minus twice %s, plus null character */
      wsprintf (source, filename);
      wsprintf (target, filename);
      size += lstrlen(sourcedir) + lstrlen(targetdir);
      buffer = malloc(size*sizeof(buffer));
      wsprintf (buffer, message, sourcedir, targetdir);
      SetWindowText(status, buffer);
      free(buffer);
      CopyFile(sourcedir,targetdir,FALSE);
    }
  } while (FindNextFile(h, &filedata));
  FindClose(h);
  *source = '\0';
  *target = '\0';
}

static BOOL
AddToStartMenu(TCHAR source[], TCHAR target[], TCHAR shortcut[], HWND status)
{ IPersistFile* ppf;
  IShellLink* psl;
  HRESULT hres;
  TCHAR options[] = TEXT("-jar -Xmx500m");
  TCHAR jarfile[] = TEXT("TreeView.jar");
  const int size = lstrlen(target) + lstrlen(options) + lstrlen(jarfile) + 4;
  /* Four more: one space, two ", and the terminating null */
  TCHAR* arguments;
  SetWindowText(status, TEXT("Adding Java TreeView to the Start menu"));
  hres = CoInitialize(NULL);
  if (!SUCCEEDED(hres)) return FALSE;
  hres = CoCreateInstance(&CLSID_ShellLink,
                          NULL,
                          CLSCTX_INPROC_SERVER,
                          &IID_IShellLink,
                          (LPVOID *) &psl);
  if (!SUCCEEDED(hres)) return FALSE;
  /* Set the path to the shortcut target and add the description. */
  arguments = malloc(size*sizeof(TCHAR));
  wsprintf (arguments, TEXT("%s \"%s%s\""), options, target, jarfile);
  lstrcat (target, TEXT("treeview.ico"));
  lstrcat (source, TEXT("windows\\treeview.ico"));
  CopyFile(source,target,FALSE);
  psl->lpVtbl->SetIconLocation(psl, target, 0);
  psl->lpVtbl->SetPath(psl, TEXT("javaw"));
  psl->lpVtbl->SetArguments(psl, arguments);
  psl->lpVtbl->SetDescription(psl, TEXT("Java TreeView"));
  free(arguments);
  hres = psl->lpVtbl->QueryInterface(psl, &IID_IPersistFile, (LPVOID*)&ppf);
  psl->lpVtbl->Release(psl);
  if (!SUCCEEDED(hres)) return FALSE;
  /* Save the link by calling IPersistFile::Save. */
  if (!CreateDirectoryRecursive (shortcut))
  { ppf->lpVtbl->Release(ppf);
    return FALSE;
  }
  hres = ppf->lpVtbl->Save(ppf, shortcut, TRUE);
  ppf->lpVtbl->Release(ppf);
  return TRUE;
}

static DWORD WINAPI
Install(PVOID pParam)
{ HWND* windows = (HWND*)pParam;
  TCHAR sourcedir[MAX_PATH];
  TCHAR targetdir[MAX_PATH];
  TCHAR shortcut[MAX_PATH];
  TCHAR* endchar;
  HWND status = GetDlgItem(windows[IDI_COPYWINDOW], ID_FILENAME);
  HINSTANCE hInst = GetModuleHandle(NULL);
  SendMessage(windows[IDI_WELCOMEWINDOW],
              IDM_GETTARGETDIR,
              (WPARAM)targetdir,
              0);
  lstrcat(targetdir,TEXT("\\"));
  SendMessage(windows[IDI_STARTMENUWINDOW],
              IDM_GETSHORTCUT,
              (WPARAM)shortcut,
              0);
  GetModuleFileName(hInst, sourcedir, MAX_PATH);
  endchar = _tcsrchr(sourcedir,'\\') + 1;
  *endchar = '\0';
  CopyFiles(sourcedir, targetdir, status);
  if (!AddToStartMenu(sourcedir, targetdir, shortcut, status))
    ShowError(TEXT("Error creating shortcut"));
  SendMessage(windows[IDI_COPYWINDOW], IDM_EXITTHREAD, 0, 0);
  return 0;
}

/*============================================================================*/
/* Callback functions                                                         */
/*============================================================================*/

BOOL CALLBACK
WelcomeProc(HWND hWnd,UINT uMsg,WPARAM wParam,LPARAM lParam)
{ static HFONT bigfont = NULL;
  static HFONT boldfont = NULL;
  static TCHAR* directory = NULL;
  static TCHAR* message = NULL;
  switch (uMsg)
  { case WM_INITDIALOG:
    { TCHAR path[MAX_PATH];
      LPITEMIDLIST pidl = NULL;
      /* Set up the message text */
      int size;
      const TCHAR source[] = TEXT(
"This will install Java TreeView %s on your computer.\n"
"\n"
"It is strongly recommended that you close all other applications\n"
"you have running before continuing. This will help prevent any\n"
"conflicts during the installation process.\n"
"\n"
"Java TreeView will be installed in the directory indicated below.\n"
"Click the \"Change directory\" button if you want to install\n"
"Java TreeView in a different directory.\n"
"\n"
"Click Next to continue, or Cancel to exit Setup.");
      TCHAR* version = GetVersionNumber();
      if (version==NULL) version = calloc(1, sizeof(TCHAR));
      size = lstrlen(source) + lstrlen(version) - 1;
      message = malloc(size*sizeof(TCHAR));
      wsprintf (message, source, version);
      free(version);
      /* Save the pointer where the directory information will be stored */
      SHGetSpecialFolderLocation(NULL, CSIDL_PROGRAM_FILES, &pidl);
      if (pidl!=NULL)
      { LPMALLOC imalloc = 0;
        BOOL result = SHGetPathFromIDList (pidl, path);
        if (SUCCEEDED(SHGetMalloc(&imalloc)))
        { imalloc->lpVtbl->Free(imalloc, pidl);
          imalloc->lpVtbl->Release(imalloc);
        }
        if(!result)
        { MessageBox(NULL,
                     TEXT("Failed to locate the Program Files directory"),
                     TEXT("Setup error"),
                     0);
          return FALSE;
        }
      }
      lstrcat(path, TEXT("\\Stanford University\\Java TreeView"));
      directory = malloc((lstrlen(path)+1)*sizeof(TCHAR));
      wsprintf (directory, path);
      SetWindowText(GetDlgItem(hWnd, ID_DIRLABEL), directory);
      /* Create the fonts */
      boldfont = CreateFont(13,
                             0,
                             0,
                             0,
                             FW_BOLD,
                             FALSE,
                             FALSE,
                             FALSE,
                             ANSI_CHARSET,
                             OUT_DEFAULT_PRECIS,
                             CLIP_DEFAULT_PRECIS,
                             DEFAULT_QUALITY,
                             DEFAULT_PITCH | FF_SWISS,
                             TEXT("MS Shell Dlg"));
      bigfont = CreateFont(24,
                            0,
                            0,
                            0,
                            FW_NORMAL,
                            FALSE,
                            FALSE,
                            FALSE,
                            ANSI_CHARSET,
                            OUT_DEFAULT_PRECIS,
                            CLIP_DEFAULT_PRECIS,
                            DEFAULT_QUALITY,
                            DEFAULT_PITCH | FF_SWISS,
                            TEXT("Microsoft Sans Serif"));
      SendDlgItemMessage(hWnd, ID_TITLE, WM_SETFONT, (WPARAM)boldfont, 0);
      SetFocus(GetDlgItem(hWnd, ID_NEXT));
      return FALSE;
    }
    case WM_PAINT:
    { PAINTSTRUCT ps;
      HDC hDC = BeginPaint (hWnd, &ps);
      RECT rect;
      HDC hDCMem = CreateCompatibleDC(hDC);
      BITMAP bmp;
      HBITMAP hWndBmp;
      rect.left   =   0;
      rect.right  = 495;
      rect.top    =   0;
      rect.bottom = 260;
      FillRect (hDC, &rect, (HBRUSH)GetStockObject(WHITE_BRUSH));
      hWndBmp = (HBITMAP)LoadImage(GetModuleHandle(NULL),
                           MAKEINTRESOURCE(ID_TREE_BMP),
                           IMAGE_BITMAP,
                           0,
                           0,
                           LR_LOADREALSIZE);
      GetObject(hWndBmp, sizeof(BITMAP), &bmp);
      SelectObject (hDCMem,hWndBmp);
      BitBlt (hDC, 18, 55, 128, 128, hDCMem, 0, 0, SRCCOPY);
      DeleteDC (hDCMem);

      SelectObject(hDC, (HGDIOBJ)bigfont);
      rect.left   =  20;
      rect.top    =  10;
      rect.bottom = 314;
      DrawText(hDC,
               TEXT("Welcome to the Java TreeView setup wizard"),
               -1,
               &rect,
               DT_LEFT | DT_TOP);

      SelectObject(hDC, (HGDIOBJ)GetStockObject(DEFAULT_GUI_FONT));
      rect.left   = 164;
      rect.top    = 50;
      DrawText(hDC, message, -1, &rect, DT_LEFT | DT_TOP);
      EndPaint (hWnd, &ps);
      return TRUE;
    }
    case WM_COMMAND:
    { switch(LOWORD(wParam))
      { case IDCANCEL:
          PostMessage(NULL,IDM_EXIT,0,0);
          return TRUE;
        case ID_NEXT:
          PostMessage(NULL,IDM_SWITCH,IDM_NEXT,0);
          return TRUE;
        case ID_CHANGEDIR:
        { TCHAR buffer[MAX_PATH];
          LPITEMIDLIST pidl = NULL;
          BROWSEINFO bi;
          bi.hwndOwner = hWnd;
          bi.pidlRoot = NULL;
          bi.pszDisplayName = directory;
          bi.lpszTitle = TEXT(
"Select the directory in which you want to install Java TreeView");
          bi.ulFlags = BIF_RETURNONLYFSDIRS;
          bi.lpfn = NULL;
          bi.lParam = 0;
          bi.iImage = 0;
          pidl = SHBrowseForFolder(&bi);
          if (pidl!=0)
          { int n;
            LPMALLOC imalloc = 0;
            if (!SHGetPathFromIDList(pidl, buffer) )
              MessageBox(NULL,
                         TEXT("Failed to access the directory"),
                         TEXT("Setup error"),
                         0);
            if (SUCCEEDED(SHGetMalloc(&imalloc)))
            { imalloc->lpVtbl->Free(imalloc, pidl);
              imalloc->lpVtbl->Release(imalloc);
            }
            free(directory);
            n = lstrlen(buffer);
            directory = malloc(n*sizeof(TCHAR));
            wsprintf(directory, buffer);
            SetWindowText(GetDlgItem(hWnd, ID_DIRLABEL), directory);
          }
          return TRUE;
        }
      }
      return FALSE;
    }
    case IDM_GETTARGETDIR:
    { TCHAR* targetdir = (TCHAR*)wParam;
      wsprintf(targetdir, directory);
      return TRUE;
    }
    case WM_SYSCOMMAND:
      if (wParam == SC_CLOSE)
      { PostMessage(NULL,IDM_EXIT,0,0);
        return TRUE;
      }
      return FALSE;
    case WM_DESTROY:
      free(directory);
      free(message);
      DeleteObject((HGDIOBJ)bigfont);
      DeleteObject((HGDIOBJ)boldfont);
      return TRUE;
  }
  return FALSE;
}

BOOL CALLBACK
StartMenuProc(HWND hWnd, UINT uMsg, WPARAM wParam, LPARAM lParam)
{ static HFONT boldfont;
  static TCHAR path[MAX_PATH];
  switch (uMsg)
  { case WM_INITDIALOG:
    { TCHAR* c;
      HWND list = GetDlgItem(hWnd, ID_STARTUP);
      WIN32_FIND_DATA ffd;
      HANDLE search;
      TCHAR name[] = TEXT("Cluster");
      LPITEMIDLIST pidl = NULL;
      SHGetSpecialFolderLocation(NULL, CSIDL_COMMON_PROGRAMS, &pidl);
      if (pidl!=NULL)
      { LPMALLOC imalloc = 0;
        BOOL result = SHGetPathFromIDList (pidl, path);
        if (SUCCEEDED(SHGetMalloc(&imalloc)))
        { imalloc->lpVtbl->Free(imalloc, pidl);
          imalloc->lpVtbl->Release(imalloc);
        }
        if(!result)
        { MessageBox(NULL,
                     TEXT("Failed to access the Start Menu"),
                     TEXT("Setup error"),
                     0);
          return FALSE;
        }
      }
      boldfont = CreateFont(14,
                             0,
                             0,
                             0,
                             FW_BOLD,
                             FALSE,
                             FALSE,
                             FALSE,
                             ANSI_CHARSET,
                             OUT_DEFAULT_PRECIS,
                             CLIP_DEFAULT_PRECIS,
                             DEFAULT_QUALITY,
                             DEFAULT_PITCH | FF_SWISS,
                             TEXT("Microsoft Sans Serif"));
      SetFocus(GetDlgItem(hWnd, ID_NEXT));
      c = _tcsrchr(path, '\0');
      wsprintf(c, TEXT("\\*"));
      search = FindFirstFile(path,&ffd); 
      if (!search) return FALSE;
      do
      { TCHAR* filename = (TCHAR*) &(ffd.cFileName);
        if (!(ffd.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)) continue;
        if (filename[0]=='.') continue;
        if (SendMessage(list, LB_FINDSTRINGEXACT, -1, (LPARAM)filename)!=LB_ERR)
          continue;
        SendMessage(list, LB_ADDSTRING, 0, (LPARAM)filename);
      } while (FindNextFile(search, &ffd));
      *(c+1) = '\0';
      if (SendMessage(list,LB_FINDSTRINGEXACT,-1,(LPARAM)name)==LB_ERR)
        SendMessage(list, LB_ADDSTRING, 0, (LPARAM)name);
      return FALSE;
    }
    case WM_PAINT:
    { PAINTSTRUCT ps;
      HDC hDC = BeginPaint (hWnd, &ps);
      RECT rect;

      HDC hDCMem = CreateCompatibleDC(hDC);
      BITMAP bmp;
      HBITMAP hWndBmp =
        (HBITMAP)LoadImage(GetModuleHandle(NULL),
                           MAKEINTRESOURCE(ID_SMALLTREE_BMP),
                           IMAGE_BITMAP,
                           0,
                           0,
                           LR_LOADREALSIZE);
      GetClientRect(hWnd, &rect);
      rect.bottom = 78;
      FillRect (hDC, &rect, (HBRUSH)GetStockObject(WHITE_BRUSH));

      GetObject(hWndBmp, sizeof(BITMAP), &bmp);
      SelectObject (hDCMem,hWndBmp);
      BitBlt (hDC, 429, 7, 64, 64, hDCMem, 0, 0, SRCCOPY);
      DeleteDC (hDCMem);
      SelectObject(hDC, (HGDIOBJ)boldfont);
      rect.left   =  20;
      rect.top    =  10;
      rect.bottom = 314;
      DrawText(hDC,
               TEXT("Select Start Menu Folder"),
               -1,
               &rect,
               DT_LEFT | DT_TOP);

      SelectObject(hDC, (HGDIOBJ)GetStockObject(DEFAULT_GUI_FONT));
      rect.left   =  30;
      rect.top    =  25;
      rect.bottom = 314;
      DrawText(hDC,
               TEXT("Where should Setup place the program's shortcuts?"),
               -1,
               &rect,
               DT_LEFT | DT_TOP);

      EndPaint (hWnd, &ps);
      return TRUE;
    }
    case WM_COMMAND:
    { switch(LOWORD(wParam))
      { case ID_BACK:
          PostMessage(NULL,IDM_SWITCH,IDM_BACK,0);
          return TRUE;
        case ID_NEXT:
          PostMessage(NULL,IDM_SWITCH,IDM_NEXT,0);
          return TRUE;
        case ID_STARTUP:
        { if (HIWORD(wParam)==LBN_SELCHANGE)
          { HWND list = (HWND)lParam;
            int i = SendMessage(list, LB_GETCURSEL, 0, 0);
            int n = SendMessage(list, LB_GETTEXTLEN, i, 0) + 1;
            TCHAR* name = malloc(n*sizeof(TCHAR));
            SendMessage(list, LB_GETTEXT, i, (LPARAM)name);
            SetWindowText(GetDlgItem(hWnd, ID_STARTUPGROUP), name);
            free(name);
            return TRUE;
          }
          break;
        }
        case ID_STARTUPGROUP:
        { if (HIWORD(wParam)==EN_CHANGE)
          { if (GetWindowTextLength(GetDlgItem(hWnd, ID_STARTUPGROUP)))
              EnableWindow(GetDlgItem(hWnd, ID_NEXT), TRUE);
            else
              EnableWindow(GetDlgItem(hWnd, ID_NEXT), FALSE);
            return TRUE;
          }
          break;
        }
      }
      return FALSE;
    }
    case IDM_GETSHORTCUT:
    { HWND hWndGroup = GetDlgItem(hWnd, ID_STARTUPGROUP);
      TCHAR* shortcut = (TCHAR*)wParam;
      TCHAR linkname[] = TEXT("\\Java Treeview.lnk");
      TCHAR* name = shortcut + wsprintf(shortcut, path);
      int n = GetWindowTextLength(hWndGroup);
      if(!GetWindowText(hWndGroup, name, n+1))
      { ShowError(TEXT("Error reading group name"));
        return TRUE;
      }
      lstrcat(name, linkname);
      return TRUE;
    }
    case WM_SYSCOMMAND:
      if (wParam == SC_CLOSE)
      { DestroyWindow (hWnd);
        return TRUE;
      }
      break;
    case WM_DESTROY:
      DeleteObject((HGDIOBJ)boldfont);
      return TRUE;
  }
  return FALSE;
}

BOOL CALLBACK
VerifyWindowProc(HWND hWnd,UINT uMsg,WPARAM wParam,LPARAM lParam)
{ static HFONT boldfont;
  static HWND* windows;
  switch (uMsg)
  { case WM_INITDIALOG:
    { windows = (HWND*)lParam;
      boldfont = CreateFont(14,
                             0,
                             0,
                             0,
                             FW_BOLD,
                             FALSE,
                             FALSE,
                             FALSE,
                             ANSI_CHARSET,
                             OUT_DEFAULT_PRECIS,
                             CLIP_DEFAULT_PRECIS,
                             DEFAULT_QUALITY,
                             DEFAULT_PITCH | FF_SWISS,
                             TEXT("Microsoft Sans Serif"));
      SetFocus(GetDlgItem(hWnd, ID_INSTALL));
      return FALSE;
    }
    case WM_SHOWWINDOW:
    { BOOL fShow = (BOOL)wParam;
      if (fShow)
      { TCHAR directory[MAX_PATH];
        TCHAR group[MAX_PATH];
        SendMessage(windows[IDI_WELCOMEWINDOW],
                    IDM_GETTARGETDIR,
                    (WPARAM)directory,
                    0);
        SendMessage(windows[IDI_STARTMENUWINDOW],
                    IDM_GETSHORTCUT,
                    (WPARAM)group,
                    0);
        SetWindowText (GetDlgItem(hWnd, ID_DIRECTORY), directory);
        SetWindowText (GetDlgItem(hWnd, ID_GROUP), group);
      }
      return TRUE;
    }
    case WM_PAINT:
    { PAINTSTRUCT ps;
      HDC hDC = BeginPaint (hWnd, &ps);
      RECT rect;

      HDC hDCMem = CreateCompatibleDC(hDC);
      BITMAP bmp;
      HBITMAP hWndBmp =
        (HBITMAP)LoadImage(GetModuleHandle(NULL),
                           MAKEINTRESOURCE(ID_SMALLTREE_BMP),
                           IMAGE_BITMAP,
                           0,
                           0,
                           LR_LOADREALSIZE);

      GetClientRect(hWnd, &rect);
      rect.bottom = 78;
      FillRect (hDC, &rect, (HBRUSH)GetStockObject(WHITE_BRUSH));

      GetObject(hWndBmp, sizeof(BITMAP), &bmp);
      SelectObject (hDCMem,hWndBmp);
      BitBlt (hDC, 429, 7, 64, 64, hDCMem, 0, 0, SRCCOPY);
      DeleteDC (hDCMem);
      SelectObject(hDC, (HGDIOBJ)boldfont);
      rect.left   =  20;
      rect.top    =  10;
      rect.bottom = 314;
      DrawText(hDC,
               TEXT("Ready to install"),
               -1,
               &rect,
               DT_LEFT | DT_TOP);

      SelectObject(hDC, (HGDIOBJ)GetStockObject(DEFAULT_GUI_FONT));
      rect.left   =  30;
      rect.top    =  25;
      rect.bottom = 314;
      DrawText(hDC,
               TEXT(
"Setup is now ready to begin installing Java TreeView on your computer."),
               -1,
               &rect,
               DT_LEFT | DT_TOP);

      EndPaint (hWnd, &ps);
      return TRUE;
    }
    case WM_COMMAND:
    { switch(LOWORD(wParam))
      { case ID_BACK:
          PostMessage(NULL,IDM_SWITCH,IDM_BACK,0);
          return TRUE;
        case ID_INSTALL:
          PostMessage(NULL,IDM_SWITCH,IDM_NEXT,0);
          return TRUE;
      }
      return FALSE;
    }
    case WM_SYSCOMMAND:
      if (wParam == SC_CLOSE)
      { DestroyWindow (hWnd);
        return TRUE;
      }
      return FALSE;
    case WM_DESTROY:
      DeleteObject((HGDIOBJ)boldfont);
      return TRUE;
  }
  return FALSE;
}

BOOL CALLBACK
CopyWindowProc(HWND hWnd,UINT uMsg,WPARAM wParam,LPARAM lParam)
{ static HFONT boldfont;
  static HWND* windows;
  static HANDLE thread = NULL;
  switch (uMsg)
  { case WM_INITDIALOG:
    { windows = (HWND*)lParam;
      boldfont = CreateFont(14,
                             0,
                             0,
                             0,
                             FW_BOLD,
                             FALSE,
                             FALSE,
                             FALSE,
                             ANSI_CHARSET,
                             OUT_DEFAULT_PRECIS,
                             CLIP_DEFAULT_PRECIS,
                             DEFAULT_QUALITY,
                             DEFAULT_PITCH | FF_SWISS,
                             TEXT("Microsoft Sans Serif"));
      return FALSE;
    }
    case WM_SHOWWINDOW:
    { BOOL fShow = (BOOL)wParam;
      DWORD threadID;
      if (fShow)
        thread = CreateThread(NULL, 0, Install, (LPVOID)windows, 0, &threadID);
      return TRUE;
    }
    case IDM_EXITTHREAD:
    { CloseHandle(thread);
      PostMessage(NULL,IDM_SWITCH,IDM_NEXT,0);
      return TRUE;
    }
    case WM_PAINT:
    { PAINTSTRUCT ps;
      HDC hDC = BeginPaint (hWnd, &ps);
      RECT rect;

      HDC hDCMem = CreateCompatibleDC(hDC);
      BITMAP bmp;
      HBITMAP hWndBmp =
        (HBITMAP)LoadImage(GetModuleHandle(NULL),
                           MAKEINTRESOURCE(ID_SMALLTREE_BMP),
                           IMAGE_BITMAP,
                           0,
                           0,
                           LR_LOADREALSIZE);

      GetClientRect(hWnd, &rect);
      rect.bottom = 78;
      FillRect (hDC, &rect, (HBRUSH)GetStockObject(WHITE_BRUSH));

      GetObject(hWndBmp, sizeof(BITMAP), &bmp);
      SelectObject (hDCMem,hWndBmp);
      BitBlt (hDC, 429, 7, 64, 64, hDCMem, 0, 0, SRCCOPY);
      DeleteDC (hDCMem);
      SelectObject(hDC, (HGDIOBJ)boldfont);
      rect.left   =  20;
      rect.top    =  10;
      rect.bottom = 314;
      DrawText(hDC,
               TEXT("Installing"),
               -1,
               &rect,
               DT_LEFT | DT_TOP);

      SelectObject(hDC, (HGDIOBJ)GetStockObject(DEFAULT_GUI_FONT));
      rect.left   =  30;
      rect.top    =  25;
      rect.bottom = 314;
      DrawText(hDC,
               TEXT(
"Please wait while Setup installs Java TreeView on your computer."),
               -1,
               &rect,
               DT_LEFT | DT_TOP);
      EndPaint (hWnd, &ps);
      return TRUE;
    }
    case WM_COMMAND:
    { switch(LOWORD(wParam))
      { case IDCANCEL:
          ShowWindow(hWnd, SW_HIDE);
          PostMessage(NULL,IDM_EXIT,2,0);
          return TRUE;
      }
      return FALSE; 
    }
    case WM_SYSCOMMAND:
      if (wParam == SC_CLOSE)
      { DestroyWindow (hWnd);
        return TRUE;
      }
      return FALSE;
    case WM_DESTROY:
      DeleteObject((HGDIOBJ)boldfont);
      return TRUE;
  }
  return FALSE;
}

BOOL CALLBACK
FinishProc(HWND hWnd,UINT uMsg,WPARAM wParam,LPARAM lParam)
{ static HFONT bigfont = NULL;
  switch (uMsg)
  { case WM_INITDIALOG:
    { bigfont = CreateFont(24,
                            0,
                            0,
                            0,
                            FW_NORMAL,
                            FALSE,
                            FALSE,
                            FALSE,
                            ANSI_CHARSET,
                            OUT_DEFAULT_PRECIS,
                            CLIP_DEFAULT_PRECIS,
                            DEFAULT_QUALITY,
                            DEFAULT_PITCH | FF_SWISS,
                            TEXT("Microsoft Sans Serif"));
      SetFocus(GetDlgItem(hWnd, IDOK));
      return FALSE;
    }
    case WM_PAINT:
    { PAINTSTRUCT ps;
      HDC hDC = BeginPaint (hWnd, &ps);
      RECT rect;
      HDC hDCMem = CreateCompatibleDC(hDC);
      BITMAP bmp;
      HBITMAP hWndBmp;
      rect.left   =   0;
      rect.right  = 495;
      rect.top    =   0;
      rect.bottom = 333;
      FillRect (hDC, &rect, (HBRUSH)GetStockObject(WHITE_BRUSH));
      hWndBmp = (HBITMAP)LoadImage(GetModuleHandle(NULL),
                           MAKEINTRESOURCE(ID_TREE_BMP),
                           IMAGE_BITMAP,
                           0,
                           0,
                           LR_LOADREALSIZE);
      GetObject(hWndBmp, sizeof(BITMAP), &bmp);
      SelectObject (hDCMem,hWndBmp);
      BitBlt (hDC, 18, 55, 128, 128, hDCMem, 0, 0, SRCCOPY);
      DeleteDC (hDCMem);

      SelectObject(hDC, (HGDIOBJ)bigfont);
      rect.left   =  20;
      rect.top    =  10;
      rect.bottom = 314;
      DrawText(hDC,
               TEXT("Finished installation of Java TreeView"),
               -1,
               &rect,
               DT_LEFT | DT_TOP);

      SelectObject(hDC, (HGDIOBJ)GetStockObject(DEFAULT_GUI_FONT));
      rect.left   = 164;
      rect.top    = 50;
      DrawText(hDC,TEXT(
"Setup has finished installing Java TreeView on your computer.\n"
"The application may be launched by selecting the installed\n"
"icons from the Start menu."
"\n"
"\n"
"Click Finish to exit Setup."),
               -1,
               &rect,
               DT_LEFT | DT_TOP);
      EndPaint (hWnd, &ps);
      return TRUE;
    }
    case WM_COMMAND:
    { if (LOWORD(wParam)==IDOK) PostMessage(NULL,IDM_EXIT,0,0);
      return TRUE;
    }
    case WM_SYSCOMMAND:
      if (wParam == SC_CLOSE)
      { PostMessage(NULL,IDM_EXIT,0,0);
        return TRUE;
      }
      return FALSE;
    case WM_DESTROY:
      DeleteObject((HGDIOBJ)bigfont);
      return TRUE;
  }
  return FALSE;
}

/*============================================================================*/
/*  Create the windows                                                        */
/*============================================================================*/

static BOOL CreateWindows(HINSTANCE hInst, HWND windows[NWINDOWS])
{ /* Create the windows that we will be showing */
  int i;
  windows[IDI_WELCOMEWINDOW] = CreateDialog(hInst,
                                   MAKEINTRESOURCE(ID_WELCOMEWINDOW),
                                   NULL,
                                   &WelcomeProc);
  windows[IDI_STARTMENUWINDOW] = CreateDialog(hInst,
                                   MAKEINTRESOURCE(ID_STARTMENUWINDOW),
                                   NULL,
                                   &StartMenuProc);
  windows[IDI_VERIFYWINDOW] = CreateDialogParam(hInst,
                                   MAKEINTRESOURCE(ID_VERIFYWINDOW),
                                   NULL,
                                   &VerifyWindowProc,
                                   (LPARAM)windows);
  windows[IDI_COPYWINDOW] = CreateDialogParam(hInst,
                                   MAKEINTRESOURCE(ID_COPYWINDOW),
                                   NULL,
                                   &CopyWindowProc,
                                   (LPARAM)windows);
  windows[IDI_FINISHWINDOW] = CreateDialog(hInst,
                                   MAKEINTRESOURCE(ID_FINISHWINDOW),
                                   NULL,
                                   &FinishProc);

  for (i = 0; i < NWINDOWS; i++) if (!windows[i]) break;
  if (i < NWINDOWS)
  { for (i = 0; i < NWINDOWS; i++) if (windows[i]) DestroyWindow(windows[i]);
    return FALSE;
  }
  return TRUE;
}

/*============================================================================*/
/*  Main                                                                      */
/*============================================================================*/

int STDCALL
WinMain (HINSTANCE hInst, HINSTANCE hPrev, LPSTR lpCmd, int nShow)
{ int i;
  HWND windows[NWINDOWS];
  MSG msg;

  /* See if the user really wants to install Java TreeView */
  if(MessageBox(NULL,
                TEXT(
"This will install Java TreeView. Do you wish to continue?"),
                TEXT("Setup"),
                MB_YESNO | MB_ICONQUESTION)!=IDYES) ExitProcess(0);

  /* Create the windows */
  if(!CreateWindows(hInst, windows)) ExitProcess(0);

  /* Show the first window */
  i = 0;
  ShowWindow(windows[i], SW_SHOW);

  while(GetMessage(&msg, NULL, 0, 0))
  { if (msg.message==IDM_EXIT) break;
    if (msg.message==IDM_SWITCH)
    { ShowWindow(windows[i], SW_HIDE);
      switch(msg.wParam)
      { case IDM_NEXT: i++; break;
        case IDM_BACK: i--; break;
      }
      ShowWindow(windows[i], SW_SHOW);
    }
    TranslateMessage(&msg);
    DispatchMessage(&msg);
  }

  for (i = 0; i < NWINDOWS; i++) DestroyWindow(windows[i]);

  ExitProcess(msg.wParam);
}
