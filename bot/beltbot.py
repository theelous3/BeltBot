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
    "delete_all_handler"
]


import json
import logging
import traceback
from uuid import uuid4
from re import compile
from copy import deepcopy
from functools import wraps, partial
from contextlib import contextmanager
from datetime import datetime, timedelta


from discord.utils import get as discord_find
from discord.ext.commands.errors import UserInputError, CommandNotFound

from bot.bot import BOT
from bot.utils import suppress_exceptions, get_now, format_requests
from bot.discord_utils import requires_role, get_role_by_name
from bot.reddit import reddit_flair_user

from bot.db import (
    add_request,
    get_all_requests,
    get_request,
    update_request,
    delete_request,
    delete_all_requests
)

from bot.constants import(
    VALID_BELTS,
    SPECIAL_REQUESTS,
    HUMAN_READABLE_BELTS
)


_request_help = "Include your username in the format `/u/username_here` anywhere in the message body to be flaired on reddit!"


@BOT.command(name="request", help=_request_help)
async def request_handler(ctx, colour, spacer, *body):
    if colour not in VALID_BELTS:
        await ctx.send(
            (
                f"{ctx.message.author.mention} I don't think {colour} is a real belt :( \n"
                f"Try one of these: {HUMAN_READABLE_BELTS}"
            ),
            mention_author=True,
        )
        return

    await ctx.send(
        f"{ctx.message.author.mention} thanks for your {VALID_BELTS[colour]['name']} request!",
        mention_author=True,
    )

    body = " ".join(body) or ""
    body = body.replace("@", "")
    request = {
        "_id": str(uuid4())[-12:],
        "author": ctx.author.display_name,
        "author_id": ctx.author.id,
        "colour": colour,
        "created_at": get_now(),
        "body": body,
        "jump_url": ctx.message.jump_url,
    }

    await add_request(request)


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

    await ctx.send(
        f"Active requests:\n\n{format_requests(requests)}",
        mention_author=True,
    )


@BOT.command(name="approve")
@requires_role("Mods")
async def approval_handler(ctx, request_id, *reason):
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

    role_name = VALID_BELTS[request["colour"]]["name"]

    try:
        role = get_role_by_name(ctx, role_name)
        await member.add_roles(role)
    except AttributeError:
        role = SPECIAL_REQUESTS[request["colour"]]

    flair_text = await reddit_flair_user(request["body"], request["colour"])

    message = (
        f"{member.mention}, {ctx.author.mention} has reviewed and approved your request. "
        f"Congrats on your {role.name}!"
    )
    if reason:
        message += " ".join(reason_part for reason_part in reason)
    if flair_text:
        message += flair_text

    await ctx.send(message)

    await delete_request(request_id)


@BOT.command(name="reject")
@requires_role("Mods")
async def rejection_handler(ctx, request_id, *reason):
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

    role_name = VALID_BELTS[request["colour"]]["name"]
    role = get_role_by_name(ctx, role_name)

    await ctx.send(
        (
            f"{member.mention}, {ctx.author.mention} has reviewed and denied your request "
            f"for {role.name}."
            f"\nNotes: {' '.join(reason_part for reason_part in reason)}"
        )
    )

    await delete_request(request_id)


@BOT.command(name="moreinfo")
@requires_role("Mods")
async def moreinfo_handler(ctx, request_id, *reason):
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

    role_name = VALID_BELTS[request["colour"]]["name"]
    role = get_role_by_name(ctx, role_name)

    await ctx.send(
        (
            f"{member.mention}, {ctx.author.mention} has reviewed your request for"
            f" {role.name} but needs more information. Please update your"
            f" request here: {request['jump_url']}"
            f"\nNotes: {' '.join(reason_part for reason_part in reason)}"
        )
    )


@BOT.command(name="review")
@requires_role("Mods")
async def review_handler(ctx, request_id):
    guild = ctx.message.guild
    request = await get_request(request_id)

    if request is None:
        await ctx.send(f"No request by id {request_id}")
        return

    member = await guild.fetch_member(request["author_id"])
    role_name = VALID_BELTS[request["colour"]]["name"]
    role = get_role_by_name(ctx, role_name)

    await ctx.send(
        (
            f"{ctx.author.mention} is reviewing `{member.display_name}`'s request for"
            f" {role.name}"
        )
    )

    await update_request(request_id, {"reviewer": ctx.author.display_name})


@BOT.command(name="unreview")
@requires_role("Mods")
async def unreview_handler(ctx, request_id):
    guild = ctx.message.guild
    request = await get_request(request_id)

    if request is None:
        await ctx.send(f"No request by id {request_id}")
        return

    member = await guild.fetch_member(request["author_id"])
    role_name = VALID_BELTS[request["colour"]]["name"]
    role = get_role_by_name(ctx, role_name)

    await ctx.send(
        (
            f"{ctx.author.mention} *stopped* the review on `{member.display_name}`'s request for"
            f" {role.name}"
        )
    )

    await update_request(request_id, {"reviewer": ""}, remove=True)


@suppress_exceptions
@BOT.command(name="delete_all", rest_is_raw=True)
@requires_role("BeltBotMaintainer")
async def delete_all_handler(ctx):
    await delete_all_requests()


@BOT.event
async def on_command_error(ctx, error):
    tb = traceback.format_exception(error.__class__, error, error.__traceback__)
    logging.error(tb)
    logging.error(error.__traceback__)
    if isinstance(error, CommandNotFound):
        await ctx.send("No such command. Try `@LPUBeltbot help` to see my commands :D")
    elif isinstance(error, UserInputError):
        command = ctx.invoked_with
        await ctx.send(f"I don't understand. Try `@LPUBeltbot {command}` to learn more :D")


@BOT.event
async def on_ready():
    logging.info("BeltBot's a ready")
    for guild in BOT.guilds:
        logging.info(f"Connected to: {guild}")
