from pyrogram import Client

api_id = 444
api_hash = ""

app = Client("my_2", api_id=api_id, api_hash=api_hash, workdir="sessions")


app.start()
app.send_message("me", "**WaveBot is On!**")