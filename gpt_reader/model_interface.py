from typing import List
import openai


class ModelInterface(object):

    def __init__(self) -> None:
        pass

    def send_msg(self, *args):
        pass


class OpenAIModel(object):

    def __init__(self, api_key, model='gpt-3.5-turbo', temperature=0.2) -> None:
        openai.api_key = api_key
        self.model = model
        self.temperature = temperature

    def send_msg(self, msg: List[dict], return_raw_text=True):
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=msg,
            temperature=self.temperature
        )

        if return_raw_text:
            return response["choices"][0]["message"]["content"]
        else:
            return response
