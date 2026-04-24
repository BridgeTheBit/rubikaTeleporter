#!/bin/bash

echo "=============================="
echo "      Tel2Rub Installer"
echo "=============================="

# Python check
if ! command -v python3 &> /dev/null
then
    echo "Python3 not installed"
    exit
fi

echo ""
echo "Enter configuration values"
echo ""

read -p "Telegram API_ID: " API_ID
read -p "Telegram API_HASH: " API_HASH
read -p "Telegram BOT_TOKEN: " BOT_TOKEN
read -p "Rubika Session: " RUBIKA_SESSION
read -p "Target Channel (default=me): " TARGET_CHANNEL

if [ -z "$TARGET_CHANNEL" ]; then
TARGET_CHANNEL="me"
fi

echo ""
echo "Creating .env..."

cat <<EOF > .env
API_ID=$API_ID
API_HASH=$API_HASH
BOT_TOKEN=$BOT_TOKEN
RUBIKA_SESSION=$RUBIKA_SESSION
TARGET_CHANNEL=$TARGET_CHANNEL
EOF

echo ".env created"

echo ""
echo "Installing system packages..."

sudo apt update
sudo apt install python3-venv python3-pip -y

echo ""
echo "Creating virtual environment..."

cd tel2rub
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Creating folders..."

mkdir -p queue
mkdir -p downloads
mkdir -p logs

touch queue/tasks.jsonl

echo ""
echo "Installing service..."

sudo cp service/tel2rub.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl enable tel2rub
sudo systemctl start tel2rub

chmod +x tel2rub
sudo ln -s /root/tel2rub/tel2rub /usr/local/bin/tel2rub

echo ""
echo "✅ Installation finished"
echo ""

sudo systemctl status tel2rub
