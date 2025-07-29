from langchain_core.prompts import ChatPromptTemplate

CONTEXT_CLASSIFIER_TEMPLATE = ChatPromptTemplate.from_template("""
    You are a helpful assistant that classifies the context of a conversation.
    Possible context_id values:
    {context_options}
    Your task is to analyze the following conversation and identify which context it belongs to, If the context cannot be identified, return "" in context_id.
    Only output the context_id value.
    Conversation:
    {input}
""")

NO_CONTEXT_INFERENCE_TEMPLATE = ChatPromptTemplate.from_template(
    """     
    You are a smart assistant answering structured data from a conversation. 

    Only output a JSON object with the following fields:
    - llm_response: a natural language reply

    Conversation:
    {input}
    """
)

EMPTY_CONTEXT_TEMPLATE = ChatPromptTemplate.from_template(
    """     
    You are a smart assistant answering structured data from a conversation. 
    The context is: {context_name} — {context_description}

    Only output a JSON object with the following fields:
    - llm_response: a natural language reply asking for missing info or confirming what's provided

    Conversation:
    {input}
    """
)

FULL_EXTRACTOR_TEMPLATE = ChatPromptTemplate.from_template(
    """
        You are a helpful and smart assistant that extracts structured values from a conversation.

        Context:
        The user may:
        - Provide values for required fields.

        Your task is to:
        - Extract the values for the following fields, if mentioned:
        {fields_description}

        - If all fields are provided, summarize the extracted data.

        Output a JSON object containing:
        - Each field mentioned in the conversation with its value (as key-value pairs).

        Return only valid JSON. Do not explain the format.

        Conversation:
        {input}
    """
)

MISSING_CONTEXT_FIELDS_TEMPLATE = ChatPromptTemplate.from_template(
    """
        You are a helpful and smart assistant that extracts structured values from a conversation.

        Context:
        The user may:
        - Ask questions about what the fields mean or what values are expected.

        Your task is to:
        - Ask for the missing fields in a friendly way using natural language:
        {fields_description}

        - If the user asks about the meaning or possible values of any field, answer clearly and concisely.

        Output a JSON object containing:
        - A field `llm_response` containing a natural-language response that:
            - Answers any user questions about required fields (if applicable).
            - Otherwise, asks for the missing fields, if they have possible values, presents the possible values to the user with some description or confirms the extracted values.

        Return only valid JSON. Do not explain the format.

        Conversation:
        {input}
    """
)

CONFIRMATION_TEMPLATE = ChatPromptTemplate.from_template(
    """
        You are a smart assistant that helps to confirm extracted information.

        Here's a summary of the extracted values:
        {fields_summary}

        Your task:
        - Politely ask the user to confirm if the above information is correct.
        - If any field is missing (value is "Not provided"), highlight that and ask the user to provide it.
        - Be concise and friendly.

        Output a JSON object with:
        - llm_response: A natural-language message asking for confirmation or missing values.

        Return only valid JSON. Do not explain the format.

        Conversation:
        {input}
    """
)

CONFIRMATION_CHECK_TEMPLATE = ChatPromptTemplate.from_template(
    """
    You are a smart assistant that checks whether the user confirmed the provided information.

    Task:
    - Analyze the user's latest message.
    - Determine if the user clearly confirmed that the information is correct.
    - If the message shows agreement, confirmation, or acceptance (e.g., "yes", "that's correct", "all good"), return true.

    Output a JSON object with:
    - confirmed: a boolean (true if the user confirmed, false otherwise)

    Return only valid JSON. Do not explain the format.

    Conversation:
    {input}
    """
)

EXECUTED_CONTEXT_TEMPLATE = ChatPromptTemplate.from_template(
    """     
    You are an smart assistant who has just performed a context-related function
    The context is: {context_name} — {context_description}
    
    This is the return from the function: {func_response}

    Only output a JSON object with the following fields:
    - llm_response: a natural language explaining that you have executed the context-related function with the following return data if they exist

    Conversation:
    {input}
    """
)
