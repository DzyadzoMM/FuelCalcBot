import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
from aiohttp import web  

from handlers.route import router

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()
dp.include_router(router)

async def handle_ping(request):
    return web.Response(text="Бот працює, порт активний! 🚀")

async def main():
    bot = Bot(token=TOKEN, default_bot_properties=DefaultBotProperties(parse_mode="HTML"))
    
    app = web.Application()
    app.router.add_get('/', handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    
    port = int(os.environ.get("PORT", 8080)) 
    site = web.TCPSite(runner, "0.0.0.0", port)
    
    asyncio.create_task(site.start())
    print(f"Фейковий веб-сервер запущено на порту: {port} 🌐")

    print("Start Bot ... 🚀")
    
    await dp.start_polling(bot)
  
if __name__ == "__main__":
    asyncio.run(main())
