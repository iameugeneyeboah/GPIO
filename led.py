#!/usr/bin/env python3
# LED Effects Menu for Raspberry Pi (gpiozero) with Speed Control

import argparse
from time import sleep
from gpiozero import LED, PWMLED

# ---------- Util ----------

def run_until_interrupt(fn):
    """Run a mode until Ctrl+C; then return to menu."""
    try:
        fn()
    except KeyboardInterrupt:
        print("\n↩ Returning to menu...\n")
        sleep(0.4)

def choose_speed(default_speed=1.0):
    """
    Ask the user to choose a speed multiplier.
    >1.0 = faster, <1.0 = slower.
    """
    print("\nSpeed options:")
    print(" 1) Slow (0.5×)")
    print(" 2) Normal (1.0×)")
    print(" 3) Fast (2.0×)")
    print(" 4) Custom (enter any positive number; e.g., 1.5)")
    print("Enter to keep current (", default_speed, ")")
    choice = input("Select speed [1-4 or Enter]: ").strip()
    if choice == "":
        return default_speed
    if choice == "1":
        return 0.5
    if choice == "2":
        return 1.0
    if choice == "3":
        return 2.0
    if choice == "4":
        while True:
            try:
                val = float(input("Custom speed (>0): ").strip())
                if val > 0:
                    return val
            except ValueError:
                pass
            print("Invalid number. Try again.")
    print("Invalid choice. Keeping current speed.")
    return default_speed

def scaled_sleep(base_seconds, speed):
    """
    Sleep helper that scales time by speed multiplier.
    Higher speed -> shorter sleep.
    """
    # avoid zero/negative
    duration = max(0.0, base_seconds / max(speed, 1e-6))
    sleep(duration)

# ---------- Modes ----------

def mode_basic_blink(pin: int, speed: float, on_s=0.5, off_s=0.5):
    led = LED(pin)
    print(f"▶ Basic Blink @ speed {speed}× (GPIO{pin}). Ctrl+C to stop.")
    def loop():
        while True:
            led.on();  scaled_sleep(on_s, speed)
            led.off(); scaled_sleep(off_s, speed)
    try:
        run_until_interrupt(loop)
    finally:
        led.off(); led.close()

def mode_sos_morse(pin: int, speed: float):
    led = LED(pin)
    print(f"▶ SOS (Morse) @ speed {speed}× (GPIO{pin}). Ctrl+C to stop.")
    DOT, DASH, GAP, WORD_GAP = 0.3, 0.9, 0.3, 2.0

    def dot():
        led.on();  scaled_sleep(DOT, speed)
        led.off(); scaled_sleep(GAP, speed)

    def dash():
        led.on();  scaled_sleep(DASH, speed)
        led.off(); scaled_sleep(GAP, speed)

    def loop():
        while True:
            for _ in range(3): dot()      # S: ...
            for _ in range(3): dash()     # O: ---
            for _ in range(3): dot()      # S: ...
            scaled_sleep(WORD_GAP, speed) # pause before repeat
    try:
        run_until_interrupt(loop)
    finally:
        led.off(); led.close()

def mode_heartbeat(pin: int, speed: float):
    led = LED(pin)
    print(f"▶ Heartbeat @ speed {speed}× (GPIO{pin}). Ctrl+C to stop.")
    # two quick beats then a longer rest (base times)
    def loop():
        while True:
            for _ in range(2):
                led.on();  scaled_sleep(0.12, speed)
                led.off(); scaled_sleep(0.12, speed)
            scaled_sleep(0.6, speed)
    try:
        run_until_interrupt(loop)
    finally:
        led.off(); led.close()

def mode_fade_pwm(pin: int, speed: float):
    led = PWMLED(pin)
    print(f"▶ Smooth Fade (PWM) @ speed {speed}× (GPIO{pin}). Ctrl+C to stop.")
    # Base step/delay; higher speed -> bigger step & shorter delay
    base_step  = 0.01
    base_delay = 0.02

    def loop():
        while True:
            # speed-adjusted parameters
            step  = min(0.2, base_step  * max(speed, 1e-6))
            delay = max(0.0, base_delay / max(speed, 1e-6))

            # fade in
            b = 0.0
            while b <= 1.0:
                led.value = b
                sleep(delay)
                b += step
            # fade out
            while b >= 0.0:
                led.value = b
                sleep(delay)
                b -= step
    try:
        run_until_interrupt(loop)
    finally:
        led.value = 0; led.close()

# ---------- Main ----------

def main():
    parser = argparse.ArgumentParser(description="LED Effects (gpiozero) with Speed Control")
    parser.add_argument("--pin", type=int, default=17, help="GPIO pin number (BCM). Default: 17")
    parser.add_argument("--speed", type=float, default=1.0,
                        help="Speed multiplier (>0). >1 faster, <1 slower. Default: 1.0")
    args = parser.parse_args()
    pin = args.pin
    speed = max(1e-6, args.speed)

    MENU = {
        "1": ("Basic Blink",        lambda s: mode_basic_blink(pin, s)),
        "2": ("SOS (Morse)",        lambda s: mode_sos_morse(pin, s)),
        "3": ("Heartbeat",          lambda s: mode_heartbeat(pin, s)),
        "4": ("Smooth Fade (PWM)",  lambda s: mode_fade_pwm(pin, s)),
        "q": ("Quit", None),
    }

    print("Raspberry Pi LED Effects (gpiozero) — Speed Control Enabled")
    print("Tip: Use a 220–330 Ω resistor in series with the LED.")

    while True:
        print("\n=== MENU ===")
        for k, (name, _) in MENU.items():
            print(f"{k}. {name}")
        print(f"Current speed: {speed}×")
        choice = input("Select a mode (1-4), 's' to change speed, or 'q' to quit: ").strip().lower()

        if choice == "q":
            print("Goodbye!")
            break
        if choice == "s":
            speed = choose_speed(speed)
            continue
        if choice in MENU and MENU[choice][1] is not None:
            # Optionally let user tweak speed before entering
            tweak = input("Change speed for this run? (y/N): ").strip().lower()
            run_speed = choose_speed(speed) if tweak == "y" else speed
            MENU[choice][1](run_speed)   # returns after Ctrl+C
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
