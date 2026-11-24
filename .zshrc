# ---- environment ------------------------------------------------------------
export DO_NOT_TRACK=1                # opt out of telemetry
export HOMEBREW_NO_ANALYTICS=1
export LOCAL_NOTEBOOK_DEV=1          # zed notebooks
export SSH_AUTH_SOCK="$HOME/Library/Containers/com.maxgoedjen.Secretive.SecretAgent/Data/socket.ssh"


# where eza and bat read their themes
export EZA_CONFIG_DIR="$HOME/.config/eza"
export BAT_CONFIG_DIR="$HOME/.config/bat"

# ---- aliases ----------------------------------------------------------------
alias ll="eza -al --group-directories-first --icons --git --header --classify"
alias cat="bat"

# ---- tools (keep last) ------------------------------------------------------
# prompt for terminals other than warp
[[ $TERM_PROGRAM != WarpTerminal ]] && eval "$(starship init zsh)"
eval "$(mise activate zsh)" # mise

# Added by LM Studio CLI (lms)
export PATH="$PATH:/Users/daniel/.lmstudio/bin"
# End of LM Studio CLI section
