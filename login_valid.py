#!/usr/bin/python2

import os
from main_menu import main_menu
#######################################Recv_function#########################################################################
def recv_fun(client):                                    #This function recieve data from client
    data = ""
    while True:
        part = client.recv(1)
	data = data + part
        if part=="~":
	         break
    return data.rstrip("~")
##############################################################################################################################################


def login_valid(client):                                           #for authentication purpose i.e. valid user name and password
                        client.send("Enter your email address:~")
		        usr_mail=recv_fun(client)
                        usr_mail=usr_mail.rstrip()
			client.send("Enter your password:~")
			u_pass=recv_fun(client)
                        u_pass=u_pass.rstrip()
                        fh=open('user_email.txt','r')
                        x=fh.readlines()
                        fh.close()
                        temp=usr_mail+"\n"
                        if temp in x:                             #if user name is valid
                                client.send("1~")
				a=x.index(temp)
				fh=open('user_pass.txt','r')
                                y=fh.readlines()
                                fh.close()
				fh=open('user_name.txt','r')
                                p=fh.readlines()
                                fh.close()
				u_name=p[a].rstrip()
				
                                temp=u_pass+"\n"
                                if y[a]==temp:                   #if password is matched
                                        client.send("1~")
					client.send("Login Successful..~")
				        main_menu(client,u_name,u_pass)    #authentication done. calling to main_menu() which is in main_menu.py file
                                else:
                                        client.send("0~")        #password doesn't match
					client.send("Sorry wrong Password...Please try again..\n~")
				        login_valid(client)      #calling itself

			else:                                    #invalid username
                             client.send("0~")
			     client.send("This email is not registered with us..~")
			     login_valid(client)                 #calling itself
			
                       
			
