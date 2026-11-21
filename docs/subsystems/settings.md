# Settings

Settings, in the system program, keeps every program's settings by owner
and key, checks who calls, writes them to flash, and seals secrets
([RFC 0025](https://github.com/pnut-labs/design/blob/master/rfcs/0025-settings.md)). How programs declare and read them is
in [Topics and settings](../architecture/topics-settings.md).

- `settings list <owner>`, `get <owner> <key>`, `set <owner> <key>
  <value>`, `reset <owner> [<key>]` from the shell, which may do what the
  system UI may (RFC 0012).
- An owner's file is loaded on a worker, so a large owner does not hold
  the system program's loop.

Interface: [Settings](../interfaces/settings.md). Code:
`src/system/settings.c`, `settings_store.c`.

!!! warning "Trap: a setting set before its owner registered"
    A program registers its owner's schema as it starts; until then its
    keys do not exist, and a set is refused. Set defaults through the
    target's `defaults.toml` instead.
