#!/bin/bash

function run {
	if ! pgrep $1 ;
	then
		$@&
	fi
}

picom --config $HOME/.config/i3/picom.conf &

run spotify &
