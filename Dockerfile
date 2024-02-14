FROM php:7.2-cli
COPY cli.php /cli.php
RUN chmod +x /cli.php
CMD php /cli.php