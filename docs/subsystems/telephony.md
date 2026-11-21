# Telephony

The telephony program drives the modem (an A7682E on the T-Deck Max)
([RFC 0030](https://github.com/pnut-labs/design/blob/master/rfcs/0030-telephony.md)).

- The modem's UART and lines come from Board. It is powered up, and down
  in order (`AT+CPOF`, then the rail once it stops answering), also as the
  program stops.
- The UART is multiplexed with **27.010** from the start, by a
  multiplexer of the program's own on its loop: one channel for AT, one
  for mobile data.
- Its state, the SIM, registration, operator and signal are on the
  `telephony` topic; the network's time on `network_time`.
- The SIM's PIN and PUK are taken from the system UI and the developer's
  shell only (`telephony pin <PIN>`). The modem's own restarts are
  followed, three an hour at most.
- **SMS** goes to and comes from Messages as a transport.
- **Mobile data** (`telephony.data`, off by default): the AT channel dials
  the default bearer, then carries PPP to NuttX's pppd through a raw
  pseudo-terminal; a failure hangs up and tries again after 30 s,
  doubling to 10 minutes.

Interface: [Telephony](../interfaces/telephony.md). Code:
`src/telephony/`.

!!! warning "Trap: `AT+ICF`"
    Never send it: `AT+ICF=3,0` cut the link until the modem was powered
    off and on. The modem's `2,2` matches the chip's 8N1.

!!! warning "Trap: band and mode experiments"
    `AT+CNMP`/`AT+CNBP` can leave the modem searching forever, drawing
    ~80 mA and not answering. The program's setup restores them at start.

!!! warning "Trap: a guessed PIN"
    Three wrong PINs block the SIM. Tests never send a PIN that is not
    known to be right.

!!! info "Why the modem does not sleep"
    Both ways of letting it sleep (its own and DTR's) proved unreliable:
    it missed wake-ups.
