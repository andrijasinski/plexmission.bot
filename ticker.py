import logging
import threading
import time
import traceback


class Ticker(object):
    @classmethod
    def start_ticker(cls, times, delay, function):
        subthread = threading.Thread(target=cls._tick, args=(times, delay, function,))
        subthread.start()
        logging.info(f"== Started {repr(subthread)}")

    @staticmethod
    def _tick(times, delay, function):
        for _ in range(times):
            try:
                time.sleep(delay)
                function()
            except Exception:
                tb = traceback.format_exc()
                logging.error(f"Error running {function.__name__}:\n{tb}")
