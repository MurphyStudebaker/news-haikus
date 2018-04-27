FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pyhyphen
RUN pip install -U nltk

COPY . .

CMD [ "python", "./newsHaikus.py" ]
