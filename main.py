import structlog
from pystyle import (
    Colors, 
    Colorate, 
    Center
)

from config import Config
from utils import members
from utils import messages

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode


API_ID = Config.API_ID
API_HASH = Config.API_HASH

app = Client('session', API_ID, API_HASH)
logger = structlog.get_logger()

text_banner = '''
██╗     ██╗   ██╗███╗   ███╗██╗███████╗██╗ █████╗ 
██║     ██║   ██║████╗ ████║██║██╔════╝██║██╔══██╗
██║     ██║   ██║██╔████╔██║██║███████╗██║███████║
██║     ██║   ██║██║╚██╔╝██║██║╚════██║██║██╔══██║
███████╗╚██████╔╝██║ ╚═╝ ██║██║███████╗██║██║  ██║
╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚══════╝╚═╝╚═╝  ╚═╝
'''

# ==================== ПАРСИНГ УЧАСТНИКОВ ====================

@app.on_message(filters.command('parse_members') & filters.me)
async def parse_members_cmd(client: Client, message: Message):

    args = message.text.split()
    if len(args) < 2:
        await message.edit_text(
            text='<b>🆘 Используйте: /parse_members [chat_link_or_id]</b>\n\n<b># Пример:</b>\n<blockquote>/parse_members @chatname</blockquote>\n<blockquote>/parse_members -100000000</blockquote>'
        )
        return
    
    chat = str(args[1])
    await members.parsing_members(client, message, chat)

# ==================== ПАРСИНГ СООБЩЕНИЙ ====================

@app.on_message(filters.command('parse_messages') & filters.me)
async def parse_messages_cmd(client: Client, message: Message):
    args = message.text.split()
    
    if len(args) < 3:
        await message.edit_text(
            text='<b>🆘 Используйте: /parse_messages [chat_link_or_id] [limit]</b>\n\n<b># Пример:</b>\n<blockquote>/parse_messages @chatname 1000</blockquote>\n<blockquote>/parse_messages -100000000 500</blockquote>'
        )
        return
    
    chat_id = args[1]
    limit = int(args[2])
    
    await messages.parsing_messages_handler(client, message, chat_id, limit)

# ==================== ОБЩАЯ КОМАНДА ПОМОЩИ ====================

@app.on_message(filters.command('parse_help') & filters.me)
async def parse_help_cmd(client: Client, message: Message):
    help_text = '''
<b>🛠 Доступные команды парсинга:</b>

<code>/parse_members [чат]</code> - Парсинг участников
<code>/parse_messages [чат] [лимит]</code> - Парсинг сообщений

<b>📝 Примеры:</b>
<code>/parse_members @chatname</code>
<code>/parse_members -100000000</code>
<code>/parse_messages @chatname 1000</code>
<code>/parse_messages -100000000 500</code>

<b>⚡ Результаты автоматически отправляются в чат «Избранное».</b>
'''
    await message.edit_text(help_text, parse_mode=ParseMode.HTML)

def main():
    print(Colorate.Horizontal(Colors.blue_to_cyan, Center.XCenter(text_banner)))
    print(Colorate.Horizontal(Colors.blue_to_cyan, Center.XCenter('LUMIS USERBOT | Use /parse_help in telegram...')))
    app.run()

if __name__ == '__main__':
    main()