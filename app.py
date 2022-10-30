
from flask import Flask, render_template, redirect, request
#from pymongo import MongoClient 
from flask_mysqldb import MySQL
from random import randint


app = Flask(__name__, template_folder='templates')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'ara1'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'ncdw'
 
mysql = MySQL(app)

def gb(fm):
    global firstname1
    firstname1=fm

@app.route('/', methods=['GET',"POST"])
def reg():
    return render_template('register.html')

@app.route('/register', methods=['GET',"POST"])
def register():
    
    firstname=" "
    lastname = " "
    gender = " "
    birthday = " "
    pincode = " "
    score=" "
    remarks=" "
    patient_id=" "
    # if request.method == 'GET':
        # return "Login via the login Form"
    if request.method == "POST":
        firstname = request.form['firstName']
        lastname = request.form['secondName']
        gender = request.form['Gender']
        birthday = request.form['DOB']
        pincode = request.form["pin number"]
        gb(firstname)
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT patient_id from user')
        pid=cursor.fetchall()
    
        if(len(pid)>0):
            for i in pid:
                id=random_n_digits(14)
                if(id!=i):
                    cursor.execute(' INSERT INTO user VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',(id,firstname,lastname,gender,birthday,pincode,score,remarks,))

                    mysql.connection.commit()
                    msg='Successfully registered !'
                    break
                else:
                    continue
                
        else:
            id=random_n_digits(14)
            cursor.execute(' INSERT INTO user VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',(id,firstname,lastname,gender,birthday,pincode,score,remarks))
            mysql.connection.commit()
    cursor.execute('SELECT patient_id from user WHERE firstname=%s',[firstname])
    patient_id= cursor.fetchone()
    return render_template('araa.html',id=id)
def random_n_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

    

@app.route('/araa', methods=['GET',"POST"])
def home():
    
    if request.method == "POST":
        # while True:
        Age = request.form.get('age')
        Smoke = request.form.get('smoke')
        Alcohol = request.form.get('alcohol')
        Waist = request.form.get('waist')
        Activity = request.form.get('activity')
        History = request.form.get('history')
    #     cursor = mysql.connection.cursor()
    #     cursor.execute(''' INSERT INTO user VALUES(%s,%s,%s,%s,%s)''',(
    #         {"firstname":firstname},
    #     {"$set": {"age" :Age,
    #     'smoke': Smoke,
    #      "alcohol":Alcohol,
    #     "waist":Waist,
    #     "activity":Activity,
    #     "history":History}}
    
    # ))
        score = float(Age) + float(Smoke)+float(Alcohol)+float(Waist) + float(Activity)+float(History)
        # global add
        add=score  
        # global res
        res=" "
        if score>4:
            res="screening needed"
            
        else:
            res="no need to screen"

        cursor = mysql.connection.cursor()
        #cursor.execute(''' INSERT INTO user VALUES(%f)''',(add))
        cursor.execute('UPDATE user SET score = %s, remarks =%s  WHERE firstname=%s',(score,res,firstname1))
        #cursor.execute('UPDATE user SET  username =% s, password =% s, email =% s,  WHERE id =% s', (username, password, email(session['id'], ), ))
        mysql.connection.commit()
        return render_template('result.html', add1=add,res=res,fnm=firstname1)
    return render_template('araa.html')



@app.route('/back',methods=['POST','GET'])
def back():
    if request.method=='POST':
        return render_template('register.html')


if __name__ == "__main__":
    #  try:
    #     client = MongoClient("mongodb://localhost:27017")
    #     db = client['patientData']
    #     Collection = db["mysamecollectionforpatient"]
    #     # client.server_info() #trigger exception if it cannot connect to database
        
    #  except Exception as e:
    #     print(e)
    #     print("Error - Cannot connect to database")
     app.run(debug=True)