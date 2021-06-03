# TG_TAG_Bot

```
/start - Yardım metnini görüntüle
/in - Bahsetmek için kaydolun
/out - Bahsedilenleri almayı devre dışı bırakma
/all - Etkinleştirilmiş tüm kullanıcılardan bahsedin
/stats - Bot istatistiklerini göster
```

## Installation

```bash
# clone the repo
git clone https://github.com/bkaanozsr1/TG_TAG_Bot.git
cd mention-all-bot

# bot tokenini ve db şifrenizi ayarlayın
echo "TGBOT_TOKEN=????????" > .env
echo "DB_PWD=????????" >> .env

# uygulamayı çalıştır
docker-compose up -d
```
