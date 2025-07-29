"""
API calls for interacting with the BGS chat
"""
import asyncio
import requests
from django.conf import settings
import datetime

DIRECT_LINE_URL = settings.DIRECT_LINE_URL
CONVERSATION_URL = 'https://directline.botframework.com/v3/directline/conversations'

# TOKENs VS SECRETS
# Also includes info on refreshing tokens
# https://learn.microsoft.com/en-us/azure/bot-service/rest-api/bot-framework-rest-direct-line-3-0-authentication?view=azure-bot-service-4.0

# The more useful documentation is here, in the response from Henry James
# https://community.powerplatform.com/forums/thread/details/?threadid=b8912aaa-0e8f-4c34-9f39-00ecd95b65ad

"""
Start the shell with:
1. python manage.py shell 
Commands to run in shell:
1. from bgs_chat.common.api_calls import DirectLineAPI
2. bot = DirectLineAPI()
3. bot.send_message('hello')
4. bot.get_response() (this will return an error message until the agent is published)
5. bot.refresh_token()
"""


class DirectLineAPI(object):
    def __init__(self):
        super().__init__()
        self.headers = {
            "Content-Type": "application/json"
        }
        self.init_conversation()
        self._watermark = None
        self.last_message_sent_timestamp = None
        self.last_message_received_timestamp = None

    def save_token_data(self, json_dl_response):
        self.headers.update(
            {"Authorization": f"Bearer {json_dl_response['token']}"}
        )
        return {
            'token': json_dl_response['token'],
            'expires_in': json_dl_response['expires_in'],
            'recieved_at': datetime.datetime.now(),
            'expires_at': datetime.datetime.now() + datetime.timedelta(seconds=json_dl_response['expires_in'])
        }

    def init_conversation(self):
        """
        Get token and conversation ID.
        This does not start a conversation.
        """
        url = DIRECT_LINE_URL
        dl_response = requests.get(url)
        if dl_response.status_code == 200:
            json_dl_response = dl_response.json()
            self._conversationid = json_dl_response['conversationId']
            self._token_data = self.save_token_data(json_dl_response)
            # initiate the conversation
            conversation_url = CONVERSATION_URL
            # NOTE: we should consider how/if we want to log errors here

            conversation_response = requests.post(conversation_url, headers=self.headers)
            if conversation_response.status_code == 201:
                self._start_conversation()
        else:
            return dl_response.status_code

    def _start_conversation(self):
        """
        Start a conversation using the generated conversationId and token
        """
        if not self._conversationid:
            self.init_conversation()
        payload = {
            "type": "event",
            "name": "startConversation"
        }
        url = '/'.join([CONVERSATION_URL, self._conversationid, 'activities'])
        res = requests.post(url, headers=self.headers, json=payload)
        return res.status_code

    def send_message(self, text):
        """Send a message"""
        url = '/'.join([CONVERSATION_URL, self._conversationid, 'activities'])
        # Can optionally include user/from in payload as 'from': {'id': ...},
        message_payload = {
            "conversationId": self._conversationid,
            "type": "message",
            "text": text
        }
        self.last_message_sent_timestamp = datetime.datetime.now()
        res = requests.post(url, headers=self.headers, json=message_payload)
        print('** MESSAGE SENT **')
        print(f'message sent at {self.last_message_sent_timestamp}')
        if res.status_code == 200:
            return res.json()

    async def poll_for_responses(self):
        url = '/'.join([
            CONVERSATION_URL,
            self._conversationid,
            'activities',
            f'?watermark {self._watermark}' if self._watermark else ''
        ])

        res = requests.get(url, headers=self.headers, json={'conversationId': self._conversationid})
        # we need to set self.last_received_message here
        if res.status_code == 200:
            json_res = res.json()
            self._watermark = int(json_res['watermark'])
            activities = json_res['activities']
            try:
                last_message = next(
                    i for i in reversed(activities)
                    if i['type'] == 'message'
                    and i['from'].get('role') == 'bot'
                    )

                last_message_details = {
                    'status_code': res.status_code,
                    'timestamp': last_message['timestamp'],
                    'text': last_message['text'],
                }
                print('** LAST RECEIVED MESSAGE **')
                print(f'{last_message_details=}')
                # self.last_message_received_timestamp = last_message['timestamp']
                return last_message_details
        # Accounts for the scenario where get_response fires and there are
        # no activities of type=message
        # We return a dict to conform with other response types.
            except StopIteration:
                return {"text": "No response found"}

        return {
            'status_code': res.status_code,
            'text': "Error contacting bot for response"
            }

    def get_response(self):
        """Get message response"""
        async def _run():
            while True: 
                response = await self.poll_for_responses()
                if self.last_message_received_timestamp and self.last_message_sent_timestamp and self.last_message_received_timestamp >= self.last_message_sent_timestamp:
                    return response
                await asyncio.sleep(2)

        try:
            return asyncio.run(_run())
        except RuntimeError:
            # safeguards against running inside an existing event loop
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(_run())

        # get_latest_responses:
        # API call to get message history.
        # while last_message_sent_timestamp < last_message_received_timestamp
        # res = self.poll_for_responses()
        # while self.last_message_received_timestamp < self.last_message_sent_timestamp:
            # wait 2
        # res = self.poll_for_responses()
        # import pdb; pdb.set_trace()
        # while self.last_message_received_timestamp < self.last_message_sent_timestamp:
        #     await asyncio.sleep(2)
        #     res = self.poll_for_responses()


        # From the docs:
        # If the client receives an ActivitySet wherein the watermark property
        # is null or missing, it should ignore that value and not overwrite
        # the prior watermark that it received.

    def refresh_token(self):
        # we don't run token_valid here as the token may be expired before refreshing
        url = 'https://directline.botframework.com/v3/directline/tokens/refresh'
        res = requests.post(url, headers=self.headers, json={'conversationId': self._conversationid})
        if res.status_code == 200:
            json_res = res.json()
            if self._conversationid != json_res['conversationId']:
                return "Error refreshing token, conversation IDs do not match"
            new_token_data = save_token_data(self, json_res)
            self._token_data.update(new_token_data)
            return "Token updated"
        return "Error refreshing token"

    def reconnect_to_conversation(self, conversation_id):
        """
        Reconnect to an existing conversation.
        From the docs:
        The watermark parameter is optional. If the watermark parameter is
        specified in the request URI, the conversation replays from the
        watermark, guaranteeing that no messages are lost. If the watermark
        parameter is omitted from the request URI, only messages received
        after the reconnection request are replayed.
        """
        # refresh the token if it has expired.
        # if not token_valid():
        self.refresh_token()

        url = '/'.join([
                CONVERSATION_URL,
                self._conversationid,
                'activities',
                f'?watermark {self._watermark}' if self._watermark else ''
            ])
        res = requests.get(url, headers=self.headers, json={'conversationId': conversation_id})
        if res.status_code == 200:
            json_res = res.json()
            if self._conversationid != json_res['conversationId']:
                return "Error reconnecting to conversation, conversation IDs do not match"
            self.headers.update({'Authorization': f"Bearer {json_res['token']}"})
            return "Reconnected to conversation"
        return "Error reconnecting to conversation"

    def end_conversation(self):
        """End a current conversation"""
        # we still want to make sure the token is valid so we can't
        # erroneously end conversations
        # if token_valid():
        url = '/'.join([CONVERSATION_URL, self._conversationid, 'activities'])
        payload = {
            "type": "endOfConversation",
            "from": {
                "id": "user1"
            }
        }
        requests.post(url, headers=self.headers, json=payload)
            # this returns a conversation id. We could store this, if we chose to.