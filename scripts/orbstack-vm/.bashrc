# ========================= personal config =========================
# ---- environment ------------------------------------------------------------
export EDITOR=hx                     # helix as default editor
export VISUAL=hx
export COLORTERM=truecolor           # ssh drops this; bat, delta and helix need it for exact colors

# ---- path -------------------------------------------------------------------
export PATH="$HOME/go/bin:$PATH"     # tools from `go install`

# ---- aliases ----------------------------------------------------------------
# LS_COLORS= stops Ubuntu's dircolors from overriding the eza theme
alias ll='LS_COLORS= eza -al --group-directories-first --icons --git --header --classify=auto'
alias lt='LS_COLORS= eza --tree --level=2 --icons --git-ignore'
alias cat='bat'

# ---- tools ------------------------------------------------------------------
eval "$(~/.local/bin/mise activate bash)"   # puts bat, eza, fzf, helix, zoxide... on PATH

# ---- fzf --------------------------------------------------------------------
export FZF_DEFAULT_OPTS_FILE="$HOME/.config/fzf/fzfrc"   # colors follow the Warp theme
__fz_skip=".git,node_modules,.venv,target,dist,.cache"
__fz_preview='if [ -d {} ]; then eza --tree --level=2 --icons=always --color=always --group-directories-first {}; else bat --color=always --style=numbers --line-range=:300 {}; fi'
export FZF_CTRL_T_OPTS="--walker=file,dir,follow,hidden --walker-skip=$__fz_skip --preview '$__fz_preview'"
export FZF_ALT_C_OPTS="--walker=dir,follow,hidden --walker-skip=$__fz_skip --preview 'eza --tree --level=2 --icons=always --color=always --group-directories-first {}'"

# fzf's Ctrl-T / Ctrl-R / Alt-C keys: off, since Warp handles keys over ssh.
# Uncomment if you connect from Zed's terminal instead.
# eval "$(fzf --bash)"

# fe [dir]: pick file(s) with a preview and open them in helix
fe() {
  local files=()
  mapfile -t files < <(fzf --multi --walker=file,follow,hidden --walker-skip="$__fz_skip" \
    --walker-root="${1:-.}" --preview "$__fz_preview")
  (( ${#files[@]} )) && ${EDITOR:-hx} "${files[@]}"
}

# fcd [dir]: pick a folder below the current one and cd into it
fcd() {
  local dir
  dir=$(fzf --walker=dir,follow,hidden --walker-skip="$__fz_skip" --walker-root="${1:-.}" \
    --preview 'eza --tree --level=2 --icons=always --color=always --group-directories-first {}') && cd "$dir"
}

# ---- zoxide (keep last) -----------------------------------------------------
# z <name> jumps to a folder you've visited, zi opens a picker
export _ZO_FZF_OPTS="--exact --no-sort --cycle --keep-right --info=inline-right --layout=reverse --tabstop=1 --exit-0 --bind=ctrl-z:ignore,btab:up,tab:down --preview='eza --tree --level=2 --icons=always --color=always --group-directories-first {2..}' --preview-window=down,40%"
eval "$(zoxide init bash)"
