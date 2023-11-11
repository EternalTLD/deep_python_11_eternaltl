import cProfile
import pstats
import io


class ProfileDeco:
    def __init__(self, function):
        self.function = function
        self.profiler = cProfile.Profile()

    def __call__(self, *args, **kwargs):
        self.profiler.enable()
        result = self.function(*args, **kwargs)
        self.profiler.disable()
        return result

    def print_stat(self):
        string = io.StringIO()
        sort_by = pstats.SortKey.CUMULATIVE
        stats = pstats.Stats(self.profiler, stream=string).sort_stats(sort_by)
        stats.print_stats()
        print(string.getvalue())
