import threading
import appdynamics.agent.models.custom_metrics as custom_metrics_mod
import appdynamics.agent.interceptor.utils.langchain_utils as langchain_utils

from appdynamics.agent.interceptor.utils.langchain_utils import LangchainConstants
from appdynamics.agent.interceptor.base import BaseInterceptor


class LangchainCommunityLLMInterceptor(BaseInterceptor):

    def __init__(self, agent, cls):
        super().__init__(agent, cls)
        self.agent = agent
        self.cls = cls
        self.model_attr_name = None

        if LangchainConstants.OPENAI_STRING in str(cls).lower():
            self.model_attr_name = LangchainConstants.MODEL_NAME_ATTR
        elif LangchainConstants.OLLAMA_STRING in str(cls).lower():
            self.model_attr_name = LangchainConstants.MODEL_ATTR

        self.thread_context = threading.local()
        self.thread_context.entry_method = None

    def report_metrics(self, model_name=None, reporting_values=dict()):
        try:
            for metric_name in reporting_values:
                if model_name:
                    self.agent.report_custom_metric(
                        custom_metrics_mod.CustomMetric(
                            name=langchain_utils.get_metric_path_from_params(
                                model_name,
                                LangchainConstants.LANGCHAIN_LLM_METRIC_PREFIX,
                                metric_name
                            ),
                            time_rollup_type=custom_metrics_mod.TIME_SUM),
                        reporting_values[metric_name]
                    )
                # Aggregate metric, - All models string
                self.agent.report_custom_metric(
                    custom_metrics_mod.CustomMetric(
                        name=langchain_utils.get_metric_path_from_params(
                            None,
                            LangchainConstants.LANGCHAIN_LLM_METRIC_PREFIX,
                            metric_name
                        ),
                        time_rollup_type=custom_metrics_mod.TIME_SUM),
                    reporting_values[metric_name]
                )
        except Exception as e:
            self.agent.logger.error(f"Error occured while reporting langchain metrics, error = {repr(e)}")

    async def __agenerate(self, _agenerate, cls_inst, prompts, *args, **kwargs):
        """
        Instrumentation for langchain_community.llms.<ThirdPartyLLMModel>'s _agenerate method
        The base method is is the asynchronous completion generation method for the LLM Model
        """
        response = None
        reporting_values = dict()
        if not self.thread_context:
            self.thread_context = threading.local()
        if not (hasattr(self.thread_context, 'entry_method') and self.thread_context.entry_method):
            self.thread_context.entry_method = '_agenerate'
        try:
            response = await _agenerate(cls_inst, prompts, *args, **kwargs)
        except:
            reporting_values[LangchainConstants.ERRORS_PERMIN_STRING] = 1
            raise
        finally:
            if hasattr(self.thread_context,
                       'entry_method') and self.thread_context.entry_method == '_agenerate':
                try:
                    input_prompts = prompts if isinstance(prompts, list) else [prompts]
                    reporting_values[LangchainConstants.PROMPTS_PERMIN_STRING] = \
                        len(input_prompts)
                    get_num_tokens = getattr(self.cls, 'get_num_tokens', None)
                    if get_num_tokens:
                        # input tokens metrics
                        input_tokens = 0
                        for prompt in input_prompts:
                            input_tokens += get_num_tokens(cls_inst, prompt)

                        reporting_values[LangchainConstants.INPUT_TOKENS_STRING] = input_tokens

                        output_tokens = 0
                        if response:
                            for n_generations in response.generations:
                                for generation in n_generations:
                                    output_tokens += get_num_tokens(cls_inst, generation.text)

                            reporting_values[LangchainConstants.OUTPUT_TOKENS_STRING] = output_tokens
                except Exception as e:
                    self.agent.logger.debug(f'Error occurred while capturing metrics: {str(e)}')
                finally:
                    model_name = None
                    if self.model_attr_name:
                        model_name = getattr(cls_inst, self.model_attr_name, None)
                    self.report_metrics(model_name, reporting_values)
                    self.thread_context.entry_method = None
        return response

    def __generate(self, _generate, cls_inst, prompts, *args, **kwargs):
        """
        Instrumentation for langchain_community.llms.<ThirdPartyLLMModel>'s _generate method
        The base method is is the synchronous completion generation method for the LLM Model
        """
        response = None
        reporting_values = dict()
        if not self.thread_context:
            self.thread_context = threading.local()
        if not (hasattr(self.thread_context, 'entry_method') and self.thread_context.entry_method):
            self.thread_context.entry_method = '_generate'
        try:
            response = _generate(cls_inst, prompts, *args, **kwargs)
        except:
            reporting_values[LangchainConstants.ERRORS_PERMIN_STRING] = 1
            raise
        finally:

            if hasattr(self.thread_context,
                       'entry_method') and self.thread_context.entry_method == '_generate':
                try:
                    input_prompts = prompts if isinstance(prompts, list) else [prompts]
                    reporting_values[LangchainConstants.PROMPTS_PERMIN_STRING] = \
                        len(input_prompts)
                    get_num_tokens = getattr(self.cls, 'get_num_tokens', None)
                    if get_num_tokens:
                        # input tokens metrics
                        input_tokens = 0
                        for prompt in input_prompts:
                            input_tokens += get_num_tokens(cls_inst, prompt)

                        reporting_values[LangchainConstants.INPUT_TOKENS_STRING] = input_tokens

                        # output tokens metrics
                        output_tokens = 0
                        if response:
                            for n_generations in response.generations:
                                for generation in n_generations:
                                    output_tokens += get_num_tokens(cls_inst, generation.text)

                            reporting_values[LangchainConstants.OUTPUT_TOKENS_STRING] = output_tokens
                except Exception as e:
                    self.agent.logger.debug(f'Error occurred while capturing metrics: {repr(e)}')
                finally:
                    model_name = None
                    if self.model_attr_name:
                        model_name = getattr(cls_inst, self.model_attr_name, None)
                    self.report_metrics(model_name, reporting_values)
                    self.thread_context.entry_method = None
        return response

    async def __astream(self, _astream, cls_inst, prompt, *args, **kwargs):
        output_tokens = 0
        reporting_values = dict()
        if not self.thread_context:
            self.thread_context = threading.local()
        if not (hasattr(self.thread_context, 'entry_method') and self.thread_context.entry_method):
            self.thread_context.entry_method = '_astream'
        try:
            response = _astream(cls_inst, prompt, *args, **kwargs)
            async for chunk in response:
                output_tokens += 1
                yield chunk
        except:
            reporting_values[LangchainConstants.ERRORS_PERMIN_STRING] = 1
            raise
        finally:

            if hasattr(self.thread_context,
                       'entry_method') and self.thread_context.entry_method == '_astream':
                try:
                    reporting_values[LangchainConstants.PROMPTS_PERMIN_STRING] = 1

                    get_num_tokens = getattr(self.cls, 'get_num_tokens', None)
                    if get_num_tokens:
                        # input tokens metrics
                        input_tokens = get_num_tokens(cls_inst, prompt)

                        reporting_values[LangchainConstants.INPUT_TOKENS_STRING] = input_tokens

                        # output tokens metrics
                        if output_tokens > 0:
                            reporting_values[LangchainConstants.OUTPUT_TOKENS_STRING] = output_tokens
                except Exception as e:
                    self.agent.logger.debug(f'Error occurred while capturing metrics: {repr(e)}')
                finally:
                    model_name = None
                    if self.model_attr_name:
                        model_name = getattr(cls_inst, self.model_attr_name, None)
                    self.report_metrics(model_name, reporting_values)
                    self.thread_context.entry_method = None

    def __stream(self, _stream, cls_inst, prompt, *args, **kwargs):
        output_tokens = 0
        reporting_values = dict()
        if not self.thread_context:
            self.thread_context = threading.local()
        if not (hasattr(self.thread_context, 'entry_method') and self.thread_context.entry_method):
            self.thread_context.entry_method = '_stream'

        try:
            response = _stream(cls_inst, prompt, *args, **kwargs)
            for chunk in response:
                output_tokens += 1
                yield chunk
        except:
            reporting_values[LangchainConstants.ERRORS_PERMIN_STRING] = 1
            raise
        finally:

            if hasattr(self.thread_context,
                       'entry_method') and self.thread_context.entry_method == '_stream':
                try:
                    reporting_values[LangchainConstants.PROMPTS_PERMIN_STRING] = 1
                    get_num_tokens = getattr(self.cls, 'get_num_tokens', None)
                    if get_num_tokens:
                        # input tokens metrics
                        input_tokens = get_num_tokens(cls_inst, prompt)

                        reporting_values[LangchainConstants.INPUT_TOKENS_STRING] = input_tokens

                        # output tokens metrics
                        if output_tokens > 0:
                            reporting_values[LangchainConstants.OUTPUT_TOKENS_STRING] = output_tokens
                except Exception as e:
                    self.agent.logger.debug(f'Error occurred while capturing llm metrics: {str(e)}')
                finally:
                    model_name = None
                    if self.model_attr_name:
                        model_name = getattr(cls_inst, self.model_attr_name, None)
                    self.report_metrics(model_name, reporting_values)
                    self.thread_context.entry_method = None


class LangchainCoreBaseModelInteceptor(BaseInterceptor):

    def report_metrics(self, reporting_values=dict()):
        try:
            for metric_name in reporting_values:
                self.agent.report_custom_metric(
                    custom_metrics_mod.CustomMetric(
                        name=metric_name,
                        cluster_rollup_type=None,
                        time_rollup_type=langchain_utils
                        .METRICS_DICT[metric_name][LangchainConstants.TIME_ROLLUP_STRING],
                        hole_handling_type=langchain_utils
                        .METRICS_DICT[metric_name][LangchainConstants.HOLE_HANDLING_STRING]
                    ),
                    reporting_values[metric_name]
                )
        except Exception as e:
            self.agent.logger.error(f"Error occured while reporting langchain metrics, error = {repr(e)}")

    async def _aget_prompts(self, aget_prompts, *args, **kwargs):
        reporting_values = dict()
        (existing_prompts, llm_string, missing_prompt_idxs, missing_prompts) = ({}, "[]", [], [])
        try:
            existing_prompts, llm_string, missing_prompt_idxs, missing_prompts = await aget_prompts(*args, **kwargs)
        except:
            reporting_values[LangchainConstants.CACHE_ERROR_METRIC_STRING] = 1
            raise
        finally:
            try:
                reporting_values[LangchainConstants.CACHE_MISSES_METRIC_STRING] = len(missing_prompt_idxs)
                reporting_values[LangchainConstants.CACHE_HITS_METRIC_STRING] = len(existing_prompts)
                self.report_metrics(reporting_values)
            except Exception as e1:
                self.agent.logger.warn(
                    f'error occurred while reporting LangchainCoreBaseModelInteceptor metrics: {repr(e1)}')
        return existing_prompts, llm_string, missing_prompt_idxs, missing_prompts

    def _get_prompts(self, get_prompts, *args, **kwargs):
        reporting_values = dict()
        (existing_prompts, llm_string, missing_prompt_idxs, missing_prompts) = ({}, "[]", [], [])
        try:
            existing_prompts, llm_string, missing_prompt_idxs, missing_prompts = get_prompts(*args, **kwargs)
        except:
            reporting_values[LangchainConstants.CACHE_ERROR_METRIC_STRING] = 1
            raise
        finally:
            try:
                reporting_values[LangchainConstants.CACHE_MISSES_METRIC_STRING] = len(missing_prompt_idxs)
                reporting_values[LangchainConstants.CACHE_HITS_METRIC_STRING] = len(existing_prompts)
                self.report_metrics(reporting_values)
            except Exception as e1:
                self.agent.logger.warn(
                    f'Error occurred while reporting LangchainCoreBaseModelInteceptor metrics: {repr(e1)}')
        return existing_prompts, llm_string, missing_prompt_idxs, missing_prompts


class LangchainCommunityEmbeddingsInterceptor(BaseInterceptor):

    def __init__(self, agent, cls):
        super().__init__(agent, cls)
        self.agent = agent
        self.cls = cls

        self.model_attr_name = None
        if any(llm_module in str(cls).lower() for llm_module in
               [LangchainConstants.OPENAI_STRING, LangchainConstants.OLLAMA_STRING]):
            self.model_attr_name = LangchainConstants.MODEL_ATTR

        self.thread_context = threading.local()
        self.thread_context.entry_method = None

    def report_metrics(self, model_name=None, reporting_values=dict()):
        try:
            for metric_name in reporting_values:
                if model_name:
                    self.agent.report_custom_metric(
                        custom_metrics_mod.CustomMetric(
                            name=langchain_utils.get_metric_path_from_params(
                                model_name,
                                LangchainConstants.LANGCHAIN_EMBEDDINGS_PREFIX,
                                metric_name
                            ),
                            cluster_rollup_type=None,
                            time_rollup_type=custom_metrics_mod.TIME_AVERAGE,
                            hole_handling_type=custom_metrics_mod.RATE_COUNTER
                        ),
                        reporting_values[metric_name]
                    )
                # Aggregate metric, - All models string
                self.agent.report_custom_metric(
                    custom_metrics_mod.CustomMetric(
                        name=langchain_utils.get_metric_path_from_params(
                            None,
                            LangchainConstants.LANGCHAIN_EMBEDDINGS_PREFIX,
                            metric_name
                        ),
                        cluster_rollup_type=None,
                        time_rollup_type=custom_metrics_mod.TIME_AVERAGE,
                        hole_handling_type=custom_metrics_mod.RATE_COUNTER
                    ),
                    reporting_values[metric_name]
                )
        except Exception as e:
            self.agent.logger.error(f"Error occured while reporting langchain metrics, error = {repr(e)}")

    async def _aembed_query(self, aembed_query, cls_inst, text):
        model_name = None
        if self.model_attr_name:
            model_name = getattr(cls_inst, self.model_attr_name, None)
        if not self.thread_context:
            self.thread_context = threading.local()
        if not (hasattr(self.thread_context, 'entry_method') and self.thread_context.entry_method):
            self.thread_context.entry_method = 'aembed_query'
        embeddings = []
        reporting_values = dict()
        try:
            embeddings = await aembed_query(cls_inst, text)
        except:
            reporting_values[LangchainConstants.EMBEDDING_ERRORS_PERMIN] = 1
            raise
        finally:

            if hasattr(self.thread_context,
                       'entry_method') and self.thread_context.entry_method == 'aembed_query':
                try:
                    reporting_values[LangchainConstants.EMBEDDING_QUERIES] = 1
                    self.report_metrics(model_name, reporting_values)
                except Exception as e:
                    self.agent.logger.warn(
                        f'error occurred while reporting LangchainCommunityEmbeddingsInterceptor metrics: {str(e)}')
                finally:
                    self.thread_context.entry_method = None
        return embeddings

    async def _aembed_documents(self, aembed_documents, cls_inst, texts):
        model_name = None
        if self.model_attr_name:
            model_name = getattr(cls_inst, self.model_attr_name, None)
        if not self.thread_context:
            self.thread_context = threading.local()
        if not (hasattr(self.thread_context, 'entry_method') and self.thread_context.entry_method):
            self.thread_context.entry_method = 'aembed_documents'

        embeddings = []

        reporting_values = dict()
        try:
            embeddings = await aembed_documents(cls_inst, texts)
        except:
            reporting_values[LangchainConstants.EMBEDDING_ERRORS_PERMIN] = 1
            raise
        finally:

            if hasattr(self.thread_context,
                       'entry_method') and self.thread_context.entry_method == 'aembed_documents':
                try:
                    reporting_values[LangchainConstants.EMBEDDING_QUERIES] = len(texts)
                    self.report_metrics(model_name, reporting_values)
                except Exception as e:
                    self.agent.logger.warn(
                        f'error occurred while reporting LangchainCommunityEmbeddingsInterceptor metrics: {str(e)}')
                finally:
                    self.thread_context.entry_method = None
        return embeddings

    def _embed_query(self, embed_query, cls_inst, text):
        model_name = None
        if self.model_attr_name:
            model_name = getattr(cls_inst, self.model_attr_name, None)
        if not self.thread_context:
            self.thread_context = threading.local()
        if not (hasattr(self.thread_context, 'entry_method') and self.thread_context.entry_method):
            self.thread_context.entry_method = 'embed_query'
        embeddings = []
        reporting_values = dict()
        try:
            embeddings = embed_query(cls_inst, text)
        except:
            reporting_values[LangchainConstants.EMBEDDING_ERRORS_PERMIN] = 1
            raise
        finally:

            if hasattr(self.thread_context,
                       'entry_method') and self.thread_context.entry_method == 'embed_query':
                try:
                    reporting_values[LangchainConstants.EMBEDDING_QUERIES] = 1
                    self.report_metrics(model_name, reporting_values)
                except Exception as e:
                    self.agent.logger.warn(
                        f'error occurred while reporting LangchainCommunityEmbeddingsInterceptor metrics: {str(e)}')
                finally:
                    self.thread_context.entry_method = None

        return embeddings

    def _embed_documents(self, embed_documents, cls_inst, texts):
        model_name = None
        if self.model_attr_name:
            model_name = getattr(cls_inst, self.model_attr_name, None)
        if not self.thread_context:
            self.thread_context = threading.local()
        if not (hasattr(self.thread_context, 'entry_method') and self.thread_context.entry_method):
            self.thread_context.entry_method = 'embed_documents'

        embeddings = []
        reporting_values = dict()
        try:
            embeddings = embed_documents(cls_inst, texts)
        except:
            reporting_values[LangchainConstants.EMBEDDING_ERRORS_PERMIN] = 1
            raise
        finally:
            if hasattr(self.thread_context,
                       'entry_method') and self.thread_context.entry_method == 'embed_documents':
                try:
                    reporting_values[LangchainConstants.EMBEDDING_QUERIES] = len(texts)
                    self.report_metrics(model_name, reporting_values)
                except Exception as e:
                    self.agent.logger.warn(
                        f'error occurred while reporting LangchainCommunityEmbeddingsInterceptor metrics: {str(e)}')
                finally:
                    self.thread_context.entry_method = None
        return embeddings


# langchain-ollama
def intercept_langchain_ollama_llms(agent, mod):
    LangchainCommunityLLMInterceptor(agent, mod.OllamaLLM).attach(['_agenerate', '_generate', '_astream', '_stream'])


def intercept_langchain_ollama_embeddings(agent, mod):
    LangchainCommunityEmbeddingsInterceptor(agent, mod.OllamaEmbeddings).attach(
        ['embed_query', 'embed_documents', 'aembed_query', 'aembed_documents'])


def intercept_langchain_ollama_chat_models(agent, mod):
    LangchainCommunityLLMInterceptor(agent, mod.ChatOllama).attach(['_agenerate', '_generate', '_astream', '_stream'])


# langchain
def intercept_langchain_community_llms(agent, mod):
    # Ollama interceptor
    LangchainCommunityLLMInterceptor(agent, mod.Ollama).attach(['_agenerate', '_generate', '_astream', '_stream'])


def intercept_langchain_community_chat_models(agent, mod):
    # Ollama async interceptor
    LangchainCommunityLLMInterceptor(agent, mod.ChatOllama).attach(['_agenerate', '_generate', '_astream', '_stream'])


def intercept_langchain_community_embeddings(agent, mod):
    # Ollama embeddings model interceptors
    LangchainCommunityEmbeddingsInterceptor(agent, mod.OllamaEmbeddings).attach(
        ['embed_query', 'embed_documents', 'aembed_query', 'aembed_documents'])


def intercept_langchain_core_language_models(agent, mod):
    LangchainCoreBaseModelInteceptor(agent, mod.llms).attach(['aget_prompts', 'get_prompts'])
