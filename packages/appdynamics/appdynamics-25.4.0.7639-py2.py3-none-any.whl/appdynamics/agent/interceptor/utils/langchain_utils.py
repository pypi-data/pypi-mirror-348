import appdynamics.agent.models.custom_metrics as custom_metrics_mod


class LangchainConstants():
    LANGCHAIN_METRIC_PREFIX = "Agent|Langchain"
    LLM_METRIC_SUBPATH = "|LLM|"
    METRIC_PATH_SEGREGATOR = "|"
    EMBEDDINGS_METRIC_SUBPATH = "|Embeddings|"
    LANGCHAIN_EMBEDDINGS_PREFIX = "Agent|Langchain|Embeddings|"
    LANGCHAIN_LLM_METRIC_PREFIX = "Agent|Langchain|LLM|"
    CACHE_ERROR_METRIC_STRING = LANGCHAIN_METRIC_PREFIX + LLM_METRIC_SUBPATH + \
        "Cache Errors per minute - All Models"
    CACHE_MISSES_METRIC_STRING = LANGCHAIN_METRIC_PREFIX + LLM_METRIC_SUBPATH + \
        "Cache Misses - All Models"
    CACHE_HITS_METRIC_STRING = LANGCHAIN_METRIC_PREFIX + LLM_METRIC_SUBPATH + \
        "Cache Hits - All Models"
    ALL_MODELS_STRING = " - All Models"
    ERRORS_PERMIN_STRING = "Errors per minute"
    PROMPTS_PERMIN_STRING = "Prompts per minute"
    INPUT_TOKENS_STRING = "Input Tokens"
    OUTPUT_TOKENS_STRING = "Output Tokens"
    EMBEDDING_QUERIES = "Embedding queries"
    EMBEDDING_ERRORS_PERMIN = "Embedding Errors per minute"
    EMBEDDING_QUERIES_ALL_MODELS = EMBEDDING_QUERIES + " - All Models"
    CLUSTER_ROLLUP_STRING = "cluster_rollup_type"
    HOLE_HANDLING_STRING = "hole_handling_type"
    TIME_ROLLUP_STRING = "time_rollup_type"
    OPENAI_STRING = "openai"
    OLLAMA_STRING = "ollama"
    MODEL_NAME_ATTR = "model_name"
    MODEL_ATTR = "model"


METRICS_DICT = {
    LangchainConstants.CACHE_ERROR_METRIC_STRING: {
        LangchainConstants.TIME_ROLLUP_STRING: custom_metrics_mod.TIME_AVERAGE,
        LangchainConstants.CLUSTER_ROLLUP_STRING: None,
        LangchainConstants.HOLE_HANDLING_STRING: custom_metrics_mod.RATE_COUNTER
    },
    LangchainConstants.CACHE_MISSES_METRIC_STRING: {
        LangchainConstants.TIME_ROLLUP_STRING: custom_metrics_mod.TIME_AVERAGE,
        LangchainConstants.CLUSTER_ROLLUP_STRING: None,
        LangchainConstants.HOLE_HANDLING_STRING: custom_metrics_mod.RATE_COUNTER
    },
    LangchainConstants.CACHE_HITS_METRIC_STRING: {
        LangchainConstants.TIME_ROLLUP_STRING: custom_metrics_mod.TIME_AVERAGE,
        LangchainConstants.CLUSTER_ROLLUP_STRING: None,
        LangchainConstants.HOLE_HANDLING_STRING: custom_metrics_mod.RATE_COUNTER
    }

}


def get_metric_path_from_params(model_name=None, metric_prefix="", metric_suffix=""):
    if model_name:
        # Replace special char as it changes metric hierarchy
        model_name = model_name.replace(":", "_")
        return metric_prefix + model_name + LangchainConstants.METRIC_PATH_SEGREGATOR + metric_suffix
    else:
        return metric_prefix + metric_suffix + LangchainConstants.ALL_MODELS_STRING
