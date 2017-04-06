#!/usr/bin/python2

import os
import commands,thread
ip="192.168.0.103"
#from staas import staas
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
	ch=recv_fun(client)
	
	if ch=='1':
		ch1=open("STAAS_USER.txt","r")
		x=ch1.readlines()
		ch1.close()
		temp=u_name+"\n"
		if temp in x:                                                        #if already regisered
			client.send("1~")
			client.send("You are already registered for free storage~")
			staas(client,u_name,u_pass)
		else:                                         #creating lv , changing ownership and mounting
			client.send("0~")
                        client.send("Please wait.... we are working on it~")
                        #client.send("mkdir /media/{0}~".format(u_name))
			s1=os.system("echo y | lvcreate --size 1G --name {0} pps".format(u_name))
			s2=os.system("mkfs.ext4 /dev/pps/{0}".format(u_name))
			s3=os.system("mkdir /home/STAAS/{0}".format(u_name))
			s4=os.system("mount /dev/pps/{0} /home/STAAS/{0}".format(u_name))
			s5=os.system("chown {0} /home/STAAS/{0}".format(u_name))
			s6=os.system("setfacl -m o::--- /home/STAAS/{0}".format(u_name))
			print s1,s2,s3,s4,s5,s6	


			if s1==0 and s2==0 and s3==0 and s4==0 :   #if all the things are successfully done
				ch1=open("STAAS_USER.txt","a")
				ch1.write(u_name+"\n")
				ch1.close()
				ch2=open("STAAS_SIZE.txt","a")
				ch2.write("1.0\n")
				
				ch2.close()
				client.send("Registration done.....Now you can use your drive.....~")
				staas(client,u_name,u_pass)
			else:                                                    #in case of any error
				#we have to send error email to server
				client.send("Some error occured!! please try again....~")
				staas(client,u_name,u_pass)
			
	elif ch=='2':              
                        ch1=open("STAAS_USER.txt","r")
		        x=ch1.readlines()
		        ch1.close()
		        temp=u_name+"\n"
		        if temp in x:                    #if it is registered user

                                client.send("1~")
                                
                                def check_drive():              #for checking a valid drive name for mounting to user desktop
		                        client.send("Enter text which you want to use as a drive name.~")
		                        drive=recv_fun(client)
                                        client.send("mkdir /media/{0}~".format(drive.rstrip()))
                                        sig=recv_fun(client)
                                       
                                        if sig=='1':               #if already a drive exists of same name
                                             
					     client.send("rmdir /media/{0}~".format(drive.rstrip()))   #try to remove that folder
                                             sign=recv_fun(client)
                                             #sign=int(sign)
                                             
                                             if sign=='1':                 #if folder is not empty
		                                     client.send("This drive is already in use in your system..Please try another name.~")
		                                     check_drive()      #calling itself
                                             else:                      #if folder is removed
                                                client.send("We are working on it.Please wait....~")
				                client.send("mkdir /media/{0}~".format(drive.rstrip()))
						os.system("systemctl restart sshd")
				                s4=os.system("mount /dev/pps/{0} /home/STAAS/{0}".format(u_name))
						client.send("echo {0} | sshfs {1}@{2}:/home/STAAS/{1} /media/{3}  -o workaround=rename -o password_stdin~".format(u_pass.rstrip().decode('base64','strict'),u_name.rstrip(),ip,drive.rstrip()))
						client.send("The drive is available on your Desktop.......~")
						main_menu(client,u_name,u_pass)   #calling main_menu() in same file when drive is mounted to client
                                                     
                                        else:                          #if folder is created 
                                                
				                client.send("We are working on it.Please wait....~")
						os.system("systemctl restart sshd")
				                s4=os.system("mount /dev/pps/{0} /home/STAAS/{0}".format(u_name))
						client.send("echo {0} | sshfs {1}@{2}:/home/STAAS/{1} /media/{3}  -o workaround=rename -o password_stdin~".format(u_pass.rstrip().decode('base64','strict'),u_name.rstrip(),ip,drive.rstrip()))
						client.send("The drive is available on your Desktop.......~")
						main_menu(client,u_name,u_pass)   #calling main_menu() in same file when drive is mounted to client
				check_drive()            #for checking a valid drive name for mounting to user desktop
		        else:                            #not a registered user
                                client.send("0~")
				client.send("You have not registered yet...Please register first..~")
			        staas(client,u_name,u_pass)  #calling itself
			
	elif ch=='3':
############################################----StAAS extend-----#################################################################
		fh=open('STAAS_USER.txt','r')
		x=fh.readlines()
		fh.close()
		u_name=u_name.rstrip()
		temp=u_name+"\n"
		if temp in x:                                 #if it is a registered user
			client.send("1~")
			usr_ind=x.index(temp)
			fh=open('STAAS_SIZE.txt','r')
			y=fh.readlines()
			fh.close()
			size=y[usr_ind].rstrip("\n")
			if size <= '3.0':                     #if occupied size is within limit
				client.send("1~")             #a condition can be minimised #we will do later
				size=float(size)
				if 3.0-size==0:              #if  using upto maximum limit
					client.send("1~")
					client.send("You are already using upto maximum size limit.You can't extend more.~")
					staas(client,u_name,u_pass)
				else:                       #if it can extend
					client.send("0~")
					
		                        client.send("Enter the size in GB by which you want to extend your drive.Currently you can extend uptp {0} GB only.~".format(3.0-size))
					
					s=recv_fun(client)
					s=s.rstrip()
				        tmp=str(3.0-size)
						
					
					if '0.0' < s <= tmp:    #if endered data is whithin extension limit
						client.send("1~")
						s=float(s)
				
					        size=size+s
						c1=os.system("lvextend --size +{0}G /dev/pps/{1}".format(s,u_name))
						c2=os.system("resize2fs /dev/pps/{0}".format(u_name))
						if c1==0 and c2==0:   #if successfully extended
							client.send("1~")
							fh=open('STAAS_SIZE.txt','r')
							y=fh.readlines()
							fh.close()
							y[usr_ind]="{0}\n".format(size)
							fh=open('STAAS_SIZE.txt','w')
							fh.writelines(y)
							fh.close()
							client.send("Your drive is extended by {0} GB~".format(s))
							main_menu(client,u_name,u_pass)
						else:                             #if any error
							#we have to send a mail to server
							client.send("0~")
							client.send("There are some technical issues.Please try after some time~")
							staas(client,u_name,u_pass)
					else:                         #if requested size is 0 or greater than max limit or any random string
						client.send("0~")
						client.send("Invalid request...~")
						staas(client,u_name,u_pass)
			else:
				client.send("0~")      #we can remove it#we will remove later
				client.send("You are already using upto maximum limit.You can't extend more size.~")	
				staas(client,u_name,u_pass)	
		else:                                     #not a registered user
			client.send("0~")
			cliend.send("You are not registered for storage service.Please Register first.~")
			staas(client,u_name,u_pass)



############################################----StAAS extend ends-----#################################################################
	elif ch=='4':
		exit()
	else:
		client.send("Sorry choose right option~")
		staas(client,u_name,u_pass)
###########################################################---STAAS Function ends----###############################################################







####################################################-----SAAS-------#########################################################################
def saas(client,u_name,u_pass):
		        client.send("""
				======================================
				Press 1 to Register for a software
				Press 2 to use a software
				Press 3 to exit the program\nEnter your choice:~""")
			che=recv_fun(client)
			
			if che=='1':
				 client.send('''Currently we have these many of softwares..
                                        =====================================================
				          Press 1 for Firefox Browser
				          Press 2 for Google Chrome Browser
                                          Press 3 for VLC media player
                                          Press 4 for Gedit text editor
                                          Press 5 to exit the program\nEnter your choice:~''')
				 chc=recv_fun(client)
			         
                                 if chc=='1':
					fh=open("/home/{0}/user_soft.txt".format(u_name),"r")
					x=fh.readlines()
                                        fh.close()
                                        y="firefox\n"
                                        if y in x:                  # if user is already registered
                                             client.send("You are already registered for Firefox Browser~")
					     saas(client,u_name,u_pass)
                                        else:             #for changing permission and creating entery in file
                                                
						fh=open("/home/{0}/user_soft.txt".format(u_name),"a")
						fh.write("firefox\n")
						fh.close()
                                                os.system("setfacl -m u:{0}:rwx /usr/bin/firefox".format(u_name))
						client.send("Successfully registered for '{0}'~".format("Firefox Browser"))
                                                
						saas(client,u_name,u_pass)
				 elif chc=='2':
					fh=open("/home/{0}/user_soft.txt".format(u_name),"r")
					x=fh.readlines()
                                        fh.close()
                                        y="google-chrome\n"
                                        if y in x:
                                             
                                             client.send("You are already registered for Google Chrome Browser~")
					     saas(client,u_name,u_pass)
                                        else:
		                                fh=open("/home/{0}/user_soft.txt".format(u_name),"a")
						fh.write("google-chrome\n")
						fh.close()
                                                os.system("setfacl -m u:{0}:rwx /usr/bin/google-chrome".format(u_name))
						client.send("Successfully registered for '{0}'~".format("Google Chrome Browser"))
                                                
						saas(client,u_name,u_pass)
				 elif chc=='3':
                                        fh=open("/home/{0}/user_soft.txt".format(u_name),"r")
					x=fh.readlines()
                                        fh.close()
                                        y="vlc\n"
                                        if y in x:
                                             
                                             client.send("You are already registered for VLC media player~")
					     saas(client,u_name,u_pass)
                                        else:
						fh=open("/home/{0}/user_soft.txt".format(u_name),"a")
						fh.write("vlc\n")
						fh.close()
                                                os.system("setfacl -m u:{0}:rwx /usr/bin/vlc".format(u_name))
						client.send("Successfully registered for '{0}'~".format("VLC media player"))
                                               
						saas(client,u_name,u_pass)
				 elif chc=='4':
                                        fh=open("/home/{0}/user_soft.txt".format(u_name),"r")
					x=fh.readlines()
                                        fh.close()
                                        y="gedit\n"
                                        if y in x:
                                             
                                             client.send("You are already registered for Gedit text editor~")
					     saas(client,u_name,u_pass)
                                        else:
						fh=open("/home/{0}/user_soft.txt".format(u_name),"a")
						fh.write("gedit\n")
						fh.close()
                                                os.system("setfacl -m u:{0}:rwx /usr/bin/gedit".format(u_name))
						client.send("Successfully registered for {0}~".format("Gedit text editor"))
                                                
						saas(client,u_name,u_pass)
				 elif chc=='5':
					exit()
				 else:
				   client.send("Please choose correct option..~")
				   saas(client,u_name,u_pass)
                                        
			elif che=='2':
                                 
                                 fh=open("/home/{0}/user_soft.txt".format(u_name),"r")
			         x=fh.readlines()
                                 fh.close()
				 length=len(x)
                                 client.send("{0}~".format(length))
				 
                                 if length==0:                   #if user is not registered
					client.send("You are not registered for any software.Please register first..~")
                                        saas(client,u_name,u_pass)  #calling itself
                                 else :                           #if user is registered
		                         client.send("You have registered for these {0} softwares...~".format(length))
		                         
		                         for y in x:
		                             y=y.rstrip()
		                             if y=="firefox":
		                                  client.send("Write   'firefox'   to use Firefox Browser~")
		                             elif y=="google-chrome":
		                                  client.send("Write   'google-chrome'   to use Google Chrome Browser~")
		                             elif y=="vlc":
		                                  client.send("Write   'vlc'   to use VLC media player~")
		                             elif y=="gedit":
		                                  client.send("Write   'gedit'   to use Gedit text editor~")
		                           
					 client.send("Write software name which you want to use?~")
					 soft=recv_fun(client)
		                         soft=soft+"\n"
                                         if soft in x:   #if requested software is reqistered by user
                                               client.send("1~")
					       
					       client.send("sshpass -p {1} ssh {0}@{3} -X {2}~".format(u_name.rstrip(),u_pass.rstrip().decode('base64','strict'),soft.strip(),ip))
                                               saas(client,u_name,u_pass)  #calling itself
                                         else:
                                             client.send("0~")   
                                             client.send("Error!! Either you Are not registered for this software or it is not a valid software name~")
                                             saas(client,u_name,u_pass)   #calling itself
                                             
					 
			elif che=='3':
				 exit()
			else:
				client.send("Please choose correct option..~")
				saas(client,u_name,u_pass)   #calling itself

#####################################################---SAAS ENDS-----#######################################################################

#####################################################--IAAS--###############################################################################

def iaas(client,u_name,u_pass):
		client.send("""
		                   
		              ===========================================================
		                    Press 1 For RedHat 7.2
				    Press 2 For Windows 8.1
				    Press 3 Centos
				    Press 4 to Go Back
				    Press 5 to exit the program\nEnter your choice:~""")
		choice=recv_fun(client)
		if choice=='1':
			PORT=5911
			client.send("Enter the size of RAM in MB~")
			ram=recv_fun(client)
			ram=int(ram)
			client.send("How many CPUs you want?~")
			cpu=recv_fun(client)
			cpu=int(cpu)
			client.send("Enter the size of Hard Disk in GB~")
			hdd=recv_fun(client)
			hdd=int(hdd)
			commands.getstatusoutput("systemctl restart vsftpd")

			cmd="virt-install --vnc --vncport={4} --vnclisten=0.0.0.0 --name {5} --memory {0} --vcpus {1} --location /var/ftp/pub/rhel72.iso --os-type linux --os-variant rhel7 --disk path=/var/lib/libvirt/images/{5}.img,size={2} --hvm --extra-args='ks=ftp://{3}/pub/anac.cfg'".format(ram,cpu,hdd,ip,PORT,u_name)
			
			thread.start_new_thread(commands.getstatusoutput,(cmd,))


			


			client.send("vncviewer {0}:{1}~".format(ip,PORT))
			iaas(client,u_name,u_pass)
		elif choice=='2':
			PORT=5911
			client.send("Enter the size of RAM in MB~")
			ram=recv_fun(client)
			ram=int(ram)
			client.send("How many CPUs you want?~")
			cpu=recv_fun(client)
			cpu=int(cpu)
			client.send("Enter the size of Hard Disk in GB~")
			hdd=recv_fun(client)
			hdd=int(hdd)
			commands.getstatusoutput("systemctl restart vsftpd")

			cmd="virt-install --vnc --vncport={4} --vnclisten=0.0.0.0 --name {5} --memory {0} --vcpus {1} --cdrom /var/ftp/pub/win81.iso --os-type windows --os-variant win8.1 --disk path=/var/lib/libvirt/images/{5}.img,size={2} --hvm".format(ram,cpu,hdd,ip,PORT,u_name)
			
			thread.start_new_thread(commands.getstatusoutput,(cmd,))


			


			client.send("vncviewer {0}:{1}~".format(ip,PORT))
			iaas(client,u_name,u_pass)
		elif choice=='3':
			pass
		elif choice=='4':
			main_menu(client,u_name,u_pass)
		elif choice=='5':
			exit()
		else:
			iaas(client,u_name,u_pass)
			

		


#######################################################--IAAS ENDS--########################################################################

#########################################################--PAAS --###########################################################################
def paas(client,u_name,u_pass):
		client.send("""
		                   
		              ===========================================================
		                    Press 1 to Run Python Program
				    Press 2 to Run C Program
				    Press 3 to Run CPP Program
				    Press 4 to Run JAVA Program
				    Press 5 to Go Back
				    Press 6 to exit the program\nEnter your choice:~""")
		choice=recv_fun(client)
		if choice=='1':
			client.send("Enter File Path~")
			path=recv_fun(client)
			client.send("Enter the file Name with extension~")
			name=recv_fun(client)
			client.send("scp {0} {2}@{1}:/home/{2}~".format(path+"/"+name,ip,u_name))
			
			status=recv_fun(client)
			
			if status=='0':
				client.send("Error Occured while uploading the file~")
				paas(client,u_name,u_pass)
			else:
				p=commands.getstatusoutput("docker run --volume /home/{1}/{0}:/copy.py centos python copy.py &> /home/{1}/pps.txt".format(name,u_name))
				fh=open("/home/{0}/pps.txt".format(u_name),"r")
				x=fh.readlines()
                                fh.close()
				x="".join(x)
				x=x+"~"
				client.send(x)
				paas(client,u_name,u_pass)
		elif choice=='2':
			client.send("Enter File Path~")
			path=recv_fun(client)
			client.send("Enter the file Name with extension~")
			name=recv_fun(client)
			client.send("scp {0} {2}@{1}:/home/{2}~".format(path+"/"+name,ip,u_name))
			
			status=recv_fun(client)
			
			if status=='0':
				client.send("Error Occured while uploading the file~")
				paas(client,u_name,u_pass)
			else:
				p=commands.getstatusoutput('cd /home/{1} && docker run --rm -v "$PWD":/home/{1} -w /home/{1} gcc:6.3.0 gcc -o myapp {0} &> compile.txt'.format(name,u_name))
				kk=commands.getstatusoutput("rm -f /home/{1}/{0}".format(name,u_name))
				fh=open("/home/{0}/compile.txt".format(u_name),"r")
				x=fh.readlines()
                                fh.close()
				if len(x)!=0:
					
					
					x="".join(x)
					x=x.replace("~","")
					x=x+"~"
					
					client.send(x)
					
					

				else:	
					p=commands.getstatusoutput("/home/{0}/myapp &> /home/{0}/pps.txt".format(u_name))
					fh=open("/home/{0}/pps.txt".format(u_name),"r")
					x=fh.readlines()
		                        fh.close()
					x="".join(x)
					x=x+"~"
					client.send(x)
					
				paas(client,u_name,u_pass) 
	
		elif choice=='3':
			client.send("Enter File Path~")
			path=recv_fun(client)
			client.send("Enter the file Name with extension~")
			name=recv_fun(client)
			client.send("scp {0} {2}@{1}:/home/{2}~".format(path+"/"+name,ip,u_name))
			
			status=recv_fun(client)
			
			if status=='0':
				client.send("Error Occured while uploading the file~")
				paas(client,u_name,u_pass)
			else:
				p=commands.getstatusoutput('cd /home/{1} && docker run --rm -v "$PWD":/home/{1} -w /home/{1} gcc:6.3.0 g++ -o myapp {0} &> compile.txt'.format(name,u_name))
				kk=commands.getstatusoutput("rm -f /home/{1}/{0}".format(name,u_name))
				fh=open("/home/{0}/compile.txt".format(u_name),"r")
				x=fh.readlines()
                                fh.close()
				if len(x)!=0:
					
					
					x="".join(x)
					x=x.replace("~","")
					x=x+"~"
					
					client.send(x)
					
					

				else:	
					p=commands.getstatusoutput("/home/{0}/myapp &> /home/{0}/pps.txt".format(u_name))
					fh=open("/home/{0}/pps.txt".format(u_name),"r")
					x=fh.readlines()
		                        fh.close()
					x="".join(x)
					x=x+"~"
					client.send(x)
					
				paas(client,u_name,u_pass) 

		elif choice=='4':
			client.send("Enter File Path~")
			path=recv_fun(client)
			client.send("Enter the file Name without extension~")
			name=recv_fun(client)
			client.send("scp {0} {2}@{1}:/home/{2}~".format(path+"/"+name+".java",ip,u_name))
			
			status=recv_fun(client)
			
			if status=='0':
				client.send("Error Occured while uploading the file~")
				paas(client,u_name,u_pass)
			else:
				p=commands.getstatusoutput('cd /home/{1} && docker run --rm -v "$PWD":/home/{1} -w /home/{1} java:7 javac {0} &> compile.txt'.format(name+".java",u_name))
				kk=commands.getstatusoutput("rm -f /home/{1}/{0}".format(name+".java",u_name))
				fh=open("/home/{0}/compile.txt".format(u_name),"r")
				x=fh.readlines()
                                fh.close()
				if len(x)!=0:
					
					
					x="".join(x)
					x=x.replace("~","")
					x=x+"~"
					
					client.send(x)
					
					

				else:	
					p=commands.getstatusoutput("cd /home/{1} && java {0} &> /home/{1}/pps.txt".format(name,u_name))
					fh=open("/home/{0}/pps.txt".format(u_name),"r")
					x=fh.readlines()
		                        fh.close()
					x="".join(x)
					x=x+"~"
					client.send(x)
					
				paas(client,u_name,u_pass) 
   
		elif choice=='5':
			main_menu(client,u_name,u_pass)
		elif choice=='6':
			exit()
		else:
			paas(client,u_name,u_pass)


##########################################################--PAAS ENDS--######################################################################

def main_menu(client,u_name,u_pass):
			client.send("""
		                   
		              ===========================================================
		                    Press 1 to SAAS(Software as a service)
				    Press 2 to StAAS(Storage as a service)
				    Press 3 to IAAS(Infrastructure as a service)
				    Press 4 to PAAS(Plateform as a service)
				    Press 5 to exit the program\nEnter your choice:~""")
			choice=recv_fun(client)
			#choice=int(choice)
			if choice=='1':
				 
				 saas(client,u_name,u_pass)    #calling saas() in same file
			elif choice=='2':
				 staas(client,u_name,u_pass)   #calling staas() in same file
			
			elif choice=='3':
				 iaas(client,u_name,u_pass)
			elif choice=='4':
				 paas(client,u_name,u_pass)
			elif choice=='5':
				 exit()
			else :
			    client.send("Please choose correct option..~")
                            main_menu(client,u_name,u_pass)
				
				
		
		
