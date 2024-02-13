FROM continuumio/miniconda3

WORKDIR /app

COPY bot.py /app/
COPY utils /app/utils

WORKDIR /app/utils

RUN conda env create -f environment.yml

WORKDIR /app

CMD ["/bin/bash", "-c", "source activate sbd_env && python bot.py"]



