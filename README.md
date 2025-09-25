# GPIO Lab: LED and Button (Raspberry Pi)

Build and run simple GPIO projects on a Raspberry Pi: LED effects with speed control and a button-driven demo.

## Project Structure

- `led.py` — Menu-driven LED effects using gpiozero (Basic Blink, SOS, Heartbeat, Smooth Fade) with adjustable speed.
- `button.py` — Button-driven interactions (e.g., print button events or control an LED). Open the file or run with `-h` (if implemented) for details.

## Hardware You’ll Need

- Raspberry Pi with 40‑pin GPIO header
- Breadboard and jumper wires
- 1× LED
- 1× 220–330 Ω resistor (for the LED)
- 1× momentary pushbutton
- Optional: Additional LEDs/resistors for experiments

## Pin Numbering

This project uses BCM numbering (e.g., GPIO17). The default LED pin in `led.py` is 17; adjust to match your wiring.

## Wiring

- LED (with series resistor):
  - GPIO17 → resistor → LED anode (+, longer leg)
  - LED cathode (−, shorter leg) → GND

ASCII sketch:
- GPIO17 ──[220–330 Ω]──|>── GND

- Button (using internal pull-up typical for gpiozero):
  - One leg → GPIO27
  - Other leg → GND

ASCII sketch:
- GPIO27 ──[button]── GND

Tip: Place the resistor in series with the LED to limit current. Double‑check the LED orientation.

## Software Setup (Raspberry Pi OS)

```bash
sudo apt update
sudo apt install -y python3 python3-gpiozero
```

Optional (development without hardware):
```bash
export GPIOZERO_PIN_FACTORY=mock
```

## Running the LED Effects

```bash
python3 led.py --pin 17 --speed 1.0
```

- You’ll see a menu:
  - 1: Basic Blink
  - 2: SOS (Morse)
  - 3: Heartbeat
  - 4: Smooth Fade (PWM)
  - s: Change speed multiplier (>1 faster, <1 slower)
  - q: Quit
- Inside any mode, press Ctrl+C to return to the menu.

Notes:
- Uses gpiozero’s LED/PWMLED.
- PWM fade works on any GPIO via software PWM in gpiozero.

## Running the Button Demo

```bash
python3 button.py
```

- If `button.py` supports CLI options, run:
  - `python3 button.py -h`
- Otherwise, open `button.py` and set the GPIO pin numbers (e.g., button on GPIO27, LED on GPIO17) to match your wiring.

Typical behaviors you might implement:
- Print “pressed/released”
- Toggle an LED on press
- Detect hold/long-press to trigger a different pattern

## Safety and Tips

- Always power down or disconnect power when changing wiring.
- Never drive an LED without a resistor.
- Verify you’re using BCM numbers (not physical BOARD numbers).
- If nothing happens:
  - Check grounds and pin numbers.
  - Flip the LED orientation.
  - Try another GPIO pin.

## Troubleshooting

- Module not found: `gpiozero`
  - Install: `sudo apt install -y python3-gpiozero`
- Permission issues
  - Generally not required; run as the default `pi` user on Raspberry Pi OS.
- Running on non‑Pi hardware
  - Use the mock pin factory for basic testing, but no real hardware control will occur.

## License

Add your preferred license here.
