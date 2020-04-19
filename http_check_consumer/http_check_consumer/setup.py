from setuptools import setup

setup(
    name="http_check_consumer",
    version="0.1",
    description="HTTP check consumer",
    packages=["http_check_consumer"],
    install_requires=[
        "click",
        "confluent-kafka",
        "psycopg2",
    ],
    entry_points={
        'console_scripts': [
            'http_check_consumer=http_check_consumer.cli:cli'
        ]
    },
    python_requires=">=3.7",
    zip_safe=False,
)
