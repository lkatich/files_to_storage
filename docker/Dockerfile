FROM python:3.10

RUN bash -c 'mkdir -pv /home/app/{files_to_storage,files,storage,files_to_storage/log}'

COPY files_to_storage /home/app/files_to_storage
COPY README.md setup.py /home/app/


WORKDIR /home/app/files_to_storage
RUN python3.10 /home/app/setup.py install

CMD ["python3.10", "handler.py"]





