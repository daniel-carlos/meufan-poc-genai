from langchain_aws import ChatBedrockConverse
from langchain.chains import RetrievalQA
from langchain_aws.retrievers import AmazonKnowledgeBasesRetriever
from langgraph.prebuilt import create_react_agent

import config

# Configuração do modelo LangChain com Bedrock
llm = ChatBedrockConverse(
    model=config.BEDROCK_MODEL_ID,
    region_name=config.BEDROCK_REGION,
    temperature=float(config.BEDROCK_MODEL_TEMPERATURE),
    max_tokens=int(config.BEDROCK_MODEL_MAX_TOKENS),
)
tools = []

# Configuração do modelo LangChain com Bedrock
if config.BEDROCK_KB_ID is not None:
    # Configuração do retriever com Bedrock
    retriever = AmazonKnowledgeBasesRetriever(
        knowledge_base_id=config.BEDROCK_KB_ID,
        retrieval_config={"vectorSearchConfiguration": {"numberOfResults": int(config.BEDROCK_KB_MAX_RESULTS)}},
    )

    tools.append(retriever.as_tool(name="knowledge_base", description="Knowledge base"))

    # Configuração da chain do LangChain
    qa = RetrievalQA.from_chain_type(
        llm=llm, retriever=retriever, 
        return_source_documents=True,
    )

# Se não houver ID de conhecimento base, usa o modelo LangChain diretamente
# agent = llm if config.BEDROCK_KB_ID is None else qa
agent = create_react_agent(
    llm, 
    tools,
)

def generate_response(prompt: str, history: list) -> dict:
    """Gera uma resposta para o prompt do usuário usando o modelo Bedrock.

    Args:
        prompt (str): O prompt do usuário

    Returns:
        dict: Um dicionário contendo a resposta gerada e métricas de uso
    """
    try:
        # Gera a resposta usando a chain do LangChain
        history_tuples = [
            (message["role"], message["content"])
            for message in history
        ]
        messages = [
            ("system", f"""{config.BEDROCK_AGENT_PROMPT}

            {"SEMPRE que o usuário tiver dúvidas consuma a tool 'knowledge_base' antes de dar uma resposta" if config.BEDROCK_KB_ID is not None else ""}
            NUNCA retorne as tags <thinking> ou <action> na resposta."""),
            *history_tuples,
            ("user", prompt),
        ]
        print(messages)
        invoke_response = agent.invoke(input={ 'messages': messages })
        print(invoke_response)
        last_message = invoke_response['messages'][-1]
        response = last_message.content
        
        # Extrai métricas de uso do último AIMessage
        usage_metadata = last_message.usage_metadata if hasattr(last_message, 'usage_metadata') else {}
        input_tokens = usage_metadata.get('input_tokens', 0)
        output_tokens = usage_metadata.get('output_tokens', 0)
        
        # Retorna resposta e métricas em um dicionário
        return {
            'content': response.strip(),
            'input_tokens': input_tokens,
            'output_tokens': output_tokens
        }
    except Exception as e:
        print(f"Erro ao gerar resposta: {str(e)}")
        return {
            'content': "Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente.",
            'input_tokens': 0,
            'output_tokens': 0
        }
        

def generate_response_stream(prompt: str):
    """Gera uma resposta em formato de stream para o prompt do usuário.

    Args:
        prompt (str): O prompt do usuário

    Yields:
        str: Caracteres da resposta gerada
    """
    try:
        # messages = [
        #     ("system", config.BEDROCK_AGENT_PROMPT),
        #     ("human", prompt),
        # ]
        messages = f""""
            {config.BEDROCK_AGENT_PROMPT}
            ---
            Mensagem do usuário: {prompt}
        """
        print("Gerando resposta em stream...")
        return agent.stream(messages)
    except Exception as e:
        print(f"Erro ao gerar resposta em stream: {str(e)}")
        error_message = "Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente."
        for char in error_message:
            yield char