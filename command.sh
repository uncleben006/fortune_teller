
########## local develop with docker ############

# Pull and Run postgres container
docker run --name postgres -p 172.17.0.2:5432:5432 -e POSTGRES_PASSWORD=1234 -d postgres

# Build image base on Dockerfile
docker build . -t uncleben006/fortune_teller

# Run container in daemon and mount project
docker run -it -d --name fortune_teller \
-p 443:443 -p 80:80 \
-e LC_ALL=C.UTF-8 \
-v /media/ben_wang/ben/github/fortune_teller/:/usr/src/app \
uncleben006/fortune_teller bash

# Execute container
docker exec -it fortune_teller bash

# Run uwsgi
# Bind soft link for project Nginx config
# Remove default Nginx config
# Start Nginx service
# Start Redis server
uwsgi uwsgi.ini
ln -s /etc/nginx/sites-available/fortune_nginx.conf /etc/nginx/sites-enabled/fortune_nginx.conf
rm /etc/nginx/sites-enabled/default
service nginx start
redis-server &

########## local develop with docker ############


########## Deploy to the cloud with docker ############

# push to my docker hub
docker push uncleben006/fortune_teller

# pull and run on the cloud
docker run -it -d --name fortune_teller \
-p 80:80 -p 443:443 \
-e LC_ALL=C.UTF-8 \
uncleben006/fortune_teller bash

########## Deploy to the cloud with docker ############

