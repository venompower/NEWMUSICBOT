import asyncio
from pyrogram import Client, enums
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import OWNER_ID
from ANJALIMUSIC import app

@app.on_message(filters.command(["banall"], prefixes=["/", "!", ".", ","]))
async def banall_command(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Get the status of the user in the group (owner or not)
    chat_member = await client.get_chat_member(chat_id, user_id)

    # Check if the user is either the bot owner or the group owner
    if user_id == OWNER_ID or chat_member.status == enums.ChatMemberStatus.OWNER:
        # Send approval request with buttons
        await message.reply_text(
            "ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ sᴛᴀʀᴛ ᴛʜᴇ ᴅᴀɴᴀʟʟ ᴘʀᴏᴄᴇss? ᴏɴʟʏ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ ᴄᴀɴ ᴀᴘᴘʀᴏᴠᴇ ᴛʜɪs ᴀᴄᴛɪᴏɴ.",
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("ᴀᴘᴘʀᴏᴠᴇ", callback_data="approve_banall"),
                    InlineKeyboardButton("ᴅᴇᴄʟɪɴᴇ", callback_data="decline_banall")
                ]]
            )
        )
    else:
        await message.reply_text("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ. ᴏɴʟʏ ᴛʜᴇ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs.")

@app.on_callback_query(filters.regex("approve_banall"))
async def approve_banall(client, callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.first_name

    # Get the status of the user to check if they are authorized
    chat_member = await client.get_chat_member(chat_id, user_id)

    if user_id == OWNER_ID or chat_member.status == enums.ChatMemberStatus.OWNER:
        await callback_query.message.edit_text(f"ʙᴀɴᴀʟʟ ꜱᴛᴀʀᴛɪɴɢ ... ᴀᴘᴘʀᴏᴠᴇᴅ ʙʏ {user_name}.")

        bot = await client.get_chat_member(chat_id, client.me.id)
        bot_permission = bot.privileges.can_restrict_members

        if bot_permission:
            ban_count = 0  # Initialize ban count
            async for member in client.get_chat_members(chat_id):
                try:
                    await client.ban_chat_member(chat_id, member.user.id)
                    ban_count += 1  # Increment ban count for each ban
                except Exception:
                    pass
            await callback_query.message.edit_text(f"<b><u>⬤ ʙᴀɴᴀʟʟ ᴘʀᴏᴄᴇss ᴄᴏᴍᴘʟᴇᴛᴇᴅ!</b></u>\n\n<b>● ᴛᴏᴛᴀʟ ᴜsᴇʀs ➠</b> {ban_count}\n<b>● ʙᴀɴɴᴇᴅ ʙʏ ➠</b> {user_name}")
        else:
            await callback_query.message.edit_text("ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ʀɪɢʜᴛ ᴛᴏ ʀᴇsᴛʀɪᴄᴛ ᴜsᴇʀs ᴏʀ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ɪɴ sᴜᴅᴏ ᴜsᴇʀs.")
    else:
        await callback_query.message.edit_text(f"{user_name}, ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴀᴘᴘʀᴏᴠᴇ ᴛʜɪs ᴀᴄᴛɪᴏɴ.")

@app.on_callback_query(filters.regex("decline_banall"))
async def decline_banall(client, callback_query: CallbackQuery):
    user_name = callback_query.from_user.first_name
    await callback_query.message.edit_text(f"</b>ʙᴀɴᴀʟʟ ᴘʀᴏᴄᴇss ʜᴀs ʙᴇᴇɴ ᴄᴀɴᴄᴇʟᴇᴅ ʙʏ</b> {user_name}.")