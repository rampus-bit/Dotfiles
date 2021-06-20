#!/bin/bash

function run {
	if ! pgrep $1 ;
	then
		$@&
	fi
}

$HOME/.config/polybar/forest/launch.sh &

xrandr --output HDMI-A-0 --rotate right --output HDMI-A-0 --left-of DisplayPort-0
feh --bg-fill /home/aldeng/Pictures/Wallpapers/Anime/Pillow-Hug.jpg &

run discord &
run spotify &
run steam &
