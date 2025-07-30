"""剪映自动化控制，主要与自动导出有关（此版本移除了对uiautomation的依赖）"""

from enum import Enum
from typing import Optional, Literal, Callable

class Export_resolution(Enum):
    """导出分辨率"""
    RES_8K = "8K"
    RES_4K = "4K"
    RES_2K = "2K"
    RES_1080P = "1080P"
    RES_720P = "720P"
    RES_480P = "480P"

class Export_framerate(Enum):
    """导出帧率"""
    FR_24 = "24fps"
    FR_25 = "25fps"
    FR_30 = "30fps"
    FR_50 = "50fps"
    FR_60 = "60fps"

# 注意：此版本的Jianying_controller类是一个虚拟类，不包含任何实际功能
# 仅用于保持API兼容性，避免导入错误
class Jianying_controller:
    """剪映控制器（虚拟类，不包含实际功能）
    
    注意：此版本移除了对uiautomation的依赖，不能实际控制剪映
    仅保留类定义以避免导入错误
    """
    
    def __init__(self):
        """初始化剪映控制器（虚拟实现）"""
        raise NotImplementedError("此版本的Jianying_controller已移除对uiautomation的依赖，不能实际使用")
    
    def export_draft(self, draft_name: str, output_path: Optional[str] = None, *,
                     resolution: Optional[Export_resolution] = None,
                     framerate: Optional[Export_framerate] = None,
                     timeout: float = 1200) -> None:
        """导出指定的剪映草稿（虚拟实现）"""
        raise NotImplementedError("此版本的Jianying_controller已移除对uiautomation的依赖，不能实际使用")
    
    def switch_to_home(self) -> None:
        """切换到剪映主页（虚拟实现）"""
        raise NotImplementedError("此版本的Jianying_controller已移除对uiautomation的依赖，不能实际使用")
    
    def get_window(self) -> None:
        """获取剪映窗口（虚拟实现）"""
        raise NotImplementedError("此版本的Jianying_controller已移除对uiautomation的依赖，不能实际使用")
