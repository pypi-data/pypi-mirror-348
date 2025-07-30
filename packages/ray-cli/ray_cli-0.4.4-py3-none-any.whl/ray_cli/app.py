import time
from typing import Generator, Optional

from ray_cli.dispatchers import SACNDispatcher
from ray_cli.modes import DmxDataGenerator
from ray_cli.utils import Feedback, ProgressBar, TableLogger


class Throttle:
    def __init__(self, rate: int):
        self._rate = rate if rate >= 0 else 1
        self.last_tick = time.perf_counter()

    @property
    def rate(self) -> int:
        return self._rate

    @property
    def time_step(self) -> float:
        return 1 / self._rate

    def wait_next(self):
        target_tick = self.last_tick + self.time_step
        now = time.perf_counter()

        if now < target_tick:
            time_to_sleep = target_tick - now
            time.sleep(time_to_sleep)

        self.last_tick = target_tick

    def loop(self, duration: Optional[int] = None) -> Generator[int, None, None]:
        ticks = 0
        max_ticks = (self.rate * duration) if duration else None
        while max_ticks is None or ticks < max_ticks:
            self.wait_next()
            yield ticks
            ticks += 1


class App:
    def __init__(
        self,
        dispatcher: SACNDispatcher,
        generator: DmxDataGenerator,
        channels: int,
        fps: int,
        duration: Optional[int] = None,
    ):
        self.dispatcher = dispatcher
        self.generator = generator
        self.channels = channels
        self.fps = fps
        self.duration = duration
        self.throttle = Throttle(fps)

        self.table_logger = TableLogger(channels)
        self.progress_bar = ProgressBar((fps * duration) if duration else None)

    def purge_output(self):
        with self.dispatcher:
            self._purge_output()

    def _purge_output(self):
        self.dispatcher.send([0 for _ in range(self.channels)])

    def run(
        self,
        feedback: Optional[Feedback] = None,
        dry=False,
    ):
        with self.dispatcher:
            t_start = time.time()
            for i in self.throttle.loop(self.duration):
                payload = next(self.generator)

                if not dry:
                    self.dispatcher.send(payload)

                if feedback == Feedback.TABULAR:
                    self.table_logger.report(i + 1, payload)

                elif feedback == Feedback.PROGRESS_BAR:
                    self.progress_bar.report(i + 1, time.time() - t_start)

            if not dry:
                self._purge_output()
