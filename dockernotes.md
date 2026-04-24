Sure — GitHub README/notes হিসেবে upload করার মতো clean version:

````md
# Docker Desktop Installation Fix on Windows + WSL2 Setup

## 1. Check Docker Installation

```powershell
docker --version
docker run hello-world
````

---

## 2. Check WSL Status

```powershell
wsl --status
wsl -l -v
```

Expected:

```text
Ubuntu            Running    2
docker-desktop    Running    2
```

---

## 3. Download and Extract PsExec

Download PsExec from Microsoft Sysinternals:

```text
https://learn.microsoft.com/en-us/sysinternals/downloads/psexec
```

Extract to:

```text
C:\Tools
```

---

## 4. Open SYSTEM CMD Using PsExec

Open **CMD as Administrator**, then run:

```cmd
cd C:\Tools
psexec.exe -i -s cmd.exe
```

Verify SYSTEM mode:

```cmd
whoami
```

Expected:

```text
nt authority\system
```

---

## 5. Fix DockerDesktop ProgramData Permission

Run these commands inside the SYSTEM CMD:

```cmd
rmdir /s /q "C:\ProgramData\DockerDesktop"
mkdir "C:\ProgramData\DockerDesktop"

icacls "C:\ProgramData\DockerDesktop" /setowner "NT AUTHORITY\SYSTEM" /T /C

icacls "C:\ProgramData\DockerDesktop" /grant "NT AUTHORITY\SYSTEM:(F)" /T /C

icacls "C:\ProgramData\DockerDesktop" /grant "BUILTIN\Administrators:(F)" /T /C
```

---

## 6. Run Docker Desktop Installer

```cmd
"C:\Users\Shuvo\Downloads\Docker Desktop Installer.exe"
```

After installation succeeds, log out or restart Windows.

---

## 7. Verify Docker After Restart

```powershell
docker --version
docker run hello-world
```

---

## 8. Verify Docker from Ubuntu WSL

Open Ubuntu/WSL:

```powershell
wsl
```

Inside Ubuntu:

```bash
docker --version
docker ps
docker run hello-world
```

If `hello-world` runs successfully, Docker Desktop is connected with WSL2.

---

## 9. Useful Test Containers

Ubuntu container:

```bash
docker run -it ubuntu bash
```

Python container:

```bash
docker run -it python:3.10 bash
```

---

## Final Status

* Docker Desktop installed successfully
* WSL2 enabled
* Ubuntu WSL detected
* Docker Desktop connected with WSL
* Docker CLI working from both Windows and Ubuntu

````

Use repo file name:

```text
docker-windows-wsl-fix.md
````
