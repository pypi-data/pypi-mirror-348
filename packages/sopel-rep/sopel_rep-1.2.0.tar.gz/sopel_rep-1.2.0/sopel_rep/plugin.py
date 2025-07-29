"""sopel-rep

Karma plugin for Sopel IRC bots, cloning the behavior of an old mIRC script.

Copyright 2015-2024 dgw
"""
from __future__ import annotations

import re

from sopel import plugin
from sopel.config.types import BooleanAttribute, StaticSection, ValidatedAttribute
from sopel.tools import time as time_tools

from .errors import ArgumentError, CooldownError, NonexistentNickError
from .manager import RepManager, r_nick


KARMA_INLINE = r'(%s)(\+{2}|-{2})' % r_nick


class RepSection(StaticSection):
    cooldown = ValidatedAttribute('cooldown', int, default=3600)
    admin_cooldown = BooleanAttribute('admin_cooldown', default=True)


def setup(bot):
    bot.config.define_section('rep', RepSection)
    bot.memory['rep_manager'] = RepManager(bot)


def shutdown(bot):
    del bot.memory['rep_manager']


def configure(config):
    config.define_section('rep', RepSection)
    config.rep.configure_setting(
        'cooldown',
        "How often should users be allowed to change someone's rep, in seconds?",
    )
    config.rep.configure_setting(
        'admin_cooldown',
        "Should bot admins also have to obey that cooldown?",
    )


@plugin.rule(r'^(?P<command></?3)\s+(%s)\s*$' % r_nick)
@plugin.ctcp('ACTION')
@plugin.require_chanmsg("You may only modify someone's rep in a channel.")
def heart_cmd(bot, trigger):
    luv_h8(bot, trigger, trigger.group(2), 'h8' if '/' in trigger.group(1) else 'luv')


@plugin.search(KARMA_INLINE)
@plugin.require_chanmsg("You may only modify someone's rep in a channel.")
def karma_cmd(bot, trigger):
    if re.match('^({prefix})({cmds})'.format(prefix=bot.config.core.prefix, cmds='|'.join(luv_h8_cmd.commands)),
                trigger.group(0)):
        return  # avoid processing commands if people try to be tricky
    for (nick, act) in re.findall(KARMA_INLINE, trigger.raw):
        if luv_h8(bot, trigger, nick, 'luv' if act == '++' else 'h8', warn_nonexistent=False):
            break


@plugin.commands('luv', 'h8')
@plugin.example(".luv johnnytwothumbs")
@plugin.example(".h8 d-bag")
@plugin.require_chanmsg("You may only modify someone's rep in a channel.")
def luv_h8_cmd(bot, trigger):
    if not trigger.group(3):
        bot.reply("No user specified.")
        return

    luv_h8(bot, trigger, trigger.group(3), trigger.group(1))


def luv_h8(bot, trigger, target, which, warn_nonexistent=True):
    try:
        message = bot.memory['rep_manager'].luv_or_h8(trigger, target, which)
    except NonexistentNickError as err:
        if warn_nonexistent:
            bot.reply(str(err))
        return False
    except ArgumentError as err:
        bot.reply(str(err))
        return False
    except CooldownError as err:
        bot.notice(
            "You can change someone's rep again {}."
            .format(time_tools.seconds_to_human(-err.remaining_time)),
            trigger.nick,
        )
        return False

    bot.say(message)
    return True


@plugin.commands('rep')
@plugin.example(".rep johnnytwothumbs")
def show_rep(bot, trigger):
    target = trigger.group(3) or trigger.nick
    rep = bot.memory['rep_manager'].get_rep(target)
    if rep is None:
        bot.say("%s has no reputation score yet." % target)
        return
    bot.say("%s's current reputation score is %d." % (target, rep))


@plugin.commands('replock', 'repunlock')
@plugin.example('.replock BullyingVictim')
@plugin.require_admin('Only bot admins may manage reputation locks')
def manage_locks(bot, trigger):
    target = trigger.group(3)
    if not target:
        bot.reply("I need a nickname!")
        return
    if 'unlock' in trigger.group(1):  # .repunlock command used
        bot.memory['rep_manager'].unlock_rep(target)
        bot.say("Unlocked rep for %s." % target)
    else:  # .replock command used
        bot.memory['rep_manager'].lock_rep(target)
        bot.say("Locked rep for %s." % target)
