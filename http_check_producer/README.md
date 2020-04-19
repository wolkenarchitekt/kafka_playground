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
