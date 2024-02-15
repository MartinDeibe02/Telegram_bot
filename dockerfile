FROM continuumio/miniconda3

WORKDIR /app

COPY bot_mdm/bot.py /app/
COPY bot_mdm/utils /app/utils

WORKDIR /app/utils

RUN conda env create -f environment.yml

WORKDIR /app

CMD ["/bin/bash", "-c", "source activate sbd_env && python bot.py"]
