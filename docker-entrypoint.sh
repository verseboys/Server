#!/bin/bash

set -e

# Usage:
#     /entrypoint.sh http   # start nginx to serve static files and proxy other requests to wsgi backend
#     /entrypoint.sh api    # start django server
#     /entrypoint.sh any-command

run_http() {
    # https://github.com/jwilder/nginx-proxy/blob/master/docker-entrypoint.sh#L22
    #local RESOLVERS=$(awk '$1 == "nameserver" {print ($2 ~ ":")? "["$2"]": $2}' ORS=' ' /etc/resolv.conf | sed 's/ *$//g')
    #sed -i "s@{{RESOLVERS}}@${RESOLVERS}@g" /etc/nginx/conf.d/default.conf

    exec nginx -g "daemon off;"
}

run_api() {
    python manage.py migrate
    rsync -av --exclude=.placeholder skeleton/images/ ./images/
    rsync -av --exclude=.placeholder skeleton/media/  ./media/
    exec gunicorn \
        --bind=0.0.0.0:8080 \
        --workers=4 \
        --name="yizhu api server" \
        yizhu.wsgi
}

run_celery() {
    exec celery -A yizhu worker -l info
}

run_celery_beat() {
    exec python manage.py celery beat --max-interval=5
}

help() {
    echo "Usage:"
    echo "    docker run ... http           # start nginx to serve static files and proxy api requests"
    echo "    docker run ... api            # start django server"
    echo "    docker run ... any-command    # run specified command in the container"
}

if test -z "$1"; then
    help
    exit 1
fi

case "$1" in
    http)
        run_http
        ;;
    api)
        run_api
        ;;
    celery)
        run_celery
        ;;
    celery_beat)
        run_celery_beat
        ;;
    *)
        exec "$@"
        ;;
esac
