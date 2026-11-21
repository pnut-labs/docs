# adb over Wi-Fi

On the T-Deck Max, adbd listens on port 5555 from the start, reached once
Wi-Fi is joined (RFC 0012). A computer gets in only once its key is let in,
on the device:

1. On the computer: `adb connect <device>:5555`. It shows the device
   *unauthorized*; the device keeps the computer's key waiting.
2. On the device's shell: `adbkeys` lists the keys waiting, each with its
   fingerprint. Compare it with the computer's:
   `cut -d' ' -f1 ~/.android/adbkey.pub | base64 -d | md5sum`.
3. `adbkeys allow <n>` lets that one in. On the computer:
   `adb disconnect <device>:5555`, then `adb connect <device>:5555`.

`adbkeys forget` lets none in any more.

!!! info "Why Wi-Fi only"
    Network has NuttX's packet filter drop connections to adbd's port from
    any other link, mobile data's included: the device is not reachable for
    adb from the operator's network.
