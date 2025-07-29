"""
Part of sopel-rep

Copyright 2024 dgw, technobabbl.es
"""
from __future__ import annotations

import re
import time
from typing import TYPE_CHECKING

from .errors import ArgumentError, CooldownError, NonexistentNickError

if TYPE_CHECKING:
    from sopel.bot import Sopel
    from sopel.config.types import StaticSection
    from sopel.tools.identifiers import Identifier
    from sopel.trigger import Trigger


r_nick = r'[a-zA-Z0-9\[\]\\`_\^\{\|\}-]{1,32}'


class RepManager:
    """Manager of reputation actions."""

    SCORE_KEY = 'rep_score'
    USED_KEY = 'rep_used'
    LOCKED_KEY = 'rep_locked'

    def __init__(self, bot: Sopel):
        """Construct a new RepManager.

        :param bot: The Sopel instance under which this plugin is running
        """
        self.sopel = bot

    @property
    def settings(self) -> StaticSection:
        return self.sopel.settings.rep

    def get_rep(self, nick: str) -> int:
        return self.sopel.db.get_nick_value(nick, self.SCORE_KEY) or 0

    def set_rep(self, nick: str, value: int):
        self.sopel.db.set_nick_value(nick, self.SCORE_KEY, value)

    def change_rep(self, nick: str, delta: int) -> int:
        rep = self.get_rep(nick)
        rep += delta
        self.set_rep(nick, rep)
        return rep

    def lock_rep(self, nick: str):
        self.sopel.db.set_nick_value(nick, self.LOCKED_KEY, True)

    def unlock_rep(self, nick: str):
        self.sopel.db.set_nick_value(nick, self.LOCKED_KEY, False)

    def is_rep_locked(self, nick: str) -> bool:
        return self.sopel.db.get_nick_value(nick, self.LOCKED_KEY) or False

    def get_rep_used(self, nick: str) -> float:
        return self.sopel.db.get_nick_value(nick, self.USED_KEY) or 0

    def set_rep_used(self, nick: str):
        self.sopel.db.set_nick_value(nick, self.USED_KEY, time.time())

    def remaining_cooldown(self, nick: str) -> float | None:
        now = time.time()
        then = self.get_rep_used(nick)
        elapsed = now - then
        cooldown = self.settings.cooldown

        if cooldown > elapsed:
            return cooldown - elapsed
        return None

    def nick_is_alias(self, nick1: str, nick2: str) -> bool:
        nick1 = self.sopel.make_identifier(nick1)
        nick2 = self.sopel.make_identifier(nick2)

        if nick1 == nick2:
            # Shortcut to catch common goofballs without hitting the DB
            return True

        try:
            id1 = self.sopel.db.get_nick_id(nick1, False)
            id2 = self.sopel.db.get_nick_id(nick2, False)
        except ValueError:
            # If either nick doesn't have an ID, it can't be in a group
            return False

        return id1 == id2

    def verified_nick(self, nick: str, channel: str) -> Identifier:
        """Make sure the given `nick` is present in the given `channel`.

        Also performs normalization, casting plain `str` to `Identifier`.
        """
        if not all((nick, channel)):
            # verification should immediately fail if either the `nick` or the
            # `channel` is falsy. This function always returns '' instead of
            # None if verification fails, to avoid breaking `==` comparisons
            return ''

        nick = re.search(r_nick, nick).group(0)
        if not nick:
            return ''

        if nick not in self.sopel.channels[channel].users:
            if nick.endswith('--'):
                if nick[:-2] in self.sopel.channels[channel].users:
                    return self.sopel.make_identifier(nick[:-2])
            return ''

        return self.sopel.make_identifier(nick)

    def luv_or_h8(
        self,
        trigger: Trigger,
        target: str,
        which: str,  # nominally, either 'luv' or 'h8'
    ) -> str:
        """Do the stuff and return what the bot should say.

        `ArgumentError` value is meant to be sent as a bot reply.

        `CooldownError.remaining_time` is meant to be used in a bot notice.
        """
        caller = trigger.nick
        channel = trigger.sender
        target = self.verified_nick(target, channel)
        which = which.lower()  # issue #18

        if not target:
            raise NonexistentNickError(
                "You can only {} someone who is here.".format(which))

        remains = self.remaining_cooldown(caller)
        if (
            remains and not (
                trigger.admin and not self.settings.admin_cooldown)
        ):
            raise CooldownError(remains)

        selfreply = verb = delta = None
        if which == 'luv':
            selfreply = "No narcissism allowed!"
            verb, delta = 'increased', 1
        elif which == 'h8':
            selfreply = "Go to 4chan if you really hate yourself!"
            verb, delta = 'decreased', -1
        else:
            raise RuntimeError("Invalid `which`: {!r}.".format(which))

        if self.nick_is_alias(caller, target):
            raise ArgumentError(selfreply)

        possessive = 'my' if target == self.sopel.nick else target + "'s"
        if self.is_rep_locked(target):
            raise ArgumentError(
                "Sorry, {} reputation has been locked by an admin."
                .format(possessive)
            )

        new_rep = self.change_rep(target, delta)
        self.set_rep_used(caller)
        return "{who} has {change} {whose} reputation score to {what}.".format(
            who=caller,
            change=verb,
            whose=possessive,
            what=new_rep,
        )
