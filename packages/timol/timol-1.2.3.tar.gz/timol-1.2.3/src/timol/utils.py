import time
from collections import defaultdict
from typing import Callable, Dict, List, Optional, Tuple

import numpy as np
import tqdm


class Benchmarker:
    starts: Dict[str, Tuple]
    running: Dict[str, bool]
    times: Dict[str, List]

    def __init__(self):
        self.starts = {}
        self.times = defaultdict(list)
        self.running = defaultdict(lambda: False)

        self.wake()

    def get_current_times(self) -> Tuple[float, float]:
        return time.perf_counter(), time.process_time()

    def start(self, name: str):
        self.running[name] = True
        self.starts[name] = self.get_current_times()

    def stop(self, name: str):
        if not self.running[name]:
            raise Exception(
                f"Benchmarker tried to stop clock `{name}`, but no such clock is currently running"
            )
        self.running[name] = False
        perf_counter, process_time = self.get_current_times()
        perf_counter0, process_time0 = self.starts[name]
        self.times[name].append(
            [perf_counter - perf_counter0, process_time - process_time0]
        )
        del self.starts[name]

    def lap(self, name: str):
        self.stop(name)
        self.start(name)

    def get_average_time(self, name: str) -> Tuple[float, float]:
        avg = np.mean(self.times[name], axis=0)
        return float(avg[0]), float(avg[1])

    def get_total_time(self, name: str) -> Tuple[float, float]:
        sum = np.sum(self.times[name], axis=0)
        return float(sum[0]), float(sum[1])

    def get_times(self, name: str) -> Tuple[np.ndarray, np.ndarray]:
        times = np.array(self.times[name])
        return times[:, 0], times[:, 1]

    def run_n_times(
        self,
        name: str,
        N: int,
        foo: Callable,
        args: Optional[List],
        desc: Optional[str] = None,
    ):
        for i in tqdm.tqdm(range(N), desc=desc):
            self.start(name)
            if args is None:
                foo()
            else:
                foo(*args[i])
            self.stop(name)

    def get_names(self) -> List[str]:
        return list(self.times.keys())

    def to_dict(self) -> dict:
        return {
            "starts": dict(self.starts),
            "running": dict(self.running),
            "times": dict(self.times),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Benchmarker":
        bm = Benchmarker()
        bm.starts = d["starts"]
        bm.running = d["running"]
        bm.times = d["times"]
        return bm

    def combine(self, bmarker: "Benchmarker"):
        for k in bmarker.starts:
            self.starts[k] = bmarker.starts[k]

        for k in bmarker.running:
            self.running[k] = bmarker.running[k] or self.running[k]

        for k in bmarker.times:
            self.times[k].extend(bmarker.times[k])

    def wake(self):
        if "total_time" in self.running:
            return
        self.start("total_time")

    def sleep(self):
        if "total_time" not in self.running:
            return
        self.stop("total_time")

    def generic_print(self):
        self.sleep()

        all_total_times = {
            name: self.get_total_time(name)[0] for name in self.get_names()
        }
        print("Benchmark:")
        for name, tot_time in sorted(
            all_total_times.items(), key=lambda item: item[1], reverse=True
        ):
            print(f"{name:<30}{tot_time:.2f}")
        self.wake()
