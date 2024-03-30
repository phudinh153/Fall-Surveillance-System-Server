FROM rabbitmq:3-management

# Define environment variables.
COPY ./docker/production/rabbitmq/start.sh /start.sh
RUN sed -i 's/r$//g' /start.sh
RUN chmod +x /start.sh