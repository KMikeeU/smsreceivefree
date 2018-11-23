# Temp-Mail client used in this example https://github.com/KMikeeU/tmp_mail
import tmp_mail
import smsreceivefree
import requests
import random

import time

# Starting the email client with a random address
print("Starting mail client")
mail = temp_mail.Client()

# Starting the sms client
print("Starting smsreceivefree")
smsr = smsreceivefree.Client()


# Printing the randomly chosen email address
print(mail.address)

# Defining a new callback for when a new email arrives
def callb(m):
	# Authenticating the sms client with the link in the email. 
	# WARNING: This is sending out a http request to any link received in the emails!
	smsr.authenticate(m.links()[0])
	print("Got link, authenticated")


# Calling callb whenever new mail arrives
mail.checkloop(callback=callb)


# Sending verification email to client
smsr.signup(mail.address)

while not smsr.authenticated:
	time.sleep(2)

# Getting a list of available numbers
nums = smsr.get_numbers()


# Choosing a random phone number from the list
num = random.choice(nums)

# Checking for new sms on the phone number "num" every few seconds
smsr.watch(num)

# Waiting for new sms to come in
time.sleep(5)

# Printing every verification code found in all the received sms
while True:
	for sms in smsr.messages[num]:
		print(sms.get_code())

	time.sleep(10)