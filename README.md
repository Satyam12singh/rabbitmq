# RabbitMQ Producer-Consumer Example

This project provides a simple command-line based producer-consumer application using RabbitMQ in Python.

## Overview

The application demonstrates the basic principles of a message queue system where a producer sends messages and a consumer receives them.

- **`producer.py`**: A command-line interface that prompts the user for a message, sends it to a RabbitMQ queue named `rabbitmq_test`, and waits for the next message.
- **`consumer.py`**: Listens to the `rabbitmq_test` queue and logs any messages it receives.
- **`mq.py`**: A utility module containing a `Rabbitmq` class that handles the connection, channel, and queue logic for both producing and consuming messages.
- **`logs/mq.log`**: All events, such as received messages and connection errors, are logged to this file.

## Prerequisites

- Python 3.12+
- A running RabbitMQ instance

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Satyam12singh/rabbitmq
    cd rabbitmq
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    or
    ```
    uv add -r requirements.txt
    ```

5.  **Configure credentials:**
    Create a `.env` file in the root of the project directory. This file should contain the connection details for your RabbitMQ instance.

    ```env
    RABBIT_MQ_HOST=localhost
    RABBIT_MQ_PORT=5672
    RABBIT_MQ_USER=guest
    RABBIT_MQ_PASSWORD=guest
    ```

## Usage

To run the application, you will need two separate terminal windows, both with the virtual environment activated.

1.  **Start the Consumer:**
    In the first terminal, run the following command to start the consumer. It will begin listening for messages on the `rabbitmq_test` queue.
    ```bash
    python consumer.py
    ```

2.  **Start the Producer:**
    In the second terminal, run this command to start the producer.
    ```bash
    python producer.py
    ```
    The producer will prompt you to enter a message. Type your message and press Enter to send it to the queue. The consumer in the other window should then receive and log it.

    To stop the producer, type `exit`.

Feel free to use this code wherever you want to use RabbitMQ hassle-free.
