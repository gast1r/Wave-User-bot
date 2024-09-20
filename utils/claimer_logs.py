from datetime import datetime 

def logger(text):
    date = datetime.today()
    now = date.strftime("%Y.%m.%d %H:%M:%S")
    with open("logs_auto.txt", "a", encoding="utf-8") as text_file:
        text_file.write(f"{now} - {text}\n")
    return True