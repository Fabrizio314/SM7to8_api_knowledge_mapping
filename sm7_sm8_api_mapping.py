# import faiss
# from langchain_core.documents import Document
# from langchain_community.docstore.in_memory import InMemoryDocstore
# from langchain_community.vectorstores import FAISS
# from langchain_core.documents import Document
# from langchain_huggingface.embeddings import HuggingFaceEmbeddings
import requests, json
from dotenv import load_dotenv
import os

load_dotenv()


def intent_generator(code):

        # Prepare the prompt
        prompt = f"""
        Analyze the following C++ or java source code and write a very very short intent of what it does.

        Be thorough, professional, and clear.

        C++ or java Source Code:
        {code}
        """

        # Build the request payload for a chat-based model (like Mistral or Falcon via OpenRouter)
        data = {
            "model": "mistralai/mixtral-8x7b-instruct",  # or another model available on OpenRouter
            "messages": [
                {"role": "system", "content": "You are a helpful expert software analyst."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1024,
            "temperature": 0.2
        }

        headers = {
            "Authorization": f"Bearer {os.environ['API_KEY']}",
            "Content-Type": "application/json"
        }

        response = requests.post('https://openrouter.ai/api/v1/chat/completions', json=data, headers=headers)

        if response.status_code == 200:
            result = response.json()
            # Extract generated text from the response structure
            description = result["choices"][0]["message"]["content"]
            return(description)
        else:
            return(f"Error: {response.status_code} - {response.text}")

def create_api_mapping(code_snippets):
     
     # Prepare the prompt
        prompt = f"""
        Analyze the following C++ source code , understand and capture the intent and exact behaviour of the C++ code and 
        output a set of Java method(s) that correspond to the same intent and mimic the same behaviour of the C++ code , 
        along with their logical relationship among the methods(e.g., AND, OR, sequence) and mapping between C++ and Java methods (e.g., 1:1, 1:many, many:many).

        C++ Source Code:
        {code_snippets}

        Output the result in a JSON format with the following structure:
        {{
            "java_methods": [
                {{
                    "method_name": "string",
                    "code_snippet": "string",
                    "description": "string",
                    "relationship": "string",  # e.g., AND, OR, sequence
                    "mapping": "string"  # e.g., 1:1, 1:many, many:many
                }}
            ]
        }}
        """
        api_key = os.environ["API_KEY"]
        response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "qwen/qwen-2.5-coder-32b-instruct",
            "messages": [
                {"role": "system", "content": "You are a helpful expert software analyst."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens":1024,
            "temperature": 0.2,
            
        })
        )
        return response.json()

if __name__ == "__main__":
    code_snippets = """
#include <iostream>
void printMessage() {
std::cout << "Hello, World!" << std::endl;
}
    """
    result = create_api_mapping(code_snippets)
    print(result)