import logging
from pathlib import Path
from typing import Optional, Union, Literal

def setup_logger(
    name: str,
    log_file: Optional[Union[str, Path]] = None,
    console: bool = True,
    log_level: Union[str, int] = "INFO",
    file_log_level: Optional[Union[str, int]] = None,
    console_log_level: Optional[Union[str, int]] = None,
    format_type: Literal["simple", "detailed"] = "simple",
    file_mode: Literal["w", "a"] = "w",
    encoding: str = "utf-8"
) -> logging.Logger:
    """
    设置并返回一个配置好的logger实例
    
    Args:
        name: logger的名称
        log_file: 日志文件路径，如果不指定则不记录到文件
        console: 是否输出到控制台
        log_level: 总体日志级别
        file_log_level: 文件日志级别，不指定则使用log_level
        console_log_level: 控制台日志级别，不指定则使用log_level
        format_type: 日志格式类型，"simple" 或 "detailed"
        file_mode: 文件写入模式，"w"覆盖，"a"追加
        encoding: 文件编码
    
    Returns:
        配置好的logger实例
    """
    # 创建logger
    logger = logging.getLogger(name)
    
    # 清除已存在的处理器
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # 设置总体日志级别
    logger.setLevel(log_level)
    
    # 定义日志格式
    if format_type == "simple":
        console_fmt = "%(levelname)s: %(message)s"
        file_fmt = "%(asctime)s - %(levelname)s: %(message)s"
    else:
        console_fmt = "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
        file_fmt = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
    
    # 控制台输出
    if console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_log_level or log_level)
        console_formatter = logging.Formatter(console_fmt)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    # 文件输出
    if log_file:
        # 确保目录存在
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 创建文件处理器
        file_handler = logging.FileHandler(
            log_file, 
            mode=file_mode,
            encoding=encoding
        )
        file_handler.setLevel(file_log_level or log_level)
        file_formatter = logging.Formatter(file_fmt)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger