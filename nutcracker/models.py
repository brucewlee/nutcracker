import numpy as np
from openai import OpenAI
from anthropic import AnthropicBedrock
import cohere
import boto3
import botocore
import os, sys, json
from collections import Counter



class OpenAI_ChatGPT():
    def __init__(self, api_key, max_retries = 5):
        self.model = "gpt-3.5-turbo-0125"
        self.client_openai = OpenAI(
            api_key=api_key,
        )
        self.max_retries = max_retries

    def respond(self, user_prompt):
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                completion = self.client_openai.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": f"{user_prompt}"}
                    ]
                )
                response = completion.choices[0].message.content
                return response
            except KeyboardInterrupt:
                sys.exit()
            except Exception as error:
                print(f"Error: {error}. Retrying...")
                retry_count += 1
        
        raise Exception("Max retries exceeded. Failed to get a response.")



class OpenAI_ChatGPT4():
    def __init__(self, api_key, max_retries = 5):
        self.model = "gpt-4-turbo-2024-04-09"
        self.client_openai = OpenAI(
            api_key=api_key,
        )
        self.max_retries = max_retries

    def respond(self, user_prompt):
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                completion = self.client_openai.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": f"{user_prompt}"}
                    ]
                )
                response = completion.choices[0].message.content
                return response
            except KeyboardInterrupt:
                sys.exit()
            except Exception as error:
                print(f"Error: {error}. Retrying...")
                retry_count += 1
        
        raise Exception("Max retries exceeded. Failed to get a response.")



class OpenAI_ChatGPT4o():
    def __init__(self, api_key, max_retries = 5):
        self.model = "gpt-4o-2024-05-13"
        self.client_openai = OpenAI(
            api_key=api_key,
        )
        self.max_retries = max_retries

    def respond(self, user_prompt):
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                completion = self.client_openai.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": f"{user_prompt}"}
                    ]
                )
                response = completion.choices[0].message.content
                return response
            except KeyboardInterrupt:
                sys.exit()
            except Exception as error:
                print(f"Error: {error}. Retrying...")
                retry_count += 1
        
        raise Exception("Max retries exceeded. Failed to get a response.")



class Bedrock_Claude3_Opus():
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name, max_retries = 5):
        self.model = "anthropic.claude-3-opus-20240229-v1:0"
        self.client_anthropic = AnthropicBedrock(
            aws_access_key=os.environ['AWS_ACCESS_KEY'],
            aws_secret_key=os.environ['AWS_SECRET_KEY'],
            aws_region="us-west-2",
        )
        self.max_retries = max_retries

    def respond(self, user_prompt):
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                completion = self.client_anthropic.messages.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": f"{user_prompt}"}
                    ],
                    max_tokens=1024,
                )
                response = completion.content[0].text
                return response
            except KeyboardInterrupt:
                sys.exit()
            except Exception as error:
                print(f"Error: {error}. Retrying...")
                retry_count += 1
        
        raise Exception("Max retries exceeded. Failed to get a response.")



class Bedrock_Claude3_Sonnet():
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name, max_retries = 5):
        self.model = "anthropic.claude-3-sonnet-20240229-v1:0"
        self.client_anthropic = AnthropicBedrock(
            aws_access_key=os.environ['AWS_ACCESS_KEY'],
            aws_secret_key=os.environ['AWS_SECRET_KEY'],
            aws_region="us-east-1",
        )
        self.max_retries = max_retries

    def respond(self, user_prompt):
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                completion = self.client_anthropic.messages.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": f"{user_prompt}"}
                    ],
                    max_tokens=1024,
                )
                response = completion.content[0].text
                return response
            except KeyboardInterrupt:
                sys.exit()
            except Exception as error:
                print(f"Error: {error}. Retrying...")
                retry_count += 1
        
        raise Exception("Max retries exceeded. Failed to get a response.")



class Bedrock_Claude3_Haiku():
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name, max_retries = 5):
        self.model = "anthropic.claude-3-haiku-20240307-v1:0"
        self.client_anthropic = AnthropicBedrock(
            aws_access_key=os.environ['AWS_ACCESS_KEY'],
            aws_secret_key=os.environ['AWS_SECRET_KEY'],
            aws_region="us-east-1",
        )
        self.max_retries = max_retries

    def respond(self, user_prompt):
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                completion = self.client_anthropic.messages.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": f"{user_prompt}"}
                    ],
                    max_tokens=1024,
                )
                response = completion.content[0].text
                return response
            except KeyboardInterrupt:
                sys.exit()
            except Exception as error:
                print(f"Error: {error}. Retrying...")
                retry_count += 1
        
        raise Exception("Max retries exceeded. Failed to get a response.")



class Cohere_CommandRPlus():
    def __init__(self, api_key, max_retries = 5):
        self.model = "command-r-plus"
        self.client_cohere = cohere.Client(
            api_key=api_key
        )
        self.max_retries = max_retries

    def respond(self, user_prompt):
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                completion = self.client_cohere.chat(
                    model=self.model,
                    message=f"{user_prompt}"
                )
                response = completion.text
                return response
            except KeyboardInterrupt:
                sys.exit()
            except Exception as error:
                print(f"Error: {error}. Retrying...")
                retry_count += 1
        
        raise Exception("Max retries exceeded. Failed to get a response.")



class Bedrock_LLaMA3_70B_Inst():
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name, max_retries = 5):
        self.model = "meta.llama3-70b-instruct-v1:0"
        self.client_bedrock = boto3.client(
            'bedrock-runtime',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )
        self.max_retries = max_retries

    def respond(self, user_prompt):
        prompt = self._format_prompt(user_prompt)
        body = {
                "prompt": prompt,
                "max_gen_len": 1024,
            }
        
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                results = self.client_bedrock.invoke_model(
                    modelId=self.model,
                    body=json.dumps(body)
                )
                response_body = json.loads(results["body"].read())
                response = response_body["generation"]
                return response
            except KeyboardInterrupt:
                sys.exit()
            except Exception as error:
                print(f"Error: {error}. Retrying...")
                retry_count += 1
        
        raise Exception("Max retries exceeded. Failed to get a response.")
    
    def _format_prompt(self, user_prompt):
        prompt = "<|begin_of_text|>"
        prompt += "<|start_header_id|>user<|end_header_id|>\n\n"
        prompt += f"{user_prompt}<|eot_id|>"
        prompt += "<|start_header_id|>assistant<|end_header_id|>"
        return prompt


class Bedrock_LLaMA3_8B_Inst():
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name, max_retries = 5):
        self.model = "meta.llama3-8b-instruct-v1:0"
        self.client_bedrock = boto3.client(
            'bedrock-runtime',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )
        self.max_retries = max_retries

    def respond(self, user_prompt):
        prompt = self._format_prompt(user_prompt)
        body = {
                "prompt": prompt,
                "max_gen_len": 1024,
            }
        
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                results = self.client_bedrock.invoke_model(
                    modelId=self.model,
                    body=json.dumps(body)
                )
                response_body = json.loads(results["body"].read())
                response = response_body["generation"]
                return response
            except KeyboardInterrupt:
                sys.exit()
            except Exception as error:
                print(f"Error: {error}. Retrying...")
                retry_count += 1
        
        raise Exception("Max retries exceeded. Failed to get a response.")
    
    def _format_prompt(self, user_prompt):
        prompt = "<|begin_of_text|>"
        prompt += "<|start_header_id|>user<|end_header_id|>\n\n"
        prompt += f"{user_prompt}<|eot_id|>"
        prompt += "<|start_header_id|>assistant<|end_header_id|>"
        return prompt