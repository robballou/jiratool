FROM python:3.6

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

# ENV PYTHONPATH="${PYTHONPATH}:/app"
# CMD python -c "import sys; print(sys.path)"
CMD [ "python", "jiratool.py" ]
