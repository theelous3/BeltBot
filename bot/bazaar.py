from bot.bot import BOT
from bot.db import update_stats


BAZAAR_PREFIXES = ["wtb", "wts", "wtt", "http://", "https://"]


async def bazaar_on_message_wtb_wts(message):
    if message.channel.name == "lock-bazaar":
        delete = False
        delete_self = False

        content = message.content.lstrip().casefold()

        if message.author != BOT.user:
            if not any(
                content.startswith(bazaar_prefix) for bazaar_prefix in BAZAAR_PREFIXES
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

                await message.author.send(
                    "The following message was deleted from #lock-bazaar. Only posts prefixed"
                    " with WTB/WTS or that are a direct link, are allowed there. You can discuss buy"
                    " and sell orders in #lock-bazaar-chat."
                    f"\n```{message.content}```"
                )
        else:
            type_ = next(
                prefix for prefix in BAZAAR_PREFIXES if content.startswith(prefix)
            )
            await update_stats(type_)
