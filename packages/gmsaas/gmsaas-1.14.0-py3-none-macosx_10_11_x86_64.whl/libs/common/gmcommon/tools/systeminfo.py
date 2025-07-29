import multiprocessing
import platform


IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"
IS_MACOS = platform.system() == "Darwin"

NPROC = multiprocessing.cpu_count()
