import mobase

from ..basic_features import BasicLocalSavegames, BasicModDataChecker, GlobPatterns
from ..basic_game import BasicGame


class SPTAKIGame(BasicGame):
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

    def init(self, organizer: mobase.IOrganizer) -> bool:
        super().init(organizer)
        # self._register_feature(BasicLocalSavegames(self.savesDirectory()))
        self._register_feature(SPTAKIModDataChecker())
        return True


class SPTAKIModDataChecker(BasicModDataChecker):
    def __init__(self, patterns: GlobPatterns = GlobPatterns()):
        super().__init__(
            GlobPatterns(
                valid=["BepInEx", "EscapeFromTarkov_Data", "SPT", "Logs", "Fika*", "*.dll", "*.exe", "*.ini", "*.txt", "*.md", "*.bat", "*.ps1", "*.log"],
                move={"*": ""},
            ).merge(patterns),
        )
