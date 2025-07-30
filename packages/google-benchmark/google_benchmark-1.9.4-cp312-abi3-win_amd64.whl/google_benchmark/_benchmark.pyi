from collections.abc import Callable, Iterator, Sequence
import enum
from typing import overload


class TimeUnit(enum.Enum):
    kNanosecond = 0

    kMicrosecond = 1

    kMillisecond = 2

    kSecond = 3

kNanosecond: TimeUnit = TimeUnit.kNanosecond

kMicrosecond: TimeUnit = TimeUnit.kMicrosecond

kMillisecond: TimeUnit = TimeUnit.kMillisecond

kSecond: TimeUnit = TimeUnit.kSecond

class BigO(enum.Enum):
    oNone = 0

    o1 = 1

    oN = 2

    oNSquared = 3

    oNCubed = 4

    oLogN = 5

    oNLogN = 6

    oAuto = 7

    oLambda = 8

oNone: BigO = BigO.oNone

o1: BigO = BigO.o1

oN: BigO = BigO.oN

oNSquared: BigO = BigO.oNSquared

oNCubed: BigO = BigO.oNCubed

oLogN: BigO = BigO.oLogN

oNLogN: BigO = BigO.oNLogN

oAuto: BigO = BigO.oAuto

oLambda: BigO = BigO.oLambda

class Benchmark:
    def unit(self, arg: TimeUnit, /) -> Benchmark: ...

    def arg(self, arg: int, /) -> Benchmark: ...

    def args(self, arg: Sequence[int], /) -> Benchmark: ...

    def range(self, start: int, limit: int) -> Benchmark: ...

    def dense_range(self, start: int, limit: int, step: int = 1) -> Benchmark: ...

    def ranges(self, arg: Sequence[tuple[int, int]], /) -> Benchmark: ...

    def args_product(self, arg: Sequence[Sequence[int]], /) -> Benchmark: ...

    def arg_name(self, arg: str, /) -> Benchmark: ...

    def arg_names(self, arg: Sequence[str], /) -> Benchmark: ...

    def range_pair(self, lo1: int, hi1: int, lo2: int, hi2: int) -> Benchmark: ...

    def range_multiplier(self, arg: int, /) -> Benchmark: ...

    def min_time(self, arg: float, /) -> Benchmark: ...

    def min_warmup_time(self, arg: float, /) -> Benchmark: ...

    def iterations(self, arg: int, /) -> Benchmark: ...

    def repetitions(self, arg: int, /) -> Benchmark: ...

    def report_aggregates_only(self, value: bool = True) -> Benchmark: ...

    def display_aggregates_only(self, value: bool = True) -> Benchmark: ...

    def measure_process_cpu_time(self) -> Benchmark: ...

    def use_real_time(self) -> Benchmark: ...

    def use_manual_time(self) -> Benchmark: ...

    def complexity(self, complexity: BigO = BigO.oAuto) -> Benchmark: ...

class Counter:
    @overload
    def __init__(self, value: float = 0.0, flags: Counter.Flags = 0, k: Counter.OneK = Counter.OneK.kIs1000) -> None: ...

    @overload
    def __init__(self, arg: float, /) -> None: ...

    @overload
    def __init__(self, arg: float, /) -> None: ...

    class Flags(enum.IntFlag):
        __str__ = __repr__

        def __repr__(self, /):
            """Return repr(self)."""

        kDefaults = 0

        kIsRate = 1

        kAvgThreads = 2

        kAvgThreadsRate = 3

        kIsIterationInvariant = 4

        kIsIterationInvariantRate = 5

        kAvgIterations = 8

        kAvgIterationsRate = 9

        kInvert = -2147483648

    kDefaults: Counter.Flags = 0

    kIsRate: Counter.Flags = 1

    kAvgThreads: Counter.Flags = 2

    kAvgThreadsRate: Counter.Flags = 3

    kIsIterationInvariant: Counter.Flags = 4

    kIsIterationInvariantRate: Counter.Flags = 5

    kAvgIterations: Counter.Flags = 8

    kAvgIterationsRate: Counter.Flags = 9

    kInvert: Counter.Flags = -2147483648

    class OneK(enum.Enum):
        kIs1000 = 1000

        kIs1024 = 1024

    kIs1000: Counter.OneK = Counter.OneK.kIs1000

    kIs1024: Counter.OneK = Counter.OneK.kIs1024

    @property
    def value(self) -> float: ...

    @value.setter
    def value(self, arg: float, /) -> None: ...

    @property
    def flags(self) -> Counter.Flags: ...

    @flags.setter
    def flags(self, arg: Counter.Flags, /) -> None: ...

    @property
    def oneK(self) -> Counter.OneK: ...

    @oneK.setter
    def oneK(self, arg: Counter.OneK, /) -> None: ...

class UserCounters:
    @overload
    def __init__(self) -> None:
        """Default constructor"""

    @overload
    def __init__(self, arg: UserCounters) -> None:
        """Copy constructor"""

    @overload
    def __init__(self, arg: dict[str, Counter], /) -> None:
        """Construct from a dictionary"""

    def __len__(self) -> int: ...

    def __bool__(self) -> bool:
        """Check whether the map is nonempty"""

    def __repr__(self) -> str: ...

    @overload
    def __contains__(self, arg: str, /) -> bool: ...

    @overload
    def __contains__(self, arg: object, /) -> bool: ...

    def __iter__(self) -> Iterator[str]: ...

    def __getitem__(self, arg: str, /) -> Counter: ...

    def __delitem__(self, arg: str, /) -> None: ...

    def clear(self) -> None:
        """Remove all items"""

    def __setitem__(self, arg0: str, arg1: Counter, /) -> None: ...

    def update(self, arg: UserCounters, /) -> None:
        """Update the map with element from `arg`"""

    def __eq__(self, arg: object, /) -> bool: ...

    def __ne__(self, arg: object, /) -> bool: ...

    class ItemView:
        def __len__(self) -> int: ...

        def __iter__(self) -> Iterator[tuple[str, Counter]]: ...

    class KeyView:
        @overload
        def __contains__(self, arg: str, /) -> bool: ...

        @overload
        def __contains__(self, arg: object, /) -> bool: ...

        def __len__(self) -> int: ...

        def __iter__(self) -> Iterator[str]: ...

    class ValueView:
        def __len__(self) -> int: ...

        def __iter__(self) -> Iterator[Counter]: ...

    def keys(self) -> UserCounters.KeyView:
        """Returns an iterable view of the map's keys."""

    def values(self) -> UserCounters.ValueView:
        """Returns an iterable view of the map's values."""

    def items(self) -> UserCounters.ItemView:
        """Returns an iterable view of the map's items."""

class State:
    def __bool__(self) -> bool: ...

    @property
    def keep_running(self) -> bool: ...

    def pause_timing(self) -> None: ...

    def resume_timing(self) -> None: ...

    def skip_with_error(self, arg: str, /) -> None: ...

    @property
    def error_occurred(self) -> bool: ...

    def set_iteration_time(self, arg: float, /) -> None: ...

    @property
    def bytes_processed(self) -> int: ...

    @bytes_processed.setter
    def bytes_processed(self, arg: int, /) -> None: ...

    @property
    def complexity_n(self) -> int: ...

    @complexity_n.setter
    def complexity_n(self, arg: int, /) -> None: ...

    @property
    def items_processed(self) -> int: ...

    @items_processed.setter
    def items_processed(self, arg: int, /) -> None: ...

    def set_label(self, arg: str, /) -> None: ...

    def range(self, pos: int = 0) -> int: ...

    @property
    def iterations(self) -> int: ...

    @property
    def name(self) -> str: ...

    @property
    def counters(self) -> UserCounters: ...

    @counters.setter
    def counters(self, arg: UserCounters, /) -> None: ...

    @property
    def thread_index(self) -> int: ...

    @property
    def threads(self) -> int: ...

def Initialize(arg: Sequence[str], /) -> list[str]: ...

def RegisterBenchmark(arg0: str, arg1: Callable, /) -> Benchmark: ...

def RunSpecifiedBenchmarks() -> None: ...

def ClearRegisteredBenchmarks() -> None: ...
