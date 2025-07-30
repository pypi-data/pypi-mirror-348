import redis
import json
import os
import traceback

class RedisMsgAPI: 
    def __init__(self,
                 group_name: str, 
                 stream_key: str,
                 worker_name: str,
                 env_host: str = 'REDIS_HOST',
                 local_host: str = 'localhost',
                 port: int = 6379,
                 verbose: bool = True):

        # Get the Redis host from the environment variables
        redis_host = os.getenv(env_host, local_host)

        # Connect to Redis using the host
        self.r = redis.Redis(host=redis_host, port=port)
        self.stream_key = stream_key
        self.group_name = group_name
        self.worker_name = worker_name
        
        try:
            self.r.xgroup_create(self.stream_key, self.group_name, id='0', mkstream=True)    
        except redis.exceptions.ResponseError as e:
            if not str(e).startswith("BUSYGROUP"):
                raise
        
        
    def process_message (self, message):
        try:
            message_id, message_data = message
            
            # Convert the bytes to strings
            data = {key.decode('utf-8'): value.decode('utf-8') for key, value in message_data.items()}
            data['message_id'] = message_id.decode('utf-8')
            # Convert the dictionary to a JSON string
            json_message = json.dumps(data)
            
            #self.ack_message(message_id)

            return json_message
        except Exception as e:
            return f"Error processing message: {str(e)}"
        
    
    def get_message(self,new_message:bool=False, message_id=None):
        stream_id = '>' if new_message else '0'
        stream_key = {self.stream_key: stream_id}
        if new_message:
            stream_id = '>'
        elif message_id:
            stream_id = message_id
        else:
            stream_id = '0'
        try:
            messages = self.r.xreadgroup(
                self.group_name, 
                self.worker_name, 
                stream_key, 
                count=1, 
                block=1000)
            if messages:
                # messages is a list of (stream, [(msg_id, {data})]) tuples
                stream_name, entries = messages[0]
                if entries:
                    # Safely access first message entry
                    json_message = self.process_message(entries[0])
                    
                else:
                    json_message = None
            else:
                json_message = None

            return json.loads(json_message)
        
        except Exception as e:
            
            traceback.print_exc()
            return f"Error getting message: {str(e)}"

    
    def get_message_data(self, message_id):
        try:
            message = self.r.hgetall(message_id)
            data = json.loads(message[b'data'])
            return data
        except Exception as e:
            return f"Error getting message data: {str(e)}"
    
    def get_pending_ack(self):
        try:
        #stream = self.r.xreadgroup(self.group_name, self.worker_name, {self.stream_key: '>'}, count=1, block=1000)[0][0]
            pending = self.r.xpending(self.stream_key, self.group_name)
            return pending
        except Exception as e:
            return f"Error retrieving pending messages: {str(e)}"
    
    def get_all_pending_messages(self):
        try:
            pending_summary = self.r.xpending(self.stream_key, self.group_name)
            #print(f"Pending summary: {pending_summary}")
            pending_messages = []
            if pending_summary['pending'] > 0:
                message_id_list = ()
                pending_details = self.r.xpending_range(self.stream_key, self.group_name, '-', '+', pending_summary['pending'])
                for message in pending_details:
                    # Print the message details for debugging
                    print(f"Pending message details: {message}")
                    
                    message_id = message['message_id']
                    message_id_list += (message_id,)
                    consumer = message['consumer']
                    #time_since_delivered = message['time_since_delivered']
                    #times_delivered = message['times_delivered']
                    idle_time = message.get('idle', 'N/A')  # Use .get() to avoid KeyError
                    delivery_count = message.get('delivery_count', 'N/A')  # Use .get() to avoid KeyError
                    
                    pending_messages.append({
                        'message_id': message_id,
                        'consumer': consumer,
                        #'time_since_delivered': time_since_delivered,
                        #'times_delivered': times_delivered,
                        'idle_time': idle_time,
                        'delivery_count': delivery_count
                    })
                print(message_id_list)
            return pending_messages
        except Exception as e:
            return f"Error retrieving pending messages: {str(e)}"
    
    def get_unassigned_pending_messages(self):
        try:
            pending_summary = self.r.xpending(self.stream_key, self.group_name)
            unassigned_messages = []
            if pending_summary['pending'] > 0:
                pending_details = self.r.xpending_range(self.stream_key, self.group_name, '-', '+', pending_summary['pending'])
                for message in pending_details:
                    # Check if the message is not assigned to any worker
                    if message['consumer'] == '':
                        message_id = message['message_id']
                        idle_time = message.get('idle', 'N/A')  # Use .get() to avoid KeyError
                        delivery_count = message.get('delivery_count', 'N/A')  # Use .get() to avoid KeyError
                        
                        unassigned_messages.append({
                            'message_id': message_id,
                            'idle_time': idle_time,
                            'delivery_count': delivery_count
                        })
            return unassigned_messages
        except Exception as e:
            return f"Error retrieving unassigned pending messages: {str(e)}"
        
    def get_stream_info(self):
        try:
            stream_info = self.r.xinfo_stream(self.stream_key)
            return stream_info
        except Exception as e:
            return f"Error retrieving stream info: {str(e)}"
    
    def get_stream_length(self):
        try:
            stream_length = self.r.xlen(self.stream_key)
            return stream_length
        except Exception as e:
            return f"Error retrieving stream length: {str(e)}"

    def ack_message(self, message_ids):
        try:
            if isinstance(message_ids, (list, tuple)):
                for message_id in message_ids:
                    self.r.xack(self.stream_key, self.group_name, message_id)
            else:
                self.r.xack(self.stream_key, self.group_name, message_ids)
        except Exception as e:
            return f"Error acknowledging message: {str(e)}"
        
    def send_message(self, json_message):
        try:
            if isinstance(json_message, str):
                message = json.loads(json_message)
            else:
                message = json_message
            
            message_id = self.r.xadd(self.stream_key, message)
            return message_id
        except Exception as e:
            return f"Error Sending Message : {str(e)}"
    
    def send_message_data(self, message_data):
        try:
            message_id = self.r.xadd(self.stream_key, {'message': message_data})
            return message_id
        except Exception as e:
            return f"Error Sending Message Data : {str(e)}"
    
    def send_file(self, file_name, file_path=None):
        try:
            message_id = self.r.xadd(self.stream_key, {'file_name': file_name, 'file_path': file_path})
            return message_id
        except Exception as e:
            return f"Error Send File : {str(e)}"
    
    def send_multiple_files(self, file_list, files_path=None):
        try:
            if isinstance(file_list, list):
                file_list_str = ','.join(file_list)
            else:
                file_list_str = str(file_list)
            message_id = self.r.xadd(self.stream_key, {'file_list': file_list_str , 'files_path': files_path})
            #print(f"Message ID: {message_id} -> {file_list_str} -> {files_path}")
            return message_id
        except Exception as e:
            return f"Error Send Multiple Files List : {str(e)}"

    def get_message_by_id(self, message_id):
        try:
            message = self.r.xrange(self.stream_key, min=message_id, max=message_id)
            if message:
                return self.process_message(message[0])
            else:
                return f"No message found with ID: {message_id}"
        except Exception as e:
            return f"Error reading message by ID: {str(e)}"
        
    def claim_message_by_id(self, message_id: str, new_consumer: str, min_idle_time_ms: int = 10000):
        """
        Claim a specific pending message by its ID and assign it to a new consumer.
        
        :param message_id: The ID of the message to claim (e.g., '1685723531577-0')
        :param new_consumer: The name of the consumer that will take over the message
        :param min_idle_time_ms: Minimum idle time in milliseconds (default: 10000 ms = 10s)
        :return: The claimed message(s) or an error string
        """
        try:
            claimed = self.r.xclaim(
                self.stream_key,
                self.group_name,
                new_consumer,
                min_idle_time_ms,
                message_ids=[message_id]
            )
            return claimed  # List of (message_id, {field: value}) tuples
        except Exception as e:
            traceback.print_exc()
            return f"Error claiming message {message_id}: {str(e)}"
            
        


