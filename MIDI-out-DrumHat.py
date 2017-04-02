#!/usr/bin/env python3

import cap1xxx
import time
import rtmidi2

"""

4 3 2
5 7 1
 6 0

"""

#modificado de los ejemplos de pimoroni para que use el rtmidi2 y se convierta
# en un instrumento MIDI

dh = cap1xxx.Cap1188(
    i2c_addr=0x2c,
    alert_pin=25)

ledmap = [
    5,
    4,
    3,
    2,
    1,
    0,
    6,
    7
]

state = [True] * 8

#Definimos el canal MIDI de salida
midi_out = rtmidi2.MidiOut()
midi_out.open_port(0)


def handle_press(event):
    """
    funcion para cuando se pulsa un pad del drum hat

    event: evento que lo dispara
    """
    # Siempre usamos la nota relacionada con el evento +1
    # por comodidad y la velocity 100
    midi_out.send_noteon(153,  event.channel + 1, 100)
    dh.set_led_state(ledmap[event.channel], True)


def handle_release(event):
    """
    funcion para cuando se despulsa un pad del drum hat

    event: evento que lo dispara
    """
    dh.set_led_state(ledmap[event.channel], False)

for x in range(8):
    dh.on(x, event='press', handler=handle_press)
    dh.on(x, event='release', handler=handle_release)

dh._write_byte(cap1xxx.R_LED_LINKING, 0b000000)

while True:
    time.sleep(1)
