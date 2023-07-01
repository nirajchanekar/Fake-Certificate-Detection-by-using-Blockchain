from flask import Flask, render_template, request, redirect, url_for, session, flash
from index import BlockChain
import json

app = Flask(__name__)
app.secret_key = "alkdjfalkdjf"

@app.route("/")
def home():
	if session.get("user"):
		return render_template('index.html')
	else:
		flash("Please login to access Verifier")
		return redirect(url_for('login'))



@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "POST":
		user = request.form["username"]
		pswd = request.form["password"]

		if user == "Admin":
			if pswd == "password":
				session["user"] = "Admin"
				return redirect(url_for("admin"))
		
		elif user == "Nike":
			if pswd == "password":
				session["user"] = "Nike"
				return redirect(url_for("shoes"))
		
		else:
			flash("Invalid Login details")
			return redirect(url_for('login'))
	else:
		return render_template('login.html')


@app.route("/verify/<kid>", methods=["GET"])
def verify(kid):
		return render_template('verify.html', keyId=kid)


@app.route("/verify", methods=["POST"])
def success():

	post_data = request.form["keyId"]

	with open('./NODES/N1/blockchain.json', 'r') as bfile:
		n1_data = str(bfile.read())
	with open('./NODES/N2/blockchain.json', 'r') as bfile:
		n2_data = str(bfile.read())
	with open('./NODES/N3/blockchain.json', 'r') as bfile:
		n3_data = str(bfile.read())
	with open('./NODES/N4/blockchain.json', 'r') as bfile:
		n4_data = str(bfile.read())

	pd = str(post_data)

	if (pd in n1_data) and (pd in n2_data) and (pd in n3_data) and (pd in n4_data):

		with open('./NODES/N1/blockchain.json', 'r') as bfile:
			for x in bfile:
				if pd in x:
					a = json.loads(x)["data"]
					b = a.replace("'", "\"")
					data = json.loads(b)
					dept = data["Department"]
					name = data["SName"]
					batch = data["SBatch"]
					Jdate = data["JoiningDate"]
					date = data["Duration"]
					id = data["SId"]
					marks = data["SMarks"]
					grade = data["SGrade"]
					course = data["SCourse"]
		
		return render_template('success.html', brand=dept, name=name, batch=batch, manfdate=Jdate, exprydate=date, id=id, price=marks, size=grade, type=course)
	
	else:
		return render_template('fake.html')


@app.route("/addproduct", methods=["POST", "GET"])
def addproduct():
	if request.method == "POST":
		brand	 = request.form["brand"]
		name	 = request.form["name"]
		batch	 = request.form["batch"]
		pid	 	 = request.form["id"]
		manfdate = request.form["manfdate"]
		exprydate= request.form["exprydate"]
		price	 = request.form["price"]
		size	 = request.form["size"]
		ptype	 = request.form["type"]
		
		print(brand, name, batch, manfdate, exprydate, pid, price, size, ptype)
		bc = BlockChain()
		bc.addProduct(brand, name, batch, manfdate, exprydate, pid, price, size, ptype)
		
		flash("Certificate added successfully to the Blockchain")
		# return render_template('home.html')
		return redirect(url_for('index'))
	else:
		# return render_template('home.html')
		return redirect(url_for('index'))


@app.route("/admin")
def admin():
	if session["user"] == "Admin":
		return render_template('admin.html')
	else:
		return redirect(url_for('login'))


@app.route("/verifyNodes")
def verifyNodes():
	bc = BlockChain()
	isBV = bc.isBlockchainValid()

	if isBV:
		flash("All Nodes of Blockchain are valid")
		return redirect(url_for('admin'))
	else:
		flash("Blockchain Nodes are not valid")
		return redirect(url_for('admin'))





@app.route("/shoes")
def shoes():
	return render_template('index.html')



@app.route("/logout")
def logout():
	session["user"] = ""
	return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
    session["user"] = ""