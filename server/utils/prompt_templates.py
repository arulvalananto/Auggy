class PromptTemplatesGenerator:

    @staticmethod
    def app_and_action_finder():
        template = """You are a JSON formatter. Convert the user input to JSON format. The JSON object should have the following fields:
        app_name: The name of the application if identifiable from the user input and matches one of the listed apps (paddyfield, gretyHR, google calendar).
        action_type: The type of action to be performed if identifiable from the user input.
        If the user input does not follow a recognizable command format or if app_name, project_name, and action_type cannot be identified, set the respective fields to null.
        Question: {query}  
        """
        return template

    def classify_query() -> str:
        template = """You are a text classifier. Your task is to classify the given user input into one of the following categories:
        app: if the user input is related to actions involving applications such as [{apps}]. Here's the list apps and its actions
            - paddyfield: actions - ['add_log', 'update_log', 'delete_log']
            - gretyHR: actions - ['apply_leave', 'delete_leave', 'approve_leave', 'reject_leave']
            - google calendar: actions: ['create_event', 'delete_event', 'update_event']
        query: It should be a company related and langchain question not an action and if the user input is a question related to company policies such as [{policies}] and langchain.
            - Ask about company policies
            - Ask about company culture
            - Ask about company benefits
            - Ask about langchain
        task: if the user input is related to tasks such as [{tasks}]. 
            - Send_email: Generate an email based on the given input and send it to the mentioned person.
            
        other: if the user input does not fit into any of the above categories.
        Output only the category and the reason for the classification. Do not provide any additional context or explanation.
        {format_instructions}
        Question: {query}
        """
        return template

    def funny_reply() -> str:
        template = """You are a comedian. Respond back with a funny joke based on the user input. Ensure the joke is appropriate and inoffensive.
        Example: User input: "Develop an web application with react and nodejs" Joke: "Oops! Looks like my creators forgot to teach me this trick. 🐾"
        Output only the joke. Do not provide any additional context or explanation.
        Question: {query}
        """
        return template

    def task() -> str:
        template = """
        You are a helpful AI assistant. Answer the following questions and obey the following commands as best you can.
        You have access to the following tools:
        email generation: Use this tool to generate an email based on the given input.
        Just answer questions related to these tools. If the user asks you to do something that cannot be executed by these tools just answer saying that you cannot help the user with that action and give a summary of all the tasks you can execute.
        Begin!
        Question: {query}
        """
        return template
