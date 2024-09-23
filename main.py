import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox as mb
from tkinter.simpledialog import askstring
from PIL import ImageTk, Image
import mysql.connector

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class LoginForm:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="748596",
            database="loginform",
            autocommit=True
        )
        self.mc = self.db.cursor()

        self.app = ctk.CTk()
        self.imgBg = ImageTk.PhotoImage(Image.open("pattern.png"))
        self.imgDark = ctk.CTkImage(Image.open("darkmd.png").resize((20,20), Image.Resampling.LANCZOS))
        self.imgLight = ctk.CTkImage(Image.open("lightmode.png").resize((20,20), Image.Resampling.LANCZOS))
        self.labelBg = ctk.CTkLabel(self.app, image=self.imgBg)
        self.frame = ctk.CTkFrame(self.labelBg, width=320, height=475, corner_radius=15)
        self.lText = ctk.CTkLabel(self.frame, text="Login", font=("Century Gothic", 20), width=50)
        self.eUser = ctk.CTkEntry(self.frame, width=220, placeholder_text="Username (not required)", font=("Century Gothic", 15))
        self.eMail = ctk.CTkEntry(self.frame, width=220, placeholder_text="E-Mail (not required)", font=("Century Gothic", 15))
        self.ePass = ctk.CTkEntry(self.frame, width=220, placeholder_text="Password", show="*", font=("Century Gothic", 15))
        self.butLog = ctk.CTkButton(self.frame,  width=220, height=40, text="Signup", corner_radius=6, font=("Century Gothic", 18), 
                     command=self.funcLog)
        self.butForget = ctk.CTkButton(self.frame, text="Forget password", font=("Century Gothic", 14), corner_radius=6, 
                          fg_color="#2b2b2b", hover_color="#242424", command=self.forgetPass)
        self.imgGoogle = ctk.CTkImage(Image.open("Google__G__Logo.svg.webp").resize((20,20), Image.Resampling.LANCZOS))
        self.imgFace = ctk.CTkImage(Image.open("124010.png").resize((20,20), Image.Resampling.LANCZOS))
        self.butGoogle = ctk.CTkButton(self.frame, width=100, height=20, image=self.imgGoogle, text="Google", corner_radius=6, 
                                       compound="left", text_color="Black", fg_color="white", hover_color="#a4a4a4")
        self.butFace = ctk.CTkButton(self.frame, width=100, height=20, image=self.imgFace, text="Facebook", corner_radius=6, 
                                     compound="left", text_color="Black", fg_color="white", hover_color="#a4a4a4")
        self.butReg = ctk.CTkButton(self.frame, text="Don't You Have Account? Register!", font=("Century Gothic", 14), corner_radius=6, 
                          fg_color="#2b2b2b", hover_color="#242424", command=self.funcReg, width=220)
        self.butAppMode = ctk.CTkButton(self.frame, image=self.imgLight, corner_radius=6, fg_color="#2b2b2b", hover_color="#242424", text="",
                           width=50, command=self.changeAppMode)
        self.appMode = "dark"

    def showMes(self, Type, text):
        typy = str(Type).lower()
        if typy == "info":
            mb.showinfo("Login", f"{text}")
        elif typy == "error":
            mb.showerror("Login", f"{text}")
        elif typy == "warn":
            mb.showwarning("Login", f"{text}")

    def getEmails(self):
        self.mc.execute("SELECT email FROM account")
        emails = self.mc.fetchall()
        return emails

    def getUsers(self):
        self.mc.execute("SELECT username FROM account")
        usernm = self.mc.fetchall()
        return usernm

    def getPasses(self):
        self.mc.execute("SELECT passwd FROM account")
        passes = self.mc.fetchall()
        return passes

    def getIDs(self):
        self.mc.execute("SELECT id FROM account")
        ids = self.mc.fetchall()
        return ids

    def isSameP(self, passwd):
        passes = self.getPasses()
        for i in passes:
            if passwd == i[0]:
                return True
        return False

    def isSameU(self, user):
        users = self.getUsers()
        for i in users:
            if user == i[0]:
                return True
        return False

    def isSameM(self, email):
        emails = self.getEmails()
        for i in emails:
            if email == i[0]:
                return True
        return False

    def run(self):
        self.app.geometry("640x535")
        self.app.title("Login")

        self.labelBg.pack()
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.lText.place(x=130, y=45)
        self.eUser.place(x=50, y=110)
        self.eMail.place(x=50, y=165)
        self.ePass.place(x=50, y=220)
        self.butForget.place(x=135, y=250)
        self.butLog.place(x=50,y=295)
        self.butGoogle.place(x=50,y=345)
        self.butFace.place(x=170,y=345)
        self.butReg.place(x=35, y=395)
        self.butAppMode.place(x=270, y=0)
        
        self.app.mainloop()

    def funcLog(self):
        user = self.eUser.get()
        mail = self.eMail.get()
        passwd = self.ePass.get()

        if passwd != "" or passwd == None:
            if user == "" and mail == "":
                self.showMes("error", "You Must Enter Email or Username!")
            elif user == "" and mail != "":
                if self.isSameP(passwd) == False and self.isSameM(mail) == False:
                    self.showMes("error", "E-Mail and Password is Wrong!")
                elif self.isSameP(passwd) == False and self.isSameM(mail):
                    self.showMes("error", "Password is Wrong!")
                elif self.isSameP(passwd) and self.isSameM(mail) == False:
                    self.showMes("error", "E-Mail is Wrong!")
                else:
                    self.showMes("info", "You Successfully Logged in!")
                    self.openHomePage()
            elif user != "" and mail == "":
                if self.isSameP(passwd) == False and self.isSameU(user) == False:
                    self.showMes("error", "Username and Password is Wrong!")
                elif self.isSameP(passwd) == False and self.isSameU(user):
                    self.showMes("error", "Password is Wrong!")
                elif self.isSameP(passwd) and self.isSameU(user) == False:
                    self.showMes("error", "Username is Wrong!")
                else:
                    self.showMes("info", "You Successfully Logged in!")
                    self.openHomePage()
            else:
                if self.isSameP(passwd) == False and self.isSameU(user) == False and self.isSameM(mail) == False:
                    self.showMes("error", "Username, Password and E-Mail is Wrong!")
                elif self.isSameP(passwd) == False and self.isSameU(user)  and self.isSameM(mail) == False:
                    self.showMes("error", "Password and E-Mail is Wrong!")
                elif self.isSameP(passwd) and self.isSameU(user) == False  and self.isSameM(mail) == False:
                    self.showMes("error", "Username and E-Mail is Wrong!")
                elif self.isSameP(passwd) and self.isSameU(user) and self.isSameM(mail) == False:
                    self.showMes("error", "E-Mail is Wrong!")
                elif self.isSameP(passwd) == False and self.isSameU(user) and self.isSameM(mail):
                    self.showMes("error", "Password is Wrong!")
                elif self.isSameP(passwd) and self.isSameU(user) == False and self.isSameM(mail):
                    self.showMes("error", "Username is Wrong!")
                else:
                    self.showMes("info", "You Successfully Logged in!")
                    self.openHomePage()
        elif user == "" and mail == "" and passwd == "":
            self.showMes("error", "You Must Enter Password, Email and Username!")
        else:
            self.showMes("error", "You Must Enter Password!")

    def forgetPass(self):
        sql = "UPDATE account SET passwd=%s WHERE email=%s"
        email = askstring("Login", "Enter E-Mail : ")
        if self.isSameM(email) == False:
            self.showMes("Login", "There is no account with this E-Mail!")
        else:
            newPass = askstring("Login", "Enter your new password : ", show="*")
            val = (newPass, email)
            self.showMes("Login", "Your password is successfully changed!")
            self.mc.execute(sql, val)
            self.db.commit()            

    def funcReg(self):
        self.app.destroy()
        reg = RegisterForm()
        reg.run()
        
    def changeAppMode(self):
        # Change to Light
        if self.appMode == "dark":
            ctk.set_appearance_mode("light")
            self.butAppMode.configure(image=self.imgDark, fg_color="#dddddd", hover_color="#aaaaaa")
            self.butReg.configure(fg_color="#dddddd", hover_color="#aaaaaa", text_color="#000000")
            self.butForget.configure(fg_color="#dddddd", hover_color="#aaaaaa", text_color="#000000")
            self.appMode = "light"
        # Change to Dark
        elif self.appMode == "light":
            ctk.set_appearance_mode("dark")
            self.butAppMode.configure(image=self.imgLight, fg_color="#2b2b2b", hover_color="#242424")
            self.butReg.configure(fg_color="#2b2b2b", hover_color="#242424", text_color="#ffffff")
            self.butForget.configure(fg_color="#2b2b2b", hover_color="#242424", text_color="#ffffff")
            self.appMode = "dark"

    def openHomePage(self):
        self.app.destroy()
        w = ctk.CTk()
        w.geometry("1280x720")
        w.title("Welcome")
        l1 = ctk.CTkLabel(w, text="Home Page", font=("Century Gothic", 100))
        l1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        w.mainloop()

    def printInfo(self):
        self.mc.execute("SELECT * FROM account")
        return self.mc.fetchall()

class RegisterForm:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="748596",
            database="loginform",
            autocommit=True
        )
        self.mc = self.db.cursor()

        self.app = ctk.CTk()
        self.imgBg = ImageTk.PhotoImage(Image.open("pattern.png"))
        #self.imgBg = ctk.CTkImage( Image.open("pattern.png"))
        #self.imgBg = ctk.CTkImage( ImageTk.PhotoImage(Image.open("pattern.png")))
        
        self.imgDark = ctk.CTkImage(Image.open("darkmd.png").resize((20,20), Image.Resampling.LANCZOS))
        self.imgLight = ctk.CTkImage(Image.open("lightmode.png").resize((20,20), Image.Resampling.LANCZOS))
        
        self.labelBg = ctk.CTkLabel(master=self.app, image=self.imgBg) #self.labelBg = ctk.CTkLabel(self.app, image=self.imgBg)
        self.frame = ctk.CTkFrame(self.labelBg, width=320, height=495, corner_radius=15)
        self.lText = ctk.CTkLabel(self.frame, text="Signup", font=("Century Gothic", 20), width=50)
        self.eMail = ctk.CTkEntry(self.frame, width=220, placeholder_text="E-Mail", font=("Century Gothic", 15))
        self.eUser = ctk.CTkEntry(self.frame, width=220, placeholder_text="Username", font=("Century Gothic", 15),)
        self.ePass1 = ctk.CTkEntry(self.frame, width=220, placeholder_text="Password", show="*", font=("Century Gothic", 15))
        self.ePass2 = ctk.CTkEntry(self.frame, width=220, placeholder_text="Password Again", show="*", font=("Century Gothic", 15))
        self.butReg = ctk.CTkButton(self.frame,  width=220, height=40, text="Signup", corner_radius=6, font=("Century Gothic", 18), 
                     command=self.funcReg)
        self.imgGoogle = ctk.CTkImage(Image.open("Google__G__Logo.svg.webp").resize((20,20), Image.Resampling.LANCZOS))
        self.imgFace = ctk.CTkImage(Image.open("124010.png").resize((20,20), Image.Resampling.LANCZOS))
        self.butGoogle = ctk.CTkButton(self.frame, width=100, height=20, image=self.imgGoogle, text="Google", corner_radius=6, 
                                       compound="left", text_color="Black", fg_color="white", hover_color="#a4a4a4")
        self.butFace = ctk.CTkButton(self.frame, width=100, height=20, image=self.imgFace, text="Facebook", corner_radius=6, 
                                     compound="left", text_color="Black", fg_color="white", hover_color="#a4a4a4")
        self.butLogin = ctk.CTkButton(self.frame, text="Do You Have Account? Login!", font=("Century Gothic", 14), corner_radius=6, 
                          fg_color="#2b2b2b", hover_color="#242424", command=self.funcLogin, width=220)
        self.butAppMode = ctk.CTkButton(self.frame, image=self.imgLight, corner_radius=6, fg_color="#2b2b2b", hover_color="#242424", text="",
                           width=50, command=self.changeAppMode)
        self.appMode = "dark"

    def showMes(self, Type, text):
        typy = str(Type).lower()
        if typy == "info":
            mb.showinfo("Register", f"{text}")
        elif typy == "error":
            mb.showerror("Register", f"{text}")
        elif typy == "warn":
            mb.showwarning("Register", f"{text}")

    def getEmails(self):
        self.mc.execute("SELECT email FROM account")
        emails = self.mc.fetchall()
        return emails

    def getUsers(self):
        self.mc.execute("SELECT username FROM account")
        usernm = self.mc.fetchall()
        return usernm

    def getPasses(self):
        self.mc.execute("SELECT passwd FROM account")
        passes = self.mc.fetchall()
        return passes

    def getIDs(self):
        self.mc.execute("SELECT id FROM account")
        ids = self.mc.fetchall()
        return ids

    def addPerson(self, usernm, passwd, email):
        sql = "INSERT INTO account (username, passwd, email) VALUES (%s, %s, %s)"
        val = (usernm, passwd, email)
        self.mc.execute(sql, val)

    def getSize(self):
        ids = self.getIDs()
        size = len(ids)
        return size

    def isSameE(self, email):
        emails = self.getEmails()
        for i in emails:
            if email == i[0]:
                return int(1)
        return int(0)
            
    def isSameU(self, user):
        users = self.getUsers()
        for i in users:
            if user == i[0]:
                return int(1)
        return int(0)

    def run(self):
        self.app.geometry("640x600")
        self.app.title("Register")

        self.labelBg.pack()
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.lText.place(x=130, y=50)
        self.eMail.place(x=50, y=110)
        self.eUser.place(x=50, y=165)
        self.ePass1.place(x=50, y=220)
        self.ePass2.place(x=50, y=275)
        self.butReg.place(x=50,y=330)
        self.butGoogle.place(x=50,y=385)
        self.butFace.place(x=170,y=385)
        self.butLogin.place(x=50, y=430)
        self.butAppMode.place(x=270, y=0)
        
        self.app.mainloop()

    def changeAppMode(self):
        # Change to Light
        if self.appMode == "dark":
            ctk.set_appearance_mode("light")
            self.butAppMode.configure(image=self.imgDark, fg_color="#dddddd", hover_color="#aaaaaa")
            self.butLogin.configure(fg_color="#dddddd", hover_color="#aaaaaa", text_color="#000000")
            self.appMode = "light"
        # Change to Dark
        elif self.appMode == "light":
            ctk.set_appearance_mode("dark")
            self.butAppMode.configure(image=self.imgLight, fg_color="#2b2b2b", hover_color="#242424")
            self.butLogin.configure(fg_color="#2b2b2b", hover_color="#242424", text_color="#ffffff")
            self.appMode = "dark"

    def funcReg(self):
        # Variables
        user = self.eUser.get()
        pass1 = self.ePass1.get()
        pass2 = self.ePass2.get()
        email = self.eMail.get()
        uState = 0
        eState = 0

        # Statement
        if pass1 != pass2:
            self.showMes("error", "Passwords are not same!")
        else:
            eState += self.isSameE(email=email)
            uState += self.isSameU(user=user)
            if eState == uState and eState == 1:
                self.showMes("error", "There is already an account with this username and email!")
            elif uState == 1:
                self.showMes("error", "There is already an account with this username!")
            elif eState == 1:
                self.showMes("error", "There is already an account with this email!")
            else:
                self.reg(user=user, pass1=pass1, email=email)
    
    def funcLogin(self):
        self.app.destroy()
        logForm = LoginForm()
        logForm.run()

    def reg(self, user, pass1, email):
        self.addPerson(user, pass1, email)
        self.showMes("info", f"{self.printInfo()}")
        self.db.commit()
        self.openHomePage()

    def openHomePage(self):
        self.app.destroy()
        w = ctk.CTk()
        w.geometry("1280x720")
        w.title("Welcome")
        l1 = ctk.CTkLabel(w, text="Home Page", font=("Century Gothic", 100))
        l1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        w.mainloop()

    def printInfo(self):
        self.mc.execute("SELECT * FROM account")
        return self.mc.fetchall()

log = LoginForm()
#log = RegisterForm()
log.run()