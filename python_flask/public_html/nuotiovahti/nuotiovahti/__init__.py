import mysql.connector
from mysql.connector import errorcode
from flask import Flask, render_template, jsonify, json, request
app = Flask(__name__)



@app.route("/")
def main():
	return render_template('index.html')


@app.route('/data')
def getData():
	try:
	        cnx = mysql.connector.connect(option_files='connector.cnf')
	except mysql.connector.Error as err:
	        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
	                print("Something is wrong with your user name or password")
	        elif err.errno == errorcode.ER_BAD_DB_ERROR:
	                print("Database does not exist")
	        else:
	                print(err)
	else:
	        print("connected to database")


	cursor = cnx.cursor()
	print("gettin data damn it...")


	cursor.execute("select (select count(f.detection_time) from Flame as f where detection_time >now()- INTERVAL 300 SECOND) as flame, (select count(p.detection_time) from Pir as p where detection_time >now()- INTERVAL 300 SECOND) as pir;")

	datarows = jsonify(cursor.fetchall())

	cursor.close()
	cnx.close()

	return datarows


if __name__ == "__main__":
    app.run()

