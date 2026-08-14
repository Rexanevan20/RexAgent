# Bot Telegram - Versi Dasar

Bot ini baru bisa membalas pesan, belum pakai AI.

## Cara jalanin di Railway
1. Upload 3 file ini (main.py, requirements.txt, Procfile) ke repo GitHub baru.
2. Di Railway, klik "New Project" > "Deploy from GitHub repo", pilih repo tadi.
3. Buka tab "Variables", tambahkan:
   - Key: `BOT_TOKEN`
   - Value: (token dari BotFather)
4. Railway otomatis install & jalanin bot. Cek tab "Deployments" > "View Logs" untuk pastikan muncul tulisan "Bot mulai jalan...".
5. Buka Telegram, chat bot km, ketik /start.
