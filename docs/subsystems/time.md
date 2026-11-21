# Time

Time, in the system program, keeps the clock and the time zone
([RFC 0028](https://github.com/pnut-labs/design/blob/master/rfcs/0028-time.md)).

- **Sources**, best first: the modem's network time when registered, NTP
  when Wi-Fi or mobile data is up, the GNSS receiver's time with a fix;
  the owner's own time only when there is none. Each source reports on a
  topic (`network_time`, `gnss_time`), stamped with when it was taken; a
  held reading needs *another* source to agree.
- **The zone**: an IANA name in a setting, one of the tz database's
  `zone.tab` (about 420) or UTC, each with its current POSIX rule (summer
  time included), in a table kept in the source (`src/lib/tz_zones.c`,
  written by `tools/gen-zones`: run it again to update the rules); by
  default it follows the network's offset. Local time is converted by
  libpnut (`pnut/tz.h`), not by NuttX's localtime.
- The last good time, and where it came from, is kept in Time's state
  file (`/var/lib/time` on the T-Deck Max, `CONFIG_PNUT_TIME_STATE`), so
  that after a power loss the clock starts near it. Across a reset the
  chip's RTC keeps the time.

Interface: [Time](../interfaces/time.md). Code: `src/system/wallclock.c`,
`ntp.c`, `src/lib/tz.c`.

!!! warning "Trap: the clock gains in light sleep"
    The RC slow clock that times light sleep runs fast: uncorrected, the
    clock gained 107 ppm of the time slept (about 9 s for a day asleep),
    measured with sleeps of at most 2 s. Single sleeps of about 24 s had
    gained about 0.85 %, a separate measurement; why they differ is not
    known. The board's description gives the sleep clock's rate
    (`sleep_clock`, in ppb); Power hands it to the kernel
    (`BOARDIOC_SLEEP_RATE`), which takes it off each sleep.
