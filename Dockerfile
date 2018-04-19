# pre-build stage
FROM python:3-alpine as base

COPY requirements.txt /opt/
WORKDIR /opt

RUN apk add --update \
gcc \
musl-dev \
linux-headers

RUN pip3 install wheel && pip3 wheel -w /tmp/wheels -r requirements.txt

# ----------------------------
# install stage
FROM python:3-alpine

RUN apk --no-cache add git

COPY --from=base /tmp /tmp
COPY . /opt
WORKDIR /opt

RUN git submodule init
RUN git submodule update --depth 1

RUN pip install --no-index --find-links=/tmp/wheels -r requirements.txt
RUN rm -rfv /tmp/*

CMD /opt/app.py
