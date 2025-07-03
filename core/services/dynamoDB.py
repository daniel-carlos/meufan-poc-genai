import boto3
import os
from datetime import datetime
from typing import Dict, List, Optional, TypedDict, Union, Literal
from dotenv import load_dotenv

load_dotenv()

# Define Evaluation type
class Evaluation(TypedDict):
    score: int
    feedback: str

# Question item type
class QuestionItem(TypedDict, total=False):
    PK: str  # QUESTION#{string}
    SK: str  # DATE#{string}
    
    DegreeDemand: int
    Topic: str
    Statement: str
    
    CorrectAlternative: str
    IncorrectAlternative: str
    
    Justification: str
    
    CreatedAt: Optional[str]
    UpdatedAt: Optional[str]
    
    FinalFeedback: Optional[str]
    Logic: Optional[Evaluation]
    Clarity: Optional[Evaluation]
    Creativity: Optional[Evaluation]
    Tokens: Optional[Dict[str, int]]

class DynamoDBService:
    def __init__(self):
        self.table_name = f"lista_onboarding-{os.getenv('ENV_NAME')}"
        
        session = boto3.Session(
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            aws_session_token=os.getenv('AWS_SESSION_TOKEN'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
        
        self.dynamodb = session.resource('dynamodb')
        self.table = self.dynamodb.Table(self.table_name)
    
    # Create
    def create_question(self, item: QuestionItem) -> QuestionItem:
        """Create a new question in DynamoDB"""
        self.table.put_item(Item=item)
        return item
    
    # Read
    def get_question(self, question_id: str, date: str) -> Optional[QuestionItem]:
        """Retrieve a question by ID and date"""
        pk = f"QUESTION#{question_id}"
        sk = f"DATE#{date}"
        
        response = self.table.get_item(
            Key={
                'PK': pk,
                'SK': sk
            }
        )
        
        return response.get('Item')
    
    # Query (Get all versions by question ID)
    def query_questions_by_id(self, question_id: str) -> List[QuestionItem]:
        """Query all versions of a question by its ID"""
        pk = f"QUESTION#{question_id}"
        
        response = self.table.query(
            KeyConditionExpression='PK = :pk',
            ExpressionAttributeValues={
                ':pk': pk
            }
        )
        
        return response.get('Items', [])
    
    # Update
    def update_question(self, question_id: str, date: str, updates: Dict) -> QuestionItem:
        """Update a question with new values"""
        pk = f"QUESTION#{question_id}"
        sk = f"DATE#{date}"
        
        update_expression_parts = []
        expression_attribute_names = {}
        expression_attribute_values = {}
        
        for key, value in updates.items():
            attr_name = f"#{key}"
            attr_value = f":{key}"
            update_expression_parts.append(f"{attr_name} = {attr_value}")
            expression_attribute_names[attr_name] = key
            expression_attribute_values[attr_value] = value
        
        update_expression = "SET " + ", ".join(update_expression_parts)
        
        response = self.table.update_item(
            Key={
                'PK': pk,
                'SK': sk
            },
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW"
        )
        
        return response.get('Attributes', {})
    
    # Delete
    def delete_question(self, question_id: str, date: str) -> Dict[str, str]:
        """Delete a question by ID and date"""
        pk = f"QUESTION#{question_id}"
        sk = f"DATE#{date}"
        
        self.table.delete_item(
            Key={
                'PK': pk,
                'SK': sk
            }
        )
        
        return {"message": "Question deleted"}