# mise
eval "$(mise activate zsh)"

# ssh auth
export SSH_AUTH_SOCK=/Users/daniel/Library/Containers/com.maxgoedjen.Secretive.SecretAgent/Data/socket.ssh

# antidote
source /opt/homebrew/opt/antidote/share/antidote/antidote.zsh
ZSH_THEME="robbyrussell"
antidote load

# eza ls replacement (long, all files, human-readable, icons, git info)
alias ll="eza -al --group-directories-first --icons --git --color=auto --long --header --classify"

# cat replacement
alias cat='bat'

# jj
alias jjp='jj git push'
alias jja='jj log -r "all()"'

# pnpm
export PNPM_HOME="/Users/daniel/Library/pnpm"
case ":$PATH:" in
  *":$PNPM_HOME:"*) ;;
  *) export PATH="$PNPM_HOME:$PATH" ;;
esac
# pnpm end
