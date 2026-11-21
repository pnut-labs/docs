# LoRa

Radio, in the radios program, drives the LoRa radio (an SX1262) through
NuttX's SX126x driver ([RFC 0034](https://github.com/pnut-labs/design/blob/master/rfcs/0034-radio.md)).

- One caller at a time opens it with a LoRa configuration and a way of
  listening (always, or the chip's duty cycle), and gets the packets heard
  as a stream with credit; the 8 newest are kept for a slow reader.
- Every send is checked against the region's band plan (EU868: the
  channel within a sub-band, the power at the antenna, the air time per
  sub-band over the last hour), then sent on a worker.
- The region from `radio.region` (`auto`: the band's plan), the antenna
  from `radio.lora.antenna`; airplane mode closes the radio.
- `radio listen …`, `radio send …` from the shell.

Interface: [Radio](../interfaces/radio.md). Code: `src/radios/`.

!!! info "MeshCore's parameters"
    MeshCore's public channel (EU): 869.618 MHz, 62.5 kHz, SF8, CR 5, sync
    word `0x12` (private), preamble 32 for SF8 and below.
