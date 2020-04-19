from setuptools import setup

setup(
    name="website_monitor_db",
    version="0.1",
    description="Retrieve website monitor records and save to DB",
    packages=["website_monitor_db"],
    install_requires=[
        "click",
        "confluent-kafka",
        "psycopg2",
    ],
    entry_points={
        'console_scripts': [
            'website_monitor_db=website_monitor_db.cli:cli'
        ]
    },
    python_requires=">=3.7",
    zip_safe=False,
)
