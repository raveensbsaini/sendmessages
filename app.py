from flask import Flask, render_template,redirect,url_for,request
import random
import sqlite3
import time

app = Flask(__name__)
@app.route("/",methods = ["GET","POST"])
def ravi():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        message = request.form.get("fmessage")
        number = request.form.get("fnumber")
        print(message,number)
        if message == None and number == None:
            return render_template("index.html")
        if message != None and number == None:
            print("second func")
            otp = random.randrange(100000,999999) 
            con = sqlite3.connect("messages.db")
            cur = con.cursor()
            cur.execute("SELECT otp FROM messages;")
            data = cur.fetchall()
            print(data,type(data),data[1],type(data[1]))
            con.close()
            list = []
            for  i in data:
                list.append(i[0])
            while otp in list:
                otp = random.randrange(100000,999999)
            current_time = time.strftime("%H:%M:%S", time.localtime())
            con = sqlite3.connect("messages.db")
            cur = con.cursor()
            cur.execute(f"INSERT INTO messages (otp,message,time) VALUES({otp},'{message}','{current_time}');")
            con.commit()
            con.close()
            return render_template("index.html",fmessage = message,fotp = otp)
        if message == None and number != None:
            number = int(number)
            con = sqlite3.connect("messages.db")
            cur = con.cursor()
            cur.execute(f"SELECT message FROM messages where otp = {number};")
            data = cur.fetchall()
            print(data,type(data))
            string = data[0][0]
            con.close()
            return render_template("index.html",f2message = string)
    return render_template("index.html")

if __name__ == '__main__':
   app.run(debug=True)