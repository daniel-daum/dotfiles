# dotfiles

Personal config for my macOS and Linux (OrbStack) machines: shell, editor, terminal, VCS, and toolchain setup.

## Notable choices

- **[Jujutsu (jj)](https://jj-vcs.github.io/jj/)** as the daily VCS, backed by git. Commits are SSH-signed at push time via [Secretive](https://github.com/maxgoedjen/secretive) (secure enclave-backed SSH keys), verified against `~/.gitallowedsigners`.
- **[mise](https://mise.jdx.dev/)** manages language runtimes and CLI tool versions.
- **[difftastic](https://difftastic.wilfred.me.uk/)** (structural diffs) and **[delta](https://github.com/dandavison/delta)** (syntax highlighting) for diffs in both git and jj.
- Primary repo lives on a self-hosted [Gitea](https://about.gitea.com/) instance (`git.danieldaum.net`). A CI job (`.gitea/workflows/mirror.yaml`) mirrors `main` to GitHub and [Tangled](https://tangled.sh/) on push.
- Linux dev machine is an OrbStack VM (`mustafar`), provisioned via the steps in `mustafar.txt`.

## Layout

| File | Purpose |
| --- | --- |
| `.zshrc`, `.bashrc` | Shell config: `mise` activation, `eza`/`bat` aliases |
| `.zsh_plugins.txt` | Zsh plugin list for [antidote](https://getantidote.github.io/) |
| `.gitconfig` | Git config, delta pager, difftastic diff tool, SSH commit signing |
| `jj.config.toml` | Jujutsu config, mirrors git identity/signing, custom log template and aliases |
| `ssh.config` | SSH client config for local VMs and remote hosts |
| `Brewfile` | macOS packages/casks (`brew bundle`) |
| `mise.config.toml`, `mise.config.lock` | Toolchain versions managed by mise |
| `zed.settings.json`, `zed.keymap.json`, `zed_extensions.txt` | [Zed](https://zed.dev/) editor config |
| `warp.settings.toml` | [Warp](https://www.warp.dev/) terminal config |
| `init.txt` | macOS bootstrap: Xcode CLT, Rosetta, Homebrew |
| `mustafar.txt` | Linux VM bootstrap: packages, mise, config sync |
| `.gitea/workflows/mirror.yaml` | CI: mirrors this repo to GitHub and Tangled |

## Usage

`init.txt` and `mustafar.txt` are step-by-step notes for bootstrapping a new macOS machine or Linux VM. The rest are config files meant to be symlinked or copied into place by hand.
