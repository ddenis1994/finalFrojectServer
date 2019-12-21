from flask import Flask,request
#flask restful api import
from flask_restful import Resource,Api
#flask mongoDB api import
from flask_mongoengine import MongoEngine
import DB.MongoRepresent as user

app=Flask(__name__)
#add restrgful for the progrem
api=Api(app)
app.config["MONGODB_SETTINGS"] = {
	"db": "myapp",
}
db = MongoEngine(app);

@app.route('/')
def hello_world():
	return 'Hello,werld!'




class LogIn(Resource):
	def get(self):
		return {'hello':'test'}

	def post(self):
		username=request.form.get('username')
		password=request.form.get('password')
		print(username);
		return {'result':True,
				'code':123}

class SaveFile(Resource):
	def post(self):
		test=user(username="test1",userUniq="1")
		test.save()

		return {
			'result':True,
			'code':0
		}



api.add_resource(
	LogIn,
	'/api/login')
api.add_resource(
	SaveFile,
	'/api/login')


if __name__ == '__main__':
	app.run(debug=True)