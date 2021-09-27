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

import os
import re
import subprocess
from typing import List  # noqa: F401

from hue_controller.hue_classes import HueBridge
# from libqtile.utils import guess_terminal
from libqtile import bar, hook, layout, widget
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy
from libqtile.widget import base
from libqtile.command.client import InteractiveCommandClient

BRIDGE = HueBridge("hawos_bridge")
LOCK_WALLPAPER = "/usr/share/wallpapers/julia_set_multicolor_lock.png"


def send_notification(message, app, urgency="normal", icon=None):
    """Send a notification using dunstify."""
    if icon is not None:
        subprocess.call(
            ["dunstify", "-a", f"{app}", f"{message}",
             "-u", urgency, "-i", icon])
    else:
        subprocess.call(
            ["dunstify", "-a", f"{app}", f"{message}", "-u", urgency])


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
        subprocess.Popen(args, stdout=subprocess.PIPE)
        .communicate()[0]
        .decode("ascii")
        .strip("\n")
    )


def toggle_light_group(qtile, group, display_name):
    """Toggle hue lights in a hue light group."""
    lockfile_path = f"{HueBridge.HUE_FILE_LOCATION}/hawos_bridge.lck"
    if not os.path.isfile(lockfile_path):
        with open(lockfile_path, "w+") as lck_file:
            lck_file.write("locked")
        BRIDGE.toggle_group(group)
        os.remove(lockfile_path)
        light = BRIDGE.groups[group][0]
        status = BRIDGE.get_light_states()[light]
        if status["on"]:
            brightness = int(status["brightness"] / 255 * 100)
        else:
            brightness = 0
        send_progress(display_name, "Lighting", brightness)


def toggle_light(qtile, lights, display_name):
    """Toggle hue lights in a hue light group."""
    lockfile_path = f"{HueBridge.HUE_FILE_LOCATION}/hawos_bridge.lck"
    if not os.path.isfile(lockfile_path):
        with open(lockfile_path, "w+") as lck_file:
            lck_file.write("locked")
        for light in lights:
            if light not in BRIDGE.lights:
                send_notification(f"Invalid Light Name: {light}",
                                  "light control", "HIGH")
                return

        BRIDGE.toggle_lights(lights)
        os.remove(lockfile_path)
        send_notification(f"Toggled {display_name}",
                          "light control", "low")


def inc_light_brightness(qtile, group, display_name, inc):
    """Increment light brightness in a hue light group."""
    lockfile_path = f"{HueBridge.HUE_FILE_LOCATION}/hawos_bridge.lck"
    if not os.path.isfile(lockfile_path):
        with open(lockfile_path, "w+") as lck_file:
            lck_file.write("locked")

        light = BRIDGE.groups[group][0]
        status = BRIDGE.get_light_states()[light]
        BRIDGE.increment_group(group, inc)
        os.remove(lockfile_path)
        light = BRIDGE.groups[group][0]
        status = BRIDGE.get_light_states()[light]
        if status["on"]:
            brightness = int(status["brightness"] / 255 * 100)
        else:
            brightness = 0
        send_progress(display_name, "Lighting", brightness)


def move_to_next_screen(qtile):
    """Move a window to the next screen."""
    active_win = qtile.current_window
    next_screen = (qtile.current_screen.index + 1) % len(qtile.screens)
    active_win.toscreen(next_screen)
    qtile.focus_screen(next_screen, warp=True)
    active_win.focus(warp=True)


def rofi_selector(option_string, prompt):
    """Create a rofi selector for options in option_str."""
    child_process = subprocess.Popen(
        ["rofi", "-dmenu", "-p", prompt, "-i"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    child_process.stdin.write(option_string.encode("ascii"))
    return child_process.communicate()[0].decode("ascii").strip("\n")


def move_to_group_selector(qtile):
    """Move window to a group with a rofi selector."""
    active_win = qtile.current_window
    str_groups = "\n".join(
        [
            f"{index:4} -> {g.label}"
            for index, g in enumerate(qtile.groups, start=1)
        ]
    )
    target = re.split(r" -> ", rofi_selector(str_groups, "chose group"))[-1]
    active_win.cmd_togroup(target)


def group_switch_selector(qtile):
    """Switch focus to a group with a selector."""
    str_groups = "\n".join(
        [
            f"{index:4} -> {g.label}"
            for index, g in enumerate(qtile.groups, start=1)
        ]
    )
    target = re.split(r" -> ", rofi_selector(str_groups, "chose group"))[0]
    qtile.groups[int(target) - 1].cmd_toscreen()


def shutdown_reboot_menu(qtile):
    """Open a rofi menu for shutting down or rebooting."""
    option_str = "\n".join(["shutdown", "reboot", "nothing"])
    result = rofi_selector(option_str, "Shutdown Menu")
    if result == "shutdown":
        send_notification("shutdown", "")
        subprocess.call(["shutdown", "0"])
    elif result == "reboot":
        send_notification("reboot", "")
        subprocess.call(["reboot"])
    else:
        send_notification("no action", "")


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
    states = {number: (name, state) for number, state, name
              in re.findall("Sink #(\d+)\n.*State: (.*)\n.*Name: (.*)\n",
                            sink_list)}

    alias_dict = {
        "alsa_output.usb-C-Media_Electronics_Inc._USB_PnP_Sound_Device-00.analog-stereo-output": "HEADSET",
        "alsa_output.pci-0000_00_1b.0.analog-stereo": "SPEAKER",
        "alsa_output.pci-0000_01_00.1.hdmi-stereo-extra1": "SCREEN",
    }

    inverted_aliases = {
        (alias_dict[name] if name in alias_dict else name): number
        for number, (name, state) in states.items()
    }

    aliased_states = {(alias_dict[name] if name in alias_dict else name): state
                      for _, (name, state) in states.items()}

    out = rofi_selector("\n".join([f"{device}{SEP_STR}{(state)}"
                        for device, state in aliased_states.items()]),
                        "SELECT AUDIO OUTPUT")

    device = out.split(SEP_STR)[0]

    try:
        subprocess.call(["pactl", "set-default-sink",
                         inverted_aliases[device]])
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
        return subprocess_output(["playerctl", "-p", player,
                                  "metadata", "-f", format])
    else:
        return subprocess_output(["playerctl", "-p", player, "metadata"])


def spotify_mark(qtile):
    """Memorise the name and artist of the current spotify track."""
    artist_track = playerctl_metadata(
        format="'{{xesam:artist}}: {{xesam:title}}'",
        player="spotify").strip("'")
    with open("/home/hawo/spotify_marks.txt", "r") as file:
        tracklist = [line.strip("\n") for line in file.readlines()]

    if artist_track not in tracklist:
        with open("/home/hawo/spotify_marks.txt", "a") as file:
            file.write(artist_track)
            file.write("\n")
        send_notification("track name marked", "spotify-mark", urgency="low")

    else:
        send_notification(
            "track already marked", "spotify-mark", urgency="low"
        )


def current_track_notification(qtile):
    """Display a Notification with the current track."""
    TMP_LOCATION = "/home/hawo/spotify_notification_tmp/tmp_icon.jpg"
    player = subprocess_output(["playerctl", "-l"])
    title = playerctl_metadata(format="{{xesam:title}}")

    if not player.startswith("spotify"):
        send_notification(f"{title}", f"{player}")
        return

    # Process spotify album cover URL
    url = playerctl_metadata(format="{{mpris:artUrl}}")
    url = "https://i.scdn.co" + url[24:]

    subprocess.call(
        ["wget", f"{url}", "-O", TMP_LOCATION])
    artist = playerctl_metadata(format="{{xesam:artist}}")

    send_notification(f"{artist}", f"{title}",
                      icon=TMP_LOCATION,
                      urgency="low")


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

        if sym[0] == "on":
            out += "\u21EA"
        else:
            out += "_"

        if sym[1] == "on":
            out += "\u21ED"
        else:
            out += "_"

        return out + " "


def reduce_brightness(hex_color, factor):
    """Reduce brightness of a color."""
    if factor > 1.0:
        factor = 1.0
    red = f"{int(float(factor) * int(hex_color[1:3], 16)):#0{4}x}"[2:4]
    green = f"{int(float(factor) * int(hex_color[3:5], 16)):#0{4}x}"[2:4]
    blue = f"{int(float(factor) * int(hex_color[5:7], 16)):#0{4}x}"[2:4]
    return "#{}{}{}".format(red, green, blue)


colors = [
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

# constants
FLOAT_RS_INC = 20
FLOAT_MV_INC = 20

# keys
win = "mod4"
alt = "mod1"

terminal = "alacritty"

groups = [
    Group("main"),
    Group("alt"),
    Group("visu", matches=Match(wm_instance_class="paraview")),
    Group("www", matches=[Match(wm_class="firefox"), Match(wm_class="Opera")]),
    Group(
        "mail",
        matches=[
            Match(wm_class=["Mail", "Thunderbird"]),
            Match(wm_class=["Rocket.Chat"]),
        ],
    ),
    Group(
        "comms",
        matches=[
            Match(wm_class=re.compile(".*telegram.*", flags=re.IGNORECASE)),
            Match(wm_class=re.compile(".*whatsapp.*", flags=re.IGNORECASE)),
            Match(wm_class=re.compile(".*signal.*", flags=re.IGNORECASE)),
        ],
    ),
    Group(
        "media",
        matches=[
            Match(wm_class=re.compile(".*spotify.*", flags=re.IGNORECASE)),
            Match(title=re.compile(".*spotify.*", flags=re.IGNORECASE)),
        ],
    ),
    Group("background"),
]

keys = [
    # Standard window Actions
    Key([win], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([alt], "F4", lazy.window.kill(), desc="Kill focused window"),
    Key([win], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [win],
        "space",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen mode for current window.",
    ),
    Key(
        [alt],
        "Tab",
        lazy.layout.next(),
        desc="Move window focus to other window",
    ),
    # Switch between windows
    Key([win], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([win], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([win], "j", lazy.layout.down(), desc="Move focus down"),
    Key([win], "k", lazy.layout.up(), desc="Move focus up"),
    Key([win], "n", lazy.next_screen(), desc="Move focus to next screen"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [win, "shift"],
        "h",
        lazy.layout.shuffle_left(),
        desc="Move window to the left",
    ),
    Key(
        [win, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key(
        [win, "shift"],
        "j",
        lazy.layout.shuffle_down(),
        desc="Move window down",
    ),
    Key([win, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key(
        [win, "shift"],
        "n",
        lazy.function(move_to_next_screen),
        desc="Move window to other Screen",
    ),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed Unsplit = 1 window displayed,
    # like Max layout, but still with
    # multiple stack panes
    Key(
        [win, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    # Window Resizing in Constrained Layout
    KeyChord(
        [win, "shift"],
        "r",
        [
            Key([], "h", lazy.layout.grow_left(), desc="Grow window left"),
            Key([], "l", lazy.layout.grow_right(), desc="Grow window right"),
            Key([], "j", lazy.layout.grow_down(), desc="Grow window down"),
            Key([], "k", lazy.layout.grow_up(), desc="Grow window up"),
            Key([], "n", lazy.layout.normalize(), desc="Reset window sizes"),
            Key([], "x", lazy.window.kill(), desc="Kill focused window"),
        ],
        mode="RESIZE",
    ),
    Key(
        [win, "shift"],
        "f",
        lazy.function(float_to_front),
        desc="Bring currently focused floating window to front.",
    ),
    # Floating Window Resizing
    KeyChord(
        [win, "shift", alt],
        "r",
        [
            Key(
                [],
                "h",
                lazy.function(change_floating_size, -FLOAT_RS_INC, 0),
                desc="Decrease floating window width",
            ),
            Key(
                [],
                "l",
                lazy.function(change_floating_size, FLOAT_RS_INC, 0),
                desc="Increase floating window width",
            ),
            Key(
                [],
                "j",
                lazy.function(change_floating_size, 0, FLOAT_RS_INC),
                desc="Increase floating window height",
            ),
            Key(
                [],
                "k",
                lazy.function(change_floating_size, 0, -FLOAT_RS_INC),
                desc="Decrease floating window height",
            ),
            Key(
                ["shift"],
                "h",
                lazy.function(change_floating_size, -4 * FLOAT_RS_INC, 0),
                desc="Decrease floating window width",
            ),
            Key(
                ["shift"],
                "l",
                lazy.function(change_floating_size, 4 * FLOAT_RS_INC, 0),
                desc="Increase floating window width",
            ),
            Key(
                ["shift"],
                "j",
                lazy.function(change_floating_size, 0, 4 * FLOAT_RS_INC),
                desc="Increase floating window height",
            ),
            Key(
                ["shift"],
                "k",
                lazy.function(change_floating_size, 0, -4 * FLOAT_RS_INC),
                desc="Decrease floating window height",
            ),
            Key([], "x", lazy.window.kill(), desc="Kill focused window"),
        ],
        mode="FLOAT RS",
    ),
    # Floating Window Moving
    KeyChord(
        [win, "shift", alt],
        "m",
        [
            Key(
                [],
                "h",
                lazy.function(move_floating, -FLOAT_MV_INC, 0),
                desc="Decrease floating window width",
            ),
            Key(
                [],
                "l",
                lazy.function(move_floating, FLOAT_MV_INC, 0),
                desc="Increase floating window width",
            ),
            Key(
                [],
                "j",
                lazy.function(move_floating, 0, FLOAT_MV_INC),
                desc="Increase floating window height",
            ),
            Key(
                [],
                "k",
                lazy.function(move_floating, 0, -FLOAT_MV_INC),
                desc="Decrease floating window height",
            ),
            Key(
                ["shift"],
                "h",
                lazy.function(move_floating, -4 * FLOAT_MV_INC, 0),
                desc="Decrease floating window width",
            ),
            Key(
                ["shift"],
                "l",
                lazy.function(move_floating, 4 * FLOAT_MV_INC, 0),
                desc="Increase floating window width",
            ),
            Key(
                ["shift"],
                "j",
                lazy.function(move_floating, 0, 4 * FLOAT_MV_INC),
                desc="Increase floating window height",
            ),
            Key(
                ["shift"],
                "k",
                lazy.function(move_floating, 0, -4 * FLOAT_MV_INC),
                desc="Decrease floating window height",
            ),
            Key([], "x", lazy.window.kill(), desc="Kill focused window"),
        ],
        mode="FLOAT MV",
    ),
    Key([win], "f", lazy.window.toggle_floating()),
    # Qtile Management Actions
    Key([win, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key(
        ["control", "shift"],
        "Escape",
        lazy.function(shutdown_reboot_menu),
        desc="Start Shutdown/Reboot Menu with Rofi",
    ),
    Key(
        [win, "control"],
        "s",
        lazy.spawn("feh ~/Pictures/qtile_layout/"),
        desc="View Qtile Key Map",
    ),
    Key(
        ["control", win],
        "l",
        lazy.spawn(f"i3lock -e -i {LOCK_WALLPAPER}"),
        desc="Lock Session",
    ),
    # Launch Applications
    Key([win], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key(
        [win],
        "r",
        lazy.spawn(
            "rofi -show-icons -modi run,drun,window,combi "
            "-combi-modi drun,window -show combi"
        ),
        desc="launch rofi",
    ),
    Key([win], "e", lazy.spawn("pcmanfm"), desc="Open File Manager"),
    Key(
        [win],
        "v",
        lazy.spawn(
            f"{terminal} -t 'openvpn_console' -e "
            "'/home/hawo/scripts/vpn_connect.sh'"
        ),
        desc="Start VPN connection",
    ),
    # VPN SELECTOR
    Key(
        [win, "shift"],
        "v",
        lazy.spawn("/home/hawo/scripts/vpn_kill.sh"),
        desc="kill openvpn",
    ),
    Key(
        [win, alt],
        "s",
        lazy.spawn(
            f"rofi -show-icons -ssh-command '{terminal}"
            ' -e bash -c "ssh {host}"\' -modi ssh -show ssh'
        ),
        desc="SSH Menu",
    ),
    Key([win, "shift"], "s", lazy.spawn("flameshot gui"), desc="Screenshot"),
    # Specific window Actions
    Key(
        [win],
        "a",
        lazy.spawn("rofi -show-icons -modi window -show window"),
        desc="Show all windows in rofi (allow to switch)",
    ),
    Key(
        ["control", alt],
        "m",
        lazy.function(move_to_group_selector),
        desc="Move current window to group using a rofi selector",
    ),
    Key(
        [win],
        "g",
        lazy.function(group_switch_selector),
        desc="Switch to group using a rofi selector",
    ),
    # sound control
    Key(
        [alt],
        "F1",
        lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"),
        desc="Mute Audio Out",
    ),
    Key(
        [alt],
        "F2",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%"),
        desc="Decrease Volume",
    ),
    Key(
        [alt],
        "F3",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%"),
        desc="Increase Volume",
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -2%"),
        desc="Decrease Volume",
    ),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +2%"),
        desc="Increase Volume",
    ),
    Key(
        [],
        "XF86AudioPlay",
        lazy.spawn("playerctl -p playerctld play-pause"),
        desc="Play/Pause Media",
    ),
    Key(
        [],
        "XF86AudioNext",
        lazy.spawn("playerctl -p playerctld next"),
        desc="Next Track",
    ),
    Key(
        [],
        "XF86AudioPrev",
        lazy.spawn("playerctl -p playerctld previous"),
        desc="Previous Track",
    ),
    Key(
        [alt, "shift"],
        "o",
        lazy.function(audio_out_selector),
        desc="Select pulseaudio sink",
    ),
    # Clipboard Manager
    Key(
        ["control", alt],
        "c",
        lazy.spawn(
            "rofi -modi 'clipboard:greenclip print' "
            "-show clipboard -run-command '{cmd}'"
        ),
        desc="Show clipboard contents",
    ),
    Key(
        ["control", alt],
        "e",
        lazy.spawn("/home/hawo/dotfiles/qtile/emoji_select.sh --rofi"),
        desc="Emoji Selector using rofi",
    ),

    Key(
        ["control", alt],
        "t",
        lazy.spawn(f"{terminal} -t translate "
                   "-e '/home/hawo/scripts/translate.sh'"),
        desc="Open translation terminal Interface."
        ),

    KeyChord(
        [win, alt],
        "l",
        [
            Key(
                [],
                "t",
                lazy.function(
                    toggle_light_group, "hawos_zimmer", "Hawos Zimmer"
                ),
                desc="Toggle Hawos Zimmer",
            ),
            Key(
                [],
                "j",
                lazy.function(
                    inc_light_brightness, "hawos_zimmer", "Hawos Zimmer", 10
                ),
                desc="Increment Lights by 10% Brightness",
            ),
            Key(
                [],
                "k",
                lazy.function(
                    inc_light_brightness, "hawos_zimmer", "Hawos Zimmer", -10
                ),
                desc="Decrement Lights by 10% Brightness",
            ),
            Key(
                ["shift"],
                "k",
                lazy.function(
                    toggle_light, ["Kueche", "Kueche2"], "Küche"
                ),
                desc="Toggle Kitchen Lights",
            ),
            Key(
                ["shift"],
                "f",
                lazy.function(
                    toggle_light, ["Flur"], "Flur"
                ),
                desc="Toggle Hallway Lights",
            ),
            Key(
                ["shift"],
                "b",
                lazy.function(
                    toggle_light, ["Bad"], "Bad"
                ),
                desc="Toggle Bathroom Lights",
            ),
        ],
        mode="LIGHT CONTROL",
    ),
    Key([win, alt], "t", lazy.function(spotify_mark)),
    Key([win, "shift"], "t", lazy.function(current_track_notification)),
]

for n, i in enumerate(groups):
    keys.extend(
        [
            # win + letter of group = switch to group
            Key(
                [win],
                str(n + 1),
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # win + shift + letter of group
            # = switch to & move focused window to group
            Key(
                [win, "shift"],
                str(n + 1),
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(
                    i.name
                ),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # win + shift + letter of group = move focused window to group
            # Key([win, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )
MARGIN = 12
BORDER_WIDTH = 4
FOCUS_BORDER = colors[15]
NORMAL_BORDER = colors[4]

layouts = [
    layout.Columns(
        border_focus=FOCUS_BORDER,
        border_normal=NORMAL_BORDER,
        border_width=BORDER_WIDTH,
        border_on_single=True,
        grow_amount=2,
        insert_position=1,
        num_columns=3,
        fair=True,
        margin=MARGIN,
    ),
    layout.Max(
        border_focus=FOCUS_BORDER,
        border_normal=NORMAL_BORDER,
        border_width=BORDER_WIDTH,
        grow_amount=2,
        margin=MARGIN,
        insert_position=1,
    ),
    layout.Bsp(
        border_focus=FOCUS_BORDER,
        border_normal=NORMAL_BORDER,
        border_width=BORDER_WIDTH,
        grow_amount=2,
        margin=MARGIN,
        insert_position=1,
    ),
]

widget_defaults = dict(
    font="NotoSansMono Nerd Font Regular",
    # font='sans',
    fontsize=24,
    padding=4,
)
extension_defaults = widget_defaults.copy()


def spacer(color):
    """Spacer in bar with color 'color'."""
    return widget.Sep(
        size_percent=80, padding=4, linewidth=2, foreground=color
    )


screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Chord(
                    foreground=colors[11],
                    background=reduce_brightness(colors[4], 0.8),
                ),
                # widget.CurrentLayout(foreground=colors[16]),
                widget.GroupBox(
                    highlight_method="block",
                    borderwidth=0,
                    padding=7,
                    # fmt="<span weight='bold>{}</span>",
                    block_highlight_text_color=colors[17],
                    this_current_screen_border=this_c,
                    this_screen_border=this_c,
                    other_current_screen_border=other_c,
                    other_screen_border=other_c,
                    urgent_border=colors[16],
                    urgent_text=colors[17],
                    disable_drag=True,
                    inactive=this_c,
                    active=colors[5],
                    hide_unused=False,
                ),
                spacer(this_c),
                widget.WindowCount(show_zero=True),
                spacer(this_c),
                widget.WindowName(foreground=colors[16]),
                # widget.CheckUpdates(display_format=u'\U0001F504 {updates}'),
                spacer(this_c),
                widget.Memory(
                    foreground=colors[6], format="RAM: {MemUsed: .0f} MB"
                ),
                spacer(this_c),
                widget.CPU(
                    foreground=colors[3],
                    format="CPU @ {freq_current} GHz {load_percent:3.0f}% ->",
                ),
                widget.ThermalSensor(
                    foreground=colors[10], foreground_alert=colors[9]
                ),
                spacer(this_c),
                widget.Net(
                    format="{down}",
                    foreground=colors[6],
                ),
                widget.TextBox(text="\u21D3 | \u21D1"),
                widget.Net(format="{up}", foreground=colors[3]),
                spacer(this_c),
                widget.Volume(),
                # widget.Open_Weather(cityid="Karlsruhe",
                #                     app_key="552454590f5ac95df45d0d8b5b92bb64"),
                CapsNumLockIndicator_Nice(
                    background=this_c, foreground=colors[17]
                ),
                widget.Systray(padding=7, background=this_c),
                widget.Clock(
                    format=" %H:%M %a %d.%m.%Y",
                    foreground=colors[17],
                    background=this_c,
                ),
                widget.CurrentLayoutIcon(scale=0.8, background=this_c),
            ],
            40,
            margin=[0, 0, 0, 0],
            background=reduce_brightness(colors[17], 0.8),
        ),
    )
    for this_c, other_c in [(colors[3], colors[14]), (colors[14], colors[3])]
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
follow_mouse_focus = True
bring_front_click = False
cursor_warp = True
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class
        # and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(title=re.compile(".*hourglass.*")),  # Hourglass timer
        Match(title="Picture in Picture"),
        Match(title="Generate Fonts"),
        Match(title=re.compile("Settings"), wm_class=re.compile("zoom")),
        Match(title=re.compile("Polls"), wm_class=re.compile("zoom")),
        Match(title=re.compile("Chat"), wm_class=re.compile("zoom")),
        Match(title=re.compile(""), wm_class=re.compile("zoom")),
        Match(wm_class=re.compile("gnuplot_qt")),
        Match(wm_class=re.compile(".*arandr.*", flags=re.IGNORECASE)),
        Match(wm_class=re.compile("matplotlib")),
        Match(title=re.compile(".*Open With.*", flags=re.IGNORECASE)),
        Match(title=re.compile(".*Import.*", flags=re.IGNORECASE)),
        Match(title=re.compile(".*Export.*", flags=re.IGNORECASE)),
        Match(title=re.compile(".*Confirm.*", flags=re.IGNORECASE)),
    ],
    border_focus=colors[5],
)
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


@hook.subscribe.startup_complete
def autostart():
    """Autostart functions."""
    home = os.path.expanduser("~")
    subprocess.call(home + "/.config/qtile/autostart.sh")


# @hook.subscribe.client_managed
# def focus_new(window):
#     """Focus newly created windows."""
#     c = InteractiveCommandClient()
#     # window.focus(warp=True)
#     # next_group = window.cmd_info()["group"]
#     # c.group[next_group].to_screen()
#     for screen in c.screen:
#         send_notification(f"{ssscreen.cmd_info()}", "screen_wins")
