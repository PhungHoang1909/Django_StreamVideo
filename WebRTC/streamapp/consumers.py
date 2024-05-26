import json
from channels.generic.websocket import AsyncWebsocketConsumer # handle websockets async (1 cach khong dong bo)

# Consumer class extends AsyncWebsocketConsumer for handle ...
class ChatConsumer(AsyncWebsocketConsumer):

    # Handle connection (connect is called when Websocket is opened)
    async def connect(self):
        self.room_group_name = 'Test-Room' # Name of group the consumers will join is set to Test-Room

        # Add Websockets connection
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept() # Accept Websockets connection
    
    # Handle disconnection (disconnect is called when Websocket is closed)
    async def disconnect(self, close_code):

        # Remove Websockets connection from the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        print('Disconnected!')
    
    # Message Handler (received is called when Websockets message is received)
    async def receive(self, text_data):

        receive_dict = json.loads(text_data) # The incoming message: text_data is parsed to JSON format: receive_dict

        # message and action are extracted from receive_dict
        message = receive_dict['message']
        action = receive_dict['action']
        
        if(action == 'new-offer') or (action == 'new-answer'):

            # Extract receiver_channel_name from the message
            receiver_channel_name = receive_dict['message']['receiver_channel_name']

            # The message receiver_channel_name is updated to the current channel name
            receive_dict['message']['receiver_channel_name'] = self.channel_name

            await self.channel_layer.send( # The message is sent directly to the receiver's channel using self.channel_layer.send
                receiver_channel_name,
                {
                    'type': 'send.sdp',
                    'receive_dict': receive_dict
                }
            )
            return

        receive_dict['message']['receiver_channel_name'] = self.channel_name

        # Else: the message is broadcast to group 
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send.sdp',
                'receive_dict': receive_dict
            }
        )
    
    # Custom handle for sending SDP
    async def send_sdp(self, event):
        receive_dict = event['receive_dict']

        await self.send(text_data=json.dumps(receive_dict))
        
# The send_sdp method is a custom handler defined to process specific events related to SDP (Session Description Protocol) messages. 
# These messages are crucial for WebRTC signaling, which establishes peer-to-peer connections for streaming video and audio.
        
# SDP messages are used to negotiate the connection details between peer