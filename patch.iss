[Setup]
AppName=Saptha Stock Manager
AppVersion=1.2
AppVerName=Saptha Stock Manager Patch 1.2
DefaultDirName={pf}\SapthaStockApp
DefaultGroupName=SapthaStockApp
OutputBaseFilename=SapthaStockApp_Patch_1_2
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
Uninstallable=no
DisableProgramGroupPage=yes
DisableReadyPage=yes
DisableFinishedPage=no
CreateAppDir=yes

[Files]
; Replace updated files, don't touch DB
Source: "dist\app.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "modules\*"; DestDir: "{app}\modules"; Flags: ignoreversion recursesubdirs createallsubdirs

; DO NOT include database or db folder, so it remains intact
; Do not include stock.db

[Icons]
Name: "{group}\Saptha Stock Manager"; Filename: "{app}\app.exe"

[Run]
Filename: "{app}\app.exe"; Description: "Launch after patch"; Flags: nowait postinstall skipifsilent
