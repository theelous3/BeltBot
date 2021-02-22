from bot.bot import BOT


async def bazaar_on_message(message):

    if message.channel.name == "lol-memes":
        delete = False
        delete_self = False

        content = message.content.lstrip().casefold()

        if message.author != BOT.user:
            if not any(
                content.startswith(bazaar_prefix) for bazaar_prefix in ["wtb", "wts"]
            ):
                delete = True
        else:
            if not content.endswith(":moneybag:"):
                delete = True
                delete_self = True

        if delete:
            await message.delete()
            if not delete_self:
                await message.channel.send(
                    content=(
                        f"{message.author.mention} :bomb: Chat is not allowed in #lock-bazaar. Please use "
                        f"#lock-bazaar-chat."
                        f"\nIf you want to buy or sell, start your message with WTB or WTS. :moneybag:"
                    ),
                    delete_after=10.0,
                )
