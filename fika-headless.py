import pathlib
from typing import Optional, List, override, Tuple

import mobase
from PyQt6.QtCore import qInfo, qWarning
from PyQt6.QtGui import QIcon


class FikaHeadless(mobase.IPluginTool, mobase.IPluginFileMapper):
    FikaHeadlessBase = "fika-headless-base"
    FikaHeadlessExecutable = "fika-headless-executable"
    FikaHeadlessOverwrite = "fika-headless-overwrite"
    EscapeFromTarkovData = "EscapeFromTarkov_Data"

    def __init__(self):
        super().__init__()
        mobase.IPluginFileMapper.__init__(self)
        self.__organizer: Optional[mobase.IOrganizer] = None
        self.__running = False

    @override
    def display(self):
        executable: str = self.__organizer.pluginSetting(self.name(), FikaHeadless.FikaHeadlessExecutable)
        overwrite: str = self.__organizer.pluginSetting(self.name(), FikaHeadless.FikaHeadlessOverwrite)
        mod_list = self.__organizer.modList()
        overwrite_mod = mod_list.getMod(overwrite)
        if overwrite_mod is None:
            qWarning(f"the overwrite mod {overwrite} does not exist")
            return
        qInfo(f"starting fika headless client, executable: {executable}, overwrite: {overwrite}")
        handle = self.__organizer.startApplication(executable, forcedCustomOverwrite=overwrite)
        self.__organizer.waitForApplication(handle)
        self.__organizer.modDataChanged(overwrite_mod)

    @override
    def displayName(self) -> str:
        return "Fika Headless"

    @override
    def icon(self) -> QIcon:
        return QIcon()

    @override
    def tooltip(self) -> str:
        return "select the profile used for fika headless first, then launch this tool"

    @override
    def author(self) -> str:
        return "Ricardo Evans"

    # @override
    # def master(self) -> str:
    #     return "SPT AKI Plugin"

    @override
    def description(self) -> str:
        return "allow launch fika headless client with spt client"

    @override
    def init(self, organizer) -> bool:
        qInfo(f"initialized")
        self.__organizer = organizer
        return True

    @override
    def name(self) -> str:
        return self.displayName()

    @override
    def settings(self) -> List[mobase.PluginSetting]:
        return [
            mobase.PluginSetting(FikaHeadless.FikaHeadlessBase, "the absolute path to the base game used by fika headless, this must be a different copy of the full game except the EscapeFromTarkov_Data folder", ""),
            mobase.PluginSetting(FikaHeadless.FikaHeadlessExecutable, "the executable used to launch fika headless client, you need to define the executable through MO2 first", ""),
            mobase.PluginSetting(FikaHeadless.FikaHeadlessOverwrite, "the overwrite mod used to store outputs from fika headless client", ""),
        ]

    @override
    def requirements(self) -> list[mobase.IPluginRequirement]:
        return [
            mobase.PluginRequirementFactory.gameDependency("SPT AKI"),
            mobase.PluginRequirementFactory.pluginDependency("SPT AKI Plugin"),
        ]

    @override
    def version(self) -> mobase.VersionInfo:
        return mobase.VersionInfo(1, 0, 0, 0)

    @staticmethod
    def create_mapping(source_path: pathlib.Path, target_path: pathlib.Path, create_target=False) -> mobase.Mapping:
        return mobase.Mapping(str(source_path.absolute()), str(target_path.absolute()), source_path.is_dir(), create_target)

    @override
    def mappings(self) -> list[mobase.Mapping]:
        if self.__organizer.managedGame().gameName() != "SPT AKI":
            return []
        target_path = pathlib.Path(self.__organizer.pluginSetting(self.name(), FikaHeadless.FikaHeadlessBase))
        if not target_path.is_dir():
            qWarning(f"the fika headless base path {target_path.absolute()} is not a valid directory")
            return []

        game_path = pathlib.Path(self.__organizer.managedGame().gameDirectory().absolutePath())
        overwrite: str = self.__organizer.pluginSetting(self.name(), FikaHeadless.FikaHeadlessOverwrite)
        result = []
        # result = [FikaHeadless.create_mapping(game_path / FikaHeadless.EscapeFromTarkovData, target_path / FikaHeadless.EscapeFromTarkovData)]
        mod_list = self.__organizer.modList()
        profile = self.__organizer.profile()
        qInfo(f"create mappings for {profile.name()}")
        for mod_name in mod_list.allModsByProfilePriority(profile):
            if mod_list.state(mod_name) & mobase.ModState.ACTIVE:
                mod = mod_list.getMod(mod_name)
                mod_path = pathlib.Path(mod.absolutePath())
                result.append(FikaHeadless.create_mapping(mod_path, target_path, mod.name() == overwrite))
        result.append(FikaHeadless.create_mapping(pathlib.Path(self.__organizer.overwritePath()), target_path))
        return result


def createPlugin() -> mobase.IPlugin:
    return FikaHeadless()
