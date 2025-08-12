"""
Author: theelous3.net
Bot config:
    Requires priviledged intent `members`.
    Requires; [
        "Manage Roles",
        "Send Messages",
        "Read Message History"
    ]
"""

__all__ = [
    "list_handler",
    "request_handler",
    "approval_handler",
    "rejection_handler",
    "moreinfo_handler",
    "review_handler",
    "unreview_handler",
    # "delete_all_handler"
]


import json
import logging
import re
import traceback
from uuid import uuid4
from re import compile
from pprint import pformat
from string import punctuation
from collections import ChainMap
from functools import wraps, partial
from contextlib import contextmanager
from datetime import datetime, timedelta

from discord.ext.commands.errors import UserInputError, CommandNotFound

from bot.bot import BOT
from bot.utils import get_now, format_requests
from bot.discord_utils import (
    requires_role,
    get_role_by_name,
    give_user_role,
    get_channel_by_name,
)
from bot.reddit import reddit_flair_user

from bot.db import (
    add_request,
    get_all_requests,
    get_request,
    update_request,
    delete_request,
    delete_all_requests,
    update_stats,
    get_stats,
)

from bot.constants import ALL_BELTS, HUMAN_READABLE_BELTS, MY_NAME


PUNCTUATION = set(punctuation)
BELT_REQUEST_REGEX = re.compile("^(?P<belt>{belts})(?P<reason>.*)".format(belts="|".join(map(re.escape, ALL_BELTS))), re.DOTALL | re.IGNORECASE)


_request_help = "Include your username in the format `/u/username_here` anywhere in the message body to be flaired on reddit!"


@BOT.command(name="request", help=_request_help)
async def request_handler(ctx, *, request):
    if ctx.message.channel.name != "belt-requests":
        await ctx.send("Only available in #belt-requests.")
        return

    match = re.match(BELT_REQUEST_REGEX, request)
    if not match:
      await ctx.send(
                f"{ctx.message.author.mention} I couldn't understand your message, the syntax is:\n"
                f"@{MY_NAME} request belt_color_goes_here any_evidence_goes_here.\n"
                f"The available belt colors are {HUMAN_READABLE_BELTS}.\n"
                 "If you mention a Reddit username anywhere in the request, that user will be flaired on reddit.",
             mention_author=True)
      return

    belt = match.group("belt")
    role_name = ALL_BELTS[belt]["name"]
    request_id = str(uuid4())[-12:]

    await ctx.send(
        f"{ctx.message.author.mention} thanks for your {role_name} request! \nID: {request_id}",
    )

    body = match.group("reason").replace("@", "")
    request = {
        "_id": request_id,
        "author": ctx.author.display_name,
        "author_id": ctx.author.id,
        "colour": belt,
        "created_at": get_now(),
        "body": body,
        "jump_url": ctx.message.jump_url,
    }

    await add_request(request)

@BOT.command(name="sync")
@requires_role("Staff")
async def sync_handler(ctx, sync):

    #Check if user in good channel
    if ctx.message.channel.name != "belt-requests":
        await ctx.send("Only available in #belt-requests.")
        return

    # Look for the belt in sync request
    match = re.match(BELT_REQUEST_REGEX, sync)
    if not match:
        await ctx.send(
                f"{ctx.message.author.mention} I couldn't understand your message, the syntax is:\n"
                f"@{MY_NAME} sync belt_color_goes_here reddit_username_goes_here.\n"
                f"The available belt colors are {HUMAN_READABLE_BELTS}.\n",
            mention_author=True)
        return
    belt = match.group("belt")
    role_name = ALL_BELTS[belt]["name"]

    # Flair the user
    flair_text = await reddit_flair_user(sync, user_roles)

    await belt_requests_channel.send(flair_text)

@BOT.command(name="list")
async def list_handler(ctx, sort="oldest"):
    if sort not in ["oldest", "newest"]:
        await ctx.send(
            (
                f"You can sort by either `oldest` or `newest`. I don't understand `{sort}`"
                "I'm going to return you the requests sorted by oldest first anyway :)"
            )
        )
        sort = "oldest"

    requests = await get_all_requests()

    if not requests:
        await ctx.send("There are no belt requests waiting for approval :D")
        return

    await ctx.send(f"Active requests:", mention_author=True)
    for formatted_request in format_requests(requests):
        await ctx.send(formatted_request, mention_author=True)


@BOT.command(name="approve")
@requires_role("Staff")
async def approval_handler(ctx, request_id, *, reason):
    request = await get_request(request_id)

    if request is None:
        await ctx.send(f"No request by id {request_id}")
        return

    member = await ctx.message.guild.fetch_member(request["author_id"])

    if member is None:
        await ctx.send(
            f"No member found. They've left the server, or have been removed."
        )
        await delete_request(request_id)
        return

    role = await give_user_role(ctx, member, request["colour"])
    if role:
        role_name = role.name
    else:
        role_name = ALL_BELTS[request["colour"]]["name"]

    logging.info(f"Processing request {request_id} for {member.mention}'s {role}")

    flair_text = await reddit_flair_user(request["body"], request["colour"])

    message = (
        f"{member.mention}, {ctx.author.mention} has reviewed and approved your request. "
        f"Congrats on your {role_name}!\n"
    )
    if reason:
        message += "\nNotes: " + "".join(reason_part for reason_part in reason)
    if flair_text:
        message += flair_text

    belt_requests_channel = get_channel_by_name(ctx, "belt-requests")

    await belt_requests_channel.send(message)

    await delete_request(request_id)

    await update_stats("belts_awarded")


@BOT.command(name="reject")
@requires_role("Staff")
async def rejection_handler(ctx, request_id, *, reason):
    request = await get_request(request_id)

    if request is None:
        await ctx.send(f"No request by id {request_id}")
        return

    if not reason:
        await ctx.send("You need to provide a reason!")
        return

    member = await ctx.message.guild.fetch_member(request["author_id"])

    if member is None:
        await ctx.send(
            f"No member found. They've left the server, or have been removed."
        )
        await delete_request(request_id)
        return

    role_name = ALL_BELTS[request["colour"]]["name"]

    belt_requests_channel = get_channel_by_name(ctx, "belt-requests")

    await belt_requests_channel.send(
        (
            f"{member.mention}, {ctx.author.mention} has reviewed and denied your request "
            f"for {role_name}."
            f"\nNotes: {''.join(reason_part for reason_part in reason)}"
        )
    )

    await delete_request(request_id)

    await update_stats("belts_to_the_glue_factory")


@BOT.command(name="delete")
@requires_role("Staff")
async def delete_handler(ctx, request_id, *, reason):
    if ctx.message.channel.name not in ("belt-requests", "bot-spam"):
        await ctx.send("Only available in #belt-requests or #bot-spam.")
        return

    request = await get_request(request_id)

    if request is None:
        await ctx.send(f"No request by id {request_id}")
        return

    if not reason:
        await ctx.send("You need to provide a reason!")
        return

    await delete_request(request_id)

    await ctx.send(
        (
            f"{ctx.author.mention} has deleted the following request: {request_id}\n"
            f"\nNotes: {''.join(reason_part for reason_part in reason)}"
        )
    )


@BOT.command(name="moreinfo")
@requires_role("Staff")
async def moreinfo_handler(ctx, request_id, *, reason):
    guild = ctx.message.guild
    request = await get_request(request_id)

    if request is None:
        await ctx.send(f"No request by id {request_id}")
        return

    if not reason:
        await ctx.send("You need to provide more information!")
        return

    member = await guild.fetch_member(request["author_id"])

    if member is None:
        await ctx.send(
            f"No member found. They've left the server, or have been removed."
        )
        await delete_request(request_id)
        return

    role_name = ALL_BELTS[request["colour"]]["name"]
    role = get_role_by_name(ctx, role_name)

    belt_requests_channel = get_channel_by_name(ctx, "belt-requests")

    await belt_requests_channel.send(
        (
            f"{member.mention}, {ctx.author.mention} has reviewed your request for"
            f" {role.name} but needs more information. Please update your"
            f" request here: {request['jump_url']}"
            f"\nNotes: {''.join(reason_part for reason_part in reason)}"
        )
    )


@BOT.command(name="review")
@requires_role("Staff")
async def review_handler(ctx, request_id):
    guild = ctx.message.guild
    request = await get_request(request_id)

    if request is None:
        await ctx.send(f"No request by id {request_id}")
        return

    member = await guild.fetch_member(request["author_id"])
    role_name = ALL_BELTS[request["colour"]]["name"]
    role = get_role_by_name(ctx, role_name)

    await ctx.send(
        (
            f"{ctx.author.mention} is reviewing `{member.display_name}`'s request for"
            f" {role.name}"
        )
    )

    await update_request(request_id, {"reviewer": ctx.author.display_name})


@BOT.command(name="unreview")
@requires_role("Staff")
async def unreview_handler(ctx, request_id):
    guild = ctx.message.guild
    request = await get_request(request_id)

    if request is None:
        await ctx.send(f"No request by id {request_id}")
        return

    member = await guild.fetch_member(request["author_id"])
    role_name = ALL_BELTS[request["colour"]]["name"]
    role = get_role_by_name(ctx, role_name)

    await ctx.send(
        (
            f"{ctx.author.mention} *stopped* the review on `{member.display_name}`'s request for"
            f" {role.name}"
        )
    )

    await update_request(request_id, {"reviewer": ""}, remove=True)


@BOT.command(name="stats")
async def stats_handler(ctx):
    stats = await get_stats()

    stats = {k["_id"]: k["count"] for k in stats}

    await ctx.send(
        f"Dump of stats:\n {pformat(stats)}",
        mention_author=True,
    )


@BOT.event
async def on_command_error(ctx, error):
    tb = traceback.format_exception(error.__class__, error, error.__traceback__)
    logging.error(tb)
    logging.error(error.__traceback__)
    if isinstance(error, CommandNotFound):
        await ctx.send("No such command. Try `@LPUBeltbot help` to see my commands :D")
    elif isinstance(error, UserInputError):
        command = ctx.invoked_with
        await ctx.send(
            f"I don't understand. Try `@LPUBeltbot help {command}` to learn more :D"
        )


# lazy debug stuff

# @BOT.command(name="delete_all", rest_is_raw=True)
# @requires_role("BeltBotMaintainer")
# async def delete_all_handler(ctx):
#     await delete_all_requests()
#     logging.info(ctx.author.roles)


@BOT.event
async def on_ready():
    logging.info("BeltBot's a ready")
    for guild in BOT.guilds:
        logging.info(f"Connected to: {guild}")
