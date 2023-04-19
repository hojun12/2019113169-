import sys
from typing import Any, List, Optional, TextIO, Type
from types import TracebackType
import inspect
import linecache

class LFTracer:
    def __init__(self, target_func: List[str] = [], list_func: bool = False, file: TextIO = sys.stdout) -> None:
        self.target_func = target_func
        self.list_func = list_func
        self.file = file
        self.lf_map = {func: {} for func in self.target_func}

    def trace(self, frame, event, arg):
        if event == "line":
            func_name = frame.f_code.co_name
            if func_name in self.target_func:
                lineno = frame.f_lineno
                if lineno not in self.lf_map[func_name]:
                    self.lf_map[func_name][lineno] = 0
                self.lf_map[func_name][lineno] += 1

        return self.trace

    def __enter__(self) -> Any:
        sys.settrace(self.trace)
        return self

    def __exit__(self, exc_tp: Type, exc_value: BaseException, exc_traceback: TracebackType) -> Optional[bool]:
        sys.settrace(None)
        if self.list_func:
            for func in self.lf_map:
                self.file.write(f"{func}:\n")
                for lineno, count in self.lf_map[func].items():
                    line = linecache.getline(inspect.currentframe().f_back.f_code.co_filename, lineno).strip()
                    self.file.write(f"\tLine {lineno} ({count}): {line}\n")

        return None

    def getLFMap(self):
        return self.lf_map
