# -*- coding: utf-8 -*-
# @Author: Tanzim Rizwan
# @Date:   2016-12-22 20:38:49
# @Last Modified by:   Tanzim Rizwan
# @Last Modified time: 2019-04-03 23:25:58



from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty
from kivy.clock import Clock
from datetime import datetime
import requests
import pytz
import math 
from bs4 import BeautifulSoup


class Counter_Timer(BoxLayout):
	l_name = StringProperty()
	days = StringProperty()
	hours = StringProperty()
	minutes = StringProperty()
	seconds = StringProperty()
	op_team = StringProperty()
	place = StringProperty()


	def update(self, dt):
		
		page = requests.get('http://www.realmadrid.com/en/football/schedule')
		#print (page.status_code)


		soup = BeautifulSoup(page.content,'html.parser')

		name = soup.select_one(".logos > img:nth-of-type(2)").get('title')
		location = soup.select_one(".stadium").text
		team1 = soup.select_one(".teams > .local").text
		team2 = soup.select_one(".teams > .visitor").text
		opponent = team2

		if team2 == 'Real Madrid':
			opponent = team1


		m_time = soup.select_one(".info_date > .hour.confirmada").text
		hour, minute = m_time.split(':')
		m_date = soup.select_one(".info_date > p:nth-of-type(2)").text
		m_date = m_date[3:] + ' 2019'
		d1= datetime.strptime(m_date, '%d %b %Y')
		m_date = d1.strftime('%d/%m/%Y')
		day,month,year = m_date.split('/')

		match_time = datetime(int(year), int(month), int(day), int(hour), int(minute))


		sp_tz = pytz.timezone('Europe/Madrid')

		match_time = sp_tz.localize(match_time)

		now_sp = datetime.now(tz=pytz.timezone('Europe/Madrid'))

		diff = match_time - now_sp


		delta = diff
		a = 1
		if delta.days == 0:
			a =0
		self.days = str(delta.days)
		hour_string = str(delta).split(', ')[a]
		self.hours = hour_string.split(':')[0]
		self.minutes = hour_string.split(':')[1]
		self.seconds = hour_string.split(':')[2].split('.')[0]
		self.l_name = name[0]
		self.op_team = opponent
		self.place = location

class countdown(App):
	def build(self):
		counter = Counter_Timer()
		Clock.schedule_interval(counter.update, 1.0)
		return counter

if __name__=='__main__':
	Window.clearcolor = get_color_from_hex('#101216')
	countdown().run()
