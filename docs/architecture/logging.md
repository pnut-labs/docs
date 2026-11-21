# Logging

Every module logs through libpnut (`pnut_log()`,
[RFC 0026](https://github.com/pnut-labs/design/blob/master/rfcs/0026-log.md))
at one of four levels: **error** (someone should look), **warning**,
**info**, **debug**.

- Each module's level is a setting, `log.level` of the owner named as the
  module: `settings set <module> log.level debug`. A target may set it in
  its `defaults.toml`.
- A line is 160 characters at most. A module logging more than 50 lines in
  a second has the rest dropped and counted, and one line says how many,
  so that no module floods the log.
- The system program keeps the log's warnings and errors in files across
  restarts (`/var/lib/log` on the device) and the crash reports beside
  them: `logs [<level>] [<service>]`, `logs crashes`, `logs crash <name>`.
  Info and debug lines are only in the RAM log (`dmesg`), which the
  T-Deck Max keeps across a reset.

## What never goes in the log

- No passphrase, PIN or key, at any level.
- No phone number, message text or position above **debug**.

!!! info "Why"
    The log is read over adb or the shell, and its warnings and errors
    are kept in files; a person debugging should not see what the owner
    wrote or where they were. At debug, the developer asked for it on
    their own device.
