from datetime import datetime
import sys
import re

class Logger:
    ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    def __init__(self, prefix: str = None, indent: int = 0, mode: str = "classic", separator: str = " "):
        self.colors = {
            'white': "\u001b[37m",
            'magenta': "\x1b[38;2;157;38;255m",
            'error': "\x1b[38;5;202m",
            'success': "\x1b[38;5;120m",
            'warning': "\x1b[38;5;214m",
            'blue': "\x1b[38;5;21m",
            'info': "\x1b[38;5;62m",
            'pink': "\x1b[38;5;176m",
            'gray': "\x1b[90m",
            'captcha': "\x1b[38;5;105m"
        }
        self.prefix: str = f"{self.colors['gray']}[{self.colors['magenta']}{prefix}{self.colors['gray']}]" if prefix else ""
        self.indent: str = " " * indent
        self.debug_mode: bool = any(arg.lower() in ['--debug', '-debug'] for arg in sys.argv)
        self.mode = mode  # Modes: "classic", "minimal", "structured"
        self.separator = separator  # Used only in minimal mode

    def strip_ansi(self, text: str) -> str:
        return self.ANSI_ESCAPE.sub('', text)

    def get_time(self) -> str:
        return datetime.now().strftime("%H:%M:%S")

    def _hex_to_ansi(self, hex_color: str) -> str:
        hex_color = hex_color.lstrip('#')
        if len(hex_color) != 6:
            raise ValueError("Hex color must be in RRGGBB format")
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        return f"\x1b[38;2;{r};{g};{b}m"

    def _log(self, color: str, message: str, level: str, additional: str = None) -> None:
        time_now = self.get_time()

        # Convert hex color to ANSI if needed
        if color.startswith("#"):
            color = self._hex_to_ansi(color)

        if self.mode == "classic":
            formatted_msg = (
                f"{self.indent}{self.prefix} {self.colors['white']}→"
                f"{self.colors['gray']}[{time_now}] {self.colors['white']}→ "
                f"{self.colors['gray']}[{color}{level}{self.colors['gray']}] {self.colors['white']}→ "
                f"{self.colors['gray']}[{color}{message}{self.colors['gray']}]"
            )

        elif self.mode == "minimal":
            formatted_msg = (
                f"{self.colors['gray']}{time_now} {color}{level} "
                f"{self.colors['white']}{self.separator} {self.colors['white']}{message}"
            )

        elif self.mode == "structured":
            parts = []

            if self.prefix:
                parts.append(self.prefix.strip())  # prefix already includes colors

            parts.append(f"{self.colors['white']}:: {self.colors['gray']}{time_now} {self.colors['white']}::")

            parts.append(f"{color}{level.upper()} {self.colors['white']}::")

            parts.append(f"{color}{message}")

            if additional:
                parts.append(f"{self.colors['white']}:: {self.colors['gray']}{additional}")

            formatted_msg = " ".join(parts)

        else:
            # fallback to simple print
            formatted_msg = f"{level}: {message}"

        print(formatted_msg)

    # Old methods unchanged:
    def success(self, message: str, level: str = "SUCCESS", additional: str = None) -> None:
        self._log(self.colors['success'], message, level, additional)

    def warning(self, message: str, level: str = "WARNING", additional: str = None) -> None:
        self._log(self.colors['warning'], message, level, additional)

    def info(self, message: str, level: str = "INFO", additional: str = None) -> None:
        self._log(self.colors['info'], message, level, additional)

    def error(self, message: str, level: str = "ERROR", additional: str = None) -> None:
        self._log(self.colors['error'], message, level, additional)

    def debug(self, message: str, level: str = "DEBUG", additional: str = None) -> None:
        if self.debug_mode:
            self._log(self.colors['magenta'], message, level, additional)

    def captcha(self, message: str, level: str = "CAPTCHA", additional: str = None) -> None:
        self._log(self.colors['captcha'], message, level, additional)

    # New custom method for any symbol, title, message, hex or ANSI color:
    def custom(self, symbol: str, title: str, message: str, color: str = 'white', **kwargs) -> None:
        ansi_color = color
        if color.startswith("#"):
            ansi_color = self._hex_to_ansi(color)
        
        time_now = self.get_time()

        additional_str = ""
        if kwargs:
            parts = []
            for k, v in kwargs.items():
                # If key ends with '_', remove it for display
                display_key = k[:-1] if k.endswith('_') else k
                parts.append(f"{ansi_color}{display_key}{self.colors['white']} {v}")
            additional_str = " " + " ".join(parts)

        formatted = (
            f"{self.colors['white']}[{self.colors['gray']}{time_now}{self.colors['white']}] "
            f"({ansi_color}{symbol}{self.colors['white']}) "
            f"{ansi_color}{title} "
            f"{self.colors['white']}{message}"
            f"{additional_str}"
        )
        print(formatted)

