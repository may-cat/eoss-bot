FROM python:3.10

# set work directory
ADD django-app /usr/src/app/
WORKDIR /usr/src/app

# install dependencies
RUN pip install -r requirements.txt

# unprivileged user for container
RUN set -x \
    && useradd -M -d /usr/src/app user -u 1000 \
    && chown -R user:user /usr/src/app

# uwsgi settings
COPY --chown=user django-app/uwsgi.ini /etc/uwsgi.ini

CMD ["uwsgi", "--ini", "/etc/uwsgi.ini"]
EXPOSE 8000
