# Storage layout

The system partition is littlefs, at **`/var/lib`** (2 MB, see
[Flashing](../getting-started/flashing.md)). A flash keeps it.

| Path | What |
|---|---|
| `/var/lib/settings/` | Settings' files, one per owner, and `secrets.key` |
| `/var/lib/log/` | the log's warnings and errors, and the crash reports |
| `/var/lib/messages/` | Messages' store, appended to |
| `/var/lib/location/state` | GNSS: the last fix and the orbit data it dumped |
| `/var/lib/motion/steps` | today's steps |
| `/var/lib/time` | Time's state: the last good time, and where it came from |
| `/var/lib/adb/keys`, `keys.new` | the keys of the computers adb lets in, and of those waiting (`adbkeys`) |
| `/var/run/` | services' sockets (not on the flash) |
| `/media/sd<n>` | a card, mounted FAT only, never formatted |

Each place is a Kconfig option. Settings, Log, Messages and Time use
`/tmp/...` by default, on the computer (tests, `sim`); the T-Deck Max's
`fragment.config` moves them to `/var/lib` (`CONFIG_PNUT_SETTINGS_DIR`,
`CONFIG_PNUT_LOG_DIR`, `CONFIG_PNUT_MESSAGES_DIR`,
`CONFIG_PNUT_TIME_STATE`). Location's and Motion's
(`CONFIG_PNUT_LOCATION_DIR`, `CONFIG_PNUT_MOTION_DIR`) are in `/var/lib`
by default.

!!! info "Why files written whole, and seldom"
    littlefs rewrites a file's blocks on every commit, and a small flash
    wears. Settings gather a burst of changes into one write a second
    after it; Messages appends; a store rewrites a file only when it must,
    writing beside the old one and renaming.

!!! warning "Trap: SQLite on littlefs"
    Measured in October: a commit rewrote nearly the whole database — 3.7 s
    for an empty one, about 12 s at 232 KB, 35–50 s at 1 MB. Stores here are
    files.
