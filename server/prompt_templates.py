class PromptTemplatesGenerator:

    @staticmethod
    def app_and_action_finder():
        template = """You are a JSON formatter. Convert the user input to JSON format. The JSON object should have the following fields:

        app_name: The name of the application if identifiable from the user input and matches one of the listed apps (paddyfield, gretyHR, google calendar).
        action_type: The type of action to be performed if identifiable from the user input.
        If the user input does not follow a recognizable command format or if app_name, project_name, and action_type cannot be identified, set the respective fields to null.

        Only return the JSON format. Do not provide any additional context or explanation.
        
        Question: {question}    
        """
        return template

    @staticmethod
    def improve_query():
        template = """Act as a spelling corrector and improver. Reply to each message only with the rewritten text

        Strictly follow these rules:
        - Correct spelling, grammar and punctuation
        - ALWAYS detect and maintain the original language of the text
        - NEVER surround the rewritten text with quotes

        Question: {question}
        """
        return template
