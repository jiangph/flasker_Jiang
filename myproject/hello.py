from flask import Flask

app=Flask(__name__)
@app.route('/')
def hello():
	response="<html>\n"
	response+="<title>Flask test</title>\n"
	response+="<body>\n"
	response+="<h2>Hello world</h2>"
	response+="</body>\n"
	response+="</html>\n"
	return response

if __name__=="__main__":
	app.run(host="0.0.0.0",port=8080,debug=True)