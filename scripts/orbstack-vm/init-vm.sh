#!/bin/bash
# Set up a new OrbStack VM.
# Run this on your Mac:
#   ./init-vm.sh MACHINE_NAME
# Afterwards, ssh in and paste your bashrc at the end of ~/.bashrc

set -e   # stop if any step fails

NAME="$1"
if [ -z "$NAME" ]; then
  echo "Usage: ./init-vm.sh MACHINE_NAME"
  exit 1
fi

# Folders in ~/.config on your Mac to copy into the VM. Edit as needed.
CONFIGS="fzf helix bat"


echo "== 0. Create isolated VM with mounted project folder =="
orb create --isolated --forward-ssh-agent \
  --mount /Users/daniel/projects:/home/daniel/projects \
  ubuntu:resolute "$NAME" --isolate-network

# The mount creates /home/daniel as root, so give it back to you
orb -m "$NAME" sudo chown daniel:daniel /home/daniel

# Because of that, Ubuntu skipped the default shell files. Copy them in.
orb -m "$NAME" cp /etc/skel/.bashrc /etc/skel/.profile /etc/skel/.bash_logout /home/daniel/


echo "== 1. Install standard packages =="
orb -m "$NAME" sudo apt update
orb -m "$NAME" sudo apt modernize-sources
orb -m "$NAME" sudo apt install -y nano vim-tiny less ca-certificates curl gnupg wget xz-utils unzip git build-essential passt bubblewrap
orb -m "$NAME" sudo apt update


echo "== 2. Install mise =="
orb -m "$NAME" bash -c 'curl https://mise.run | sh'


echo "== 3. Install global tools with mise =="
orb -m "$NAME" bash -c '~/.local/bin/mise use -g bat delta difftastic eza fd fzf helix jj jq node pi ripgrep zoxide'


echo "== 4. Copy ~/.config folders from your Mac =="
orb -m "$NAME" mkdir -p /home/daniel/.config
for folder in $CONFIGS; do
  echo "  copying $folder"
  orb push -m "$NAME" ~/.config/$folder /home/daniel/.config/
done


echo "Done. Now run: ssh $NAME@orb"
echo "Then paste your bashrc at the end of ~/.bashrc"
