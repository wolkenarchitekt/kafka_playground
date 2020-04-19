FROM ubuntu:bionic
RUN apt-get update --fix-missing
RUN apt-get install nginx -y
COPY index.html /var/www/html/
EXPOSE 80
CMD ["nginx","-g","daemon off;"]
