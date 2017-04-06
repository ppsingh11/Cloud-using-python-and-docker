#!/usr/bin/python2

import os
ip="192.168.43.178"
#from main_menu import main_menu
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
############################################################-------STAAS Function------######################################################
def staas(client,u_name,u_pass): 
	client.send("""
                       Press 1:To register for 1GB free volume
		       Press 2:To use your volumes
		       Press 3:To extend your volume
		       Press 4:To exit from program\nEnter your choice : ~""")
	ch=client.recv(1)
	ch=int(ch)
	if ch==1:
		ch1=open("STAAS_USER.txt","r")
		x=ch1.readlines()
		ch1.close()
		temp=u_name+"\n"
		if temp in x:
			client.send("1")
			client.send("You are already registered for free storage~")
			staas(client,u_name,u_pass)
		else:
			client.send("0")
                        client.send("Please wait.... we are working on it~")
                        client.send("mkdir /media/{0}~".format(u_name))
			s1=os.system("lvcreate --size 1G --name {0} pps".format(u_name))
			s2=os.system("mkfs.ext4 /dev/pps/{0}".format(u_name))
			s3=os.system("mkdir /home/STAAS/{0}".format(u_name))
			s4=os.system("mount /dev/pps/{0} /home/STAAS/{0}".format(u_name))
			s5=os.system("chown {0} /home/STAAS/{0}".format(u_name))
			s6=os.system("setfacl -m o::--- /home/STAAS/{0}".format(u_name))	


			if s1==0 and s2==0 and s3==0 and s4==0 and s5==0 and s6==0:
				ch1=open("STAAS_USER.txt","a")
				ch1.write(u_name+"\n")
				ch1.close()
				ch2=open("STAAS_SIZE.txt","a")
				ch2.write("1")
				ch2.write("\n")
				ch2.close()
				client.send("Registration done.....now you can use your drive and enjoy.....~")
				staas(client,u_name,u_pass)
			else:
				client.send("Some error occured!! please try again....~")
				staas(client,u_name,u_pass)
			
	elif ch==2:              
                        ch1=open("STAAS_USER.txt","r")
		        x=ch1.readlines()
		        ch1.close()
		        temp=u_name+"\n"
		        if temp in x:
                                client.send("1")
				os.system("systemctl restart sshd")
				client.send("echo {0} | sshfs {1}@{2}:/home/STAAS/{1} /media/{1}  -o workaround=rename -o password_stdin~".format(u_pass.rstrip().decode('base64','strict'),u_name.rstrip(),ip))
				client.send("The drive is available on your Desktop with your username.......~")
                                main_menu(client,u_name,u_pass)
			        
		        else:
                                client.send("0")
				client.send("You have not registered yet...Please register first..~")
			        staas(client,u_name,u_pass) 
			
	elif ch==3:
			pass
	elif ch==4:
		exit()
	else:
		client.send("Sorry choose right option~")
		staas(client,u_name,u_pass)
###########################################################---STAAS Function ends----###############################################################


