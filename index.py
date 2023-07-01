import sys
import json
import random
import qrcode
import hashlib
import datetime

# from config import mycol

# VERIFICATION_URL = "http://localhost:8080/?id="
VERIFICATION_URL = "http://127.0.0.1:5000/verify/"

class Login:

	MANF = ""
	LOGGEDIN = False
	MANUFACTURERS = {
		"DRREDDY": "password123",
		"LUPIN": "hello123",
		"KOTLIN": "qwerty",
		"ADMIN": "qwerty"
	}

	def main(self):
		loginid = input("Enter your login id:\t")
		password = input("Enter your password:\t")

		if loginid in self.MANUFACTURERS.keys():
			if self.MANUFACTURERS[loginid] == password:
				self.LOGGEDIN = True
				self.MANF = loginid

	def isLoggedIn(self):
		if self.LOGGEDIN:
			print("\nWelcome to the blockchain world\n")
		else:
			sys.exit("Please login to experience the blockchain world")

	def getManf(self):
		return self.MANF


class BlockChain:

	def __init__(self):
		self.dept = ""
		self.name = ""
		self.batch = ""
		self.Jdate = ""
		self.date = ""
		self.id = ""
		self.marks = ""
		self.grade = ""
		self.course = ""


	def actions(self):
		choice = input("Enter 1 to ADD item or 2 to Verify BlockChain\n")

		if choice == "1":
			self.dept = input("Enter department:\n")
			self.name = input("Enter name:\n")
			self.batch = input("Enter batch:\n")
			self.Jdate = input("Enter Joining date:\n")
			self.date = input("Enter Duration:\n")
			self.id = input("Enter email:\n")
			self.marks = input("Enter marks:\n")
			self.grade = input("Enter grade:\n")
			self.course = input("Enter course:\n")
			self.newProduct()
		
		elif choice == "2":
			if self.isBlockchainValid():
				sys.exit("BlockChain is valid")
			else:
				sys.exit("BlockChain is invalid")

		else:
			sys.exit("Logged out successfully")

	
	def newProduct(self):
		data = {
			"Department": self.dept,
			"SName": self.name,
			"SBatch": self.batch,
			"JoiningDate": self.Jdate,
			"Duration": self.date,
			"SId": self.id,
			"SMarks": self.marks,
			"SGrade": self.grade,
			"SCourse": self.course,
		}

		proHash = hashlib.sha256(str(data).encode()).hexdigest()
		print(proHash)
		data["hash"] = proHash

		# x = mycol.insert_one(data)
		
		self.createBlock(data)

		imgName  = self.imgNameFormatting()
		self.createQR(proHash, imgName)

	def addProduct(
		self,
		dept,
		name,
		batch,
		Jdate,
		date,
		id,
		marks,
		grade,
		course
	):
		self.SName = name
		data = {
			"Department": dept,
			"SName": name,
			"SBatch": batch,
			"Joiningdate": Jdate,
			"Duration": date,
			"SId": id,
			"SMarks": marks,
			"SGrade": grade,
			"SCourse": course,
		}

		proHash = hashlib.sha256(str(data).encode()).hexdigest()
		print(proHash)
		data["hash"] = proHash

		# x = mycol.insert_one(data)
		
		self.createBlock(data)

		imgName  = self.imgNameFormatting()
		self.createQR(proHash, imgName)


	def createBlock(self, data):

		if self.isBlockchainValid():
			blocks = []
			for block in open('./NODES/N1/blockchain.json', 'r'):
				blocks.append(block)
			print(blocks[-1], "jsdata===========")

			preBlock = json.loads(blocks[-1])

			index = preBlock["index"] + 1
			preHash = hashlib.sha256(str(preBlock).encode()).hexdigest()

		transaction = {
			'index': index,
			'proof': random.randint(1, 1000),
			'previous_hash': preHash,
			# 'hash': proHash,
			'timestamp': str(datetime.datetime.now()),
			'data': str(data),
		}

		with open("./NODES/N1/blockchain.json", "a") as file:
			file.write("\n" + json.dumps(transaction))
		with open("./NODES/N2/blockchain.json", "a") as file:
			file.write("\n" + json.dumps(transaction))
		with open("./NODES/N3/blockchain.json", "a") as file:
			file.write("\n" + json.dumps(transaction))
		with open("./NODES/N4/blockchain.json", "a") as file:
			file.write("\n" + json.dumps(transaction))

		# currHash = hashlib.sha256(str(transaction).encode()).hexdigest()
		# imgName  = self.imgNameFormatting()

		# self.createQR(currHash, imgName)
		return


	def createQR(self, hashc, imgName):
		img = qrcode.make(VERIFICATION_URL + hashc)
		img.save("./QRcodes/" + imgName)

		# sys.exit("Product added successfully")
		return


	def imgNameFormatting(self):
		dt = str(datetime.datetime.now())
		dt = dt.replace(" ", "_").replace("-", "_").replace(":", "_")
		return self.name + "_" + dt + ".png"


	def isBlockchainValid(self):
		with open("./NODES/N1/blockchain.json", "r") as file:
			n1_hash = hashlib.sha256(str(file.read()).encode()).hexdigest()
			print(n1_hash)
		with open("./NODES/N2/blockchain.json", "r") as file:
			n2_hash = hashlib.sha256(str(file.read()).encode()).hexdigest()
			print(n2_hash)
		with open("./NODES/N3/blockchain.json", "r") as file:
			n3_hash = hashlib.sha256(str(file.read()).encode()).hexdigest()
			print(n3_hash)
		with open("./NODES/N4/blockchain.json", "r") as file:
			n4_hash = hashlib.sha256(str(file.read()).encode()).hexdigest()
			print(n4_hash)

		if n1_hash == n2_hash == n3_hash == n4_hash:
			return True
		else:
			return False


if __name__ == "__main__":
	lof = Login()
	lof.main()
	lof.isLoggedIn()

	LOGGEDINUSER = lof.getManf()

	bc = BlockChain()
	bc.actions()