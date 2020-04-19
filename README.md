# Kafka HTTP check processor

[![Build Status](https://travis-ci.com/wolkenarchitekt/kafka_playground.svg?branch=master)](https://travis-ci.com/wolkenarchitekt/kafka_playground)

Perform HTTP checks against a website and write check results to Kafka and 
Postgres, consisting of these components:

### HTTP check producer

Python application to perform HTTP checks against a website.
Check results are pushed to a Kafka topic, using Avro schema.

The producer can be used as a CLI client or as a Python library.
Usage as CLI client to run once:

```bash
http_check_producer run-once --url ${URL} --match-regex ${REGEX}
```

Usage as CLI client to run forever:

```bash
http_check_producer run --url ${URL} --match-regex ${REGEX}
```

### HTTP check consumer

Python application to read HTTP check result messages from Kafka and write
them to Postgres. 

The consumer can be used as a CLI client or as a Python library.

Usage as CLI client to run once:

```bash
http_check_consumer run-once
```

Usage as CLI client to run forever:

```bash
http_check_producer run
```

 
## Development
For local development, `docker-compose.dev.yml` contains a full development
 environment to test HTTP-check-producer and HTTP-check-consumer on a
  workstation.

Components:
* nginx serving dummy website
* postgres DB with http-check Schema applied
* http-check-producer
* http-check-consumer
* Kafka all-in-one stack provided by lensesio
  
All development commands are wrapped within the Makefile.
  
Run local development stack:
```.makefile
make up
```
This will start all required services, including `http_check_producer`
and `http_check_consumer`, which will immediately start doing their work.

## Tests

All tests, including integration tests are running within Travis: 

https://travis-ci.com/github/wolkenarchitekt/kafka_playground

Run unit tests:
```.makefile
make test-unit
```

Run integration tests (tests run against full docker compose stack, including Kafka and Postgres):

```.makefile
make test-integration
```

Run all linting checks (mypy, flake8):
```.makefile
make lint
```


## TODO

If I had more time, these are the things I would put more thoughts into:

* Prepare project so it can be configured to use Aiven services
  * Allow passing Aiven credentials to connect to Postgres
  * Allow passing credentials and certificates to connect to Aiven Kafka
* Optimize Postgres schema - use Indexes efficiently
* Push Docker images for `http-check-producer` and `http-check-consumer` to docker hub 
for faster Docker-cached CI builds 
* Add more meaningful unit tests and integration tests, increase code coverage
* Evaluate DB schema migration tools ([Sqitch](https://github.com/sqitchers/sqitch), 
[Flyway](https://flywaydb.org/)) to migrate DB schema for production use

Furthermore I'd investigate if there is a need to write code for `http-check-producer` 
and `http-check-consumer` at all: 

* `http-check-consumer` could possibly be replaced with Kafka-connect JDBC-sink 
* Prometheus, Blackbox-exporter and Kafka-exporter could possibly replace `http-check-producer` 
(but might be overkill...)
