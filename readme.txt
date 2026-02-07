This is an auto setup from Tony Teaches Tech's video on 
"How to Deploy Django on Nginx with uWSGI (full tutorial)"
& 
"his autosetup video basically just uses certbot on a properly set up server"

This saves you hours on system setup & redeployment of Django webservers!

Add a new user - configure the user to your project settings

apt-get update -y; apt-get upgrade -y
apt-get install python3.8
apt install python3.8-venv


python -m venv VM1 
source VM1/bin/activate
sudo chmod 777 * -R 
sudo chown -R www-data:www-data /home/stalin/VM1

<~ Install all the packged need your for your Django project ~>

