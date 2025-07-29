import logging
import typing as t

from apolo_app_types import (
    HuggingFaceModel,
    VLLMOutputsV2,
)
from apolo_app_types.clients.kube import get_service_host_port
from apolo_app_types.outputs.utils.ingress import get_ingress_host_port
from apolo_app_types.outputs.utils.parsing import parse_cli_args
from apolo_app_types.protocols.common.openai_compat import (
    OpenAICompatChatAPI,
    OpenAICompatEmbeddingsAPI,
)
from apolo_app_types.protocols.llm import LLMApiKey, LLMModel


logger = logging.getLogger()


async def get_llm_inference_outputs(helm_values: dict[str, t.Any]) -> dict[str, t.Any]:
    internal_host, internal_port = await get_service_host_port(
        match_labels={"application": "llm-inference"}
    )
    server_extra_args = helm_values.get("serverExtraArgs", [])
    cli_args = parse_cli_args(server_extra_args)
    # API key could be defined in server args or within envs.
    # The first one has higher priority
    api_key = cli_args.get("api-key") or helm_values.get("env", {}).get("VLLM_API_KEY")

    model_name = helm_values["model"]["modelHFName"]
    tokenizer_name = helm_values["model"].get("tokenizerHFName", "")

    chat_internal_api = OpenAICompatChatAPI(
        host=internal_host,
        port=int(internal_port),
        protocol="http",
    )
    embeddings_internal_api = OpenAICompatEmbeddingsAPI(
        host=internal_host,
        port=int(internal_port),
        protocol="http",
    )

    ingress_host_port = await get_ingress_host_port(
        match_labels={"application": "llm-inference"}
    )
    chat_external_api = None
    embeddings_external_api = None
    if ingress_host_port:
        chat_external_api = OpenAICompatChatAPI(
            host=ingress_host_port[0],
            port=int(ingress_host_port[1]),
            protocol="https",
        )
        embeddings_external_api = OpenAICompatEmbeddingsAPI(
            host=ingress_host_port[0],
            port=int(ingress_host_port[1]),
            protocol="https",
        )

    vllm_outputs = VLLMOutputsV2(
        chat_internal_api=chat_internal_api,
        chat_external_api=chat_external_api,
        embeddings_internal_api=embeddings_internal_api,
        embeddings_external_api=embeddings_external_api,
        llm=LLMModel(
            hugging_face_model=HuggingFaceModel(model_hf_name=model_name),
            tokenizer_hf_name=tokenizer_name,
            server_extra_args=server_extra_args,
        ),
        llm_api_key=LLMApiKey(key=api_key),
    )
    return vllm_outputs.model_dump()
