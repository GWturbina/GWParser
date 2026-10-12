; GW Parser - установщик (Inno Setup 6). Собирается на GitHub, руками не запускать.
; Ставится без прав администратора - в папку пользователя, ярлык на рабочий стол.
#define AppVer GetEnv("APP_VERSION")
#if AppVer == ""
  #define AppVer "3.2"
#endif

[Setup]
AppId={{3AA52D2B-10E7-4525-BCFA-FF3DA3D21EE1}
AppName=Поиск контактов GlobalWay
AppVersion={#AppVer}
AppPublisher=GlobalWay
AppPublisherURL=https://cgift.club
DefaultDirName={localappdata}\Programs\GWParser
DefaultGroupName=Поиск контактов
DisableProgramGroupPage=yes
DisableDirPage=yes
PrivilegesRequired=lowest
OutputDir=dist
OutputBaseFilename=GWParser_Setup
SetupIconFile=poisk.ico
UninstallDisplayIcon={app}\GWParser.exe
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
CloseApplications=yes

[Languages]
Name: "ru"; MessagesFile: "compiler:Languages\Russian.isl"

[Files]
Source: "dist\GWParser.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "poisk.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autodesktop}\Поиск контактов"; Filename: "{app}\GWParser.exe"; IconFilename: "{app}\poisk.ico"
Name: "{group}\Поиск контактов"; Filename: "{app}\GWParser.exe"; IconFilename: "{app}\poisk.ico"
Name: "{group}\Поиск контактов - живой режим"; Filename: "{app}\GWParser.exe"; Parameters: "live"; IconFilename: "{app}\poisk.ico"
Name: "{group}\Поиск контактов - выбрать страну"; Filename: "{app}\GWParser.exe"; Parameters: "setup"; IconFilename: "{app}\poisk.ico"
Name: "{group}\Удалить Поиск контактов"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\GWParser.exe"; Description: "Запустить сейчас"; Flags: nowait postinstall skipifsilent
