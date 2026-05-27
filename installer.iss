[Setup]
AppName=NexCustoms
AppVersion=1.0
DefaultDirName={autopf}\NexCustoms
DefaultGroupName=NexCustoms

SetupIconFile=assets\logo.ico
UninstallDisplayIcon={app}\NexCustoms.exe

OutputBaseFilename=NexCustomsSetup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\NexCustoms"; Filename: "{app}\NexCustoms.exe"; IconFilename: "{app}\NexCustoms.exe"
Name: "{commondesktop}\NexCustoms"; Filename: "{app}\NexCustoms.exe"; IconFilename: "{app}\NexCustoms.exe"

[Run]
Filename: "{app}\NexCustoms.exe"; Description: "Launch NexCustoms"; Flags: nowait postinstall skipifsilent