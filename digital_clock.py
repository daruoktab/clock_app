"""
A premium digital clock app with animations, themes, and advanced features.
"""

from datetime import datetime
import time
try:
    from zoneinfo import ZoneInfo
except ImportError:
    # Fallback for older Python versions
    ZoneInfo = None

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Label, Static
from textual.binding import Binding
from textual.reactive import reactive

# ASCII art for the big clock display. Each character is 5 rows high.
ASCII_DIGITS = {
    '0': [" ##### ", "#     #", "#     #", "#     #", " ##### "],
    '1': ["  #    ", " ##    ", "  #    ", "  #    ", " ###   "],
    '2': [" ##### ", "     # ", " ##### ", "#     ", " ##### "],
    '3': [" ##### ", "     # ", "  #### ", "     # ", " ##### "],
    '4': ["#   #  ", "#   #  ", "#######", "    #  ", "    #  "],
    '5': [" ##### ", "#      ", " ####  ", "     # ", " ##### "],
    '6': [" ##### ", "#      ", " ##### ", "#     #", " ##### "],
    '7': [" ##### ", "    #  ", "   #   ", "  #    ", " #     "],
    '8': [" ##### ", "#     #", " ##### ", "#     #", " ##### "],
    '9': [" ##### ", "#     #", " ##### ", "     # ", " ##### "],
    ':': [" ", "•", " ", "•", " "],
    'A': ["  ###  ", " #   # ", " ##### ", "#     #", "#     #"],
    'P': [" ####  ", "#    # ", " ####  ", "#      ", "#      "],
    'M': ["#     #", "##   ##", "# # # #", "#  #  #", "#     #"],
    ' ': ["       ", "       ", "       ", "       ", "       "],
}


class DigitalClockApp(App):
    """A digital clock with themes, animations, and world time."""

    BINDINGS = [
        Binding("t", "toggle_theme", "Toggle Theme"),
        Binding("f", "toggle_format", "12/24H Format"),
        Binding("s", "toggle_seconds", "Toggle Seconds"),
        Binding("q", "quit", "Quit"),
    ]

    clock_theme: reactive[str] = reactive("neon")
    time_format: reactive[int] = reactive(24)
    show_seconds: reactive[bool] = reactive(True)

    CSS = """
    Screen {
        align: center middle;
        background: #0a0a1a;
    }

    .clock-container {
        width: 85;
        height: 28;
        padding: 2;
        border: heavy $accent;
        background: #16213e;
    }

    .neon {
        border: heavy cyan;
        background: #001122;
    }

    .classic {
        border: heavy gold;
        background: #221100;
    }

    .matrix {
        border: heavy green;
        background: #001100;
    }

    .cyberpunk {
        border: heavy magenta;
        background: #220022;
    }

    .title {
        text-align: center;
        color: $accent;
        text-style: bold;
        margin-bottom: 1;
        height: 1;
    }

    .main-time {
        text-align: center;
        color: cyan;
        text-style: bold;
        /* FIXED: Restored height for the multi-line ASCII art display. */
        height: 7;
        margin: 1 0;
        content-align: center middle;
    }

    .neon .main-time { color: cyan; text-style: bold; }
    .classic .main-time { color: gold; text-style: bold; }
    .matrix .main-time { color: green; text-style: bold; }
    .cyberpunk .main-time { color: magenta; text-style: bold; }

    .date-info {
        text-align: center;
        color: white;
        height: 2;
        margin: 0 0 1 0;
        content-align: center middle;
    }

    .world-times {
        height: 8;
        margin: 1 0;
        border: solid $primary;
        background: rgba(0, 0, 0, 0.3);
        padding: 1;
    }

    .timezone-row {
        height: 1;
        color: $text;
        text-align: left;
        margin: 0;
        padding: 0 1;
    }

    .controls {
        height: 2;
        text-align: center;
        color: $text-disabled;
        margin-top: 1;
        content-align: center middle;
    }

    .status-bar {
        dock: bottom;
        height: 1;
        background: $panel;
        color: $text-muted;
        text-align: center;
        content-align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical(classes="clock-container neon"):
            yield Label("Digital Clock", classes="title")
            yield Static("", id="main-time", classes="main-time")
            yield Static("", id="date-info", classes="date-info")

            with Vertical(classes="world-times"):
                yield Label("🌍 World Times", classes="title")
                yield Static("", id="world-ny", classes="timezone-row")
                yield Static("", id="world-london", classes="timezone-row")
                yield Static("", id="world-tokyo", classes="timezone-row")
                yield Static("", id="world-sydney", classes="timezone-row")
                yield Static("", id="world-dubai", classes="timezone-row")

            yield Static("T:Theme | F:Format | S:Seconds | Q:Quit", classes="controls")

        yield Static("", id="status", classes="status-bar")

    def on_ready(self) -> None:
        """Initialize the clock when ready."""
        self._start_time = time.time()
        self.update_display()
        self.set_interval(1, self.update_display)

    def update_display(self) -> None:
        """Update all time displays."""
        now = datetime.now()

        # Main time with bigger display
        if self.time_format == 12:
            time_format_str = "%I:%M:%S %p" if self.show_seconds else "%I:%M %p"
        else:
            time_format_str = "%H:%M:%S" if self.show_seconds else "%H:%M"

        time_str = now.strftime(time_format_str).strip()
        
        big_time = self.create_big_time(time_str)
        self.query_one("#main-time", Static).update(big_time)

        # Enhanced date info
        date_str = now.strftime("%A, %B %d, %Y")
        week_num = now.isocalendar()[1]
        self.query_one("#date-info", Static).update(f"📅 {date_str} • Week {week_num}")

        # World times
        self.update_world_times()

        # Status bar
        uptime = int(time.time() - self._start_time)
        hours, remainder = divmod(uptime, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        status = f"Theme: {self.clock_theme.upper()} | Format: {self.time_format}H | Uptime: {uptime_str} | {now.strftime('%Z')}"
        self.query_one("#status", Static).update(status)

    def create_big_time(self, time_str: str) -> str:
        """
        FIXED: Create a large multi-line ASCII art time display that fits
        within the container's boundaries.
        """
        # We have 5 rows for our ASCII art
        output_lines = [""] * 5
        
        for char in time_str.upper():
            # Get the ASCII pattern for the character, or a blank space if not found
            pattern = ASCII_DIGITS.get(char, ASCII_DIGITS[' '])
            for i in range(5):
                # Add a single space between characters for separation
                output_lines[i] += pattern[i] + " "
        
        # Join the assembled lines with newlines to form the final multi-line string
        return "\n".join(output_lines)

    def update_world_times(self) -> None:
        """Update world time displays with proper timezone handling."""
        try:
            times = {}
            if ZoneInfo:
                times['ny'] = datetime.now(ZoneInfo("America/New_York")).strftime("%H:%M")
                times['london'] = datetime.now(ZoneInfo("Europe/London")).strftime("%H:%M")
                times['tokyo'] = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%H:%M")
                times['sydney'] = datetime.now(ZoneInfo("Australia/Sydney")).strftime("%H:%M")
                times['dubai'] = datetime.now(ZoneInfo("Asia/Dubai")).strftime("%H:%M")
            else:
                import pytz
                timezones = {
                    'ny': 'America/New_York', 'london': 'Europe/London', 
                    'tokyo': 'Asia/Tokyo', 'sydney': 'Australia/Sydney', 'dubai': 'Asia/Dubai'
                }
                for key, tz_name in timezones.items():
                    tz = pytz.timezone(tz_name)
                    times[key] = datetime.now(pytz.UTC).astimezone(tz).strftime("%H:%M")
            
            self.query_one("#world-ny", Static).update(f"🗽 New York    {times['ny']}")
            self.query_one("#world-london", Static).update(f"🏰 London      {times['london']}")
            self.query_one("#world-tokyo", Static).update(f"🗾 Tokyo       {times['tokyo']}")
            self.query_one("#world-sydney", Static).update(f"🇦🇺 Sydney      {times['sydney']}")
            self.query_one("#world-dubai", Static).update(f"🏜️ Dubai       {times['dubai']}")
            
        except Exception:
            self.query_one("#world-ny", Static).update("🗽 New York    --:--")
            self.query_one("#world-london", Static).update("🏰 London      --:--")
            self.query_one("#world-tokyo", Static).update("🗾 Tokyo       --:--")
            self.query_one("#world-sydney", Static).update("🇦🇺 Sydney      --:--")
            self.query_one("#world-dubai", Static).update("🏜️ Dubai       --:--")

    def action_toggle_theme(self) -> None:
        """Cycle through themes."""
        themes = ["neon", "classic", "matrix", "cyberpunk"]
        current_idx = themes.index(self.clock_theme)
        self.clock_theme = themes[(current_idx + 1) % len(themes)]
        
        container = self.query_one(".clock-container")
        container.remove_class("neon", "classic", "matrix", "cyberpunk")
        container.add_class(self.clock_theme)

    def action_toggle_format(self) -> None:
        """Toggle between 12h and 24h format."""
        self.time_format = 12 if self.time_format == 24 else 24

    def action_toggle_seconds(self) -> None:
        """Toggle seconds display."""
        self.show_seconds = not self.show_seconds


if __name__ == "__main__":
    app = DigitalClockApp()
    app.run()