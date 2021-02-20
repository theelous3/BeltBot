from functools import wraps


def get_role_by_name(ctx, role_name):
    roles = ctx.message.guild.roles
    return next((role for role in roles if role.name == role_name), None)


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
