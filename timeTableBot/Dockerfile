FROM python:3.8

# -- Install Pipenv stable
RUN pip install pipenv==v2020.11.4 --upgrade pip  
RUN pip install psycopg2

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# -- Install dependencies:
ADD ./req.txt ./tmp/req.txt
RUN cd /tmp &&  pip install -r req.txt

# -- Update system
RUN apt-get update
RUN apt-get install binutils libproj-dev gdal-bin -y