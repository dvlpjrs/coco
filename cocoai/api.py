import json
import openai


class CocoAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key

    def fetch_result(self, question, platform):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": 'your name is coco, Assist users by providing list of valid cli commands based on platform and the question. you response must be in valid json format {"commands" : ["command1", "command2"]}. The output must be loadable by json.loads()',
                    },
                    {
                        "role": "user",
                        "content": f"platform: {platform}\nquestion: {question}",
                    },
                ],
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            answer = response.choices[0].message.content
            print(answer)
            return json.loads(answer)["commands"]
        except openai.error.Timeout as e:
            raise Exception("Please check your internet connection and try again.")
        except (
            openai.error.APIError,
            openai.error.AuthenticationError,
            openai.error.PermissionError,
            openai.error.RateLimitError,
        ) as e:
            raise Exception(
                f"API Error: {e}\n Suggested action: reset your API key using `coco -t`"
            )
        except openai.error.APIConnectionError as e:
            raise Exception("Please check your internet connection and try again.")
        except openai.error.InvalidRequestError as e:
            raise Exception(f"API Error: {e}")
        except Exception as e:
            raise Exception(f"OpenAI: {str(e)}")
