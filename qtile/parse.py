import os
import sys
from libqtile.config import KeyChord
from libqtile.config import Key
from libqtile.confreader import Config

colors = [
    "#8e733f",
    "#99d59d",
    "#b380b0",
    "#c1a78e",
    "#ce9bcb",
    "#e49b5d",
    "#ebc06d",
    "#f17c64",
]


def gen_key_str(key):
    mod_str = " + ".join(key.modifiers)
    if len(key.modifiers) > 0:
        key_str = f"<b>{mod_str} + {key.key}</b>: {key.desc}"
    else:
        key_str = f"<b>{key.key}</b>: {key.desc}"

    return key_str


def wrap(wrap_str):
    return f"<tt>{wrap_str}</tt>"


def safe_get_str(list, i, bound):
    if i >= bound:
        return "\n"
    else:
        return list[i]


if len(sys.argv) > 1:
    config_path = sys.argv[1]
else:
    config_path = os.path.join(
        os.path.expanduser("~"), ".config/qtile/config.py"
    )

cfg = Config(config_path)
cfg.load()

key_chords = []

groups = {}
groups["GROUP ACTIONS"] = []
groups["WINDOW ACTIONS"] = []
groups["LAYOUT ACTIONS"] = []
groups["AUDIO ACTIONS"] = []
groups["LAUNCH"] = []
groups["CONNECTIONS"] = []
groups["NOTIFICATIONS"] = []
groups["SYSTEM ACTIONS"] = []
groups["OTHER"] = []

for key in cfg.keys:
    if isinstance(key, Key):
        key_str = gen_key_str(key)

        if "group: " in key.desc.lower():
            groups["GROUP ACTIONS"].append(
                    key_str.replace("Group: ", ""))
        elif "layout: " in key.desc.lower():
            groups["LAYOUT ACTIONS"].append(
                    key_str.replace("Layout: ", ""))
        elif "window: " in key.desc.lower():
            groups["WINDOW ACTIONS"].append(
                    key_str.replace("Window: ", ""))
        elif "audio: " in key.desc.lower():
            groups["AUDIO ACTIONS"].append(
                    key_str.replace("Audio: ", ""))
        elif "launch: " in key.desc.lower():
            groups["LAUNCH"].append(
                    key_str.replace("Launch: ", ""))
        elif "connections: " in key.desc.lower():
            groups["CONNECTIONS"].append(
                    key_str.replace("Connections: ", ""))
        elif "system: " in key.desc.lower():
            groups["SYSTEM ACTIONS"].append(
                    key_str.replace("System: ", ""))
        elif "notifications: " in key.desc.lower():
            groups["NOTIFICATIONS"].append(
                    key_str.replace("Notifications: ", ""))
        else:
            groups["OTHER"].append(key_str)
    if isinstance(key, KeyChord):
        key_chords.append(key)

chords = {}
for chord in key_chords:
    mod_str = " + ".join(chord.modifiers)
    chord_str = f"{chord.mode} ({mod_str} + {chord.key})"
    chords[chord_str] = []
    for key in chord.submappings:
        if not key.key == "Escape":
            chords[chord_str].append(gen_key_str(key))

keylist = []

gkeys = [key for key in list(groups.keys()) if not key == "OTHER"]
gkeys.sort()
lastc = 0
for i, group in enumerate(gkeys):
    lastc = i
    cur_op = f"<span foreground='{colors[i % len(colors)]}'>"
    keylist.append(f"{cur_op}<b><tt>  {group}</tt></b></span>\n")
    groups[group].sort()
    for key_str in groups[group]:
        keylist.append(f"{cur_op}<tt>    {key_str}</tt></span>\n")


if len(groups["OTHER"]) > 0:
    lastc += 1
    cur_op = f"<span foreground='{colors[lastc % len(colors)]}'>"
    keylist.append(f"{cur_op}<tt><b>  OTHER:</b></tt></span>\n")
    groups["OTHER"].sort()
    for key_str in groups["OTHER"]:
        keylist.append(f"{cur_op}<tt>    {key_str}</tt></span>\n")
    lastc += 1


ckeys = list(chords.keys())
ckeys.sort()
chordlist = []
for i, chord in enumerate(ckeys):
    i += lastc
    chords[chord].sort()
    cur_op = f"<span foreground='{colors[i % len(colors)]}'>"
    chordlist.append(f"{cur_op}<tt><b>  {chord}</b></tt></span>\n")
    for key in chords[chord]:
        chordlist.append(f"{cur_op}<tt>    {key}</tt></span>\n")

# Replace mod keys with human description
for i in range(len(keylist)):
    keylist[i] = keylist[i].replace("mod1", "alt")
    keylist[i] = keylist[i].replace("mod4", "win")

for i in range(len(chordlist)):
    chordlist[i] = chordlist[i].replace("mod4", "win")
    chordlist[i] = chordlist[i].replace("mod1", "alt")

with open("keychords_mangled.txt", "w") as file:
    n = int(len(keylist) / 2) if \
        int(len(keylist) / 2) > len(chordlist) else len(chordlist)
    for i in range(0, n + 1):
        file.write(safe_get_str(keylist, n * 0 + i, n))
        file.write(safe_get_str(keylist, n * 1 + i, len(keylist)))
        file.write(safe_get_str(chordlist, i, len(chordlist)))
