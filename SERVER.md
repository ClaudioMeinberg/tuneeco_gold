# SERVER Configuration

sudo apt update
sudo apt upgrade

sudo apt install ntp
sudo dpkg-reconfigure tzdata #America -> Sao_Paulo

# install required stuff
sudo apt-get install -yq git python3-virtualenv nginx uwsgi uwsgi-plugin-python3 virtualenv

sudo apt-get install -yq python3-dev default-libmysqlclient-dev build-essential

#adicionar usuario ao grupo www-data
sudo usermod -a -G www-data ubuntu
#NECESSÁRIO RE-LOGAR

# Cloning the repository
cd /usr/share/nginx/html/
sudo mkdir tuneeco_gold_INICIAL
sudo chown www-data:www-data tuneeco_gold_INICIAL
sudo chmod 775 tuneeco_gold_INICIAL
sudo ln -snf tuneeco_gold_INICIAL tuneeco_gold
cd /usr/share/nginx/html/tuneeco_gold
git clone https://Meinberg@bitbucket.org/Meinberg/tuneeco_gold.git .

# configure
sudo mkdir -p /var/log/tuneeco_gold/
sudo cp .env_sample .env
sudo vi .env


# Setup virtual environment
cd /usr/share/nginx/html
sudo mkdir venv-python3
sudo chown www-data:www-data venv-python3
sudo chmod 775 venv-python3
cd venv-python3
virtualenv -p python3 .
source bin/activate

# install stuff into venv
pip install -r /usr/share/nginx/html/tuneeco_gold/requirements.txt

# Fixing permissions
sudo chown www-data:www-data -R /usr/share/nginx/html/tuneeco_gold_INICIAL/

# nginx
## Removing the symlink
sudo rm -i /etc/nginx/sites-enabled/default

## Configuring
sudo su
cat > /etc/nginx/sites-available/tuneeco_gold << EOF
upstream django {
        server unix:///run/uwsgi/app/tuneeco_gold/socket;
}
server {
        listen 80;
        server_name SERVER_NAME;

        charset utf-8;
        client_max_body_size 5M;
        error_log  /var/log/nginx/tuneeco_gold.error.log;
        access_log /var/log/nginx/tuneeco_gold.access.log;

        location / {
                include uwsgi_params;
                uwsgi_pass django;
        }

        location /static {
            alias /usr/share/nginx/html/tuneeco_gold/collectedstaticfiles/;
        }
        location /cdn {
            alias /usr/share/nginx/html/tuneeco_gold/youtube/;
        }
}
EOF
exit

sudo ln -snf /etc/nginx/sites-available/tuneeco_gold /etc/nginx/sites-enabled/tuneeco_gold
sudo service nginx restart


# Configuring uwsgi
sudo su
cat > /etc/uwsgi/apps-available/tuneeco_gold.ini << EOF
[uwsgi]
# Project base dir.
chdir=/usr/share/nginx/html/tuneeco_gold/
# virtualenv
home=/usr/share/nginx/html/venv-python3/
socket=/run/uwsgi/app/tuneeco_gold/socket
pidfile=/run/uwsgi/app/tuneeco_gold/pid
module=tuneeco_gold.wsgi:application
plugin=python3
uid=www-data
gid=www-data
master=True
vacuum=True
max-requests=5000
harakiri=30
daemonize=/var/log/uwsgi/tuneeco_gold.log
env = DJANGO_SETTINGS_MODULE=tuneeco_gold.settings
single-interpreter=True
enable-threads=True
EOF
exit

sudo ln -snf /etc/uwsgi/apps-available/tuneeco_gold.ini /etc/uwsgi/apps-enabled/tuneeco_gold.ini
sudo service uwsgi restart

sudo chown www-data:www-data /var/log/uwsgi/app
sudo chown www-data:www-data /var/log/uwsgi/app/tuneeco_gold.log
sudo chown www-data:www-data /var/log/nginx/*.log
sudo touch /var/log/tuneeco_gold/debug.log
sudo chown www-data:www-data /var/log/tuneeco_gold/debug.log

mkdir /usr/share/nginx/html/tuneeco_gold/log
touch /usr/share/nginx/html/tuneeco_gold/log/debug.log
sudo chmod 006 /usr/share/nginx/html/tuneeco_gold/log/debug.log

cd /usr/share/nginx/html/tuneeco_gold

./manage.py migrate
./manage.py createsuperuser
./manage.py loaddata terra/fixtures/*


# install certbot - let's encrypt
sudo snap install --classic certbot
sudo certbot --nginx

# criar cronjob para
sudo systemctl enable cron
crontab -e
*/5 * * * * /usr/share/nginx/html/tuneeco_gold/cronjob.sh
crontab -l

# MariaDB
CREATE DATABASE tuneeco_gold;
CREATE USER 'DB_USER'@'%' IDENTIFIED BY '!';

grant select,update,delete,insert,create,drop,index,alter,lock tables, execute, create temporary tables, execute, trigger, create view, show view, event on tuneeco_gold.* to DB_USER@'%' ;

SHOW GRANTS for DB_USER;
SHOW GRANTS for 'DB_USER'@'%';
