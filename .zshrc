# General Settings
export HISTCONTROL=ignoreboth:erasedups

export EDITOR='nvim'
export VISUAL='nvim'
export BROWSER='brave'
export TERMINAL='kitty'

# Prompt
PROMPT='%B%F{red}%1~%f%b %F{magenta}➜ %f'

# General Aliases
alias ls='ls --color=auto'
alias la='ls -a'
alias ll='ls -la'
alias l='ls'
alias l.="ls -A | egrep '^\.'"

# Personal Aliases
alias rc="nvim .config/zsh/.zshrc"
alias v='nvim'

# History Settings
HISTFILE=~/.config/zsh/.zsh_hist
HISTSIZE=10000
SAVEHIST=10000
setopt appendhistory

~/geode/geode.sh
