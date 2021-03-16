# ported by @Kakashi_HTK/@ashwinstr

from pyrogram import filters
from pyrogram.errors import FloodWait

from userge import Config, Message, userge

RECENT_PM = None
COUNT = 0


@userge.on_message(filters.group & ~filters.bot & ~filters.me)
async def grp_log(_, message: Message):
    if not Config.PM_LOG_GROUP_ID:
        return
    me = await userge.get_me()
    id = message.message_id
    reply = message.reply_to_message
    log = f"""
#TAGS
<b>Sent by :</b> {message.from_user.mention}
<b>Group :</b> <code>{message.chat.title}</code>
<b>Message link :</b> <a href={message.link}>link</a>
<b>Message :</b> ⬇
"""
    if reply:
        replied = reply.from_user.id
        if replied == me.id:
            try:
                await userge.send_message(
                    Config.PM_LOG_GROUP_ID,
                    log,
                    parse_mode="html",
                    disable_web_page_preview=True,
                )
                await userge.forward_messages(
                    Config.PM_LOG_GROUP_ID, message.chat.id, message_ids=id
                )
            except FloodWait as e:
                await asyncio.sleep(e.x + 3)
    if ("@" + me.username) in message.text:
        try:
            await userge.send_message(
                Config.PM_LOG_GROUP_ID,
                log,
                parse_mode="html",
                disable_web_page_preview=True,
            )
            await userge.forward_messages(
                Config.PM_LOG_GROUP_ID, message.chat.id, message_ids=id
            )
        except FloodWait as e:
            await asyncio.sleep(e.x + 3)


@userge.on_message(filters.private, ~filters.bot)
async def pm_log(_, message: Message):
    chat_id = message.chat.id
    chat = await userge.get_chat(chat_id)
    chat_name = " ".join([chat.first_name, chat.last_name or ""])
    id = message.message_id
    if not Config.PM_LOG_GROUP_ID:
        return
    log1 = f"""
👤 [{chat_name}](tg://user?id={chat_id}) sent a new message.
#⃣ <b>ID : </b><code>{chat_id}</code>
✉ <b>Message :</b> ⬇
"""
    log2 = f"""
<b>#Conversation</b> with:
👤 [{chat_name}](tg://user?id={chat_id})
✉ <b>Message :</b> ⬇
"""
    try:
        await userge.send_message(
            Config.PM_LOG_GROUP_ID, log2, disable_web_page_preview=True
        )
        await userge.forward_messages(
            Config.PM_LOG_GROUP_ID,
            chat_id,
            id,
            parse_mode="html",
            disable_notification=True,
        )
    except FloodWait as e:
        await asyncio.sleep(e.x + 3)

    global RECENT_USER
    global COUNT
    if RECENT_USER != u_id or COUNT > 4:
        RECENT_USER = u_id
        try:
            await userge.send_message(
                Config.PM_LOG_GROUP_ID,
                log1,
                parse_mode="html",
                disable_web_page_preview=True,
            )
            await userge.forward_messages(
                Config.PM_LOG_GROUP_ID, chat_id, id, disable_notification=True
            )
        except FloodWait as e:
            await asyncio.sleep(e.x + 3)


#     COUNT = 0
# else:
#     try:
#         await userge.send_message(
#             Config.PM_LOG_GROUP_ID, log2, disable_web_page_preview=True
#         )
#         await userge.forward_messages(
#             Config.PM_LOG_GROUP_ID,
#             chat,
#             id,
#             parse_mode="html",
#             disable_notification=True,
#         )
#     except FloodWait as e:
#         await asyncio.sleep(e.x + 3)
# COUNT += 1
