"""
GPT Tools Module
This module contains AI/ML tools for processing chat messages
"""


import os
import openai
from openai import OpenAIError
import json
import ast
import re
import time
import logging
from datetime import datetime
import traceback
import requests


from Monolithic.constants.constants import *


def print_statement(*args):
    print(datetime.now(),args)
    
def get_gpt_list(code):
    gpt35_16k_list = [OPENAI_ENGINE_NAME_GPT3_5_16K_V3, OPENAI_ENGINE_NAME_GPT3_5_16K, OPENAI_ENGINE_NAME_GPT3_5_16K_V2]
    gpt4_32k_list = [OPENAI_ENGINE_NAME_GPT4_32K_V3, OPENAI_ENGINE_NAME_GPT4_32K, OPENAI_ENGINE_NAME_GPT4_32K_V2]
    gpt4o_12k_list = [OPENAI_ENGINE_NAME_GPT4O_12K]
    gpt4_VE_32k_list = [OPENAI_ENGINE_NAME_GPT_VECT_EMBED]
    gpt4o_50k_LIST = [OPENAI_ENGINE_NAME_GPT4o_50k]
    if code == GPT_35_16K:
        return gpt35_16k_list
    if code == GPT_4_32K:
        return gpt4_32k_list
    if code == GPT_4O_12K:
        return gpt4o_12k_list
    if code == GPT_VECT_EMBED:
        return gpt4_VE_32k_list
    if code == GPT_4o_50k:
        return gpt4o_50k_LIST

def init_openai_params(engine_name):
    if(engine_name == OPENAI_ENGINE_NAME_GPT3_5_16K):
        openai.api_type = "azure"
        openai.api_base = "https://cloobot-openai-v2.openai.azure.com/"
        openai.api_version = "2023-07-01-preview"
        openai.api_key = "e70f6b6a54b44af794c2835f3d50c35d"
    elif(engine_name == OPENAI_ENGINE_NAME_GPT4_32K):
        openai.api_type = "azure"
        openai.api_base = "https://cloobot-gpt-australia-east.openai.azure.com/"
        openai.api_version = "2023-07-01-preview"
        openai.api_key = "d55fe2ccb78c4a8d88fb2f2d9ef05b1d"
    elif(engine_name == OPENAI_ENGINE_NAME_GPT4_32K_V2):
        openai.api_type = "azure"
        openai.api_base = "https://cloobot-openai-switznorth.openai.azure.com/"
        openai.api_version = "2023-07-01-preview"
        openai.api_key = "21f3be2548614a7f986f1f38a0942a11"
    elif(engine_name == OPENAI_ENGINE_NAME_GPT3_5_16K_V2):
        openai.api_type = "azure"
        openai.api_base = "https://cloobot-openai-switznorth.openai.azure.com/"
        openai.api_version = "2023-07-01-preview"
        openai.api_key = "21f3be2548614a7f986f1f38a0942a11"
    elif(engine_name == OPENAI_ENGINE_NAME_GPT4_32K_V3):
        # print("\n\nOPENAI_ENGINE_NAME_GPT4_32K_V3")
        openai.api_type = "azure"
        openai.api_base = "https://cloobot-openai-canadaeast.openai.azure.com/"
        # openai.api_version = "2023-07-01-preview"
        openai.api_version = "2024-08-01-preview"
        openai.api_key = "e074eb0376044e918e5597ea0809f807"
    elif(engine_name == OPENAI_ENGINE_NAME_GPT3_5_16K_V3):
        openai.api_type = "azure"
        openai.api_base = "https://cloobot-openai-canadaeast.openai.azure.com/"
        openai.api_version = "2023-07-01-preview"
        openai.api_key = "e074eb0376044e918e5597ea0809f807"
    elif(engine_name == OPENAI_ENGINE_NAME_GPT4O_12K):
        openai.api_type = "azure"
        openai.api_base = "https://cloobot-openai-vector-embedding-east-us.openai.azure.com/"
        openai.api_version = "2023-07-01-preview"
        openai.api_key = "1314143312bd46c38d5c48aaaf200b4f"
    elif(engine_name == OPENAI_ENGINE_NAME_GPT_VECT_EMBED): #for vector embedding test
        openai.api_type = "azure"
        openai.api_base = "https://cloobot-openai-vector-embedding-east-us.openai.azure.com/"
        openai.api_version = "2023-07-01-preview"
        openai.api_key = "1314143312bd46c38d5c48aaaf200b4f"
    elif(engine_name == OPENAI_ENGINE_NAME_GPT4o_50k): #for vector embedding test
        openai.api_type = "azure"
        openai.api_base = "https://idsgpt4o.openai.azure.com/"
        openai.api_version = "2024-08-01-preview"
        openai.api_key = "22e36c76c51c451c95eaa87c48754947"
    else:
        pass

def extract_json_obj_from_string(text_with_json):
    # print_statement('ejofs:r1:',text_with_json)
    json_obj_str = ""
    re_str = '\{.*\}'
    stats_re = re.compile(re_str, re.MULTILINE | re.DOTALL)

    for match in stats_re.findall(text_with_json):
        # print_statement(match)
        json_obj_str = match
        # print_statement('ejofs:r2:',match)
        break
    
    return json_obj_str


def extract_json_obj_list_from_string(text_with_json):
    # print_statement('ejofs:r1:',text_with_json)
    json_obj_str = ""
    re_str = '\[.*\]'
    stats_re = re.compile(re_str, re.MULTILINE | re.DOTALL)
    for match in stats_re.findall(text_with_json):
        # print_statement(match)
        json_obj_str = match
        # print_statement('ejofs:r2:',match)
        break
    return json_obj_str



def get_gpt_response(code,messages,max_tokens=10000):
    # max_tokens = 4000
    gptl = get_gpt_list(code)
    # print("ggr::gptl :: 1 ::",gptl)
    for tryindex in range(len(gptl)):
        try:
            # print_statement('ggrf:r1::',tryindex,'::',json.dumps(messages,indent=4), "::",gptl[tryindex])
            
            init_openai_params(gptl[tryindex])
            response = openai.ChatCompletion.create(
                        engine=gptl[tryindex],
                        messages = messages,
                        temperature=0.7,
                        max_tokens=max_tokens,
                        top_p=0.95,
                        frequency_penalty=0,
                        presence_penalty=0,
                        request_timeout=600, 
                    stop=None)
            
            print_statement('ggrf:r2:',response)
            
            input_tokens = response["usage"]["prompt_tokens"]
            output_tokens = response["usage"]["completion_tokens"]
            
            for c in response.choices:
                uc_string = c.message.content
                # print_statement('ggrf:r3',c.message.content)
                break
        
            # print_statement("ggr::",uc_string)
            return True, uc_string, input_tokens, output_tokens, gptl[tryindex]
        except openai.error.RateLimitError:
            print_statement(':e1:RateLimitError::',tryindex)
        except openai.error.Timeout:
            print_statement(':e2:Timeout::',tryindex)
        except Exception as e:
            print_statement(':e3:Openai error::',tryindex,'::',e)

    return False, "", 0, 0 , ""




def process_gpt_response(gpt_code, messages, jsontype, getmsg=False, max_tokens=10000):
    input_tokens = 0
    output_tokens = 0
    status = False
    for tryindex in range(5):
        try:
            status, uc_string, input_tokens, output_tokens, gpttype = get_gpt_response(gpt_code, messages, max_tokens)

            # print_statement('ggrf:r2:',uc_string)
            op = None
            if jsontype == JSON_OBJ:
                op = json.loads(extract_json_obj_from_string(uc_string.strip().replace("\n","").replace("\\'","'")))
            elif jsontype == JSON_LIST:
                op = json.loads(extract_json_obj_list_from_string(uc_string.strip().replace("\n","").replace("\\'","'")))
            else:
                op = uc_string
            
            if status:
                if getmsg:
                    messages.append({"role":"assistant","content":uc_string})
                    return op, input_tokens, output_tokens, gpttype, messages
                else:
                    return op, input_tokens, output_tokens, gpttype
            else:
                time.sleep(10)
        except json.decoder.JSONDecodeError:
            print_statement(':e2:JSONDecodeError:',tryindex)
            
            if tryindex > 0:
                del messages[-2]
                del messages[-1]
                
            messages.append({"role":"assistant","content":str(uc_string)})
            if not uc_string:
                messages.append({"role":"user","content":"Response can't be empty. Please provide response in given format."})
            else:
                if jsontype == JSON_OBJ:
                    messages.append({"role":"user","content":"Not able to decode this response as JSON object. Please fix and respond."})
                if jsontype == JSON_LIST:
                    messages.append({"role":"user","content":"Not able to decode this response as JSON Array. Please fix and respond."})
            
    if getmsg:                
        if jsontype == JSON_OBJ:
            return {}, 0, 0, "", []
        elif jsontype == JSON_LIST:
            return [], 0, 0, "", []
        else:
            return "", 0, 0, "", []
    else:
        if jsontype == JSON_OBJ:
            return {}, 0, 0, ""
        elif jsontype == JSON_LIST:
            return [], 0, 0, ""
        else:
            return "", 0, 0, ""

def process_message(session_id, message_text):
    """
    Process chat message using AI/ML tools
    This is a placeholder function that will be implemented later
    
    Args:
        session_id (int): The chat session ID
        message_text (str): The message text to process
    
    Returns:
        str: The processed response message
    """
    # Placeholder implementation
    # TODO: Implement actual AI/ML processing logic
    return f"Processed response for: {message_text}"

