
import platform

if platform.system() == "Windows":
    from .install_packeges import configPaths, start
else:
    from .install_packeges_linux import configPaths, start

from .maneger import stepComplete, statusProdution, checkVideos, config, getThemeLesson, priorityQueur

__all__ = ['configPaths','start','stepComplete', 'statusProdution', 'checkVideos', 'config', 'getThemeLesson', 'priorityQueur']