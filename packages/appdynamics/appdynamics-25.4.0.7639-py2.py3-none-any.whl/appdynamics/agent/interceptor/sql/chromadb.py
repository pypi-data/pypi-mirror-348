from __future__ import unicode_literals

from ..base import ExitCallInterceptor, BaseInterceptor
from appdynamics.agent.models.exitcalls import EXIT_DB, EXIT_SUBTYPE_DB
from appdynamics.lib import MissingConfigException
import appdynamics.agent.models.custom_metrics as custom_metrics_mod
from appdynamics import config

TIER_METRIC_PATH = "Agent|Langchain|VectorStores|Chromadb"
TIME_ROLLUP_STRING = "time_rollup_type"
CLUSTER_ROLLUP_STRING = "cluster_rollup_type"
HOLE_HANDLING_STRING = "hole_handling_type"
METRIC_PATH_SEGREGATOR = "|"

DOCS_RETRIEVED_STRING = "Documents retrieved count"
SEARCH_SCORE_STRING = "Search Score"
INSERTION_COUNT_STRING = "Document insertion count"
INSERTION_TIME_TAKEN = "Insertion Time taken"


def get_db_backend(client_obj):
    host = 'unknown'
    port = 'unknown'
    naming_format_string = None
    if "fastapi" in client_obj.__class__.__name__.lower():
        naming_format_string = '{HOST}:{PORT} - {DATABASE} - {VENDOR} - {VERSION}'
        try:
            url_string = getattr(client_obj, '_api_url', None)
            if url_string:
                host_port_path = url_string.split('//')[1]
                host_port = host_port_path.split('/')[0]
                host = host_port.split(':')[0]
                port = host_port.split(':')[1]
        except:
            pass
    else:
        host = 'localhost'
        naming_format_string = '{HOST} - {DATABASE} - {VENDOR} - {VERSION}'

    backend_properties = {
        'VENDOR': 'Chroma',
        'HOST': str(host),
        'PORT': str(port),
        'DATABASE': 'ChromaDB',
        'VERSION': 'unknown',
    }
    return backend_properties, naming_format_string


class ChromadbInterceptor(ExitCallInterceptor):

    def __init__(self, agent, cls):
        super(ChromadbInterceptor, self).__init__(agent, cls)
        self.operation_count_metric_dict = dict()
        self.num = 0
        self.searchScoreMetric = custom_metrics_mod.CustomMetric(
            name=TIER_METRIC_PATH + METRIC_PATH_SEGREGATOR + SEARCH_SCORE_STRING,
            time_rollup_type=custom_metrics_mod.TIME_AVERAGE,
            hole_handling_type=custom_metrics_mod.REGULAR_COUNTER)
        self.errorMetric = custom_metrics_mod.CustomMetric(
            name=TIER_METRIC_PATH + METRIC_PATH_SEGREGATOR + "Errors",
            time_rollup_type=custom_metrics_mod.TIME_AVERAGE,
            hole_handling_type=custom_metrics_mod.REGULAR_COUNTER)
        self.docsCountMetric = custom_metrics_mod.CustomMetric(
            name=TIER_METRIC_PATH + METRIC_PATH_SEGREGATOR + DOCS_RETRIEVED_STRING,
            time_rollup_type=custom_metrics_mod.TIME_AVERAGE,
            hole_handling_type=custom_metrics_mod.REGULAR_COUNTER
        )

    def run_command(self, command_func, *args, **kwargs):
        response_obj = None
        bt = self.bt
        backend = None
        try:
            client_obj = getattr(args[0], '_client', None)
            if client_obj:
                if self.agent.backend_registry is None:
                    raise MissingConfigException
                backend_properties, naming_format_string = get_db_backend(client_obj)
                backend = self.agent.backend_registry.get_backend(EXIT_DB, EXIT_SUBTYPE_DB,
                                                                  backend_properties, naming_format_string)
        except MissingConfigException:
            pass
        except Exception as e:
            self.agent.logger.error(f"Error occured while creating appd backend: {repr(e)}")

        query_type = getattr(command_func, '__name__', 'Query')
        db_input_query = None
        # for Collection.upsert operation, db query string is not retrieved from appd_db_query
        if "appd_db_query" in kwargs:
            db_input_query = kwargs.get('appd_db_query')
            kwargs.pop("appd_db_query")
        elif "documents" in kwargs:
            db_input_query = kwargs.get('documents')

        exit_call = None
        err = False
        try:
            if bt and backend:
                exit_call = self.start_exit_call(bt, backend, operation=f"Collection.{query_type}")
            response_obj = command_func(*args, **kwargs)
        except:
            err = True
            raise
        finally:
            if exit_call:
                if config.ENABLE_GENAI_DATA_CAPTURE and db_input_query:
                    exit_call.optional_properties["VectorDB input query"] = str(db_input_query)
                if config.ENABLE_GENAI_DATA_CAPTURE and response_obj:
                    exit_call.optional_properties["VectorDB response"] = self.get_db_output_res(response_obj)
                self.end_exit_call(exit_call)

            try:
                if query_type not in self.operation_count_metric_dict:
                    self.operation_count_metric_dict[query_type] = custom_metrics_mod.CustomMetric(
                        name=TIER_METRIC_PATH + METRIC_PATH_SEGREGATOR + "operation" +
                        METRIC_PATH_SEGREGATOR + query_type + METRIC_PATH_SEGREGATOR + "Calls per minute",
                        time_rollup_type=custom_metrics_mod.TIME_SUM,
                        hole_handling_type=custom_metrics_mod.RATE_COUNTER
                    )

                if response_obj and 'distances' in response_obj and response_obj['distances']:
                    for score in response_obj['distances'][0]:
                        self.agent.report_custom_metric(
                            self.searchScoreMetric,
                            int(score * 100)
                        )
                    self.agent.report_custom_metric(
                        self.docsCountMetric,
                        len(response_obj['documents'][0])
                    )
                if (query_type in self.operation_count_metric_dict):
                    self.agent.report_custom_metric(
                        self.operation_count_metric_dict[query_type],
                        1
                    )
                if err:
                    self.agent.report_custom_metric(
                        self.errorMetric,
                        1
                    )
            except Exception as e:
                self.agent.logger.warn(f'error occurred while reporting chromadb metrics: {repr(e)}')
        return response_obj

    def get_db_output_res(self, create_response):
        db_output_res = []
        try:
            for result in zip(create_response["distances"][0],
                              create_response["documents"][0],
                              create_response["metadatas"][0]):
                score_doc_dict = dict()
                score_doc_dict["Search score"] = result[0]
                score_doc_dict["Document"] = result[1]
                score_doc_dict["Metadata"] = result[2]
                db_output_res.append(score_doc_dict)
        except:
            self.agent.logger.error("Error occured while parsing vectorDB response")
        return db_output_res


class ChromaQuerySearchInterceptor(BaseInterceptor):

    # for stashing query string used in the exit call context and populating in SEC
    def _similarity_search_with_score(self, similarity_search_with_score, *args, **kwargs):
        if config.ENABLE_GENAI_DATA_CAPTURE:
            appd_db_query = None
            if 'query' in kwargs:
                appd_db_query = kwargs.get('query')
            elif args and len(args) > 1:
                appd_db_query = args[1]
            return similarity_search_with_score(*args, appd_db_query=appd_db_query, **kwargs)
        else:
            return similarity_search_with_score(*args, **kwargs)


def intercept_chromadb_similarity_search(agent, mod):
    ChromadbInterceptor(agent, mod.Collection).attach([
        'add',
        'get',
        'peek',
        'delete',
        'upsert',
        'query',
        'modify',
        'update',
    ], patched_method_name='run_command')


def intercept_chromadb_collection_operations(agent, mod):
    ChromaQuerySearchInterceptor(agent, mod.Chroma).attach('similarity_search_with_score')
