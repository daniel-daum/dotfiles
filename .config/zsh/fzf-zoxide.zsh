# ---- fzf + zoxide ---------------------------------------------------------
# Colors live in ~/.config/fzf/fzfrc and use the terminal's 16 colors,
# so fzf (and zoxide's picker, which runs fzf) follow the active Warp theme.
export FZF_DEFAULT_OPTS_FILE="$HOME/.config/fzf/fzfrc"

# Folders the file/folder pickers skip
__fz_skip=".git,node_modules,.venv,target,dist,.cache,.Trash,Library"

# Previews: bat for files, an eza tree for folders
__fz_preview='if [ -d {} ]; then eza --tree --level=2 --icons=always --color=always --group-directories-first {}; else bat --color=always --style=numbers --line-range=:300 {}; fi'

export FZF_CTRL_T_OPTS="--walker=file,dir,follow,hidden --walker-skip=$__fz_skip --preview '$__fz_preview'"
export FZF_ALT_C_OPTS="--walker=dir,follow,hidden --walker-skip=$__fz_skip --preview 'eza --tree --level=2 --icons=always --color=always --group-directories-first {}'"

# Key bindings (ctrl-t, ctrl-r, alt-c) and ** tab completion.
# Warp replaces the shell's line editor and lists fzf's bindings as a conflict,
# so load them everywhere except Warp (they work in Zed's terminal, iTerm, etc).
if [[ $TERM_PROGRAM != "WarpTerminal" ]]; then
  source <(fzf --zsh)
fi

# Commands that work in Warp too:
#   fe [dir]   pick file(s) with a preview and open them in $EDITOR
#   fcd [dir]  pick a folder below the current one and cd into it
fe() {
  local files
  files=("${(@f)$(fzf --multi --walker=file,follow,hidden --walker-skip=$__fz_skip \
    --walker-root="${1:-.}" --preview "$__fz_preview")}") || return
  (( ${#files} )) && ${=EDITOR:-zed} "${files[@]}"
}
fcd() {
  local dir
  dir=$(fzf --walker=dir,follow,hidden --walker-skip=$__fz_skip --walker-root="${1:-.}" \
    --preview 'eza --tree --level=2 --icons=always --color=always --group-directories-first {}') && cd "$dir"
}

# zoxide: z <part of a path> jumps to the best match, zi opens a picker.
# These are zoxide's own picker settings with an eza preview instead of ls.
export _ZO_FZF_OPTS="--exact --no-sort --cycle --keep-right --info=inline-right --layout=reverse --tabstop=1 --exit-0 --bind=ctrl-z:ignore,btab:up,tab:down --preview='eza --tree --level=2 --icons=always --color=always --group-directories-first {2..}' --preview-window=down,40%"
eval "$(zoxide init zsh)"   # keep this last in .zshrc
