# ---- environment ------------------------------------------------------------
export DO_NOT_TRACK=1                # opt out of telemetry
export HOMEBREW_NO_ANALYTICS=1
export LOCAL_NOTEBOOK_DEV=1          # zed notebooks
export SSH_AUTH_SOCK="$HOME/Library/Containers/com.maxgoedjen.Secretive.SecretAgent/Data/socket.ssh"

# where eza and bat read their themes
export EZA_CONFIG_DIR="$HOME/.config/eza"
export BAT_CONFIG_DIR="$HOME/.config/bat"

# ---- path -------------------------------------------------------------------
typeset -U path                      # skip duplicate entries
path+=(
  "$HOME/.lmstudio/bin"              # LM Studio CLI (lms)
  "${GOPATH:-$HOME/go}/bin"          # tools from `go install`
)

# ---- plugins ----------------------------------------------------------------
source /opt/homebrew/opt/antidote/share/antidote/antidote.zsh
setopt PROMPT_SUBST
antidote load

# ---- aliases ----------------------------------------------------------------
alias ll="eza -al --group-directories-first --icons --git --header --classify"
alias cat="bat"

# ---- tools (keep last) ------------------------------------------------------
eval "$(mise activate zsh)" # mise
source "$HOME/.config/zsh/fzf-zoxide.zsh"   # fzf + zoxide
