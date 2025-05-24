[Setup]
AppName=Saptha Stock Manager
AppVersion=1.0
DefaultDirName={pf}\SapthaStockApp
DefaultGroupName=Saptha Stock Manager
OutputBaseFilename=SapthaStockAppInstaller
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
UninstallDisplayIcon={app}\app.exe

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"; Flags: checkablealone checkedonce

[Files]
Source: "dist\app\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Saptha Stock Manager"; Filename: "{app}\app.exe"
Name: "{userdesktop}\Saptha Stock Manager"; Filename: "{app}\app.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\app.exe"; Description: "Launch Saptha Stock Manager"; Flags: nowait postinstall skipifsilent
