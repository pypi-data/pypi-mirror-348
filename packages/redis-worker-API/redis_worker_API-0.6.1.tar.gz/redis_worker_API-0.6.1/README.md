
Redis Message API
Overview
This Python module provides an interface to interact with a Redis server for sending, receiving, and processing messages and files. The RedisMsgAPI class facilitates the use of Redis streams to create and manage message groups, send and receive messages, and handle files across different streams.

Features
Message Processing: Convert Redis stream messages to JSON format.
Message Acknowledgment: Acknowledge messages in the stream after processing.
File Handling: Send single or multiple file names as messages through Redis streams.
Customizable: Allows for custom Redis host configuration through environment variables or default settings.
Installation
Make sure you have Redis and Python installed. You can install the required Python packages using pip:

bash
Copy code
pip install redis
Usage
Initialization
To use the RedisMsgAPI, you need to create an instance of the class with the required parameters:

python
Copy code
from redis_msg_api import RedisMsgAPI

api = RedisMsgAPI(
    group_name="your_group_name",
    in_stream_key="input_stream",
    in_app="app_name",
    out_stream_key="output_stream",
    out_file_key="output_file_stream",
    out_files_keys="output_files_stream",
    out_app="out_app_name",
    worker_name="worker_name"
)
Methods
process_message(message): Processes a message from the Redis stream and returns it as a JSON string.

get_message(in_stream): Retrieves a message from the specified input stream.

get_message_data(message_id): Retrieves message data based on the message ID.

ack_message(message_id): Acknowledges a message in the stream.

send_message(json_message): Sends a message to the output stream in JSON format.

send_message_data(message_data): Sends message data to the output stream.

send_file(file_name): Sends a file name as a message to the output file stream.

send_multiple_files(file_list): Sends multiple file names as a single message to the output files stream.

Example
Here is an example of how to use the RedisMsgAPI class:

python
Copy code
api = RedisMsgAPI(
    group_name="example_group",
    in_stream_key="in_stream",
    in_app="example_app",
    out_stream_key="out_stream",
    out_file_key="out_file",
    out_files_keys="out_files",
    out_app="out_app",
    worker_name="worker_1"
)

# Sending a message
api.send_message_data({"key": "value"})

# Receiving and processing a message
message = api.get_message("in_stream")
print("Received Message:", message)

# Acknowledging a message
api.ack_message("message_id")
Configuration
You can configure the Redis host using an environment variable. By default, the class connects to a Redis server on localhost on port 6379.

To change the Redis host, set the REDIS_HOST environment variable:

bash
Copy code
export REDIS_HOST="your_redis_host"
License
This project is licensed under the MIT License - see the LICENSE file for details.


To create the library use the following command codes
rm -rf dist/ build/
python3 setup.py sdist bdist_wheel
twine upload dist/*