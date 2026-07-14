from system.hexpansion.config import HexpansionConfig
from machine import Pin
import time

# --- PORTS ---
PORT_TX = 1
PORT_RX = 6

# --- TX SIDE (HEX 4) ---
cfg_tx = HexpansionConfig(PORT_TX)
tx_data = cfg_tx.pin[0]   # HS0
tx_clk  = cfg_tx.pin[1]   # HS1

tx_data.init(Pin.OUT)
tx_clk.init(Pin.OUT)

tx_data.value(0)
tx_clk.value(0)

SPEED = 2

# --- RX SIDE (HEX 5) ---
cfg_rx = HexpansionConfig(PORT_RX)
rx_data = cfg_rx.pin[0]   # HS0
rx_clk  = cfg_rx.pin[1]   # HS1

rx_data.init(Pin.IN)
rx_clk.init(Pin.IN)

# --- SEND ONE BYTE BIT‑BY‑BIT ---
def send_byte(byte):
    rx_byte = 0

    for i in range(8):
        bit = (byte >> i) & 1
        tx_data.value(bit)

        # Rising edge
        tx_clk.value(1)

        # Allow expander to propagate
        for _ in range(SPEED):
            pass

        # Sample
        rx_bit = rx_data.value()
        rx_byte |= (rx_bit << i)

        # Falling edge
        tx_clk.value(0)

        for _ in range(SPEED):
            pass
    
    return rx_byte

# --- SEND A STRING ---
def send_string(s):
    for ch in s:
        tx_val = ord(ch)
        rx_val = send_byte(tx_val)
        print("TX:", ch, " RX:", chr(rx_val))

# --- MAIN LOOP ---
while True:
    msg = "This is the Badge to Badge local test"
    msg_len = len(msg)

    start = time.ticks_us()
    send_string(msg)
    end = time.ticks_us()

    elapsed_s = time.ticks_diff(end, start) / 1_000_000.0
    chrrate = msg_len / elapsed_s

    print("Elapsed:", elapsed_s, "seconds")
    print("Character Rate:", chrrate, "cps")
    print()

    time.sleep(1)


