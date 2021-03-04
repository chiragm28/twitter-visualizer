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
        print("works")
        print(data)
        # filter data containing location details
        message = json.loads(data)
        if message["place"] is not None:
            client = get_kafka_client()
            topic = client.topics["twitterdata1"]
            producer = topic.get_sync_producer()
            producer.produce(data.encode("ascii"))
        return True

    def on_error(self, status):
        print(status)


if __name__ == "__main__":
    auth = OAuthHandler(credentials.API_Key, credentials.API_Secret_Key)
    auth.set_access_token(credentials.Access_Token, credentials.Access_Token_Secret)
    listener = StdOutListener()
    stream = Stream(auth, listener)
    stream.filter(locations=[-180, -90, 180, 90])

