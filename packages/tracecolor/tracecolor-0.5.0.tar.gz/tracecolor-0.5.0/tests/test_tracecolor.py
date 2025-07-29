import pytest
import logging
from tracecolor import tracecolor
import io
import sys
import re

def test_tracecolor_creation():
    """Test basic logger creation."""
    logger = tracecolor("test_logger")
    assert isinstance(logger, tracecolor)
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_logger"

def test_log_levels():
    """Test all log levels are properly defined."""
    logger = tracecolor("test_logger")
    assert logger.TRACE_LEVEL == 5
    assert logging.getLevelName(logger.TRACE_LEVEL) == "TRACE"
    assert logger.PROGRESS_LEVEL == 15
    assert logging.getLevelName(logger.PROGRESS_LEVEL) == "PROGRESS"
    
    # Test standard levels still work
    assert logger.level <= logging.DEBUG
    assert logger.level <= logging.INFO
    assert logger.level <= logging.WARNING
    assert logger.level <= logging.ERROR
    assert logger.level <= logging.CRITICAL

def test_log_output(capsys):
    """Test that log messages are properly formatted."""
    # Redirect stdout to capture log messages
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    try:
        logger = tracecolor("test_output")
        logger.info("Test info message")
        
        # Use capsys to capture stderr (where logging outputs by default)
        captured = capsys.readouterr()
        output = captured.err
        # Remove ANSI color codes for assertion
        ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
        clean_output = ansi_escape.sub('', output)
        # Check for basic format
        assert "I |" in clean_output
        assert "Test info message" in clean_output
        
        # Check timestamp format using regex
        timestamp_pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}"
        assert re.search(timestamp_pattern, output) is not None
        
    finally:
        sys.stdout = old_stdout

def test_progress_rate_limiting():
    """Test that progress messages are rate-limited."""
    logger = tracecolor("test_rate_limit")
    
    # Ensure PROGRESS_INTERVAL is default for this test to avoid cross-test contamination
    saved_progress_interval = tracecolor.PROGRESS_INTERVAL
    tracecolor.PROGRESS_INTERVAL = 1.0  # Default value for rate-limiting

    try:
        # Capture all handler calls
        calls = []
        
        class MockHandler(logging.Handler):
            def emit(self, record):
                calls.append(record)
        
        mock_handler = MockHandler()
        logger.handlers = [mock_handler]  # Replace the default handler
        
        # Two immediate progress calls from the same site should result in only one log
        for _ in range(2):
            logger.progress("Progress message from same site")
        
        assert len(calls) == 1
    finally:
        tracecolor.PROGRESS_INTERVAL = saved_progress_interval # Restore

@pytest.mark.parametrize("set_level,expected_levels", [
    (tracecolor.PROGRESS_LEVEL, ["PROGRESS", "INFO", "WARNING", "ERROR", "CRITICAL"]), # PROGRESS is 15
    (tracecolor.TRACE_LEVEL, ["TRACE", "DEBUG", "PROGRESS", "INFO", "WARNING", "ERROR", "CRITICAL"]), # TRACE is 5
    (logging.DEBUG, ["DEBUG", "PROGRESS", "INFO", "WARNING", "ERROR", "CRITICAL"]), # DEBUG is 10
    (logging.INFO, ["INFO", "WARNING", "ERROR", "CRITICAL"]),
    (logging.WARNING, ["WARNING", "ERROR", "CRITICAL"]),
    (logging.ERROR, ["ERROR", "CRITICAL"]),
    (logging.CRITICAL, ["CRITICAL"]),
])
def test_log_level_filtering(set_level, expected_levels, capsys):
    logger = tracecolor("test_level_filter")
    logger.setLevel(set_level)
# Restore original colorlog formatter usage
# standard_formatter = logging.Formatter("%(levelname).1s |%(asctime)s.%(msecs)03d| %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
# original_handlers = list(logger.handlers)
# for handler in logger.handlers:
#     handler.setFormatter(standard_formatter)
    
        
    # Map level names to log calls
    log_calls = [
        ("TRACE", lambda: logger.trace("trace message")),
        ("DEBUG", lambda: logger.debug("debug message")),
        ("PROGRESS", lambda: logger.progress("progress message")),
        ("INFO", lambda: logger.info("info message")),
        ("WARNING", lambda: logger.warning("warning message")),
        ("ERROR", lambda: logger.error("error message")),
        ("CRITICAL", lambda: logger.critical("critical message")),
    ]
    
    # Patch time to avoid issues with other time-sensitive parts if any,
    # but primary rate-limiting bypass is now through PROGRESS_INTERVAL
    import time as _time
    orig_time_func = _time.time # Save the original time function
    _time.time = lambda: 0 # Mock time to a constant for predictability if other parts rely on it

    original_progress_interval = tracecolor.PROGRESS_INTERVAL
    try:
        tracecolor.PROGRESS_INTERVAL = 0  # Disable rate-limiting for this test
        for level, call in log_calls:
            call()
    finally:
        _time.time = orig_time_func # Restore original time function
        tracecolor.PROGRESS_INTERVAL = original_progress_interval # Restore original interval
        # No need to restore formatters now
        # for i, handler in enumerate(logger.handlers):
        #      if i < len(original_handlers):
        #          handler.setFormatter(original_handlers[i].formatter)

    captured = capsys.readouterr().err
    # Remove ANSI color codes for assertion
    import re
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    clean_captured = ansi_escape.sub('', captured)
    for level, _ in log_calls:
        if level in expected_levels:
            # Adjust assertion for STRACE first letter
            expected_char = level[0] if level != "PROGRESS" else "P"
            assert f"{expected_char} |" in clean_captured
        else:
            expected_char = level[0] if level != "PROGRESS" else "P"
            assert f"{expected_char} |" not in clean_captured