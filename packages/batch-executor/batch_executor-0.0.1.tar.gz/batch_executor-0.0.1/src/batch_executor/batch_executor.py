"""Main module."""
"""
批量任务执行器，支持异步、多线程和多进程三种模式
- batch_async_executor: 异步并发执行（适用于IO密集型）
- batch_thread_executor: 多线程并发（适用于IO密集型）
- batch_process_executor: 多进程并发（适用于CPU密集型）
"""
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
from typing import List, Callable, Any, Coroutine, Optional
from logger_config import setup_logger
import logging
import asyncio
from tqdm.asyncio import tqdm # Use tqdm's async-compatible version

_thread_logger = setup_logger('multi_thread', log_level="INFO")
_process_logger = setup_logger('multi_process', log_level="INFO")
_async_logger = setup_logger('multi_async', log_level="INFO")

def _process_wrapper(args):
    """外部包装函数，用于多进程执行"""
    item, idx, func = args
    try:
        result = func(item)
        return idx, result, None
    except Exception as e:
        return idx, None, e

def batch_process_executor(
    items: List[Any],
    func: Callable[[Any], Any],
    nproc: int = 5,
    task_desc: str = "",
    logger: Optional[logging.Logger] = _process_logger,
    keep_order: bool = True
) -> List[Any]:
    """
    并发执行进程任务，带进度条和并发数控制
    """
    if not len(items):
        return []

    results_with_idx = []
    failures = []
    
    desc = f"{task_desc} " if task_desc else ""
    pbar = tqdm(total=len(items), desc=desc, ncols=80, dynamic_ncols=True)

    with ProcessPoolExecutor(max_workers=nproc) as executor:
        # 准备参数
        process_args = [(item, i, func) for i, item in enumerate(items)]
        
        # 提交所有任务
        future_to_idx = {
            executor.submit(_process_wrapper, args): args[1] 
            for args in process_args
        }

        # 处理完成的任务
        for future in as_completed(future_to_idx):
            idx, result, error = future.result()
            if error:
                failures.append((idx, error))
                if logger:
                    logger.error(f"Task {idx} failed: {error}")
            results_with_idx.append((idx, result))
            pbar.update(1)

    pbar.close()

    if failures and logger:
        logger.warning(f"Total failures: {len(failures)}")
        
    if keep_order:
        results_with_idx.sort(key=lambda x: x[0])
        return [r for _, r in results_with_idx]
    else:
        return [r for _, r in results_with_idx]

def batch_thread_executor(
    items: List[Any],
    func: Callable[[Any], Any],
    nproc: int = 5,
    task_desc: str = "",
    logger: Optional[logging.Logger] = _thread_logger,
    keep_order: bool = True
) -> List[Any]:
    """
    并发执行线程任务，带进度条和并发数控制
    Args:
        items: 要处理的项目列表
        func: 函数，接受一个参数并返回结果
        nproc: 最大线程数
        task_desc: tqdm进度条描述
        logger: 日志记录器
        keep_order: 是否按输入顺序返回结果
    
    Returns:
        处理结果列表
    """
    if not len(items):
        return []

    # 定义任务函数 -> idx, result, error
    def wrapped_func(item, idx):
        try:
            result = func(item)
            if logger:
                logger.debug(f"Successfully processed item {idx}")
            return idx, result, None
        except Exception as e:
            if logger:
                logger.error(f"Error processing item {idx}: {str(e)}")
            return idx, None, e

    results_with_idx = []
    failures = []
    
    desc = f"{task_desc} " if task_desc else ""
    pbar = tqdm(total=len(items), desc=desc, ncols=80, dynamic_ncols=True)

    with ThreadPoolExecutor(max_workers=nproc) as executor:
        # 提交所有任务
        future_to_idx = {
            executor.submit(wrapped_func, item, i): i 
            for i, item in enumerate(items)
        }

        # 处理完成的任务
        for future in as_completed(future_to_idx):
            idx, result, error = future.result()
            if error:
                failures.append((idx, error))
                if logger:
                    logger.error(f"Task {idx} failed: {error}")
            results_with_idx.append((idx, result))
            pbar.update(1)

    pbar.close()

    if failures and logger:
        logger.warning(f"Total failures: {len(failures)}")
        
    if keep_order:
        # 按原始顺序排序
        results_with_idx.sort(key=lambda x: x[0])
        return [r for _, r in results_with_idx]
    else:
        # 按完成顺序返回
        return [r for _, r in results_with_idx]

async def batch_async_executor(
    items: List[Any],
    func_async: Callable[[Any], Coroutine],
    nproc: int = 5,
    task_desc: str = "",
    logger: Optional[logging.Logger] = _async_logger,
    keep_order: bool = True
) -> List[Any]:
    """
    并发执行异步任务，带进度条和并发数控制

    Args:
        items: 要处理的项目列表
        func_async: 异步函数，接受一个参数并返回一个协程
        nproc: 最大并发数
        task_desc: tqdm进度条描述
        logger: 日志记录器
        keep_order: 是否按输入顺序返回结果
    
    Returns:
        处理结果列表
    """
    if not len(items):
        return []
    sem = asyncio.Semaphore(nproc)

    # 定义任务函数 -> idx, result, error
    async def wrapped_func(item, idx):
        async with sem:
            try:
                result = await func_async(item)
                if logger:
                    logger.debug(f"Successfully processed item {idx}")
                return idx, result, None
            except Exception as e:
                if logger:
                    logger.error(f"Error processing item {idx}: {str(e)}")
                return idx, None, e
    
    tasks = [wrapped_func(item, i) for i, item in enumerate(items)]
    results_with_idx = []
    
    desc = f"{task_desc} " if task_desc else ""
    pbar = tqdm(total=len(tasks), desc=desc, ncols=80, dynamic_ncols=True)

    failures = []
    for coro in asyncio.as_completed(tasks):
        idx, result, error = await coro
        if error:
            failures.append((idx, error))
            if logger:
                logger.error(f"Task {idx} failed: {error}")
        results_with_idx.append((idx, result))
        pbar.update(1)
    pbar.close()

    if failures and logger:
        logger.warning(f"Total failures: {len(failures)}")
        
    if keep_order:
        # 按原始顺序排序
        results_with_idx.sort(key=lambda x: x[0])
        return [r for _, r in results_with_idx]
    else:
        # 按完成顺序返回
        return [r for _, r in results_with_idx]

def batch_executor(
    items: List[Any],
    func: Callable[[Any], Any],
    nproc: int = 5,
    task_desc: str = "",
    logger: Optional[logging.Logger] = _thread_logger,
    keep_order: bool = True,
):
    """
    批量执行任务，支持线程和异步执行

    Args:
        items: 要处理的项目列表
        func: 函数，接受一个参数并返回结果
        nproc: 最大线程数或并发数
        task_desc: tqdm进度条描述
        logger: 日志记录器
        keep_order: 是否按输入顺序返回结果
    
    Returns:
        处理结果列表
    """
    if not len(items):
        return []

    if asyncio.iscoroutinefunction(func):
        return asyncio.run(batch_async_executor(items, func, nproc, task_desc, logger, keep_order))
    else:
        return batch_process_executor(items, func, nproc, task_desc, logger, keep_order)
