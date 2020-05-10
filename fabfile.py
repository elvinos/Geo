from fabric2 import task, Connection
from fabric2.transfer import Transfer
import time
import getpass
from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.getenv('IP')
KEY_FILE = os.getenv('KEY_FILE')
DEFAULT_LOGIN = os.getenv('DEFAULT_LOGIN')
DEFAULT_PASS = os.getenv('DEFAULT_PASS')
DEFAULT_USER = os.getenv('DEFAULT_USER')
GIT = os.getenv('GIT')
APP_NAME = os.getenv('APP_NAME')
BACKEND_NAME = os.getenv('BACKEND_NAME')
NGINX_NAME = os.getenv('NGINX_NAME')
DB_NAME = os.getenv('DB_NAME')
DOCKER_PASS = os.getenv('DOCKER_PASS')
DOCKER_USER = os.getenv('DOCKER_USER')

host = Connection(host=str(HOST),
                  user='ubuntu',
                  port=22, 
                  connect_kwargs={"key_filename":[KEY_FILE]})

@task
def install_instance(c):
    if True or host.sudo('service docker status', hide='out', warn=True).failed:
        print('Docker not found. Installing it.')
        host.sudo('apt-get update')
        host.sudo('apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common')
        host.sudo('curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -')
        host.sudo('apt-key fingerprint 0EBFCD88')
        host.sudo('add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"')
        host.sudo('apt-get update')
        host.sudo('apt-get install -y docker-ce docker-ce-cli containerd.io')
        host.sudo('usermod -a -G docker $USER')
        host.sudo('systemctl restart docker')
        host.sudo('docker login -u %s -p %s' % (DOCKER_USER,DOCKER_PASS))
        host.sudo('docker swarm init')
        print('### KEY ######################################################################')
        host.run('ssh-keygen -t rsa -C "' + DEFAULT_LOGIN + '" -f ~/.ssh/id_rsa -q -N ""')
        host.run('cat ~/.ssh/id_rsa.pub')
        print('### KEY ######################################################################')
        res = 't'
        while res.lower():
            res = getpass.getpass('Update you github account and hit enter.')
        host.run('ssh-keyscan github.com >> ~/.ssh/known_hosts')
        host.run('mkdir ' + APP_NAME)
        host.sudo('chmod 666 /var/run/docker.sock')
        with host.cd(APP_NAME):
            host.run('git clone '+ GIT + ' .')
            host.put(".env", ("/home/ubuntu/"+APP_NAME+"/.env"))
            host.run('''docker build -t %s backend''' % BACKEND_NAME)
            host.run('''docker build -f nginx/Dockerfile  -t %s .''' % NGINX_NAME)
            host.run('''docker stack deploy -c docker-compose-prod.yml %s''' % APP_NAME.lower())
            while True:
                res = host.run('docker service ls | grep '+ BACKEND_NAME +'.*0/')
                if not res.stdout.strip():
                    time.sleep(4)
                    break
                time.sleep(2)
            host.sudo('chmod +x backend/manage.py')
            host.run('''docker exec $(docker ps -q -f name=%s) python /backend/manage.py createsuperuser --noinput''' % BACKEND_NAME)
    else:
        print('Docker already installed.')
        
@task
def set_pass(c):
    host.sudo('chmod +x backend/manage.py')
    host.run('''docker exec $(docker ps -q -f name=%s) python /backend/manage.py createsuperuser --noinput''' % BACKEND_NAME)

@task
def deploy(c):
    host.run('docker login -u %s -p %s' % (DOCKER_USER,DOCKER_PASS))
    with host.cd(APP_NAME):
        host.run('git pull')
        host.run('git checkout master')
        host.put(".env", ("/home/ubuntu/"+APP_NAME+"/.env"))
        host.run('''docker build -t %s backend''' % BACKEND_NAME.replace("_", "-"))
        host.run('''docker build -f nginx/Dockerfile  -t %s .''' % NGINX_NAME.replace("_", "-"))
        host.run('''docker stack deploy -c docker-compose-prod.yml %s''' % APP_NAME.lower())
        while True:
            res = host.run('docker service ls | grep '+ BACKEND_NAME +'.*0/')
            if not res.stdout.strip():
                time.sleep(4)
                break
            time.sleep(2)
        host.sudo('chmod +x backend/manage.py')
        host.run('''docker exec $(docker ps -q -f name=%s) python /backend/manage.py createsuperuser --noinput''' % BACKEND_NAME)
        host.run('docker service update ' + BACKEND_NAME)

@task
def pgdump(c):
    cid = host.run('docker container ls | grep ' + DB_NAME +' | head -c 12').stdout.strip()
    host.run('''docker container exec %s sh -c "pg_dump -U %s %s | gzip > '/var/lib/postgresql/backups/%s.gz'"'''  % (cid, APP_NAME, APP_NAME, APP_NAME))
    host.run('docker cp %s:/var/lib/postgresql/backups/%s.gz /tmp/%s.gz' % (cid, APP_NAME, APP_NAME))
    t = Transfer(host)
    t.get('/tmp/&s.gz' % APP_NAME)

@task
def test(c):
     host.run('''docker exec $(docker ps -q -f name=%s) ''' % BACKEND_NAME)