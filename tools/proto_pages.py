#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Write the Interfaces pages from pnut-os's .proto files.

    python tools/proto_pages.py <pnut-os checkout> [docs dir] [config]

Each interface file under proto/pnut becomes docs/interfaces/<name>.md: its
own description, then its calls (the interface's number, each method's
number, version, permission, request and reply), its topics, its settings
(key, type, default, range or choices, public or secret) and its messages
and enums, with their fields' limits (nanopb's max_size and max_count) and
the comments written above or beside each in the .proto.  The section's nav
in zensical.toml (between the "interfaces" markers) is written to match.
Nothing here is edited by hand: change the .proto in pnut-os instead.
"""

import os
import re
import subprocess
import sys
import tempfile

from google.protobuf import descriptor_pb2

FIELD_TYPES = {
    1: "double", 2: "float", 3: "int64", 4: "uint64", 5: "int32",
    6: "fixed64", 7: "fixed32", 8: "bool", 9: "string", 12: "bytes",
    13: "uint32", 15: "sfixed32", 16: "sfixed64", 17: "sint32",
    18: "sint64",
}

NAV_BEGIN = "  # interfaces: begin (tools/proto_pages.py)"
NAV_END = "  # interfaces: end"


def compile_protos(root, out):
    """A descriptor set with comments, and pnut's options as a module."""
    import grpc_tools
    import nanopb

    std = os.path.join(os.path.dirname(grpc_tools.__file__), "_proto")
    nano = os.path.join(os.path.dirname(nanopb.__file__), "generator",
                        "proto")
    proto = os.path.join(root, "proto")
    files = sorted(os.path.join("pnut", f)
                   for f in os.listdir(os.path.join(proto, "pnut"))
                   if f.endswith(".proto"))
    common = [sys.executable, "-m", "grpc_tools.protoc", "-I", proto,
              "-I", nano, "-I", std]
    subprocess.run(common + ["--python_out=" + out,
                             "pnut/options.proto"], check=True)
    desc = os.path.join(out, "descriptors.pb")
    subprocess.run(common + ["--include_source_info", "--include_imports",
                             "--descriptor_set_out=" + desc] + files,
                   check=True)
    sys.path.insert(0, out)
    sys.path.insert(0, nano)
    import nanopb_pb2  # noqa: F401  (registers nanopb's options)
    from pnut import options_pb2  # noqa: F401
    fds = descriptor_pb2.FileDescriptorSet()
    with open(desc, "rb") as f:
        fds.ParseFromString(f.read())
    return fds


def reparse(fds):
    """Parse again now that the options' extensions are registered."""
    data = fds.SerializeToString()
    fds = descriptor_pb2.FileDescriptorSet()
    fds.ParseFromString(data)
    return fds


def comments(fd):
    out = {}
    for loc in fd.source_code_info.location:
        text = loc.leading_comments or loc.trailing_comments
        if text:
            out[tuple(loc.path)] = " ".join(
                line.strip() for line in text.strip().splitlines())
    return out


def file_intro(fd):
    """The comments at the file's top, the licence's lines left out."""
    for loc in fd.source_code_info.location:
        if tuple(loc.path) == (12,):          # syntax
            parts = [c for c in loc.leading_detached_comments
                     if "SPDX" not in c and "Copyright" not in c]
            return "\n\n".join(" ".join(l.strip() for l in c.splitlines())
                               for c in parts)
    return ""


def ext(options, module, name):
    """An extension's value on options, or None when not set."""
    import nanopb_pb2
    from pnut import options_pb2
    mod = {"nanopb": nanopb_pb2, "pnut": options_pb2}[module]
    field = getattr(mod, name)
    return options.Extensions[field] if options.HasExtension(field) else None


def esc(text):
    return (text or "").replace("|", "\\|").replace("<", "&lt;")


# Every message's and enum's full name: (its page, its anchor)

TYPES = {}
PAGE = [""]                                    # The page being written


def index_types(fd):
    base = os.path.splitext(os.path.basename(fd.name))[0]

    def walk(prefix, anchor_prefix, msgs, enums):
        for e in enums:
            TYPES[prefix + e.name] = (base, anchor(anchor_prefix + e.name))
        for m in msgs:
            TYPES[prefix + m.name] = (base, anchor(anchor_prefix + m.name))
            walk(prefix + m.name + ".", anchor_prefix + m.name + "-",
                 m.nested_type, m.enum_type)

    walk("." + fd.package + ".", "", fd.message_type, fd.enum_type)


def link(full, text):
    if full not in TYPES:
        return "`%s`" % text
    page, anc = TYPES[full]
    return "[`%s`](%s#%s)" % (text, "" if page == PAGE[0] else page + ".md",
                              anc)


def type_name(field):
    if field.type in (11, 14):                 # message, enum
        return link(field.type_name, field.type_name.split(".")[-1])
    return "`" + FIELD_TYPES.get(field.type, "?") + "`"


def limits(field):
    out = []
    nano = ext(field.options, "nanopb", "nanopb")
    if nano is not None:
        if nano.HasField("max_size"):
            out.append("max_size %d" % nano.max_size)
        if nano.HasField("max_count"):
            out.append("max_count %d" % nano.max_count)
    if field.label == 3:
        out.insert(0, "repeated")
    return ", ".join(out)


def anchor(name):
    return name.lower()


def message_md(msg, path, cm, depth=3, parent=""):
    full = parent + msg.name
    lines = ["%s `%s` {#%s}" % ("#" * depth, msg.name, anchor(full)), ""]
    if cm.get(path):
        lines += [cm[path], ""]
    topic = ext(msg.options, "pnut", "topic")
    if topic:
        lines += ["Topic **`%s`**, depth %d." %
                  (topic, ext(msg.options, "pnut", "depth") or 1), ""]
    if msg.field:
        lines += ["| # | Field | Type | Limits | |", "|---|---|---|---|---|"]
        for j, f in enumerate(msg.field):
            lines.append("| %d | `%s` | %s | %s | %s |" % (
                f.number, f.name, type_name(f), limits(f),
                esc(cm.get(path + (2, j), ""))))
        lines.append("")
    for k, e in enumerate(msg.enum_type):
        lines += enum_md(e, path + (4, k), cm, depth + 1, full + "-")
    for k, m in enumerate(msg.nested_type):
        if not m.options.map_entry:
            lines += message_md(m, path + (3, k), cm, depth + 1, full + "-")
    return lines


def enum_md(enum, path, cm, depth=3, parent=""):
    lines = ["%s `%s` {#%s}" % ("#" * depth, enum.name,
                                anchor(parent + enum.name)), ""]
    if cm.get(path):
        lines += [cm[path], ""]
    lines += ["| Value | Name | |", "|---|---|---|"]
    for j, v in enumerate(enum.value):
        lines.append("| %d | `%s` | %s |" % (v.number, v.name,
                                             esc(cm.get(path + (2, j), ""))))
    return lines + [""]


def settings_md(msg, path, cm):
    owner = ext(msg.options, "pnut", "settings")
    lines = ["### Settings of `%s`" % owner, ""]
    if cm.get(path):
        lines += [cm[path], ""]
    lines += ["| Key | Type | Default | Range or choices | | |",
              "|---|---|---|---|---|---|"]
    slots = {}
    for f in msg.field:
        s = ext(f.options, "pnut", "setting")
        m = re.fullmatch(r"(.+)\.(\d+)", (s.key or f.name) if s else "")
        if m:
            slots.setdefault(m.group(1), []).append(int(m.group(2)))
    for j, f in enumerate(msg.field):
        s = ext(f.options, "pnut", "setting")
        if s is None:
            continue
        key = s.key or f.name
        m = re.fullmatch(r"(.+)\.(\d+)", key)
        if m and int(m.group(2)) != min(slots[m.group(1)]):
            continue                        # One row for a key's slots
        if m:
            n = slots[m.group(1)]
            key = "%s.%d` … `%s.%d` (%d slots)" % (
                m.group(1), min(n), m.group(1), max(n), len(n))
        kind = ("secret" if s.secret else
                "choice" if s.choices else FIELD_TYPES.get(f.type, "?"))
        rng = (", ".join(s.choices) if s.choices else
               "%d to %d" % (s.min, s.max)
               if s.HasField("min") or s.HasField("max") else "")
        flags = ", ".join(x for x in ("public" if s.public else "",
                                      s.unit) if x)
        lines.append("| `%s | %s | %s | %s | %s | %s |" % (
            key if m else key + "`", kind,
            "`%s`" % s.default if s.default else "", esc(rng), flags,
            esc(cm.get(path + (2, j), ""))))
    return lines + [""]


TITLES = {"wifi": "Wi-Fi", "ui": "UI"}


def title_of(fd):
    base = os.path.splitext(os.path.basename(fd.name))[0]
    return TITLES.get(base, base.replace("_", " ").capitalize())


def page(fd):
    PAGE[0] = os.path.splitext(os.path.basename(fd.name))[0]
    cm = comments(fd)
    name = os.path.basename(fd.name)
    lines = ["# %s" % title_of(fd), "",
             "!!! note \"Generated\"",
             "    Written from [`proto/%s`](https://github.com/pnut-labs/"
             "pnut-os/blob/master/proto/%s) on pnut-os's master; change "
             "the comments there, not here." % (fd.name, fd.name), ""]
    intro = file_intro(fd)
    if intro:
        lines += [intro, ""]
    for i, svc in enumerate(fd.service):
        iface = ext(svc.options, "pnut", "iface")
        lines += ["## Service `%s`" % svc.name, ""]
        if cm.get((6, i)):
            lines += [cm[(6, i)], ""]
        if iface is not None:
            lines += ["Interface number **%d**." % iface, ""]
        lines += ["| # | Call | Request | Reply | | |",
                  "|---|---|---|---|---|---|"]
        for j, m in enumerate(svc.method):
            num = ext(m.options, "pnut", "method")
            ver = ext(m.options, "pnut", "version") or 1
            perm = ext(m.options, "pnut", "permission") or ""
            req = link(m.input_type, m.input_type.split(".")[-1])
            reply = ("stream " if m.server_streaming else "") + \
                link(m.output_type, m.output_type.split(".")[-1])
            extra = ", ".join(x for x in (
                "v%d" % ver if ver != 1 else "",
                "needs `%s`" % perm if perm else "") if x)
            lines.append("| %s | `%s` | %s | %s | %s | %s |" % (
                num if num is not None else "", m.name, req, reply, extra,
                esc(cm.get((6, i, 2, j), ""))))
        lines.append("")
    topics = [(i, m) for i, m in enumerate(fd.message_type)
              if ext(m.options, "pnut", "topic")]
    settings = [(i, m) for i, m in enumerate(fd.message_type)
                if ext(m.options, "pnut", "settings")]
    if topics:
        lines += ["## Topics", ""]
        for i, m in topics:
            lines += message_md(m, (4, i), cm)
    if settings:
        lines += ["## Settings", ""]
        for i, m in settings:
            lines += settings_md(m, (4, i), cm)
    rest = [(i, m) for i, m in enumerate(fd.message_type)
            if (i, m) not in topics and (i, m) not in settings]
    if rest:
        lines += ["## Messages", ""]
        for i, m in rest:
            lines += message_md(m, (4, i), cm)
    if fd.enum_type:
        lines += ["## Enums", ""]
        for i, e in enumerate(fd.enum_type):
            lines += enum_md(e, (5, i), cm)
    return "\n".join(lines).rstrip() + "\n"


def iface_of(fd):
    for svc in fd.service:
        n = ext(svc.options, "pnut", "iface")
        if n is not None:
            return n
    return None


def write_nav(config, entries):
    with open(config) as f:
        text = f.read()
    begin = text.index(NAV_BEGIN)
    end = text.index(NAV_END)
    body = "".join('    { "%s" = "%s" },\n' % e for e in entries)
    text = text[:begin + len(NAV_BEGIN)] + "\n" + body + text[end:]
    with open(config, "w") as f:
        f.write(text)


def main():
    root = os.path.abspath(sys.argv[1])
    docs = sys.argv[2] if len(sys.argv) > 2 else "docs"
    config = sys.argv[3] if len(sys.argv) > 3 else "zensical.toml"
    out_dir = os.path.join(docs, "interfaces")
    os.makedirs(out_dir, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        fds = reparse(compile_protos(root, tmp))
        ours = [fd for fd in fds.file if fd.name.startswith("pnut/")
                and fd.name != "pnut/options.proto"]
        for fd in fds.file:
            index_types(fd)
        rows = []
        nav = [("Overview", "interfaces/index.md")]
        for fd in sorted(ours, key=lambda fd: (iface_of(fd) is None,
                                               iface_of(fd) or 0, fd.name)):
            base = os.path.splitext(os.path.basename(fd.name))[0]
            with open(os.path.join(out_dir, base + ".md"), "w") as f:
                f.write(page(fd))
            n = iface_of(fd)
            svcs = ", ".join("`%s`" % s.name for s in fd.service)
            rows.append("| %s | [%s](%s.md) | %s |" % (
                n if n is not None else "", title_of(fd), base, svcs))
            nav.append((title_of(fd), "interfaces/%s.md" % base))
    with open(os.path.join(out_dir, "index.md"), "w") as f:
        f.write("# Interfaces\n\n"
                "Every interface pnut-os's programs serve, by its number, "
                "and the files that only declare messages (no number). "
                "Each page is written from the .proto file on pnut-os's "
                "master by `tools/proto_pages.py`.\n\n"
                "| # | Interface | Services |\n|---|---|---|\n" +
                "\n".join(rows) + "\n")
    write_nav(config, nav)
    print("%d interface pages" % len(rows))


if __name__ == "__main__":
    main()
