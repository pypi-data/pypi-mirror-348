"""
Decorators Module
"""
import numpy as np
from datetime import datetime
from ka_uts_uts.utils.fnc import Fnc
from ka_uts_log.log import Log


def timer(fnc):
    """
    Timer Decorator
    """
    def wrapper(*args, **kwargs):
        start = datetime.now()
        fnc(*args, **kwargs)
        _fnc_name = Fnc.sh_fnc_name(fnc)
        end = datetime.now()
        elapse_time = end.timestamp() - start.timestamp()
        np_elapse_time = np.format_float_positional(elapse_time, trim='k')
        msg = f"{_fnc_name} elapse time [sec] = {np_elapse_time}"
        Log.info(msg, stacklevel=2)
    return wrapper
