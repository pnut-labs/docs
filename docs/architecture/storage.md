# Storage layout

The system partition is littlefs, at **`/var/lib`** (2 MB, see
[Flashing](../getting-started/flashing.md)). A flash keeps it.

| Path | What |
|---|---|
| `/var/lib/settings/` | Settings' files, one per owner, and `secrets.key` |
| `/var/lib/log/` | the log, and the crash reports |
| `/var/lib/messages/` | Messages' store, appended to |
| `/var/lib/location/state` | GNSS: the last fix and the orbit data it dumped |
| `/var/lib/motion/steps` | today's steps |
| `/var/run/` | services' sockets (not on the flash) |
| `/media/sd<n>` | a card, mounted FAT only, never formatted |

On the computer (tests, `sim`) the same programs use `/tmp/...` by default:
each directory is a Kconfig option (`CONFIG_PNUT_SETTINGS_DIR`,
`CONFIG_PNUT_LOG_DIR`, `CONFIG_PNUT_MESSAGES_DIR`, …) that the target's
`fragment.config` sets.

!!! info "Why files written whole, and seldom"
    littlefs rewrites a file's blocks on every commit, and a small flash
    wears. Settings gather a burst of changes into one write a second
    after it; Messages appends; a store rewrites a file only when it must,
    writing beside the old one and renaming.

!!! warning "Trap: SQLite on littlefs"
    Measured in October: a commit rewrote nearly the whole database — 3.7 s
    for an empty one, about 12 s at 232 KB, 35–50 s at 1 MB. Stores here are
    files.
