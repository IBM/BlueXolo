## Install BlueXolo in Windows 10 Home

### Requirements
* Windows 10 (version 2004 or higher)
* WSL 2
  - 64 bit processor with Second Level Address Translation (SLAT)
  - 4GB system RAM
  - BIOS-level hardware virtualization support must be enabled in the BIOS settings.
* Docker
* Git
* BlueXolo Repository

### Steps
**1.** Run Windows PowerShell as administrator

**2.** Install Windows Subsystem for Linux
```
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
```

**3.** Enable Virtual Machine Platform
```
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

**4.** Restart your machine

**5.** Update the WSL 2 Linux kernel
>  [WSL Documentation]

**6.** Run again Windows PowerShell and set the WSL default version
```
wsl --set-default-version 2
```

**7.** Download Docker Desktop for Windows from [Docker Hub]

**8.** Run the installer and enable the WSL 2 features, then start the installation

**9.** Restart your machine

**10.** To verify your Docker version, open a terminal and run the following command
```
docker -v
```

**11.** Clone the BlueXolo repository from GitHub
```
git clone https://github.com/IBM/BlueXolo
```
> If you do not have Git installed in your machine: [Git Downloads]

**12.** Create a folder to save BlueXolo data
```
mkdir bluexolo-data
```

**13.** Run BlueXolo
<pre><code>docker run --privileged -p 8000:8000 -h bluexolo -e container=docker -v <b>path/to/your/repository</b>:/opt/BlueXolo-src -v <b>path/to/your/bluexolo-data</b>:/var/lib/postgresql --name bluexolo bluexolo/bluexolo </code></pre>
> BlueXolo is now running on localhost at port 8000

**14.** Stop BlueXolo
```
docker kill bluexolo
docker rm $(docker ps -qa)
```

[WSL Documentation]: https://docs.microsoft.com/en-us/windows/wsl/wsl2-kernel
[Docker Hub]: https://hub.docker.com/editions/community/docker-ce-desktop-windows/
[Git Downloads]: https://git-scm.com/downloads