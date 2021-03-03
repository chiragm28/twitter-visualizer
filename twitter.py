from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import credentials
from pykafka import KafkaClient
import json


def get_kafka_client():
    return KafkaClient(hosts="127.0.0.1:9092")


class StdOutListener(StreamListener):
    def on_data(self, data):
        print(data)
        client = get_kafka_client()
        topic = client.topics["twitterdata1"]
        return True

    def on_error(self, status):
        print(status)


if __name__ == "__main__":
    auth = OAuthHandler(credentials.API_Key, credentials.API_Secret_Key)
    auth.set_access_token(credentials.Access_Token, credentials.Access_Token_Secret)
    listener = StdOutListener()
    stream = Stream(auth, listener)
    stream.filter(track=["codeanddogs"])

