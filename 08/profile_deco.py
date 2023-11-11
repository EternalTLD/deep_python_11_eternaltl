import cProfile
import pstats
import io
from typing import Any
from collections.abc import Callable


class ProfileDeco:
    def __init__(self, function: Callable) -> None:
        self.function = function
        self.profiler = cProfile.Profile()

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        self.profiler.enable()
        result = self.function(*args, **kwargs)
        self.profiler.disable()
        return result

    def print_stat(self) -> None:
        s = io.StringIO()
        sortby = pstats.SortKey.CUMULATIVE
        stats = pstats.Stats(self.profiler, stream=s).sort_stats(sortby)
        stats.print_stats("^(?!.*disable).*$")
        print(s.getvalue())


@ProfileDeco
def add(a, b):
    return a + b


@ProfileDeco
def sub(a, b):
    return a - b


if __name__ == "__main__":
    add(1, 1)
    add(1, 1)
    sub(1, 1)

    add.print_stat()
    sub.print_stat()
