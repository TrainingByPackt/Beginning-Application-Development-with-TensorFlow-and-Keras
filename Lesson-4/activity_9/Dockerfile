#
#  Docker image for the Cryptonic application.
#  The image copies the complete application
#  directory and starts a Flask server. 
#
FROM python:3.6
ENV TZ=America/New_York

#
#  Setting up timezone to EST (New York).
#  Change this to whichever timezone your
#  data is configured to use.
#
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


COPY . /cryptonic

WORKDIR "/cryptonic"
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "run.py"]