#     _    _     _               ____                _
#    / \  | | __| | ___ _ __    / ___| __ _ _ __ ___(_) __ _
#   / _ \ | |/ _` |/ _ \ '_ \  | |  _ / _` | '__/ __| |/ _` |
#  / ___ \| | (_| |  __/ | | | | |_| | (_| | | | (__| | (_| |
# /_/   \_\_|\__,_|\___|_| |_|  \____|\__,_|_|  \___|_|\__,_|

# Dog goes crazy
# https://www.youtube.com/watch?v=zCZEbnblMIE

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

# Variable Definitions
alt = "mod1"
mod = "mod4"
terminal = guess_terminal()

keys = [
    ### Frequently Used Lone Hotkeys
    Key ([alt], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([alt], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([alt, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([alt, "shift"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([alt], "x", lazy.shutdown(), desc="Shutdown Qtile"),

    # My Custom Keybindings
    Key([alt, "shift"], "d", lazy.spawn("rofi -show run")),
    Key([alt], "f", lazy.window.toggle_fullscreen()),

    # Custom Application Spawning
    Key([alt, "shift"], "s", lazy.spawn("steam")),
    Key([alt, "shift"], "n", lazy.spawn("nitrogen")),
    Key([alt, "shift"], "a", lazy.spawn("atom")),
    Key([alt, "shift"], "b", lazy.spawn("brave")),
    Key([alt, "shift"], "Return", lazy.spawn("nautilus")),

    # Mod Subset
    Key([mod, "shift"], "d", lazy.spawn("discord")),

    # Window Shuffle
    Key([alt, "shift"], "Left", lazy.layout.shuffle_left()),
    Key([alt, "shift"], "Right", lazy.layout.shuffle_right()),
    Key([alt, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([alt, "shift"], "Up", lazy.layout.shuffle_up()),

    ### Personally Redundant Hotkeys
    Key([alt, "shift"], "t", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),

    Key([alt], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # Change Window Focus
    Key([alt], "h", lazy.layout.left()),
    Key([alt], "l", lazy.layout.right()),
    Key([alt], "j", lazy.layout.down()),
    Key([alt], "k", lazy.layout.up()),
    Key([alt], "space", lazy.layout.next()),

    # Edit Window Size
    Key([alt, "control"], "h", lazy.layout.grow_left()),
    Key([alt, "control"], "l", lazy.layout.grow_right()),
    Key([alt, "control"], "j", lazy.layout.grow_down()),
    Key([alt, "control"], "k", lazy.layout.grow_up()),
    Key([alt], "n", lazy.layout.normalize()),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        Key([alt], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        Key([alt, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
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
        margin = 8,
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
        wallpaper = '~/Pictures/Wallpapers/generic/forest1.jpg',
        wallpaper_mode = 'fill',
        bottom = bar.Bar(
            [
                widget.Spacer(
                    length = 8
                    ),
                widget.Image(
                    filename = '~/.config/qtile/icons/python-white.png',
                    scale = 'False',
                    padding = 10,
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('atom .')}
                    ),
                widget.CurrentLayout(
                    foreground = '#61a5ff',
                    ),
                widget.Sep(),
                widget.TextBox(
                    text = ' ⌨️',
                    padding = 0
                    ),
                widget.CPU(
                    foreground = '#c561ff'
                    ),
                widget.Sep(),
                widget.TextBox(
                    text = ' 🖬',
                    padding = 0,
                ),
                widget.Memory(
                    foreground = '#61ff8e',
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e htop')},
                    ),
                widget.Sep(),
                widget.TextBox(
                    text = ' 🪙',
                    padding = 0
                    ),
                widget.BitcoinTicker(
                    foreground = 'ff5757',
                    currency = 'CAD'
                    ),
                widget.Sep(),
                widget.TextBox(
                    text = ' 🖇️',
                    padding = 0
                    ),
                widget.WindowName(
                    foreground = 'ffae57',
                ),
                widget.Prompt(),
                widget.Chord(
                    chords_colors={
                        'launch': ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.TextBox(
                    text = ' 💎',
                    padding = 0
                    ),
                widget.TextBox(
                    foreground = '#ff5757',
                    text = 'Cross the Rubicon',
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e cmatrix')},
                    ),
                # widget.Sep(),
                # widget.TextBox(
                #     text = ' ⟳',
                #     padding = 0
                #     ),
                # widget.CheckUpdates(
                #     color_no_updates = '57ffab',
                #     colour_have_updates = '57ffab',
                #     foreground = '#57ffab',
                #     ),
                widget.Sep(),
                widget.TextBox(
                    text = ' 🔊',
                    padding = 0
                    ),
                widget.TextBox(
                    text = 'Vol:',
                    foreground = 'c561ff',
                    ),
                widget.Volume(
                    foreground = 'c561ff',
                    ),
                widget.Sep(),
                widget.TextBox(
                    text = ' 🗓️',
                    padding = 0
                    ),
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
        #xrandr --output HDMI-A-0 --rotate left
        wallpaper = '~/Pictures/Wallpapers/generic/forest1.jpg',
        wallpaper_mode = 'stretch',
        #screen_change = 'xrandr --output HDMI-A-0 --rotate left',
        bottom = bar.Bar(
            [
                widget.Spacer(
                    length = 8
                    ),
                widget.Image(
                    filename = '~/.config/qtile/icons/python-white.png',
                    scale = 'False',
                    padding = 10,
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('atom .')}
                    ),
                widget.CurrentLayout(
                    foreground = '#61a5ff',
                    ),
                widget.Sep(),
                widget.TextBox(
                    text = ' ⌨️',
                    padding = 0
                    ),
                widget.CPU(
                    foreground = '#c561ff'
                    ),
                widget.Sep(),
                widget.TextBox(
                    text = ' 🖬',
                    padding = 0,
                ),
                widget.Memory(
                    foreground = '#61ff8e',
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e htop')},
                    ),
                widget.Spacer(),
                widget.Prompt(),
                widget.Chord(
                    chords_colors={
                        'launch': ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                # widget.TextBox(
                #     text = ' ⟳',
                #     padding = 0
                #     ),
                # widget.CheckUpdates(
                #     mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal)},
                #     color_no_updates = '57ffab',
                #     colour_have_updates = '57ffab',
                #     foreground = '#57ffab',
                #     ),
                widget.TextBox(
                    text = ' 🔊',
                    padding = 4
                    ),
                widget.TextBox(
                    text = 'Vol:',
                    foreground = 'c561ff',
                    padding = 4
                    ),
                widget.Volume(
                    foreground = 'c561ff',
                    padding = 4
                    ),
                widget.Sep(
                    padding = 10
                ),
                widget.TextBox(
                    text = 'Active:',
                    foreground = 'ff5757',
                    padding = 4
                    ),
                widget.Systray(
                    padding = 6,
                ),
                widget.Spacer(
                    length = 8
                    ),
                widget.Sep(),
                widget.TextBox(
                    text = ' 🗓️',
                    padding = 0
                    ),
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
    Drag([alt], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([alt], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([alt], "Button2", lazy.window.bring_to_front())
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
