FROM  php:7.2-apache
COPY armbook_packaged/ /var/www/html/

RUN docker-php-ext-install mysqli && docker-php-ext-enable mysqli