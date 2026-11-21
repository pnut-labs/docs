# The shell over serial

The T-Deck Max's NuttShell is on its USB Serial/JTAG port,
`/dev/ttyACM0` on Linux. Any terminal works (`picocom /dev/ttyACM0`); for
scripts and tests, two tools in pnut-os's `tools/device/` (they need
pyserial):

```sh
python3 tools/device/nsh.py "uname -a" "free" "logs warning"
python3 tools/device/uiscreen.py -o shot.png "keys alt+n" "keys s"
```

`nsh.py` sends each command and prints its output up to the next prompt;
`uiscreen.py` runs its commands, then saves what the screen shows as a
PNG. Close any other serial monitor first.

## Commands worth knowing

| Command | Does |
|---|---|
| `keys w alt+enter f2`, `keys text <word>` | presses keys as the keyboard's driver gives them |
| `screen` | the framebuffer as a base64 PBM |
| `logs [<level>] [<service>]`, `logs crashes` | the log kept in files across restarts, the crash reports |
| `settings list <owner>`, `get`, `set`, `reset` | any program's settings, as the system UI may |
| `telephony`, `messages`, `wifi`, `radio`, `location`, `motion`, `haptics` | each service's state and its calls |
| `uidemo list` … | an app from the shell showing one of the system UI's templates with made-up content |

Screenshots stay on your computer: they can show neighbours' network
names and real messages.

!!! warning "Trap: `#` starts a comment"
    NSH treats `#` at the start of a word as a comment: the rest of the
    line is lost. Quote it, or avoid it in test data.

!!! warning "Trap: double-quoted arguments"
    A double-quoted argument (`"Still on for Thursday?"`) once left the
    command without its prompt, and the next command looked hung. Keep test
    arguments to plain words.

!!! warning "Trap: a command's length"
    A line is 128 bytes at most, and 16 arguments: over them NSH prints an
    error but still runs the command, cut. `nsh.py --pace 32` types a long
    line slowly: the console drops characters of a fast one.

!!! warning "Trap: background output"
    A background command (`cmd &`) writes to the console whenever it likes,
    which breaks the prompt detection: a later command looks hung. Redirect
    it: `cmd > /dev/null &`.

!!! warning "Trap: a hung command"
    `nsh.py` waits for the prompt; if a command never returns, it times out,
    and rerunning it changes nothing. Look with a raw serial read, or reset
    the board.
