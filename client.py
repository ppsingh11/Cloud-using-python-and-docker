#!/usr/bin/python

#-----------------------------------------------------*	 Maa _/\_ Papa	*--------------------------------------------------------#

import os,commands,getpass,socket,signal,time,thread
from validate_email import validate_email

ip="192.168.0.103"
port=5555

def control(a,b):
	print "\n\nThanks for using my services....\nBye.....See you soon........"
	exit()

signal.signal(signal.SIGINT,control)
s=socket.socket()
s.connect((ip,port))

#############################################	   Receiving data from server	   ##################################################

def recvall():
    data = ""
    while True:
        part = s.recv(1)
        data = data + part

	if part=="~":
		break

    return data.rstrip("~")

################################################	      STAAS       	#####################################################

def STAAS():
	os.system("tput setaf 3")
	print recvall()
	os.system("tput setaf 0")
	ch=raw_input()
	s.send("{0}~".format(ch))
        if ch=='1':
                sig=recvall()
		if sig=='1':
			print recvall()	
			STAAS()
		else:
			print recvall()
			print recvall()
			STAAS()	
        elif ch=='2':
			sig=recvall()
			if sig=='1':
				def create_drive():
					print recvall()
					drive=raw_input()
					s.send(drive+"~")
					cmd=recvall()
					flag=commands.getstatusoutput(cmd)
					if flag[0]==0:
						s.send("0~")
						print recvall()
						tempcommand=recvall()
						os.system(tempcommand)
						print recvall()
						Service_Menu()
					else:
						s.send("1~")
						command=recvall()
						status=commands.getstatusoutput(command)
						sai=status[0]
						if sai==0:
							s.send("0~")
							print recvall()
							tempcommand=recvall()
							os.system(tempcommand)
							tmpcommand=recvall()
							os.system(tmpcommand)
							print recvall()
							Service_Menu()
						else:
							s.send("1~")
							print recvall()
							create_drive()
				create_drive()	
			else:
				print recvall()
				STAAS()
        elif ch=='3':
			sig=recvall()
			if sig=='1':
				s2=recvall()
				if s2=='1':
					s3=recvall()
					if s3=='1':
						print recvall()
						STAAS()
					else:
						print recvall()
						volume=raw_input()
						s.send(volume+"~")
						new_sig=recvall()
						if new_sig=='1':
							final_sig=recvall()
							if final_sig=='1':
								print recvall()
								Service_Menu()
							else:
								print recvall()
								STAAS()
						else:
							print recvall()
							STAAS()	
				else:
					print recvall()
					STAAS()
			else:
				print recvall()
				STAAS()
        elif ch=='4':
                Service_Menu()
	elif ch=='5':
                exit()
	else:
		print recvall()
		STAAS()

################################################	      SAAS       	#####################################################

def SAAS():
	os.system("tput setaf 3")
	print recvall()
	os.system("tput setaf 0")
	ch=raw_input()
	s.send("{0}~".format(ch))
	if ch=='1':
		os.system("tput setaf 3")
		print recvall()
		os.system("tput setaf 0")
		nch=raw_input()
		s.send("{0}~".format(nch))
		if nch=='1':
			print recvall()
			SAAS()
		elif nch=='2':
			print recvall()
			SAAS()
		elif nch=='3':
			print recvall()
			SAAS()
		elif nch=='4':
			print recvall()
			SAAS()
		elif nch=='5':
			SAAS()
		elif nch=='6':
			exit()
		else:
			print recvall()
			SAAS()
	elif ch=='2':
		length=recvall()
		leng=int(length)
		if length=='0':
			print recvall()
			SAAS()
		else:
			print recvall()
			a=0
			while a<leng:
				print recvall()
				a+=1
			print recvall()
			soft=raw_input()
			s.send(soft+"~")
			nch=recvall()
			if nch=='1':
				data=recvall()

				thread.start_new_thread(commands.getstatusoutput,(data,))
				SAAS()
			else:
				print recvall()
				SAAS()
				
	elif ch=='3':
		Service_Menu()
	elif ch=='4':
		exit()
	else:
		os.system("clear")
		print recvall()
		SAAS()

######################################################     IAAS	   ###########################################################

def hw_requirement():
	print recvall()
	ram=raw_input()
	s.send(ram+"~")
	print recvall()
	cpu=raw_input()
	s.send(cpu+"~")
	print recvall()
	hdd=raw_input()
	s.send(hdd+"~")


def IAAS():
	os.system("tput setaf 3")
	print recvall()
	os.system("tput setaf 0")
	ch=raw_input()
	s.send(ch+"~")
	if ch=='1' or ch=='2':
		hw_requirement()
		cmd=recvall()
		os.system("tput setaf 5")
		print("Default password for root user is deathstorm\n")
		print("Please wait a moment.....\n")
		os.system("tput setaf 0")
		time.sleep(10)

		thread.start_new_thread(commands.getstatusoutput,(cmd,))		

		c=os.system('gnome-terminal -e "{0}"'.format(cmd))
		IAAS()

	elif ch=='3':	
		pass
	elif ch=='4':
		Service_Menu()
	elif ch=='5':
		exit()
	else:
		os.system("clear")
		print "Choose correct option.........."
		IAAS()

################################################	    PAAS       ##############################################################

def FILE():
	print recvall()
	loc=raw_input()
	s.send(loc+"~")
	print recvall()
	name=raw_input()
	s.send(name+"~")
	cmd=recvall()

	p=commands.getstatusoutput(cmd)
	p=str(p)
	s.send(p+"~")
	print recvall()
	PAAS()

def PAAS():
	os.system("tput setaf 3")
	print recvall()
	os.system("tput setaf 0")
	ch=raw_input()
	s.send(ch+"~")
	if ch=='1' or ch=='2' or ch=='3' or ch=='4':
		FILE()
	elif ch=='5':
		os.system("clear")
		Service_Menu()
	elif ch=='6':
		exit()
	else:
		os.system("clear")
		os.system("tput setaf 5")
		print  "Please choose right option............."
		os.system("tput setaf 0")
		PAAS()

################################################	Menu of services	#####################################################

def Service_Menu():
	os.system("clear")
	os.system("tput setaf 3")
	print recvall()
	os.system("tput setaf 0")
	ch=raw_input()
	s.send("{0}~".format(ch))
	if ch=='1':
		SAAS()
	elif ch=='2':
		os.system("clear")
		STAAS()
	elif ch=='3':
		os.system("clear")
		IAAS()
	elif ch=='4':
		os.system("clear")
		PAAS()
	elif ch=='5':
		exit()	
	else:
		print recvall()
		Service_Menu()	

################################################	User Registretion 	#####################################################

def User_Reg():
	c1='1'
	


	while c1=='1':
		print recvall()
		c2='1'
		while c2=='1':
			usr_mail=raw_input()
			if validate_email(usr_mail.rstrip()):
				c2='0'
			else:
				print "Please enter valid email address..."
		

		s.send(usr_mail+"~")
		c1=recvall()
		if c1=='1':
			print recvall()
	
	
	print recvall()
	Pass=getpass.getpass()
	Pass=Pass.encode('base64','strict')
	s.send(Pass+"~")
	print recvall()
	print recvall()
	
	code=raw_input()
	s.send(code+"~")
	
	tmpsig=recvall()
	if tmpsig=='1':
		sig=recvall()
		if sig=='0':
			print recvall()
			Main_Menu()
		else:
			print recvall()
			User_Reg()
	else:
		print recvall()
		User_Reg()

################################################	User login validation	###################################################

def Login():
	print recvall()
	Uname=raw_input()
	s.send(Uname+"~")
	print recvall()
	Pass=getpass.getpass()
	Pass=Pass.encode('base64','strict')
	s.send(Pass+"~")
	flag=recvall()
	#flag=int(flag)
	if flag=='1':
		tempflag=recvall()
		#tempflag=int(tempflag)
		if tempflag=='1':
			print recvall()
			Service_Menu()
		else:
			print recvall()
			Login()
	else:
		print recvall()
		Login()

################################################	   Forgot Password	 ####################################################

def ForgotPassword():
	print recvall()
	uname=raw_input()
	s.send(uname+"~")
	sig=recvall()
	if sig=='1':
		print recvall()
		print recvall()
		otp=raw_input()
		s.send(otp+"~")
		tempsig=recvall()
		if tempsig=='1':
			print recvall()
			new_pass=getpass.getpass()
			new_pass=new_pass.encode('base64','strict')
			s.send(new_pass+"~")
			flag=recvall()
			#flag=int(flag)
			if flag=='1':
				print recvall()
				Main_Menu()
			else:
				print recvall()
				Main_Menu()
		else:
			print recvall()
			Main_Menu()
	else:
		print recvall()
		Main_Menu()
	
################################################	Entering in main menu	 ####################################################

def Main_Menu():
	os.system("tput setaf 3")
	print recvall()
	os.system("tput setaf 0")
	ch=raw_input()
	s.send("{0}~".format(ch))
	if ch=='1':
		User_Reg()
	elif ch=='2':
		Login()
	elif ch=='3':
		ForgotPassword()
	elif ch=='4':
		exit()
	else:
		os.system("clear")
		print recvall()
		Main_Menu()
		
################################################	Entering in program	 ####################################################

Main_Menu()

################################################	  End of program	#####################################################


