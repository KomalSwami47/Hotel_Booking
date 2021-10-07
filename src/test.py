from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from email.mime.text import MIMEText
from datetime import date
from datetime import datetime
import smtplib
app = Flask(__name__)

roomlist = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

customerlist =[]
feedbacklist = []

app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_PORT']= 3306
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= 'Enter_MYSQL_PASSWORD'
app.config['MYSQL_DB']= 'Hotel'

interface = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
	customerlist = interface.connection.cursor()
	if request.method == 'POST':
		mail = request.form['mail']
		return render_template('index.html', value=mail ,output=" has been recorded")
	else:
		return render_template('index.html')

@app.route('/booking', methods= ['GET', 'POST'])
def booking():
	cursor = interface.connection.cursor()
	global roomnumber
	global roomlist
	global customerlist
	roomcharges = 2000
	totalcharges=0
	if request.method == 'POST':
		mailid = request.form['mailid']
		flag=0
		for room in range(len(roomlist)):
			if roomlist[room] ==0:
				flag=3
				try:
					for user in customerlist:
						if user['mailid'] == mailid:
							flag=2
							break
				except:
					print('Something went wrong')
				if flag == 3:
					name = request.form['name']
					password = request.form['password']
					mobnumber = request.form['mobnumber']
					voterid = request.form['voterid']
					came = request.form['from']
					left = request.form['to']
					child = request.form['child']
					adult = request.form['adult']
					roomnumber=room
					roomlist[room]=1

					checkin = datetime.strptime(came,"%Y-%m-%d")
					checkout = datetime.strptime(left,"%Y-%m-%d")

					days = (checkout - checkin).days
					print("\n Days : ", days, "\n")
					totalcharges = days*roomcharges
					if totalcharges <= 0:
						return render_template('roombook.html', output='Select the valid date.')
					print("\n totalcharges : ", totalcharges, "\n")


					userdata = {'name' : name, 'mailid' : mailid, 'mobnumber' : mobnumber,\
								 'roomnumber' : roomnumber,\
								'checkin' : checkin, 'checkout' : checkout,\
								 'voterid' : voterid, 'days' : days,\
								  'totalcharges' : totalcharges,'password' : password, 'child' : child,\
								  'adult' : adult}
					cursor.execute(
						"""INSERT INTO 
							Bookingdata(
							name,
							mobilenum,
							email,
							password,
							adharid,
							checkin,
							checkout,
							adult,
							child,
							days,
							roomnum
							)
						VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (name, mobnumber, mailid, password, voterid, checkin,\
						 checkout, adult, child, days, roomnumber))
					interface.connection.commit()


					msg = MIMEText("Hi "+ name+"\nYour Booking Has Been Confirmed In IDFC Hotel.\
						\nFor " +str(days) + " Days \nTotal Charges are Rs." +str(totalcharges)+".\
						\nRoom Number : " +str(roomnumber) +".\
						\nIDFC Which Makes Your Booking Experience Better And Happier \
						\n\nFollow Us on Social Media :\
						\nFacbook-: facebook_link\
						\n\nTwitter-: twitter_link\
						\nInstagram-: instagram_link\
						\n\nLinkedin-: linkedin_link\
						\n\nCall us for any inquiry on +91123456789.\n\nThankyou")
					msg['Subject'] = 'Booking Confirmed'
					msg['From'] = "enter_your_mail_id"
					msg['To'] = mailid
					server = smtplib.SMTP("smtp.gmail.com", 587)
					server.starttls()
					server.login("enter_your_mail_id", "enter_your_mailid_password")
					server.sendmail("enter_your_mail_id", mailid, msg.as_string())

					customerlist.append(userdata)
					return render_template('confirm.html', confirmation=userdata)
			else:
				pass
		if flag==0:
			return render_template('roombook.html', output='Sorry Rooms are not availabel')
		elif flag==2:
			return render_template('roombook.html', output='Sorry this ID is already Exist.')

	else:
		return render_template('roombook.html',output=' ')

@app.route('/check', methods= ['GET', 'POST'])
def checking():
	cursor = interface.connection.cursor()
	global roomlist
	global customerlist
	if request.method == 'POST':
		flag=0
		mailid = request.form['mailid']
		password = request.form['password']
		for user in customerlist:
			if mailid == user['mailid'] and password == user['password']:
				flag=1

				return render_template('details.html', confirmation=user)
		if flag==0:
			return render_template("roomcheck.html", confirmation = 'Sorry ID or password does not matched.')

	else:
		return render_template('roomcheck.html', output='')

@app.route('/cancel', methods= ['GET', 'POST'])
def cancellation():
	cursor = interface.connection.cursor()
	if request.method == 'POST':
		global roomlist
		global customerlist
		flag=0
		mailid = request.form['mailid']
		password = request.form['password']

		for user in range(len(customerlist) ):
			if mailid == customerlist[user]['mailid'] and password == customerlist[user]['password']:
				msg = MIMEText("Hi "+ customerlist[user]['name']+"\nYour Booking Has Been Cancelled From IDFC Hotel.\
					\nYou will get your refund Rs." +str(customerlist[user]['totalcharges'])+" soon.\
					\nFollow Us on Social Media :\
					\nFacbook-: facebook_link\
					\nTwitter-: twitter_link\
					\nInstagram-: instagram_link \
					\nLinkedin-: linkedin_link\
					\nCall us for any inquiry on +91123456789.\n\nThankyou")
				msg['Subject'] = 'Booking Cancelled'
				msg['From'] = "enter_your_mail_id"
				msg['To'] = mailid
				server = smtplib.SMTP("smtp.gmail.com", 587)
				server.starttls()
				server.login("enter_your_mail_id", "enter_your_mailid_password")
				server.sendmail("enter_your_mail_id", mailid, msg.as_string())

				flag=1
				data = customerlist[user]
				roomlist[customerlist[user]['roomnumber']]=0
				del customerlist[user]
				return render_template('canceldetails.html', confirmation=data)
			else:
				pass
		if flag==0:
			return render_template('roomcancel.html', confirmation= "ID or Password does not matched.")

	else:
		return render_template('roomcancel.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
	if request.method == 'POST':
		mail = request.form['mail']
		return render_template('about.html', value=mail ,output=" has been recorded")
	else:
		return render_template('about.html')


@app.route('/rooms', methods=['GET', 'POST'])
def rooms():
	if request.method == 'POST':
		mail = request.form['mail']
		return render_template('rooms.html', value=mail ,output=" has been recorded")
	else:
		return render_template('rooms.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
	cursor = interface.connection.cursor()
	if request.method == 'POST':
		name = request.form['name']
		phone = request.form['phone']
		email = request.form['email']
		message = request.form['message']
		feedbackdic = {'name' : name, 'phone' : phone, 'email' : email, "message" : message}
		feedbacklist.append(feedbackdic)

		cursor.execute(
			"""INSERT INTO 
				Feedback(
				name,
				mobilenum,
				email,
				message
				)
			VALUES (%s,%s,%s,%s)""", (name, phone, email, message))
		interface.connection.commit()


		return render_template('contact.html', confirmation="Feedback from", mail=email,  \
			op2="has been recorded", op3="\nThankyou For Your Feedback.")
		print(feedbackdic)
	else:
		return render_template('contact.html')

@app.route('/forgotpassword', methods= ['GET', 'POST'])
def forgotpassword():
	cursor = interface.connection.cursor()
	if request.method == 'POST':
		global roomlist
		global customerlist
		flag=0
		mailid = request.form['mailid']
		for user in range(len(customerlist) ):
			if mailid == customerlist[user]['mailid']:
				flag=1
				msg = MIMEText("Hi "+ customerlist[user]['name']+\
					"\nYour Password is " +customerlist[user]['password'] + "\
					\nFollow Us on Social Media :\
					\nFacbook-: facebook_link\
					\nTwitter-: twitter_link\
					\nInstagram-: instagram_link\
					\nLinkedin-: linkedin_link\
					\nCall us for any inquiry on +91123456789.\n\nThankyou")
				msg['Subject'] = 'Password Recovery'
				msg['From'] = "enter_your_mail_id"
				msg['To'] = mailid
				server = smtplib.SMTP("smtp.gmail.com", 587)
				server.starttls()
				server.login("enter_your_mail_id", "enter_your_mailid_password")
				server.sendmail("enter_your_mail_id", mailid, msg.as_string())
				return render_template('getpswrd.html', confirmation='Your password has been sent to ', ids=customerlist[user]['mailid'])
		if flag== 0:
			return render_template('getpswrd.html', confirmation="Sorry You Haven't Booked Any Room From ", ids=mailid)
	else:
		return render_template('getpswrd.html', confirmation='')




if __name__=='__main__':
	app.run(port=5050)