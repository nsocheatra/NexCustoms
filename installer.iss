[Setup]
AppName=NexCustoms
AppVersion=1.0.0
DefaultDirName={autopf}\NexCustoms
DefaultGroupName=NexCustoms
OutputDir=output
OutputBaseFilename=NexCustoms_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
SetupIconFile=assets\logo.ico
UninstallDisplayIcon={app}\NexCustoms.exe


[Files]
Source: "dist\NexCustoms.exe"; DestDir: "{app}"; Flags: ignoreversion


[Icons]
Name: "{group}\NexCustoms"; Filename: "{app}\NexCustoms.exe"
Name: "{autodesktop}\NexCustoms"; Filename: "{app}\NexCustoms.exe"


[Run]
Filename: "{app}\NexCustoms.exe"; Description: "Launch NexCustoms"; Flags: nowait postinstall skipifsilent