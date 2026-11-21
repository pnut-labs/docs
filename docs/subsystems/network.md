# Network and Wi-Fi

The network program runs Wi-Fi and Network.

**Wi-Fi** ([RFC 0031](https://github.com/pnut-labs/design/blob/master/rfcs/0031-wifi.md)): the radio up and down with
`wifi.enabled`; a scan; a join and an address by DHCP; the link's state on
the `wifi` topic. Up to 16 known networks, last used first, kept in Wi-Fi's
settings with their passphrases as secrets, joined on their own while
Wi-Fi is on (the one joined last if in reach, else the strongest; one
whose joins fail tried less and less often, up to every 8 minutes).

**Network** ([RFC 0015](https://github.com/pnut-labs/design/blob/master/rfcs/0015-network.md)): the link in use — Wi-Fi
when joined with an address and a router, else mobile data — on the
`network` topic, with whether it costs money; NuttX's default route and
name server follow it; adb's port is reachable from Wi-Fi only.

Interfaces: [Wi-Fi](../interfaces/wifi.md),
[Network](../interfaces/network.md). Code: `src/network/`.

!!! info "2.4 GHz only"
    The ESP32-S3's Wi-Fi is 2.4 GHz: a phone's hotspot must offer it.

!!! warning "Trap: passphrases"
    A passphrase is only ever in the request and the sealed secret: never
    in a file, a commit, a log or a test script. A test joins a network
    already known, or the owner types it at the shell.
