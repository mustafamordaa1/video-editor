from telegram import *
from telegram.ext import *
import os
import json
from methods import edit_video, YTdownload, cut_video


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Welcome Sir! Just send me a video and You'll see")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg_id = update.message.id
    user_id = update.message.from_user.id
    video_id = update.message.video.file_id
    file = await context.bot.get_file(video_id)
    await file.download_to_drive(custom_path=f'{user_id}.mp4')

    try:
        with open('users_data.json', 'r', encoding='utf-8') as outfile:
            data = json.load(outfile)

        index = 0
        for i in data:
            if i["id"] == user_id:
                data.pop(index)
                with open('users_data.json', 'w', encoding='utf-8') as outfile:
                    json_data = json.dump(data, outfile, indent=4)
            index +=1

    except FileNotFoundError:
        data = []

    data.append({"id": user_id, "cutSilence":0, "19:6": 0, "speedup": 0, "music": 0 })
    with open('users_data.json', 'w', encoding='utf-8') as outfile:
        json_data = json.dump(data, outfile, indent=4)

    buttons = [[InlineKeyboardButton('إزالة الفراغات', callback_data=f'{msg_id+1}&cutSilence')], [InlineKeyboardButton('تحويل المقطع طولياً', callback_data=f'{msg_id+1}&19:6')],
                [InlineKeyboardButton('تسريع المقطع ل58 ثانية', callback_data=f'{msg_id+1}&speedup')], [InlineKeyboardButton('اضافة موسيقا تصويرية', callback_data=f'{msg_id+1}&music')], [InlineKeyboardButton('تأكيد', callback_data=f'{msg_id+1}&done')]]
    await update.message.reply_text("اختر الخيارات التي تريد تطبيقها ثم اضغط على تأكيد", reply_markup = InlineKeyboardMarkup(buttons))
    
async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = user_id = update.message.from_user.id
    link = user_id = update.message.text
    file = YTdownload(user_id, link)

    if file:
        file = edit_video(file, 1, 0, 0, 0)
        await update.message.reply_text(text="Done!")
        await update.message.reply_document(document=file)
        os.remove(f'{file}')
    


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id =  update.callback_query.message.chat.id
    query = update.callback_query.data.split('&')
    msg_id, request_type = int(query[0]), query[1]

    try:
        index = 0

        with open('users_data.json', 'r', encoding='utf-8') as outfile:
            data = json.load(outfile)
        
        for i in data:
            if i["id"] == user_id:
                break

            index += 1
            
    except FileNotFoundError:
        data = []

        return 0

    if request_type == 'cutSilence':
        data[index]["cutSilence"] = 1
    elif request_type == '19:6':
        data[index]["19:6"] = 1
    elif request_type == 'speedup':
        data[index]["speedup"] = 1
    elif request_type == 'music':
        data[index]["music"] = 1

    with open('users_data.json', 'w', encoding='utf-8') as outfile:
        json_data = json.dump(data, outfile, indent=4)


    added = []
    buttons = [[InlineKeyboardButton('إزالة الفراغات', callback_data=f'{msg_id}&cutSilence')], [InlineKeyboardButton('تحويل المقطع طولياً', callback_data=f'{msg_id}&19:6')],
                [InlineKeyboardButton('تسريع المقطع ل58 ثانية', callback_data=f'{msg_id}&speedup')], [InlineKeyboardButton('اضافة موسيقا تصويرية', callback_data=f'{msg_id}&music')], [InlineKeyboardButton('تأكيد', callback_data=f'{msg_id}&done')]]
    if data[index]["cutSilence"]:
        added.append('-إزالة الفراغات')
        buttons.remove([InlineKeyboardButton('إزالة الفراغات', callback_data=f'{msg_id}&cutSilence')])
    if data[index]["19:6"]:
        added.append('-تحويل المقطع طولياً')
        buttons.remove([InlineKeyboardButton('تحويل المقطع طولياً', callback_data=f'{msg_id}&19:6')])
    if data[index]["speedup"]:
        added.append('-تسريع المقطع ل58 ثانية')
        buttons.remove([InlineKeyboardButton('تسريع المقطع ل58 ثانية', callback_data=f'{msg_id}&speedup')])
    if data[index]["music"]:
        added.append('-اضافة موسيقا تصويرية')
        buttons.remove([InlineKeyboardButton('اضافة موسيقا تصويرية', callback_data=f'{msg_id}&music')])

    await context.bot.edit_message_text(chat_id=user_id, message_id=msg_id, text=f"الخيارات التي اخترتها:({' - '.join(added)}) اضغط على تأكيد عندما تنتهي من الاختيار..")
    await context.bot.edit_message_reply_markup(chat_id=user_id, message_id=msg_id, reply_markup = InlineKeyboardMarkup(buttons))
    
    if request_type == 'done':
        await context.bot.delete_message(update.callback_query.message.chat.id, update.callback_query.message.id)
        await context.bot.send_message(user_id, text='تجري معالجة طلبك..')
        print(data[index])
        file = edit_video(user_id, data[index]["cutSilence"], data[index]["19:6"], data[index]["speedup"], data[index]["music"])
        print(file)
        await context.bot.send_message(user_id, text="Done!")
        await context.bot.send_document(user_id, document=f'{file}')
        
        if data[index]["cutSilence"]:
            os.remove(f'{id}_ALTERED.mp4')
        if data[index]["speedup"]:
            os.remove(f'{id}_ALTERED_ALTERED.mp4')
        if data[index]["19:6"]:
            os.remove(f'{file}')
        
        data.pop(index)
        with open('users_data.json', 'w', encoding='utf-8') as outfile:
            json_data = json.dump(data, outfile, indent=4)




app = ApplicationBuilder().token("6572714563:AAFDUiD1z-U88NbI1GMffs1jO9HwCCs0-Ps").build()

app.add_handler(CommandHandler("start", hello))

app.add_handler(MessageHandler(filters.VIDEO, handle_video))
app.add_handler(MessageHandler(filters.TEXT, handle_url))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()

#pip install Pillow==9.5.0
