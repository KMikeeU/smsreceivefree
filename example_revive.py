import smsreceivefree
import random

import time

print("Starting smsreceivefree")

smsr = smsreceivefree.Client()


revival_token = "YOUR_TOKEN"
smsr.authenticate(revival_token)

nums = smsr.get_numbers()

num = random.choice(nums)

smsr.watch(num)

time.sleep(5)

while True:
	for sms in smsr.messages[num]:
		print(sms.get_code())

	time.sleep(10)
