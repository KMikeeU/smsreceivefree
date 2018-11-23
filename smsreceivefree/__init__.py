import requests
from bs4 import BeautifulSoup
import _thread
import time
import re

class Client():
	def __init__(self, email: str = ""):
		self.messages = {}
		self.email = email

		self.base = "https://smsreceivefree.com/"
		self.signup_url = "signup"
		self.numbers_url = "country/"
		self.info_url = "info/"

		self.realistic = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
			"Referer": "https://smsreceivefree.com/"
		}

		self.signup_headers = {
			"Content-Type": "application/x-www-form-urlencoded",
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
			"DNT": 1,
			"Upgrade-Insecure-Requests": 1
		}

		self.session = requests.Session()
		self.session.get(self.base)

		self.authenticated = False

	def signup(self, email):
		self.email = email
		data = {
			"address": self.email
		}

		req = self.session.post(self.base + self.signup_url, data=data, headers={**self.realistic, **self.signup_headers})
		if "Unable to generate an account for:" in req.text:
			raise ValueError("Invalid Email Address or IP Ban")
		else:
			return

	def authenticate(self, auth_url):
		req = self.session.get(auth_url, headers=self.realistic)
		self.authenticated = True

	def get_numbers(self):
		country_codes = ["usa", "canada"]

		numbers = []

		for country in country_codes:
			req = self.session.get(self.base+self.numbers_url+country, headers=self.realistic)

			soup = BeautifulSoup(req.text, "html.parser")
			numbers += [ i["href"][6:-1] for i in soup.findAll("a", {"class": "numbutton"}) ]

		return numbers

	def watch(self, number, async=True):
		if async:
			_thread.start_new_thread(self.watch, (number,), {"async": False})
		else:
			while True:
				req = self.session.get(self.base + self.info_url + number, headers=self.realistic)
				soup = BeautifulSoup(req.text, "html.parser")

				rows = soup.find("tbody").findChildren("tr", recursive=False)

				sms = []

				for row in rows:
					data = row.findChildren("td", recursive=False)
					sms.append(SMS(data[0].decode_contents(), data[2].decode_contents()))

				self.messages[number] = sms

				time.sleep(10)

class SMS():
	def __init__(self, by, content):
		self.by = by
		self.content = content
	def get_code(self):
		return [re.findall(r".*?(\d{3,}).*?", self.content), self.content, self.by]