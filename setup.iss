[Setup]
AppName=CloudMonitorAgent
AppVersion=1.0
DefaultDirName={localappdata}\CloudMonitorAgent
DefaultGroupName=CloudMonitorAgent
OutputDir=.
OutputBaseFilename=CloudMonitorAgentSetup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest

[Files]
Source: "dist\agent.exe"; DestDir: "{app}"; Flags: ignoreversion

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "CloudMonitorAgent"; ValueData: "{app}\agent.exe"; Flags: uninsdeletevalue

[Run]
Filename: "{app}\agent.exe"; Description: "Run CloudMonitorAgent"; Flags: nowait postinstall skipifsilent