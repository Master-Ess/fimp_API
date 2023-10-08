from flask import Flask, request, jsonify
import psycopg2


#host="dpg-ckefq85tj22c73e17aag-a.singapore-postgres.render.com" --> for local machine

#host="dpg-ckefq85tj22c73e17aag-a" -- for q online

connection = psycopg2.connect(
        host="dpg-ckefq85tj22c73e17aag-a",
        database="fimpdatabase",
        user="base",
        password="QCGu3Zeq9F2tJb1lqjhETHH4qbjf66sY"
    )

app = Flask(__name__)

@app.route("/")
def home():
    return "API CONNECTED - FIMP DATABASE CONNECTED"

@app.route("/login/<email>/<hash>")
def login(email, hash):
    return check_pswrd(email, hash)

@app.route("/nuser/<email>/<hash>")
def nsuer(email, hash):
    return create_new_user(email, hash)


def sql_get(table, qualifyer, request):
    cursor = connection.cursor()

    str_code = "SELECT " + str(request) + ' FROM public."' + str(table) + '" WHERE ' + str(qualifyer) 
    print(str_code)
    cursor.execute(str_code)

    results = cursor.fetchall()

    if len(results) > 1:
        print("results larger then 1 ignoring values")

    if results != None:
        res = results[0][0] #assumes only one value is returned will ignore anymore then the first
    else:
        return "No Data Found"

    cursor.close()
    

    return res

def check_pswrd(email, hash):
    stored_hash = sql_get("user", "email = '"  + email + "'" , '"password"')

    if stored_hash == hash:
        return "True"
    return "False"

def create_new_user(email, pswrd):
    cursor = connection.cursor()

    str_code = 'INSERT INTO public."user" (email, "password")' + " VALUES('" + email +"', '" + pswrd + "')"
    print(str_code)
    cursor.execute(str_code)

    connection.commit()

    cursor.close()

    return "ran the following command: " + str_code



if (__name__) == "__main__":
    app.run(debug=True)