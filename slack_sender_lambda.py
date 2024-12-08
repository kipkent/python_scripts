import urllib3
import json

http = urllib3.PoolManager()

def lambda_handler(event, context):
    # Parse the incoming CloudWatch Alarm SNS message
    sns_message = json.loads(event['Records'][0]['Sns']['Message'])

    # Extract the fields you want to send to Slack
    alarm_name = sns_message['AlarmName']
    alarm_description = sns_message.get('AlarmDescription', '')
    new_state_value = sns_message['NewStateValue']

    # Check the new_state_value and format the message accordingly
    if new_state_value == "ALARM":
        simplified_message = (
            f"AlarmName: {alarm_name}\n"
            f"AlarmDescription: {alarm_description}\n"
            f"NewStateValue: {new_state_value} :warning:"
        )
    elif new_state_value == "OK":
        simplified_message = (
            f"AlarmName: {alarm_name}\n"
            f"NewStateValue: {new_state_value} :white_check_mark:"
        )
    else:
        # Default message for any other state
        simplified_message = (
            f"AlarmName: {alarm_name}\n"
            f"AlarmDescription: {alarm_description}\n"
            f"NewStateValue: {new_state_value}"
        )

    # Create the payload for Slack
    msg = {
        "channel": "#CHANNEL_NAME",
        "username": "WEBHOOK_USERNAME",
        "text": simplified_message,  # Send the simplified message as plain text
        "icon_emoji": ""  # You can set an emoji here if needed
    }

    # Encode the message to JSON and send it to the Slack webhook
    encoded_msg = json.dumps(msg).encode('utf-8')
    url = "https://hooks.slack.com/services/<token>"
    resp = http.request('POST', url, body=encoded_msg)

    # Log the response and message for debugging
    print({
        "message": simplified_message,  # Log the simplified message
        "status_code": resp.status,
        "response": resp.data
    })
