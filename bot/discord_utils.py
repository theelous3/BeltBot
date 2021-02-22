from functools import wraps
from bot.constants import VALID_BELTS, NON_BELTS, BET_ROLE_NAMES


def get_role_by_name(ctx, role_name):
    roles = ctx.message.guild.roles
    return next((role for role in roles if role.name == role_name), None)


async def give_user_role(ctx, member, colour):

    standard_role = True
    assignable = True

    try:
        role_name = VALID_BELTS[colour]["name"]
    except KeyError:
        role_name = NON_BELTS[colour]["name"]
        standard_role = False
        assignable = False

    role = get_role_by_name(ctx, role_name)

    if assignable:
        await member.add_roles(role)

    if standard_role:
        roles_to_remove = [role for role in member.roles if role.name in BET_ROLE_NAMES]
        await member.remove_roles(*roles_to_remove)

    return role


def check_authz(ctx, role_name):
    matching_role = get_role_by_name(ctx, role_name)
    approver_roles = ctx.author.roles

    if matching_role in approver_roles:
        return True

    return False


def requires_role(role_name):
    def bleep_bloop(coro):
        @wraps(coro)
        async def inner(ctx, *args, **kwargs):
            if check_authz(ctx, role_name):
                return await coro(ctx, *args, **kwargs)
            else:
                await ctx.send(
                    (
                        f"{ctx.author.display_name}, you don't have the permissions required"
                        f" for the command `{ctx.command.qualified_name}`."
                    )
                )

        return inner

    return bleep_bloop
