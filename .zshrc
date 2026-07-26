# do not track
export DO_NOT_TRACK=1
export HOMEBREW_NO_ANALYTICS=1

# ssh auth
export SSH_AUTH_SOCK=/Users/daniel/Library/Containers/com.maxgoedjen.Secretive.SecretAgent/Data/socket.ssh

# antidote
source /opt/homebrew/opt/antidote/share/antidote/antidote.zsh
setopt PROMPT_SUBST
antidote load

# eza ls replacement (long, all files, human-readable, icons, git info)
alias ll="eza -al --group-directories-first --icons --git --color=auto --long --header --classify"

# cat replacement
alias cat='bat'

# Added by LM Studio CLI (lms)
export PATH="$PATH:/Users/daniel/.lmstudio/bin"
# End of LM Studio CLI section

# mise
eval "$(mise activate zsh)"
