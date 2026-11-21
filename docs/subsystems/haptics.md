# Haptics

Haptics, in the media program, drives the vibration motor
([RFC 0033](https://github.com/pnut-labs/design/blob/master/rfcs/0033-haptics.md)) through NuttX's force-feedback driver.

- Named effects (tick, click, double click, notification, ring, alarm,
  success, error): the short ones from the DRV2605's own library, the
  others as steps of a level; and callers' patterns of up to 16 steps and
  5 s.
- One vibration at a time, by use (app, interface, notification, ring,
  alarm): a higher one stops a lower, a lower one asked meanwhile is
  dropped; an app's at most one a second.
- `haptics.strength` (weak, medium, strong), `haptics.interface` (off);
  what plays on the `haptics` topic.

Interface: [Haptics](../interfaces/haptics.md). Code: `src/media/`.
