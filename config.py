import os
import subprocess

from typing import List  # noqa: F401
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

alt = "mod1"
mod = "mod4"
terminal = guess_terminal()

keys = [
    ### Frequently Used Lone Hotkeys
    Key([alt], "Return", lazy.spawn("kitty"), desc="Launch terminal"),
    Key([alt], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([alt, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([alt, "shift"], "r", lazy.restart(), desc="Restart Qtile"),

    # My Custom Bindings
    Key([alt, "shift"], "d", lazy.spawn("rofi -show run")),
    Key([alt], "x", lazy.spawn("arcolinux-logout")),
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
        # mod1 + letter of group = switch to group
        Key([alt], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([alt, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
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
        border_normal = '#1D2330',
        ratio = 0.5
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

    Screen(
        wallpaper = '~/Pictures/Wallpapers/Personal/Tokyo.png',
        wallpaper_mode = 'fill',
        bottom = bar.Bar(
            [
                widget.Spacer(
                    length = 8
                    ),
                # widget.Image(
                #     filename = '~/.config/qtile/icons/python-white.png',
                #     scale = 'False',
                #     padding = 10,
                #     mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('atom .')}
                #     ),
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
dgroups_app_rules = []  # type: List
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
reconfigure_screens = True

auto_minimize = True

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

wmname = "LG3D"
