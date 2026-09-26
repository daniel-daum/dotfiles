# dotfiles

Personal config for my macOS and Linux (OrbStack) machines: shell, editor, terminal, VCS, and toolchain setup.

## Layout

| File | Purpose |
| --- | --- |
| `.zshrc`, `.bashrc` | Shell config: `mise` activation, `eza`/`bat` aliases |
| `.zsh_plugins.txt` | Zsh plugin list for [antidote](https://getantidote.github.io/) |
| `.gitconfig` | Git config, delta pager, difftastic diff tool, SSH commit signing |
| `ssh.config` | SSH client config for local VMs and remote hosts |
| `Brewfile` | macOS packages/casks (`brew bundle`) |
| `zed.settings.json`, `zed.keymap.json`, `zed_extensions.txt` | [Zed](https://zed.dev/) editor config |
| `init.txt` | macOS bootstrap: Xcode CLT, Rosetta, Homebrew |
| `mustafar.txt` | Linux VM bootstrap: packages, mise, config sync |
| `.gitea/workflows/mirror.yaml` | CI: mirrors this repo to GitHub |
