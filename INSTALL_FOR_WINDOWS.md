# BlueXolo in Windows 10 Home with Docker

## Requirements

* Windows 10 (version 2004 or higher)
* WSL 2
  * 64 bit processor with Second Level Address Translation (SLAT)
  * 4GB system RAM
  * BIOS-level hardware virtualization support must be enabled in the BIOS settings.
* Docker
* Git
* BlueXolo Repository

## Setup WSL 2

Open PowerShell as administrator and execute the following commands.

```powershell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

Once the commands were executed, restart your machine and update to WSL 2.

> [Check the documentation for moving to WSL 2]

The last thing to do in this step is set the version 2 as default for WSL.

```powershell
wsl --set-default-version 2
```

## Install Docker Desktop

Download from [Docker Hub] and make sure to enable WSL features if it is asked during
the installation. To verify your Docker version you can open a terminal and run the
```docker -v``` command.

## Get the BlueXolo Repository

```powershell
git clone https://github.com/IBM/BlueXolo.git
```

## Using BlueXolo

Before you can use BlueXolo, create a folder named _BlueXoloData_ in a directory with
read and write permissions, you will need the path of this folder and the path of the
BlueXolo repository. If you want to run BlueXolo execute the following script located
inside the repository.

```powershell
.\docker\tools\start-bluexolo.bat
```

This script will ask for the path of the repository and the path of _BlueXoloData_, and
that is it, the BlueXolo will be running after a few minutes in _localhost:8000_.

To stop BlueXolo run the script:

```powershell
.\docker\tools\stop-bluexolo.bat
```

> Tip: You can modify your _start-bluexolo.bat_ script and set a value for the variable
__BLUEXOLO_DIR__ with the path of the repository and __BLUEXOLO_DATA__ with the path to
the folder that you have created.

<!-- Used links -->
[Check the documentation for moving to WSL 2]: https://docs.microsoft.com/en-us/windows/wsl/wsl2-kernel
[Docker Hub]: https://hub.docker.com/editions/community/docker-ce-desktop-windows/
