from setuptools import setup

setup(
    name="website_monitor",
    version="0.1",
    description="Website monitor",
    packages=["website_monitor"],
    install_requires=[
        "click",
        "confluent-kafka",
    ],
    entry_points={
        'console_scripts': [
            'website_monitor=website_monitor.cli:cli'
        ]
    },
    python_requires=">=3.7",
    zip_safe=False,
)
