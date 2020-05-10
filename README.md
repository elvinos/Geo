# Deployment Setup For Vue + Django on Free AWS Server with Docker

This is an amalgamation of a some great repositories I came across in my quest to create a robust but repeatable setup to combine a Vue app with a backend onto a server on the premises of making code shareable, testable and streamlined for a hobbyist developer. There are a lot of great frameworks out there for developing apps, but when it came to deployment resources seem much more sparse and divided. Going from MAMP and FTP to then a world of using virtual machines with Trellis (Ansible) and Bedrock for Wordpress deployments - this still feels a world away from deploying Web-Apps (Progressive Web App), that embed scripts and APIs to give much more functionality than just a blog.

To build an app like this effectively and most importantly getting this deployed the technology reading list includes:

- Docker
- NGINX
- Modern servers - I.e. Heroku, AWS, Digital Ocean
- Python or Node.js backend framework - e.g. Django
- Front end framework e.g. Vue

To achieve something with the ease o  short reading list includes technologies to learn include docker and docker compose for development (easy enough if you are cloning someone else’s repository),  

Based of the Vue-Django cookie cutter fork, this code base enables Vue and Django to be developed and hosted in unison on the same server via NGINX.

This setup acts as a framework to accelerate the launch of Vue-Django apps on the web for hobbyists, using docker to keep the development and production environments aligned - similar to traditional server based web development with VMs. 

By completely separating the frontend and backed sections of the app, developers can easily swap out VUE for any other static front end (e.g. React), with a few NGINX tweaks.


## Ideology

Through Docker, the development environment is completely shareable to teams only requiring docker to be installed and running on their local machine and the .env file to be shared in order to deploy.
Docker Compose makes it super convenient to switch between a full development environment (with hot reloading for Vue), a mock staging environment - replicating the docker containers on the server. For a hobbyist time is invested to ensure that these Docker containers work correctly where by extension it makes sense for a remote server to follow these same principles to save time and cut down the testing process. Thanks docker deploy stack  (via Docker swarm) enables images on a server to be run in a very similar manner. Therefore this framework goes by the principle - time invested in creating the create docker compose setup is equally invested in the infrastructure and deployment side. 

As this is a hobbyist framework, the most important step is to get this app hosted in the most simple and cheap manner. After a lot of experimentation with Heroku (if someone has a similar setup like this which works there please share) , the 750 hours AWS EC2 server proved much easier to get running and best of all is FREE! Therefore the deployment workflow is focused around setting up and app on AWS. 




- [https://github.com/dwyl/learn-travis/blob/master/encrypted-ssh-keys-deployment.md]
- [https://github.com/vchaptsev/cookiecutter-django-vue]
- [https://github.com/creotiv/aws-docker-example]
- [https://hackernoon.com/deploying-on-aws-free-tire-with-docker-and-fabric-d9eca7c629e6]

