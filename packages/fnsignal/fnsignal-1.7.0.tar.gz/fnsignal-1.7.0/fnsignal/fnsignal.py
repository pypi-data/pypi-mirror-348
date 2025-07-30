import time
import asyncio
from typing import Optional, Callable

# 전역 변수로 시그널 상태 관리
_signal_sender: Optional[str] = None
_signal_received = False
_signal_callbacks = {}
_event_loop = None
_running_tasks = set()

def send_signal(target_function: str) -> None:
    """
    특정 함수를 호출하기 위한 시그널을 보냅니다.
    
    Args:
        target_function (str): 호출할 함수의 이름
    """
    global _signal_sender, _signal_received
    _signal_sender = target_function
    _signal_received = True

async def receive_signal_async(sender: Optional[str] = None, callback: Optional[Callable] = None) -> bool:
    """
    시그널을 받았는지 비동기적으로 확인합니다.
    """
    global _signal_sender, _signal_received
    
    while True:
        if _signal_received and (sender is None or _signal_sender == sender):
            _signal_received = False
            if callback:
                callback()
        await asyncio.sleep(0.1)

def receive_signal(sender: Optional[str] = None, callback: Optional[Callable] = None) -> bool:
    """
    시그널을 받았는지 확인합니다. 콜백 함수가 지정되면 시그널이 올 때까지 비동기적으로 대기합니다.
    
    Args:
        sender (Optional[str]): 시그널을 보낸 함수의 이름. None이면 모든 시그널을 받습니다.
        callback (Optional[Callable]): 시그널이 왔을 때 실행할 콜백 함수
    
    Returns:
        bool: 콜백이 없는 경우에만 사용되며, 시그널을 받았으면 True
    """
    global _event_loop, _running_tasks, _signal_received, _signal_sender
    
    if callback is not None:
        # 이벤트 루프가 없으면 생성
        if _event_loop is None:
            _event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(_event_loop)
        
        # 비동기 태스크 시작
        task = _event_loop.create_task(receive_signal_async(sender, callback))
        _running_tasks.add(task)
        return True
    
    # 콜백이 없는 경우 기존 동기 처리
    if not _signal_received:
        return False
        
    if sender is None:
        result = _signal_received
        _signal_received = False
        return result
        
    if _signal_sender == sender:
        result = _signal_received
        _signal_received = False
        return result
    
    return False

def wait_for_signals() -> bool:
    """
    모든 시그널 처리가 완료될 때까지 대기합니다.
    
    Returns:
        bool: 모든 시그널이 성공적으로 처리되었으면 True, 아니면 False
    """
    global _event_loop, _running_tasks
    if _event_loop is not None and _running_tasks:
        try:
            _event_loop.run_until_complete(asyncio.gather(*_running_tasks))
            _running_tasks.clear()
            return True
        except Exception:
            return False
    return True