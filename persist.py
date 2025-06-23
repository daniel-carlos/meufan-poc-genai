import boto3
from datetime import datetime
import config

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(config.DYNAMODB_TABLE)

def save_chat(user_id: str, chat_id: str):
    print(f'Salvando chat {chat_id} do usuário {user_id}')
    date_now = datetime.now().isoformat()
    table.put_item(
        Item={
            'PK': f'CHAT#{chat_id}',
            'SK': 'DETAILS',
            'USER_ID': f'USER#{user_id}',
            'CREATED_AT': date_now,
            'UPDATED_AT': date_now,
        }
    )

    table.put_item(
        Item={
            'PK': f'USER#{user_id}',
            'SK': f'CHAT#{chat_id}',
            'CREATED_AT': date_now,
            'UPDATED_AT': date_now,
        }
    )

def save_message(chat_id: str, message_id: str, role: str, content: str, input_tokens: int, output_tokens: int):
    print(f'Salvando mensagem {message_id} do chat {chat_id}')
    date_now = datetime.now().isoformat()
    table.put_item(
        Item={
            'PK': f'CHAT#{chat_id}',
            'SK': f'MESSAGE#{message_id}',
            'ROLE': role.upper(),
            'CONTENT': content,
            'INPUT_TOKENS': input_tokens,
            'OUTPUT_TOKENS': output_tokens,
            'CREATED_AT': date_now,
            'UPDATED_AT': date_now,
        }
    )

def save_feedback(chat_id: str, message_id: str, feedback: int):
    date_now = datetime.now().isoformat()
    feedback_value = 'POSITIVE' if feedback else 'NEGATIVE'
    print(f'Salvando feedback {feedback_value} para mensagem {message_id} do chat {chat_id}')
    table.update_item(
        Key={
            'PK': f'CHAT#{chat_id}',
            'SK': f'MESSAGE#{message_id}'
        },
        UpdateExpression='SET FEEDBACK = :feedback, UPDATED_AT = :updated_at',
        ExpressionAttributeValues={
            ':feedback': feedback_value,
            ':updated_at': date_now
        }
    )
    table.put_item(
        Item={
            'PK': f'FEEDBACK#{feedback_value.upper()}',
            'SK': f'CHAT#{chat_id}#MESSAGE#{message_id}',
            'CREATED_AT': date_now,
        }
    )