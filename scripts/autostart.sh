#!/bin/bash

WM=$DESKTOP_SESSION

function run {
	if ! pgrep $1 ;
	then
			$@&
	fi
}

if [[ $WM = i3 ]]
then
	sudo mount -b /dev/sdb1
fi

picom --config $HOME/.config/bspwm/picom.conf &

run discord &
run spotify &
