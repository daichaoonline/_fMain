import os
import shutil
import asyncio
import time
import yt_dlp
from dataclasses import dataclass
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

@dataclass
class LinkExtractor:
    output_dir: str = 'links'

    def extract_username(self, url):
        url = url.rstrip('/')
        if '@' in url:
            return url.split('@')[-1].split('/')[0]
        elif 'channel/' in url:
            return url.split('channel/')[-1].split('/')[0]
        else:
            return url.split('/')[-1].split('?')[0]

    async def process_url(self, url):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        ydl_opts = {'extract_flat': True, 'quiet': True}

        try:
            loop = asyncio.get_event_loop()
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=False))
                
                if info_dict and 'entries' in info_dict:
                    video_urls = [entry['url'] for entry in info_dict['entries'] if entry.get('url')]
                    if not video_urls: return None, "No videos found."

                    username = self.extract_username(url)
                    output_file = os.path.join(self.output_dir, f"{username}.txt")
                    
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write("\n".join(video_urls))
                    
                    return output_file, len(video_urls)
                return None, "No entries found."
        except Exception as e:
            return None, str(e)

async def update_timer(message, start_time, stop_event):
    index = 0
    while not stop_event.is_set():
        elapsed_time = int(time.time() - start_time)
        bar = ["□"] * 5
        bar[index % 5] = "■"
        progress_str = "".join(bar)
        index += 1
        
        try:
            await message.edit_text(
                f"⚡ **Scraping in progress...**\n"
                f"📂 Status: `[{progress_str}]` Scanning\n"
                f"⏱ Time: `{elapsed_time}s`"
            )
        except Exception:
            pass 
        await asyncio.sleep(1.5)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 **Link Extractor Bot**\n\nPaste a TikTok/YouTube profile link to start.\n\n/clear - Wipe server files")

async def clear_directory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    folder = 'links'
    if os.path.exists(folder):
        shutil.rmtree(folder)
        os.makedirs(folder)
        await update.message.reply_text("🧹 **Links folder cleared!**")
    else:
        await update.message.reply_text("Folder is already empty.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_url = update.message.text.strip()
    if not user_url.startswith("http"):
        await update.message.reply_text("❌ Please send a valid URL.")
        return

    start_time = time.time()
    status_msg = await update.message.reply_text("⏳ Initializing...")
    stop_event = asyncio.Event()
    timer_task = asyncio.create_task(update_timer(status_msg, start_time, stop_event))
    
    try:
        extractor = LinkExtractor()
        file_path, result = await extractor.process_url(user_url)

        stop_event.set()
        await timer_task 

        if file_path:
            total_time = int(time.time() - start_time)
            with open(file_path, 'rb') as document:
                await context.bot.send_document(
                    chat_id=update.effective_chat.id,
                    document=document,
                    caption=(
                        f"✅ **Extraction Complete**\n"
                        f"━━━━━━━━━━━━━━━\n"
                        f"📊 **Links found:** `{result}`\n"
                        f"⏱ **Total time:** `{total_time}s`"
                    ),
                    read_timeout=60
                )
        else:
            await update.message.reply_text(f"❌ **Error:** {result}")
            
    finally:
        stop_event.set()
        try:
            await status_msg.delete()
        except:
            pass

if __name__ == '__main__':
    TOKEN = '8594266876:AAG7CN60Qf2ngmlCwNiRWe39L4uarSgTDUs'
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("clear", clear_directory))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()