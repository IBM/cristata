import requests
import argparse


class MessageHubRest(object):
    def __init__(self, rest_endpoint, api_key):
        self.path = '{0}/admin/topics'.format(rest_endpoint)
        self.headers = {
            'X-Auth-Token': api_key,
            'Content-Type': 'application/json'
        }

    def create_topic(self, topic_name, partitions=1, retention_hours=24):
        """
        POST /admin/topics
        """
        payload = {
            'name': topic_name,
            'partitions': partitions,
            'configs': {
                'retentionMs': retention_hours * 60 * 60 * 1000
            }
        }
        return requests.post(self.path, headers=self.headers, json=payload)

    def list_topics(self):
        """
	GET /admin/topics
        """
        return requests.get(self.path, headers=self.headers)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Mhub admin client')
    parser.add_argument('--url', action='store', dest='url', 
                            required=True, help='Kafka admin url')
    parser.add_argument('--api_key', action='store', dest='api_key',
                            required=True, help='api key')
    parser.add_argument('--topic', action='store', dest='topic',
                            required=True, help='topic')
    args = parser.parse_args()

    client = MessageHubRest(args.url, args.api_key)

    print('Creating the topic {0} with Admin REST API'.format(args.topic))
    response = client.create_topic(args.topic, 1, 24)

    response = client.list_topics()
    print(response.text)

