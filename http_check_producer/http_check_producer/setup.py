from setuptools import setup

setup(
    name="http_check_producer",
    version="0.1",
    description="HTTP check producer",
    packages=["http_check_producer"],
    install_requires=[
        "click",
        "confluent-kafka",
    ],
    entry_points={
        'console_scripts': [
            'http_check_producer=http_check_producer.cli:cli'
        ]
    },
    python_requires=">=3.7",
    zip_safe=False,
)
