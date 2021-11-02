FROM  php:8-apache

COPY ./armbook_packaged/ /var/www/html/

COPY ./csec380.pem /etc/apache2/ssl/csec380.pem

COPY ./csec380.key /etc/apache2/ssl/csec380.key

RUN a2enmod ssl
RUN docker-php-ext-install mysqli && docker-php-ext-enable mysqli