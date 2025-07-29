import requests
import bgs_chat_site.settings as settings
import datetime

"""
Start the shell with:
1. python manage.py shell 
Commands to run in shell:
1. from bgs_chat.common.websocket import DirectLineAPI
2. bot = DirectLineAPI()
3. bot._get_token()
4. bot.start_conversation()
Then in any order
5. bot.send_message('hello')
6. bot.get_response()
7. bot.get_all_conversation_activity()
8. bot.get_all_messages()
TODO: listener
TODO: listener to be triggered by start_conversation, should be async/await.
May be easier to implement this in JS? ie. send message, make call to get_response every x seconds
This would only work if the watermark is being used effectively and we only get the latest response back, for the relevant question
"""

TOKEN_URL = settings.DIRECT_LINE_URL
DL_URL = 'https://directline.botframework.com/v3/directline'


def save_token_data(self, json_token_response):
    self.headers = {
            "Authorization": f"Bearer {json_token_response['token']}",
            "Content-Type": "application/json"
        }
    return {
        'token': json_token_response['token'],
        'expires_in': json_token_response['expires_in'],
        'recieved_at': datetime.datetime.now(),
        'expires_at': datetime.datetime.now() + datetime.timedelta(seconds=json_token_response['expires_in'])
    }


class DirectLineAPI(object):
    def __init__(self):
        super().__init__()
        self.headers = {
            "Content-Type": "appication/json"
        }
        # TODO: pull user id from session;
        # Logged in token?
        self.user_id = "user"
        self.conversation_id = None
        self.stream_url = None
        self.bot_responses = []
        self.watermark = None

    def _get_token(self):
        """
        Get token and conversation ID.
        This does not start a conversation.
        """
        url = TOKEN_URL
        token_respone = requests.get(url)
        if token_respone.status_code == 200:
            json_token_response = token_respone.json()
            self.conversation_id = json_token_response['conversationId']
            self.token_data = save_token_data(self, json_token_response)

    def start_conversation(self):
        url = '/'.join([DL_URL, 'conversations'])
        res = requests.post(url, headers=self.headers)

        if res.status_code != 201:
            raise Exception(f"Failed to start a conversation {res.status_code}: {res.text}")

        json_res = res.json()
        self.conversation_id = json_res['conversationId']
        self.stream_url = json_res['streamUrl']
        return {
            "conversation_id": self.conversation_id,
            "stream_url": self.stream_url
        }

    def send_message(self, text: str):
        # TODO: sanitise text
        # prevent XSS attacks
        # limit message length?
        if not self.conversation_id:
            raise ValueError("No conversation id")

        url = '/'.join([DL_URL, 'conversations', self.conversation_id, 'activities'])
        message_payload = {
            "type": "message",
            "from": {"id": self.user_id},
            "text": text
        }
        res = requests.post(url, headers=self.headers, json=message_payload)

        if res.status_code not in [200, 201]:
            raise Exception(f"Failed to send message, {res.status_code}: {res.text}")

        return res.json()

    def get_response(self):
        if not self.conversation_id:
            raise ValueError("Conversation ID")

        # TODO: move this behind another function
        url = '/'.join([DL_URL, 'conversations', self.conversation_id, 'activities', f'?watermark {self.watermark}' if self.watermark else ''])
        json_res = requests.get(url, headers=self.headers).json()

        activities = json_res['activities']
        # bot_responses = next(i for i in activities if i['type'] == 'message' and i['from'].get('role') == 'bot')

        # this needs some thinking about, but roughly
        # while len(bot_responses) < len(self.bot_responses)... or maybe len(sent_messages?):
        #     json_res = requests.get(url, headers=self.headers).json()
        #     activities = json_res['activities']
        #     bot_responses = next(i for i in activities if i['type'] == 'message' and i['from'].get('role') == 'bot')
            # save the latest watermark

        self.watermark = json_res['watermark']
        try:
            last_message = next(
                i for i in reversed(activities)
                if i['type'] == 'message'
                and i['from'].get('role') == 'bot'
            )
            # This will return only bot responses.
            # TODO:
            # save the response to self.bot_responses
            # while len(res.bot_responses) == len(self.bot_responses):
                # rerun get_responses every 2? seconds
                # return
            # append to self.bot_responses
            bot_response = {
                'timestamp': last_message['timestamp'],
                'text': last_message['text'],
            }
            self.bot_responses.append(bot_response)
            return bot_response
        # Accounts for the scenario where get_response fires and there are
        # no activities of type=message
        # We return a dict to conform with other response types.
        except StopIteration:
            return {"text": "No response found"}

    def get_all_conversation_activity(self):
        if not self.conversation_id:
            raise ValueError("Conversation ID")

        url = '/'.join([DL_URL, 'conversations', self.conversation_id, 'activities'])
        res = requests.get(url, headers=self.headers)
        json_res = res.json()

        return json_res

    def get_all_messages(self):
        if not self.conversation_id:
            raise ValueError("Conversation ID")
        messages = []
        url = '/'.join([DL_URL, 'conversations', self.conversation_id, 'activities'])
        res = requests.get(url, headers=self.headers)
        json_res = res.json()
        for activity in json_res.get('activities', []):
            if activity['type'] == 'message':
                messages.append({
                    'message': activity['text'],
                    'from': activity['from']
                })

        return messages

    def end_conversation(self):
        url = '/'.join([DL_URL, 'conversations'])
        data = {
            "type": "endOfConversation",
        }
        res = requests.post(url, headers=self.headers, json=data)
        return res.json()