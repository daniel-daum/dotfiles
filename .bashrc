# ============================== personal config ==============================

# mise
eval "$(~/.local/bin/mise activate bash)"

# go via mise
export PATH="$HOME/go/bin:$PATH"

# eza ls replacement
alias ll="eza -al --group-directories-first --icons --git --color=auto --long --header --classify"

# bat cat replacement
alias cat='bat'
