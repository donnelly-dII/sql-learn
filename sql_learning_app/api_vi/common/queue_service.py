#
# An abstract Service class for sending messages to a Queue
#
from typing import Union


class QueueService:
    def __init__(self, name: str):
        """Constructor for a Queue Service that can direct messages to different messaging queues
        :param name: Name of messaging queue to direct your message
        """
        self.queue_destination = name

    def enqueue(self, msg: str, user: Union[str, int]):
        """Sends the message to the destination queue
        :param msg: Message to send to the Queue
        :param user: username or ID for user getting getting a message
        """
        print(f'Queue Destination: {self.queue_destination} Sucessfully Recieved Message: "{msg} for User {str(user)}')
