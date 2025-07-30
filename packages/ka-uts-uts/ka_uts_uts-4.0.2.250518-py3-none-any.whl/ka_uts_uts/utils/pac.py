# coding=utf-8
from typing import Any

import os
import importlib.resources

# from ka_uts_log.log import LogEq
# from ka_uts_log.log import Log

TyArr = list[Any]
TyDic = dict[Any, Any]
TyPackage = str
TyPackages = list[str]
TyPath = str
TnPath = None | TyPath


class Pac:

    @classmethod
    def sh_path_of_class_by_path(cls, cls_app, path: TyPath) -> Any:
        # def sh_path_in_cls(cls, path: TyPath) -> Any:
        """
        show directory
        """
        _package = cls_app.__module__.split[0]
        return cls.sh_path_by_path(_package, path)

    @staticmethod
    def sh_path(package: TyPackage) -> Any:
        return str(importlib.resources.files(package))

    @staticmethod
    def sh_path_by_path(
            package: TyPackage, path: TyPath) -> Any:
        # def sh_path_by_pack(
        """ show directory
        """
        _path = str(importlib.resources.files(package).joinpath(path))
        if not _path:
            print(f"path {_path} is empty")
            return ''
        if os.path.exists(_path):
            print(f"path {_path} exists")
            return _path
        print(f"path {_path} does not exist")
        return ''

    @classmethod
    def sh_path_by_path_and_prefix(
            cls, package: TyPackage, path: TyPath, prefix: TyPath = '') -> Any:
        # def sh_path_by_pack(
        """
        show directory
        """
        return cls.sh_path_by_path(package, os.path.join(prefix, path))
