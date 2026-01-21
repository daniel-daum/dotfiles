# ssh auth
export SSH_AUTH_SOCK=/Users/daniel/Library/Containers/com.maxgoedjen.Secretive.SecretAgent/Data/socket.ssh

# antidote
source /opt/homebrew/opt/antidote/share/antidote/antidote.zsh
ZSH_THEME="robbyrussell"
antidote load

# eza ls replacement (long, all files, human-readable, icons, git info)
alias ll="eza -al --group-directories-first --icons --git --color=auto --long --header --classify"
