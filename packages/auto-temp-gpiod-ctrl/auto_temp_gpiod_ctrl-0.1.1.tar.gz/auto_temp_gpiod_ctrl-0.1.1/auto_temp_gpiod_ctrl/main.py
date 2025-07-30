from .utils.gpio_control import parse_offset, send_signal
from .utils.temps_monitor import fetch_temps, clear_screen
import threading
import sys
import time
import argparse

def heavy_calc(stop_event: threading.Event):
    """
    Run a CPU‐intensive loop until stop_event is set.
    Simulates a realistic CPU load by performing math operations in a loop.
    """
    while not stop_event.is_set():
        total = 0
        for i in range(1_000_000):
            total += i * i
        # Optionally, short sleep to avoid 100% pegging
        # time.sleep(0.01)

def print_help():
    """
    Print detailed help and configuration instructions for the user.
    """
    help_text = f"""
    auto-temp-gpiod-ctrl: Temperature-based GPIO Control
    ---------------------------------------------------
    This tool monitors system temperatures and controls a GPIO pin based on configurable thresholds.

    Usage:
      python -m auto_temp_gpiod_ctrl.main [OPTIONS]

    Options:
      -i, --interval FLOAT    Seconds between temperature checks and table refresh (default: 5.0)
      --soc-pin PIN           SoC pin spec to control (e.g. H2, PH2) (default: PH2)
      -c, --chip CHIP         GPIO chip device (e.g. gpiochip0 or /dev/gpiochip1) (default: gpiochip1)
      --on-temp FLOAT         Threshold to turn ON GPIO (≥ this temperature, default: 50.0)
      --off-temp FLOAT        Threshold to turn OFF GPIO (≤ this temperature, default: 40.0)
      --test-mode             Enable heavy calculation simulation (for testing only)
      -h, --help              Show this help message and exit

    Example:
      python -m auto_temp_gpiod_ctrl --soc-pin PH2 --chip gpiochip1 --on-temp 55 --off-temp 45 --interval 3

    Notes:
      - The GPIO pin will always be set to OFF (0) at startup and shutdown for safety.
      - Use --test-mode to simulate CPU load for testing the control logic.
      - Ensure you have the necessary permissions to access GPIO devices.
    """
    print(help_text)

def run_auto_temp_ctrl(
    interval=5.0,
    soc_pin='PH2',
    chip='gpiochip1',
    on_temp=50.0,
    off_temp=40.0,
    test_mode=False,
    print_help=False
):
    """
    Main entry point for auto_temp_gpiod_ctrl, callable from Python code.
    Arguments match CLI options.
    """
    if print_help:
        print_help_func = globals().get('print_help')
        if print_help_func:
            print_help_func()
        else:
            print("Help function not found.")
        return

    try:
        offset = parse_offset(soc_pin, 'soc')
    except ValueError as e:
        print(f"Error parsing soc_pin: {e}", file=sys.stderr)
        raise RuntimeError(f"Error parsing soc_pin: {e}. Hint: Check your --soc-pin argument or try another available pin.")

    stop_event = threading.Event()
    if test_mode:
        thread = threading.Thread(
            target=heavy_calc,
            args=(stop_event,),
            daemon=True
        )
        thread.start()
    else:
        thread = None

    # Initialize GPIO state: always set to 0 (OFF) at start
    gpio_state = 0
    try:
        send_signal(offset, 0, chip)
    except Exception as e:
        print(f"Failed to initialize GPIO line (chip: {chip}, pin: {soc_pin}): {e}", file=sys.stderr)
        raise RuntimeError(f"Failed to initialize GPIO line (chip: {chip}, pin: {soc_pin}): {e}. Hint: Try another --chip value (e.g., gpiochip0, gpiochip1) or check your permissions.")

    try:
        while True:
            temps = fetch_temps()
            clear_screen()
            header_keys = list(temps.keys())
            display_keys = [k.replace('_thermal_0', '') for k in header_keys]
            col_width = 10
            header = ' '.join(f"{k:>{col_width}}" for k in display_keys)
            print(header)
            print('-' * len(header))
            print(' '.join(f"{temps[k]:>{col_width}}" for k in header_keys))

            max_temp = max(float(v) for v in temps.values())

            if max_temp >= on_temp and gpio_state == 0:
                try:
                    send_signal(offset, 1, chip)
                    gpio_state = 1
                except Exception as e:
                    print(f"Failed to set GPIO ON: {e}", file=sys.stderr)
                    raise RuntimeError(f"Failed to set GPIO ON: {e}. Hint: Try another --chip value or check your wiring.")
            elif max_temp <= off_temp and gpio_state == 1:
                try:
                    send_signal(offset, 0, chip)
                    gpio_state = 0
                except Exception as e:
                    print(f"Failed to set GPIO OFF: {e}", file=sys.stderr)
                    raise RuntimeError(f"Failed to set GPIO OFF: {e}. Hint: Try another --chip value or check your wiring.")
    finally:
        # On any exit, always reset GPIO to 0 (OFF) and release the line
        send_signal(offset, 0, chip)
        stop_event.set()
        if thread:
            thread.join()

def main():
    parser = argparse.ArgumentParser(
        description='Run CPU load simulation and temperature‐based GPIO control',
        add_help=False
    )
    parser.add_argument('-i', '--interval', type=float, default=5.0, help='Seconds between temperature checks and table refresh')
    parser.add_argument('--soc-pin', default='PH2', help='SoC pin spec to control (e.g. H2, PH2)')
    parser.add_argument('-c', '--chip', default='gpiochip1', help='GPIO chip device (e.g. gpiochip0 or /dev/gpiochip1)')
    parser.add_argument('--on-temp', type=float, default=50.0, help='Threshold to turn ON GPIO (≥ this temperature)')
    parser.add_argument('--off-temp', type=float, default=40.0, help='Threshold to turn OFF GPIO (≤ this temperature)')
    parser.add_argument('--test-mode', action='store_true', help='Enable heavy calculation simulation (for testing only)')
    parser.add_argument('-h', '--help', action='store_true', help='Show this help message and exit')
    args = parser.parse_args()

    run_auto_temp_ctrl(
        interval=args.interval,
        soc_pin=args.soc_pin,
        chip=args.chip,
        on_temp=args.on_temp,
        off_temp=args.off_temp,
        test_mode=args.test_mode,
        print_help=args.help
    )
