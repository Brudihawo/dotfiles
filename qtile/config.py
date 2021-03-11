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
import subprocess

from typing import List  # noqa: F401

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import hook


# colors
def reduce_brightness(hex_color, factor):
    if factor > 1.0:
        factor = 1.0
    red   = f"{int(float(factor) * int(hex_color[1:3], 16)):#0{4}x}"[2:4]
    green = f"{int(float(factor) * int(hex_color[3:5], 16)):#0{4}x}"[2:4]
    blue  = f"{int(float(factor) * int(hex_color[5:7], 16)):#0{4}x}"[2:4]
    return "#{}{}{}".format(red,green,blue)


clr_foreground = "#9da8b7"
clr_background = "#01070f"
clr_color0 = "#01070f"
clr_color1 = "#562c5b"
clr_color2 = "#a50e46"
clr_color3 = "#1d6599"
clr_color4 = "#4e6677"
clr_color5 = "#448cc0"
clr_color6 = "#75b1de"
clr_color7 = "#9da8b7"
clr_color8 = "#3b526f"
clr_color9 = "#562c5b"
clr_color10 = "#a50e46"
clr_color11 = "#1d6599"
clr_color12 = "#4e6677"
clr_color13 = "#448cc0"
clr_color14 = "#75b1de"
clr_color15 = "#9da8b7"

# keys
win = "mod4"
alt = "mod1"

terminal = "termite -e fish"

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

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([win, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([win, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([win, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([win, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([win, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),

    # Window Resizing
    KeyChord([win, "shift"], "r", [
                Key([], "h", lazy.layout.grow_left(), desc="Grow window left"),
                Key([], "l", lazy.layout.grow_right(), desc="Grow window right"),
                Key([], "j", lazy.layout.grow_down(), desc="Grow window down"),
                Key([], "k", lazy.layout.grow_up(), desc="Grow window up"),
                Key([], "n", lazy.layout.normalize(), desc="Reset window sizes"),
            ],
            mode=u"\U0001F589"),

    # Qtile Management Actions
    Key([win, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([win, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    # Launch Applications
    Key([win], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([win], "r", 
            lazy.spawn("rofi -modi drun,window,combi -combi-modi drun,window -show combi"),
            desc="launch rofi"),
    Key([win], "f", lazy.window.toggle_floating()),

    # sound control
    Key([alt], "F1", lazy.spawn("amixer -q sset Master toggle &")),
    Key([alt], "F2", lazy.spawn("amixer -q sset Master 5%- &")),
    Key([alt], "F3", lazy.spawn("amixer -q sset Master 5%+ &")),
    
]

groups = [Group(i) for i in "123456789"]
for i in groups:
    keys.extend([
        # win + letter of group = switch to group
        Key([win], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # win + shift + letter of group = switch to & move focused window to group
        Key([win, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # win + shift + letter of group = move focused window to group
        # Key([win, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

layouts = [
    layout.Columns(border_focus=clr_color2,
                   border_normal=clr_color4,
                   border_width=1,
                   grow_amount=2,
                   margin=5,
                   insert_position=1),
    layout.Max(margin=5),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2,
                 # margin=8),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(border_focus=clr_color2,
                     # border_normal=clr_color4,
                     # margin=8),
    # layout.MonadWide(),
    # layout.RatioTile(),
    layout.Tile(margin=8),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='sans',
    fontsize=16,
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
                widget.CurrentLayoutIcon(scale=0.8,
                                         background=clr_color7),

                widget.Chord(foreground=clr_color2,
                             background=clr_color7),
                # widget.CurrentLayout(foreground=clr_foreground),

                widget.GroupBox(highlight_method='line',
                                # highlight_color=[clr_color6, clr_color6],
                                highlight_color=[reduce_brightness(clr_color11, 0.5)],
                                block_highlight_text_color=clr_color2,
                                disable_drag=True,
                                inactive=clr_color7,
                                active=clr_color6),
                spacer,
                widget.WindowCount(show_zero=True),
                spacer,
                widget.WindowName(foreground=clr_foreground),
                
                widget.Notify(background=clr_color2,
                              foreground=clr_foreground),

                widget.CheckUpdates(display_format=u'\U0001F504 {updates}'),
                spacer,
                widget.CPU(format='CPU @ {freq_current} GHz {load_percent:03.1f}%'),
                spacer,
                widget.Net(format="{down}",
                           foreground=clr_color2,),
                # widget.TextBox(text="\u2BAF | \u2BAC"),
                widget.TextBox(text="\u21E9 |  \u21EA"),
                widget.Net(format="{up}",
                           foreground=clr_color6,),
                spacer, 
                widget.Volume(),
                widget.Clock(format=' %H:%M %a %d.%m.%Y',
                             foreground=clr_color2,
                             background=clr_color7),
            ],
            26,
            margin=[0, 0, 0, 0],
            background=reduce_brightness(clr_color11,0.5),
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([win], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([win], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([win], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
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
