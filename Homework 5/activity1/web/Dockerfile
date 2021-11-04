FROM  php:8-apache

COPY ./armbook_packaged/ /var/www/html/
COPY 000-default.conf /etc/apache2/sites-enabled/000-defauft.conf
COPY ./csec380.pem /etc/apache2/ssl/csec380.pem
COPY ./csec380.key /etc/apache2/ssl/csec380.key

RUN a2enmod ssl && a2enmod rewrite
RUN docker-php-ext-install mysqli && docker-php-ext-enable mysqli

EXPOSE 80 
EXPOSE 443