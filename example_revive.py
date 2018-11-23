import smsreceivefree
import random

import time

print("Starting smsreceivefree")

smsr = smsreceivefree.Client()


revival_token = "https://www.smsreceivefree.com/activate?id=b266eeb7a784725e929c0451cdb9f8e352a85320"
smsr.authenticate(revival_token)

nums = smsr.get_numbers()

num = random.choice(nums)

smsr.watch(num)

time.sleep(5)

while True:
	for sms in smsr.messages[num]:
		print(sms.get_code())

	time.sleep(10)