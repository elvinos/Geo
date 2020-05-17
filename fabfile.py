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
DB_USER = os.getenv('POSTGRES_USER')
DB_DB = os.getenv('POSTGRES_DB')


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
        host.sudo('curl -L "https://github.com/docker/compose/releases/download/1.25.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose')
        host.sudo('chmod +x /usr/local/bin/docker-compose')
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
        host.sudo('docker service create --name registry --publish 5000:5000 registry:2')
        with host.cd(APP_NAME):
            host.run('git clone '+ GIT + ' .')
            host.put(".env", ("/home/ubuntu/"+APP_NAME+"/.env"))
            host.put('''docker-compose -c docker-compose-prod.yml build''')
            host.put('''docker-compose -c docker-compose-prod.yml push''')
            host.run('''docker stack deploy -c docker-compose-prod.yml %s''' % APP_NAME.lower())
            host.sudo('chmod +x backend/manage.py')
            host.run('''docker exec $(docker ps -q -f name=%s) python /manage.py createsuperuser --noinput''' % BACKEND_NAME)
    else:
        print('Docker already installed.')
        
@task
def set_pass(c):
      host.run('''docker exec $(docker ps -q -f name=%s) python manage.py createsuperuser --noinput''' % BACKEND_NAME)

@task
def deploy(c):
#     host.run('docker login -u %s -p %s' % (DOCKER_USER,DOCKER_PASS))
    with host.cd(APP_NAME):
        host.run('git pull')
        host.run('git checkout master')
        host.put(".env", ("/home/ubuntu/"+APP_NAME+"/.env"))
        host.run('''sudo docker-compose -f docker-compose-prod.yml build''')
        host.run('''sudo docker-compose -f docker-compose-prod.yml push''')
        host.run('''sudo docker stack deploy -c docker-compose-prod.yml %s''' % APP_NAME.lower())


@task
def pgdump(c):
    cid = host.run('docker container ls | grep ' + APP_NAME.lower()  +'_postgres | head -c 12').stdout.strip()
    host.run('''docker container exec %s sh -c "pg_dump -U %s %s | gzip > '/var/lib/postgresql/backups/%s.gz'"'''  % (cid, DB_USER, DB_DB, DB_DB))
    host.run('docker cp %s:/var/lib/postgresql/backups/%s.gz /tmp/%s.gz' % (cid, DB_DB, DB_DB))
    t = Transfer(host)
    t.get('/tmp/%s.gz' % DB_NAME)

@task
def test(c):
     host.run('''docker exec $(docker ps -q -f name=%s) ''' % BACKEND_NAME)
@task
def clean_docker(c):
     host.run('''docker system prune --volumes -f''')