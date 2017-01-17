#!/home/victormora/.local/bin/python3⁄

import datetime
import calendar
import pandas as pd
import warnings
from datetime import date
pd.set_option('display.float_format', lambda x: '%.2f' % x)
warnings.filterwarnings('ignore')

def grab_data():
	url = 'https://docs.google.com/spreadsheets/d/1-MEOxWn6VeUgFgjzoIRY-d6teP5xS_fr34X5cldbwwY/export?gid=0&format=csv'
	data = pd.read_csv(url, error_bad_lines=False)

	data['timestamp_arrive'] = pd.to_datetime(data['Date']+' '+data['Line-up Time'])
	data['timestamp_depart'] = pd.to_datetime(data['Date']+' '+data['Line-up Time'])
	data = data.rename(columns={'User':'user',
								'Day of Week':'weekday',
								'# in Line':'count',
								'Notes':'notes'})
	data = data.drop(['Date', 'Line-up Time', 'Pick-up Time'], axis=1)

	return data

def format_df(df, day):
	df['timestamp'] = df['timestamp_arrive'].apply(lambda x: x.replace(month=1, day=1, year=2017))
	df = df.set_index('timestamp')
	df = df.sort_index()
	df = df.drop('timestamp_arrive', axis=1)
	grp = df.groupby(pd.TimeGrouper(freq='10min')).mean()
	grp.index = grp.index.time

	html_body = """
		<h2>{} Average</h2>
		""".format(day)

	html_body += grp.to_html()

	return html_body

def main():
	html_body = ""
	weekday = calendar.day_name[date.today().weekday()]

	data = grab_data()

	today_df = data[data['weekday'] == weekday][['count', 'timestamp_arrive']]
	average_df = data[['count', 'timestamp_arrive']]

	html_body += format_df(today_df, weekday)
	html_body += format_df(average_df, 'Weekly')

	html_header = """
		<html>
		<head>
			<title>Casual Carpool</title>
		</head>
		<body>
		"""

	html_footer = """
		</body>
		</head>
		</html>
		"""

	html = html_header + html_body + html_footer

	html_file = open('casual_carpool.html', 'w')
	html_file.write(html)
	html_file.close()

	# print(weekday+' Average')
	# format_df(today_df)
	# print('Weekly Average')
	# format_df(average_df)

if __name__ == '__main__':
	main()