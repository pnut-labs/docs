# Firmware updates

MCUboot starts the firmware from the first of two slots
([RFC 0013](https://github.com/pnut-labs/design/blob/master/rfcs/0013-firmware-updates.md)). An update goes into the
second slot, marked for a trial; at the next start MCUboot swaps the slots
(about 70 s for 1.5 MB, a bar on the screen: "Installing the update"),
keeping the previous firmware. The system program confirms the new one
once every program has stayed ready for 10 s; a start before that swaps
them back ("Undoing the update").

Until Packages installs updates, a trial is made by hand: see
[Flashing](../getting-started/flashing.md).
