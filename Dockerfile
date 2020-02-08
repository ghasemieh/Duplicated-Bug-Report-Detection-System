FROM python:3
WORKDIR /home/alireza/PycharmProjects/Duplicate-Bug-Identification-System
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_lg
COPY . .
CMD ["python","./main.py"]
