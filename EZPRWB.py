from time import sleep
import sys
import os
import time
import os

textchunk = """# the upstream component nginx needs to connect to
upstream django {
    server unix:///home/udoms/microdomains/microdomains.sock;
}
# configuration of the server
server {
    listen      80;
    server_name micro.domains www.micro.domains;
    charset     utf-8;
    # max upload size
    client_max_body_size 75M;
    # Django media and static files
    location /media  {
        alias /home/udoms/microdomains/media;
    }
    location /static {
        alias /home/udoms/microdomains/static;
    }
    # Send all non-media requests to the Django server.
    location / {
        uwsgi_pass  django;
        include     /home/udoms/microdomains/uwsgi_params;
    }
}"""

blocktext = """uwsgi_param  QUERY_STRING       $query_string;
uwsgi_param  REQUEST_METHOD     $request_method;
uwsgi_param  CONTENT_TYPE       $content_type;
uwsgi_param  CONTENT_LENGTH     $content_length;
uwsgi_param  REQUEST_URI        $request_uri;
uwsgi_param  PATH_INFO          $document_uri;
uwsgi_param  DOCUMENT_ROOT      $document_root;
uwsgi_param  SERVER_PROTOCOL    $server_protocol;
uwsgi_param  REQUEST_SCHEME     $scheme;
uwsgi_param  HTTPS              $https if_not_empty;
uwsgi_param  REMOTE_ADDR        $remote_addr;
uwsgi_param  REMOTE_PORT        $remote_port;
uwsgi_param  SERVER_PORT        $server_port;
uwsgi_param  SERVER_NAME        $server_name;"""


def get_folder_path(folder_name):
    current_directory = os.getcwd()
    folder_path = os.path.join(current_directory, folder_name)
    return folder_path


def get_parent_directory(input_dir):
    # Use os.path.dirname to get the parent directory
    parent_dir = os.path.dirname(input_dir)
    return parent_dir

def replace_line(filename, keyword, replacement):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        with open(filename, 'w') as file:
            for line in lines:
                if keyword in line:
                    file.write(replacement + '\n')
                else:
                    file.write(line)

        print(f"Lines containing '{keyword}' replaced in {filename}.")

    except FileNotFoundError:
        print(f"File '{filename}' not found.")


def get_allowed_hosts():
    while True:
        try:
            user_input = input("How many hosts would you like to add to ALLOWED_HOSTS? (Press Enter for default 2) ")
            num_hosts = int(user_input) if user_input else 2
            if num_hosts <= 0:
                print("Please enter a positive number.")
            elif num_hosts > 20:
                print("The maximum allowed hosts is 20. Please enter a number less than or equal to 20.")
            else:
                break
        except ValueError:
            print("Please enter a valid number.")
    if num_hosts == 1:
        host_input = input("Enter the host (e.g., 'example.com'): ")
        allowed_hosts = f"ALLOWED_HOSTS = ['{host_input}']"
    elif num_hosts > 1:
        allowed_hosts = "ALLOWED_HOSTS = ["
        for i in range(num_hosts):
            host_input = input(f"Enter host {i + 1}: ")
            allowed_hosts += f"'{host_input}', "
        allowed_hosts = allowed_hosts[:-2] + "]"  # Remove the trailing comma and space
    else:
        allowed_hosts = "ALLOWED_HOSTS = ['*']"
    return allowed_hosts

print("Have the directory to your VM ready\n")
print("Make sure you are running EZPRWB in the VM")
print("Make sure EZPRWB is located in the same folder as your django project")
input("press enter to continue..")

print("\n[Installing packages]\n")
os.system("sudo apt-get install gcc -y")
os.system("python --version")
print("Provide the version of python you use")
print("Ex (3.8, 3.9, 3.11, 3.12) 1 period max")
v_num = input("Version: ")
object_one = "sudo apt-get install python"+v_num+"-dev"+" -y"
os.system(object_one)
os.system("pip install uwsgi; pip install django")
print("\n\n!!!!! ERRORS ARE OKAY !!!!!\n\n")
sleep(3)
os.system("sudo apt-get install nginx -y")
print("[+] Done")


project_name = input("Project Folder name :")
one_content = project_name + "/" + project_name.lower() + "/" + "settings.py"
two_content = get_allowed_hosts() # returns allowed domains from user input in list displayed as python string
replace_line(one_content, "ALLOWED_HOSTS", two_content)


data_to_workW = get_folder_path(project_name)

while 1:
    print("provide the directory to your Virtual Enviornment ")
    path_to_vm = input("DIR: ")
    print("Do not inlcude www. | https:// | http:// | .com")
    print("Ex http://super.website.com | you would provide (super.website)")
    wb_name = input("name: ")
    print("Now provide your domain registrar Ex (.com, .org, .live)")
    wb_domain = input("domain registrar: ")
    print(f"is this correct ( www.{wb_name}{wb_domain} ) ?")
    domain_name = f"{wb_name}{wb_domain}"
    y_n = input("(Y \ No )")
    if y_n.upper() == "Y": break
    if y_n.upper() == "YES": break


set_folder_privs = f"sudo chmod 777 {project_name}; sudo chmod 777 {project_name}/* -R;"
os.system(set_folder_privs)
content_three = f"/etc/nginx/sites-available/{wb_name}.conf"

datablock_one = f"\tserver unix://{data_to_workW}/{project_name}.sock;"
datablock_two = f"\tserver_name {domain_name} www.{domain_name};"
datablock_three = f"\t\t alias {data_to_workW}/"
datablock_four = datablock_three +"media;" 
datablock_five = datablock_three + "static;"
datablock_six = f"\t\tinclude     {data_to_workW}/uwsgi_params;"




print("[!] Creating Configuration File")
with open('thedoc', 'w+') as fp2:
    fp2.write(textchunk)
replace_line('thedoc', 'microdomains.sock', datablock_one)
replace_line('thedoc', 'server_name', datablock_two)
replace_line('thedoc', '/microdomains/media', datablock_four)
replace_line('thedoc', '/microdomains/static', datablock_five)
replace_line('thedoc', 'uwsgi_params', datablock_six)
time.sleep(1)

print("[!] adding UWSGI PARAMS in your project")
dt_op = data_to_workW+"/uwsgi_params"
with open(dt_op, 'w+') as fp1:
    fp1.write(blocktext)

print("[+] Moving Configuration file to available sites")
cTthree = "sudo mv thedoc "+content_three
os.system(cTthree)

print("[+] Enabling Sites with sim link")
sim_link_cmd = f"sudo ln -s {content_three} /etc/nginx/sites-enabled/"
os.system(sim_link_cmd)
print("[!] Creating Media file")
hamuo = f"{data_to_workW}/media"
try: os.mkdir(hamuo)
except: pass
print("Restarting Nginx webserver")
emperor_log_dir = get_parent_directory(data_to_workW)
emperor_log_dir += "/uwsgi-emperor.log"
os.system('sudo /etc/init.d/nginx restart')
print("creating UWSGI pathway ")
texty_block = f"""[uwsgi]
# full path to Django project's root directory
chdir            = {data_to_workW}/
# Django's wsgi file
module           = {project_name}.wsgi
# full path to python virtual env
home             = {path_to_vm}
# enable uwsgi master process
master          = true
# maximum number of worker processes
processes       = 10
# the socket (use the full path to be safe
socket          = {data_to_workW}/{project_name}.sock
# socket permissions
chmod-socket    = 666
# clear environment on exit
vacuum          = true
# daemonize uwsgi and write messages into given log
daemonize       = {emperor_log_dir}"""
pathway_name =  f"{data_to_workW}/{project_name}_uwsgi.ini"

with open(pathway_name, 'w+') as fp3:
    fp3.write(texty_block)

allowme = f"sudo chmod 777 {pathway_name}"
os.system(allowme)
print("Configuring Emperor with Vassals")
vast_holes = f"{path_to_vm}/vassals"
os.mkdir(vast_holes)
cmd_huhboathat = f"sudo ln -s {data_to_workW}/{project_name}_uwsgi.ini {path_to_vm}/vassals"
os.system(cmd_huhboathat)

print("Creating Startup Service")

print("How would you describe your website")
description = input("Description: ")
print("Type the username that will deploy the webserver?")
user = input("Username: ")
startup_service_configuration = f"""[Unit]
Description={description}
After=network.target
[Service]
User={user}
Restart=always
ExecStart={path_to_vm}/bin/uwsgi --emperor {path_to_vm}/vassals --uid www-data --gid www-data
[Install]
WantedBy=multi-user.target"""
the_beans = "emperor.uwsgi.service"
with open(the_beans, 'w+') as fp4:
    fp4.write(startup_service_configuration)

os.system("sudo mv emperor.uwsgi.service /etc/systemd/system/")

os.system("systemctl enable emperor.uwsgi.service ; systemctl start emperor.uwsgi.service")