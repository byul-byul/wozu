#!/bin/bash

# Перейти в корень проекта, если скрипт запущен из scripts/
cd "$(dirname "$0")/.."

# Убить уже работающий ngrok, если есть
pkill -f "ngrok http" 2>/dev/null

# Запустить ngrok на 8000 порту, если он ещё не запущен
if ! pgrep -f "ngrok http 8000" > /dev/null; then
  nohup ngrok http 8000 > /dev/null 2>&1 &
  echo "🚀 Ngrok started..."
fi

# Подождать появления URL (максимум 10 секунд)
for i in {1..10}; do
  URL=$(curl -s http://localhost:4040/api/tunnels \
    | grep -o 'https://[0-9a-zA-Z.-]*\.ngrok[^"]*' \
    | head -n1)
  if [[ $URL ]]; then break; fi
  sleep 1
done

# Проверка: если URL не найден
if [[ -z "$URL" ]]; then
  echo "❌ Ngrok URL not found. Make sure ngrok is running and port 8000 is forwarded."
  exit 1
fi

# Обновить EMAIL_VERIFICATION_BASE_URL в .env
if grep -q '^EMAIL_VERIFICATION_BASE_URL=' .env; then
  sed -i "s|^EMAIL_VERIFICATION_BASE_URL=.*|EMAIL_VERIFICATION_BASE_URL=$URL|" .env
else
  echo "EMAIL_VERIFICATION_BASE_URL=$URL" >> .env
fi

echo "✅ Ngrok URL updated: $URL"
