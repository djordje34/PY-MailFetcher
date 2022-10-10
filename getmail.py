import imaplib
import email
from email.header import decode_header
import datetime as DT
import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
import pandas as pd


ukupno=0

def getMails():
    global address
    global password
    #print(transliterate.get_available_language_codes())
    
    #keywords=["predavanja","fakultet","vezbe","kolokvijum","ispit","predavanje","ispita","termin"]
    #select specific mails
    #searchString='OR "predavanja" "fakultet"'


    searchString='(OR (OR (OR (OR BODY predavanja BODY fakultet) (OR BODY vezbe BODY kolokvijum)) (OR (OR BODY ispit BODY predavanje) (OR TEXT moodle BODY termin))) (OR (OR BODY studenti BODY predmet) (FROM kg.ac.rs FROM no_reply_fink@kg.ac.rs)))'
    today = DT.date.today()
    week_ago = today - DT.timedelta(days=7)
    since=week_ago.strftime("%d-%b-%Y")
    searchString+=' SINCE '+since
    tempStr='BODY "predavanje"'

    gmail_host= 'imap.gmail.com'
    #set connection
    mail = imaplib.IMAP4_SSL(gmail_host)
    search_criteria = 'REVERSE DATE'

    #login
    
    mail.login(address, password)
    mail.select("INBOX")


    _, selected_mails = mail.search(None, searchString)
    
    global ukupno
    ukupno=len(selected_mails[0].split())
    return selected_mails,mail




def main():
    loginsc=tk.Tk()
    global address
    global emailVar
    global password
    global pswdVar
    emailVar = tk.StringVar()
    pswdVar=tk.StringVar()
    
    readerl=open("charmander.txt","r")
    readerp=open("pikachu.txt","r")
    content = readerl.read()
    contentP=readerp.read()
    if(content):
        address=content
        emailVar.set(address)
        password=contentP
        pswdVar.set(password)

    def Logs():
        global emailVar
        global pswdVar
        global address
        global password
        address = emailVar.get()
        password=pswdVar.get()
        loginsc.destroy()
    
    loginsc.title("mailFetcher 0.1")
    loginsc.geometry("1080x680")
    loginsc.config(bg="white")
    emailField=Entry(width=30,font=("Arial",20),bg='lawn green',borderwidth=0,textvariable=emailVar)
    password=Entry(width=30,font=("Arial",20),show="*",bg='lawn green',borderwidth=0,textvariable=pswdVar)
    Label(text="E-mail adresa").pack(pady=(80,0))
    emailField.pack(pady=(0,40),anchor=CENTER)
    Label(text="E-mail Passcode").pack()
    password.pack(pady=(0,40),anchor=CENTER)
    loginBtn=Button(command=Logs,text="Ulogujte se",borderwidth=0,bg='lawn green',width=10,height=2,font=("Arial",13)).pack()
    loginsc.mainloop()  #dodaj za logger da loguje
        
    global counter
    counter=-1
    def Counter():

        window.grab_set()

        global counter
        
        S.configure(state="normal")
        F.configure(state="normal")
        D.configure(state="normal")
        M.configure(state="normal")
        
        num=selected_mails[0].split()[len(selected_mails[0].split())-counter-1]
        S.delete("1.0","end")
        F.delete("1.0","end")
        D.delete("1.0","end")
        M.delete("1.0","end")
        S.insert(tk.END,'Tema: ')
        F.insert(tk.END,'Od: ')
        D.insert(tk.END,'Datum: ')
        
        _, data = mail.fetch(num , '(RFC822)')
        _, bytes_data = data[0]

        #convert the byte data to message
        email_message = email.message_from_bytes(bytes_data)

        #print (urllib.parse.unquote(str(email_message)))
        #translit(, 'ka', reversed=True)
        #access data
        #subject=decode_header(email_message["subject"])[0]
        fromWhoBBB=''
        if(email_message['from'][0]=='"'):
            fromWhoBBB=email_message["from"].split(' ')[1]
        subject,encSub=decode_header(email_message["subject"])[0]
        fromWho,encFrom=decode_header(email_message["from"])[0]
        
        if encSub:
            subject=subject.decode('utf-8','replace')
        if fromWhoBBB!='':
            fromWho=fromWhoBBB
        if encFrom:
            fromWho=fromWho.decode('utf-8','replace')
        #fromWho=email_message["from"]
        #print("Subject: ",subject[0])
    
        
        S.insert(tk.END, subject)
        S.pack(fill=BOTH,expand=1)
        #print("From: ",fromWho[0])
        F.insert(tk.END, fromWho)
        F.pack(fill=BOTH,expand=1)
        #print("Date: ",email_message["date"])
        D.insert(tk.END, email_message["date"])
        D.pack(fill=BOTH,expand=1)
        for part in email_message.walk():
            if part.get_content_type()=="text/plain" or part.get_content_type()=="text/html":
                message = part.get_payload(decode=True)
                #print("Message: \n", message.decode())
                M.insert(tk.END,message.decode())
                
                #print("==========================================\n")
                break
            M.pack(fill=BOTH,expand=1)
            
        global ukupno
        
        CTR.config(text=str(counter+1)+"/"+str(ukupno))
        CTR.pack(fill=BOTH)
        
        S.configure(state="disabled")
        F.configure(state="disabled")
        D.configure(state="disabled")
        M.configure(state="disabled")
        
        
        window.grab_release()

    def counterForward():
        global counter
        counter+=1
        if counter==len(selected_mails[0].split()):
            counter=0
        
    def incCounter():
        counterForward()
        Counter()
        
    def counterBackward():
        global counter
        counter-=1
        if counter==-1:
            counter=len(selected_mails[0].split())-1
        
    def decCounter():
        counterBackward()
        Counter()
        
    def shortcutRight(event):
        incCounter()    
        
    def shortcutLeft(event):
        decCounter()
        
    def shortcutExit(event):
        window.destroy()
        
    selected_mails,mail=getMails()
    window=tk.Tk()
    logins = open("charmander.txt","w+")
    passws=open("pikachu.txt","w+")
    logins.write(address+"\n")
    passws.write(password+"\n")
    
    window.bind('<Right>', shortcutRight)
    window.bind('<Left>', shortcutLeft)
    window.bind('<Escape>', shortcutExit)
    window.title("mailFetcher 0.1")
    window.geometry("1080x680")
    window.config(bg="white")
    frame1 = Frame(window)
    frame1.config(bg="white")
    window.wm_attributes("-transparentcolor", 'grey')
    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.configure(size=15,family='Arial')
    S=tk.Text(window,height=3,width=60,font=default_font)
    F=tk.Text(window,height=2,width=60,font=default_font)
    D=tk.Text(window,height=1,width=60,font=default_font)
    M=tk.Text(window,height=12,width=60,font=default_font)
    B=tk.Button(frame1, text = "Dalje",command=incCounter,bg="lawn green", borderwidth=0,activeforeground="lawn green",activebackground="white")
    P=tk.Button(frame1, text = "Prethodni",command=decCounter,bg="lawn green", borderwidth=0,activeforeground="lawn green",activebackground="white")
    global ukupno

    U=Label(text="Pronađeno ukupno "+str(ukupno)+" mejlova vezanih za fakultet",bg="lawn green")
    #frame1 = Frame(window)
    #frame1.pack(side="top")
    U.pack(anchor=N,fill=BOTH)
    B.pack(side="right",anchor=N,padx=10)
    P.pack(side="left",anchor=N,padx=10)
    frame1.pack()
    CTR=Label(text=str(counter+1)+"/"+str(ukupno),bg="deep sky blue")
    incCounter()
        
    
    window.mainloop()
if __name__=="__main__":
    main()
