# coding=utf-8
from typing import Any

from datetime import datetime
import subprocess

from ka_uts_log.log import LogEq

TyClsName = Any
TyModName = Any
TyPacName = Any
TyPacModName = Any
TyFncName = Any


class Srv:

    @staticmethod
    def get_start_timestamp(service_name):
        """
        show module name of function
        """
        cmds = ["systemctl", "show", service_name, "--property=ExecMainStartTimestamp"]
        try:
            # Run the systemctl command to get service details
            result = subprocess.run(
                cmds,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )

            # Extract the start timestamp from the output
            output = result.stdout.strip()
            if output.startswith("ExecMainStartTimestamp="):
                _start_time = output.split("=", 1)[1]
                LogEq.debug("_start_time", _start_time)
                _start_timestamp = datetime.strptime(
                        _start_time, "%a %Y-%m-%d %H:%M:%S %Z").timestamp()
                LogEq.debug("_start_timestamp", _start_timestamp)
                return _start_timestamp
            else:
                msg = "Start time not available or service not running."
                raise Exception(msg)
        except subprocess.CalledProcessError as e:
            msg = f"Error retrieving service information: {e}"
            raise Exception(msg)
