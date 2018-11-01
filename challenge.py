"""
TNumb3rs Challenge
Created by Marcio Almeida
https://github.com/pimps/tnumb3rs
"""

import sys
import inspect
import sqlite3
import binascii
from bottle import route, run, debug, template, request, static_file, error
from bottle import default_app
import re
import html
import math


################
### TEMPLATE ###
################

scoreboard_tpl = """
	<html>
	<head>
	<!-- Bootstrap 4 -->
	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css">
	<script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js"></script>
	<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/limonte-sweetalert2/7.28.5/sweetalert2.min.js"></script>
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/limonte-sweetalert2/7.28.5/sweetalert2.min.css">
	<style>
	.swal2-modal pre {
		  background: #49483e;
		  color: #f7f7f7;
		  padding: 10px;
		  font-size: 14px;
		  text-align: left;
		}
	</style>
	</head>
	<body>
	<div class="container">
		<p><a href='/source'>Click Here to print the Source Code!</a></p>
		<button id="register-btn" type="button" class="btn btn-secondary">
	  		Register
		</button>
		<button id="sendnumb3r-btn" type="button" class="btn btn-primary">
	  		Send a Numb3r
		</button>
		<p><h3>Scoreboard:</h3></p>
		<table class="table table-hover">
			<thead class="thead-inverse">
				<tr>
					<th>User ID</th>
					<th>Name</th>
					<th><button id="0" type="button" class="btn btn-info">c0</button></th>
					<th><button id="1" type="button" class="btn btn-info">c1</button></th>
					<th><button id="2" type="button" class="btn btn-info">c2</button></th>
					<th><button id="3" type="button" class="btn btn-info">c3</button></th>
					<th><button id="4" type="button" class="btn btn-info">c4</button></th>
					<th><button id="5" type="button" class="btn btn-info">c5</button></th>
					<th><button id="6" type="button" class="btn btn-info">c6</button></th>
					<th><button id="7" type="button" class="btn btn-info">c7</button></th>
					<th><button id="8" type="button" class="btn btn-info">c8</button></th>
					<th><button id="9" type="button" class="btn btn-info">c9</button></th>
					<th>Points</th>
				</tr>
			</thead>
			<tbody>
			%for row in rows:
			  <tr>
			  %for col in row:
			    <td>{{col}}</td>
			  %end
			  </tr>
			%end
			</tbody>
		</table>
	</div>
	<script>
		function getChallengeDesc(id) {
			return $.ajax({
				type: "GET",
				url: '/challenge/'+id,
				async: false
			}).responseText;
		}
		$(".btn.btn-info").click( function()
		   {
			var id = $(this).attr('id');
			var chall_desc = getChallengeDesc(id);
			showModal("Challenge " + id, chall_desc + "Numb3r format is [user_id{6}]["+id+"][numb3r] => ex: 000037"+id+"1337", 900, "execute");
		   }
		);
		$("#register-btn").click( function()
		   {
			showModal("Insert your e-mail and name to register", "Registration format is [e-mail]|[name{1-20}] ex: user@test.com|nickname", 600, "register");
		   }
		);
		$("#sendnumb3r-btn").click( function()
		   {
		    showModal("Insert a Numb3r", "Numb3r format is [user_id{6}][chall_id][numb3r] => [000037][0][1337] => ex: 00003701337", 900, "execute");
		   }
		);
		function showModal(title, description, width, api){
			swal({
				  title: title,
				  input: 'text',
				  html: description,
				  width: width,
				  inputAttributes: {
				    autocapitalize: 'off'
				  },
				  showCancelButton: true,
				  confirmButtonText: 'Send',
				  showLoaderOnConfirm: true,
				  preConfirm: (input) => {
				    return fetch(`/${api}/${input}`)
				      .then(response => {
					if (!response.ok) {
					  throw new Error(response.statusText)
					}
					return response.json()
				      })
				      .catch(error => {
					swal.showValidationMessage(
					  'Numb3r failed... Try Again...'
					)
				      })
				  },
				  allowOutsideClick: () => !swal.isLoading()
				}).then((result) => {
					if (result.value){
						if (result.value.error){
						    swal({
						      type: 'error',
						      text: result.value.error,
						    })
						} else {
						    swal({
						      type: 'success',
						      text: result.value.success,
						    })
						}
					}
				})

		}
	</script>
	</body>
	</html>
"""


##################
### CHALLENGES ###
##################

def c0(userid, num):
	if(convertToInt(num) < 0):
		return solve(userid, "c0")

def c1(userid, num):
	if(convertToInt(num) == -31337):
		return solve(userid, "c1")

def c2(userid, num):
	s = binascii.unhexlify(num).decode('utf8')
	if(s == "t31str4"):
		return solve(userid, "c2")

def c3(userid, num):
	x = binascii.hexlify("TNumb3rs".encode('utf8'))
	y = binascii.hexlify("telstra".encode('utf8'))
	z = str(int(x[::-1] + y, 16) * 2018)
	if(num == z):
		return solve(userid, "c3")

def c4(userid, num):
	a, *b, c = [int(i) for i in str(num)]
	x = ""
	for i in b:
		if i == 0:
			a -= c
		elif i == 1:
			a += c
		else:
			x += chr(a * i)
	if x == "t3L$Tr4":
		return solve(userid, "c4")

def c5(userid, num):
	if len(num) > 20:
		return False
	x = float(binascii.unhexlify(num).decode('utf8')); 
	y = x*x
	z = y - y
	if z != z:
		return solve(userid, "c5")

def c6(userid, num) :
	n = int(num, 2)
	value = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
	if value == "TELSTRA":
		return solve(userid, "c6")

def c7(userid, num) :
	value = 432
	valuе = 5341
	value += 5431
	valuе += 654
	value -= 6421
	valuе -= 2345
	value += 65412
	valuе += 2351
	value += 6542
	valuе += 12345
	value += 65421
	valuе *= 7567
	value += 669
	valuе += 8545
	value -= 645743
	valuе += 8654
	value += 17456
	valuе -= 8674
	value += 967657
	valuе += 8678532
	value += 86785
	value += 63423
	value = value * valuе
	if num == str(valuе):
		return solve(userid,"c7")

def c8(userid, num):
	if len(num) != 15:
		return False
	a, *b, c = [int(i) for i in str(num)]
	b = "".join(map(str, b))
	val = a ** c * int(b)
	if val < 1337 or val > 31337:
		return False
	try:
		val = a - c / math.log(float(b))
	except ZeroDivisionError:
		return solve(userid, "c8")

def c9(userid, num):
	p = 31337
	n = 2248600233161889077989201
	#e = 520266880399545901718231
	q, d, c = [int(i) for i in num.split("00000")]
	if n != p * q:
		return False
	t = format(pow(c, d, n), '02x')
	msg = binascii.unhexlify(t).decode('utf8')
	if msg == "TELSTRA":
		return solve(userid, "c9")

#################
##### UTIL ######
#################

def convertToInt(val):
	val = int(val)
	if not -sys.maxsize-1 <= val <= sys.maxsize:
		val = (val + (sys.maxsize + 1)) % (2 * (sys.maxsize + 1)) - sys.maxsize - 1
	return val

def solve(userid, challenge):
	conn = sqlite3.connect('scoreboard.db')
	c = conn.cursor()
	c.execute("UPDATE scoreboard SET %s = 1 WHERE user_id = ?" % challenge, (int(userid),))
	conn.commit()
	c.close()
	return '{"success" : "WHOOHOO! user %s scored challenge %s!"}' % (userid, challenge)

def create_db():
	conn = sqlite3.connect('scoreboard.db') 
	conn.execute("CREATE TABLE if not exists scoreboard (user_id INTEGER PRIMARY KEY, email TEXT NOT NULL UNIQUE, name TEXT NOT NULL, c0 INTEGER, c1 INTEGER, c2 INTEGER,c3 INTEGER,c4 INTEGER,c5 INTEGER,c6 INTEGER,c7 INTEGER,c8 INTEGER,c9 INTEGER)")
	conn.commit()

def scoreboard():
	try:
		conn = sqlite3.connect('scoreboard.db')
		c = conn.cursor()
		c.execute("SELECT user_id, name, c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, (c0+c1+c2+c3+c4+c5+c6+c7+c8+c9) as points FROM scoreboard ORDER BY points DESC")
		result = c.fetchall()
		c.close()
		output = template(scoreboard_tpl, rows=result)
		return output
	except:
		create_db()
		return "Database Created! <meta http-equiv='refresh' content='3;' />"

def isUserRegistered(user_id, email):
	conn = sqlite3.connect('scoreboard.db')
	c = conn.cursor()
	c.execute("SELECT user_id FROM scoreboard WHERE user_id=? OR email=?", (int(user_id),email))
	data = c.fetchall()
	c.close()
	if len(data)==0:
		return False
	else:
		return data[0][0]

def isValidEmail(email):
	if len(email) > 7:
		if re.match("[^@]+@[^@]+\.[^@]+", email) != None:
			return True
	return False

def isValidName(name):
	if len(name) > 1 and len(name) < 20:
		if re.match("^[\w\s]+$", name) != None:
			return True
	return False


#####################
###### MAPPING ######
#####################

# Function used to register a new user 
# The format is http://x.x.x.x/register/[email]|[name]
# Ex: Register a new user with the e-mail user@test.com and name First Last
#		http://x.x.x.x/register/user@test.com|First Last
@route('/register/<email>', method='GET')
def register(email):
	[email, name] = email.split("|")
	if not isValidEmail(email):
		return '{"error" : "Invalid email... Please insert a valid e-mail!"}'
	if not isValidName(name):
		return '{"error" : "Invalid name... Please insert a valid name!"}'
	user_id = isUserRegistered(0, email)
	if not user_id:
		conn = sqlite3.connect('scoreboard.db') 
		c = conn.cursor()
		c.execute("""INSERT INTO scoreboard (email, name, c0, c1, c2, c3, c4, c5, c6, c7, c8, c9) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", (email,name,0,0,0,0,0,0,0,0,0,0,))
		new_id = c.lastrowid
		conn.commit()
		c.close()
		return '{"success" : "Registered with success, your User ID is %s"}' % new_id
	else:
		return '{"error" : "User already registered! User ID: %s"}' % user_id


# Function used to execute a guess 
# The format is http://x.x.x.x/execute/[user_id][chall_id][guess]
# Ex: Send the guess 123456 to the challenge 1 with the user 37:
#		http://x.x.x.x/execute/0000371123456
@route('/execute/<number:re:[0-9]+>', method='GET')
def execute(number):
	userid = str(number[:6])
	check_id = str(number[6])
	num = str(number[7:])
	if(isUserRegistered(userid, "")):
		return getattr(sys.modules[__name__], "c%s" % check_id)(userid, num)
	else:
		return '{"error" : "User not registered. Register a new user first."}'

# Function used to print the source code 
# The format is http://x.x.x.x/source
@route('/source', method='GET')
def source():
	source = ""
	with open(__file__) as f:
		source = f.read()
	return "<pre style='font-family: Lucida'>" + html.escape(source) + "</pre>"

# Function used to print the source code of a challenge
# The format is http://x.x.x.x/challenge/[id]
@route('/challenge/<chall_id:re:[0-9]>', method='GET')
def source(chall_id):
	source = inspect.getsource(getattr(sys.modules[__name__], "c%s" % chall_id))
	return "<pre style='font-family: Lucida'><code>" + html.escape(source) + "</code></pre>"

# Function used to print the Scoreboard
@route('/', method='GET')
def main():
	return scoreboard()

@error(403)
def mistake403(code):
    return '{"error" : "There is a problem in your url!"}'

@error(404)
def mistake404(code):
    return '{"error" : "Sorry, this page does not exist!"}'

@error(500)
def mistake500(code):
    return '{"error" : "OOOOOPS... something went really wrong :-/"}'

if __name__ == "__main__":
    run(host="127.0.0.1", port=9090, reloader=True)
else:
    application = default_app()
