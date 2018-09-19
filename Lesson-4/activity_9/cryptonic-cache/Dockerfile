FROM redis:alpine
ENV TZ=America/New_York
# COPY redis.conf /usr/local/etc/redis/redis.conf
# CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]

#
#  Setting up timezone to EST (New York).
#  Change this to whichever timezone your
#  data is configured to use.
#
RUN apk add -U tzdata \
        && cp /usr/share/zoneinfo/$TZ /etc/localtime

EXPOSE 6379

CMD [ "redis-server" ]