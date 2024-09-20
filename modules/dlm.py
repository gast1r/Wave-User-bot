from pyrogram import Client, filters
from config import pref_p
import requests
import os
import zipfile

@Client.on_message(filters.command(["dlm","dlm"], prefixes=pref_p) & filters.me)
async def dlm(client, message):
# Ссылка на GitHub с файлами для скачивания
    github_url = "https://github.com/gil9red/parsing-captcha-2/archive/master.zip"
# Название архива
    zip_file_name = "files.zip"

# Скачивание файлов по ссылке GitHub
    response = requests.get(github_url)
    if response.status_code == 200:
        with open(zip_file_name, 'wb') as file:
            file.write(response.content)
        print("Файлы успешно скачаны.")
    else:
        print("Не удалось скачать файлы. Проверьте URL.")

# Создание архива с скачанными файлами
    with zipfile.ZipFile(zip_file_name, 'w') as zipf:
        files = os.listdir(".")  # Получаем список файлов в текущей директории
        for file in files:
            if file.endswith(".png"):  # Добавляем в архив только Python-файлы (можете изменить по вашему усмотрению)
                zipf.write(file)
# Отправка архива в Telegram
    await client.send_document(message.id, zip_file_name, caption="Files from GitHub")
    print("Архив успешно отправлен в Telegram.")
    #await message.edit_text("Думаю....")
