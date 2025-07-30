# Auto Temp GPIOd Control

Automatic temperature-based GPIO control for any device with libgpiod 2.x support.

## Features
- Monitors all available temperature sensors using `psutil`
- Controls a GPIO pin based on user-defined temperature thresholds
- Displays a live, aligned temperature table in the terminal
- Optional test mode to simulate CPU load for thermal testing
- Clean startup/shutdown: always resets GPIO to OFF on exit

## Requirements
- Python 3.7+
- [libgpiod 2.x](https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git/) and its Python bindings
- psutil

## Installation

Install via pip (recommended):

```bash
pip install auto-temp-gpiod-ctrl
```

Or from source:

```bash
git clone https://github.com/Anthony-s-Personal-Projects/orange-pi-zero-auto-temp-ctrl.git
cd orange-pi-zero-auto-temp-ctrl
pip install .
```

## Usage

Run the controller with your desired parameters:

```bash
python -m auto_temp_gpiod_ctrl --on-temp 50 --off-temp 45 --soc-pin PH2
```

Or, if installed as a script:

```bash
auto-temp-gpiod-ctrl --on-temp 50 --off-temp 45 --soc-pin PH2
```

### Parameters
- `-i`, `--interval`   : Seconds between temperature checks and table refresh (default: 5.0)
- `--soc-pin`          : SoC pin spec to control (e.g. H2, PH2)
- `-c`, `--chip`       : GPIO chip device (e.g. gpiochip0 or /dev/gpiochip1, default: gpiochip0)
- `--on-temp`          : Threshold to turn ON GPIO (≥ this temperature, required)
- `--off-temp`         : Threshold to turn OFF GPIO (≤ this temperature, required)
- `--test-mode`        : Enable heavy calculation simulation (for testing only)

### Example

```bash
python -m auto_temp_gpiod_ctrl --on-temp 60 --off-temp 50 --soc-pin PH2 --test-mode
```

## How it works
- Reads all temperature sensors and displays a live table
- Monitors the maximum temperature
- Sends GPIO output HIGH when max_temp ≥ on_temp, LOW when max_temp ≤ off_temp
- Optionally simulates CPU load if `--test-mode` is enabled
- Always resets GPIO to OFF on exit

## License
MIT

---
**Author:** Anthony (<anthonyma24.development@gmail.com>)
