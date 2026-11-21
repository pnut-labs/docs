# Location

Location, in the sensors program, drives the GNSS receiver (u-blox, over
UBX: `ubx.c`) ([RFC 0035](https://github.com/pnut-labs/design/blob/master/rfcs/0035-location.md)).

- On only while a caller waits for a position or follows them, and 5 s
  after. At each start it is given the time (when the clock came from a
  network or satellites), the last position, and the orbit data it dumped
  before it was switched off, kept in `/var/lib/location/state`.
- A request is answered from a recent fix without switching on, or with
  the best known when its time runs out.
- Positions are rounded to 0.05 degrees unless precise ones are asked.
- The `location` topic says on, fix, satellites — never where. The
  satellites' time goes to Time on `gnss_time`.

Interface: [Location](../interfaces/location.md). Code: `src/sensors/`.

!!! warning "Trap: a position is private"
    Never in a log above debug, a file outside its state, a report or a pull
    request.

!!! warning "Trap: the receiver's TX line"
    Left high while the GPS rail was off, it fed the receiver: 25 mA. It is
    driven low while the rail is off.
