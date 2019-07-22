# divipay-challenge

I've used RabbitMQ for message broker service
```shell
rabbitmq-server
```

To launch celery worker
```shell
cd divipay
celery -A divipay worker -l info
```
