class AnsiColor:
    BLUE = "\033[94m"  # Blue for directories
    GREEN = "\033[92m"  # Green for Python files
    YELLOW = "\033[93m"  # Yellow for compiled Python files
    RESET = "\033[0m"  # Reset to default color
    ORANGE = "\033[33m"  # Orange for JavaScript files
    RED = "\033[31m"  # Red for C files
    LIGHT_BLUE = "\033[36m"  # Light blue for C++ files
    PURPLE = "\033[35m"  # Purple for Java files
    PINK = "\033[95m"  # Pink for Ruby files
    WHITE = "\033[97m"  # White for text files
    GRAY = "\033[90m"  # Gray for other files
    MAGENTA = "\033[95m"  # Magenta for image files
    CYAN = "\033[96m"  # Cyan for audio files
    LIGHT_GREEN = "\033[92m"  # Light green for video files
    LIGHT_YELLOW = "\033[93m"  # Light yellow for compressed files
    LIGHT_RED = "\033[91m"  # Light red for executable files
    LIGHT_PURPLE = "\033[95m"  # Light purple for library directories
    UNDERLINE = "\033[4m"  # Underline for symbolic links


ASSIGNED_COLORS = {
    ".md": AnsiColor.GRAY,
    ".py": AnsiColor.GREEN,
    ".pyc": AnsiColor.YELLOW,
    ".js": AnsiColor.ORANGE,
    ".c": AnsiColor.RED,
    ".cpp": AnsiColor.LIGHT_BLUE,
    ".java": AnsiColor.PURPLE,
    ".rb": AnsiColor.PINK,
    ".txt": AnsiColor.WHITE,
    ".jpg": AnsiColor.MAGENTA,
    ".png": AnsiColor.MAGENTA,
    ".gif": AnsiColor.MAGENTA,
    ".mp3": AnsiColor.CYAN,
    ".wav": AnsiColor.CYAN,
    ".mp4": AnsiColor.LIGHT_GREEN,
    ".avi": AnsiColor.LIGHT_GREEN,
    ".mkv": AnsiColor.LIGHT_GREEN,
    ".zip": AnsiColor.LIGHT_YELLOW,
    ".tar": AnsiColor.LIGHT_YELLOW,
    ".gz": AnsiColor.LIGHT_YELLOW,
    ".exe": AnsiColor.LIGHT_RED,
}

class Icons:
    DIR = "📁"
    FILE = "📄"
    IMG = "🖼️"
    ARCHIVE = "📦"

ASSIGNED_ICONS = {
    ".png": Icons.IMG,
    ".jpg": Icons.IMG,
    ".gif": Icons.IMG,
    ".zip": Icons.ARCHIVE,
    ".tar": Icons.ARCHIVE,
    ".gz": Icons.ARCHIVE,
}