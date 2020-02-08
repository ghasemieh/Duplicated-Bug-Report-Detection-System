FROM python:3
WORKDIR /prj
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_lg
COPY . .
EXPOSE 5000
CMD ["python","./main.py"]
