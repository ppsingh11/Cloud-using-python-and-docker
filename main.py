#!/usr/bin/python2

import os
import commands
import signal
import socket
import thread,random
from user_reg import newuser
from login_valid import login_valid

s=socket.socket()
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
#ip="192.168.43.178"
port=5555
s.bind( ("",port) )

s.listen(5)

def fun(x,y):
	print "\nBye , See you!!"
        exit()
signal.signal(signal.SIGINT,fun)  #For Handeling Signal ctrl+c

##########################################################    --OTP--  ###########################################################
import smtplib
def send_otp(email,msg):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.login('cloudservices.nitp@gmail.com','omipps@redhat')

	
	server.sendmail('cloudservices.nitp@gmail.com', '{0}'.format(email.rstrip()), msg)
	server.close()





#####################################################---OTP send fun ends---###################################################

#######################################Recv_function#########################################################################
def recv_fun(client):
    data = ""
    while True:
        part = client.recv(1)
	#length=len(part)
        data = data + part
        if part=="~":
	         break
    return data.rstrip("~")
##############################################################################################################################################


####################################### forget password  #####################################################################################
def forgot_password(client):
		client.send("Enter your UserName~")
                usr=recv_fun(client)
                usr=usr.rstrip()
                fh=open('user_name.txt','r')
                y=fh.readlines()
                fh.close()
                temp=usr+"\n"
                if temp in y:                                         #if user name is valid
                        client.send("1~")
                        a=y.index(temp)
			fh=open('user_email.txt','r')
               	        z=fh.readlines()
                        fh.close()
			email=z[a]
                        client.send("Please wait......~")   #client
                        otp_num=random.randint(100000,999999)
			message='''
                                   Your OTP to change Password on cloud services is - {0}.
                                   
                                   Team - cloud services.'''.format(otp_num)
                        
                        send_otp(email.rstrip(),message)
                 
			
			client.send("A 6 digit OTP has been sent to your registered email address.\nEnter OTP to change your password~")
			otp=recv_fun(client)
                        
                        if otp=="":                              #if user sends null 
				otp=0
			#we have to handle string input
			otp=int(otp)
			if otp==otp_num:                          #if otp is matched
				client.send("1~")
				client.send("Enter new password~")
				paswd=recv_fun(client)
				paswd=paswd.rstrip()
				c1=os.system("echo {1} | passwd {0} --stdin".format(usr.strip(),paswd.decode('base64','strict'))) #reseting password
				
				if c1==0:                          #if password changed
					client.send("1~")
                                        fh=open('user_pass.txt','r')
               	                        p=fh.readlines()
                                        fh.close()
					p[a]=paswd+"\n"
					fh=open('user_pass.txt','w')
               	                        fh.writelines(p)
                                        fh.close()
                                        
					client.send("Your password has been updated successfully~")
					login_menu(client)   #calling login_menu() of same file
				else:                      #in case of technical error, a email is send to server admin
                                        message='''
                                        Password change request of - {0} failed.'''.format(usr)
                        
                                        send_otp("cloudservices.nitp@gmail.com",message)
                                        client.send("0~")
					client.send("There are some technical issues..\nPlease try after some time..~")
					login_menu(client)            #calling login_menu() of same file

				
			else:                                   #if wrong otp is entered
				client.send("0~")
				client.send("You have entered wrong OTP.Try Again..~")
				login_menu(client)              #calling login_menu() of same file
                else:                                           #wrong user name
                        client.send("0~")
			client.send("user does not exist.Try Again..~")
			login_menu(client)                      #calling login_menu() of same file
                
####################################   forget password ends   ##############################################################################





##################################         login_menu            #############################################################################
def login_menu(client):
		client.send("""
						           WELCOME TO CLOUD SERVICES
					      ========================================================
					       New User?.                    Press 1 to Register
					       Alredy Registered?.           Press 2 to login
                                               Forgot Password ? .           Press 3 to change your password
					       Press 4 to exit the program\nEnter your choice:~""")
			
		ch=recv_fun(client)
		
		if ch=='1':
		    newuser(client)      	 #This function resides in user_reg.py file
		    login_menu(client)   	 #Called itself
		elif ch=='2':
		    login_valid(client) 	 #This function resides in login_valid.py file
                elif ch=='3':
			forgot_password(client)  #This function resides in same(main.py) file
		elif ch=='4':
		      exit()
		else:
		   client.send("Please choose correct option..~")
		   login_menu(client)		 #Called itself
                
##########################################################################################################################

os.system("systemctl stop firewalld")
while True:
	client,add=s.accept()
	thread.start_new_thread(login_menu,(client,))       #for every new connection a cpoy of program is started
