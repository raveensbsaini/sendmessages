from flask import Flask, render_template,redirect,url_for,request
import random
import sqlite3
import time
class Sqlite:
    def __init__(self,message,number):
        self.message = message
        self.number = number
    def otpreturn(self):
        list = []
        con = sqlite3.connect("messages.db")
        cur = con.cursor()
        cur.execute("SELECT otp FROM messages;")
        con.commit()
        data = cur.fetchall()
        for i in data:
            list.append(i[0])
        otp = random.randrange(100000,999999)
        while otp in list:
            otp = random.randrange(100000,999999)
        con.close()
        return otp
    def setdatabase(self,otp):
        current_time = time.strftime("%a, %d %b %Y %H:%M:%S +0000",time.gmtime())
        con = sqlite3.connect("messages.db")
        cur = con.cursor()
        cur.execute(f"INSERT INTO messages (otp,message,time) VALUES({ otp },'{ self.message}','{ current_time}');")
        con.commit()
        con.close()
    def getdatabase(self):
        con = sqlite3.connect("messages.db")
        cur = con.cursor()
        cur.execute(f"SELECT * FROM messages WHERE otp = {self.number};")
        con.commit()
        data = cur.fetchall()
        con.close()
        return data[0][1]

class Dictionary:
    dic = {}
    def __init__(self,message,number):
        self.message = message
        self.number = number
    def setdatabase(self,otp):  
        self.dic[otp] = self.message
        return None
    def otpreturn(self):
        otp = random.randrange(100000,999999)
        while otp in self.dic:
            otp = random.randrange(100000,999999)
        return otp
    def getdatabase(self):
        return self.dic[int(self.number)]
def main(bool: bool,message,number):
    if bool == True:
       object = Dictionary(message,number)
       return object
    else:
        object= Sqlite(message,number)
        return object

app = Flask(__name__)
@app.route("/",methods = ["GET","POST"])
def ravi():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        message = request.form.get("fmessage")
        number = request.form.get("fnumber")
        ravi = main(False,message,number)
        if message == None and number == None:
            return render_template("index.html")
        if message != None and number == None:
            otp = ravi.otpreturn()
            ravi.setdatabase(otp)
            return render_template("index.html",fmessage = "ONE TIME OTP: ",fotp = otp)
        if message == None and number != None:
            string = ravi.getdatabase()
            return render_template("index.html",f2message = string)
    return render_template("index.html")

if __name__ == '__main__':
   app.run(debug=True)