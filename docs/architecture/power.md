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

- USB power present (the charger is asked every 2 s);
- a light on;
- the GNSS receiver's rail on (its UART stops in light sleep);
- the modem's UART in use, and for 1 s after; its ring indicator low, and
  for 2 s after. The modem's rail itself does not hold it: the device
  light-sleeps with the modem on;
- an audio stream reserved (`/dev/audio/pcm0`, `/dev/audio/pcm_in0`);
- Wi-Fi once brought up (until a restart); the Bluetooth controller while
  it runs;
- an I2C transfer, an SPI DMA transfer;
- console input, for 6 s;
- `/dev/awake` while it is open, for a program that needs the device
  awake.

The named holds show in `/proc/pm/wakelock0` on the device. Wake
sources: the keyboard, the touch layer while it is open, LoRa's DIO1, the
IMU's interrupt, and the modem's ring indicator while the modem's rail is
on.

!!! info "Why idle at 80 MHz"
    DFS runs the CPU at 80 MHz when idle and 240 MHz when busy, with the
    chip's own calibrated core voltages (eFuse): awake went from 43 to
    27 mA.

!!! warning "Trap: the GNSS UART's transmit line"
    With the GPS rail off, the chip's transmit line into the receiver
    (GPIO 16), left high, fed the receiver through its input: 25 mA. It is
    held low while the rail is off.

!!! warning "Trap: the modem's sleep"
    Both ways of letting the modem sleep (its own and DTR's) proved
    unreliable: it missed wake-ups. The modem does not sleep.

The battery's level and charging are on the `battery` topic (Power, in the
system program); at a low battery Power stops the programs in order and
powers off, at the voltage the board's description gives.
