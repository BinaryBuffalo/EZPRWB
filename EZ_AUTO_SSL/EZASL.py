from os import system


system("sudo apt-get install snapd -y")
system("sudo snap install --classic certbot")
system("sudo ln -s /snap/bin/certbot /usr/bin/certbot")

system("sudo certbot --nginx")