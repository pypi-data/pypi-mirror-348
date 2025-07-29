from freezegun import freeze_time
import datetime
# import asyncio
import pytest
# import pytest-asyncio
from ..common.api_calls import DirectLineAPI
# from unittest.mock import patch


@pytest.fixture
def message_bot():
    return DirectLineAPI()


@pytest.fixture
def message_bot_with_message():
    bot = DirectLineAPI()
    bot.send_message('Hello')
    return bot


# test _generate_token() generates token, conversation id, calls start_conversation
def test_get_token_saves_token_data(message_bot):
    # bot = DirectLineAPI()
    message_bot._get_token()
    assert '_conversationid' in message_bot.__dict__.keys()
    assert '_token_data' in message_bot.__dict__.keys()


def test_send_message(message_bot):

    res = message_bot.send_message("hello")
    assert res.status_code == 200


# TODO: combine incorrect_conversation_id and invalid_token
def test_send_message_incorrect_conversation_id():
    """Sending a message with an valid token but invalid conversation id will
    return None"""
    bot = DirectLineAPI()
    bot._conversationid = "1"
    # A bad request to the message API returns a None response
    assert not bot.send_message("hello")


def test_send_message_invalid_token():
    """Sending a message with an invalid token but valid conversation id will
    return None"""
    bot = DirectLineAPI()
    invalid_token_data = {
        'token': 1,
        'expires_in': 2,
    }
    invalid_header_token = {
        "Authorization": "Bearer 1",
    }
    bot._headers.update(invalid_header_token)
    bot._token_data.update(invalid_token_data)
    # A bad request to the message API returns a None response
    assert not bot.send_message("hello")


def test_get_response(message_bot_with_message):
    bot = DirectLineAPI()
    send_res = bot.send_message("Hi")
    response = bot.get_response()
    # assert 0
    while response['text'] == 'Hi':
        response = bot.get_response()

    assert "Hello, I'm BGS AI Agent - Non Production, a virtual assistant." in response['text']


    # print('*'*30, 'fires')
    # # assert 0
    # asyncio.sleep(20)
    # print('*'*30, 'fires again')

    # res = message_bot_with_message.get_response()
    # # This is currently the stock response from the AI chatbot
    # assert "Hello, I'm BGS AI Agent" in res['text']


def test_refresh_token():
    with freeze_time('2025-01-01 01:00:01'):
        bot = DirectLineAPI()
        assert bot._token_data['expires_at'] == datetime.datetime(2025, 1, 1, 2, 0, 1)
        with freeze_time('2025-01-01 01:59:01'):
            bot.refresh_token()
            assert bot._token_data['expires_at'] == datetime.datetime(2025, 1, 1, 2, 59, 1)


# test _start_conversation() returns 201
# test send_message returns 200 response
# test send_message no conversation id returns 200 response
# test send_message no conversation id returns 200 response