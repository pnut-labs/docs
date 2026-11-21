# Time

Time, in the system program, keeps the clock and the time zone
([RFC 0028](https://github.com/pnut-labs/design/blob/master/rfcs/0028-time.md)).

- **Sources**, best first: the modem's network time when registered, NTP
  when Wi-Fi or mobile data is up, the GNSS receiver's time with a fix;
  the owner's own time only when there is none. Each source reports on a
  topic (`network_time`, `gnss_time`), stamped with when it was taken; a
  held reading needs *another* source to agree.
- **The zone**: an IANA name in a setting, every zone of the tz database
  compiled at build time into POSIX rules (summer time included); by
  default it follows the network's offset. Local time is converted by
  libpnut (`pnut/tz.h`), not by NuttX's localtime.
- The last good time is kept across a power loss (in the RTC's memory).

Interface: [Time](../interfaces/time.md). Code: `src/system/wallclock.c`,
`ntp.c`, `src/lib/tz.c`.

!!! warning "Trap: the clock gains in light sleep"
    The RC slow clock that times light sleep runs fast: uncorrected, the
    clock gained about 107 ppm (0.85 % of the time slept, measured). The
    board's description gives the sleep clock's rate (`sleep_clock`, in
    ppb); Power hands it to the kernel (`BOARDIOC_SLEEP_RATE`), which takes
    it off each sleep.
