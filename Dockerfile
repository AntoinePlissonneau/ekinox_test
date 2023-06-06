FROM python:3.10

ENV DASH_DEBUG_MODE True
COPY ./app /app
WORKDIR /app
RUN set -ex && \
    pip install -r requirements.txt
EXPOSE 8501

EXPOSE 8888

CMD ["streamlit", "run", "webapp.py", "--server.port=8501", "--server.address=0.0.0.0"]

