###############################################################################
#    byobu's tmux f-key keybindings
#
#    Copyright (C) 2011-2012 Dustin Kirkland <dustin.kirkland@gmail.com>
#
#    Authors: Dustin Kirkland <dustin.kirkland@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################

# Add F12 to the prefix list
set -g prefix F12

# Byobu's Keybindings
# Documented in: $BYOBU_PREFIX/share/doc/byobu/help.tmux.txt

bind-key -n C-a new-window -n "ctrl-a" "byobu-ctrl-a"

# Set 1 (designed for standard layout keyboards)
bind-key -n F4 new-window -k -n config byobu-config
bind-key -n F3 new-window \; rename-window ""
bind-key -n S-F3 display-panes \; split-window -h
bind-key -n C-S-F3 display-panes \; split-window -v
bind-key -n F1 previous-window
bind-key -n F2 next-window
bind-key -n S-Up display-panes \; select-pane -U
bind-key -n S-Down display-panes \; select-pane -D
bind-key -n S-Left display-panes \; select-pane -L
bind-key -n S-Right display-panes \; select-pane -R
bind-key -n C-F11 display-panes \; select-pane -U
bind-key -n C-F10 display-panes \; select-pane -D
bind-key -n C-F9 display-panes \; select-pane -L
bind-key -n C-F12 display-panes \; select-pane -R
bind-key -n C-F3 display-panes \; swap-pane -s :. -t :.- \; select-pane -t :.-
bind-key -n C-F4 display-panes \; swap-pane -s :. -t :.+ \; select-pane -t :.+
bind-key -n S-F1 swap-window -t :-1
bind-key -n S-F2 swap-window -t :+1
bind-key -n C-Up resize-pane -U
bind-key -n C-Down resize-pane -D
bind-key -n C-Left resize-pane -L
bind-key -n C-Right resize-pane -R
bind-key -n F6 source $BYOBU_PREFIX/share/byobu/keybindings/f-keys.tmux.disable
bind-key -n S-F6 run-shell 'exec touch $BYOBU_RUN_DIR/no-logout' \; detach
bind-key -n C-F6 kill-pane
bind-key -n F7 copy-mode
bind-key -n S-F7 command-prompt -p "(rename-window)" "rename-window %%"
bind-key -n M-IC paste-buffer

# Set 2 (designed for small layout keyboards)
bind-key -n M-i display-panes \; split-window -h
bind-key -n M-- display-panes \; split-window -v
bind-key -n M-k display-panes \; select-pane -U
bind-key -n M-j display-panes \; select-pane -D
bind-key -n M-h display-panes \; select-pane -L
bind-key -n M-l display-panes \; select-pane -R
bind-key -n M-a break-pane
bind-key -n M-e source $BYOBU_PREFIX/share/byobu/keybindings/f-keys.tmux.disable
bind-key -n M-r source $BYOBU_PREFIX/share/byobu/keybindings/f-keys.tmux


# Unused
#bind-key -n S-F1 new-window -k -n help '$BYOBU_PAGER $BYOBU_PREFIX/share/doc/byobu/help.tmux.txt'
#bind-key -n C-S-F2 new-session
#bind-key -n M-Up choose-session \; send-keys Up \; send-keys Enter
#bind-key -n M-Down choose-session \; send-keys Down \; send-keys Enter
#bind-key -n S-F3 display-panes \; select-pane -t :.-
#bind-key -n S-F4 display-panes \; select-pane -t :.+
#bind-key -n M-NPage copy-mode \; send-keys NPage
#bind-key -n M-PPage copy-mode \; send-keys PPage
#bind-key -n F9 new-window -k -n config byobu-config
#bind-key -n C-F11 join-pane -h -s :. -t :-1
#bind-key -n S-F11 join-pane -v -s :. -t :-1
#bind-key -n C-S-F12 new-window $BYOBU_PREFIX/lib/byobu/include/mondrian
#bind-key -n F8 command-prompt -p "(rename-window)" "rename-window %%"
#bind-key -n S-F8 next-layout
#bind-key -n C-F8 new-window -k "byobu-layout restore; clear; $SHELL"
#bind-key -n C-S-F8 command-prompt -p "Save byobu layout as:" "run-shell 'byobu-layout save %%'"
#bind-key -n F5 source $BYOBU_PREFIX/share/byobu/profiles/tmuxrc
#bind-key -n S-F5 new-window -k "$BYOBU_PREFIX/lib/byobu/include/cycle-status" \; source $BYOBU_PREFIX/share/byobu/profiles/tmuxrc
#bind-key -n C-F5 send-keys ". $BYOBU_PREFIX/bin/byobu-reconnect-sockets" \; send-keys Enter
#bind-key -n C-S-F5 new-window -d "byobu-select-profile -r"
#bind-key -n F6 detach
