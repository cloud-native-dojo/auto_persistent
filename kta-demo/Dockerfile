FROM ubuntu:22.04

# 必要なパッケージをインストール
RUN apt update && apt install -y \
    openssh-server \
    python3 python3-pip git \
    && mkdir -p /run/sshd \
    && echo 'root:password' | chpasswd \
    && sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config \
    && sed -i 's/#PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config

# エントリーポイントスクリプトを追加
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# ポートを開放
EXPOSE 22 5003 5004

# エントリーポイントスクリプトを実行
CMD ["/entrypoint.sh"]
