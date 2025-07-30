from openai import OpenAI
from jvcore import getConfig

class OpenAIConversation():
    def __init__(self) -> None:
        self.__config = getConfig().get('tools.openai')
        self.__client = OpenAI(api_key=self.__config['accessKey'])
        self.__messages = []
    
    def getResponse(self, request: str) -> str:
        result = self.__getCompletion(request)
        return result.choices[0].message.content

    def __getCompletion(self, content: str):
        self.__messages = [*self.__messages, 
            {
                "role": "user",
                "content": content
            }
        ]
        return self.__client.chat.completions.create(
            model=self.__config['model'], 
            messages= self.__messages
        )
