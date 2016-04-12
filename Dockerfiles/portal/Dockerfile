# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/c3s.ado

FROM c3sado_tryton
MAINTAINER Udo Spallek <udono@virtual-things.biz>

WORKDIR /opt
RUN wget -O phantomjs.tar.bz2 https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
RUN mkdir phantomjs
RUN tar -xf phantomjs.tar.bz2 -C phantomjs --strip-components=1
RUN ln -s /opt/phantomjs/bin/phantomjs /usr/local/bin/phantomjs
WORKDIR /ado

RUN pip install  \
    colander==1.0  \
    cornice==1.0.0  \
    coverage==3.7.1  \
    cryptacular==1.4.1  \
    deform==2.0a2  \
    nose==1.3.6  \
    pyramid==1.5.7  \
    pyramid_beaker==0.8 \
    pyramid-chameleon==0.3  \
    pyramid_debugtoolbar==2.3  \
    pyramid_mailer==0.14 \
    pyramid_oauth2_provider==0.2  \
    webtest==2.0.18  \
    waitress==0.8.9 \
    requests==2.9.1 \
    selenium==2.53.1
