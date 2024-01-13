from flask import Flask, render_template,redirect,url_for,request
import random
import sqlite3
import time
class Sqlite:
    def __init__(self):
        con = sqlite3.connect("messages.db")
        cur = con.cursor()
        self.con = con
        self.cur = cur
    def otpreturn(self,message):
        list = []
        
        self.cur.execute("SELECT otp FROM messages;")
        self.con.commit()
        data = self.cur.fetchall()
        for i in data:
            list.append(i[0])
        otp = random.randrange(100000,999999)
        while otp in list:
            otp = random.randrange(100000,999999)
        self.setdatabase(otp,message)
        return otp
    def setdatabase(self,otp,message):
        current_time = time.strftime("%a, %d %b %Y %H:%M:%S +0000",time.gmtime())
        self.cur.execute("INSERT INTO messages (otp,message,time) VALUES(?,?,?);",(otp,message,current_time))
        self.con.commit()
    def getdatabase(self,number):
        self.cur.execute(f"SELECT * FROM messages WHERE otp = {number};")
        self.con.commit()
        data = self.cur.fetchall()
        return data[0][1]
    def __del__(self):
        self.con.close()
class Dictionary:
   
    def __init__(self): 
        dic = {}
        print("creating object")
        self.dic = dic
    def setdatabase(self,otp,message):  
        self.dic[otp] = message
        print(self.dic)
        return None
    def otpreturn(self,message):
        otp = random.randrange(100000,999999)
        while otp in self.dic:
            otp = random.randrange(100000,999999)
        self.setdatabase(otp,message)
        return otp
    def getdatabase(self,number):
        print(self.dic)
        return self.dic[int(number)]
def main(bool:bool):
    if bool == True:
       object = Dictionary()
       return object
    else:
        object= Sqlite()
        return object
ravi = main(True)
app = Flask(__name__)
@app.route("/",methods = ["GET","POST"])
def home():
    
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        message = request.form.get("fmessage")
        number = request.form.get("fnumber")
        
        if message == None and number == None:
            return render_template("index.html")
        if message != None and number == None:
            otp = ravi.otpreturn(message)
            return render_template("index.html",fmessage = "ONE TIME OTP: ",fotp = otp)
        if message == None and number != None:
            string = ravi.getdatabase(number)
            return render_template("index.html",f2message = string)
    return render_template("index.html")

if __name__ == '__main__':
   app.run(debug=True)