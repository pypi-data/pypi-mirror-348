from typing import TypeVar, get_args, get_origin

from pydantic import BaseModel

from forecasting_tools.ai_models.ai_utils.ai_misc import clean_indents
from forecasting_tools.ai_models.general_llm import GeneralLlm

T = TypeVar("T")


async def structure_output(
    output: str, output_type: type[T], model: GeneralLlm | str = "gpt-4o-mini"
) -> T:
    # Initialize with empty instructions
    pydantic_instructions = ""

    # Check if output_type is directly a BaseModel subclass
    try:
        if issubclass(output_type, BaseModel):
            pydantic_instructions = (
                GeneralLlm.get_schema_format_instructions_for_pydantic_type(
                    output_type
                )
            )
    except TypeError:
        # Not a class, might be a generic type like list[BaseModel]
        pass

    # Check if output_type is list[BaseModel]
    origin = get_origin(output_type)
    if origin is list:
        args = get_args(output_type)
        if args and len(args) == 1:
            item_type = args[0]
            try:
                if issubclass(item_type, BaseModel):
                    pydantic_instructions = GeneralLlm.get_schema_format_instructions_for_pydantic_type(
                        item_type
                    )
            except TypeError:
                pass

    prompt = clean_indents(
        f"""
        You are a secretary helping to convert text into structured data.
        You will receive text in between a bunch of <><><><><><><><><><><><> (each with 'start' and 'end' tags)
        Please convert the text to the following python parsable type:
        {output_type}

        When you give your answer, give no reasoning. Just output the final type w/o any other words.
        If the type requires fields (e.g. dict or pydantic type):
        - Please return a JSON object (i.e. a dict)
        - Only fill in fields that are explicitly given and required in the text
        - Do not guess the fields
        - Do not fill in fields that are not explicitly given and required in the text
        - Do not summarize any of the text. Only give direct quotes (with only slight formatting changes)

        Please prioritize using any 'final answers' to fill your structured response if they are mentioned (avoid using intermediary steps)
        Here is the text:

        <><><><><><><><><><><> START TEXT <><><><><><><><><><><>



        {output}



        <><><><><><><><><><><> END TEXT <><><><><><><><><><><>


        Please convert the text to the following type:
        {output_type}

        {pydantic_instructions}
        """
    ).strip()

    llm = GeneralLlm.to_llm(model)
    result = await llm.invoke_and_return_verified_type(prompt, output_type)
    return result
