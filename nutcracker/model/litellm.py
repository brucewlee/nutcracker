import logging
#
from litellm import completion
#
#
#
class Litellm:
    def __init__(self, **kwargs):
        self.litellm_attributes = kwargs
        self._control_logging()



    def respond(
            self,
            user_prompt
        ) -> None:
        """Respond to a given user_prompt.

        Args:
            task (Task): Task object.

        Raises:
            None

        Returns:
            None
        """

        self.litellm_attributes['messages'] = [{ "content": user_prompt, "role": "user"}]
        response = completion(**self.litellm_attributes)

        return response["choices"][0]["message"]["content"]
   
    

    def _control_logging(
            self,
        ) -> None:
        """Control logging for LiteLLM.

        Args:
            None
        
        Raises:
            None
        
        Returns:
            None
        """

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.CRITICAL)  # This silences all logging below CRITICAL level for LiteLLM
        logging.getLogger('httpx').setLevel(logging.CRITICAL)
        logging.getLogger('LiteLLM').setLevel(logging.CRITICAL)