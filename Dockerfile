FROM python:3.10
# set work directory
ADD django-app /usr/src/app/
WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install -y supervisor
RUN apt-get install -y nano

# install dependencies
RUN pip install -r requirements.txt

# unprivileged user for container
RUN set -x \
    && useradd -M -d /usr/src/app user -u 1000 \
    && chown -R user:user /usr/src/app

# uwsgi settings
COPY --chown=user django-app/uwsgi.ini /etc/uwsgi.ini
COPY --chown=user static/ /usr/src/app/

USER 0
CMD ["supervisord", "-c", "/usr/src/app/supervisord.conf"]
EXPOSE 8000
