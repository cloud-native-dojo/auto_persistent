#!/bin/bash

# SSH サーバーを起動
service ssh restart

# Flask アプリの準備
if [ ! -d "/Flask_execute-button" ]; then
    echo "Cloning Flask_execute-button repository..."
    git clone https://github.com/cloud-native-dojo/Flask_execute-button.git /Flask_execute-button
fi

# 必要な Python パッケージをインストール
pip3 install -r /Flask_execute-button/requirements.txt

# Flask アプリを起動
cd /Flask_execute-button || exit 1
nohup python3 main.py name-list 5003 > /var/log/flask-5003.log 2>&1 &
nohup python3 main.py name-list-old 5004 > /var/log/flask-5004.log 2>&1 &

# 3秒待機して Flask アプリが起動しているか確認
sleep 3
if ! pgrep -f "python3 main.py name-list"; then
    echo "Flask (5003) failed to start, check logs: /var/log/flask-5003.log"
    exit 1
fi

if ! pgrep -f "python3 main.py name-list-old"; then
    echo "Flask (5004) failed to start, check logs: /var/log/flask-5004.log"
    exit 1
fi

# SSHD をフォアグラウンドで実行（コンテナが終了しないようにする）
exec /usr/sbin/sshd -D
