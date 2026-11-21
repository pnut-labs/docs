# Writing these docs

The site is built with [Zensical](https://zensical.org) from the Markdown
under `docs/` and published to GitHub Pages from `master`.

## Building it

From the repository's root, with Python 3.11 or later (the workflow uses
3.13):

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
git clone https://github.com/pnut-labs/pnut-os ../pnut-os   # once
.venv/bin/python tools/proto_pages.py ../pnut-os            # Interfaces
.venv/bin/zensical serve                                    # http://localhost:8000
```

`zensical build --clean` writes the site to `site/`, which is not kept in
git, nor are the generated `docs/interfaces/` pages. Without the
`tools/proto_pages.py` step the Interfaces section is empty. That step also
writes the section's navigation into `zensical.toml`, which git keeps with
the Overview entry alone: do not commit those lines (`git restore
zensical.toml` takes them out, with any change of your own to the file).

## The Interfaces pages

`tools/proto_pages.py` compiles every `.proto` under `proto/pnut` of a
pnut-os checkout and writes one page per file: the interface's number, its
calls with their numbers, versions and permissions, its topics, its
settings and its messages and enums with their limits, each with the
comment written above or beside it. It also writes the section's
navigation in `zensical.toml` (between the `interfaces` markers).

To change what an interface's page says, change the comments in its
`.proto` in pnut-os. The site picks it up at its next build: on every
merge here, every day, and on demand (the workflow's *Run workflow*).

## Conventions

- One page per subsystem, part of the system UI, or topic; a page links to
  its RFC and to the code (`src/...` on GitHub) rather than repeating them.
- The reason for something that looks odd goes in a **Why** box; something
  that bit us goes in a **Trap** box:

    ```markdown
    !!! info "Why"
        Wi-Fi is off by default: a radio up keeps the device from its light
        sleep.

    !!! warning "Trap"
        A double-quoted word in an NSH command line can leave the command
        without its prompt.
    ```

- Pages describe master. A pull request in pnut-os that changes behaviour
  comes with a pull request here, and the pnut-os one merges first: this
  repository's check builds against pnut-os's master, so a page that links
  to what the pnut-os pull request adds fails it until then. Once pnut-os
  has merged, run this pull request's check again, then merge it. To see
  the pages as they will be, run `tools/proto_pages.py` against the pnut-os
  branch.
- A pnut-os change that renames or removes a `.proto` file, a message or an
  enum that a page here links to changes those links in its pull request
  here: until that merges, the site's build fails and the site stays as it
  was.
- Plain words, short sentences; numbers with their units.

## What never goes here

The site is public. Never write a phone number, an IMEI or an ICCID, a
PIN, a Wi-Fi network's name or passphrase from a real place, a person's
name or a message's text, a position, or a key. Screens shown here come
from the tests' made-up content, never from a phone in use.
The same holds for anything pasted: log lines, shell and adb sessions,
modem answers and scan results come from the simulator or the tests, or
have those values replaced with made-up ones. It holds for the comments in
pnut-os's `.proto` files too: they are published here as they are written.
