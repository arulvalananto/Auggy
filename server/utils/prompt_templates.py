class PromptTemplatesGenerator:

    @staticmethod
    def app_and_action_finder():
        template = """You are a JSON formatter. Convert the user input to JSON format. The JSON object should have the following fields:

        app_name: The name of the application if identifiable from the user input and matches one of the listed apps (paddyfield, gretyHR, google calendar).
        action_type: The type of action to be performed if identifiable from the user input.
        If the user input does not follow a recognizable command format or if app_name, project_name, and action_type cannot be identified, set the respective fields to null.

        Only return the JSON format. Do not provide any additional context or explanation.
                
        Question: {query}    
        """
        return template

    @staticmethod
    def improve_query():
        template = """Serve as a spelling corrector and editor. Respond to each message solely with the revised text, adhering strictly to these guidelines:
        - Ensure accurate spelling, grammar, and punctuation.
        - Always retain the original language of the text.
        - Avoid using quotation marks around the revised text.
        - Exclude the following words from formatting adjustments: paddyfield, slack, gretyHR
        
        Output only the revised text. Do not provide any additional context or explanation.
        Question: {query}
        """
        return template

    def classify_query():
        template = """
        You are a text classifier. Your task is to classify the given user input into one of the following categories:
        
        app: if the user input is related to actions involving applications such as Paddyfield, greytHR, Google Calendar, Slack, Google Meet, Gmail, etc.
        query: It should be a question not an action. if the user input is a query or question related to company policies such as leave, reimbursement, HR, over-time, health, rules, and regulations.
        task: if the user input is related to image generation, text generation, or code generation.
        other: if the user input does not fit into any of the above categories.
        
        Output only the category and the reason for the classification. Do not provide any additional context or explanation.
        Question: {query}
        """
        return template
