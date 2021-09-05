Dotbot yay Plugin

For use with dotbot, this plugin allows one to easily install or upgrade a list of pamac packages.

This plugin is inspired by dotbot-yay.

dotbot-yay was itself heavily inspired by the apt-get plugin.
Usage

It's easiest to track this plugin in your dotfiles repo:

git submodule add https://github.com/smokeythemonkey/dotbot-pamac

The original author also recommends having your yay list in a separate file since dotbot will need root privileges in order to use the plugin.

If you use the default install script provided by dotbot, using the plugin will look like this:

./dotbot/bin/dotbot -p dotbot-yay/yay.py -c packages.conf.yaml

Using the install script provided by this repo, using the plugin will look like this:

./install packages

Example for packages.conf.yaml:

- pamac:
  - vim
  - zsh
  - tldr