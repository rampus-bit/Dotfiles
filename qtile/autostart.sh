#!/bin/bash

function run {
	if ! pgrep $1 ;
	then
		$@&
	fi
}

$HOME/.config/polybar/forest/launch.sh &

run discord &
run spotify &
run steam &
