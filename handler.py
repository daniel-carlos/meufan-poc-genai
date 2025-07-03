import json


def get_survey(event, context):
    try:
        # Obter o ID da pesquisa da URL
        survey_id = event.get('pathParameters', {}).get('id')
        
        if not survey_id:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Missing survey ID"
                })
            }
            
        # Aqui você implementaria a lógica para buscar a pesquisa pelo ID
        # Por exemplo, consultar um banco de dados como DynamoDB
        
        # Dados fictícios para exemplo
        survey_data = {
            "id": survey_id,
            "title": "Example Survey",
            "questions": [
                {"id": 1, "text": "What is your name?"},
                {"id": 2, "text": "How did you hear about us?"}
            ]
        }
        
        return {
            "statusCode": 200,
            "body": json.dumps(survey_data)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Error fetching survey",
                "error": str(e)
            })
        }


def list_surveys(event, context):
    try:
        # Aqui você implementaria a lógica para listar todas as pesquisas
        # Por exemplo, consultar um banco de dados como DynamoDB
        
        # Dados fictícios para exemplo
        surveys = [
            {"id": "123", "title": "Músico apaixonado por discos antigos"},
            {"id": "456", "title": "Criador de conteúdo digital e hippie"},
            {"id": "789", "title": "Amante de cachorros"}
        ]
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "surveys": surveys
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Error listing surveys",
                "error": str(e)
            })
        }
