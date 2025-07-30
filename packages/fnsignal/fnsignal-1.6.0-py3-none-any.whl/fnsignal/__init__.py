from .fnsignal import (
    send_signal,
    receive_signal,
    receive_signal_async,
    wait_for_signals
)

__version__ = "1.6.0"

# 패키지 레벨에서 함수들을 직접 사용할 수 있게 함
__all__ = ["send_signal", "receive_signal", "receive_signal_async", "wait_for_signals"]

# 패키지 레벨에 함수들을 직접 할당
globals().update({
    "send_signal": send_signal,
    "receive_signal": receive_signal,
    "receive_signal_async": receive_signal_async,
    "wait_for_signals": wait_for_signals
}) 