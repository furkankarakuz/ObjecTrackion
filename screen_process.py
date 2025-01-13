import ctypes


def get_size() -> tuple[int, int]:
    """Get Size

    This method returns main screen size detail

    Returns:
        tuple[int, int]: width and height of the main screen
    """
    width = ctypes.windll.user32.GetSystemMetrics(0)
    height = ctypes.windll.user32.GetSystemMetrics(1)

    return width, height
