
########## local develop with docker ############

# Build image base on Dockerfile
docker build . -t uncleben006/fortune_telling

# Run container in daemon and mount project
docker run -it -d --name fortune_telling \
-p 443:443 -p 80:80 \
-e LC_ALL=C.UTF-8 \
-v /media/ben_wang/ben/github/fortune_telling/:/usr/src/app \
uncleben006/fortune_telling bash

# Execute container
docker exec -it fortune_telling bash

# Run uwsgi
# Bind soft link for project Nginx config
# Remove default Nginx config
# Start Nginx service
uwsgi uwsgi.ini
ln -s /etc/nginx/sites-available/fortune_nginx.conf /etc/nginx/sites-enabled/fortune_nginx.conf
rm /etc/nginx/sites-enabled/default
service nginx start

########## local develop with docker ############


########## Deploy to the cloud with docker ############

# push to my docker hub
docker push uncleben006/fortune_telling

# pull and run on the cloud
docker run -it -d --name fortune_telling \
-p 80:80 -p 443:443 \
-e LC_ALL=C.UTF-8 \
uncleben006/fortune_telling bash

########## Deploy to the cloud with docker ############

