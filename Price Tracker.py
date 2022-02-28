import requests
from bs4 import BeautifulSoup
import smtplib
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

preset_value = 1600

product_link = "https://www.amazon.in/Logitech-G102-Customizable-Lighting-Programmable/dp/B08LT9BMPP?ref_=ast_sto_dp&th=1&psc=1"

headers = {
          "Accept-Language" : "en-US,en;q=0.9",
          "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
}

response = requests.get(url = product_link, headers = headers)
html_code = response.text

soup = BeautifulSoup(html_code , "lxml")
price_text = soup.find(name = "span", id = "priceblock_ourprice").getText()

text_list = price_text.split("₹")[1].split(",")
price = float(text_list[0] + text_list[1])

if price < preset_value :
   with smtplib.SMTP("smtp.gmail.com") as connection :
        connection.starttls()
        connection.login(user = os.getenv("EMAIL"), password = os.getenv("PASSWORD"))
        connection.sendmail(
                            from_addr = os.getenv("EMAIL"),
                            to_addrs = os.getenv("EMAIL"),
                            msg = (f"Low price alert! Product available only at ₹{price}.").encode("utf-8")

        )





