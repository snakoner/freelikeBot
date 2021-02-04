# Freelike.Online Bot liker
# 		this program use selenium module for autoliking at bosslike.ru
#		@author: 	2021, February / Andrey Stroganov
#		@contact:	https://github.com/snakoner/ 
#		This program is free to use
#

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys

import selenium
import time
import sys
import random
import datetime
import os
import constant

def error_report(message):
	'''
	@brief: function to stdout error message
	
		@message: 	error message
	'''
	print("[ERROR]: {}".format(message))
	pass

def rand_time(time):
	'''
	@brief: function to get random float + noise, where noise is random float < 1
	
		@time: 	time value
	'''
	noise = random.randint(0,100)/100.0
	return time + noise


def read_user_data(filename):
	'''
	@brief: function to get user's auth data

		@filename: 	source file with user's auth data
	'''
	data = []
	try:
		with open(filename, 'r') as f:
			data = f.read().splitlines()
	except IOError:
		error_report("Can't open file: {}".format(filename))
		return
	return data[0], data[1]

def auth_freelike(browser, iuname, ipass):
	'''
	@brief: function to auth on bosslike.ru

		@browser: 	actual browser object
		@iuname:	username to set
		@ipass:		password to set (plain text, no md5)
	'''

	browser.get(constant.FREELIKE_URL)
	insta_btn = browser.find_elements_by_xpath('//i[@class="socico instaico"]')
	try:
		insta_btn[0].click()
		time.sleep(rand_time(1))
	except IndexError:
		error_report("Can't click button [1]")
		return

	input_insta = browser.find_elements_by_id('linkinsta')
	time.sleep(rand_time(1))
	try:
		input_insta[0].send_keys(iuname)
		time.sleep(rand_time(.5))
	except IndexError:
		error_report("Can't set key [1]")
		return

	next_button = browser.find_elements_by_xpath('//button[@onclick="logininsta();"]')
	try:
		next_button[0].click()
		time.sleep(rand_time(5))
	except IndexError:
		error_report("Can't click button [2]")
		return
	
	randphrase = browser.find_element_by_id('randphrase').text
	time.sleep(rand_time(1))
	if not randphrase:
		error_report("Can't get random phrase [1]")	
		return 

	main_window = browser.current_window_handle
	browser.execute_script("window.open('https://www.instagram.com/accounts/login/', '_blank');");
	time.sleep(rand_time(.8))
	chwd = browser.window_handles
	for x in chwd:
		if x!=main_window:
			browser.switch_to.window(x)
			time.sleep(rand_time(.8))
	if browser.current_window_handle == main_window:
		error_report("Can't open link [1]")
		return 

	log = browser.find_elements_by_xpath('//input[@name="username"]')
	try:
		log[0].send_keys(iuname)
		time.sleep(rand_time(.8))
	except IndexError:
		error_report("Can't set key [2]")
		return

	passw = browser.find_elements_by_xpath('//input[@name="password"]')
	try:
		passw[0].send_keys(ipass)
		time.sleep(rand_time(1))
	except IndexError:
		error_report("Can't set key [3]")
		return

	enter = browser.find_elements_by_xpath('//button')
	try:
		enter[1].click()
		time.sleep(rand_time(4))
	except IndexError:
		error_report("Can't click button [3]")
		return

	browser.get('{}/{}/'.format(constant.INSTAGRAM_URL, iuname))
	time.sleep(rand_time(1))

	edit_button = browser.find_elements_by_class_name('sqdOP.L3NKy._8A5w5.ZIAjV')

	try:
		edit_button[0].click()
		time.sleep(rand_time(2))
	except IndexError:
		error_report("Can't click button [4]")
		return
	try:
		textarea = browser.find_elements_by_class_name('p7vTm')
		textarea[0].clear()
		time.sleep(rand_time(1))
		textarea[0].send_keys(randphrase)
		time.sleep(rand_time(1))
	except IndexError:
		error_report("Can't set key [4]")
		return

	send_button = browser.find_elements_by_class_name('sqdOP.L3NKy.y3zKF')
	try:
		send_button[-1].click()
		time.sleep(rand_time(1))
	except IndexError:
		error_report("Can't click button [4]")
		return

	browser.close()
	browser.switch_to.window(main_window)
	time.sleep(rand_time(1))
	if browser.current_window_handle != main_window:
		error_report("Can't open link [2]")
		return

	check = browser.find_elements_by_id('btn_link2')
	try:
		check[0].click()
	except IndexError:
		error_report("Can't click button [5]")
		return
	print("AUTH was successfull\n")

def get_user_balance(browser):
	'''
	@brief: function to get user's balance at bosslike.ru. 
			To get balance current window must be bosslike.ru.

		@browser: 	actual browser object
	'''
	return browser.find_elements_by_id('points2')[0].text

if __name__ == '__main__':
	#driver start
	opts = Options()
	opts.headless = True if '-s' in sys.argv else False
	opts.add_argument("user-agent={}".format(constant.DRIVER_USER_AGENT))

	browser = webdriver.Chrome(constant.DRIVER_EXEC_PATH_CHROME, options=opts)

	#auth bosslike + instagram
	iuname, ipass = read_user_data('instadata.txt')
	auth_freelike(browser, iuname, ipass)
	time.sleep(rand_time(2))
	browser.get(constant.FREELIKE_URL + '/earn/instagram/instalike')
	i = 0
	n = browser.find_elements_by_class_name('do.do-task.btn.btn-primary.btn-block')
	print("\nEnable tasks number: {}".format(len(n)))
	while i!=len(n):
		main_window = browser.current_window_handle
		browser.switch_to.window(main_window)
		time.sleep(rand_time(1))
		task_buttons = browser.find_elements_by_class_name('do.do-task.btn.btn-primary.btn-block')
		time.sleep(rand_time(1))
		try:
			task_buttons[i].click()
			time.sleep(rand_time(1))
		except IndexError:
			print("Rebooting program")
			os.system('python {} -s &'.format(constant.PY_LIKE_SCRIPT_NAME))
			os.system('kill -9 {}'.format(os.getpid()))

		chwd = browser.window_handles
		for x in chwd:
			if x!=main_window:
				browser.switch_to.window(x)
		if browser.current_window_handle == main_window:
			error_report("Can't open link [5]")
		time.sleep(rand_time(0.2))

		insta_like_button = browser.find_elements_by_class_name('wpO6b ')
		if len(insta_like_button):
			insta_like_button[1].click()
			time.sleep(rand_time(2))
			browser.close()
			time.sleep(rand_time(1))
	
		browser.switch_to.window(main_window)
		task_buttons = browser.find_elements_by_class_name('do.do-task.btn.btn-primary.btn-block')
		task_buttons[i].click()
		time.sleep(rand_time(2))

		i += 1
		balance = get_user_balance(browser)
		print("{}\t{}".format(str(datetime.datetime.now().time()).split('.')[0], balance))
		