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

from hue_controller.hue_classes import HueBridge

from typing import List  # noqa: F401

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import hook
from libqtile.widget import base


def send_notification(message, app):
    subprocess.call(["notify-send", "-a", f"{app}", f"{message}"])

def toggle_lights(qtile):
    # bridge = HueBridge("hawos_bridge")
    # lockfile_path = f"{HueBridge.HUE_FILE_LOCATION}/hawos_bridge.lck"
    # if not os.path.isfile(lockfile_path):
    #     with open(lockfile_path, "w+") as lck_file:
    #         lck_file.write("locked")
    #     bridge.toggle_group("hawos_zimmer")
    #     os.remove(lockfile_path)

    send_notification("toggled lights", "")


def move_to_next_screen(qtile):
    active_win = qtile.current_window
    next_screen = (qtile.current_screen.index + 1) % len(qtile.screens)
    active_win.toscreen(next_screen)
    qtile.focus_screen(next_screen)
    active_win.focus(warp=True)


def rofi_selector(option_string, prompt):
    child_process = subprocess.Popen(['rofi', '-dmenu', '-p', prompt, "-i"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    child_process.stdin.write(option_string.encode('ascii'))
    return child_process.communicate()[0].decode('ascii').strip("\n")


def move_to_group_selector(qtile):
    active_win = qtile.current_window
    str_groups = '\n'.join([f"{index:4} -> {g.label}" for index, g in enumerate(qtile.groups, start=1)])
    target = re.split(r" -> ", rofi_selector(str_groups, "chose group"))[-1]
    active_win.cmd_togroup(target)


def group_switch_selector(qtile):
    str_groups = '\n'.join([f"{index:4} -> {g.label}" for index, g in enumerate(qtile.groups, start=1)])
    target = re.split(r" -> ", rofi_selector(str_groups, "chose group"))[0]
    qtile.groups[int(target) - 1].cmd_toscreen()


def shutdown_reboot_menu(qtile):
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


def change_floating_size(qtile, dw, dh):
    qtile.current_window.cmd_resize_floating(dw, dh)


def move_floating(qtile, dw, dh):
    qtile.current_window.cmd_move_floating(dw, dh)


def audio_out_selector(qtile):
    result = rofi_selector("HEADSET\nSPEAKER", "Audio Sink")
    if result == "HEADSET":
        subprocess.call(["pactl", "set-default-sink", "2"])
        send_notification("HEADSET ACTIVATED", "sound control")
    elif result == "SPEAKER":
        subprocess.call(["pactl", "set-default-sink", "1"])
        send_notification("SPEAKER ACTIVATED", "sound control")


class CapsNumLockIndicator_Nice(base.ThreadPoolText):
    """A nicer Caps/Num Lock indicator."""

    orientations = base.ORIENTATION_HORIZONTAL
    defaults=[('update_interval', 0.25, 'Update Time in seconds.')]


    def __init__(self, **config):
        base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(CapsNumLockIndicator_Nice.defaults)


    def get_indicators(self):
        """Return a list with the current State"""
        try: 
            output = self.call_process(['xset', 'q'])
        except subprocess.CalledProcessError as err:
            output = err.output.decode()

        if output.startswith("Keyboard"):
            indicators = re.findall("(?:Caps|Num)\s+Lock:\s*(on|off)", output)
            return indicators 


    def poll(self):
        """Poll content for the text box."""
        sym = self.get_indicators()
        out = ' '

        if sym[0] == 'on':
            out += u"\u21EA"
        else: 
            out += '_'

        if sym[1] == 'on':
            out += u"\u21ED"
        else:
            out += '_'

        return out + " "


# colors
def reduce_brightness(hex_color, factor):
    if factor > 1.0:
        factor = 1.0
    red   = f"{int(float(factor) * int(hex_color[1:3], 16)):#0{4}x}"[2:4]
    green = f"{int(float(factor) * int(hex_color[3:5], 16)):#0{4}x}"[2:4]
    blue  = f"{int(float(factor) * int(hex_color[5:7], 16)):#0{4}x}"[2:4]
    return "#{}{}{}".format(red,green,blue)


clr_foreground = "#ebdbb2"
clr_background = "#282828"
clr_color0 = "#282828"
clr_color1 = "#cc241d"
clr_color2 = "#98971a"
clr_color3 = "#d79921"
clr_color4 = "#458588"
clr_color5 = "#b16286"
clr_color6 = "#689d6a"
clr_color7 = "#a89984"
clr_color8 = "#928374"
clr_color9 = "#fb4934"
clr_color10 = "#b8bb26"
clr_color11 = "#fabd2f"
clr_color12 = "#83a598"
clr_color13 = "#d3869b"
clr_color14 = "#8ec07c"
clr_color15 = "#ebdbb2"

# constants
FLOAT_RS_INC = 20
FLOAT_MV_INC = 20 

# keys
win = "mod4"
alt = "mod1"

terminal = "termite"

keys = [
    # Standard window Actions
    Key([win], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([alt], "F4", lazy.window.kill(), desc="Kill focused window"),
    Key([win], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([win], "space", lazy.layout.next(),
        desc="Move window focus to other window"),
    Key([alt], "Tab", lazy.layout.next(),
        desc="Move window focus to other window"),
# Switch between windows
    Key([win], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([win], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([win], "j", lazy.layout.down(), desc="Move focus down"),
    Key([win], "k", lazy.layout.up(), desc="Move focus up"),
    Key([win], "n", lazy.next_screen(), desc="Move focus to next screen"),


    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    KeyChord([win, "shift"], 'm', [
        Key([], "h", lazy.layout.shuffle_left(),
            desc="Move window to the left"),
        Key([], "l", lazy.layout.shuffle_right(),
            desc="Move window to the right"),
        Key([], "j", lazy.layout.shuffle_down(),
            desc="Move window down"),
        Key([], "k", lazy.layout.shuffle_up(), desc="Move window up"),
        Key([], "x", lazy.window.kill(), desc="Kill focused window"),
    ], 
    mode="MOVE"),

    Key([win, 'shift'], 'n', lazy.function(move_to_next_screen), desc="Move window to other Screen"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([win, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),

    # Window Resizing in Constrained Layout
    KeyChord([win, "shift"], "r", [
                Key([], "h", lazy.layout.grow_left(), desc="Grow window left"),
                Key([], "l", lazy.layout.grow_right(), desc="Grow window right"),
                Key([], "j", lazy.layout.grow_down(), desc="Grow window down"),
                Key([], "k", lazy.layout.grow_up(), desc="Grow window up"),
                Key([], "n", lazy.layout.normalize(), desc="Reset window sizes"),
                Key([], "x", lazy.window.kill(), desc="Kill focused window"),
            ],
            mode="RESIZE"),
            # mode=u"\U0001F589"),
    
    # Floating Window Resizing
    KeyChord([win, "shift", alt], "r", [
            Key([], "h", lazy.function(change_floating_size, -FLOAT_RS_INC, 0), desc="Decrease floating window width"),
            Key([], "l", lazy.function(change_floating_size, FLOAT_RS_INC, 0), desc="Increase floating window width"),
            Key([], "j", lazy.function(change_floating_size, 0, FLOAT_RS_INC), desc="Increase floating window height"),
            Key([], "k", lazy.function(change_floating_size, 0, -FLOAT_RS_INC), desc="Decrease floating window height"),
            Key(["shift"], "h", lazy.function(change_floating_size, -4 * FLOAT_RS_INC, 0), desc="Decrease floating window width"),
            Key(["shift"], "l", lazy.function(change_floating_size, 4 * FLOAT_RS_INC, 0), desc="Increase floating window width"),
            Key(["shift"], "j", lazy.function(change_floating_size, 0, 4 * FLOAT_RS_INC), desc="Increase floating window height"),
            Key(["shift"], "k", lazy.function(change_floating_size, 0, -4 * FLOAT_RS_INC), desc="Decrease floating window height"),
            Key([], "x", lazy.window.kill(), desc="Kill focused window"),
        ],
        mode="FLOAT RS"),

    # Floating Window Moving
    KeyChord([win, "shift", alt], "m", [
            Key([], "h", lazy.function(move_floating, -FLOAT_MV_INC, 0), desc="Decrease floating window width"),
            Key([], "l", lazy.function(move_floating, FLOAT_MV_INC, 0), desc="Increase floating window width"),
            Key([], "j", lazy.function(move_floating, 0, FLOAT_MV_INC), desc="Increase floating window height"),
            Key([], "k", lazy.function(move_floating, 0, -FLOAT_MV_INC), desc="Decrease floating window height"),
            Key(["shift"], "h", lazy.function(move_floating, -4 * FLOAT_MV_INC, 0), desc="Decrease floating window width"),
            Key(["shift"], "l", lazy.function(move_floating, 4 * FLOAT_MV_INC, 0), desc="Increase floating window width"),
            Key(["shift"], "j", lazy.function(move_floating, 0, 4 * FLOAT_MV_INC), desc="Increase floating window height"),
            Key(["shift"], "k", lazy.function(move_floating, 0, -4 * FLOAT_MV_INC), desc="Decrease floating window height"),
            Key([], "x", lazy.window.kill(), desc="Kill focused window"),
        ],
        mode="FLOAT MV"),

    Key([win], "f", lazy.window.toggle_floating()),

    # Qtile Management Actions
    Key([win, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key(["control", "shift"], "Escape", lazy.function(shutdown_reboot_menu), desc="Start Shutdown/Reboot Menu with Rofi"),
    Key([win, "control"], "s", lazy.spawn("feh ~/Pictures/qtile_layout/"), desc="View Qtile Key Map"),
    Key([win, "shift"], "l", lazy.spawn("xscreensaver-command -lock"), desc="Lock Session"),

    # Launch Applications
    Key([win], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([win], "r", 
            lazy.spawn("rofi -show-icons -modi run,drun,window,combi -combi-modi drun,window -show combi"),
            desc="launch rofi"),
    Key([win], "e", lazy.spawn("pcmanfm"), desc="Open File Manager"),
    Key([win], 'v', lazy.spawn("termite -t 'openvpn_console' -e '/home/hawo/scripts/vpn_connect.sh'"), desc="Start VPN connection"), # VPN SELECTOR
    Key([win, "shift"], 'v', lazy.spawn('/home/hawo/scripts/vpn_kill.sh'), desc="kill openvpn"),
    Key([win, alt], 's', lazy.spawn("rofi -show-icons -ssh-command 'termite -e \"ssh {host}\"' -modi ssh -show ssh"), desc="SSH Menu"),
    Key([win, "shift"], 's', lazy.spawn('flameshot gui'), desc="Screenshot"),

    # Specific window Actions
    Key([win], "a", lazy.spawn("rofi -show-icons -modi window -show window"), desc="Show all windows in rofi (allow to switch)"),
    Key(['control', alt], 'm', lazy.function(move_to_group_selector), desc="Move current window to group using a rofi selector"),
    Key([win], "g", lazy.function(group_switch_selector), desc="Switch to group using a rofi selector"),

    # sound control
    Key([alt], "F1", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"), desc="Mute Audio Out"),
    Key([alt], "F2", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%"), desc="Decrease Volume"),
    Key([alt], "F3", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%"), desc="Increase Volume"),

    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -2%"), desc="Decrease Volume"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +2%"), desc="Increase Volume"),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="Play/Pause Media"),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Next Track"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Previous Track"),

    Key([alt, "shift"], "o", lazy.function(audio_out_selector), desc="Select pulseaudio sink"),

    # Clipboard Manager
    Key(['control', alt], 'c', lazy.spawn("rofi -modi 'clipboard:greenclip print' -show clipboard -run-command '{cmd}'"), desc="Show clipboard contents"),
    Key(['control', alt], 'e', lazy.spawn('/home/hawo/dotfiles/qtile/emoji_select.sh --rofi'), desc="Emoji Selector using rofi"),

    Key([win], 'l', lazy.function(toggle_lights), desc="Turn on Lights"),

    
]
groups = [
        Group("main"),
        Group("alt"),
        Group("www", matches=[Match(wm_class="Firefox"),
                              Match(wm_class="Opera")]),
        Group("mail", matches=[Match(wm_class=["Mail", "Thunderbird"]),
                               Match(wm_class=["Rocket.Chat"])]),
        Group("comms", matches=[Match(wm_class="TelegramDesktop"),
                                Match(wm_class=re.compile(".*whatsapp.*")),
                                Match(wm_class="Signal")]),
        Group("media", matches=Match(wm_class="Spotify")),
        ]

for n, i in enumerate(groups):
    keys.extend([
        # win + letter of group = switch to group
        Key([win], str(n + 1), lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # win + shift + letter of group = switch to & move focused window to group
        Key([win, "shift"], str(n + 1), lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # win + shift + letter of group = move focused window to group
        # Key([win, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

layouts = [
    layout.Columns(border_focus=clr_color1,
                   border_normal=clr_color2,
                   border_width=3,
                   grow_amount=2,
                   margin=16,
                   insert_position=1,
                   num_columns=4),
    layout.Max(margin=16),
    layout.Tile(margin=16,
                border_width=2),
]

widget_defaults = dict(
    font='NotoSansMono Nerd Font Regular',
    # font='sans',
    fontsize=24,
    padding=4,
)
extension_defaults = widget_defaults.copy()

spacer = widget.Sep(size_percent=80, padding=4,
                    linewidth=2,
                    foreground=clr_color5)

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Chord(foreground=clr_color11,
                             background=clr_color4),
                # widget.CurrentLayout(foreground=clr_foreground),

                widget.GroupBox(highlight_method='block',
                                borderwidth=0,
                                padding=7,
                                # fmt="<span weight='bold>{}</span>",
                                block_highlight_text_color=clr_background,
                                this_current_screen_border=clr_color14,
                                this_screen_border=clr_color6,
                                other_current_screen_border=clr_color11,
                                other_screen_border=clr_color3,
                                urgent_border=clr_foreground,
                                urgent_text=clr_background,
                                disable_drag=True,
                                inactive=clr_color12,
                                active=clr_color5,
                                hide_unused=False),
                spacer,
                widget.WindowCount(show_zero=True),
                spacer,
                widget.WindowName(foreground=clr_foreground),
                # widget.CheckUpdates(display_format=u'\U0001F504 {updates}'),
                spacer,
                widget.Memory(foreground=clr_color6,
                              format='RAM: {MemUsed: .0f} MB'),
                spacer,
                widget.CPU(foreground=clr_color3,
                           format='CPU @ {freq_current} GHz {load_percent:3.0f}% ->'),
               widget.ThermalSensor(foreground=clr_color10, 
                                     foreground_alert=clr_color9),
                spacer,
                widget.Net(format="{down}",
                           foreground=clr_color6,),
                widget.TextBox(text=u"\u21D3 | \u21D1"),
                widget.Net(format="{up}",
                           foreground=clr_color3),
                spacer, 
                widget.Volume(),
                # widget.Open_Weather(cityid="Karlsruhe",
                #                     app_key="552454590f5ac95df45d0d8b5b92bb64"),
                CapsNumLockIndicator_Nice(background=clr_color3,
                                          foreground=clr_background),
                widget.Systray(padding=7,
                               background=clr_color3),
                widget.Clock(format=' %H:%M %a %d.%m.%Y',
                             foreground=clr_background,
                             background=clr_color3),
                widget.CurrentLayoutIcon(scale=0.8,
                                         background=clr_color3),
            ],
            40,
            margin=[0, 0, 0, 0],
            background=reduce_brightness(clr_color4,0.5),
        ),
    ),
    Screen(),
]

# Drag floating layouts.
# Button 4 -> Scroll Up
# Button 5 -> Scroll Down
mouse = [
    Drag([win], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([win], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([win], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = True
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),    # gitk
    Match(wm_class='maketag'),       # gitk
    Match(wm_class='ssh-askpass'),   # ssh-askpass
    Match(title='branchdialog'),     # gitk
    Match(title='pinentry'),         # GPG key password entry
    Match(title=re.compile('.*hourglass.*')),      # Hourglass timer
    Match(title='Picture in Picture'),
    Match(title='openvpn_console'),
    Match(title='Generate Fonts'),
    Match(title=re.compile("Settings"),
          wm_class=re.compile("zoom")),
    Match(title=re.compile("Polls"),
          wm_class=re.compile("zoom")),
    # Match(title=re.compile("Chat"),
    #       wm_class=re.compile("zoom")),
],
    border_focus=clr_color5)
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
    home = os.path.expanduser('~')
    subprocess.call(home + "/.config/qtile/autostart.sh")
