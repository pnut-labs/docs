# Topics and settings

## Topics

A topic carries fixed-size messages that any native program may publish
and read: state and events meant for everyone (`telephony`, `wifi`,
`battery`, `network`, …;
[RFC 0005](https://github.com/pnut-labs/design/blob/master/rfcs/0005-communication.md)).
On NuttX it is a **uORB** topic; on the computer, local datagram sockets
in the loop's run directory stand in for it.

- A reader gets every message, oldest first, and **the latest one
  published before it subscribed**: a topic of state needs no first call.
- uORB keeps `depth` messages for a reader who has not read them; a newer
  one takes the oldest's place. A topic of events therefore carries a
  sequence number of its own, and a reader who sees a gap reads the state
  again.

!!! warning "Trap: the last message outlives its publisher"
    uORB keeps a topic's last message after the program that published it
    is gone: a reader started later gets that old message. A screen that
    showed a state nobody publishes any more was reading such a leftover.

## Settings

Settings (in the system program,
[RFC 0025](https://github.com/pnut-labs/design/blob/master/rfcs/0025-settings.md))
keeps every program's settings, by **owner** (a service's name) and key.

- An owner's settings are declared in its `.proto` as a message with
  `option (pnut.settings) = "<owner>"`, a field per setting with its
  default, range or choices, label and group. The program registers the
  schema as it starts, through its generated cache, and reads the values
  in a struct kept up to date.
- A target's defaults may differ: `configs/<target>/defaults.toml`,
  checked against the schemas at build time.
- Changes are written to the owner's file a second after a burst of them
  ends (`/var/lib/settings` on the device); the `settings` topic says what
  changed.
- A **secret** (a Wi-Fi passphrase) is sealed with XChaCha20-Poly1305 under
  Settings' own key (`secrets.key`); only the program that runs its owner
  reads it back, never the shell.
- A program reaches its own services' settings only; the system UI and the
  developer's shell may reach any (RFC 0012).

| Limit (master) | |
|---|---|
| Settings an owner's cache holds | 64 (`PNUT_SETTINGS_CACHE_MAX`) |
| Settings, all owners together | 256 (`CONFIG_PNUT_SETTINGS_MAX`) |
| Owners | 32 |
| Secrets holding a value | 24 |

!!! info "Why every module owns a setting"
    Each module's log level is a setting, `log.level`, of the owner named
    as the module (RFC 0026), so a module counts as an owner even when it
    has no settings of its own.
