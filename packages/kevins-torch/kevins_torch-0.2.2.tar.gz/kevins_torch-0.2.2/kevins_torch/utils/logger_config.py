import logging
import os
from typing import Optional


def setup_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """設置並返回一個配置好的 logger。

    Args:
        name: logger 的名稱
        level: 日誌級別，如果為 None 則根據環境變量設置

    Returns:
        logging.Logger: 配置好的 logger 實例
    """
    logger = logging.getLogger(name)
    
    # 如果 logger 已經有處理器，則直接返回
    if logger.handlers:
        return logger
    
    # 設置日誌級別
    is_debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
    level = logging.DEBUG if is_debug_mode else logging.WARNING
   
    logger.setLevel(level)
    
    # 創建控制台處理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # 創建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # 添加處理器到 logger
    logger.addHandler(console_handler)
    
    return logger
