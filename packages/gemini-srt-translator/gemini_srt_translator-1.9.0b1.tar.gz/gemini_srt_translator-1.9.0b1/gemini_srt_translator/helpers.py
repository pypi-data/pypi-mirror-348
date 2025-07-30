from google.genai import types


def get_instruction(language: str, description: str) -> str:
    """
    Get the instruction for the translation model based on the target language.
    """
    instruction = (
        f"You are an assistant that translates subtitles.\n"
        f"You will receive a list of objects, each with two fields:\n"
        f"- index: a string identifier\n"
        f"- content: the subtitle text to translate\n\n"
        f"Translate ONLY the 'content' field of each object into {language}.\n"
        f"Return a list of objects with the same structure, preserving the original 'index' values.\n"
        f"Keep all formatting, line breaks, and special characters in the 'content' field that do not affect translation.\n"
        f"Do NOT merge or split objects. Translate each object's 'content' separately."
    )
    if description:
        instruction += f"\nAdditional user instruction: '{description}'"
    return instruction


def get_safety_settings() -> list[types.SafetySetting]:
    """
    Get the safety settings for the translation model.
    """
    return [
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=types.HarmBlockThreshold.BLOCK_NONE,
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=types.HarmBlockThreshold.BLOCK_NONE,
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY,
            threshold=types.HarmBlockThreshold.BLOCK_NONE,
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=types.HarmBlockThreshold.BLOCK_NONE,
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=types.HarmBlockThreshold.BLOCK_NONE,
        ),
    ]


def get_response_schema() -> types.Schema:
    """
    Get the response schema for the translation model.
    """
    return types.Schema(
        type="ARRAY",
        items=types.Schema(
            type="OBJECT",
            properties={
                "index": types.Schema(type="STRING"),
                "content": types.Schema(type="STRING"),
            },
            required=["index", "content"],
        ),
    )
