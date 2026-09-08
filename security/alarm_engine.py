import threading
import time


_alarm_thread = None
_alarm_stop_event = threading.Event()
_alarm_active = False


def _alarm_loop() -> None:
    global _alarm_active

    try:
        import winsound

        while not _alarm_stop_event.is_set():
            winsound.Beep(1200, 500)

            if _alarm_stop_event.wait(0.2):
                break

            winsound.Beep(800, 500)

            if _alarm_stop_event.wait(0.2):
                break

    except ImportError:
        while not _alarm_stop_event.wait(1):
            pass

    finally:
        _alarm_active = False


def start_alarm() -> None:
    global _alarm_thread
    global _alarm_active

    if _alarm_active:
        return

    _alarm_stop_event.clear()
    _alarm_active = True

    _alarm_thread = threading.Thread(
        target=_alarm_loop,
        daemon=True,
    )

    _alarm_thread.start()


def stop_alarm() -> None:
    global _alarm_active

    _alarm_stop_event.set()
    _alarm_active = False


def is_alarm_active() -> bool:
    return _alarm_active