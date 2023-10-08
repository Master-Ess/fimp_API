from flask import Flask, request, jsonify
import psycopg2
import random

#host="dpg-ckefq85tj22c73e17aag-a.singapore-postgres.render.com" --> for local machine

#host="dpg-ckefq85tj22c73e17aag-a" -- for q online

connection = psycopg2.connect(
        host="dpg-ckefq85tj22c73e17aag-a",
        database="fimpdatabase",
        user="base",
        password="QCGu3Zeq9F2tJb1lqjhETHH4qbjf66sY"
    )

app = Flask(__name__)


########## routes

@app.route("/")
def home():
    return "API CONNECTED - FIMP DATABASE CONNECTED"

@app.route("/login/<email>/<hash>")
def login(email, hash):
    return check_pswrd(email, hash)

@app.route("/nuser/<email>/<hash>")
def nsuer(email, hash):
    return create_new_user(email, hash)

@app.route("/nuser/<email>/<hash>/<gender>/<school>/<DOB>/<suburb>/<fname>")


@app.route("/count") #testing call remove before prod
def count():
    return str(get_max_entries('affirmations'))

@app.route("/randaff")
def randaff():
    return str(random_affirmation())


###################


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

def create_new_user_max(email, pswrd, gender, school, DOB, suburb, Fname):
    cursor = connection.cursor()

    #requires clensing espc DOB --> format is YYYY/MM/DD

    str_code = 'INSERT INTO public."user" (email,"password",gender,school,dob,suburb,fname)' + " VALUES('" + email +"', '" + pswrd + "', '"+ gender +"', '"+ school +"', '"+ DOB +"', '"+"', '"+ suburb + "', '" + Fname +  "')"
    print(str_code)
    cursor.execute(str_code)

    connection.commit()

    cursor.close()

    return "User created with name: " + Fname

def get_max_entries(table):
    cursor = connection.cursor()

    str_code = 'SELECT COUNT(*) AS row_count FROM public.' + table
    print(str_code)
    cursor.execute(str_code)

    results = cursor.fetchall()

    cursor.close()

    return results[0][0]

def random_affirmation():
    maxaf =  get_max_entries('affirmations')
    rand_aff = random.randint(1,maxaf)

    cursor = connection.cursor()

    str_code = 'SELECT contents FROM public.affirmations WHERE id = ' + str(rand_aff)
    print(str_code)
    cursor.execute(str_code)

    results = cursor.fetchall()[0][0]

    cursor.close()
    return results

    

if (__name__) == "__main__":
    app.run(debug=True)