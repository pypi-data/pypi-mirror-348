from __future__ import unicode_literals

from ..base import ExitCallInterceptor
from appdynamics.agent.models.exitcalls import EXIT_DB, EXIT_SUBTYPE_DB
from .. import HOST_PROPERTY_MAX_LEN, DB_NAME_PROPERTY_MAX_LEN
from appdynamics.lib import MissingConfigException
import threading
import appdynamics.agent.models.custom_metrics as custom_metrics_mod
from appdynamics import config

TIER_METRIC_PATH = "Agent|Langchain|VectorStores|PGVector"
TIME_ROLLUP_STRING = "time_rollup_type"
CLUSTER_ROLLUP_STRING = "cluster_rollup_type"
HOLE_HANDLING_STRING = "hole_handling_type"
METRIC_PATH_SEGREGATOR = "|"


def get_db_backend_props(connection_string):
    naming_format_string = '{HOST}:{PORT} - {DATABASE} - {VENDOR} - {VERSION}'
    host = 'unknown'
    port = 'unknown'
    database = 'unknown'
    try:
        suffix = connection_string.split("://")[1]
        if "?" in suffix:
            suffix = suffix.split("?")[0]
        if "@" in suffix:
            suffix = suffix.split("@")[1]
        database = 'unknown'
        if "/" in suffix:
            database = suffix.split("/")[1]
            suffix = suffix.split("/")[0]
        host = suffix.split(":")[0]
        port = suffix.split(":")[1]
    except:
        pass

    host = host[:HOST_PROPERTY_MAX_LEN]
    database = database[:DB_NAME_PROPERTY_MAX_LEN]

    backend_properties = {
        'VENDOR': 'PostgreSQL',
        'HOST': host,
        'PORT': str(port),
        'DATABASE': database,
        'VERSION': 'unknown',
    }

    return backend_properties, naming_format_string


class PGVectorInterceptor(ExitCallInterceptor):

    def __init__(self, agent, cls):
        super(PGVectorInterceptor, self).__init__(agent, cls)
        self.docsCountMetric = custom_metrics_mod.CustomMetric(
            name=TIER_METRIC_PATH + METRIC_PATH_SEGREGATOR + "Documents retrieved count",
            time_rollup_type=custom_metrics_mod.TIME_AVERAGE,
            hole_handling_type=custom_metrics_mod.REGULAR_COUNTER
        )
        self.errorMetric = custom_metrics_mod.CustomMetric(
            name=TIER_METRIC_PATH + METRIC_PATH_SEGREGATOR + "Errors",
            time_rollup_type=custom_metrics_mod.TIME_AVERAGE,
            hole_handling_type=custom_metrics_mod.REGULAR_COUNTER
        )
        self.searchScoreMetric = custom_metrics_mod.CustomMetric(
            name=TIER_METRIC_PATH + METRIC_PATH_SEGREGATOR + "Search Score",
            time_rollup_type=custom_metrics_mod.TIME_AVERAGE,
            hole_handling_type=custom_metrics_mod.REGULAR_COUNTER
        )
        self.threadlocal_storage = None

    def __query_collection(self, _query_collection, *args, **kwargs):
        return self.___query_collection(_query_collection, *args, **kwargs)

    def ___query_collection(self, __query_collection, *args, **kwargs):
        exit_call = None
        err = False
        bt = self.bt
        appd_db_query = None
        db_output_res = []
        create_response = None
        # Unset the query string stashed in threadlocal_storage
        if self.threadlocal_storage and hasattr(self.threadlocal_storage, "appd_db_query"):
            appd_db_query = self.threadlocal_storage.appd_db_query
            self.threadlocal_storage.appd_db_query = None
        backend = self.create_db_backend(args[0])
        try:
            if bt and backend:
                exit_call = self.start_exit_call(bt, backend, operation="Query Collection")
            create_response = __query_collection(*args, **kwargs)
        except:
            err = True
            raise
        finally:
            if exit_call:
                if config.ENABLE_GENAI_DATA_CAPTURE:
                    if appd_db_query:
                        exit_call.optional_properties["VectorDB input query"] = str(appd_db_query)
                    db_output_res = self.get_db_output_res(create_response)
                    if db_output_res:
                        exit_call.optional_properties["VectorDB response"] = str(db_output_res)
                self.end_exit_call(exit_call)
            try:
                self.agent.report_custom_metric(
                    self.docsCountMetric,
                    len(create_response)
                )
                if err:
                    self.agent.report_custom_metric(
                        self.errorMetric,
                        1
                    )
                if db_output_res:
                    for result in create_response:
                        self.agent.report_custom_metric(
                            self.searchScoreMetric,
                            int(result._mapping.distance * 100)
                        )
            except Exception as e:
                self.agent.logger.warn(f'Error occurred while reporting pgvector metrics: {repr(e)}')
        return create_response

    async def ___aquery_collection(self, __aquery_collection, *args, **kwargs):
        exit_call = None
        err = False
        bt = self.bt
        appd_db_query = None
        db_output_res = []
        create_response = None
        if self.threadlocal_storage and hasattr(self.threadlocal_storage, "appd_db_query"):
            appd_db_query = self.threadlocal_storage.appd_db_query
            self.threadlocal_storage.appd_db_query = None
        backend = self.create_db_backend(args[0])
        try:
            if bt and backend:
                exit_call = self.start_exit_call(bt, backend, operation="Query Collection")
            create_response = await __aquery_collection(*args, **kwargs)
        except:
            err = True
            raise
        finally:
            if exit_call:
                if config.ENABLE_GENAI_DATA_CAPTURE:
                    if appd_db_query:
                        exit_call.optional_properties["VectorDB input query"] = str(appd_db_query)
                    db_output_res = self.get_db_output_res(create_response)
                    if db_output_res:
                        exit_call.optional_properties["VectorDB response"] = str(db_output_res)
                    self.end_exit_call(exit_call)
            try:
                self.agent.report_custom_metric(
                    self.docsCountMetric,
                    len(create_response)
                )
                if err:
                    self.agent.report_custom_metric(
                        self.errorMetric,
                        1
                    )
                if db_output_res:
                    for result in create_response:
                        self.agent.report_custom_metric(
                            self.searchScoreMetric,
                            int(result._mapping.distance * 100)
                        )
            except Exception as e:
                self.agent.logger.warn(f'Error occurred while reporting pgvector metrics: {repr(e)}')
        return create_response

    def _add_embeddings(self, add_embeddings, *args, **kwargs):
        exit_call = None
        err = False
        bt = self.bt
        backend = self.create_db_backend(args[0])
        create_response = None
        try:
            if backend and bt:
                exit_call = self.start_exit_call(bt, backend, operation="Add Embeddings")
            create_response = add_embeddings(*args, **kwargs)
        except:
            err = True
            raise
        finally:
            if exit_call:
                if config.ENABLE_GENAI_DATA_CAPTURE:
                    db_input_query = None
                    if 'texts' in kwargs:
                        db_input_query = kwargs.get('texts')
                    elif args and len(args) > 1:
                        db_input_query = args[1]

                    if db_input_query:
                        exit_call.optional_properties["VectorDB input query"] = str(db_input_query)
                self.end_exit_call(exit_call)
            try:
                if err:
                    self.agent.report_custom_metric(
                        self.errorMetric,
                        1
                    )
            except Exception as e:
                self.agent.logger.warn(f'Error occurred while reporting pgvector metrics: {repr(e)}')
        return create_response

    async def _aadd_embeddings(self, aadd_embeddings, *args, **kwargs):
        exit_call = None
        err = False
        bt = self.bt
        backend = self.create_db_backend(args[0])
        create_response = None
        try:
            if backend and bt:
                exit_call = self.start_exit_call(bt, backend, operation="Add Embeddings")
            create_response = await aadd_embeddings(*args, **kwargs)
        except:
            err = True
            raise
        finally:
            if exit_call:
                if config.ENABLE_GENAI_DATA_CAPTURE:
                    db_input_query = None
                    if 'texts' in kwargs:
                        db_input_query = kwargs.get('texts')
                    elif args and len(args) > 1:
                        db_input_query = args[1]

                    if db_input_query:
                        exit_call.optional_properties["VectorDB input query"] = str(db_input_query)
                self.end_exit_call(exit_call)
            try:
                if err:
                    self.agent.report_custom_metric(
                        self.errorMetric,
                        1
                    )
            except Exception as e:
                self.agent.logger.warn(f'Error occurred while reporting pgvector metrics: {repr(e)}')
        return create_response

    def create_db_backend(self, pg_instance):
        backend = None
        try:
            if self.agent.backend_registry is None:
                raise MissingConfigException
            db_conn_string = self.get_db_conn_string(pg_instance)
            if not db_conn_string:
                raise Exception("Cannot retrieve db connection string")
            backend_properties, naming_format_string = get_db_backend_props(db_conn_string)
            backend = self.agent.backend_registry.get_backend(EXIT_DB, EXIT_SUBTYPE_DB,
                                                              backend_properties, naming_format_string)
        except MissingConfigException:
            pass
        except Exception as exc:
            self.agent.logger.error(f"Error occured identifying pgvector backend, error = {repr(exc)}")
        return backend

    def get_db_conn_string(self, pg_instance):
        conn_string = getattr(pg_instance, 'connection_string', None)
        if conn_string:
            return conn_string
        db_engine = getattr(pg_instance, '_engine', None)
        if not db_engine:
            db_engine = getattr(pg_instance, '_async_engine', None)
            db_engine = db_engine.sync_engine
        if db_engine:
            conn_string = db_engine.url.__to_string__()
        return conn_string

    # Stash DB query to threadlocal_storage global obj in this class, unset in __query_collection
    def search(self, search, *args, **kwargs):
        if not self.threadlocal_storage:
            self.threadlocal_storage = threading.local()
        self.threadlocal_storage.appd_db_query = self.get_appd_db_query(*args, **kwargs)
        return search(*args, **kwargs)

    async def asearch(self, asearch, *args, **kwargs):
        if not self.threadlocal_storage:
            self.threadlocal_storage = threading.local()
        self.threadlocal_storage.appd_db_query = self.get_appd_db_query(*args, **kwargs)
        return await asearch(*args, **kwargs)

    def get_appd_db_query(self, *args, **kwargs):
        db_input_query = None
        if 'query' in kwargs:
            db_input_query = kwargs.get('query')
        elif args and len(args) > 1:
            db_input_query = args[1]
        return db_input_query

    def get_db_output_res(self, create_response):
        db_output_res = []
        try:
            for result in create_response:
                score_doc_dict = dict()
                if hasattr(result._mapping, "distance"):
                    score_doc_dict["Search score"] = result._mapping.distance
                score_doc_dict["Document"] = result._mapping.EmbeddingStore.document
                score_doc_dict["Metadata"] = result._mapping.EmbeddingStore.cmetadata
                db_output_res.append(score_doc_dict)
        except:
            self.agent.logger.error("Error occured while parsing vectorDB response")
        return db_output_res


def intercept_pg_vector(agent, mod):
    pgvectorInterceptor = PGVectorInterceptor(agent, mod.PGVector)
    # In newer langchain_community.pgvector they changed method to _query_collection
    try:
        pgvectorInterceptor.attach('__query_collection')
    except:
        pgvectorInterceptor.attach('_query_collection')
    pgvectorInterceptor.attach('add_embeddings')
    if config.ENABLE_GENAI_DATA_CAPTURE:
        pgvectorInterceptor.attach([
            'similarity_search',
            'similarity_search_with_score',
            'max_marginal_relevance_search',
            'max_marginal_relevance_search_with_score'
        ], patched_method_name='search')


def intercept_langchain_postgres(agent, mod):
    pgvectorInterceptor = PGVectorInterceptor(agent, mod.PGVector)
    pgvectorInterceptor.attach([
        '__query_collection',
        '__aquery_collection',
        'add_embeddings',
        'aadd_embeddings',
    ])
    if config.ENABLE_GENAI_DATA_CAPTURE:
        pgvectorInterceptor.attach([
            'similarity_search',
            'similarity_search_with_score',
            'max_marginal_relevance_search',
            'max_marginal_relevance_search_with_score'
        ], patched_method_name='search')
        pgvectorInterceptor.attach([
            'asimilarity_search',
            'asimilarity_search_with_score',
            'amax_marginal_relevance_search',
            'amax_marginal_relevance_search_with_score'
        ], patched_method_name='asearch')
