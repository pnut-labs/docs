# Power

Power, in the system program, says the battery's level and whether it
charges, and powers the device off at a low battery.

- The `battery` topic: the level and charging, at the first reading and at
  each change, from the gauge and charger the board's description names.
- At the voltage the description gives, Power stops the other programs in
  order (each finishing: the modem powered down) and powers off.
- It hands the kernel the sleep clock's rate (see [Time](time.md)).
- A restart (`pnut.Power`'s Restart, the system UI's alone) is answered
  first, then the programs stop as for the power-off.

How the device sleeps: [Power management](../architecture/power.md).
Interface: [Power](../interfaces/power.md).
