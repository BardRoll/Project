# Settings on Raspberry Pi 3 Model B+
## Config ip address for WiFi
```bash
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```
```bash
network={
    ssid="WiFi name"
    psk="WiFi password"
}
```
If you have WiFi more than 1
```bash
network={
    ssid="WiFi name 1"
    psk="WiFi password 1"
    priority=1
}

network={
    ssid="WiFi name 2"
    psk="WiFi password 2"
    priority=2
}
```
---
## Avahi
 Avahi is use for multicast DNS/DNS-SD service discovery.
 [More details](https://en.wikipedia.org/wiki/Avahi_%28software%29)

 For example, to access local web application, I can use `http://hostname.local:8000` instead of `http://127.0.0.1:8000` or Raspberry Pi ip address.

 For another example, to SSH Raspberry Pi, I can use `hostname.local` instead of Raspberry Pi ip address
 
 **_(Raspberry Pi and your device must be on the same network.)_**

 ### Install and setup Avahi
(I followed the steps from this [website](https://forums.raspberrypi.com/viewtopic.php?t=267113).)
```bash
sudo apt-get install avahi-utils
sudo apt-get install avahi-daemon
sudo systemctl enable avahi-daemon.service
sudo systemctl start avahi-daemon.service
```
---
## Create virtual environment and install libraries for this project
Create virtual environment
```bash
python -m venv venv
```

Start virtual environment
```bash
source venv/bin/activate
```

Install libraries
```bash
pip install django
pip install launchpad
pip install launchpad_py
pip install psycopg2-binary
pip install pygame
```
---
## Install, settings and create (local) PostgreSQL database (on Raspberry Pi)
### Install
```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install postgresql postgresql-contrib
```

### Setting in file `pg_hba.conf`
```bash
sudo nano /etc/postgresql/{version}/main/pg_hba.conf
```

In file `pg_hba.conf`, add these command under #IPV4 and #IPV6
```bash
#IPV4
host    all             all             0.0.0.0/0            md5
#IPV6
host    all             all             ::1/0            md5
```

### Setting in file `postgresql.conf`
```bash
sudo nano /etc/postgresql/{version}/main/postgresql.conf
```

In file `postgresql.conf`, look for '**listen_address**' and change value to **'*'** **_(Don't forget to disable comment!)_**
```bash
listen_address = '*'
```

### Create user and database
Start PostgreSQL shell
```bash
sudo -u postgres psql
```

Create user and database *(replace `your_database_name`, `your_username`, `your_password` with your data)*
```sql
CREATE DATABASE your_database_name;
CREATE USER your_username WITH PASSWORD 'your_password';
ALTER ROLE your_username SET client_encoding TO 'utf8';
ALTER ROLE your_username SET default_transaction_isolation TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_username;
```
(exit shell with `\q`)

### Edit Django settings
Edit `DATABASE` in file `settings.py`
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'your_raspi_ip_address',
        'PORT': '5432',
    }
}
```
---
## Django `views.py`
Need to change some path in file `views.py`
```python
python_path = os.path.join(BASE_DIR, '..','.venv', 'Scripts', 'python.exe')
```

Change path to python in virtual environment
```python
python_path = os.path.join(BASE_DIR, '..','venv', 'bin', 'python')
```
---
## Automatically start PostgreSQL and Django server
Create shell script file
```bash
nano start_sjango.sh
```

Add command
```bash
#!/bin/bash

sudo service postgres start
cd /path/to/django/project
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

Change permission for this file
```bash
chmod +x start_django.sh
```

Open file `rc.local`
```bash
sudo nano /etc/rc.local
```

Add this command before `exit 0`
```bash
/path/to/start_django.sh
```
---
## Automatically send data from local PostgreSQL to PostgreSQL service
**Note: I use Aiven service in this project.**

### `backup_script.sh`
Create shell script file (like `backup_script.sh`)
```bash
#!/bin/bash

if ping -q -c 1 -W 1 google.com >/dev/null; then
    pg_dump -h localhost -p 5432 -U your_username -d your_database_name -F c -f /path/to/backup/datadump.dump
    pg_restore -h your_aiven_host -p your_aiven_port -U your_aiven_username -d your_aiven_database_name -F c -j 8 -v --clean /path/to/backup/datadump.dump
else
    echo "No internet connection."
fi
```
**Note: in `pg_restore` command is not the good way to send or update data**

Change permission for this file
```bash
chmod +x backup_script.sh
```

### `.pgpass`
Create and open file `.pgpass` in user home directory (to make the `pg_dump` and `pg_restore` commands work without having to enter a password each time.)
```bash
touch ~/.pgpass
nano ~/.pgpass
```

Add data for login PostgreSQL
```bash
localhost:5432:*:your_username:your_password
your_aiven_host:your_aiven_port:*:your_aiven_username:your_aiven_password
```

Change permission for this file
```bash
chmod 600 ~/.pgpass
```

### Cron job
Add cron job for run script every 3 minutes
```bash
crontab -e
```

Add this command at the end of script ([Cron format examples](https://crontab.guru/))
```bash
*/3 * * * * /path/to/backup_script.sh
```
---
## `show.py`
At this code
```python
media_path = os.path.join(BASE_DIR, 'Launchpad', 'web_server', 'myapp', 'media')
```
Need to change path, for example
```python
media_path = os.path.join(BASE_DIR, 'your_project_folder', 'web_server', 'myapp', 'media')
```