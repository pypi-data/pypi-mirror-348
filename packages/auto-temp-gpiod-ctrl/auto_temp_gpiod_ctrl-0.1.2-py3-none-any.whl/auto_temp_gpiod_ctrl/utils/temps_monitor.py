# temps_monitor.py
#!/usr/bin/env python3
"""
temps_monitor.py: Utilities for fetching and displaying live temperature readings.

Functions:
  - clear_screen(): Clears the terminal for each update cycle.
  - fetch_temps(): Reads all available temperature sensors via psutil, returning
a mapping of sensor labels to their current values.
  - monitor(interval): Continuously renders a table of temperature readings,
refreshing every `interval` seconds until interrupted.
"""
import psutil
import time
import os
import sys

# ----------------------------------------------------------------------------
# Clear the terminal screen
# ----------------------------------------------------------------------------
def clear_screen():
    """Clears the terminal screen (cross-platform)."""
    os.system('cls' if os.name == 'nt' else 'clear')

# ----------------------------------------------------------------------------
# Fetch all temperature sensor readings
# ----------------------------------------------------------------------------
def fetch_temps():
    """
    Reads temperature sensors and returns a dict mapping each sensor entry
    to its current temperature (string formatted).

    Returns:
        dict: { '<sensor>_<label or idx>': 'XX.X' }
    """
    temps = psutil.sensors_temperatures()  # capture all thermal sensors
    data = {}
    for sensor, entries in temps.items():
        for idx, entry in enumerate(entries):
            # Use entry.label if provided, else fallback to index
            key = entry.label or f"{sensor}_{idx}"
            data[key] = f"{entry.current:.1f}"
    return data

# ----------------------------------------------------------------------------
# Monitor loop: display live table
# ----------------------------------------------------------------------------
def monitor(interval: float = 5.0):
    """
    Continuously displays a table of temperature readings.

    Args:
        interval (float): Refresh interval in seconds between updates.
    """
    initial = fetch_temps()
    if not initial:
        print("No temperature sensors found.", file=sys.stderr)
        raise RuntimeError("No temperature sensors found.")

    # Prepare table headers and column widths
    headers = list(initial.keys())
    col_widths = [max(len(h), 6) for h in headers]

    try:
        while True:
            data = fetch_temps()     # get fresh readings
            clear_screen()           # redraw table from top

            # Render header row
            header_row = "  ".join(
                f"{h:<{col_widths[i]}}" for i, h in enumerate(headers)
            )
            print(header_row)

            # Underline header with dashes
            print("  ".join('-' * col_widths[i] for i in range(len(headers))))

            # Render current values row
            value_row = "  ".join(
                f"{data.get(h, ''):<{col_widths[i]}}" for i, h in enumerate(headers)
            )
            print(value_row)

            time.sleep(interval)     # wait before next refresh

    except KeyboardInterrupt:
        # Graceful exit on user interrupt (Ctrl-C)
        print("\nMonitoring stopped by user.")

# Example usage:
#   python -m auto_temp_gpiod_ctrl --interval 5 --soc-pin PH2 --chip gpiochip1 --on-temp 60 --off-temp 50
