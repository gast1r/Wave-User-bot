from pyrogram import Client

api_id = 21760452
api_hash = "25e354715e4da9d992d76c6e5514e536"

app = Client("my_2", api_id=api_id, api_hash=api_hash, workdir="sessions")


app.start()
app.send_message("me", "**WaveBot is On!**")