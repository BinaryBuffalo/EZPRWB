from os import system
from time import sleep


print("\n[Installing packages]\n")
system("sudo apt-get install gcc -y")
system("python --version")
print("Provide the version of python you use")
print("Ex (3.8, 3.9, 3.11, 3.12) 1 period max")
v_num = input("Version: ")
object_one = "sudo apt-get install python"+v_num+"-dev"+" -y"
system(object_one)
system("pip install uwsgi; pip install django")
print("\n\n!!!!! ERRORS ARE OKAY !!!!!\n\n")
sleep(3)
system("sudo apt-get install nginx -y")
print("[+] Done")
