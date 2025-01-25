import requests
import random
from ANJALIMUSIC import app, userbot
from ANJALIMUSIC.misc import SUDOERS
from pyrogram import * 
from pyrogram.types import *
from ANJALIMUSIC.utils.anjali_ban import admin_filter
from config import OWNER_ID
from pyrogram.types import ChatPrivileges
from pyrogram.errors import RPCError






Yumikoo_text = [
"hey please don't disturb me.",
"who are you",    
"aap kon ho",
"aap mere owner to nhi lgte ",
"hey tum mera name kyu le rhe ho meko sone do",
"ha bolo kya kaam hai ",
"dekho abhi mai busy hu ",
"hey i am busy",
"aapko smj nhi aata kya ",
"leave me alone",
"dude what happend",    
]

strict_txt = [
"i can't restrict against my besties",
"are you serious i am not restrict to my friends",
"fuck you bsdk k mai apne dosto ko kyu kru",
"hey stupid admin ", 
"ha ye phele krlo maar lo ek dusre ki gwaand",  
"i can't hi is my closest friend",
"i love him please don't restict this user try to usertand "
]

boss_txt = [
    "Arrey Boss Aap Yha 🤩",
    "Hello Master !",
    "Kaise Ho Master ?",
    "Welcome Master !",
    "Darling Tum Yha 🤩"
]

full_promote = [
    "Kaise Ho Master ? Mai Yha Hu !",
    "Aapke Dil Me Master.. 😉",
    "Yess Boss !"
]

bot_leave_txt = [
    "Ok Boss Jaa Rhi Hu Yha Se... 😥",
    "I leaving group TC all 😔",
    "Jaisa Aap Bole !"
]


 
ban = ["ban","boom", "laura"]
unban = ["unban", "gpay"]
mute = ["mute","silent","shut", "chup"]
unmute = ["unmute","speak","free", "bolne"]
kick = ["kick", "out","nikaal","nikal", "nikal"]
promote = ["promote","adminship"]
fullpromote = ["fullpromote","fulladmin", "baby"]
demote = ["demote","lelo"]
group = ["group"]
channel = ["channel"]
botleave = ["leave","nikal"]
dlt = ["delete", "dlt"]



# ========================================= #


@app.on_message(filters.command(["iri", "arling", "aan"], prefixes=["s", "S", "d", "D", "j", "J"]) & SUDOERS)
async def restriction_app(app :app, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    if len(message.text) < 2:
        return await message.reply(random.choice(Yumikoo_text))
    bruh = message.text.split(maxsplit=1)[1]
    data = bruh.split(" ")
    
    if reply:
        user_id = reply.from_user.id
        for banned in data:
            print(f"present {banned}")
            if banned in ban:
                if user_id in SUDOERS:
                    await message.reply(random.choice(strict_txt))          
                else:
                    await app.ban_chat_member(chat_id, user_id)
                    await message.reply("OK, Ban kar diya madrchod ko sala Chutiya tha !")
                    
        for unbanned in data:
            print(f"present {unbanned}")
            if unbanned in unban:
                await app.unban_chat_member(chat_id, user_id)
                await message.reply(f"Ok, aap bolte hai to unban kar diya") 
                
        for kicked in data:
            print(f"present {kicked}")
            if kicked in kick:
                if user_id in SUDOERS:
                    await message.reply(random.choice(strict_txt))
                
                else:
                    await app.ban_chat_member(chat_id, user_id)
                    await app.unban_chat_member(chat_id, user_id)
                    await message.reply("get lost! bhga diya bhosdi wale ko") 
                    
        for muted in data:
            print(f"present {muted}") 
            if muted in mute:
                if user_id in SUDOERS:
                    await message.reply(random.choice(strict_txt))
                
                else:
                    permissions = ChatPermissions(can_send_messages=False)
                    await message.chat.restrict_member(user_id, permissions)
                    await message.reply(f"muted successfully! Disgusting people.") 
                    
        for unmuted in data:
            print(f"present {unmuted}")            
            if unmuted in unmute:
                permissions = ChatPermissions(can_send_messages=True)
                await message.chat.restrict_member(user_id, permissions)
                await message.reply(f"Huh, OK, sir!")   


        for promoted in data:
            print(f"present {promoted}")            
            if promoted in promote:
                await app.promote_chat_member(chat_id, user_id, privileges=ChatPrivileges(
                    can_change_info=False,
                    can_invite_users=True,
                    can_delete_messages=True,
                    can_restrict_members=False,
                    can_pin_messages=True,
                    can_promote_members=False,
                    can_manage_chat=True,
                    can_manage_video_chats=True,
                       )
                     )
                await message.reply("promoted !")

        for demoted in data:
            print(f"present {demoted}")            
            if demoted in demote:
                await app.promote_chat_member(chat_id, user_id, privileges=ChatPrivileges(
                    can_change_info=False,
                    can_invite_users=False,
                    can_delete_messages=False,
                    can_restrict_members=False,
                    can_pin_messages=False,
                    can_promote_members=False,
                    can_manage_chat=False,
                    can_manage_video_chats=False,
                       )
                     )
                await message.reply("demoted !")


#async def your_function():
    for fullpromoted in data:
        print(f"present {fullpromoted}")            
        if fullpromoted in fullpromote:
            await app.promote_chat_member(chat_id, user_id, privileges=ChatPrivileges(
                can_change_info=True,
                can_invite_users=True,
                can_delete_messages=True,
                can_restrict_members=True,
                can_pin_messages=True,
                can_promote_members=True,
                can_manage_chat=True,
                can_manage_video_chats=True,
               )
             )
            await message.reply("fullpromoted !")

    #leave bot
    for botleaved in data:
        if botleaved in botleave:
            if message.from_user.id != OWNER_ID:
                return await message.reply_text("ʙʜᴀɢ ʙᴇʜᴀɴᴄʜᴏᴅ .")
            else:
                await message.reply_text(random.choice(bot_leave_txt))
                await app.leave_chat(message.chat.id)


    # Deleting the replied message if a trigger word is found
    for delete in data:
        print(f"present {delete}")
        if delete in dlt:  # Assuming `dlt` contains the trigger words
            if user_id in SUDOERS:
                await message.reply(random.choice(strict_txt))
            else:
                try:
                    await reply.delete()  # Deletes the replied message
                except Exception as e:
                    print(f"Failed to delete the message. Error: {e}")
                return