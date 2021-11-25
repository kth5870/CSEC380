FROM  php:8-apache

RUN mkdir -p /etc/apache2/ssl
RUN a2enmod ssl && a2enmod rewrite && a2enmod http2 && a2enmod headers 
RUN docker-php-ext-install mysqli && docker-php-ext-enable mysqli

COPY ./hw7_armbook/ /var/www/html/
COPY ./000-default.conf /etc/apache2/sites-enabled/000-default.conf
COPY ./csec380.pem /etc/apache2/ssl/csec380.pem
COPY ./csec380.key /etc/apache2/ssl/csec380.key

RUN service apache2 restart

EXPOSE 80 
EXPOSE 443