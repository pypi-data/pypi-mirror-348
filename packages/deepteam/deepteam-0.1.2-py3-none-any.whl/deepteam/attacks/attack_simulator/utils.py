from pydantic import BaseModel
from .schema import SyntheticData, SyntheticDataList

from deepeval.metrics.utils import trimAndLoadJson, initialize_model
from deepeval.models import DeepEvalBaseLLM


def generate_schema(
    prompt: str,
    schema: BaseModel,
    using_native_model: bool = None,
    model: DeepEvalBaseLLM = None,
) -> BaseModel:
    """
    Generate schema using the provided model.

    Args:
        prompt: The prompt to send to the model
        schema: The schema to validate the response against
        using_native_model: Whether the model is a native model
        model: The model to use

    Returns:
        The validated schema object
    """
    # If using_native_model is not provided, initialize from model
    if using_native_model is None and model is not None:
        _, using_native_model = initialize_model(model=model)

    if using_native_model:
        res, _ = model.generate(prompt, schema=schema)
        return res
    else:
        try:
            res = model.generate(prompt, schema=schema)
            return res
        except TypeError:
            res = model.generate(prompt)
            data = trimAndLoadJson(res)
            if schema == SyntheticDataList:
                data_list = [SyntheticData(**item) for item in data["data"]]
                return SyntheticDataList(data=data_list)
            else:
                return schema(**data)


async def a_generate_schema(
    prompt: str,
    schema: BaseModel,
    using_native_model: bool = None,
    model: DeepEvalBaseLLM = None,
) -> BaseModel:
    """
    Asynchronously generate schema using the provided model.

    Args:
        prompt: The prompt to send to the model
        schema: The schema to validate the response against
        using_native_model: Whether the model is a native model
        model: The model to use

    Returns:
        The validated schema object
    """
    # If using_native_model is not provided, initialize from model
    if using_native_model is None and model is not None:
        _, using_native_model = initialize_model(model=model)

    if using_native_model:
        res, _ = await model.a_generate(prompt, schema=schema)
        return res
    else:
        try:
            res = await model.a_generate(prompt, schema=schema)
            return res
        except TypeError:
            res = await model.a_generate(prompt)
            data = trimAndLoadJson(res)
            if schema == SyntheticDataList:
                data_list = [SyntheticData(**item) for item in data["data"]]
                return SyntheticDataList(data=data_list)
            else:
                return schema(**data)
