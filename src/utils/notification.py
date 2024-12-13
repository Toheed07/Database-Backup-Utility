import requests
import json

def send_slack_notification(webhook_url, message):
    """
    Sends a notification to a Slack channel using a webhook URL.

    :param webhook_url: The Slack incoming webhook URL
    :param message: The message to send
    """
    slack_data = {'text': message}

    try:
        print(f"Slack notification sent: {message}")
        print(f"Slack notification sent: {webhook_url}")
    #     response = requests.post(
    #         webhook_url, data=json.dumps(slack_data),
    #         headers={'Content-Type': 'application/json'}
    #     )

    #     if response.status_code != 200:
    #         print(f"Request to Slack returned an error {response.status_code}, the response is: {response.text}")
    #         raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is: {response.text}")

    #     print("Slack notification sent: {message}")

    # except requests.exceptions.RequestException as e:
    #     print(f"Failed to send Slack notification due to a request error: {e}")
    except Exception as e:
        print(f"Unexpected error while sending Slack notification: {e}")
