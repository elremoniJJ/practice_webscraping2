from quart import Quart, render_template, url_for
from datetime import datetime
import pytz
import requests
from bs4 import BeautifulSoup


app = Quart(__name__)


@app.route('/')
async def index():

	tz = pytz.timezone('Asia/Ho_Chi_Minh')
	date = datetime.now(tz).strftime("%Y, %b %d")
	time = datetime.now(tz).strftime("%H:%M:%S")
	return await render_template("index.html",
				date=date,
				time=time)



def pythonJobs():
	thisBS4 = []

	html_response = requests.get('https://www.careerjet.vn/search/jobs?s=python&radius=100&sort=relevance')
	html_text = html_response.text

	soup = BeautifulSoup(html_text, 'lxml')

	jobs = soup.find_all('article', class_='job clicky')
	for job in jobs:

		companyName = job.find('p', class_='company').text
		position = job.find('h2').text
		location = job.find('ul', class_='location').text

		date_published = "None"
		date_publishedAttempt = job.footer.find('span', class_='badge-icon')
		if date_publishedAttempt != None:
			date_published = date_publishedAttempt.text

		thisBS4.append([companyName, position, location, date_published])


	return thisBS4



@app.route('/go')
async def go():

	thisBS4 = pythonJobs()
	return await render_template("index2.html", thisBS4=thisBS4)

app.run()
