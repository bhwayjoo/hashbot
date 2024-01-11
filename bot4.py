import requests
import hashlib ,hmac
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import os
from keys import TOKEN
base_url = "http://127.0.0.1:5000/"

def wpa(cap, passw):
    hl = cap.split("*")
    mic = bytes.fromhex(hl[2])
    mac_ap = bytes.fromhex(hl[3])
    mac_cl = bytes.fromhex(hl[4])
    essid = bytes.fromhex(hl[5])
    nonce_ap = bytes.fromhex(hl[6])
    nonce_cl = bytes.fromhex(hl[7][34:98])
    eapol_client = bytes.fromhex(hl[7])

    def passwpa(password):
        def min_max(a, b):
            if len(a) != len(b):
                raise ValueError('Unequal byte string lengths')
            for entry in zip(bytes(a), bytes(b)):
                if entry[0] < entry[1]:
                    return a, b
                elif entry[1] < entry[0]:
                    return b, a
            return a, b

        macs = min_max(mac_ap, mac_cl)
        nonces = min_max(nonce_ap, nonce_cl)
        ptk_inputs = b''.join([b'Pairwise key expansion\x00',
                               macs[0], macs[1], nonces[0], nonces[1], b'\x00'])
        password = password.encode()
        pmk = hashlib.pbkdf2_hmac('sha1', password, essid, 4096, 32)
        ptk = hmac.new(pmk, ptk_inputs, hashlib.sha1).digest()
        try_mic = hmac.new(ptk[:16], eapol_client, hashlib.sha1).digest()[:16]
        return try_mic, mic

    return passwpa(passw)

def calculate_hash(word, hash_algorithm):
    hash_object = hash_algorithm()
    hash_object.update(word.encode('utf-8'))
    hashed_string = hash_object.hexdigest()
    return hashed_string

def passlist(passdir, hash_algorithm, target_hash, hash_type):
    with open(passdir, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            line = line.strip()
            if hash_type == '1' or hash_type == '2':
                hashed_word = calculate_hash(line, hash_algorithm)
                if hashed_word == target_hash:
                    return f'Your password is {line}'
            elif hash_type == '3':
                a = wpa(target_hash, line)
                if a[0] == a[1]:
                    return f'Your password is {line}'
    return None

def generate_words(characters, hash_algorithm, num, hash_type, target_hash, current_word="", index=0):
    hashed_word = None
    if index == num:
        if hash_type == '1' or hash_type == '2':
            hashed_word = calculate_hash(current_word, hash_algorithm)
            if hashed_word == target_hash:
                return f'Your password is {current_word}'
        elif hash_type == '3':
            a = wpa(target_hash, current_word)
            if a[0] == a[1]:
                return f'Your password is {current_word}'
        return None
    for char in characters:
        result = generate_words(characters, hash_algorithm, num, hash_type, target_hash, current_word + char, index + 1)
        if result:
            return result
    return None
def start(chat_id, hash_type, target_hash, brut, text, min_num, max_num,passdir):
    if hash_type == '1':
        hash_algorithm = hashlib.md5
    elif hash_type == '2':
        hash_algorithm = hashlib.sha256
    elif hash_type == '3':
        a = wpa(target_hash, '')

        hash_algorithm = wpa

    if brut == '1':
        text = text
        min_num = min_num
        max_num = max_num
        output_text = list(text)
        for num in range(min_num, max_num + 1):
            result = generate_words(output_text, hash_algorithm, num, hash_type, target_hash)
            if result:
                return chat_id, result
    elif brut == '2':
        passdir = passdir
        a = passlist(passdir, hash_algorithm, target_hash, hash_type)
        return chat_id, a
    else:
        passdir = 'rockyou.txt'
        a = passlist(passdir, hash_algorithm, target_hash, hash_type)
    return chat_id, a




async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="salam had bot dar bach ydir decript lchi hash b brute force kaybda ydir brute force ou fhad so2al kadir 'Type your characters:' kdir l7orof li bghtihom ykono  /start",
    )
async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    username = update.message.from_user.username
    first_name = update.message.from_user.first_name
    chat_id = update.message.from_user.id

    payload = {
        "output": message_text,
        "username": username,
        "first_name": first_name,
        "chat_id": chat_id,
    }
    r = requests.get(base_url + "start", params=payload)
    if r.status_code == 200:
        result=r.json()
        chat_id = result.get("chat_id")
        message=result.get('message')

        await context.bot.send_message(
            chat_id=chat_id,
            text=message,
        )

async def shorten_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    username = update.message.from_user.username
    first_name = update.message.from_user.first_name
    chat_id = update.message.from_user.id
    
    if (update.message.document):
        
        file_id = update.message.document.file_id
        _, f_ext = os.path.splitext(update.message.document.file_name)
        unique_file_id = update.message.document.file_unique_id
        file_name = f"{unique_file_id}.{f_ext}"
        photo_file = await context.bot.get_file(file_id)
        filedir = f'./wordlist/{file_name}'
        await photo_file.download_to_drive(custom_path=filedir)

        payload = {
                    "output": filedir,
                    "username": username,
                    "first_name": first_name,
                    "chat_id": chat_id,
                }
        r = requests.get(base_url + "file", params=payload)
        result = r.json()

        chat_id = result.get("chat_id")
        passdir = result.get("filedir")
        hash_type=result.get("hassh")
        target_hash=result.get("targetHash")
        conn=result.get("complete")
        brut='2'

        if conn=='file':
            try:
                await context.bot.send_message(chat_id=chat_id, text=f"your password is only cracked ..", )

                crack=start( chat_id,"1", "9df3b01c60df20d13843841ff0d4482c", "2", '', '', '',passdir)
                
                await context.bot.send_message(chat_id=chat_id, text=f"{crack}", )
                os.remove(filedir)
            except:
                await context.bot.send_message(chat_id=chat_id, text=f"please send file ", )
                os.remove(filedir)
        else:
            await context.bot.send_message(chat_id=chat_id, text=f"Sending a file smaller than 20 mg", )
            os.remove(filedir)
    
    else:
        message_text = update.message.text
        payload = {
            "output": message_text,
            "username": username,
            "first_name": first_name,
            "chat_id": chat_id,}

    try:

        r = requests.get(base_url + "sum", params=payload)
        if r.status_code == 200:
            result = r.json()
            comm = result.get("complete")


            if result.get("complete") == "yes":

                hash_type =result.get("hassh")
                target_hash=result.get("targetHash")
                brut=result.get("brutetype")
                text=result.get("characters")
                min_num=int(result.get("min_num"))
                max_num=int(result.get("min_num"))
                chat_id = result.get("chat_id")
                await context.bot.send_message(chat_id=chat_id, text=f"your password is only cracked ...", )

                chat_id, a = start(chat_id, hash_type, target_hash, brut, text, min_num, max_num,'')
                
                await context.bot.send_message(chat_id=chat_id, text=f"{a}",)
                
            elif comm==("rok"):
                await context.bot.send_message(chat_id=chat_id, text=f"your password is only cracked ...", )
                hash_type = result.get("hassh")
                target_hash = result.get("targetHash")
                brut = result.get("brutetype")

                chat_id = result.get("chat_id")

                chat_id,a = start( chat_id,hash_type, target_hash, brut, '', '', '','')
                await context.bot.send_message(chat_id=chat_id, text=f"{a}",)
        

            elif comm == ("file"):
                print('hisse')
                if (update.message.document):
                    print('hie')
                    file_id = update.message.document.file_id
                    _, f_ext = os.path.splitext(update.message.document.file_name)
                    unique_file_id = update.message.document.file_unique_id
                    file_name = f"{unique_file_id}.{f_ext}"
                    photo_file = await context.bot.get_file(file_id)
                    filedir = f'./wordlist/{file_name}'
                    await photo_file.download_to_drive(custom_path=filedir)
                    await context.bot.send_message(chat_id=update.effective_chat.id, text='wait ')
                    payload = {
                        "output": filedir,
                        "username": username,
                        "first_name": first_name,
                        "chat_id": chat_id,
                    }

                    



            else:
                message = result.get("message")

                await context.bot.send_message(
                    chat_id=chat_id,
                    text= message,
                )

        else:
            await context.bot.send_message(
                chat_id=chat_id, text=f"The message does not contain a valid "
            )

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f'sorry  i dont find your password')





if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    # command handlers
    help_handler = CommandHandler("help", help_callback)
    start_handler = CommandHandler("start", start_callback)
    msg_handler = MessageHandler(filters.TEXT | filters.Document.ALL, shorten_link)

    # register commands
    app.add_handler(help_handler)
    app.add_handler(start_handler)
    app.add_handler(msg_handler)
    app.run_polling()
