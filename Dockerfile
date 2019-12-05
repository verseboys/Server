FROM registry.docker-cn.com/library/node:8 as npm-builder

ARG NPM_TOKEN

RUN set -e \
	&& npm config set unsafe-perm true \
	&& npm config set //npm.natureself.site/:_authToken "$NPM_TOKEN" \
	&& npm config set registry https://npm.natureself.site

WORKDIR /project

COPY api/front/anniversary/ /project/anniversary/
COPY supervisor/new_manager/ /project/new_manager/

RUN set -e \
	&& cd /project/anniversary/ && npm install && npm run build \
	&& cd /project/new_manager/ && npm install && npm run build

# -------- 8< --------

FROM registry.docker-cn.com/library/alpine:3.7

ENV PROJECT_ROOT /project
WORKDIR $PROJECT_ROOT

RUN sed -i 's@http://dl-cdn.alpinelinux.org/alpine@https://mirrors.ustc.edu.cn/alpine@g' /etc/apk/repositories \
	&& apk add --no-cache python2 py2-pip nginx bash rsync py2-pillow mariadb-client-libs \
	&& mkdir -p /run/nginx \
	&& ln -snf /dev/stdout /var/log/nginx/access.log \
	&& ln -snf /dev/stdout /var/log/nginx/error.log

ADD requirements.txt $PROJECT_ROOT/
RUN apk add --no-cache --virtual .build-dep python2-dev build-base mariadb-dev \
	&& pip install -i https://mirrors.ustc.edu.cn/pypi/web/simple -r requirements.txt \
	&& apk del .build-dep

ADD . $PROJECT_ROOT
ADD docker-entrypoint.sh /entrypoint.sh
ADD nginx.conf /etc/nginx/conf.d/default.conf
RUN set -x \
	&& ln -snf settings_build.py yizhu/settings.py \
	&& python manage.py collectstatic --noinput \
	&& rm -f yizhu/settings.py

COPY --from=npm-builder /project/anniversary/dist/anniversary_static /project/frontend-apps/anniversary_static
COPY --from=npm-builder /project/anniversary/dist/index.html /project/frontend-apps/anniversary/index.html
COPY --from=npm-builder /project/new_manager/dist/new_manager_static/ /project/frontend-apps/new_manager_static
COPY --from=npm-builder /project/new_manager/dist/index.html /project/frontend-apps/new_manager/index.html

ENTRYPOINT ["/entrypoint.sh"]
