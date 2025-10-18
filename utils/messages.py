import json
import asyncio

from pyrogram import Client
from pyrogram.types import Message
from pyrogram.enums import ParseMode

async def parsing_messages_handler(client: Client, message: Message, chat_input: str, limit: int):
    data = []
    parsed_count = 0
    my_user_id = str(message.from_user.id)
    
    chat = await client.get_chat(chat_input)
    chat_id = chat.id
    status_msg = await message.edit_text(
        text=f'<b>📰 Начинаю парсинг сообщений чата «{chat.title}»...</b>',
        parse_mode=ParseMode.HTML
    )
    await asyncio.sleep(2)
    
    async for msg in client.get_chat_history(chat_id=chat_id, limit=limit):
        sender = None
        if msg.from_user:
            full_name = (msg.from_user.first_name or "") + (" " + msg.from_user.last_name if msg.from_user.last_name else "")
            sender = {
                'name': full_name.strip(),
                'user_id': msg.from_user.id,
                'username': msg.from_user.username or 'None'
            }
            
        elif msg.sender_chat:
            sender = {
                'chat_title': msg.sender_chat.title,
                'id': msg.sender_chat.id
            }
            
        else:
            sender = 'Unknown sender'
            
        message_info = {
            'message_id': msg.id,
            'message_text': msg.text or 'None',
            'sender': sender,
            'date': msg.date.strftime('%Y-%m-%d %H:%M:%S')
        }
        data.append(message_info)
        
        parsed_count += 1
        
        if parsed_count % 100 == 0:
            await status_msg.edit_text(
                text=f'📊 <b>Парсинг сообщений: {parsed_count}/{limit}</b>',
                parse_mode=ParseMode.HTML
            )

    filename = f'parsed_messages_{chat.id}.json'
    with open(filename, mode='w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        
    await client.send_document(
        chat_id=my_user_id,
        document=filename,
        caption=f'<b>📰 Парсинг сообщений чата: {chat.title}\n💬 Сообщений: {parsed_count}</b>'
    )
    
    await status_msg.edit_text(
        text=f'<b>✅ Парсинг сообщений завершен!</b>\n\n<blockquote><b>- Чат: {chat.title}\n- Лимит: {limit}\n- Сообщений: {parsed_count}</b></blockquote>',
        parse_mode=ParseMode.HTML
    )