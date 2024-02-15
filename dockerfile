FROM continuumio/miniconda3


ARG WEATHER_TOKEN
ARG NASA_TOKEN

ENV WEATHER_TOKEN=$WEATHER_TOKEN
ENV NASA_TOKEN=$NASA_TOKEN


WORKDIR /app

COPY bot_mdm/bot.py /app/
COPY bot_mdm/utils /app/utils

WORKDIR /app/utils

RUN conda env create -f environment.yml

WORKDIR /app

CMD ["/bin/bash", "-c", "source activate sbd_env && python bot.py"]
