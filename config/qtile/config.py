# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
# Copyright (c) 2021 Alden Garcia (Not actually Copyrighted)
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
import socket
import subprocess

from typing import List  # noqa: F401
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import qtile

from Xlib import X, display
from Xlib.ext import randr
from pprint import pprint

mod = "mod4"
terminal = guess_terminal()

keys = [
    ### Frequently Used Lone Hotkeys
    Key ([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "shift"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod], "x", lazy.shutdown(), desc="Shutdown Qtile"),

    # My Custom Keybindings
    Key([mod, "shift"], "d", lazy.spawn("dmenu_run")),

    # Window Shuffle
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),

    ### Personally Redundant Hotkeys
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),

    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # Change Window Focus
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "space", lazy.layout.next()),

    # Edit Window Size
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod], "n", lazy.layout.normalize()),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
    ])

layouts = [
    layout.Columns(
        margin = 4,
        border_width = 2,
        border_focus = '#c561ff',
        border_normal = '#1D2330',
        grow_amount = 1
    ),

    layout.MonadTall(
        margin = 6,
        border_width = 2,
        border_focus = '#c561ff',
        border_normal = '#1D2330'
    ),

    layout.Bsp(
        margin=60
    ),

    ### Revisit Later
    # layout.Tile(),
    # layout.Max(),
]

widget_defaults = dict(
    font = 'Ubuntu Mono',
    fontsize = 16,
    padding = 10,
)

extension_defaults = widget_defaults.copy()

# xrandr --output HDMI-A-O --rotate left

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.CurrentLayout(
                    foreground = '#61a5ff',
                    ),
                widget.Sep(),
                widget.CPU(
                    foreground = '#c561ff'
                    ),
                widget.Sep(),
                widget.Memory(
                    foreground = '#61ff8e',
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('dmenu_run')}
                    ),
                widget.Sep(),
                widget.BitcoinTicker(
                    foreground = 'ff5757',
                    currency = 'CAD'
                    ),
                widget.Spacer(),
                widget.Prompt(),
                widget.Chord(
                    chords_colors={
                        'launch': ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.TextBox(
                    foreground = '#ff5757',
                    text = 'Cross the Rubicon'
                    ),
                widget.Sep(),
                widget.CheckUpdates(
                    colour_have_updates = '57ffab',
                    foreground = '#57ffab',
                    ),
                widget.Sep(),
                widget.Volume(
                    foreground = 'c561ff',
                    ),
                widget.Sep(),
                widget.Clock(
                    foreground = 'ffae57',
                    format = '%Y-%m-%d %a %I:%M %p'
                    ),
            ],
            24,
            background="#282a36"
        ),
    ),

    Screen(
        bottom=bar.Bar(
            [
                widget.CurrentLayout(
                    foreground = '#61a5ff',
                    ),
                widget.Sep(),
                widget.CPU(
                    foreground = '#c561ff'
                    ),
                widget.Sep(),
                widget.Memory(
                    foreground = '#61ff8e',
                    ),
                widget.Sep(),
                widget.BitcoinTicker(
                    foreground = 'ff5757',
                    currency = 'CAD'
                    ),
                widget.Spacer(),
                widget.Prompt(),
                widget.Chord(
                    chords_colors={
                        'launch': ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Systray(),
                widget.TextBox(
                    foreground = '#ff5757',
                    text = 'Cross the Rubicon'
                    ),
                widget.Sep(),
                widget.CheckUpdates(
                    colour_have_updates = '57ffab',
                    foreground = '#57ffab',
                    ),
                widget.Sep(),
                widget.Volume(
                    foreground = 'c561ff',
                    ),
                widget.Sep(),
                widget.Clock(
                    foreground = 'ffae57',
                    format = '%Y-%m-%d %a %I:%M %p'
                    ),
            ],
            24,
            background="#282a36"
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[

    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),
    Match(wm_class='makebranch'),
    Match(wm_class='maketag'),
    Match(wm_class='ssh-askpass'),
    Match(title='branchdialog'),
    Match(title='pinentry'),
])
auto_fullscreen = True
focus_on_window_activation = "smart"

### Funny Comment
# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
