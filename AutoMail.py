# coding=utf-8
import smtplib
import requests
import re
import json
from threading import Timer
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

host_mail = '1178362914@qq.com'
authorization_code = 'skivfapazztlbaci'
mailLists = ['lsldragon@outlook.com', '2273785747@qq.com']
intervalTime = 40

html_email1 = "<html > <font color = red ><body ><h1> 全国数据 </h1 ><h2> 确诊: "
html_email2 = "</h2><h2> 治愈:"
html_email3 = "</h2><h2> 死亡: "
html_email4 = "</h2></body></html >"


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def getData():
    """
    get the data
    """
    headers = {"User-Agent":
               "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Mobile Safari/537.36"}
    response = requests.get(
        'https://3g.dxy.cn/newh5/view/pneumonia', headers=headers)
    response.encoding = 'utf-8'

    rawresult = re.search(
        '<script id="getAreaStat">(.*)</script>', response.text)
    provincedata = re.search(
        '\[.*\]', rawresult.group(1)).group(0).split('catch')

    finalresult = provincedata[0]
    finalresult = finalresult[0:-1]

    jsondata = json.loads(finalresult)

    chinaConfirmCount = 0
    chinaCuredCount = 0
    chinaDeadCount = 0

    for province in jsondata:
        chinaConfirmCount += province.get('confirmedCount')
        chinaDeadCount += province.get('deadCount')
        chinaCuredCount += province.get('curedCount')

    # displayString = "全国 确: %s 亡: %s 愈 %s" % (
    #     chinaConfirmCount, chinaDeadCount, chinaCuredCount)
    displayString = html_email1 + str(chinaConfirmCount) + html_email2 + str(
        chinaDeadCount) + html_email3 + str(chinaCuredCount) + html_email4
    return displayString


def sendEmail():
    """
    To send email
    """
    msg_from = host_mail  # 发送方邮箱
    passwd = authorization_code  # 填入发送方邮箱的授权码
    msg_to = mailLists  # 收件人邮箱

    subject = "武汉加油"  # 主题
    # content = "<html><font size=6 color=red> 加油 武汉</html>"

    contents = getData()
    msg = MIMEText(contents, "html", "utf-8")
    msg['Subject'] = subject
    msg['From'] = _format_addr('Elliot Lee <%s>' % msg_from)

    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print("发送成功")
        t = Timer(intervalTime, sendEmail)
        t.start()

    except (s.SMTPException):
        print("发送失败")
    finally:
        s.quit()


if __name__ == "__main__":
    sendEmail()
