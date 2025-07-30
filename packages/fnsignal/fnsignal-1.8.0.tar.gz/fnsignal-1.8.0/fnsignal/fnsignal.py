import time
import asyncio
import threading
from typing import Optional, Callable, Dict, Set, NoReturn
from concurrent.futures import ThreadPoolExecutor
from queue import Queue, Empty
import logging
import sys
import traceback
from contextlib import contextmanager
from functools import wraps

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('fnsignal.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# 전역 변수로 시그널 상태 관리
_signal_sender: Optional[str] = None
_signal_received: bool = False
_signal_callbacks: Dict[Callable, Optional[str]] = {}
_event_loop: Optional[asyncio.AbstractEventLoop] = None
_running_tasks: Set[asyncio.Task] = set()
_executor: Optional[ThreadPoolExecutor] = None
_lock: threading.Lock = threading.Lock()
_signal_queue: Queue = Queue()
_is_initializing: bool = False
_is_shutting_down: bool = False
_initialized: bool = False
_error_count: int = 0
_max_retries: int = 3
_task_lock: threading.Lock = threading.Lock()
_queue_lock: threading.Lock = threading.Lock()
_callback_lock: threading.Lock = threading.Lock()
_loop_lock: threading.Lock = threading.Lock()
_executor_lock: threading.Lock = threading.Lock()
_state_lock: threading.Lock = threading.Lock()
_init_lock: threading.Lock = threading.Lock()
_error_lock: threading.Lock = threading.Lock()
_signal_lock: threading.Lock = threading.Lock()

@contextmanager
def _error_handler(operation: str):
    """에러 처리를 위한 컨텍스트 매니저"""
    global _error_count
    try:
        yield
        with _error_lock:
            _error_count = 0  # 성공 시 에러 카운트 리셋
    except Exception as e:
        with _error_lock:
            _error_count += 1
            logger.error(f"{operation} 중 오류 발생: {e}\n{traceback.format_exc()}")
            if _error_count >= _max_retries:
                logger.critical(f"최대 재시도 횟수({_max_retries})를 초과했습니다. 시스템을 재초기화합니다.")
                _initialize()
                _error_count = 0
        raise

def _safe_operation(func: Callable) -> Callable:
    """안전한 작업 실행을 위한 데코레이터"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        with _error_handler(func.__name__):
            return func(*args, **kwargs)
    return wrapper

def _initialize() -> None:
    """전역 변수들을 초기화합니다."""
    global _signal_sender, _signal_received, _signal_callbacks, _event_loop, _running_tasks, _executor
    global _is_initializing, _is_shutting_down, _initialized, _error_count
    
    with _init_lock:
        if _is_initializing:
            return
        with _state_lock:
            _is_initializing = True
            _is_shutting_down = True
        
        try:
            # 진행 중인 작업이 있다면 완료될 때까지 대기
            with _loop_lock:
                if _event_loop is not None and not _event_loop.is_closed():
                    try:
                        # 이벤트 루프가 실행 중이 아닐 때만 run_until_complete 호출
                        if not _event_loop.is_running():
                            _event_loop.run_until_complete(asyncio.sleep(0.1))
                    except Exception as e:
                        logger.error(f"이벤트 루프 대기 중 오류 발생: {e}\n{traceback.format_exc()}")
            
            # 실행 중인 태스크 취소
            with _task_lock:
                for task in _running_tasks:
                    if not task.done():
                        task.cancel()
                        try:
                            with _loop_lock:
                                if _event_loop is not None and not _event_loop.is_closed():
                                    if not _event_loop.is_running():
                                        _event_loop.run_until_complete(task)
                        except asyncio.CancelledError:
                            pass
                        except Exception as e:
                            logger.error(f"태스크 취소 중 오류 발생: {e}\n{traceback.format_exc()}")
            
            # 이벤트 루프 종료
            with _loop_lock:
                if _event_loop is not None and not _event_loop.is_closed():
                    try:
                        if not _event_loop.is_running():
                            _event_loop.stop()
                        _event_loop.close()
                    except Exception as e:
                        logger.error(f"이벤트 루프 종료 중 오류 발생: {e}\n{traceback.format_exc()}")
            
            # ThreadPoolExecutor 종료
            with _executor_lock:
                if _executor is not None:
                    try:
                        _executor.shutdown(wait=True)
                    except Exception as e:
                        logger.error(f"ThreadPoolExecutor 종료 중 오류 발생: {e}\n{traceback.format_exc()}")
            
            # 상태 초기화
            with _signal_lock:
                _signal_sender = None
                _signal_received = False
            with _callback_lock:
                _signal_callbacks.clear()
            with _loop_lock:
                _event_loop = None
            with _task_lock:
                _running_tasks.clear()
            with _executor_lock:
                _executor = ThreadPoolExecutor(max_workers=1)
            with _error_lock:
                _error_count = 0
            
            # 시그널 큐 초기화
            with _queue_lock:
                while not _signal_queue.empty():
                    try:
                        _signal_queue.get_nowait()
                    except Empty:
                        break
                    except Exception as e:
                        logger.error(f"시그널 큐 초기화 중 오류 발생: {e}\n{traceback.format_exc()}")
                        break
                
        except Exception as e:
            logger.error(f"초기화 중 오류 발생: {e}\n{traceback.format_exc()}")
        finally:
            with _state_lock:
                _is_initializing = False
                _is_shutting_down = False
                _initialized = True

@_safe_operation
def send_signal(target_function: str) -> None:
    """
    특정 함수를 호출하기 위한 시그널을 보냅니다.
    
    Args:
        target_function (str): 호출할 함수의 이름
    """
    if not _initialized:
        _initialize()
        
    with _state_lock:
        if _is_shutting_down:
            logger.warning("시스템이 종료 중이어서 시그널을 보낼 수 없습니다.")
            return
        
    global _signal_sender, _signal_received
    with _lock:
        try:
            with _signal_lock:
                _signal_sender = target_function
                _signal_received = True
            with _queue_lock:
                _signal_queue.put(target_function)
            logger.debug(f"시그널 전송: {target_function}")
        except Exception as e:
            logger.error(f"시그널 전송 중 오류 발생: {e}\n{traceback.format_exc()}")
            raise

async def receive_signal_async(sender: Optional[str] = None, callback: Optional[Callable] = None) -> NoReturn:
    """
    시그널을 받았는지 비동기적으로 확인합니다.
    """
    global _signal_sender, _signal_received
    
    try:
        with _state_lock:
            if _is_shutting_down:
                return
                
        while True:
            with _state_lock:
                if _is_shutting_down:
                    break
                    
            try:
                # 시그널 큐에서 시그널 가져오기
                try:
                    with _queue_lock:
                        signal = _signal_queue.get_nowait()
                    with _lock:
                        with _signal_lock:
                            if _signal_received and (sender is None or _signal_sender == sender):
                                _signal_received = False
                                with _callback_lock:
                                    if callback and callback in _signal_callbacks:
                                        try:
                                            # 콜백을 별도 스레드에서 실행
                                            with _loop_lock, _executor_lock:
                                                if _event_loop is not None and not _event_loop.is_closed() and _executor is not None:
                                                    await _event_loop.run_in_executor(_executor, callback)
                                                    logger.debug(f"콜백 실행 완료: {callback.__name__ if hasattr(callback, '__name__') else 'unknown'}")
                                        except Exception as e:
                                            logger.error(f"콜백 실행 중 오류 발생: {e}\n{traceback.format_exc()}")
                except Empty:
                    pass
                await asyncio.sleep(0.1)
            except asyncio.CancelledError:
                logger.debug("시그널 수신 태스크가 취소되었습니다.")
                return
            except Exception as e:
                logger.error(f"시그널 수신 중 오류 발생: {e}\n{traceback.format_exc()}")
                await asyncio.sleep(0.1)
    finally:
        # 리소스 정리
        with _callback_lock:
            if callback in _signal_callbacks:
                del _signal_callbacks[callback]
                logger.debug(f"콜백 제거됨: {callback.__name__ if hasattr(callback, '__name__') else 'unknown'}")

@_safe_operation
def receive_signal(sender: Optional[str] = None, callback: Optional[Callable] = None) -> bool:
    """
    시그널을 받았는지 확인합니다. 콜백 함수가 지정되면 시그널이 올 때까지 비동기적으로 대기합니다.
    
    Args:
        sender (Optional[str]): 시그널을 보낸 함수의 이름. None이면 모든 시그널을 받습니다.
        callback (Optional[Callable]): 시그널이 왔을 때 실행할 콜백 함수
    
    Returns:
        bool: 콜백이 없는 경우에만 사용되며, 시그널을 받았으면 True
    """
    if not _initialized:
        _initialize()
        
    global _event_loop, _running_tasks, _signal_received, _signal_sender
    
    if callback is not None:
        try:
            # 콜백이 이미 등록되어 있는지 확인
            with _callback_lock:
                if callback in _signal_callbacks:
                    logger.debug(f"콜백이 이미 등록되어 있습니다: {callback.__name__ if hasattr(callback, '__name__') else 'unknown'}")
                    return True
                    
                # 이벤트 루프가 없거나 종료된 경우 새로 생성
                with _loop_lock:
                    if _event_loop is None or _event_loop.is_closed():
                        _event_loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(_event_loop)
                
                # 콜백 등록
                _signal_callbacks[callback] = sender
                logger.debug(f"콜백 등록됨: {callback.__name__ if hasattr(callback, '__name__') else 'unknown'}")
                
                # 비동기 태스크 시작
                with _loop_lock:
                    task = _event_loop.create_task(receive_signal_async(sender, callback))
                with _task_lock:
                    _running_tasks.add(task)
                return True
        except Exception as e:
            logger.error(f"시그널 등록 중 오류 발생: {e}\n{traceback.format_exc()}")
            return False
    
    # 콜백이 없는 경우 기존 동기 처리
    with _lock:
        try:
            with _signal_lock:
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
        except Exception as e:
            logger.error(f"시그널 확인 중 오류 발생: {e}\n{traceback.format_exc()}")
            return False

@_safe_operation
def wait_for_signals() -> bool:
    """
    모든 시그널 처리가 완료될 때까지 대기합니다.
    
    Returns:
        bool: 모든 시그널이 성공적으로 처리되었으면 True, 아니면 False
    """
    if not _initialized:
        _initialize()
        
    global _event_loop, _running_tasks
    with _loop_lock:
        if _event_loop is not None and _running_tasks:
            try:
                # 모든 시그널이 처리될 때까지 대기
                if not _event_loop.is_running():
                    _event_loop.run_until_complete(asyncio.sleep(0.5))
                
                # 실행 중인 태스크 취소
                with _task_lock:
                    for task in _running_tasks:
                        if not task.done():
                            task.cancel()
                            try:
                                if not _event_loop.is_running():
                                    _event_loop.run_until_complete(task)
                            except asyncio.CancelledError:
                                pass
                            except Exception as e:
                                logger.error(f"태스크 취소 중 오류 발생: {e}\n{traceback.format_exc()}")
                
                # 이벤트 루프 종료
                if not _event_loop.is_closed():
                    try:
                        if not _event_loop.is_running():
                            _event_loop.stop()
                        _event_loop.close()
                    except Exception as e:
                        logger.error(f"이벤트 루프 종료 중 오류 발생: {e}\n{traceback.format_exc()}")
                
                _event_loop = None
                with _task_lock:
                    _running_tasks.clear()
                
                # 상태 초기화
                _initialize()
                return True
            except Exception as e:
                logger.error(f"시그널 대기 중 오류 발생: {e}\n{traceback.format_exc()}")
                # 오류 발생 시에도 리소스 정리
                _initialize()
                return False
    return True

# 초기화
_initialize()