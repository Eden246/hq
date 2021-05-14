import smtplib
from email.mime.text import MIMEText
 
# 送受信先
to_email = "so-kan@life-techno.jp"
from_email = "tsu-watase@life-techno.jp"
 
# MIMETextを作成
message = "メール本文"
msg = MIMEText(message, "html")
msg["Subject"] = "メール表題"
msg["To"] = "so-kan@life-techno.jp"
msg["From"] = "tsu-watase@life-techno.jp"
 
# サーバを指定する
server = smtplib.SMTP("118.21.150.161", 587)
# メールを送信する
server.send_message(msg)
# 閉じる
server.quit()