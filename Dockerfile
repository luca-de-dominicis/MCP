# Pulls an image endowed with minizinc
FROM minizinc/minizinc:latest

# Setting the base folder for the container 
WORKDIR /src

# Coping all the content of this folder into the container
COPY . .  

# Installing python and its required libraries
RUN apt-get update \
  && apt-get install -y python3 \
  && apt-get install -y python3-pip

CMD python3 -m http.server 