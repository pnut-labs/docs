# Power management

The T-Deck Max sleeps on NuttX's own power-management framework, in the
NuttX fork: the board and its drivers **hold** the device awake while they
need it (`pm_stay()`/`pm_relax()`), and when nothing holds it, the
ESP32-S3 light-sleeps until the scheduler's next timer.

| On the cell, nothing running | |
|---|---|
| awake | about 27 mA |
| light sleep | below the battery gauge's resolution |

## What holds it awake

- USB power present (the charger's power-good, polled every 2 s);
- the backlights on; the GPS, modem and audio rails up; the radios up;
- an I2C transfer, an SPI DMA transfer;
- pnut-os itself, through `/dev/awake`.

Wake sources: the keyboard, the touch layer while it is open, the BOOT
key, LoRa's DIO1, the IMU's interrupt.

!!! info "Why idle at 80 MHz"
    DFS runs the CPU at 80 MHz when idle and 240 MHz when busy, with the
    chip's own calibrated core voltages (eFuse): awake went from 43 to
    27 mA.

!!! warning "Trap: the GNSS receiver's TX line"
    With the GPS rail off, its UART's TX line left high fed the receiver
    through its input: 25 mA. It is driven low while the rail is off.

!!! warning "Trap: the modem's sleep"
    Both ways of letting the modem sleep (its own and DTR's) proved
    unreliable: it missed wake-ups. The modem does not sleep.

The battery's level and charging are on the `battery` topic (Power, in the
system program); at a low battery Power stops the programs in order and
powers off, at the voltage the board's description gives.
