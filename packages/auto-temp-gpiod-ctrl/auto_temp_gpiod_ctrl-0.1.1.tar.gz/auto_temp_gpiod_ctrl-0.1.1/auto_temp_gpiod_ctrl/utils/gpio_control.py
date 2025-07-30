#!/usr/bin/env python3
"""
gpio_control.py: GPIO output control with automatic offset parsing

Supports two modes for specifying a pin:
  - SOC mode: use bank-letter/number (e.g. H2, PH2)
  - Physical mode: use physical header pin number (only mapped GPIO pins)

Example usage:
  python -m auto_temp_gpiod_ctrl -m soc -p PH2 -c gpiochip1 -v 1 --pulse 0.5
  python -m auto_temp_gpiod_ctrl -m physical -p 8  -c gpiochip1 -v 1
"""
import argparse    # parse command line arguments
import re          # regular expressions for parsing SOC pin spec
import sys         # exit with error codes
import time        # sleep for pulse durations
import glob        # find available gpiochip devices
import os          # file and path operations
import gpiod       # libgpiod Python bindings

# ----------------------------------------------------------------------------
# Physical pin-to-SoC-pin mapping (only pins that can be driven as GPIO)
# Key: physical header pin number; Value: SoC pin spec for SOC parser
# ----------------------------------------------------------------------------
Physical_MAP = {
    3:  "PH5",   # I2C3 SDA
    5:  "PH4",   # I2C3 SCL
    7:  "PC9",   # GPIO
    8:  "PH2",   # UART5 TX
    10: "PH3",   # UART5 RX
    11: "PC6",
    12: "PC11",
    13: "PC5",
    15: "PC8",
    16: "PC15",
    18: "PC14",
    19: "PH7",   # SPI1 MOSI
    21: "PH8",   # SPI1 MISO
    22: "PC7",   # SPI1 CS
    23: "PH6",   # SPI1 CLK
    24: "PH9",
    26: "PC10"
}

# ----------------------------------------------------------------------------
# Helper: open a gpiochip by name or full device path
# ----------------------------------------------------------------------------
def open_chip(chip_name: str) -> gpiod.Chip:
    """Open a GPIO chip by name (e.g. gpiochip1) or device path (/dev/gpiochip1)."""
    # Prepend /dev/ if a bare name was provided
    path = chip_name if chip_name.startswith('/dev/') else f'/dev/{chip_name}'
    # Return a Chip object for low-level GPIO operations
    return gpiod.Chip(path)

# ----------------------------------------------------------------------------
# Helper: list all gpiochip device paths on the system
# ----------------------------------------------------------------------------
def list_chips() -> list[str]:
    """Return sorted list of all /dev/gpiochip* paths."""
    return sorted(glob.glob('/dev/gpiochip*'))

# ----------------------------------------------------------------------------
# Offset parsing: SOC or physical modes
# ----------------------------------------------------------------------------
def parse_offset(pin_spec: str, mode: str) -> int:
    """
    Convert pin_spec to a numeric line offset.

    - SOC mode: parse bank-letter + number, e.g. H2 or PH2.
      Calculates offset = (bank_index * 32) + pin_number.

    - Physical mode: look up header pin in Physical_MAP, resolve
      to a SoC pin spec, then reuse SOC logic.
    """
    if mode.lower() == 'soc':
        # Regex: optional leading 'P', then one letter, then digits
        m = re.match(r'^(?:P)?([A-Za-z])(\d+)$', pin_spec, re.IGNORECASE)
        if not m:
            raise ValueError(f"Invalid SOC pin spec: {pin_spec}")
        bank_str, num_str = m.group(1).upper(), m.group(2)
        bank_idx = ord(bank_str) - ord('A')    # A=0, B=1, ...
        pin_idx = int(num_str)
        # Each bank has 32 lines
        return bank_idx * 32 + pin_idx

    elif mode.lower() == 'physical':
        # Must be a number corresponding to a header pin
        if not pin_spec.isdigit():
            raise ValueError(f"Physical mode requires numeric pin, got: {pin_spec}")
        phys = int(pin_spec)
        if phys not in Physical_MAP:
            raise ValueError(f"Unknown or non-programmable physical pin: {phys}")
        # Translate to SoC spec (e.g. 'PH2'), then recurse into SOC logic
        soc_pin = Physical_MAP[phys]
        return parse_offset(soc_pin, 'soc')

    else:
        raise ValueError(f"Unknown mode: {mode}")

# ----------------------------------------------------------------------------
# Send a GPIO output signal to the specified line offset
# ----------------------------------------------------------------------------
def send_signal(
    line_offset: int,
    value: int,
    chip_name: str,
    pulse: float = None
):
    """
    Request and drive a single GPIO line.

    - Attempts to request the given offset on chip_name.
    - On failure, suggests an alternate gpiochip if available.
    - Optionally pulses (sets HIGH then LOW after delay).
    """
    try:
        # Open the chip and set up a line request for output
        chip = open_chip(chip_name)
        settings = gpiod.LineSettings()
        settings.direction = gpiod.line.Direction.OUTPUT

        # Determine active/inactive values from enum
        initial = gpiod.line.Value.ACTIVE if value else gpiod.line.Value.INACTIVE

        # Request the line(s) with initial output value
        req = chip.request_lines(
            { line_offset: settings },
            consumer='run',
            output_values={ line_offset: initial }
        )

    except (ValueError, OSError):
        # Handle "offset out of range" or other chip errors
        current = chip_name if chip_name.startswith('/dev/') else f'/dev/{chip_name}'
        alt_chip = None
        # Search other chips for a valid offset
        for dev in list_chips():
            if dev == current:
                continue
            try:
                alt = gpiod.Chip(dev)
                # If offset is valid for this chip
                if 0 <= line_offset < alt.get_info().num_lines:
                    alt_chip = os.path.basename(dev)
                    alt.close()
                    break
                alt.close()
            except Exception:
                continue

        # Inform the user and exit
        msg = f"Error: offset {line_offset} out of range for {chip_name}."
        if alt_chip:
            msg += f" Try using chip '{alt_chip}' instead."
        else:
            msg += " No alternative gpiochip found with sufficient lines."
        print(msg, file=sys.stderr)
        raise RuntimeError(msg)

    # If a pulse duration was given, wait then reset to INACTIVE
    if pulse is not None:
        time.sleep(pulse)
        req.set_values({ line_offset: gpiod.line.Value.INACTIVE })

    # Release the line request and close the chip
    req.release()
    chip.close()
