import asyncio
from time import time
import os
import sys
from pyrogram import Client, enums
from pyrogram import filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import ChatPermissions, ChatPrivileges, Message
from ANJALIMUSIC import app
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.errors import MessageDeleteForbidden, RPCError
from config import OWNER_ID

# Helper function to check if the user is bot owner or group owner
async def is_authorized(client, chat_id, user_id):
    chat_member = await client.get_chat_member(chat_id, user_id)
    return user_id == OWNER_ID or chat_member.status == enums.ChatMemberStatus.OWNER

@app.on_message(filters.command(["unbanall"], prefixes=["/", "!", "."]))
async def unbanall_command(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Check if the user is either the bot owner or the group owner
    if await is_authorized(client, chat_id, user_id):
        # Send confirmation message with buttons
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Approve", callback_data="approve_unbanall"),
                    InlineKeyboardButton("Decline", callback_data="decline_unbanall")
                ]
            ]
        )
        await message.reply_text(
            "ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜɴʙᴀɴ ᴀʟʟ ʙᴀɴɴᴇᴅ ᴜsᴇʀs? ᴏɴʟʏ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ ᴄᴀɴ ᴀᴘᴘʀᴏᴠᴇ ᴛʜɪs ᴀᴄᴛɪᴏɴ.",
            reply_markup=reply_markup
        )
    else:
        await message.reply_text("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ. ᴏɴʟʏ ᴛʜᴇ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs.")

# Callback query handler for button clicks
@app.on_callback_query(filters.regex("approve_unbanall|decline_unbanall"))
async def callback_handler(client, callback_query):
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id

    # Check if the user who clicked is either the bot owner or the group owner
    if await is_authorized(client, chat_id, user_id):
        approver_name = callback_query.from_user.first_name  # Fetch approver's name

        if callback_query.data == "approve_unbanall":
            # If approved, start the unban process
            await callback_query.message.edit_text("ᴜɴʙᴀɴᴀʟʟ ꜱᴛᴀʀᴛɪɴɢ ...")
            
            bot = await client.get_chat_member(chat_id, client.me.id)
            bot_permission = bot.privileges.can_restrict_members

            if bot_permission:
                unban_count = 0  # Counter for unbanned members
                async for member in client.get_chat_members(chat_id, filter=enums.ChatMembersFilter.BANNED):
                    try:
                        await client.unban_chat_member(chat_id, member.user.id)
                        unban_count += 1  # Increment counter for each successful unban
                    except Exception:
                        pass
                
                # Final message with the approver's name
                await callback_query.message.edit_text(
                    f"<u><b>⬤ ᴜɴʙᴀɴ ᴄᴏᴍᴘʟᴇᴛᴇᴅ!</u></b>\n\n<b>● ᴛᴏᴛᴀʟ ᴜsᴇʀs ➠</b> {unban_count}\n<b>● ᴜɴʙᴀɴɴᴇᴅ ʙʏ ➠</b> {approver_name}"
                )
            else:
                await callback_query.message.edit_text("I don't have the right to unban users or you are not in sudo users.")
        elif callback_query.data == "decline_unbanall":
            # If declined, send a cancellation message
            await callback_query.message.edit_text("ᴜʙᴀɴᴀʟʟ ᴄᴏᴍᴍᴀɴᴅ ᴡᴀs ᴅᴇᴄʟɪɴᴇᴅ.")
    else:
        # If an unauthorized user tries to click the button
        await callback_query.answer("You are not authorized to approve or decline this action.", show_alert=True)