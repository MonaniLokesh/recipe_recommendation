from langchain.chains import LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq

def get_recipe_suggestions(ingredients, groq_api_key):
    """
    Given a list of ingredients, get recipe suggestions from the Groq model.
    """
    groq_chat = ChatGroq(groq_api_key=groq_api_key, model_name="llama3-8b-8192")
    
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content="You are a helpful cooking assistant."),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{human_input}"),
        ]
    )
    
    conversation = LLMChain(
        llm=groq_chat,
        prompt=prompt,
        verbose=True,
        memory=ConversationBufferWindowMemory(k=5, memory_key="chat_history", return_messages=True),
    )
    
    query = f"""
    You have the following ingredients: {', '.join(ingredients)}.
    Suggest some recipes that can be made just using these ingredients.
    Ensure the suggestions strictly use the listed ingredients.
    """
    
    return conversation.predict(human_input=query)
