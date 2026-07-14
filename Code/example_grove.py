# Prints GPIO Status

# Optional - Detect Badge2Badge

from system.hexpansion.config import HexpansionConfig
from machine import Pin
import time

PORT = 2
cfg = HexpansionConfig(PORT)

# cfg.pin = HS pins (may be empty)
# cfg.ls_pin = LS pins (may be empty)

all_pins = []

# Add HS pins if present
for p in cfg.pin:
    if p is not None:
        p.init(Pin.IN)
        all_pins.append(p)

# Add LS pins if present
for p in cfg.ls_pin:
    if p is not None:
        p.init(Pin.IN)
        all_pins.append(p)

while True:
    vals = [p.value() for p in all_pins]
    print(vals)
    time.sleep(0.05)
