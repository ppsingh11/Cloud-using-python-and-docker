#!/usr/bin/python2

import os
import random,commands
from validate_email import validate_email                 #importing validate_email function from validate_email module 

#######################################Recv_function#########################################################################
def recv_fun(client):                        #This function recieve data from client
    data = ""
    while True:
        part = client.recv(1)
	
        data = data + part
        if part=="~":
	         break
    return data.rstrip("~")
##############################################################################################################################################

##########################################################    --OTP--  ###########################################################
import smtplib
def otp(email,msg):                                                  #This function is used to send OTP to client by email
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.login('cloudservices.nitp@gmail.com','omipps@redhat')

	
	v=server.sendmail('cloudservices.nitp@gmail.com', '{0}'.format(email.rstrip()), msg)
	server.close()





#####################################################---OTP send fun ends---###################################################


def newuser(client):                                          #Registration for new user
        c1=1
	
	while c1==1:                                          #finds unique user name
		client.send("Enter your email address:~")
                usr_mail=recv_fun(client)
		usr_mail=usr_mail.rstrip()
		fh=open('user_email.txt','r')
                x=fh.readlines()
                fh.close()
                temp3=usr_mail+"\n"
                c1=0
		if temp3 in x:                                #if unique user name is found , loop is breaked
                           c1=1
                client.send("{0}~".format(c1))
		if c1==1:
		     client.send("This email address is already registered with us...\n~")
 		     
        
        client.send("Enter Password:~")
        pas=recv_fun(client)
        pas=pas.rstrip()
        client.send("For email verification one time password has been sent to your email.~")
	client.send("Enter 6 digit OTP that you have recieved in your mailbox~") 
        
        otp_num=random.randint(100000,999999)                              #generating 6 digit random number for otp
        msg = '''
                  Hi {0}.
                    Your OTP for registration on cloud services is - {1}.
                    Enter this OTP and complete your registration process.
                    OTP is confidential.Do not share it with any one.
                    In the case you have not requested for registration,ignore this message.

                    Team - cloud services'''.format(usr_mail,otp_num)
        
        otp(usr_mail,msg)                                        #for sending otp.This function is in same file
            
        otpnum=recv_fun(client)
	if otpnum=="":                                                 #if cliends sends NULL OTP
		otpnum=0
	#we have to handle for string input
        otpnum=int(otpnum)
        if otpnum==otp_num:                                            #if otp is matched                                          
		client.send("1~")
		temp_usr=commands.getstatusoutput('(date +%s%N)')
		usr=temp_usr[1]
		usr=int(usr)
		usr=usr%1000000
		print usr
		usr=str(usr)
                os.system("useradd {0}".format(usr.rstrip()))          #create user
	        c2=os.system("echo {1} | passwd {0} --stdin".format(usr.strip(),pas.decode('base64','strict')))   #set password
	
		if c2!=0:                                             #if password is not set successfully
			c2=1
		client.send("{0}~".format(c2))
		if c2==0: 
			temp2=usr+"\n"                                  #if user created successfully
			fh=open("/home/{0}/user_soft.txt".format(usr),"w")
			fh.close()
			fh=open("user_name.txt","a")
			fh.write(temp2)
			fh.close()
                        fh=open("user_pass.txt","a")
			fh.write(pas+"\n")
			fh.close()
                        fh=open("user_email.txt","a")
			fh.write(usr_mail+"\n")
			fh.close()
                        client.send("Registration Done.Please login to use services...~")
		                             
			#now the program will go to main.py file and calls login_menu(client) function
		else:
			client.send("There are some technical issues.Please try after some time~")
			newuser(client)		
	else:
		client.send("0~")
		client.send('Wrong OTP entered...~')        #wrong otp entered by client
                newuser(client)                             #calls itself
