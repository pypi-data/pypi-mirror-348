from typing import Any
from collections.abc import Callable

import os
import time
import calendar
from datetime import datetime
import logging
import logging.config
from logging import Logger
import psutil

from ka_uts_uts.ioc.jinja2_ import Jinja2_
from ka_uts_uts.utils.pacs import Pacs
# from ka_uts_uts.utils.pacmod import PacMod

TyAny = Any
TyCallable = Callable[..., Any]
TyDateTime = datetime
TyTimeStamp = int
TyArr = list[Any]
TyBool = bool
TyDic = dict[Any, Any]
TyDir = str
TyPath = str
TyLogger = Logger
TyStr = str

TnAny = None | Any
TnArr = None | TyArr
TnBool = None | bool
TnDic = None | TyDic
TnTimeStamp = None | TyTimeStamp
TnDateTime = None | TyDateTime
TnStr = None | TyStr


class LogEq:
    """Logging Class
    """
    @staticmethod
    def sh_eq(key: Any, value: Any) -> TyStr:
        return f"{key} = {value}"

    @classmethod
    def debug(cls, key: Any, value: Any) -> None:
        Log.debug(cls.sh_eq(key, value), stacklevel=3)

    @classmethod
    def info(cls, key: Any, value: Any) -> None:
        Log.info(cls.sh_eq(key, value), stacklevel=3)

    @classmethod
    def warning(cls, key: Any, value: Any) -> None:
        Log.warning(cls.sh_eq(key, value), stacklevel=3)

    @classmethod
    def error(cls, key: Any, value: Any) -> None:
        Log.error(cls.sh_eq(key, value), stacklevel=3)

    @classmethod
    def critical(cls, key: Any, value: Any) -> None:
        Log.critical(cls.sh_eq(key, value), stacklevel=3)


class LogDic:

    @classmethod
    def debug(cls, dic: TyDic) -> None:
        for key, value in dic.items():
            LogEq.debug(key, value)

    @classmethod
    def info(cls, dic: TyDic) -> None:
        for key, value in dic.items():
            LogEq.info(key, value)

    @classmethod
    def warning(cls, dic: TyDic) -> None:
        for key, value in dic.items():
            LogEq.warning(key, value)

    @classmethod
    def error(cls, dic: TyDic) -> None:
        for key, value in dic.items():
            LogEq.error(key, value)

    @classmethod
    def critical(cls, dic: TyDic) -> None:
        for key, value in dic.items():
            LogEq.critical(key, value)


class Utils:

    @staticmethod
    def sh_username(kwargs: TyDic) -> str:
        """
        Show username
        """
        _log_type = kwargs.get('log_type', 'std')
        if _log_type == "usr":
            _username: str = psutil.Process().username()
        else:
            _username = ''
        return _username

    @classmethod
    def sh_dir_run(cls, kwargs: TyDic) -> TyPath:
        """
        Show dir_run
        """
        _app_data: str = kwargs.get('app_data', '/data')
        _tenant: str = kwargs.get('tenant', '')
        _cls_app = kwargs.get('cls_app')
        _package = _cls_app.__module__.split(".")[0]
        _username = cls.sh_username(kwargs)
        _cmd: TyStr = kwargs.get('cmd', '')
        _path: TyPath = os.path.join(
                _app_data, _tenant, 'RUN', _package, _username, _cmd)
        return _path

    @classmethod
    def sh_d_dir_run(cls, kwargs) -> TyDic:
        """
        Read log file path with jinja2
        """
        _dir_run = cls.sh_dir_run(kwargs)
        if kwargs.get('sw_single_log_dir', True):
            return {
                    'dir_run_debs': f"{_dir_run}/debs",
                    'dir_run_infs': f"{_dir_run}/logs",
                    'dir_run_wrns': f"{_dir_run}/logs",
                    'dir_run_errs': f"{_dir_run}/logs",
                    'dir_run_crts': f"{_dir_run}/logs",
            }
        return {
                'dir_run_debs': f"{_dir_run}/debs",
                'dir_run_infs': f"{_dir_run}/infs",
                'dir_run_wrns': f"{_dir_run}/wrns",
                'dir_run_errs': f"{_dir_run}/errs",
                'dir_run_crts': f"{_dir_run}/crts",
        }

    @classmethod
    def sh_path_log_cfg(cls_log, kwargs: TyDic) -> Any:
        """ show directory
        """
        _log_type = kwargs.get('log_type', 'std')
        _cls_app = kwargs.get('cls_app')
        _log_package = cls_log.__module__.split(".")[0]
        _app_package = _cls_app.__module__.split(".")[0]
        _packages = [_app_package, _log_package]
        _path = os.path.join('cfg', f"log.{_log_type}.yml")
        _path = Pacs.sh_path_by_path(_packages, _path)
        return _path

    @staticmethod
    def sh_calendar_ts(kwargs) -> Any:
        """Set static variable log level in log configuration handlers
        """
        _log_ts_type = kwargs.get('log_ts_type', 'ts')
        if _log_ts_type == 'ts':
            return calendar.timegm(time.gmtime())
        else:
            return calendar.timegm(time.gmtime())

    @staticmethod
    def sh_level(kwargs) -> int:
        _sw_debug = kwargs.get('sw_debug', False)
        if _sw_debug:
            return logging.DEBUG
        else:
            return logging.INFO

    @staticmethod
    def sh_app_module(kwargs) -> TyStr:
        _cls_app = kwargs.get('cls_app')
        _a_app_pacmod = _cls_app.__module__.split(".")
        if len(_a_app_pacmod) > 1:
            _module: TyStr = _a_app_pacmod[1]
        else:
            _module = _a_app_pacmod[0]
        return _module

    @classmethod
    def sh_d_log_cfg(cls, kwargs: TyDic) -> TyDic:
        """Read log file path with jinja2
        """
        _d_dir_run = cls.sh_d_dir_run(kwargs)
        if kwargs.get('log_sw_mkdirs', True):
            aopath: TyArr = list(_d_dir_run.values())
            for _path in aopath:
                os.makedirs(_path, exist_ok=True)

        _path_log_cfg = cls.sh_path_log_cfg(kwargs)
        _module = cls.sh_app_module(kwargs)
        _pid = os.getpid()
        _ts = cls.sh_calendar_ts(kwargs)

        _d_log_cfg: TyDic = Jinja2_.read(
                _path_log_cfg, module=_module, pid=_pid, ts=_ts, **_d_dir_run)
        _level = cls.sh_level(kwargs)
        _log_type = kwargs.get('log_type', 'std')
        logger_name = _log_type
        _d_log_cfg['handlers'][f"{logger_name}_debug_console"]['level'] = _level
        _d_log_cfg['handlers'][f"{logger_name}_debug_file"]['level'] = _level

        return _d_log_cfg


class Log:

    sw_init: bool = False
    sw_debug: bool = False
    log: TyLogger = logging.getLogger('dummy_logger')
    # log_type: TyStr = 'std'
    # pid = os.getpid()
    # ts = calendar.timegm(time.gmtime())
    # username: TyStr = psutil.Process().username()
    # path_log_cfg: TyStr = ''
    # d_pacmod: TyDic = {}
    # d_app_pacmod: TyDic = {}

    @classmethod
    def debug(cls, *args, **kwargs) -> None:
        if kwargs is None:
            kwargs = {}
        kwargs['stacklevel'] = kwargs.get('stacklevel', 2)
        cls.log.debug(*args, **kwargs)

    @classmethod
    def info(cls, *args, **kwargs) -> None:
        if kwargs is None:
            kwargs = {}
        kwargs['stacklevel'] = kwargs.get('stacklevel', 2)
        cls.log.info(*args, **kwargs)

    @classmethod
    def warning(cls, *args, **kwargs) -> None:
        if kwargs is None:
            kwargs = {}
        kwargs['stacklevel'] = kwargs.get('stacklevel', 2)
        cls.log.warning(*args, **kwargs)

    @classmethod
    def error(cls, *args, **kwargs) -> None:
        if kwargs is None:
            kwargs = {}
        kwargs['stacklevel'] = kwargs.get('stacklevel', 2)
        cls.log.error(*args, **kwargs)

    @classmethod
    def critical(cls, *args, **kwargs) -> None:
        if kwargs is None:
            kwargs = {}
        kwargs['stacklevel'] = kwargs.get('stacklevel', 2)
        cls.log.critical(*args, **kwargs)

    @classmethod
    def init(cls, **kwargs) -> None:
        """Set static variable log level in log configuration handlers
        """
        if cls.sw_init:
            return
        # cls.log_type = kwargs.get('log_type', 'std')
        # cls.ts = cls.sh_calendar_ts(kwargs))

        # cls.d_pacmod = PacMod.sh_d_pacmod(cls)
        # cls_app = kwargs.get('cls_app')
        # cls.d_app_pacmod = PacMod.sh_d_pacmod(cls_app)

        _d_log_cfg = Utils.sh_d_log_cfg(kwargs)
        _log_type = kwargs.get('log_type', 'std')
        logging.config.dictConfig(_d_log_cfg)
        cls.log = logging.getLogger(_log_type)
        cls.sw_debug = kwargs.get('sw_debug', False)
        cls.sw_init = True

    @classmethod
    def sh(cls, **kwargs) -> Any:
        if cls.sw_init:
            return cls
            # return cls.log
        cls.init(**kwargs)
        return cls
