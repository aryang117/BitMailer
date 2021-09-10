import requests
import json
import smtplib
import ssl
import time


class Work:

    def __init__(self):
        self.port = 465
        self.smtp_server_domain_name = "smtp.gmail.com"
        self.sender_mail = "trolled00gamer@gmail.com"
        self.password = "&MN,xHVPbm6J1VL("

    def send(self, email, content):
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(
            self.smtp_server_domain_name, self.port, context=ssl_context)
        service.login(self.sender_mail, self.password)

        result = service.sendmail(
            self.sender_mail, email, f"Subject: {content}")

        service.quit()


def apiCall():
    response = requests.get(
        'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false')
    print(response)

    x = response.json()
    return x[0]['current_price']

    #return y['current_price']


def main():

    time_interval = 60
    work = Work()
    #work.send('aryu100@gmail.com', x)

    while True:
        price = apiCall()

        # if the price falls below threshold, send an immediate msg
        if price < 50000:
           print(price)
           #  work.send('aryu100@gmail.com', f"PriceDrop!! {price}")

        # fetch the price for every dash minutes
        time.sleep(time_interval)

if __name__ == '__main__':
    main()