import json
import asyncio
import structlog

from pyrogram import Client
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from pyrogram.enums import ChatMembersFilter

logger = structlog.get_logger()

async def parsing_members(client: Client, message: Message, shared_chat: str):
    parsed_count = 0
    chat = await client.get_chat(shared_chat)
    chat_id = chat.id
    filename = f'parsed_members_{chat.id}.json'
    parsed = []
    
    my_user_id = str(message.from_user.id)
    msg = await message.edit_text(
        text=f'<b>👥 Начинаю парсинг участников чата {chat.title}...</b>',
        parse_mode=ParseMode.HTML
    )
    
    async for member in client.get_chat_members(chat_id, filter=ChatMembersFilter.SEARCH):
        full_name = (member.user.first_name or "") + (" " + member.user.last_name if member.user.last_name else "")
        
        info = {
            'full_name': full_name.strip() or 'None',
            'username': member.user.username or 'None',
            'user_id': member.user.id
        }
        parsed.append(info)
        parsed_count += 1
        
        if parsed_count % 100 == 0:
            logger.info(f'Parsed {parsed_count} members...')
            await msg.edit_text(
                text=f'<b>📊 Парсинг участников: получено [ {parsed_count} ] участников...</b>',
                parse_mode=ParseMode.HTML
            )
        
        await asyncio.sleep(0.1)
        
    with open(filename, mode='w', encoding='utf-8') as file:
        json.dump(parsed, file, ensure_ascii=False, indent=4)

    await client.send_document(
        chat_id=my_user_id,
        document=filename,
        caption=f'<b>📊 Парсинг участников чата: «{chat.title}»\n👥 Участников: [ {parsed_count} ]</b>',
        parse_mode=ParseMode.HTML
    )
        
    await msg.edit_text(
        text=f'<b>✅ Парсинг участников завершен!</b>\n\n<blockquote><b>- Чат: {chat.title}\n- Чат-ID: {chat.id}\n- Участников: {parsed_count}</b></blockquote>',
        parse_mode=ParseMode.HTML
    )

    logger.info(f'Saved {parsed_count} members in {filename}')