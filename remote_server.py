from flask import Flask,request
#flask restful api import
from flask_restful import Resource,Api

app=Flask(__name__)
#add restrgful for the progrem
api=Api(app)

@app.route('/')
def hello_world():
	return 'Hello,werld!'




class LogIn(Resource):
	def get(self):
		return {'hello':'test'}

	def post(self):
		username=request.form.get('username')
		password=request.form.get('password')
		return {'hello':request.form.get('username')}




api.add_resource(
	LogIn,
	'/api/login')


if __name__ == '__main__':
	app.run(debug=True)