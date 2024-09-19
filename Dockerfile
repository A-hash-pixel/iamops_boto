FROM python
WORKDIR /app
COPY ./ ./
RUN ls /app
RUN chmod +x /app/entrypoint.sh
RUN pip install -r /app/requirements.txt
ENTRYPOINT ["./entrypoint.sh"]