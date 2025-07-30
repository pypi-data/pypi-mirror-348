import logging
import sys
from pathlib import Path
from typing import Optional

# Níveis customizados
SUCCESS_LEVEL = 25
STARTUP_LEVEL = 15
VALIDATION_LEVEL = 21
DRY_RUN_LEVEL = 16

logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")
logging.addLevelName(STARTUP_LEVEL, "STARTUP")
logging.addLevelName(VALIDATION_LEVEL, "VALIDATION")
logging.addLevelName(DRY_RUN_LEVEL, "DRY_RUN")

def success(self, message, *args, **kwargs):
    if self.isEnabledFor(SUCCESS_LEVEL):
        self._log(SUCCESS_LEVEL, message, args, **kwargs)

def startup(self, message, *args, **kwargs):
    if self.isEnabledFor(STARTUP_LEVEL):
        self._log(STARTUP_LEVEL, message, args, **kwargs)

def validation(self, message, *args, **kwargs):
    if self.isEnabledFor(VALIDATION_LEVEL):
        self._log(VALIDATION_LEVEL, message, args, **kwargs)

def dry_run(self, message, *args, **kwargs):
    if self.isEnabledFor(DRY_RUN_LEVEL):
        self._log(DRY_RUN_LEVEL, message, args, **kwargs)

logging.Logger.success = success
logging.Logger.startup = startup
logging.Logger.validation = validation
logging.Logger.dry_run = dry_run

def get_logger(
    name: str,
    level: int = logging.DEBUG,
    log_to_file: bool = False,
    log_file_path: Optional[str] = None,
    use_colors: bool = True,
    overwrite_handlers: bool = False
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if overwrite_handlers:
        logger.handlers.clear()

    if not logger.handlers:
        try:
            import colorlog
            formatter = colorlog.ColoredFormatter(
                fmt="%(log_color)s[%(asctime)s] [%(levelname)s] : %(message)s",
                datefmt="%H:%M:%S",
                log_colors={
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'bold_red',
                    'SUCCESS': 'bold_green',
                    'STARTUP': 'bold_blue',
                    'VALIDATION': 'blue',
                    'DRY_RUN': 'purple',
                }
            )
        except ImportError:
            formatter = logging.Formatter(
                fmt="[%(asctime)s] [%(levelname)s] : %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        if log_to_file and log_file_path:
            log_path = Path(log_file_path)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_path, encoding='utf-8')
            file_handler.setFormatter(logging.Formatter(
                fmt="[%(asctime)s] [%(levelname)s] : %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            ))
            logger.addHandler(file_handler)

    logger.propagate = False
    return logger
