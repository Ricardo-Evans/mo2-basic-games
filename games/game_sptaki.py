from typing import List

import mobase
from PyQt6.QtCore import QFileInfo

from ..basic_features import BasicModDataChecker, GlobPatterns, BasicLocalSavegames
from ..basic_game import BasicGame


class SPTAKIGame(BasicGame, mobase.IPluginFileMapper):
    Name = "SPT AKI Plugin"
    Author = "Archon"
    Version = "1.1.1"
    GameName = "SPT AKI"
    GameShortName = "sptaki"
    GameBinary = "EscapeFromTarkov.exe"
    GameDataPath = "%GAME_PATH%"
    GameSaveExtension = "json"
    GameSavesDirectory = "%GAME_PATH%/user/profiles"

    def __init__(self):
        super().__init__()
        mobase.IPluginFileMapper.__init__(self)

    def init(self, organizer: mobase.IOrganizer) -> bool:
        super().init(organizer)
        # self._register_feature(BasicLocalSavegames(self.savesDirectory()))
        self._register_feature(SPTAKIModDataChecker())
        return True

    def executables(self) -> List[mobase.ExecutableInfo]:
        execs = super().executables()

        """
        A bat script file to bridge the environment to server and launcher.
        """
        workaround_path = self._gamePath + "/sptvfsbridge.bat"

        try:
            workaround = open(workaround_path, "rt")
        except FileNotFoundError:
            with open(workaround_path, "wt") as workaround:
                workaround.write(
                    """
@echo off
setlocal

set "launcher_path=SPT.Launcher.exe"
set "server_path=SPT.Server.exe"

REM Launch the server.exe
start "" "%server_path%"

REM Wait for a moment to ensure the server.exe has started
timeout /t 5 /nobreak >nul

REM Launch the launcher.exe
start "" "%launcher_path%"

endlocal
"""
                )
        workaround.close()

        execs.append(
            mobase.ExecutableInfo("Launch SP Tarkov", QFileInfo(workaround_path))
        )
        execs.pop(0)
        return execs

    def mappings(self) -> list[mobase.Mapping]:
        return []


class SPTAKIModDataChecker(BasicModDataChecker):
    def __init__(self, patterns: GlobPatterns = GlobPatterns()):
        super().__init__(
            GlobPatterns(
                valid=["SPT_Data", "BepInEx", "ClientMods", "EscapeFromTarkov_Data", "user", "*.dll", "*.exe", "*.ini", "*.txt"],
                move={"plugins": "BepInEx/", "patchers": "BepInEx/", "package.json": "user/Mods/", "*": ""},
            ).merge(patterns),
        )
