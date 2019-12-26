from flask import Flask,request,jsonify
# flask restful api import
from flask_restful import Resource,Api
# flask mongoDB api import
from flask_pymongo import PyMongo
from pymongo import MongoClient


import json

app=Flask(__name__)
# add resentful for the program
api = Api(app)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo=PyMongo(app)

client = MongoClient('localhost', 27017)
db = client['local']
collection = db['testDB']


@app.route('/')
def hello_world():
	return 'Hello,werld!'




class LogIn(Resource):
	def get(self):
		username = request.form.get('username')
		password = request.form.get('password')
		print(username)
		return {'result':True}

	def post(self):
		d = {'website': 'www.carrefax.com', 'author': 'Daniel Hoadley', 'colour': 'purple'}

		# Insert the dictionary into Mongo
		collection.insert(d)
		username=request.form.get('username')
		password=request.form.get('password')
		answer={}
		answer['result']=True
		return jsonify(answer)

class SaveFile(Resource):
	def post(self):

		username = request.form.get('username')
		password = request.form.get('password')
		print(username)
		mongo.send_file("test",username)


		return {
			'result':True,
			'code':0
		}



api.add_resource(
	LogIn,
	'/api/login')
api.add_resource(
	SaveFile,
	'/api/newData')


if __name__ == '__main__':
	app.run(debug=True)