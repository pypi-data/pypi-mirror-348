from fast_mcp.structures.context import Context, Requirement
from fast_mcp.structures.taggers import create_dynamic_output_model, create_dynamic_output_model_without_response, ContextConfirmation
from fast_mcp.ai.provider import create_model as instantiate_model
from fast_mcp.structures.llm_config import OpenAIModelConfig
from fast_mcp.constants.classifiers import NO_CONTEXT_INFERENCE_TEMPLATE, EMPTY_CONTEXT_TEMPLATE, FULL_EXTRACTOR_TEMPLATE, MISSING_CONTEXT_FIELDS_TEMPLATE, CONFIRMATION_TEMPLATE, CONFIRMATION_CHECK_TEMPLATE, EXECUTED_CONTEXT_TEMPLATE
from fast_mcp.chat import Chat
from typing import List

def no_context_inference(model_config: OpenAIModelConfig, chat: Chat) -> str:
    """
    Inference function for the no context.
    """
    model = instantiate_model(model_config).with_structured_output(create_dynamic_output_model([]))
    overhead_text = "\n".join(m.content for m in NO_CONTEXT_INFERENCE_TEMPLATE.format_messages(input=""))
    conversation = chat.format_and_truncate_conversation(overhead_text)
    formatted_prompt = NO_CONTEXT_INFERENCE_TEMPLATE.format_messages(
        input=conversation,
    )
    result = model.invoke(formatted_prompt)
    return result.llm_response

def empty_context_inference(model_config: OpenAIModelConfig, chat: Chat, context: Context) -> str:
    """
    Inference function for the empty context.
    """
    model = instantiate_model(model_config).with_structured_output(create_dynamic_output_model([]))
    overhead_text = "\n".join(m.content for m in EMPTY_CONTEXT_TEMPLATE.format_messages(input="", context_name=context.id, context_description=context.description))
    conversation = chat.format_and_truncate_conversation(overhead_text)
    formatted_prompt = EMPTY_CONTEXT_TEMPLATE.format_messages(
        input=conversation,
        context_name=context.id,
        context_description=context.description
    )
    result = model.invoke(formatted_prompt)
    return result.llm_response

def ask_for_missing_fields(model_config: OpenAIModelConfig, chat: Chat, requirements: List[Requirement]) -> str:
    """
    Inference function for asking for missing fields.
    """
    model = instantiate_model(model_config).with_structured_output(create_dynamic_output_model([]))
    fields_description = "\n".join([
        f"- {req.id}: {req.description}" + (
            "\n  Possible values:\n" +
            "\n".join([f"  - {pv.id}: {pv.description}" for pv in req.possible_values])
            if req.possible_values else ""
        )
        for req in requirements
    ])
    overhead_text = "\n".join(m.content for m in MISSING_CONTEXT_FIELDS_TEMPLATE.format_messages(input="", fields_description=fields_description))
    conversation = chat.format_and_truncate_conversation(overhead_text)
    formatted_prompt = MISSING_CONTEXT_FIELDS_TEMPLATE.format_messages(
        input=conversation,
        fields_description=fields_description
    )
    result = model.invoke(formatted_prompt)
    return result.llm_response

def generate_confirmation_message(model_config: OpenAIModelConfig, chat: Chat, context: Context) -> str:
    model = instantiate_model(model_config).with_structured_output(create_dynamic_output_model([]))
    extracted_values = chat.memory.fields.get(context.id, {})
    fields_summary = "\n".join([
        f"- {req.id}: {extracted_values.get(req.id, 'Not provided')}"
        for req in context.requirements
    ])
    overhead_text = "\n".join(m.content for m in CONFIRMATION_TEMPLATE.format_messages(input="", fields_summary=fields_summary))
    conversation = chat.format_and_truncate_conversation(overhead_text)
    formatted_prompt = CONFIRMATION_TEMPLATE.format_messages(
        input=conversation,
        fields_summary=fields_summary
    )
    result = model.invoke(formatted_prompt)
    return result.llm_response

def generate_post_execution_message(model_config: OpenAIModelConfig, chat: Chat, context: Context, func_response) -> str:
    model = instantiate_model(model_config).with_structured_output(create_dynamic_output_model([]))
    overhead_text = "\n".join(m.content for m in EXECUTED_CONTEXT_TEMPLATE.format_messages(input="", context_name=context.id, context_description=context.description, func_response=func_response))
    conversation = chat.format_and_truncate_conversation(overhead_text)
    formatted_prompt = EXECUTED_CONTEXT_TEMPLATE.format_messages(
        input=conversation,
        context_name=context.id, 
        context_description=context.description, 
        func_response=func_response
    )
    result = model.invoke(formatted_prompt)
    return result.llm_response

def full_extractor_inference(model_config: OpenAIModelConfig, chat: Chat, context: Context):
    """
    Inference function for the full extractor.
    """
    model = instantiate_model(model_config).with_structured_output(create_dynamic_output_model_without_response(context.requirements))
    fields_description = "\n".join([
        f"- {req.id}: {req.description}" + (
            "\n  Possible values:\n" +
            "\n".join([f"  - {pv.id}: {pv.description}" for pv in req.possible_values])
            if req.possible_values else ""
        )
        for req in context.requirements
    ])
    overhead_text = "\n".join(m.content for m in FULL_EXTRACTOR_TEMPLATE.format_messages(input="", fields_description=fields_description))
    conversation = chat.format_and_truncate_conversation(overhead_text)
    
    formatted_prompt = FULL_EXTRACTOR_TEMPLATE.format_messages(
        input=conversation,
        fields_description=fields_description
    )
    result = model.invoke(formatted_prompt)
    return result

def check_context_confirmation(model_config: OpenAIModelConfig, chat: Chat) -> bool:
    model = instantiate_model(model_config).with_structured_output(ContextConfirmation)
    overhead_text = "\n".join(m.content for m in CONFIRMATION_CHECK_TEMPLATE.format_messages(input=""))
    conversation = chat.format_and_truncate_conversation(overhead_text)
    formatted_prompt = CONFIRMATION_CHECK_TEMPLATE.format_messages(
        input=conversation
    )
    result = model.invoke(formatted_prompt)
    return result.confirmed

    
