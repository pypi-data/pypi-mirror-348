# coding=utf-8
from typing import Any

import os

# from ka_uts_uts.utils.pac import Pac

TyArr = list[Any]
TyDic = dict[Any, Any]
TyPath = str
TyStr = str
TyTup = tuple[Any, Any]


class Path:
    """ Package Module Management
    """
    # @staticmethod
    # def sh_t_pacmod(cls) -> TyTup:
    #     """ Show Pacmod Dictionary
    #     """
    #     a_pacmod: TyArr = cls.__module__.split(".")
    #     return tuple(a_pacmod)

    # @staticmethod
    # def sh_d_pacmod(cls) -> TyDic:
    #     """ Show Pacmod Dictionary
    #     """
    #     a_pacmod: TyArr = cls.__module__.split(".")
    #     return {'package': a_pacmod[0], 'module': a_pacmod[1:]}

    # @staticmethod
    # def sh_path_module_yaml(d_pacmod: TyDic) -> Any:
    #     """ show directory
    #     """
    #     _package = d_pacmod['package']
    #     _package = cls_com.__module__.split(".")[0]
    #     _module = d_pacmod['module']
    #     _path = f"{_module}/data/{_module}.yml"
    #     return Pac.sh_path_by_path(_package, _path)

    # @classmethod
    # def sh_path_by_data_keys_yml(cls, cls_com) -> Any:
    #     """
    #     show path to configuration yaml-file in data directory of package
    #     """
    #     _package = cls_com.__module__.split(".")[0]
    #     _path = os.path.join('data', 'keys.yml')
    #     return Pac.sh_path_by_path(_package, _path)

    # @classmethod
    # def sh_path_cfg_yml(cls, cls_app) -> Any:
    #     """
    #     show path to configuration yaml-file in data directory of package
    #     """
    #     _d_pacmod = cls.sh_d_pacmod(cls_app)
    #     _package = _d_pacmod['package']
    #     _path = os.path.join('data', 'cfg.yml')
    #     return Pac.sh_path_by_path(_package, _path)

    # @classmethod
    # def sh_dir_type(cls, kwargs: TyDic, type_: TyStr) -> TyPath:
    #     """
    #     Show run_dir
    #     """
    #     app_com = kwargs.get('app_com')
    #     app_data = kwargs.get('app_data', '')
    #     tenant = kwargs.get('tenant', '')
    #     a_pacmod: TyArr = app_com.__module__.split(".")
    #     package = a_pacmod[0]
    #     module = a_pacmod[1]
    #     return os.path.join(app_data, tenant, package, module, type_)

    @staticmethod
    def sh_app_data_path_by_type_and_file_pattern(
            kwargs: TyDic, filename, type_: str, suffix: str) -> TyPath:
        """
        show type specific path
        """
        _app_com = kwargs.get('app_com')
        _app_data = kwargs.get('app_data', '')
        _tenant = kwargs.get('tenant', '')
        _a_pacmod: TyArr = _app_com.__module__.split(".")
        _package = _a_pacmod[0]
        _module = _a_pacmod[1]
        _path = os.path.join(_app_data, _tenant, _package, _module, type_)
        return os.path.join(_path, f"{filename}*.{suffix}")
