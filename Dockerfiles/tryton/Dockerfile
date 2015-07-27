# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/c3s.ado

FROM debian:jessie
MAINTAINER Udo Spallek <udono@virtual-things.biz>

RUN apt-get update && apt-get install -y --no-install-recommends  \
    locales  \
    wget  \
    build-essential  \
    postgresql-client-9.4  \
    sqlite3  \
    ssl-cert  \
    ca-certificates  \
    python

RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py

RUN apt-get install -y --no-install-recommends  \
    python-dev  \
    python-pydot  \
    # python2.7-lxml  \
        libxml2-dev  \
        libxslt-dev  \
    # python-psycopg2  \
        libpq-dev  \
    # python-openssl  \
        libssl-dev  \
        libffi-dev

ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
RUN localedef -i en_US -f UTF-8 en_US.UTF-8

ENV PYTHONUNBUFFERED 1
RUN pip install  \
    PyWebDAV==0.9.8  \
    click==4.0  \
    interlude==1.3.1  \
    lxml==3.4.0  \
    mock==1.0.1  \
    polib==1.0.5  \
    "proteus<3.5.0" \
    psycopg2==2.5.4  \
    py-bcrypt==0.4  \
    pyOpenSSL==0.14  \
    python-Levenshtein==0.11.2  \
    python-dateutil==2.2  \
    python-sql==0.4  \
    pytz==2015.4  \
    relatorio==0.6.1  \
    simplejson==3.6.5  \
    vatnumber==1.2


RUN mkdir -p /ado
WORKDIR /ado
ENV PATH $PATH:/ado
