import logging
import colorlog
import time
import inspect

class tracecolor(logging.Logger):
    """
    Enhanced logger with colorized output and TRACE/PROGRESS levels.
    
    Features:
    - Custom TRACE logging level (5, lower than DEBUG)
    - Custom PROGRESS logging level (15, between DEBUG and INFO)
    - Colorized output for different log levels
    - Rate-limiting for PROGRESS messages (once per second)
    - Timestamped log format
    
    Usage:
    ```python
    from tracecolor import tracecolor
    
    logger = tracecolor(__name__)
    logger.trace("Detailed trace message")
    logger.debug("Debug information")
    logger.progress("Progress update (rate-limited)")
    logger.info("General information")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical error")
    ```
    """
    TRACE_LEVEL = 5  # TRACE below DEBUG (10)
    PROGRESS_LEVEL = 15  # PROGRESS between DEBUG (10) and INFO (20)
    PROGRESS_INTERVAL: float = 1  # Default interval in seconds for progress messages (0 or less disables rate-limiting for testing)

    def __init__(self, name):
        super().__init__(name)

        # Register custom levels
        logging.addLevelName(self.TRACE_LEVEL, "TRACE")
        logging.addLevelName(self.PROGRESS_LEVEL, "PROGRESS")

        # Set up color formatter for standard log levels
        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(levelname).1s%(reset)s |%(asctime)s.%(msecs)03d| %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
                'TRACE': 'bold_black',  # Use bold_black for gray
                'PROGRESS': 'blue',
            }
        )

        # Console handler for standard log levels
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.addHandler(console_handler)

        # Set the logger level to the lowest to capture all messages
        self.setLevel(self.TRACE_LEVEL)
        self.propagate = False

        # Initialize last log time for rate-limiting
        self._last_progress_log_times = {}

    def trace(self, message, *args, **kwargs):
        """Log a message with severity 'TRACE'."""
        if self.level <= self.TRACE_LEVEL:
            self.log(self.TRACE_LEVEL, message, *args, **kwargs)

    def progress(self, message, *args, **kwargs):
        """Log a message with severity 'PROGRESS' (for progress updates, rate-limited per call site)."""
        # First, check if the logger is even enabled for the PROGRESS level.
        # This is the standard check: PROGRESS_LEVEL (15) must be >= logger.getEffectiveLevel().
        if not self.isEnabledFor(self.PROGRESS_LEVEL):
            return

        # If PROGRESS_INTERVAL is non-positive, log directly and bypass rate-limiting
        if self.PROGRESS_INTERVAL <= 0:
            # Directly call _log as per instruction, handling relevant kwargs
            exc_info_val = kwargs.get('exc_info')
            extra_val = kwargs.get('extra')
            stack_info_val = kwargs.get('stack_info', False)
            # stacklevel=2 ensures findCaller in _log points to the caller of progress()
            super()._log(self.PROGRESS_LEVEL, message, args, exc_info=exc_info_val, extra=extra_val, stack_info=stack_info_val, stacklevel=2)
            return

        # Per-call-site rate-limiting logic
        try:
            # Get the frame of the caller of this progress() method
            current_frame = inspect.currentframe()
            if current_frame and current_frame.f_back:
                frame = current_frame.f_back
                call_site_key = (frame.f_code.co_filename, frame.f_lineno)
            else:
                # Fallback if frame inspection is not possible (e.g., no caller frame)
                call_site_key = "__global_progress_no_caller_frame__"
        except Exception: # Catch any other unexpected errors during inspection
            # Fallback to a different global key if inspect raises an unexpected exception
            call_site_key = "__global_progress_inspect_exception__"

        current_time = time.time()
        # Get the last log time for this specific call site, default to 0 if not found
        last_log_time_for_site = self._last_progress_log_times.get(call_site_key, 0)

        # Log only if a second has passed since the last log from this specific call site
        if current_time - last_log_time_for_site >= self.PROGRESS_INTERVAL:
            self._last_progress_log_times[call_site_key] = current_time
            # Actually log the message using the base Logger's log method
            self.log(self.PROGRESS_LEVEL, message, *args, **kwargs)
    
    def debug(self, message, *args, **kwargs):
        """Log a message with severity 'DEBUG'."""
        if self.level <= logging.DEBUG:
            super().debug(message, *args, **kwargs)
    
    def info(self, message, *args, **kwargs):
        """Log a message with severity 'INFO'."""
        if self.level <= logging.INFO:
            super().info(message, *args, **kwargs)
    
    def warning(self, message, *args, **kwargs):
        """Log a message with severity 'WARNING'."""
        if self.level <= logging.WARNING:
            super().warning(message, *args, **kwargs)
    
    def error(self, message, *args, **kwargs):
        """Log a message with severity 'ERROR'."""
        if self.level <= logging.ERROR:
            super().error(message, *args, **kwargs)
    
    def critical(self, message, *args, **kwargs):
        """Log a message with severity 'CRITICAL'."""
        if self.level <= logging.CRITICAL:
            super().critical(message, *args, **kwargs)

# Monkey-patching removed as methods are defined in tracecolor class
