"""Qtile Configuration."""

# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import math
import os
import re
import subprocess
import time
from typing import List  # noqa: F401

import libqtile
import psutil

# from libqtile.utils import guess_terminal
from libqtile import bar, hook, layout, widget
from libqtile.config import (Click, Drag, EzKey, Group, Key, KeyChord, Match,
                             Screen)
from libqtile.core.manager import Qtile
from libqtile.lazy import lazy
from libqtile.widget import base
from Xlib import X, display
from Xlib.ext import randr

LOCK_WALLPAPER = "/usr/share/wallpapers/hex_melange_2_lock.png"
WALLPAPER = "/usr/share/wallpapers/hex_melange_2.png"


def send_notification(message, app, urgency="normal", icon=None):
    """Send a notification using dunstify."""
    if icon is not None:
        subprocess.call(
            ["dunstify", "-a", f"{app}", f"{message}", "-u", urgency, "-i", icon]
        )
    else:
        subprocess.call(["dunstify", "-a", f"{app}", f"{message}", "-u", urgency])


def send_progress(message, app, progress, urgency="low"):
    """Send a progress notification using dunstify."""
    subprocess.call(
        [
            "dunstify",
            "-a",
            f"{app}",
            f"{message}",
            "-h",
            f"int:value:{progress}",
            "-u",
            urgency,
        ]
    )


def subprocess_output(args):
    """Get the output of a subprocess."""
    return (
        subprocess.Popen(args, stdout=subprocess.PIPE, start_new_session=True)
        .communicate()[0]
        .decode("utf-8")
        .strip("\n")
    )


def get_clipboard(clipboard="primary"):
    """Returns clipboard contents via xclip.

    Args:
        selection (string): 'primary', 'secondary', or 'clipboard'.

    Returns:
        string: contents of clipboard / selection
    """
    return subprocess_output(["xclip", "-selection", clipboard, "-o"])


def open_in_firefox(url, how="tab"):
    """Open url in firefox.

    Args:
        url (string): url to open
        how (string): 'window', 'tab', 'private'
    """
    mode_map = {
        "window": "--new-window",
        "tab": "--new-tab",
        "private": "--private-window",
    }
    subprocess.call(["firefox", mode_map[how], url])


def g_scholar_search(query, how="window"):
    """Search query in google scholar, open in firefox.

    Args:
        query (string): what to search
    """
    query_str = f"https://scholar.google.com/scholar?hl=en&q={query}"
    open_in_firefox(query_str, how=how)


def scholar_search_cur_selection(qtile):
    """Open a google scholar search of the current selection in firefox."""
    selection = get_clipboard("primary")
    send_notification(
        f"Searching for: {selection}",
        "Scholar Search",
        icon="/home/hawo/dotfiles/qtile/img/gscholar_logo.png",
    )
    g_scholar_search(selection, how="tab")


def open_selection_in_firefox(qtile):
    """Open Highlighed URL in firefox"""
    selection = get_clipboard("primary")
    send_notification(
        f"Opening {selection} as URL in firefox.",
        "Open In Firefox",
        icon="/home/hawo/dotfiles/qtile/img/firefox_logo.png",
    )
    open_in_firefox(selection, how="tab")


def check_process_running(proc_name):
    """Check if a process is running."""
    for proc in psutil.process_iter():
        try:
            if proc_name.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return False

def move_to_prev_screen(qtile):
    """Move a window to the next screen."""
    active_win = qtile.current_window
    next_screen = (qtile.current_screen.index - 1) % len(qtile.screens)
    active_win.cmd_toscreen(next_screen)
    qtile.focus_screen(next_screen, warp=True)
    active_win.focus(warp=True)

def move_to_next_screen(qtile):
    """Move a window to the next screen."""
    active_win = qtile.current_window
    next_screen = (qtile.current_screen.index + 1) % len(qtile.screens)
    active_win.cmd_toscreen(next_screen)
    qtile.focus_screen(next_screen, warp=True)
    active_win.focus(warp=True)


def circular_selector(options):
    """Use a circular selector for selecting one of the commands"""
    # sel = subprocess.call(["/home/hawo/bin/selgl", "480", f"{len(options)}"],
    #                        start_new_session=True)
    # if sel > 0:
    #     return options[sel]

    return None


@lazy.function
def circ_selector_pen(qtile):
    keystrokes = ["1", "2", "3", "K", "J", "O", "P"]
    selected = circular_selector(keystrokes)
    send_notification("test")
    if selected is not None:
        subprocess.call(["xdotool", "key", keystrokes[selected]])


def rofi_selector(option_string, prompt):
    """Create a rofi selector for options in option_str."""
    child_process = subprocess.Popen(
        ["rofi", "-dmenu", "-p", prompt, "-i"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    child_process.stdin.write(option_string.encode("utf-8"))
    return child_process.communicate()[0].decode("utf-8").strip("\n")


def move_to_group_selector(qtile):
    """Move window to a group with a rofi selector."""
    active_win = qtile.current_window
    str_groups = "\n".join(
        [
            f"{index:4} {g.label} \uf942 {g.name}"
            for index, g in enumerate(qtile.groups, start=1)
        ]
    )
    target = re.split(r"\s+", rofi_selector(str_groups, "chose group"))[-1]
    active_win.cmd_togroup(target)


def group_switch_selector(qtile):
    """Switch focus to a group with a selector."""
    str_groups = "\n".join(
        [
            f"{index:4} {g.label} \uf942 {g.name}"
            for index, g in enumerate(qtile.groups, start=1)
        ]
    )
    target = re.split("\s+", rofi_selector(str_groups, "chose group"))
    qtile.groups[int(target[1]) - 1].cmd_toscreen()


def shutdown_reboot_menu(qtile):
    """Open a rofi menu for shutting down or rebooting."""
    option_str = "\n".join(["shutdown", "reboot", "suspend", "nothing"])
    result = rofi_selector(option_str, "Shutdown Menu")
    if result == "shutdown":
        send_notification("shutdown", "")
        subprocess.call(["shutdown", "0"])
    elif result == "reboot":
        send_notification("reboot", "")
        subprocess.call(["reboot"])
    elif result == "suspend":
        send_notification("suspend", "")
        subprocess.call(["systemctl", "suspend"])
    else:
        send_notification("no action", "")


def update_background():
    subprocess.run(
        [
            "python3",
            os.path.expanduser("~/dotfiles/qtile/set_lockscreen_bkg.py"),
            os.path.expanduser("~/mypaint/daily.ora"),
            os.path.expanduser("~/mypaint/daily_bkg.png"),
            os.path.expanduser("~/mypaint/daily_blurred.png"),
        ]
    )


def reconf_screens(data):
    autorandr_output = (
        subprocess.run("autorandr --change".split(), capture_output=True)
        .stdout.decode()
        .splitlines()
    )
    current = None
    for i in autorandr_output:
        if "(detected) (current)" in i:
            current = i.split(" (detected) (current)")[0]
            break

    if current is None:
        send_notification(
            "Could not detect known screen configuration", "Reconfigure Screens"
        )
        return

    send_notification(f"Now configuration {current}", "Reconfigure Screens")

    if data is not None:
        update_background()
        lazy.restart()


def change_floating_size(qtile, dw, dh, bottom_right=True):
    """Change size of current floating window."""
    current_window = qtile.current_window
    if bottom_right:
        qtile.current_window.cmd_resize_floating(dw, dh)
    else:
        qtile.current_window.cmd_move_floating(-dw, -dh)
        qtile.current_window.cmd_resize_floating(dw, dh)

    current_window.focus(warp=True)


def move_floating(qtile, dw, dh):
    """Change position of current floating window."""
    current_window = qtile.current_window
    qtile.current_window.cmd_move_floating(dw, dh)
    current_window.focus(warp=True)


def audio_out_selector(qtile):
    """Select audio output."""
    SEP_STR = "     |     "
    sink_list = subprocess_output(["pactl", "list", "sinks"])
    states = {
        number: (name, state)
        for number, state, name in re.findall(
            "Sink #(\d+)\n.*State: (.*)\n.*Name: (.*)\n", sink_list
        )
    }

    alias_dict = {
        "alsa_output.usb-Generic_USB_Audio-00.HiFi__hw_Audio__sink": "00_SPEAKER",
        "alsa_output.usb-Logitech_G733_Gaming_Headset-00.analog-stereo": "01_HEADSET",
    }

    inverted_aliases = {
        (alias_dict[name] if name in alias_dict else name): number
        for number, (name, state) in states.items()
    }

    aliased_states = {
        (alias_dict[name] if name in alias_dict else name): state
        for _, (name, state) in states.items()
    }

    out = rofi_selector(
        "\n".join(
            sorted(
                [
                    f"{device}{SEP_STR}{(state)}"
                    for device, state in aliased_states.items()
                ]
            )
        ),
        "SELECT AUDIO OUTPUT",
    )

    device = out.split(SEP_STR)[0]

    try:
        subprocess.call(["pactl", "set-default-sink", inverted_aliases[device]])
        send_notification(f"Selected {device}", "sound control", urgency="low")
    except KeyError:
        send_notification("Changed Nothing", "sound control", urgency="low")
        pass


def playerctl_metadata(format=None, player="playerctld"):
    """Return playerctl metadata for current player.

    Args:
        format (str): format specification for metadata
        player (str): player to use (default playerctld)

    Returns (str): requested metadata from playerctl
    """
    if format is not None:
        return subprocess_output(["playerctl", "-p", player, "metadata", "-f", format])
    else:
        return subprocess_output(["playerctl", "-p", player, "metadata"])


def spotify_mark(qtile):
    """Memorise the name and artist of the current spotify track."""
    artist_track = playerctl_metadata(
        format="'{{xesam:artist}}: {{xesam:title}}'", player="spotify"
    ).strip("'")
    with open("/home/hawo/spotify_marks.txt", "r") as file:
        tracklist = [line.strip("\n") for line in file.readlines()]

    if artist_track not in tracklist:
        with open("/home/hawo/spotify_marks.txt", "a") as file:
            file.write(artist_track)
            file.write("\n")
        send_notification("track name marked", "spotify-mark", urgency="low")

    else:
        send_notification("track already marked", "spotify-mark", urgency="low")


def current_track_notification(qtile):
    """Display a Notification with the current track."""
    TMP_LOCATION = "/home/hawo/spotify_notification_tmp/tmp_icon.jpg"
    player = subprocess_output(["playerctl", "-l"])
    title = playerctl_metadata(format="{{xesam:title}}")

    if not player.startswith("spotify"):
        send_notification(f"{title}", f"{player}")
        return

    # Get spotify album cover URL and set temporary file
    url = playerctl_metadata(format="{{mpris:artUrl}}")
    subprocess.call(["wget", f"{url}", "-O", TMP_LOCATION])

    artist = playerctl_metadata(format="{{xesam:artist}}")

    send_notification(f"{artist}", f"{title}", icon=TMP_LOCATION, urgency="low")


def float_to_front(qtile):
    """Bring all floating windows of the group to front."""
    window = qtile.current_window
    if window.floating:
        window.cmd_bring_to_front()


class CapsNumLockIndicator_Nice(base.ThreadPoolText):
    """A nicer Caps/Num Lock indicator."""

    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [("update_interval", 0.25, "Update Time in seconds.")]

    def __init__(self, **config):
        """Initialise CapsNumLockIndicator_Nice."""
        base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(CapsNumLockIndicator_Nice.defaults)

    def get_indicators(self):
        """Return a list with the current State."""
        try:
            output = self.call_process(["xset", "q"])
        except subprocess.CalledProcessError as err:
            output = err.output.decode()

        if output.startswith("Keyboard"):
            indicators = re.findall("(?:Caps|Num)\s+Lock:\s*(on|off)", output)
            return indicators

    def poll(self):
        """Poll content for the text box."""
        sym = self.get_indicators()
        out = " "

        if sym[0] == "on":  # Caps Lock
            out += "\uf55f"
        else:
            out += "\uf48b"

        if sym[1] == "on":  # Num Lock
            out += "\uf560"
        else:
            out += "\uf48b"

        return out + " "


def reduce_brightness(hex_color, factor):
    """Reduce brightness of a color."""
    if factor > 1.0:
        factor = 1.0
    red = f"{int(float(factor) * int(hex_color[1:3], 16)):#0{4}x}"[2:4]
    green = f"{int(float(factor) * int(hex_color[3:5], 16)):#0{4}x}"[2:4]
    blue = f"{int(float(factor) * int(hex_color[5:7], 16)):#0{4}x}"[2:4]
    return "#{}{}{}".format(red, green, blue)


def invert_color(hex_color):
    """Invert Hex color."""
    red = f"{255 - int(hex_color[1:3], 16):#0{4}x}"[2:4]
    green = f"{255 - int(hex_color[3:5], 16):#0{4}x}"[2:4]
    blue = f"{255 - int(hex_color[5:7], 16):#0{4}x}"[2:4]
    return "#{}{}{}".format(red, green, blue)


def show_cheatsheet(qtile):
    """Open Cheatsheet with all Keybindings using yad."""
    cheatsheet_fname = os.path.join(
        os.path.expanduser("~"), "dotfiles/qtile/keychords_mangled.txt"
    )

    catp = subprocess.Popen(["cat", cheatsheet_fname], stdout=subprocess.PIPE)
    out, _ = catp.communicate()
    p = subprocess.Popen(
        [
            "yad",
            "--list",
            "--close-on-unfocus",
            "--no-header",
            "--no-click",
            "--no-selection",
            "--center",
            "--width=3000",
            "--height=1688",
            "--title='KEY COMBINATIONS AND KEYS'",
            "--column=KEYS:text",
            "--column=KEYS (2):text",
            "--column=KEY CHORDS:text",
        ],
        stdin=subprocess.PIPE,
    )
    p.communicate(input=out, timeout=0.001)


gruvbox_colors = [
    "#282828",  # color0
    "#cc241d",  # color1
    "#98971a",  # color2
    "#d79921",  # color3
    "#458588",  # color4
    "#b16286",  # color5
    "#689d6a",  # color6
    "#a89984",  # color7
    "#928374",  # color8
    "#fb4934",  # color9
    "#b8bb26",  # color10
    "#fabd2f",  # color11
    "#83a598",  # color12
    "#d3869b",  # color13
    "#8ec07c",  # color14
    "#ebdbb2",  # color15
    "#ebdbb2",  # foreground
    "#1d2021",  # background
]

melange_colors = [
    "#2a2520",  # color0
    "#7d2a2f",  # color1
    "#78997a",  # color2
    "#e49b5d",  # color3
    "#485f84",  # color4
    "#b380b0",  # color5
    "#729893",  # color6
    "#8e733f",  # color7
    "#4d453e",  # color8
    "#c65333",  # color9
    "#99d59d",  # color10
    "#d7898c",  # color11
    "#697893",  # color12
    "#ce9bcb",  # color13
    "#86a3a3",  # color14
    "#ece1d7",  # color15
    "#f4f0ed",  # foreground
    "#352f2a",  # background
]

colors = melange_colors

d = display.Display()
s = d.screen()
r = s.root
res = r.xrandr_get_screen_resources()._data

n_monitors = 0
resolutions = []
diags = []
for output in res["outputs"]:
    mon = d.xrandr_get_output_info(output, res["config_timestamp"])._data
    if mon["num_preferred"] == 1:
        n_monitors += 1
        modes = sum(
            [[m for m in res["modes"] if m["id"] == mode] for mode in mon["modes"]], []
        )
        diag = max([math.sqrt(mode.width**2 + mode.height**2) for mode in modes])
        diags.append(diag)

diag = min(diags)

FLOAT_RS_INC = int(diag * 0.01)
FLOAT_MV_INC = int(diag * 0.01)

# keys
win = "mod4"
alt = "mod1"

terminal = "alacritty"

group_names = ["main", "alt", "visu", "www", "mail", "comms", "media", "background"]

group_syms = [
    "\uf015",  # House
    "\uf46d",  # Another House
    "\uf06e",  # Eye
    "\uf484",  # Globe
    "\uf6ef",  # Mail
    "\uf0e6",  # Speech Bubbles
    "\uf26c",  # Screen
    "\uf756",  # Folder
]

groups = [
    Group(group_names[0], label=group_syms[0]),
    Group(group_names[1], label=group_syms[1]),
    Group(
        group_names[2],
        label=group_syms[2],
        matches=[Match(wm_instance_class="paraview"), Match(wm_class="Zotero")],
    ),
    Group(
        group_names[3],
        label=group_syms[3],
        matches=[
            Match(wm_class=w) for w in ["firefox_firefox", "Opera", "Google Chrome"]
        ],
    ),
    Group(
        group_names[4],
        label=group_syms[4],
        matches=[
            Match(wm_class=["Mail", "Thunderbird"]),
            Match(wm_class=["Rocket.Chat"]),
        ],
    ),
    Group(
        group_names[5],
        label=group_syms[5],
        matches=[
            Match(wm_class=re.compile(".*telegram.*", flags=re.IGNORECASE)),
            Match(wm_class=re.compile(".*whatsapp.*", flags=re.IGNORECASE)),
            Match(wm_class=re.compile(".*signal.*", flags=re.IGNORECASE)),
        ],
    ),
    Group(
        group_names[6],
        label=group_syms[6],
        matches=[
            Match(wm_class=re.compile(".*spotify.*", flags=re.IGNORECASE)),
            Match(title=re.compile(".*spotify.*", flags=re.IGNORECASE)),
        ],
    ),
    Group(group_names[7], label=group_syms[7]),
]

keys = [
    # Standard window Actions
    EzKey("M-<Tab>", lazy.next_layout(), desc="Layout: Toggle between layouts"),
    EzKey("M-w", lazy.window.kill(), desc="Window: Kill focused."),
    EzKey(
        "M-<space>", lazy.window.toggle_fullscreen(), desc="Window: Toggle fullscreen."
    ),
    EzKey("A-<Tab>", lazy.layout.next(), desc="Window: Move window focus to other."),
    # Switch between windows
    EzKey("M-h", lazy.layout.left(), desc="Window: Focus left"),
    EzKey("M-l", lazy.layout.right(), desc="Window: Focus right"),
    EzKey("M-j", lazy.layout.down(), desc="Window: Focus down"),
    EzKey("M-k", lazy.layout.up(), desc="Window: Focus up"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    EzKey("M-S-h", lazy.layout.shuffle_left(), desc="left"),
    EzKey("M-S-l", lazy.layout.shuffle_right(), desc="right"),
    EzKey("M-S-j", lazy.layout.shuffle_down(), desc="down"),
    EzKey("M-S-k", lazy.layout.shuffle_up(), desc="up"),
    EzKey("M-n", lazy.next_layout(), desc="next layout"),
    EzKey("M-A-h", lazy.prev_screen(), desc="Window: Focus previous screen."),
    EzKey("M-A-l", lazy.next_screen(), desc="Window: Focus next screen."),
    EzKey("M-d", lazy.function(reconf_screens), desc="Reconfigure Screens"),
    EzKey("M-A-S-h", lazy.function(move_to_prev_screen), desc="prev screen"),
    EzKey("M-A-S-l", lazy.function(move_to_next_screen), desc="next screen"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed Unsplit = 1 window displayed,
    # like Max layout, but still with
    # multiple stack panes
    EzKey(
        "M-A-<Return>",
        lazy.layout.toggle_split(),
        desc="Layout: Toggle stack split.",
    ),
    # Window Resizing in Constrained Layout
    KeyChord(
        [win, "shift"],
        "r",
        [
            EzKey("h", lazy.layout.grow_left(), desc="Grow left"),
            EzKey("l", lazy.layout.grow_right(), desc="Grow right"),
            EzKey("j", lazy.layout.grow_down(), desc="Grow down"),
            EzKey("k", lazy.layout.grow_up(), desc="Grow up"),
            EzKey("n", lazy.layout.normalize(), desc="Reset sizes"),
            EzKey("i", lazy.layout.grow(), desc="Monad Grow"),
            EzKey("m", lazy.layout.shrink(), desc="Monad Shrink"),
            EzKey("x", lazy.window.kill(), desc="Kill focused"),
        ],
        name="RESIZE",
        mode=True,
    ),
    Key(
        [win, "shift"],
        "f",
        lazy.function(float_to_front),
        desc="Window: Bring currently focused floating window to front.",
    ),
    Key(
        [win], "f", lazy.window.toggle_floating(), desc="Window: Toggle floating status"
    ),
    # Qtile Management Actions
    EzKey("M-C-r", lazy.restart(), desc="System: Restart Qtile"),
    EzKey(
        "C-S-<Escape>",
        lazy.function(shutdown_reboot_menu),
        desc="System: Start Shutdown/Reboot Menu with Rofi",
    ),
    EzKey(
        "M-C-s",
        lazy.function(show_cheatsheet),
        desc="Launch: Qtile Key Map View",
    ),
    EzKey(
        "M-C-l",
        lazy.spawn(f"i3lock -e -i {LOCK_WALLPAPER} -t"),
        desc="System: Lock Session",
    ),
    EzKey(
        "A-<minus>",
        lazy.spawn("/home/hawo/scripts/circ_pen_selector.sh"),
        desc="Launch: Cycle Pen Script",
    ),
    # Launch Applications
    EzKey(
        "M-S-<Return>",
        lazy.spawn(f"{terminal} -e 'tmux'"),
        desc="Launch: tmux terminal",
    ),
    EzKey("M-<Return>", lazy.spawn(f"{terminal}"), desc=f"Launch: {terminal}"),
    EzKey(
        "M-C-n",
        lazy.spawn(
            f"mypaint --fullscreen '{os.path.expanduser('~/mypaint/daily.ora')}'"
        ),
        desc=f"Launch: daily notes",
    ),
    Key(
        [win],
        "r",
        lazy.spawn(
            "rofi -show-icons -modi run,drun,window,combi "
            "-combi-modi drun,window -show combi"
        ),
        desc="Launch: rofi application start",
    ),
    Key([win], "e", lazy.spawn("pcmanfm"), desc="Launch: pcmanfn"),
    Key(
        [win],
        "v",
        lazy.spawn(
            f"{terminal} -t 'openvpn_console' -e " "'/home/hawo/scripts/vpn_connect.sh'"
        ),
        desc="Connections: Start VPN",
    ),
    # Notifications
    Key(
        ["control", "shift"],
        "space",
        lazy.spawn("dunstctl close-all"),
        desc="Notifications: Close all Notifications",
    ),
    Key(
        ["control", "shift"],
        "h",
        lazy.spawn("dunstctl history-pop"),
        desc="Notifications: Show Notification History",
    ),
    Key(
        ["control", "shift"],
        "a",
        lazy.spawn("dunstctl action"),
        desc="Notifications: Dunstctl default action",
    ),
    # VPN SELECTOR
    Key(
        [win, "shift"],
        "v",
        lazy.spawn("/home/hawo/scripts/vpn_kill.sh"),
        desc="Connections: Kill openVPN",
    ),
    Key(
        [win, alt],
        "s",
        lazy.spawn(
            f"rofi -show-icons -ssh-command '{terminal}"
            '-c "ssh {host}"\' -modi ssh -show ssh'
        ),
        desc="Connections: SSH Menu",
    ),
    Key([win, "shift"], "s", lazy.spawn("flameshot gui"), desc="Launch: Screenshot"),
    # Specific window Actions
    Key(
        [win],
        "a",
        lazy.spawn("rofi -show-icons -modi window -show window"),
        desc="Window: Show all in rofi (allow to switch)",
    ),
    Key(
        ["control", alt],
        "m",
        lazy.function(move_to_group_selector),
        desc="Window: Move current to group using rofi",
    ),
    Key(
        [win],
        "g",
        lazy.function(group_switch_selector),
        desc="Group: Switch using rofi selector",
    ),
    # sound control
    Key(
        [alt],
        "F1",
        lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"),
        desc="Audio: Mute Audio Out",
    ),
    Key(
        [alt],
        "F2",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%"),
        desc="Audio: Decrease Volume",
    ),
    Key(
        [alt],
        "F3",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%"),
        desc="Audio: Increase Volume",
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -2%"),
        desc="Audio: Decrease Volume",
    ),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +2%"),
        desc="Audio: Increase Volume",
    ),
    Key(
        [],
        "XF86AudioPlay",
        lazy.spawn("playerctl -p playerctld play-pause"),
        desc="Audio: Play/Pause Media",
    ),
    Key(
        [],
        "XF86AudioNext",
        lazy.spawn("playerctl -p playerctld next"),
        desc="Audio: Next Track",
    ),
    Key(
        [],
        "XF86AudioPrev",
        lazy.spawn("playerctl -p playerctld previous"),
        desc="Audio: Previous Track",
    ),
    Key(
        [alt, "shift"],
        "o",
        lazy.function(audio_out_selector),
        desc="Audio: Select pulseaudio sink",
    ),
    # Clipboard Manager
    Key(
        ["control", alt],
        "c",
        lazy.spawn(
            "rofi -modi 'clipboard:greenclip print' "
            "-show clipboard -run-command '{cmd}'"
        ),
        desc="System: Show clipboard contents",
    ),
    Key(
        ["control", alt],
        "e",
        lazy.spawn("/home/hawo/dotfiles/qtile/emoji_select.sh --rofi"),
        desc="Launch: Emoji Selector using rofi",
    ),
    Key(
        [alt, "shift"],
        "s",
        lazy.function(scholar_search_cur_selection),
        desc="Launch: Search current selection in google scholar.",
    ),
    Key(
        [alt, "shift"],
        "f",
        lazy.function(open_selection_in_firefox),
        desc="Launch: Open current selection as URL in firefox.",
    ),
    Key(
        [win, alt],
        "t",
        lazy.function(spotify_mark),
        desc="Audio: Mark current spotify track.",
    ),
    Key(
        [win, "shift"],
        "t",
        lazy.function(current_track_notification),
        desc="Audio: Display notification with current track",
    ),
]

for n, grp in enumerate(groups):
    keys.extend(
        [
            # win + letter of group = switch to group
            Key(
                [win],
                str(n + 1),
                lazy.group[grp.name].toscreen(toggle=True),
                desc="Group: Switch to {}".format(group_names[n]),
            ),
            # win + shift + letter of group
            # = switch to & move focused window to group
            Key(
                [win, "shift"],
                str(n + 1),
                lazy.window.togroup(grp.name, switch_group=True),
                desc="Group: Switch to and move focused window {}".format(grp.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # win + shift + letter of group = move focused window to group
            # Key([win, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

MARGIN = 12
BORDER_WIDTH = 2

border_cfg = {
    "border_focus": colors[3],
    "border_normal": colors[4],
    "border_width": BORDER_WIDTH,
    "border_normal_stack": colors[2],
    "border_focus_stack": colors[10],
    "margin": MARGIN,
}

layouts = [
    layout.Columns(
        **border_cfg,
        border_on_single=True,
        grow_amount=2,
        insert_position=1,
        num_columns=2,
        fair=True,
    ),
    layout.MonadTall(
        **border_cfg,
        ratio=0.6,
    ),
    layout.MonadThreeCol(
        **border_cfg,
        ratio=0.6,
    ),
]

widget_defaults = dict(
    font="NotoSansM Nerd Font Mono",
    # font='sans',
    fontsize=int(diag * 0.007),
    padding=int(diag * 0.002),
)

extension_defaults = widget_defaults.copy()
bar_margin = int(diag * 0.002)
bar_height = int(diag * 0.012)


def spacer(fore, back, height, dir="l", padding=0):
    """Spacer in bar with color 'color'."""
    if dir == "l":
        return widget.TextBox(
            text=" \ue0b6",
            fontsize=height,
            padding=0,
            foreground=fore,
            background=back,
        )
    else:
        return widget.TextBox(
            text="\ue0b4 ",
            fontsize=height,
            padding=0,
            foreground=fore,
            background=back,
        )


def gen_widgets(this_c, screen):
    widgetlist = [
        spacer(this_c, None, bar_height, dir="l"),
        widget.Chord(
            foreground=colors[0],
            background=this_c,
            fmt="\uf085 {}  ",
        ),
        widget.GroupBox(
            spacing=bar_margin,
            borderwidth=int(diag * 0.0008),
            highlight_method="line",
            highlight_color=[this_c, this_c],
            background=this_c,
            foreground=colors[0],
            this_screen_border=colors[17],
            other_screen_border=colors[17],
            this_current_screen_border=colors[16],
            other_current_screen_border=colors[17],
            urgent_border=colors[5],
            urgent_text=colors[5],
            active=colors[16],
            inactive=colors[17],
            disable_drag=True,
            hide_unused=False,
        ),
        spacer(this_c, None, bar_height, dir="r"),
        spacer(colors[0], None, bar_height, dir="l"),
        widget.WindowName(
            foreground=this_c,
            background=colors[0],
            font="noto sans",
        ),
        spacer(colors[0], None, bar_height, dir="r"),
        spacer(colors[0], None, bar_height, dir="l"),
        widget.Memory(
            foreground=colors[6],
            background=colors[0],
            format="RAM: {MemUsed: .0f} MB  ",
        ),
        # spacer(this_c),
        widget.CPU(
            foreground=colors[11],
            background=colors[0],
            format="CPU @ {freq_current} GHz {load_percent:3.0f}%",
        ),
        widget.TextBox(foreground=colors[16], background=colors[0], text=" \ue20a "),
        widget.ThermalSensor(
            foreground=colors[6], background=colors[0], foreground_alert=colors[9]
        ),
        spacer(colors[0], None, bar_height, dir="r"),
        spacer(colors[0], None, bar_height, dir="l"),
        widget.Net(
            format="{down:6.2f} {down_suffix:2}",
            foreground=colors[6],
            background=colors[0],
        ),
        widget.TextBox(text=" \uf0ab | \uf0aa ", background=colors[0]),
        widget.Net(
            format="{up:<6.2f} {up_suffix:2}",
            foreground=colors[11],
            background=colors[0],
        ),
        spacer(colors[0], None, bar_height, dir="r"),
        spacer(this_c, None, bar_height, dir="l"),
        widget.PulseVolume(
            background=this_c,
            foreground=colors[0],
        ),
        CapsNumLockIndicator_Nice(background=this_c, foreground=colors[17]),
        widget.Clock(
            format=" %H:%M %a %d.%m.%Y",
            foreground=colors[17],
            background=this_c,
        ),
        widget.CurrentLayoutIcon(scale=0.8, background=this_c),
        spacer(this_c, None, bar_height, dir="r"),
    ]
    if screen == 0:
        widgetlist.insert(
            -6,
            widget.Systray(padding=7, icon_size=int(bar_height * 0.6), background=None),
        )

    return widgetlist


screens = [
    Screen(
        top=bar.Bar(
            gen_widgets(this_c, screen),
            bar_height,
            margin=[bar_margin, 0, 0, 0],
            background="#00000000",
            x11_drag_polling_rate=60,
        ),
    )
    for screen, this_c in enumerate([colors[3], colors[2], colors[4]])
]

# Drag floating layouts.
# Button 4 -> Scroll Up
# Button 5 -> Scroll Down
mouse = [
    Drag(
        [win],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [win],
        "Button3",
        lazy.window.set_size_floating(),
        start=lazy.window.get_size(),
    ),
    Drag(
        ["control"],
        "Button2",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Click([win], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class
        # and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="pavucontrol"),
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(title="Picture in Picture"),
        Match(title="Generate Fonts"),
        Match(title=re.compile("^.*settings((?!.*firefox).)*$", flags=re.IGNORECASE)),
        Match(
            title=re.compile("^.*preferences((?!.*firefox).)*$", flags=re.IGNORECASE)
        ),
        Match(title=re.compile("Polls"), wm_class=re.compile("zoom")),
        Match(title=re.compile("Chat"), wm_class=re.compile("zoom")),
        Match(title=re.compile(""), wm_class=re.compile("zoom")),
        Match(wm_class=re.compile("gnuplot_qt")),
        Match(wm_class=re.compile(".*arandr.*", flags=re.IGNORECASE)),
        Match(wm_class=re.compile("matplotlib")),
        Match(role=re.compile("Event.*Dialog", flags=re.IGNORECASE)),
        Match(title=re.compile(".*Open With.*", flags=re.IGNORECASE)),
        Match(title=re.compile(".*Import.*", flags=re.IGNORECASE)),
        Match(title=re.compile(".*Export.*", flags=re.IGNORECASE)),
        Match(title=re.compile(".*Confirm.*", flags=re.IGNORECASE)),
        Match(title=re.compile(".*gpick.*", flags=re.IGNORECASE)),
        Match(wm_class=re.compile(".*yad.*", flags=re.IGNORECASE)),
        Match(title=re.compile(".*clocks.*", flags=re.IGNORECASE)),
    ],
    border_width=BORDER_WIDTH,
)
auto_fullscreen = True
focus_on_window_activation = "smart"
# reconfigure_screens = True


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


@hook.subscribe.startup_once
def autostart():
    """Autostart functions."""
    subprocess.Popen("dunst")
    logger.warn("started dunst")
    reconf_screens(None)
    logger.warn("ran reconf_screens")

    subprocess.Popen("picom -b".split())
    logger.warn("started picom")
    update_background()

    subprocess.call(
        [os.path.expanduser("~/.config/qtile/autostart.sh"), WALLPAPER, LOCK_WALLPAPER]
    )
    logger.warn("called autostart")


# @hook.subscribe.client_managed
# def focus_new(window):
#     """Focus newly created windows."""
#     c = InteractiveCommandClient()
#     # window.focus(warp=True)
#     # next_group = window.cmd_info()["group"]
#     # c.group[next_group].to_screen()
#     for screen in c.screen:
#         setd_notification(f"{screen.cmd_info()}", "screen_wins")
