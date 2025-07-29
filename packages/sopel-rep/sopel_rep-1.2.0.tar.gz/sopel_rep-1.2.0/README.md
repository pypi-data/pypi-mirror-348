# sopel-rep

Karma plugin for Sopel IRC bots.

Lets users "luv" and "h8" other users on IRC. Functional clone of a mIRC script
someone used in a channel I was in. (Never saw their code, not that I'd want to
do a *port* of anything written for mIRC...)

## Requirements

This plugin is compatible with Sopel 7.1 or higher. However, even though Sopel 7
supports many legacy Python versions back to 2.7, the plugin is only tested
against current versions of Python (3.8+).

## Installing

Releases are hosted on PyPI, so after installing Sopel, all you need is `pip`:

```shell
$ pip install sopel-rep
```

## Configuring

The easiest way to configure `sopel-rep` is via Sopel's configuration
wizard—simply run `sopel-plugins configure rep` and enter the values for which
it prompts you. Settings are described below:

* `cooldown`: How long in seconds each user must wait after changing anyone's
  rep before they are permitted to do so again.\
  _Default: 3600_
* `admin_cooldown`: Whether the bot's owner & admins must obey the cooldown.\
  _Default: true_

## Usage
### Commands
* `.luv nick`: Adds +1 to the user's reputation score
* `.h8 nick`: Adds -1 to the user's reputation score

### Actions
* `/me <3 nick`: Adds +1 to the user's reputation score
* `/me </3 nick`: Adds -1 to the user's reputation score

### Inline karma
* `nick++` anywhere in a message adds +1 to the user's reputation score
* `nick--` anywhere in a message adds -1 to the user's reputation score
