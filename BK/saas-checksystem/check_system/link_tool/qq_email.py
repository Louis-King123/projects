import smtplib
from email.mime.text import MIMEText
from email.header import Header
from config import mail_pass, sender

class Mail:
    def __init__(self, receivers, content, sender_name, recipients_name,):
        # 第三方 SMTP 服务

        self.mail_host = "smtp.qq.com"  # 设置服务器:这个是qq邮箱服务器，直接复制就可以
        self.mail_pass = mail_pass  # 刚才我们获取的授权码
        self.sender = sender  # 你的邮箱地址
        self.receivers = receivers  # 收件人的邮箱地址，可设置为你的QQ邮箱或者其他邮箱，可多个

        self.content = content
        self.sender_name = sender_name
        self.recipients_name = recipients_name

    def send(self):

        content = '你要发送的邮件内容'
        message = MIMEText(self.content, 'plain', 'utf-8')

        message['From'] = Header(self.sender_name, 'utf-8')
        message['To'] = Header(self.recipients_name, 'utf-8')

        subject = '蓝鲸巡检报告'  # 发送的主题，可自由填写
        message['Subject'] = Header(subject, 'utf-8')
        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, 465)
            smtpObj.login(self.sender, self.mail_pass)
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            smtpObj.quit()
            return {'coed': 200, 'msg': "发送成功"}
        except smtplib.SMTPException as e:
            return {'coed': 500, 'msg': "发送失败"}

# if __name__ == '__main__':
#     mail = Mail()
#     mail.send()