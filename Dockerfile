# based on official python image
FROM python:3.8

# update and install gcc and python3-dev
RUN apt-get update
RUN apt-get install -y --no-install-recommends gcc libc-dev python3-dev python3-setuptools

#  upgrade pip
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

# change working directory 
RUN mkdir /app
WORKDIR /app

# install dependencies
COPY requirements.txt . 

# install dependencies
RUN pip install -r requirements.txt

# copy everything else from the current directory to the app directory
COPY . .

# run entrypoint.sh
ENTRYPOINT ["sh", "entrypoint.sh"]