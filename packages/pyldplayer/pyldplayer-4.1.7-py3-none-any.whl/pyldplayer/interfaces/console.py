import typing

from pyldplayer.model.list2meta import List2Meta
from pyldplayer.enums import SOptional
from pyldplayer.enums.consoleCmds import (
    BATCHABLE_COMMANDS, SIMPLE_EXEC_LIST, SIMPLE_QUERY_LIST, VARIED_QUERY_LIST, VARIED_EXEC_LIST, FULL_COMMANDS_LIST
)


class LDConsoleI:
    # simple exec
    rock: typing.Callable[["LDConsoleI"], None]
    zoomOut: typing.Callable[["LDConsoleI"], None]
    zoomIn: typing.Callable[["LDConsoleI"], None]
    sortWnd: typing.Callable[["LDConsoleI"], None]
    quitall : typing.Callable[["LDConsoleI"], None]

    # simple varied exec
    def quit(
        self, name: typing.Optional[str] = None, index: typing.Optional[int] = None
    ):
        pass

    def launch(
        self, name: typing.Optional[str] = None, index: typing.Optional[int] = None
    ):
        pass

    def reboot(
        self, name: typing.Optional[str] = None, index: typing.Optional[int] = None
    ):
        pass

    def add(self, name: typing.Optional[str] = None):
        pass

    def copy(self, name: typing.Optional[str] = None, _from: SOptional[str] = None):
        pass

    def remove(
        self, name: typing.Optional[str] = None, index: typing.Optional[int] = None
    ):
        pass

    def rename(
        self,
        name: typing.Optional[str] = None,
        index: typing.Optional[int] = None,
        title: SOptional[str] = None,
    ):
        pass

    def installapp(
        self,
        name: typing.Optional[str] = None,
        index: typing.Optional[int] = None,
        filename: typing.Optional[str] = None,
        packagename: typing.Optional[str] = None,
    ):
        pass

    def uninstallapp(
        self,
        name: typing.Optional[str] = None,
        index: typing.Optional[int] = None,
        packagename: SOptional[str] = None,
    ):
        pass

    def runapp(
        self,
        name: typing.Optional[str] = None,
        index: typing.Optional[int] = None,
        packagename: SOptional[str] = None,
    ):
        pass

    def killapp(
        self,
        name: typing.Optional[str] = None,
        index: typing.Optional[int] = None,
        packagename: SOptional[str] = None,
    ):
        pass

    def locate(
        self,
        name: typing.Optional[str] = None,
        index: typing.Optional[int] = None,
        LLI: SOptional[str] = None,
    ):
        pass

    def adb(
        self,
        name: typing.Optional[str] = None,
        index: typing.Optional[int] = None,
        command: SOptional[str] = None,
    ):
        pass

    def setprop(
        self,
        name: typing.Optional[str] = None,
        index: typing.Optional[int] = None,
        key: SOptional[str] = None,
        value: SOptional[str] = None,
    ):
        pass

    def downcpu(
        self,
        name: typing.Optional[str] = None,
        index: typing.Optional[int] = None,
        rate: SOptional[int] = None,
    ):
        pass

    def backup(
        self,
        name: typing.Optional[str] = None,
        index: typing.Optional[int] = None,
        file: SOptional[str] = None,
    ):
        pass

    def restore(
        self,
        name: typing.Optional[str] = None,
        index: typing.Optional[int] = None,
        file: SOptional[str] = None,
    ):
        pass

    def action(
        self,
        name: typing.Optional[str] = None,
        index: typing.Optional[int] = None,
        key: SOptional[str] = None,
        value: SOptional[str] = None,
    ):
        pass

    def scan(
        self,
        name: typing.Optional[str] = None,
        index: typing.Optional[int] = None,
        file: SOptional[str] = None,
    ):
        pass

    def pull(
        self,
        name: typing.Optional[str] = None,
        index: typing.Optional[int] = None,
        remote: SOptional[str] = None,
        local: SOptional[str] = None,
    ):
        pass

    def push(
        self,
        name: typing.Optional[str] = None,
        index: typing.Optional[int] = None,
        remote: SOptional[str] = None,
        local: SOptional[str] = None,
    ):
        pass

    def backupapp(
        self,
        name: typing.Optional[str] = None,
        index: typing.Optional[int] = None,
        packagename: SOptional[str] = None,
        file: SOptional[str] = None,
    ):
        pass

    def restoreapp(
        self,
        name: typing.Optional[str] = None,
        index: typing.Optional[int] = None,
        packagename: SOptional[str] = None,
        file: SOptional[str] = None,
    ):
        pass

    def launchex(
        self,
        name: typing.Optional[str] = None,
        index: typing.Optional[int] = None,
        packagename: SOptional[str] = None,
    ):
        pass

    def operaterecord(
        self,
        name: typing.Optional[str] = None,
        index: typing.Optional[int] = None,
        content: SOptional[str] = None,
    ):
        pass

    # simple query
    list: typing.Callable[["LDConsoleI"], None]
    runninglist: typing.Callable[["LDConsoleI"], None]
    list2: typing.Callable[["LDConsoleI"], None]

    # varied query
    def operatelist(
        self, name: typing.Optional[str] = None, index: typing.Optional[int] = None
    ):
        pass

    def operateinfo(
        self,
        name: typing.Optional[str] = None,
        index: typing.Optional[int] = None,
        file: SOptional[str] = None,
    ):
        pass

    def getprop(
        self,
        name: typing.Optional[str] = None,
        index: typing.Optional[int] = None,
        key: SOptional[str] = None,
    ):
        pass

    def isrunning(
        self, name: typing.Optional[str] = None, index: typing.Optional[int] = None
    ):
        pass

    # special
    def modify(
        self,
        mnq_name: typing.Optional[typing.Optional[str]] = None,
        mnq_idx: typing.Optional[typing.Optional[int]] = None,
        resolution: typing.Optional[str] = None,
        cpu: typing.Optional[typing.Literal[1, 2, 3, 4]] = None,
        memory: typing.Optional[
            typing.Literal[256, 512, 768, 1024, 2048, 4096, 8192]
        ] = None,
        manufacturer: typing.Optional[str] = None,
        model: typing.Optional[str] = None,
        pnumber: typing.Optional[int] = None,
        imei: typing.Optional[typing.Union[typing.Literal["auto"], str]] = None,
        imsi: typing.Optional[typing.Union[typing.Literal["auto"], str]] = None,
        simserial: typing.Optional[typing.Union[typing.Literal["auto"], str]] = None,
        androidid: typing.Optional[typing.Union[typing.Literal["auto"], str]] = None,
        mac: typing.Optional[typing.Union[typing.Literal["auto"], str]] = None,
        autorotate: typing.Optional[bool] = None,
        lockwindow: typing.Optional[bool] = None,
        root: typing.Optional[bool] = None,
    ):
        pass

    def globalsetting(
        self,
        fps: typing.Optional[int] = None,
        audio: typing.Optional[bool] = None,
        fastplay: typing.Optional[bool] = None,
        cleanmode: typing.Optional[bool] = None,
    ):
        pass

    def list2(self) -> typing.List[List2Meta]:
        pass