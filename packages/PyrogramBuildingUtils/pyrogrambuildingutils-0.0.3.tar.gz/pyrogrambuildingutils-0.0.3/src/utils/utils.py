import time
import traceback
from typing import Any, Callable


class Utils:
    @staticmethod
    def init_time_measure(*, silent: bool = False):
        def decorator(func: Callable[..., Any]):
            def wrapper(*args, **kwargs) -> Any:
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                except Exception:
                    print("INIT ERROR: ")
                    traceback.print_exc()
                    exit(1)
                end_time = time.time()
                if args and hasattr(args[0], "__class__"):
                    cls = args[0].__class__
                    if hasattr(cls, "logger"):
                        total_time = end_time - start_time
                        if not silent:
                            cls.logger.info(
                                f"Initialization {cls.__name__} complete on {total_time:.2f}s"
                            )
                return result

            return wrapper

        return decorator

    @staticmethod
    def clear_pycache():
        exec(
            "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
        )
        exec(
            "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"
        )
