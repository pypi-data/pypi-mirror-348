from typing import Any

from ka_uts_path.dodopath import DoDoPath
from ka_uts_log.log import LogEq

TyArr = list[Any]
TyAoPath = list[str]
TyDic = dict[Any, Any]
TyAoD = list[TyDic]
TyPath = str


class AoDoDPath:
    """
    Manage Array of Path-Dictionaries
    """
    @staticmethod
    def sh_aopath(aodod_path: TyAoD, kwargs: TyDic) -> TyAoPath:
        _aopath: TyAoPath = []
        LogEq.debug("aodod_path", aodod_path)
        if not aodod_path:
            LogEq.debug("_aopath", _aopath)
            return _aopath
        for _dod_path in aodod_path:
            _path: TyPath = DoDoPath.sh_path(_dod_path, kwargs)
            _aopath.append(_path)
        LogEq.debug("_aopath", _aopath)
        return _aopath
