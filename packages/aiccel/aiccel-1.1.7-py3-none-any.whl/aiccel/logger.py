# aiccl/logger.py
import sys
import json
import logging
import traceback
from datetime import datetime
from typing import Dict, Any, List, Optional, Union, TextIO, cast, Tuple, Type # Added Type
from pathlib import Path

# Define ExcInfoType for better type hinting of exc_info
ExcInfoType = Union[None, bool, Tuple[Type[BaseException], BaseException, Optional[traceback.TracebackException]], BaseException]


class ColorFormatter(logging.Formatter):
    """Formatter adding colors to logging output for TTYs."""
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[41m\033[37m', # White on Red bg
        'RESET': '\033[0m'
    }

    def __init__(self, fmt: Optional[str] = None, datefmt: Optional[str] = None, style: str = '%', validate: bool = True, *, defaults: Optional[Dict[str, Any]] = None):
        super().__init__(fmt, datefmt, style, validate, defaults=defaults) # Python 3.10+
        # For older Python versions:
        # super().__init__(fmt, datefmt, style)
        self.is_tty = sys.stdout.isatty() # Check if output is a TTY

    def format(self, record: logging.LogRecord) -> str:
        log_message = super().format(record)
        if self.is_tty: # Only apply colors if outputting to a TTY
            return f"{self.COLORS.get(record.levelname, '')}{log_message}{self.COLORS['RESET']}"
        return log_message

class JSONFormatter(logging.Formatter):
    """Formatter for structured JSON logging."""
    def format(self, record: logging.LogRecord) -> str:
        log_entry: Dict[str, Any] = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(), # Use record.created
            'name': record.name,
            'level': record.levelname,
            'message': record.getMessage(), # Use getMessage() for formatted message
            'pathname': record.pathname, # Changed from file to pathname for consistency
            'lineno': record.lineno,
            'funcName': record.funcName
        }
        if record.exc_info:
            log_entry['exception'] = { # Structured exception info
                'type': record.exc_info[0].__name__ if record.exc_info[0] else "UnknownException",
                'message': str(record.exc_info[1]) if record.exc_info[1] else "No message",
                'stack_trace': self.formatException(record.exc_info)
            }
        if hasattr(record, 'extra_data') and isinstance(record.extra_data, dict): # For extra context
            log_entry.update(record.extra_data)
        return json.dumps(log_entry, default=str) # Added default=str for non-serializable


class AILogger:
    """Advanced logging for AI components with tracing and structured logging."""
    _instance = None # For potential singleton pattern if desired, though not strictly implemented here

    def __init__(self, name: str, level: Union[int, str] = logging.INFO, 
                 verbose: bool = False, log_file: Optional[str] = None, 
                 structured_logging: bool = False, use_colors: bool = True):
        self.name = name
        self.logger = logging.getLogger(name)
        
        # Set level: if verbose is True, override level to DEBUG
        effective_level = logging.DEBUG if verbose else level
        self.logger.setLevel(effective_level)
        
        # Prevent duplicate handlers if logger already configured
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        if use_colors:
            console_formatter: logging.Formatter = ColorFormatter(
                '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        else:
            console_formatter = logging.Formatter(
                '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler
        if log_file:
            try:
                log_path = Path(log_file)
                log_path.parent.mkdir(parents=True, exist_ok=True)
                file_handler = logging.FileHandler(log_path, encoding='utf-8')
                if structured_logging:
                    file_handler.setFormatter(JSONFormatter())
                else:
                    file_handler.setFormatter(logging.Formatter(
                        '%(asctime)s [%(name)s] [%(levelname)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S'
                    ))
                self.logger.addHandler(file_handler)
            except IOError as e:
                self.logger.error(f"Failed to configure file logger for {log_file}: {e}", exc_info=True)
        
        self.trace_history: List[Dict[str, Any]] = [] # Trace history specific to this logger instance
        self.verbose = verbose # Store verbose state, mainly for trace printing
        self.max_traces = 100 # Added for compatibility with agent.py

    def _log(self, level: int, message: str, exc_info: ExcInfoType = None, extra_data: Optional[Dict[str, Any]] = None):
        """Internal log method to handle extra_data for JSONFormatter."""
        if extra_data:
            self.logger.log(level, message, exc_info=exc_info, extra={'extra_data': extra_data})
        else:
            self.logger.log(level, message, exc_info=exc_info)

    def debug(self, message: str, exc_info: ExcInfoType = None, extra: Optional[Dict[str, Any]] = None):
        self._log(logging.DEBUG, message, exc_info=exc_info, extra_data=extra)
        
    def info(self, message: str, exc_info: ExcInfoType = None, extra: Optional[Dict[str, Any]] = None):
        self._log(logging.INFO, message, exc_info=exc_info, extra_data=extra)
        
    def warning(self, message: str, exc_info: ExcInfoType = None, extra: Optional[Dict[str, Any]] = None):
        self._log(logging.WARNING, message, exc_info=exc_info, extra_data=extra)
        
    def error(self, message: str, exc_info: ExcInfoType = True, extra: Optional[Dict[str, Any]] = None): # Default exc_info=True for errors
        self._log(logging.ERROR, message, exc_info=exc_info, extra_data=extra)
        
    def critical(self, message: str, exc_info: ExcInfoType = True, extra: Optional[Dict[str, Any]] = None):
        self._log(logging.CRITICAL, message, exc_info=exc_info, extra_data=extra)
    
    # ADDED COMPATIBILITY METHOD: Add this to support code that expects the log() method
    def log(self, message: str, exc_info: ExcInfoType = None, extra_data: Optional[Dict[str, Any]] = None):
        """Compatibility method for code that uses the log() method from agent.py."""
        self.info(message, exc_info=exc_info, extra=extra_data)
    
    def trace_start(self, action: str, inputs: Optional[Dict[str, Any]] = None) -> int:
        trace_id = len(self.trace_history)
        trace = {
            "id": trace_id,
            "action": action,
            "start_time": datetime.now().isoformat(),
            "inputs": inputs or {},
            "steps": [],
            "end_time": None,
            "outputs": None,
            "duration_ms": None,
            "errors": []
        }
        self.trace_history.append(trace)
        
        if self.verbose: # Use self.verbose, not logger's level for this specific print
            input_str = json.dumps(inputs, indent=2, default=str) if inputs else "None"
            self.info(f"⏳ START {action} [trace_id={trace_id}]\nInputs: {input_str}")
        return trace_id
    
    def trace_step(self, trace_id: int, step_name: str, details: Optional[Dict[str, Any]] = None):
        if not (0 <= trace_id < len(self.trace_history)):
            self.error(f"Invalid trace_id for step: {trace_id}")
            return
            
        step = {
            "name": step_name,
            "time": datetime.now().isoformat(),
            "details": details or {}
        }
        self.trace_history[trace_id]["steps"].append(step)
        
        if self.verbose:
            details_str = json.dumps(details, indent=2, default=str) if details else "None"
            self.debug(f"➡️ STEP {step_name} [trace_id={trace_id}]\nDetails: {details_str}")
    
    def trace_error(self, trace_id: int, error: BaseException, context: str):
        if not (0 <= trace_id < len(self.trace_history)):
            self.error(f"Invalid trace_id for error recording: {trace_id}")
            return
            
        error_info = {
            "time": datetime.now().isoformat(),
            "context": context,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "stack_trace": traceback.format_exception(type(error), error, error.__traceback__)
        }
        self.trace_history[trace_id]["errors"].append(error_info)
        # Log the error using the logger's error method, which includes stack trace if exc_info is True
        self.error(f"Trace Error [trace_id={trace_id}]: {context}: {str(error)}", exc_info=error)
    
    def trace_end(self, trace_id: int, outputs: Optional[Dict[str, Any]] = None):
        if not (0 <= trace_id < len(self.trace_history)):
            self.error(f"Invalid trace_id for end: {trace_id}")
            return
            
        trace = self.trace_history[trace_id]
        end_time = datetime.now()
        try:
            start_time = datetime.fromisoformat(trace["start_time"])
            duration_ms = (end_time - start_time).total_seconds() * 1000
        except ValueError: # Should not happen
            duration_ms = -1.0

        trace.update({
            "end_time": end_time.isoformat(),
            "outputs": outputs or {},
            "duration_ms": duration_ms
        })
        
        if self.verbose:
            output_str = json.dumps(outputs, indent=2, default=str) if outputs else "None"
            error_count = len(trace.get("errors", []))
            self.info(f"✅ END {trace['action']} [trace_id={trace_id}] - {duration_ms:.2f}ms, Errors: {error_count}\nOutputs: {output_str}")
    
    def get_trace(self, trace_id: int) -> Optional[Dict[str, Any]]:
        return self.trace_history[trace_id] if 0 <= trace_id < len(self.trace_history) else None
    
    def get_traces(self) -> List[Dict[str, Any]]: # Return list of traces
        return list(self.trace_history)
    
    def visualize_trace(self, trace_id: int) -> str:
        trace = self.get_trace(trace_id)
        if not trace:
            return f"Invalid trace ID: {trace_id}"
        
        output_parts = [
            f"Trace #{trace_id}: {trace.get('action', 'N/A')}",
            f"Started: {trace.get('start_time', 'N/A')}",
            f"Duration: {trace.get('duration_ms', -1):.2f}ms", # Default to -1 if missing
            f"Errors: {len(trace.get('errors', []))}",
            "\nInputs:",
            json.dumps(trace.get('inputs',{}), indent=2, default=str),
            "\nSteps:"
        ]
        
        for i, step in enumerate(trace.get('steps',[])):
            output_parts.append(f"  Step {i+1}: {step.get('name','N/A')} ({step.get('time','N/A')})")
            output_parts.append(f"    Details: {json.dumps(step.get('details',{}), indent=4, default=str)}")
        
        if trace.get("errors"):
            output_parts.append("\nErrors:")
            for i, error_info in enumerate(trace["errors"]):
                output_parts.append(f"  Error {i+1}: {error_info.get('context','N/A')} ({error_info.get('time','N/A')})")
                output_parts.append(f"    Type: {error_info.get('error_type','N/A')}")
                output_parts.append(f"    Message: {error_info.get('error_message','N/A')}")
                # Stack trace can be very long, consider summarizing or conditional inclusion
                # stack_trace_str = "".join(error_info.get('stack_trace',[]))
                # output_parts.append(f"    Stack Trace:\n      {stack_trace_str.replace('\n', '\n      ')}")
        
        output_parts.extend([
            "\nOutputs:",
            json.dumps(trace.get('outputs',{}), indent=2, default=str)
        ])
        
        return "\n".join(output_parts)

    # ADDED FOR COMPATIBILITY with agent.py AILogger
    def _archive_oldest_trace(self):
        """Archive oldest trace when max is reached - compatibility with agent.py."""
        if len(self.trace_history) > self.max_traces:
            self.trace_history.pop(0)