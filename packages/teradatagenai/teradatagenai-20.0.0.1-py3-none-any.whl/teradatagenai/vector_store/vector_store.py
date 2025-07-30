"""
Unpublished work.
Copyright (c) 2025 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: aanchal.kavedia@teradata.com
Secondary Owner: akhil.bisht@teradata.com

This file implements VectorStore class along with its method.
"""
import base64
import json, os, pandas as pd, time, re, glob
from json.decoder import JSONDecodeError
from teradataml.common.constants import HTTPRequest, TeradataConstants
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes
from teradataml.common.utils import UtilFuncs
from teradataml.context.context import _get_user
from teradataml import DataFrame, copy_to_sql, execute_sql
from teradataml.options.configure import configure
from teradataml.utils.validators import _Validators
from teradataml.scriptmgmt.UserEnv import _get_auth_token
from teradataml.utils.internal_buffer import _InternalBuffer
from teradatagenai.garbage_collector.garbage_collector import GarbageCollector

from teradatagenai.common.constants import VectorStoreURLs, _Grant, _Revoke, VSApi

# Getting VectorStoreURLs.
vector_store_urls = VectorStoreURLs()

class VSManager:
    """
    Vector store manager allows user to:
        * Perform health check for the vector store service.
        * List all the vector stores.
        * List all the active sessions of the vector store service.
        * List all available patterns for creating metadata-based vector store.
        * Disconnect from the database session.
    """
    log = False

    @classmethod
    def get_log(cls):
        """
        DESCRIPTION:
            Get the int representation of log which is required for the API calls.

        PARAMETERS:
            None

        RETURNS:
            int value required for API calls.

        RAISES:
            None

        EXAMPLES:
            >>> VSManager.get_log()
        """
        return 0 if not cls.log else 1

    @staticmethod
    def _connect(**kwargs):
        """
        DESCRIPTION:
            Establishes connection to Teradata Vantage.

        PARAMETERS:
             host:
                Optional Argument.
                Specifies the fully qualified domain name or IP address of the
                Teradata System to connect to.
                Types: str

            username:
                Optional Argument.
                Specifies the username for connecting to/create a vector
                store in Teradata Vantage.
                Types: str

            password:
                Optional Argument.
                Specifies the password required for the username.
                Types: str

            database:
                Optional Argument.
                Specifies the initial database to use after logon,
                instead of the user's default database.
                Types: str

        RETURNS:
            None

        RAISES:
            TeradataMlException

        EXAMPLES:
            from teradatagenai import VSManager
            # Example 1: Connect to the database using host, database,
            #            username and password.
            >>> VSManager._connect(host='<host>',
                                   username='<user>',
                                   password='<password>',
                                   database='<database>')
        """
        ## Initialize connection parameters.
        host = kwargs.get("host", None)
        user = kwargs.get("username", None)
        password = kwargs.get("password", None)
        database = kwargs.get("database", _get_user())

        # get the JWT token or basic authentication token in case of username
        # and password is passed.
        headers = _get_auth_token()

        # Validations
        arg_info_matrix = []
        arg_info_matrix.append(["host", host, True, (str), True])
        arg_info_matrix.append(["username", user, True, (str), True])
        arg_info_matrix.append(["password", password, True, (str), True])
        arg_info_matrix.append(["database", database, True, (str), True])

        if user and password:
            # Check if vector_store_base_url is set or not.
            _Validators._check_required_params(arg_value=configure._vector_store_base_url,
                                               arg_name="configure._vector_store_base_url",
                                               caller_func_name="_connect()",
                                               target_func_name="set_config_params")
        else:
            _Validators._check_required_params(arg_value=configure._vector_store_base_url,
                                               arg_name="Auth token",
                                               caller_func_name="VectorStore()",
                                               target_func_name="set_auth_token")

        # Validate argument types.
        _Validators._validate_function_arguments(arg_info_matrix)

        # Form the header with username and password if it is non ccp enabled
        # tenant when explictly _connect is called.
        if user and password:
            # If the host and user are passed, we will set the new connection params.
            credentials = f"{user}:{password}"
            # Encode the credentials string using Base64
            encoded_credentials = base64.b64encode(
                credentials.encode('utf-8')).decode('utf-8')
            # Form the Authorization header value
            headers = {"Authorization": f"Basic {encoded_credentials}"}

        # Triggering the 'connect' API
        data = {
            'database_name': database,
            'hostname': host
        }
        # Only add arguments which are not None as
        # service accepts only non None arguments.                                                                                                        
        data = {k: v for k, v in data.items() if v is not None}

        http_params = {
            "url": vector_store_urls.session_url,
            "method_type": HTTPRequest.POST,
            "headers": headers,
            "json": data,
            "verify": configure._ssl_verify
        }

        response = UtilFuncs._http_request(**http_params)

        session_id = response.cookies.get("session_id")
        # Only add the session id if it is not None,
        # meaning when connect went through.
        if session_id:
            _InternalBuffer.add(vs_session_id=session_id)
            _InternalBuffer.add(vs_header=headers)

        VectorStore._process_vs_response(api_name="connect", response=response)

    @staticmethod
    def _generate_session_id(**kwargs):
        """
        DESCRIPTION:
            Internal function to generate or get the session_id.

        PARAMETERS:
            generate:
                Optional Argument.
                Specifies whether to generate the session_id or not.
                In case of 'disconnect()`, we do not want to generate
                the session_id again in case it is called multiple times.
                Default Value: True
                Types: bool

        RETURNS:
            dict containing the headers and the session_id.

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> VSManager._generate_session_id()
        """
        # If the buffer is empty, meaning its the first call to
        # _connect, call _connect to generate the session id.
        if _InternalBuffer.get("vs_session_id") is None and kwargs.get("generate", True):
            VSManager._connect()
        # This is for cases when 'vs_session_id' is not stored in the buffer,
        # it should return None instead of returning a dict with None values.
        if _InternalBuffer.get("vs_session_id") is not None:
            return {"vs_session_id": _InternalBuffer.get("vs_session_id"),
                    "vs_header": _InternalBuffer.get("vs_header")}

    @staticmethod
    def list(**kwargs):
        """
        DESCRIPTION:
            Lists all the vector stores.
            Notes:
                * Lists all vector stores if user has admin role permissions.
                * Lists vector stores permitted to the user.

        RETURNS:
            teradataml DataFrame containing the vector store details.

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> from teradatagenai import VSManager

            # List all the vector stores.
            >>> VSManager.list()
        """
        # Triggering the 'list_vector_stores' API
        list_vs_url = vector_store_urls.vectorstore_url
        session_header = VSManager._generate_session_id()
        response = UtilFuncs._http_request(list_vs_url, HTTPRequest.GET,
                                           cookies={'session_id': session_header["vs_session_id"]},
                                           headers=session_header["vs_header"]
                                           )
        # Process the response and return the dataframe.
        if kwargs.get("return_type", "teradataml") == "json":
            return VectorStore._process_vs_response("list_vector_stores", response)['vector_stores_list']
        data = pd.DataFrame(VectorStore._process_vs_response("list_vector_stores", response)['vector_stores_list'])
        return VectorStore._convert_to_tdmldf(data)

    @staticmethod
    def health():
        """
        DESCRIPTION:
            Performs sanity check for the service.

        RETURNS:
            teradataml DataFrame containing details on the health of the service.

        RAISES:
            TeradataMlException

        EXAMPLES:
            # Example 1: Check the health of the service.
            >>> VSManager.health()
        """
        health_url = f'{vector_store_urls.base_url}health'
        session_header = VSManager._generate_session_id()
        response = UtilFuncs._http_request(health_url, HTTPRequest.GET,
                                           headers=session_header["vs_header"])
        data = pd.DataFrame([VectorStore._process_vs_response("health", response)])
        return VectorStore._convert_to_tdmldf(data)

    @staticmethod
    def list_sessions():
        """
        DESCRIPTION:
            Lists all the active sessions of the vector store service.
            Notes:
                * Only admin users can use this method.
                * Refer to the 'Admin Flow' section in the
                  User guide for details.
        RETURNS:
            teradataml DataFrame containing the active sessions.

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> from teradatagenai import VSManager

            # List all the vector stores.
            >>> VSManager.list_sessions()
        """
        session_header = VSManager._generate_session_id()
        response = UtilFuncs._http_request(f"{vector_store_urls.session_url}s",
                                           HTTPRequest.GET,
                                           cookies={'session_id': session_header["vs_session_id"]},
                                           headers=session_header["vs_header"]
                                           )
        result = _ListSessions(VectorStore._process_vs_response("list_sessions", response))
        return result

    @staticmethod
    def list_patterns():
        """
        DESCRIPTION:
            Lists all the patterns in the vector store.
            Notes:
                * Only admin users can use this method.
                * Refer to the 'Admin Flow' section in the
                  User guide for details.

        PARAMETERS:
            None

        RETURNS:
            teradataml DataFrame containing the patterns.

        RAISES:
            TeradataMlException

        EXAMPLES:
            from teradataml import VSManager

            # List all the patterns.
            VSManager.list_patterns()
        """
        session_header = VSManager._generate_session_id()
        response = UtilFuncs._http_request(f"{vector_store_urls.patterns_url}?log_level={VSManager.get_log()}",
                                           HTTPRequest.GET,
                                           cookies={'session_id': session_header["vs_session_id"]},
                                           headers=session_header["vs_header"]
                                           )
        data = pd.DataFrame(VectorStore._process_vs_response("list_patterns", response)['pattern_list'])
        return VectorStore._convert_to_tdmldf(data)

    @staticmethod
    def disconnect(session_id=None, raise_error=True):
        """
        DESCRIPTION:
            Databse session created for vector store operation is disconnected
            and corresponding underlying objects are deleted.
            Notes:
                * When 'session_id' argument is passed, only that session is
                  disconnected, else all session IDs created during the
                  current Python session are disconnected.
                * Only admin users can disconnect session
                  created by other users.
                * Refer to the 'Admin Flow' section in the
                  User guide for details.

        PARAMETERS:
            session_id:
                Optional Argument.
                Specifies the session ID to terminate.
                If not specified all the database sessions created
                in current Python session are terminated.
                Types: str

            raise_error:
                Optional Argument.
                Specifies a boolean flag that decides whether to raise error or not.
                Default Values: True
                Types: bool

        RETURNS:
            None

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> from teradatagenai import VSManager
            # Example 1: Disconnect from the database.
            # Create an instance of the VectorStore class.
            >>> vs = VectorStore(name="vec1")

            # Create a vector store.
            >>> vs.create(object_names="amazon_reviews_25",
                          description="vector store testing",
                          key_columns=['rev_id', 'aid'],
                          data_columns=['rev_text'],
                          vector_column='VectorIndex',
                          embeddings_model="amazon.titan-embed-text-v1")

            # Disconnect from the database.
            >>> VSManager.disconnect()
        """
        # Validations
        arg_info_matrix = []
        arg_info_matrix.append(["session_id", session_id, True, (str), True])
        arg_info_matrix.append(["raise_error", raise_error, True, (bool), True])

        # Validate argument types.
        _Validators._validate_function_arguments(arg_info_matrix)
        session_header = VSManager._generate_session_id(generate=False)
        if session_header is None:
            if raise_error:
                error_msg = Messages.get_message(MessageCodes.FUNC_EXECUTION_FAILED,
                                                 "disconnect",
                                                 "No active database session to disconnect.")
                raise TeradataMlException(error_msg, MessageCodes.FUNC_EXECUTION_FAILED)
            return

        if session_id:
            # Delete a user specified session.
            url = f"{vector_store_urls.session_url}s/{session_id}"
            update_internal_buffer = session_id == session_header["vs_session_id"]
            func_name = "terminate_session"
        else:
            # Delete the current active session.
            url = vector_store_urls.session_url
            update_internal_buffer = True
            func_name = "disconnect"

        response = UtilFuncs._http_request(url,
                                           HTTPRequest.DELETE,
                                           cookies={'session_id': session_header["vs_session_id"]},
                                           headers=session_header["vs_header"])
        VectorStore._process_vs_response(func_name, response, raise_error=raise_error)

        # Remove the session_id and header from the internal header.
        if update_internal_buffer and _InternalBuffer.get("vs_session_id"):
            _InternalBuffer.remove_key("vs_session_id")
            _InternalBuffer.remove_key("vs_header")

class _SimilaritySearch:
    """
    Internal class to create a similarity search object which is needed
    to display the results in a tabular format and at the same time store
    the json object which is used in prepare response.
    """
    def __init__(self, response, batch=False, **kwargs):
        """
        DESCRIPTION:
            Initializes the SimilaritySearch object.

        PARAMETERS:
            response:
                Required Argument.
                Specifies the response from the REST API.
                Types: dict

            batch:
                Optional Argument.
                Specifies whether the batch is enabled or not.
                Default Value: False
                Types: bool

            return_type:
                Optional Argument.
                Specifies the return type of similarity_search.
                By default returns a teradataml DataFrame.
                Permitted Values: "teradataml", "pandas", "json"
                Default Value: "teradataml"
                Types: str

        RETURNS:
            None

        RAISES:
            None
        """
        self.similar_objects_count = response['similar_objects_count']
        self._json_obj = response['similar_objects_list']
        return_type = kwargs.get('return_type')
        return_type = 'teradataml' if return_type is None else return_type.lower()
        __arg_info_matrix = [["return_type", return_type, False, str, True, ["teradataml", "pandas", "json"]]]
        # Make sure that a correct type of values has been supplied to the arguments.
        _Validators._validate_function_arguments(__arg_info_matrix)

        if return_type == "json":
            self.similar_objects = self._json_obj
        else:
            if batch:
                data = pd.DataFrame([
                {**item, "batch_id": batch_id} for batch_id, values in self._json_obj.items() for item in values
                ]).set_index("batch_id")
            else:
                data = pd.DataFrame(self._json_obj)
            self.similar_objects = VectorStore._convert_to_tdmldf(data, index=True) if return_type == "teradataml" else data

    def __repr__(self):
        return f"similar_objects_count:{self.similar_objects_count}\nsimilar_objects:\n{self.similar_objects})"

class _ListSessions:
    """
    Internal class to create a _ListSessions object which is needed
    to display the results in a readable format.
    """
    def __init__(self, response):
        self.total_active_sessions = response['count']
        self.current_session_id = response['self_session_id']
        # Currently copy_to does not support adding list into columns, hence the
        # list should be converted to str before giving it to copy_to
        response = pd.DataFrame(response['session_details'])
        response['vs_names'] = response['vs_names'].apply(lambda x: ','.join(map(str, x)))
        self.session_details = VectorStore._convert_to_tdmldf(pd.DataFrame(response))

    def __repr__(self):
        return f"total_active_sessions:{self.total_active_sessions}\n\ncurrent_session_id:\n{self.current_session_id}" \
               f"\n\nsession_details:\n{self.session_details}"

class VectorStore:
    def __init__(self,
                 name,
                 log=False,
                 **kwargs):
        """
        DESCRIPTION:
            VectorStore contains a vectorized version of data.
            The vectorization typically is a result of embeddings generated by
            an AI LLM.
            There are two types of vector stores based on the use cases:
                * Content-based vector store: A vector store built on the
                  contents of table/view/teradataml DataFrame.
                  The table can be formed from the contents of file / pdf.
                  Questions can be asked against the contents of the table and
                  top matches of relevant rows are returned based on search.
                  This can be followed by a textual response generated using
                  an LLM by manipulating the top matches.

                * Metadata-based vector store: A vector store built on the
                  metadata of a set of tables. Questions can be asked
                  against a table or set of tables and top table
                  matches are returned.
            Notes:
                * If the vector store mentioned in the name argument
                  already exists, it is initialized for use.
                * If not, user needs to call create() to create the same.

        PARAMETERS:
            name:
                Required Argument.
                Specifies the name of the vector store either to connect, if it
                already exists or to create a new vector store.
                Types: str

            log:
                Optional Argument.
                Specifies whether logging should be enabled for vector store
                methods.
                Note:
                    In case of any errors, by default it will be written
                    in datadog even if logging not enabled.
                Default Value: False
                Types: bool

        RETURNS:
            None

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> vs = VectorStore(name="vs", log=True)
        """
        # Initialize variables.
        self.name = name
        self._log = log

        # Validating name and log.
        arg_info_matrix = []
        arg_info_matrix.append(["name", self.name, False, (str), True])
        arg_info_matrix.append(["log", self._log, True, (bool)])

        # As the rest call accepts 0, 1 converting it.
        self._log = 0 if not self._log else 1

        _Validators._validate_missing_required_arguments(arg_info_matrix)
        # Validate argument types.
        _Validators._validate_function_arguments(arg_info_matrix)
        
        # Check if vector_store_base_url is set or not.
        _Validators._check_required_params(arg_value=configure._vector_store_base_url,
                                           arg_name="Auth token",
                                           caller_func_name="VectorStore()",
                                           target_func_name="set_auth_token")

        # Call connect in case of CCP enabled tenant.
        # If non-ccp, connect should be explicitly called passing the required params.
        session_header = VSManager._generate_session_id()
        self.__session_id = session_header["vs_session_id"]
        self.__headers = session_header["vs_header"]

        # Create all the REST API urls.
        self.__url = f'{vector_store_urls.vectorstore_url}/{self.name}'
        self.__common_url = f'{self.__url}?log_level={self._log}'
        self.__list_user_permission_url = f'{vector_store_urls.base_url}permissions/{self.name}'
        self.__similarity_search_url = '{0}/similarity-search?question={1}&log_level={2}'

        self.__prepare_response_url = f'{self.__url}/prepare-response?log_level={self._log}'
        self.__ask_url = f'{self.__url}/ask?log_level={self._log}'
        self.__set_user_permissions_url = "{0}permissions/{1}?user_name={2}&action={3}&permission={4}&log_level={5}"
        self.__get_objects_url = f"{self.__url}?get_object_list=true&log_level={self._log}"
        self.__get_details_url = f"{self.__url}?get_details=true&log_level={self._log}"
        self.__batch_url = '{0}/{1}?log_level={2}'

        # Check if the vector store exists by calling the list API and validating for the name.
        try:
            vs_list = VSManager.list(return_type="json")
        except Exception as e:
            if 'No authorized vector stores found for the user' in str(e):
                vs_list = pd.DataFrame(columns=["vs_name", "description", "target_database"])
            else:
                raise e

        vs_dict = {vs['vs_name']: vs for vs in vs_list}  # Convert list to dictionary for faster lookup

        # Check for the name in the dict.
        if self.name in vs_dict:
            vs = vs_dict[self.name]
            # If status does not contain keyword 'FAILED' and Vector Store is there in
            # the dict, then initialize it for the session
            if 'FAILED' not in vs['vs_status']:
                print(f"Vector store {self.name} is initialized for the session.")
            else:
                # This means some operation failed and hence print which operation failed.
                print(f"Vector Store {self.name} has status '{vs['vs_status']}'. Take the appropriate action before moving ahead.")
        else:
            # Otherwise, it does not exists and guide the user to create it.
            print(f"Vector Store {self.name} does not exist. Call create() to create the same.")

    # TODO: https://teradata-pe.atlassian.net/browse/ELE-7518
    def get_objects(self):
        """
        DESCRIPTION:
            Get the list of objects in the metadata-based vector store.

        PARAMETERS:
            None

        RETURNS:
            teradataml DataFrame containing the list of objects.

        RAISES:
            TeradataMlException

        EXAMPLES:
            # Create an instance of the VectorStore class.
            >>> vs = VectorStore(name="vs")

            # Example: Get the list of objects that are used for creating the vector store.
            >>> vs.get_objects()
        """
        response = UtilFuncs._http_request(self.__get_objects_url, HTTPRequest.GET,
                                           headers=self.__headers,
                                           cookies={'session_id': self.__session_id})

        data = VectorStore._process_vs_response("get_objects", response)
        return VectorStore._convert_to_tdmldf(pd.DataFrame(data['object_list']))

    def get_details(self):
        """
        DESCRIPTION:
            Get details of the vector store.
            Details include embeddings model, search algorithm
            and any other details which the user has setup while
            creating or updating the vector store.

        PARAMETERS:
            None

        RETURNS:
            teradataml DataFrame containing the details.

        RAISES:
            TeradataMlException

        EXAMPLES:
            # Create an instance of the VectorStore 'vs'
            # which already exists.
            >>> vs = VectorStore(name="vs")

            # Example: Get details of a vector store.
            >>> vs.get_details()
        """
        response = UtilFuncs._http_request(self.__get_details_url, HTTPRequest.GET,
                                           headers=self.__headers,
                                           cookies={'session_id': self.__session_id})

        data = VectorStore._process_vs_response("get_details", response)
        return VectorStore._convert_to_tdmldf(pd.DataFrame([data]))

    def __set_vs_index_and_vs_parameters(self, create=True, **kwargs):
        """
        DESCRIPTION:
            Internal function to set the parameters for the vector store.
            Keeping it common, as it will be required by update and initialize
            methods.

        PARAMETERS:
            create:
                Optional Argument.
                Specifies whether call is from create or update function.
                Default Value: True
                Types: bool

            kwargs:
                Optional Argument.
                Specifies keyword arguments required for creating/updating vector store.
        RAISES:
            None

        EXAMPLES:
            >>> self.__set_vs_index_and_vs_parameters(key_columns="a",
                                                      create=False)
        """
        ## Initializing vs_index params
        self._target_database = kwargs.get('target_database', None)
        self._object_names = kwargs.get('object_names', None)
        self._key_columns = kwargs.get('key_columns', None)
        self._data_columns = kwargs.get('data_columns', None)
        self._vector_column = kwargs.get('vector_column', None)
        self._chunk_size = kwargs.get("chunk_size", None)
        self._optimized_chunking = kwargs.get('optimized_chunking', None)
        self._header_height = kwargs.get('header_height', None)
        self._footer_height = kwargs.get('footer_height', None)
        self._include_objects = kwargs.get('include_objects', None)
        self._exclude_objects = kwargs.get('exclude_objects', None)
        self._include_patterns = kwargs.get('include_patterns', None)
        self._exclude_patterns = kwargs.get('exclude_patterns', None)
        self._sample_size = kwargs.get('sample_size', None)
        self._alter_operation = kwargs.get('alter_operation', None)
        self._update_style = kwargs.get('update_style', None)
        # TODO specific to nim. Add it in documentation when service exposes it.
        self._nv_ingestor = kwargs.get('nv_ingestor', False if create else None)
        self._display_metadata = kwargs.get('display_metadata', False if create else None)
        self._extract_text = kwargs.get('extract_text', None)
        self._extract_images = kwargs.get('extract_images', None)
        self._extract_tables = kwargs.get('extract_tables', None)

        # TODO ELE-6025: Bug in Feb drop for these arguments, hence commented them.
        # self._acronym_objects = kwargs.get('acronym_objects', None)
        # self._acronym_objects_global = kwargs.get('acronym_objects_global', None)
        # self._acronym_files_global = kwargs.get('acronym_files_global', None)

        ## Initializing vs_parameters
        self._description = kwargs.get("description", None)
        self._embeddings_model = kwargs.get("embeddings_model", None)
        self._embeddings_dims = kwargs.get("embeddings_dims", None)
        self._metric = kwargs.get("metric", None)
        self._search_algorithm = kwargs.get("search_algorithm", None)
        self._top_k = kwargs.get("top_k", None)
        self._search_threshold = kwargs.get("search_threshold", None)
        self._initial_centroids_method = kwargs.get("initial_centroids_method", None)
        self._train_numcluster = kwargs.get("train_numcluster", None)
        self._max_iternum = kwargs.get("max_iternum", None)
        self._stop_threshold = kwargs.get("stop_threshold", None)
        self._seed = kwargs.get("seed", None)
        self._num_init = kwargs.get("num_init", None)
        self._search_numcluster = kwargs.get("search_numcluster", None)
        self._prompt = kwargs.get("prompt", None)
        self._document_files = kwargs.get("document_files", None)
        self._chat_completion_model = kwargs.get("chat_completion_model", None)
        self._ef_search = kwargs.get("ef_search", None)
        self._num_layer = kwargs.get("num_layer", None)
        self._ef_construction = kwargs.get("ef_construction", None)
        self._num_connpernode = kwargs.get("num_connpernode", None)
        self._maxnum_connpernode = kwargs.get("maxnum_connpernode", None)
        self._apply_heuristics = kwargs.get("apply_heuristics", None)
        self._rerank_weight = kwargs.get("rerank_weight", None)
        self._relevance_top_k = kwargs.get("relevance_top_k", None)
        self._relevance_search_threshold = kwargs.get("relevance_search_threshold", None)
        # TODO: ELE-6018
        # self._batch = kwargs.get("batch", None)
        self._ignore_embedding_errors = kwargs.get("ignore_embedding_errors", None)
        # TODO specific to nim. Add it in documentation when service exposes it.
        self._chat_completion_max_tokens = kwargs.get("chat_completion_max_tokens", None)
        self._embeddings_base_url = kwargs.get("emdeddings_base_url", None)
        self._completions_base_url = kwargs.get("completions_base_url", None)
        self._ranking_base_url = kwargs.get("ranking_base_url", None)
        self._ingest_host = kwargs.get("ingest_host", None)
        self._ranking_model = kwargs.get("ranking_model", None)
        self._ingest_port = kwargs.get("ingest_port", None)

        # Validating vs_index
        arg_info_matrix = []
        arg_info_matrix.append(["target_database", self._target_database, True, (str), True])
        arg_info_matrix.append(["object_names", self._object_names, True, (str, DataFrame, list), True])
        arg_info_matrix.append(["key_columns", self._key_columns, True, (str, list), True])
        arg_info_matrix.append(["data_columns", self._data_columns, True, (str, list), True])
        arg_info_matrix.append(["vector_column", self._vector_column, True, (str), True])
        arg_info_matrix.append(["chunk_size", self._chunk_size, True, (int), True])
        arg_info_matrix.append(["optimized_chunking", self._optimized_chunking, True, (bool), True])
        arg_info_matrix.append(["header_height", self._header_height, True, (int), True])
        arg_info_matrix.append(["footer_height", self._footer_height, True, (int), True])
        arg_info_matrix.append(["extract_text", self._extract_text, True, (bool), True])
        arg_info_matrix.append(["extract_images", self._extract_images, True, (bool), True])
        arg_info_matrix.append(["extract_tables", self._extract_tables, True, (bool), True])
        # TODO ELE-4937 check if this is str or DataFrame.
        arg_info_matrix.append(["include_objects", self._include_objects, True, (str, DataFrame, list), True])
        arg_info_matrix.append(["exclude_objects", self._exclude_objects, True, (str, DataFrame, list), True])
        arg_info_matrix.append(["include_patterns", self._include_patterns, True, (VSPattern, list), True])
        arg_info_matrix.append(["exclude_patterns", self._exclude_patterns, True, (VSPattern, list), True])
        arg_info_matrix.append(["sample_size", self._sample_size, True, (int), True])
        arg_info_matrix.append(["nv_ingestor", self._nv_ingestor, True, (bool), True])
        arg_info_matrix.append(["display_metadata", self._display_metadata, True, (bool), True])
        arg_info_matrix.append(["alter_operation", self._alter_operation, True, (str), True])
        arg_info_matrix.append(["update_style", self._update_style, True, (str), True])

        # TODO ELE-6025: Bug in Feb drop for these arguments, hence commented them.
        # arg_info_matrix.append(["acronym_objects", self._acronym_objects, True, (str, list), True])
        # arg_info_matrix.append(["acronym_objects_global", self._acronym_objects_global, True, (bool, list), True])
        # arg_info_matrix.append(["acronym_files_global", self._acronym_files_global, True, (bool, list), True])

        # Validating vs_parameters
        arg_info_matrix.append(["description", self._description, True, (str), True])
         # embeddings_model has default values, hence making optional.
        arg_info_matrix.append(["embeddings_model", self._embeddings_model, True, (str), True])
        arg_info_matrix.append(["embeddings_dims", self._embeddings_dims, True, (int), True])
        arg_info_matrix.append(["metric", self._metric, True, (str), True])
        arg_info_matrix.append(["search_algorithm", self._search_algorithm, True, (str), True])
        arg_info_matrix.append(["top_k", self._top_k, True, (int), True])
        arg_info_matrix.append(["initial_centroids_method", self._initial_centroids_method, True, (str),
                                True])
        arg_info_matrix.append(["train_numcluster", self._train_numcluster, True, (int), True])
        arg_info_matrix.append(["max_iternum", self._max_iternum, True, (int), True])
        arg_info_matrix.append(["stop_threshold", self._stop_threshold, True, (float), True])
        arg_info_matrix.append(["seed", self._seed, True, (int), True])
        arg_info_matrix.append(["num_init", self._num_init, True, (int), True])
        arg_info_matrix.append(["search_threshold", self._search_threshold, True, (float), True])
        arg_info_matrix.append(["search_numcluster", self._search_numcluster, True, (int), True])
        arg_info_matrix.append(["prompt", self._prompt, True, (str), True])
        arg_info_matrix.append(["chat_completion_model", self._chat_completion_model, True, (str),
                                True])
        arg_info_matrix.append(["document_files", self._document_files, True, (str, list),
                                True])
        arg_info_matrix.append(["ef_search", self._ef_search, True, (int), True])
        arg_info_matrix.append(["num_layer", self._num_layer, True, (int), True])
        arg_info_matrix.append(["ef_construction", self._ef_construction, True, (int), True])
        arg_info_matrix.append(["num_connpernode", self._num_connpernode, True, (int), True])
        arg_info_matrix.append(["maxnum_connpernode", self._maxnum_connpernode, True, (int), True])
        arg_info_matrix.append(["apply_heuristics", self._apply_heuristics, True, (bool), True])
        arg_info_matrix.append(["rerank_weight", self._rerank_weight, True, (float), True])
        arg_info_matrix.append(["relevance_top_k", self._relevance_top_k, True, (int), True])
        arg_info_matrix.append(["relevance_search_threshold", self._relevance_search_threshold, True, (float), True])
        # TODO: ELE-6018
        #arg_info_matrix.append(["batch", self._batch, True, (bool), True])
        arg_info_matrix.append(["ignore_embedding_errors", self._ignore_embedding_errors, True, (bool), True])
        arg_info_matrix.append(["chat_completion_max_tokens", self._chat_completion_max_tokens, True, (int), True])
        arg_info_matrix.append(["emdeddings_base_url", self._embeddings_base_url, True, (str), True])
        arg_info_matrix.append(["completions_base_url", self._completions_base_url, True, (str), True])
        arg_info_matrix.append(["ranking_base_url", self._ranking_base_url, True, (str), True])
        arg_info_matrix.append(["ingest_host", self._ingest_host, True, (str), True])
        arg_info_matrix.append(["ranking_model", self._ranking_model, True, (str), True])
        arg_info_matrix.append(["ingest_port", self._ingest_port, True, (int), True])

        # Validate required arguments.
        _Validators._validate_missing_required_arguments(arg_info_matrix)
        # Validate argument types.
        _Validators._validate_function_arguments(arg_info_matrix)

        # Forming document files structure as the API accepts:
        # Input document files structure is: [fully_qualified_file_name1,
        #                                     fully_qualified_file_name2]
        # document_files = [('document_files', ('file1.pdf',
        #                    open('/location/file1.pdf', 'rb'),
        #                    'application/pdf')),
        #                   ('document_files', ('file2.pdf',
        #                    open('/location/file2.pdf', 'rb'),
        #                    'application/pdf'))
        #                   ]
        if self._document_files:
            # Normalize input to a list
            if isinstance(self._document_files, str):
                self._document_files = [self._document_files]

            resolved_files = []
            for path in self._document_files:
                files = []
                # Wildcard pattern
                if any(char in path for char in ['*', '?']):
                    files = glob.glob(path, recursive= "**" in path)
                # Directory path
                elif os.path.isdir(path):
                    for root , _, filenames in os.walk(path):
                        files.extend(os.path.join(root , f) for f in filenames)
                # Single file path
                else:
                    files = [path]

                # Filter valid PDF files
                pdfs = [f for f in files if os.path.isfile(f)]
                resolved_files.extend(pdfs)

            self._document_files = []
            # Get the file name from fully qualified path
            for file in resolved_files:
                file_name = os.path.basename(file)
                # Form the string 'application/pdf' based on the file extension.
                file_type = f"application/{os.path.splitext(file_name)[1]}".replace(".", "")
                file_handle = open(file, 'rb')
                self._document_files.append(('document_files', (file_name, file_handle, file_type)))
                # Register the file handle with the GarbageCollector.
                GarbageCollector.add_open_file(file_handle)
        # TODO ELE-6025: Bug in Feb drop for these arguments, hence commented them.
        # Will reuse again in April drop.
        # if self._acronym_objects:
        #     acronym_objects = self._acronym_objects
        #     self._acronym_objects = []

        #     for file in acronym_objects:
        #         # Get the file name from fully qualified path
        #         file_name = os.path.basename(file)
        #         # Form the string 'application/pdf' based on the file extension.
        #         file_type = f"application/{os.path.splitext(file_name)[1]}".replace(".", "")
        #         self._acronym_objects.append(('acronym_objects', (file_name,
        #                                                         open(file, 'rb'),
        #                                                         file_type)))

        expected_parameters = ["include_objects", "exclude_objects", "include_patterns", "exclude_patterns"]
        if any(param in list(kwargs.keys()) for param in expected_parameters):
            error_str = f"Required configuration is not available for creating metadata-based" \
                        f" vector store. Do not use the following parameters: {', '.join(expected_parameters)} " \
                        f"while creating/updating the vector store"
            error_msg = Messages.get_message(MessageCodes.FUNC_EXECUTION_FAILED,
                                             "create/update", error_str)
            try:
                op_query1 = execute_sql("SHOW TYPE SYSUDTLIB.Signature;").fetchall()
                op_query2 = execute_sql("SELECT UDFS.Signature_Version();").fetchall()
                if "CREATE TYPE SYSUDTLIB.Signature AS VARBYTE(61440) FINAL" \
                        not in op_query1[0][0] or \
                        "Signature: V0.8.2 Compiled on 'Dec 12 2024 05:35:04'" \
                        not in op_query2[0][0]:

                    raise TeradataMlException(error_msg, MessageCodes.FUNC_EXECUTION_FAILED)
            except Exception as e:
                raise TeradataMlException(error_msg, MessageCodes.FUNC_EXECUTION_FAILED)
        # Extracting pattern names from include_patterns and exclude_patterns
        if self._include_patterns is not None:     
            include_patterns = []
            for pattern in UtilFuncs._as_list(self._include_patterns):
                include_patterns.append(pattern._pattern_name)
            self._include_patterns = include_patterns

        if self._exclude_patterns is not None:
            exclude_patterns = []
            for pattern in UtilFuncs._as_list(self._exclude_patterns):
                exclude_patterns.append(pattern._pattern_name)
            self._exclude_patterns = exclude_patterns

        vs_parameters = {"description": self._description,
                         "embeddings_model": self._embeddings_model,
                         "embeddings_dims": self._embeddings_dims,
                         "metric": self._metric,
                         "search_algorithm": self._search_algorithm,
                         "top_k": self._top_k,
                         "initial_centroids_method": self._initial_centroids_method,
                         "train_numcluster": self._train_numcluster,
                         "max_iternum": self._max_iternum,
                         "stop_threshold": self._stop_threshold,
                         "seed": self._seed,
                         "num_init": self._num_init,
                         "search_threshold": self._search_threshold,
                         "search_numcluster": self._search_numcluster,
                         "prompt": self._prompt,
                         "chat_completion_model": self._chat_completion_model,
                         "ef_search": self._ef_search,
                         "num_layer": self._num_layer,
                         "ef_construction": self._ef_construction,
                         "num_connPerNode": self._num_connpernode,
                         "maxNum_connPerNode": self._maxnum_connpernode,
                         "apply_heuristics": self._apply_heuristics,
                         "rerank_weight": self._rerank_weight,
                         "relevance_top_k": self._relevance_top_k,
                         "relevance_search_threshold": self._relevance_search_threshold,
                         # TODO: ELE-6018
                         #"batch": self._batch,
                         "ignore_embedding_errors": self._ignore_embedding_errors,
                         "chat_completion_max_tokens": self._chat_completion_max_tokens,
                         "base_url_embeddings": self._embeddings_base_url,
                         "base_url_completions": self._completions_base_url,
                         "base_url_ranking": self._ranking_base_url,
                         "doc_ingest_host": self._ingest_host,
                         "nim_ranking_model": self._ranking_model,
                         "doc_ingest_port": self._ingest_port}

        # Only add keys with non-None values
        self.__vs_parameters = {k: v for k, v in vs_parameters.items() if v is not None}
        if self._object_names is not None:
            self._object_names = UtilFuncs._as_list(self._object_names)
            self._object_names = list(map(lambda obj: obj._table_name.replace("\"", "")
                                          if _Validators._check_isinstance(obj, DataFrame) 
                                          else obj, self._object_names))
        vs_index = {
            'target_database': self._target_database,
            'object_names': self._object_names,
            'key_columns': self._key_columns,
            'data_columns': self._data_columns,
            'vector_column': self._vector_column,
            'chunk_size': self._chunk_size,
            'optimized_chunking': self._optimized_chunking,
            'header_height': self._header_height,
            'footer_height': self._footer_height,
            'include_objects': self._include_objects,
            'exclude_objects': self._exclude_objects,
            'include_patterns': self._include_patterns,
            'exclude_patterns': self._exclude_patterns,
            'sample_size': self._sample_size,
            'alter_operation': self._alter_operation,
            'update_style': self._update_style,
            'nv_ingestor': self._nv_ingestor,
            'display_metadata': self._display_metadata,
            'extract_text': self._extract_text,
            'extract_images': self._extract_images,
            'extract_tables': self._extract_tables
        }

        # TODO ELE-6025: Bug in Feb drop for these arguments, hence commented them.
        # 'acronym_objects': self._acronym_objects,
        # 'acronym_objects_global': self._acronym_objects_global,
        # 'acronym_files_global': self._acronym_files_global

        # Only add keys with non-None values
        self.__vs_index = {k: v for k, v in vs_index.items() if v is not None}

    def create(self, **kwargs):
        """
        DESCRIPTION:
            Creates a new vector store.
            Once vector store is created, it is initialized for use.
            If vector store already exists, error is raised.
            Notes:
                * Only admin users can use this method.
                * Refer to the 'Admin Flow' section in the
                  User guide for details.

        PARAMETERS:
            description:
                Optional Argument.
                Specifies the description of the vector store.
                Types: str

            target_database:
                Optional Argument.
                Specifies the database name where the vector store is created.
                When "document_files" is passed, it refers to the database where
                the file content splits are stored.
                Note:
                    If not specified, vector store is created in the database
                    which is in use.
                Types: str

            object_names:
                Required for 'content-based vector store', Optional otherwise.
                Specifies the table name(s)/teradataml DataFrame(s) to be indexed for
                vector store. Teradata recommends to use teradataml DataFrame as input.
                Notes:
                    * For content-based vector store:
                        * Multiple tables/views can be passed in object_names.
                        * If the table is in another database than
                          the database in use, make sure to pass in
                          the fully qualified name or a DataFrame object.
                          For example,
                            * If the table_name is 'amazon_reviews' and it is
                              under 'oaf' database which is not the user's
                              logged in database,
                                * Either pass in str as 'oaf.amazon_reviews' or
                                * DataFrame(in_schema('oaf', 'amazon_reviews'))
                        * If multiple tables/views are passed, each table should
                          have the columns which are mentioned in "data_columns"
                          and "key_columns".
                        * When document_files are used, only one name should be
                          specified to be used for file content splits.
                    * For metadata-based vector store:
                        * Use "include_objects" or
                          "include_patterns" parameters instead of "object_names".
                    * When "target_database" is not set, and only table name is passed to
                      "object_names", then the input is searched in default database.
                Types: str or list of str or DataFrame

            key_columns:
                Optional Argument.
                Specifies the name(s) of the key column(s) to be used for indexing.
                Note:
                    * When "document_files" is used, this parameter is not needed.
                    * In case of multiple input files, a single key column
                      containing the file names are generated.
                Types: str, list of str

            data_columns:
                Optional Argument.
                Specifies the name(s) of the data column(s) to be used
                for embedding generation(vectorization).
                Note:
                    * When multiple data columns are specified, data is unpivoted
                      to get a new key column "AttributeName" and a single data column
                      "AttributeValue".
                    * For document_files, it refers to the column name where the
                      file content splits will be stored.
                Types: str, list of str

            vector_column:
                Optional Argument.
                Specifies the name of the column to be used for storing
                the embeddings.
                Default Value: vector_index
                Types: str

            chunk_size:
                Optional Argument.
                Specifies the size of each chunk when dividing document files
                into chunks.
                Note:
                    Applicable only when "document_files" are specified.
                Default Value: 512
                Types: int

            optimized_chunking:
                Optional Argument.
                Specifies whether an optimized splitting mechanism supplied by
                Teradata should be used.
                The documents are parsed internally in an intelligent fashion
                based on file structure and chunks are dynamically created
                based on section layout.
                Notes:
                    * The "chunk_size" field is not applicable when
                      "optimized_chunking" is set to True.
                    *  Applicable only for "document_files".
                Default Value: True
                Types: bool

            header_height:
                Optional Argument.
                Specifies the height (in points) of the header section of a PDF
                document to be trimmed before processing the main content.
                This is useful for removing unwanted header information
                from each page of the PDF.
                Recommended value is 55.
                Default Value: 0
                Types: int

            footer_height:
                Optional Argument.
                Specifies the height (in points) of the footer section of a PDF
                document to be trimmed before processing the main content.
                This is useful for removing unwanted footer information from
                each page of the PDF.
                Recommended value is 55.
                Default Value: 0
                Types: int

            embeddings_model:
                Required Argument.
                Specifies the embeddings model to be used for generating the
                embeddings.
                Default Values:
                    * AWS: amazon.titan-embed-text-v2:0
                    * Azure: text-embedding-3-small                                                                                                                 
                Permitted Values:
                    * AWS
                        * amazon.titan-embed-text-v1
                        * amazon.titan-embed-image-v1
                        * amazon.titan-embed-text-v2:0
                    * Azure
                        * text-embedding-ada-002
                        * text-embedding-3-small
                        * text-embedding-3-large
                Types: str

            embeddings_dims:
                Optional Argument.
                Specifies the number of dimensions to be used for generating the embeddings.
                The value depends on the "embeddings_model".
                Permitted Values:
                    AWS:
                        * amazon.titan-embed-text-v1: 1536
                        * amazon.titan-embed-image-v1: [256, 384, 1024]
                        * amazon.titan-embed-text-v2:0: [256, 512, 1024]
                    Azure:
                        * text-embedding-ada-002: 1536 only
                        * text-embedding-3-small: 1 <= dims <= 1536
                        * text-embedding-3-large: 1 <= dims <= 3072
                Default Value:
                    AWS:
                        * amazon.titan-embed-text-v1: 1536
                        * amazon.titan-embed-image-v1: 1024
                        * amazon.titan-embed-text-v2:0: 1024
                    Azure:
                        * text-embedding-ada-002: 1536
                        * text-embedding-3-small: 1536
                        * text-embedding-3-large: 3072
                Types: str

            metric:
                Optional Argument.
                Specifies the metric to be used for calculating the distance
                between the vectors.
                Permitted Values:
                    * EUCLIDEAN
                    * COSINE
                    * DOTPRODUCT
                Default Value: EUCLIDEAN
                Types: str

            search_algorithm:
                Optional Argument.
                Specifies the algorithm to be used for searching the
                tables and views relevant to the question.
                Permitted Values: VECTORDISTANCE, KMEANS, HNSW.
                Default Value: VECTORDISTANCE
                Types: str

            initial_centroids_method:
                Optional Argument.
                Specifies the algorithm to be used for initializing the
                centroids.
                Note:
                    Applicable when "search_algorithm" is 'KMEANS'.
                Permitted Values: RANDOM, KMEANS++
                Default Value: RANDOM
                Types: str

            train_numcluster:
                Optional Argument.
                Specifies the number of clusters to be trained.
                Note:
                    Applicable when "search_algorithm" is 'KMEANS'.
                Types: int

            max_iternum:
                Optional Argument.
                Specifies the maximum number of iterations to be run during
                training.
                Note:
                    Applicable when "search_algorithm" is 'KMEANS'.
                Permitted Values: [1-2147483647]
                Default Value: 10
                Types: int

            stop_threshold:
                Optional Argument.
                Specifies the threshold value at which training should be
                stopped.
                Note:
                    Applicable when "search_algorithm" is 'KMEANS'.
                Default Value: 0.0395
                Types: float

            seed:
                Optional Argument.
                Specifies the seed value to be used for random number
                generation.
                Note:
                    Applicable when "search_algorithm" is 'KMEANS'.
                Permitted Values: [0-2147483647]
                Default Value: 0
                Types: int

            num_init:
                Optional Argument.
                Specifies the number of times the k-means algorithm should
                run with different initial centroid seeds.
                Permitted Values: [1-2147483647]
                Default Value: 1
                Types: int

            top_k:
                Optional Argument.
                Specifies the number of top clusters to be considered while searching.
                Permitted Values: [1-1024]
                Default Value: 10
                Types: int

            search_threshold:
                Optional Argument.
                Specifies the threshold value to consider for matching tables/views
                while searching.
                A higher threshold value limits responses to the top matches only.
                Note:
                    Applicable when "search_algorithm" is 'VECTORDISTANCE' and 'KMEANS'.
                Types: float

            search_numcluster:
                Optional Argument.
                Specifies the number of clusters to be considered while
                searching.
                Note:
                    Applicable when "search_algorithm" is 'KMEANS'.
                Types: int

            prompt:
                Optional Argument.
                Specifies the prompt to be used by language model
                to generate responses using top matches.
                Types: str

            chat_completion_model:
                Optional Argument.
                Specifies the name of the chat completion model to be used for
                generating text responses.
                Permitted Values:
                    AWS:
                        * anthropic.claude-3-haiku-20240307-v1:0
                        * anthropic.claude-instant-v1
                        * anthropic.claude-3-5-sonnet-20240620-v1:0
                    Azure:
                        gpt-35-turbo-16k
                Default Value:
                    AWS: anthropic.claude-3-haiku-20240307-v1:0
                    Azure: gpt-35-turbo-16k
                Types: str

            document_files:
                Optional Argument.
                Specifies the input dataset in document files format.
                It can be used to specify input documents in file format.
                A directory path or wildcard pattern can also be specified
                The files are processed internally, converted to chunks and stored
                into a database table.
                Alternatively, users can choose to chunk their files themselves,
                store them into a database table, create a table and specify
                the details of that using "target_database", "object_names",
                "data_columns" where the file content splits are stored.
                Notes:
                    * Only PDF format is currently supported.
                    * Multiple document files can be supplied.
                    * Fully qualified file name should be specified.
                Examples:
                    Example 1 : Multiple files specified within a list
                    >>> document_files=['file1.pdf','file2.pdf']

                    Example 2 : Path to the directory containing pdf files 
                    >>> document_files = "/path/to/pdfs"

                    Example 3 : Path to directory containing pdf files as a wildcard string
                    >>> document_files = "/path/to/pdfs/*.pdf"

                    Example 4 : Path to directory containing pdf files and subdirectory of pdf files
                    >>> document_files = "/path/to/pdfs/**/*.pdf
                Types: str, list

            ef_search:
                Optional Argument.
                Specifies the number of neighbors to be considered during search
                in HNSW graph.
                Note:
                    Applicable when "search_algorithm" is 'HNSW'.
                Permitted Values: [1-1024]
                Default Value: 32
                Types: int

            num_layer:
                Optional Argument.
                Specifies the maximum number of layers for the HNSW graph.
                Note:
                    Applicable when "search_algorithm" is 'HNSW'.
                Permitted Values: [1-1024]
                Types: int

            ef_construction:
                Optional Argument.
                Specifies the number of neighbors to be considered during
                construction of the HNSW graph.
                Applicable when "search_algorithm" is 'HNSW'.
                Permitted Values: [1-1024]
                Default Value: 32
                Types: int

            num_connpernode:
                Optional Argument.
                Specifies the number of connections per node in the HNSW graph
                during construction.
                Note:
                    Applicable when "search_algorithm" is 'HNSW'.
                Permitted Values: [1-1024]
                Default Value: 32
                Types: int

            maxnum_connpernode:
                Optional Argument.
                Specifies the maximum number of connections per node in the
                HNSW graph during construction.
                Note:
                    Applicable when "search_algorithm" is 'HNSW'.
                Default Value: 32
                Permitted Values: [1-1024]
                Types: int

            apply_heuristics:
                Optional Argument.
                Specifies whether to apply heuristics optimizations during construction
                of the HNSW graph.
                Applicable when "search_algorithm" is 'HNSW'.
                Default Value: True
                Types: bool

            include_objects:
                Optional Argument.
                Specifies the list of tables and views included 
                in the metadata-based vector store.
                Types: str or list of str or DataFrame
            
            exclude_objects:
                Optional Argument.
                Specifies the list of tables and views excluded from 
                the metadata-based vector store.
                Types: str or list of str or DataFrame

            sample_size:
                Optional Argument.
                Specifies the number of rows to sample from tables and views 
                for the metadata-based vector store embeddings.
                Default Value: 20
                Types: int

            rerank_weight:
                Optional Argument.
                Specifies the weight to be used for reranking the search results.
                Applicable range is 0.0 to 1.0.
                Default Value: 0.2
                Types: float

            relevance_top_k:
                Optional Argument.
                Specifies the number of top similarity matches to be considered for reranking.
                Applicable range is 1 to 1024.
                Permitted Values: [1-1024]
                Default Value: 60
                Types: int

            relevance_search_threshold:
                Optional Argument.
                Specifies the threshold value to consider matching tables/views while reranking.
                A higher threshold value limits responses to the top matches only.
                Types: float

            include_patterns:
                Optional Argument.
                Specifies the list of patterns to be included in the metadata-based vector store.
                Types: VSPattern or list of VSPattern

            exclude_patterns:
                Optional Argument.
                Specifies the list of patterns to be excluded from the metadata-based vector store.
                Types: VSPattern or list of VSPattern

            batch:
                Optional Argument.
                Specifies whether to use batch processing for embedding generation.
                Note:
                    Applicable only for AWS.
                Default Value: False
                Types: bool

            ignore_embedding_errors:
                Optional Argument.
                Specifies whether to ignore errors during embedding generation.
                Note:
                    Applicable only for AWS.
                Default Value: False
                Types: bool
            
            chat_completion_max_tokens:
                Optional Argument.
                Specifies the maximum number of tokens to be generated by the chat completion model.
                Permitted Values: [1-16384]
                Default Value: 16384
                Types: int

            emdeddings_base_url:
                Optional Argument.
                Specifies the base URL for the service which is used for generating embeddings.
                Types: str

            completions_base_url:
                Optional Argument.
                Specifies the base URL for the service which is used for generating completions.
                Types: str

            ranking_url:
                Optional Argument.
                Specifies the URL for the service which is used for reranking.
                Types: str

            ingest_host:
                Optional Argument.
                Specifies the HTTP host to be used for document parsing.
                Types: str

            ingest_port:
                Optional Argument.
                Specifies the port to be used for document parsing.
                Default Value: 7670
                Types: int

        RETURNS:
            Pandas DataFrame containing status of create operation.

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> from teradatagenai import VectorStore

            # Create an instance of the VectorStore class.
            >>> vs = VectorStore(name="vec1")

            # Example 1: Create a content based vector store for the data
            #            in table 'amazon_reviews_25'.
            #            Use 'amazon.titan-embed-text-v1' embedding model for
            #            creating vector store.
            >>> vs.create(object_names="amazon_reviews_25",
                          description="vector store testing",
                          target_database='oaf',
                          key_columns=['rev_id', 'aid'],
                          data_columns=['rev_text'],
                          vector_column='VectorIndex',
                          embeddings_model="amazon.titan-embed-text-v1")

            # Example 2: Create a content based vector store for the data
            #            in DataFrame 'df'.
            #            Use 'amazon.titan-embed-text-v1' embedding model for
            #            creating vector store.
            >>> from teradataml import DataFrame
            >>> df = DataFrame("amazon_reviews_25")
            >>> vs = VectorStore('vs_example_2') 
            >>> vs.create(object_names=df,
                          description="vector store testing",
                          target_database='oaf',
                          key_columns=['rev_id', 'aid'],
                          data_columns=['rev_text'],
                          vector_column='VectorIndex',
                          embeddings_model="amazon.titan-embed-text-v1")

            # Example 3: Create a content based vector store for the data
            #            in 'SQL_Fundamentals.pdf' file.
            #            Use 'amazon.titan-embed-text-v1' embedding model
            #            for creating vector store.

            # Get the absolute path for 'SQL_Fundamentals.pdf' file.
            >>> import teradatagenai
            >>> files= [os.path.join(os.path.dirname(teradatagenai.__file__), "example-data",
                                 "SQL_Fundamentals.pdf")]
            >>> vs = VectorStore('vs_example_3')
            >>> vs.create(object_names="amazon_reviews_25",
                          description="vector store testing",
                          target_database='oaf',
                          key_columns=['rev_id', 'aid'],
                          data_columns=['rev_text'],
                          vector_column='VectorIndex',
                          embeddings_model="amazon.titan-embed-text-v1"
                          document_files=files)

            # Example 4: Create a content based vector store of all PDF files
            #            in a directory by passing the directory path
            #            Use 'amazon.titan-embed-text-v1' embedding model
            #            for creating vector store.

            # Get the absolute path of the directory.
            >>> files= "/path/to/pdfs"
            >>> vs = VectorStore('vs_example_4')
            >>> vs.create(object_names="amazon_reviews_25",
                          description="vector store testing",
                          target_database='oaf',
                          data_columns=['rev_text'],
                          vector_column='VectorIndex',
                          embeddings_model="amazon.titan-embed-text-v1"
                          document_files=files)

            # Example 5: Create a content based vector store of all PDF files
            #            in a directory by passing the path as a wildcard
            #            Use 'amazon.titan-embed-text-v1' embedding model
            #            for creating vector store.

            # Pass the wildcard pattern containing the pdf files
            >>> files= "/path/to/pdfs/*.pdf"
            >>> vs = VectorStore('vs_example_5')
            >>> vs.create(object_names="amazon_reviews_25",
                          description="vector store testing",
                          target_database='oaf',
                          data_columns=['rev_text'],
                          vector_column='VectorIndex',
                          embeddings_model="amazon.titan-embed-text-v1"
                          document_files=files)

        """
        # Set the vs_index and vs_parameters
        self.__set_vs_index_and_vs_parameters(**kwargs)

        # Form the data to be passed to the API
        data = {}
        if self.__vs_parameters or self.__vs_index:
            data = {}
            if self.__vs_parameters:
                data['vs_parameters'] = json.dumps(self.__vs_parameters)
            if self.__vs_index:
                data['vs_index'] = json.dumps(self.__vs_index)
        # Form the http_params
        http_params = {
            "url": self.__common_url,
            "method_type": HTTPRequest.POST,
            "headers": self.__headers,
            "data": data,
            "files": self._document_files,
            "cookies": {'session_id': self.__session_id}
        }
        # Call the 'create' API
        response = UtilFuncs._http_request(**http_params)
        # Process the response
        self._process_vs_response("create", response) 
        self.__display_status_check_message()

    def destroy(self):
        """
        DESCRIPTION:
            Destroys the vector store.
            Notes:
                * Only admin users can use this method.
                * Refer to the 'Admin Flow' section in the
                  User guide for details.

        PARAMETERS:
            None

        RETURNS:
            teradataml DataFrame containing status of destroy operation.

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> from teradatagenai import VectorStore

            # Create an instance of the VectorStore class.
            >>> vs = VectorStore(name="vec1")

            # Example 1: Create a content based vector store for the data
            #            in table 'amazon_reviews_25'.
            #            Use 'amazon.titan-embed-text-v1' embedding model for
            #            creating vector store.

            # Note this step is not needed if vector store already exists.
            >>> vs.create(object_names="amazon_reviews_25",
                          description="vector store testing",
                          target_database='oaf',
                          key_columns=['rev_id', 'aid'],
                          data_columns=['rev_text'],
                          vector_column='VectorIndex',
                          embeddings_model="amazon.titan-embed-text-v1")

            # Destroy the Vector Store.
            >>> vs.destroy()
        """
        response = UtilFuncs._http_request(self.__common_url, HTTPRequest.DELETE,
                                           headers=self.__headers,
                                           cookies={'session_id': self.__session_id})
        self._process_vs_response("destroy", response)
        self.__display_status_check_message()

    def update(self, **kwargs):
        """
        DESCRIPTION:
            Updates an existing vector store with the specified parameters.
            Notes:
                * Addition of new data and deletion of existing data
                  stored in table/view(s) is possible using
                  "alter_operation" and "update_style".
                * Updating when input data is present in pdf files is not supported.
                * Only admin users can use this method.
                * Refer to the 'Admin Flow' section in the
                  User guide for details.

        PARAMETERS:
            description:
                Optional Argument.
                Specifies the description of the vector store.
                Types: str

            embeddings_model:
                Required Argument.
                Specifies the embeddings model to be used for generating the
                embeddings.
                Default Values:
                    * AWS: amazon.titan-embed-text-v2:0
                    * Azure: text-embedding-3-small
                Permitted Values:
                    * AWS
                        * amazon.titan-embed-text-v1
                        * amazon.titan-embed-image-v1
                        * amazon.titan-embed-text-v2:0
                    * Azure
                        * text-embedding-ada-002
                        * text-embedding-3-small
                        * text-embedding-3-large
                Types: str

            embeddings_dims:
                Optional Argument.
                Specifies the number of dimensions to be used for generating the embeddings.
                The value depends on the "embeddings_model".
                Permitted Values:
                    * AWS
                        * amazon.titan-embed-text-v1: 1536
                        * amazon.titan-embed-image-v1: [256, 384, 1024]
                        * amazon.titan-embed-text-v2:0: [256, 512, 1024]
                    * Azure
                        * text-embedding-ada-002: 1536 only
                        * text-embedding-3-small: 1 <= dims <= 1536
                        * text-embedding-3-large: 1 <= dims <= 3072
                Types: int

            metric:
                Optional Argument.
                Specifies the metric to be used for calculating the distance
                between the vectors.
                Permitted Values:
                    * EUCLIDEAN
                    * COSINE
                    * DOTPRODUCT
                Types: str

            search_algorithm:
                Optional Argument.
                Specifies the algorithm to be used for searching the tables and
                views relevant to the question.
                Permitted Values: VECTORDISTANCE, KMEANS, HNSW.
                Types: str

            chat_completion_model:
                Optional Argument.
                Specifies the name of the chat completion model to be used for
                generating text responses.
                Permitted Values:
                    AWS:
                        * anthropic.claude-3-haiku-20240307-v1:0
                        * anthropic.claude-instant-v1
                        * anthropic.claude-3-5-sonnet-20240620-v1:0
                    Azure:
                        gpt-35-turbo-16k
                Default Value:
                    AWS: anthropic.claude-3-haiku-20240307-v1:0
                    Azure: gpt-35-turbo-16k
                Types: str

            initial_centroids_method:
                Optional Argument.
                Specifies the Algorithm to be used for initializing the
                centroids.
                Note:
                    Applicable when "search_algorithm" is 'KMEANS'.
                Permitted Values: RANDOM, KMEANS++
                Types: str

            train_numcluster:
                Optional Argument.
                Specifies the number of clusters to be trained.
                Note:
                    Applicable when "search_algorithm" is 'KMEANS'.
                Permitted Values: [2-33553920]
                Types: int

            max_iternum:
                Optional Argument.
                Specifies the maximum number of iterations to be run during
                training.
                Note:
                    Applicable when "search_algorithm" is 'KMEANS'.
                Permitted Values: [1-2147483647]
                Types: int

            stop_threshold:
                Optional Argument.
                Specifies the threshold value at which training should be
                stopped.
                Note:
                    * Applicable when "search_algorithm" is 'KMEANS'.
                    * Should be >= 0.0
                Types: int

            seed:
                Optional Argument.
                Specifies the seed value to be used for random number
                generation.
                Note:
                    Applicable when "search_algorithm" is 'KMEANS'.
                Permitted Values: [0-2147483647]
                Types: int

            num_init:
                Optional Argument.
                Specifies the number of times the k-means algorithm will
                be run with different initial centroid seeds.
                Note:
                    Applicable when "search_algorithm" is 'KMEANS'.
                Permitted Values: [0-2147483647]
                Types: int

            top_k:
                Optional Argument.
                Specifies the number of top clusters to be considered while searching.
                Permitted Values: [1-1024]
                Types: int

            search_threshold:
                Optional Argument.
                Specifies the threshold value to consider matching tables/views
                while searching.
                A higher threshold value limits responses to the top matches only.
                Note:
                    * Applicable when "search_algorithm" is 'VECTORDISTANCE'
                      or 'KMEANS'.
                Types: float

            search_numcluster:
                Optional Argument.
                Specifies the number of clusters to be considered while
                searching.
                Notes:
                    Applicable when "search_algorithm" is 'KMEANS'.
                Types: int

            prompt:
                Optional Argument.
                Specifies the prompt to be used for generating answers.
                Types: str

            document_files:
                Optional Argument.
                Specifies the list of PDF files to be divided into chunks and
                used for document embedding.
                Types: tuple, list of tuple

            ef_search:
                Optional Argument.
                Specifies the number of neighbors to be considered during search
                in HNSW graph.
                Note:
                    Applicable when "search_algorithm" is 'HNSW'.
                Permitted Values: [1-1024]
                Default Value: 32
                Types: int

            num_layer:
                Optional Argument.
                Specifies the maximum number of layers for the HNSW graph.
                Note:
                    Applicable when "search_algorithm" is 'HNSW'.
                Types: int

            ef_construction:
                Optional Argument.
                Specifies the number of neighbors to be considered during
                construction of the HNSW graph.
                Note:
                    Applicable when "search_algorithm" is 'HNSW'.
                Permitted Values: [1-1024]
                Default Value: 32
                Types: int

            num_connpernode:
                Optional Argument.
                Specifies the number of connections per node in the HNSW graph
                during construction.
                Note:
                    Applicable when "search_algorithm" is 'HNSW'.
                Permitted Values: [1-1024]
                Default Value: 32
                Types: int

            maxnum_connpernode:
                Optional Argument.
                Specifies the maximum number of connections per node in the
                HNSW graph during construction.
                Note:
                    Applicable when "search_algorithm" is 'HNSW'.
                Default Value: 32
                Types: int

            apply_heuristics:
                Optional Argument.
                Specifies whether to apply heuristics optimizations during construction
                of the HNSW graph.
                Note:
                    Applicable when "search_algorithm" is 'HNSW'.
                Default Value: True
                Types: bool

            include_objects:
                Optional Argument.
                Specifies the list of tables and views to be included in the
                metadata-based vector store.
                Types: str or list of str or DataFrame

            exclude_objects:
                Optional Argument.
                Specifies the list of tables and views to be excluded from the
                metadata-based vector store.
                Types: str or list of str or DataFrame

            sample_size:
                Optional Argument.
                Specifies the number of rows to sample from tables and views
                for the metadata-based vector store embeddings.
                Default Value: 20
                Types: int

            rerank_weight:
                Optional Argument.
                Specifies the weight to be used for reranking the search results.
                Applicable range is 0.0 to 1.0.
                Default Value: 0.2
                Types: float

            relevance_top_k:
                Optional Argument.
                Specifies the number of top similarity matches to be considered for reranking.
                Permitted Values: [1-1024]
                Default Value: 60
                Types: int

            relevance_search_threshold:
                Optional Argument.
                Specifies the threshold value to consider matching tables/views while reranking.
                A higher threshold value limits responses to the top matches only.
                Types: float

            include_patterns:
                Optional Argument.
                Specifies the list of patterns to be included in the metadata-based vector store.
                Types: VSPattern or list of VSPattern

            exclude_patterns:
                Optional Argument.
                Specifies the list of patterns to be excluded from the metadata-based vector store.
                Types: VSPattern or list of VSPattern

            target_database:
                Optional Argument.
                Specifies the database name where the vector store is created.
                When "document_files" is passed, it refers to the database where
                the file content splits are stored.
                Note:
                    * If not specified, vector store is created in the database
                      which is in use.
                Types: str

            alter_operation:
                Optional Argument.
                Specifies the type of operation to be performed while adding new data or
                deleting existing data from the vector store.
                Permitted Values: ADD, DROP
                Types: str

            update_style:
                Optional Argument.
                Specifies the style to be used for "alter_operation" of the data
                from the vector store when "search_algorithm" is KMEANS/HNSW.
                Permitted Values:
                    * MINOR: Involves building the index with only the new data which is added/deleted.
                    * MAJOR: Involves building the entire index again with the entire data including
                             the data which was added/deleted.
                Default Value: MINOR
                Types: str

            object_names:
                Required for 'content-based vector store', Optional otherwise.
                Specifies the table name(s)/teradataml DataFrame(s) to be indexed for
                vector store. Teradata recommends to use teradataml DataFrame as input.
                Notes:
                    * For content-based vector store:
                        * Multiple tables/views can be passed in object_names.
                        * If the table is in another database than
                          the database in use, make sure to pass in
                          the fully qualified name or a DataFrame object.
                          For example,
                            * If the table_name is 'amazon_reviews' and it is
                              under 'oaf' database which is not the user's
                              logged in database,
                                * Either pass in str as 'oaf.amazon_reviews' or
                                * DataFrame(in_schema('oaf', 'amazon_reviews'))
                        * If multiple tables/views are passed, each table should
                          have the columns which are mentioned in "data_columns"
                          and "key_columns".
                        * When document_files are used, only one name should be
                          specified to be used for file content splits.
                    * For metadata-based vector store:
                        * Use "include_objects" or
                          "include_patterns" parameters instead of "object_names".
                    * When "target_database" is not set, and only table name is passed to
                      "object_names", then the input is searched in default database.
                Types: str or list of str or DataFrame

            ignore_embedding_errors:
                Optional Argument.
                Specifies whether to ignore errors during embedding generation.
                Types: bool
                Default Value: False

            chat_completion_max_tokens:
                Optional Argument.
                Specifies the maximum number of tokens to be generated by the chat completion model.
                Permitted Values: [1-16384]
                Default Value: 16384
                Types: int

        RETURNS:
            teradataml DataFrame containing status of update operation.

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> from teradatagenai import VectorStore

            # Create an instance of the VectorStore class.
            >>> vs = VectorStore(name="vec1")

            # Create the Vector Store.
            # Note this step is not needed if vector store already exists.
            >>> vs.create(object_names="amazon_reviews_25",
                          description="vector store testing",
                          key_columns=['rev_id', 'aid'],
                          data_columns=['rev_text'],
                          vector_column='VectorIndex',
                          embeddings_model="amazon.titan-embed-text-v1"
                          )

            # Example 1: Update the search_algorithm, search_threshold and
            #            description of the Vector Store.
            >>> vs.update(search_algorithm='KMEANS',
                          search_threshold=0.6,
                          description='KMeans clustering method')
            
            # Example 2: Add the object_names of the content-based Vector Store using
            #            alter_operation and update_style.
            >>> vs = VectorStore(name="vs_update")
            >>> vs.create(embeddings_model= 'amazon.titan-embed-text-v1',
                          chat_completion_model= 'anthropic.claude-instant-v1',
                          search_algorithm= 'HNSW',
                          seed=10,
                          top_k=10,
                          ef_construction=32,
                          num_connpernode=32,
                          maxnum_connpernode=32,
                          metric='EUCLIDEAN',
                          apply_heuristics=True,
                          ef_search=32,
                          object_names= 'amazon_reviews_25',
                          key_columns= ['rev_id', 'aid'],
                          data_columns= ['rev_text'],
                          vector_column= 'VectorIndex')

            >>> vs.update(object_names='amazon_reviews_10_alter',
                          alter_operation="ADD",
                          update_style="MINOR")

            # Example 3: Delete the object_names of the content-based Vector Store using
            #            alter_operation and update_style.
            >>> vs.update(object_names='amazon_reviews_25',
                          alter_operation="DELETE",
                          update_style="MAJOR")
        """
        self.__set_vs_index_and_vs_parameters(**kwargs, create=False)

        if self.__vs_parameters or self.__vs_index:
            data = {}
            if self.__vs_parameters:
                data['vs_parameters'] = json.dumps(self.__vs_parameters)
            if self.__vs_index:
                data['vs_index'] = json.dumps(self.__vs_index)


        response = UtilFuncs._http_request(self.__common_url,
                                           HTTPRequest.PATCH,
                                           data=data,
                                           files=self._document_files,
                                           headers=self.__headers,
                                           cookies={'session_id': self.__session_id})
        self._process_vs_response("update", response)
        self.__display_status_check_message()

    def similarity_search(self, 
                          question=None,
                          **kwargs):
        """
        DESCRIPTION:
            Performs similarity search in the Vector Store for the input question.
            The algorithm specified in "search_algorithm" is used to perform
            the search against the vector store.
            The result contains "top_k" rows along with similarity score
            found by the "search_algorithm".

        PARAMETERS:
            question:
                Required Argument, Optional for batch mode.
                Specifies a string of text for which similarity search
                needs to be performed.
                Types: str

            batch_data:
                Required for batch mode.
                Specifies the table name or teradataml DataFrame to be indexed for batch mode.
                Types: str, teradataml DataFrame
            
            batch_id_column:
                Required for batch mode.
                Specifies the ID column to be indexed for batch mode.
                Types: str

            batch_query_column:
                Required for batch mode.
                Specifies the query column to be indexed for batch mode.
                Types: str

            return_type:
                Optional Argument.
                Specifies the return type of similarity_search.
                Permitted Values: "teradataml", "pandas", "json"
                Default Value: "teradataml"
                Types: str

        RETURNS:
            list

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> from teradatagenai import VectorStore

            # Create an instance of the VectorStore class.
            >>> vs = VectorStore(name="vs")

            # Create a Vector Store.

            # Note this step is not needed if vector store already exists.
            >>> vs.create(object_names="amazon_reviews_25",
                          description="vector store testing",
                          key_columns=['rev_id', 'aid'],
                          data_columns=['rev_text'],
                          vector_column='VectorIndex',
                          embeddings_model="amazon.titan-embed-text-v1",
                          search_algorithm='VECTORDISTANCE',
                          top_k=10
                          )

            # Example 1: Perform similarity search in the Vector Store for
            #            the input question.
            >>> question = 'Are there any reviews about books?'
            >>> response = vs.similarity_search(question=question)

            Example 2: Perform batch similarity search in the Vector Store.
            # Create an instance of the VectorStore class.
            >>> vs = VectorStore(name="vs_batch")

            # Creates a Vector Store.
            # Note this step is not needed if vector store already exists.
            >>> vs.create(embeddings_model="amazon.titan-embed-text-v1",
                          embeddings_dims=2048,
                          chat_completion_model="anthropic.claude-3-haiku-20240307-v1:0",
                          search_algorithm="HNSW",
                          top_k=10,
                          object_names="valid_passages",
                          key_columns="pid",
                          data_columns="passage",
                          vector_column="VectorIndex")

            # Perform batch similarity search in the Vector Store.
            >>> response = vs.similarity_search(batch_data="valid_passages",
                                                batch_id_column="pid",
                                                batch_query_column="passage")

            # Retrieve the batch similarity results.
            from teradatagenai import VSApi
            >>> similarity_results = vs.get_batch_result(api_name=VSApi.SimilaritySearch)

        """
        # Check if batch mode is enabled
        batch = self.__batch_mode_args_validation(**kwargs)

        if batch:
            # Post request for batch similarity search
            response = UtilFuncs._http_request(self.__batch_url.format(self.__url,
                                                                       'similarity-search-batch',
                                                                       self._log),
                                               HTTPRequest.POST,
                                               headers=self.__headers,
                                               json=self.__set_batch_index,
                                               cookies={'session_id': self.__session_id})
            self._process_vs_response(api_name="similarity-search-batch", response=response)
            self.__display_status_check_message(batch)
            return
        else:

            # Initializing params
            self._question = question

            # Validating params
            arg_info_matrix = []
            arg_info_matrix.append(["question", self._question, False, (str), True])
            _Validators._validate_missing_required_arguments(arg_info_matrix)

            # Validate argument types.
            _Validators._validate_function_arguments(arg_info_matrix)

            response = UtilFuncs._http_request(self.__similarity_search_url.format(self.__url,
                                                                                   question,
                                                                                   self._log),
                                               HTTPRequest.POST,
                                               headers=self.__headers,
                                               cookies={'session_id': self.__session_id})

            return _SimilaritySearch(self._process_vs_response(api_name="similarity-search",
                                                               response=response),
                                     return_type=kwargs.get("return_type"))

    def prepare_response(self,
                         similarity_results,
                         question=None,
                         prompt=None,
                         **kwargs):
        """
        DESCRIPTION:
            Prepare a natural language response to the user using the input
            question and similarity_results provided by
            VectorStore.similarity_search() method.
            The response is generated by a language model configured
            in the environment using a pre-configured prompt.
            An optional parameter prompt can be used to specify a customized
            prompt that replaces the internal prompt.

        PARAMETERS:
            question:
                Required Argument, Optional for batch mode.
                Specifies a string of text for which similarity search
                needs to be performed.
                Types: str

            similarity_results:
                Required Argument.
                Specifies the similarity results obtained by similarity_search().
                Types: str

            prompt:
                Optional Argument.
                Specifies a customized prompt that replaces the internal prompt.
                Types: str
            
            batch_data:
                Required for batch mode.
                Specifies the table name or teradataml DataFrame to be indexed for batch mode.
                Types: str, teradataml DataFrame

            batch_id_column:
                Required for batch mode.
                Specifies the ID column to be indexed for batch mode.
                Types: str

            batch_query_column:
                Required for batch mode.
                Specifies the query column to be indexed for batch mode.
                Types: str

        RETURNS:
            HTTP Response json.

        RAISES:
            TypeError, TeradataMlException

        EXAMPLES:
            # Create an instance of the VectorStore class.
            >>> vs = VectorStore(name="vs")

            # Creates a Vector Store.
            # Note this step is not needed if vector store already exists.
            >>> vs.create(object_names="amazon_reviews_25",
                          description="vector store testing",
                          key_columns=['rev_id', 'aid'],
                          data_columns=['rev_text'],
                          vector_column='VectorIndex',
                          embeddings_model="amazon.titan-embed-text-v1",
                          search_algorithm='VECTORDISTANCE',
                          top_k = 10
                          )

            # Perform similarity search in the Vector Store for
            # the input question.
            >>> question = 'Are there any reviews about books?'
            >>> response = vs.similarity_search(question=question)

            # Example 1: Prepare a natural language response to the user
            #            using the input question and similarity_results
            #            provided by similarity_search().

            question='Did any one feel the book is thin?'
            similar_objects_list = response['similar_objects_list']
            >>> vs.prepare_response(question=question,
                                    similarity_results=similar_objects_list)

            # Example 2: Perform batch similarity search in the Vector Store.
            # Create an instance of the VectorStore class.
            >>> vs = VectorStore(name="vs_batch")

            # Creates a Vector Store.
            # Note this step is not needed if vector store already exists.
            >>> vs.create(embeddings_model="amazon.titan-embed-text-v1",
                          embeddings_dims=2048,
                          chat_completion_model="anthropic.claude-3-haiku-20240307-v1:0",
                          search_algorithm="HNSW",
                          top_k=10,
                          object_names="valid_passages",
                          key_columns="pid",
                          data_columns="passage",
                          vector_column="VectorIndex")

            # Perform batch similarity search in the Vector Store.
            >>> vs.similarity_search(batch_data="valid_passages",
                                     batch_id_column="pid",
                                     batch_query_column="passage")

            # Get the similarity results.
            from teradatagenai import VSApi
            >>> similar_objects_list = vs.get_batch_result(api_name=VSApi.SimilaritySearch)

            # Perform batch prepare response.
            >>> vs.prepare_response(similarity_results=similar_objects_list,
                                    batch_data="valid_passages",
                                    batch_id_column="pid",
                                    batch_query_column="passage")
            
            # Retrieve the batch prepare response.
            >>> similarity_results = vs.get_batch_result(api_name=VSApi.PrepareResponse)

        """ 

        # Initializing params
        self._question = question
        self._similarity_results = similarity_results
        self._prompt = prompt
        # Check if batch mode is enabled
        batch = self.__batch_mode_args_validation(**kwargs)

        # Validating params
        arg_info_matrix = []
        arg_info_matrix.append(["similarity_results", self._similarity_results, False, _SimilaritySearch, True])
        arg_info_matrix.append(["prompt", self._prompt, True, (str), True])

        # Non-batch mode params
        if not batch:
            arg_info_matrix.append(["question", self._question, False, (str), True])

        _Validators._validate_missing_required_arguments(arg_info_matrix)

        # Explicitly checking similarity search API, as correct message is not displayed.
        if not isinstance(similarity_results, _SimilaritySearch):
            raise TypeError(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE,
                                                 "similarity_results", "output of similarity_search()"))
        # Validate argument types.
        _Validators._validate_function_arguments(arg_info_matrix)

        # data for prepare response
        data = {'similar_objects': self._similarity_results._json_obj,
                'prompt': self._prompt}
        
        # Prepare response in batch mode
        if batch:
            data['batch_input_index'] = self.__set_batch_index
            api_name = "prepare-response-batch"
            url = self.__batch_url.format(self.__url, api_name, self._log)
        else:
            # Non-batch mode
            api_name = "prepare-response"
            data['question'] = self._question
            url = self.__prepare_response_url

        # POST request for prepare response
        response = UtilFuncs._http_request(url, 
                                           HTTPRequest.POST,
                                           headers=self.__headers,
                                           cookies={'session_id': self.__session_id},
                                           json=data)
        
        response = self._process_vs_response(api_name=api_name, response=response)
        if batch:
            self.__display_status_check_message(batch)
            return
        return response


    def ask(self, 
            question=None,
            prompt=None,
            **kwargs):
        """
        DESCRIPTION:
            Performs similarity search in the vector store for
            the input question followed by preparing a natural
            language response to the user. This method combines
            the operation of similarity_search() and prepare_response()
            into one call for faster response time.

        PARAMETERS:
            question:
                Required Argument, Optional for batch mode.
                Specifies a string of text for which similarity search
                needs to be performed.
                Types: str

            prompt:
                Optional Argument.
                Specifies a customized prompt that replaces the internal prompt.
                Types: str

            batch_data:
                Required for batch mode.
                Specifies the table name or teradataml DataFrame to be indexed for batch mode.
                Types: str, teradataml DataFrame

            batch_id_column:
                Required for batch mode.
                Specifies the ID column to be indexed for batch mode.
                Types: str

            batch_query_column:
                Required for batch mode.
                Specifies the query column to be indexed for batch mode.
                Types: str

        RETURNS:
            dict

        RAISES:
            TeradataMlException

        EXAMPLES:
            # Create an instance of the VectorStore class.
            >>> vs = VectorStore(name="vs")

            # Create a Vector Store.

            # Note this step is not needed if vector store already exists.
            >>> vs.create(object_names="amazon_reviews_25",
                          description="vector store testing",
                          key_columns=['rev_id', 'aid'],
                          data_columns=['rev_text'],
                          vector_column='VectorIndex',
                          embeddings_model="amazon.titan-embed-text-v1",
                          search_algorithm='VECTORDISTANCE',
                          top_k=10
                          )

            >>> custom_prompt = '''List good reviews about the books. Do not assume information.
                                Only provide information that is present in the data.
                                Format results like this:
                                Review ID:
                                Author ID:
                                Review:
                                '''
            # Example 1: Perform similarity search in the Vector Store for
            #            the input question followed by preparing a natural
            #            language response to the user.

            >>> question = 'Are there any reviews saying that the books are inspiring?'
            >>> response = vs.ask(question=question, prompt=custom_prompt)

            # Example 2: Perform batch similarity search in the Vector Store.
            # Create an instance of the VectorStore class.
            >>> vs = VectorStore(name="vs_batch")

            # Create a Vector Store.
            >>> vs.create(embeddings_model="amazon.titan-embed-text-v1",
                          embeddings_dims=2048,
                          chat_completion_model="anthropic.claude-3-haiku-20240307-v1:0",
                          search_algorithm="HNSW",
                          top_k=10,
                          object_names="valid_passages",
                          key_columns="pid",
                          data_columns="passage",
                          vector_column="VectorIndex")

            # Perform batch similarity search in the Vector Store.
            >>> prompt = "Structure the response briefly in 1-2 lines."
            >>> vs.ask(batch_data="home_depot_train",
                       batch_id_column="product_uid",
                       batch_query_column="search_term",
                       prompt=prompt)

            # Retrieve the batch ask results.
            from teradatagenai import VSApi
            >>> ask_results = vs.get_batch_result(api_name=VSApi.Ask)

        """
        # Initializing params
        self._question = question
        self._prompt = prompt
        # Validating batch mode arguments
        batch = self.__batch_mode_args_validation(**kwargs)

        # Validating params
        arg_info_matrix = []

        # Non-batch mode params
        if not batch: 
            arg_info_matrix.append(["question", self._question, False, (str), True])
        arg_info_matrix.append(["prompt", self._prompt, True, (str), True])
        _Validators._validate_missing_required_arguments(arg_info_matrix)

        # Validate argument types.
        _Validators._validate_function_arguments(arg_info_matrix)

        # Data for ask
        data = {'prompt': self._prompt}

        # Ask in batch mode
        if batch:
            # Data for batch mode
            data['batch_input_index'] = self.__set_batch_index
            api_name = "ask-batch"
            url = self.__batch_url.format(self.__url, api_name, self._log)
        else:
            # Non-batch mode
            data['question'] = self._question
            api_name = "ask"
            url = self.__ask_url

        # POST request for ask
        response = UtilFuncs._http_request(url,
                                           HTTPRequest.POST,
                                           headers=self.__headers,
                                           cookies={'session_id': self.__session_id},
                                           json=data)
        
        response = self._process_vs_response(api_name=api_name, response=response)
        if batch:
            self.__display_status_check_message(batch)
            return
        return response
        
    
    @property
    def __set_batch_index(self):
        """ Set the batch index for the batch APIs. """
        return {"batch_input_table": self._batch_data,
                "batch_input_id_column": self._batch_id_column,
                "batch_input_query_column": self._batch_query_column
                }
    
    def __batch_mode_args_validation(self, **kwargs):
        """
        DESCRIPTION:
            Internal method to validate the batch mode and batch arguments.

        PARAMETERS:
            batch_data:
                Required Argument for batch mode.
                Specifies the table name/teradataml DataFrame to be indexed for batch mode.
                Types: str, teradataml DataFrame

            batch_id_column:
                Required Argument for batch mode.
                Specifies the ID column to be indexed for batch mode.
                Types: str

            batch_query_column:
                Required Argument for batch mode.
                Specifies the query column to be indexed for batch mode.
                Types: str

        RETURNS:
            bool

        RAISES:
            TeradataMlException
        
        """
        # Check if any batch argument is available
        if len(kwargs) == 0:
            return False

        # initialize the batch arguments
        self._batch_data = kwargs.get('batch_data', None)
        self._batch_id_column = kwargs.get('batch_id_column', None)
        self._batch_query_column = kwargs.get('batch_query_column', None)

        # Check if any batch argument is available
        if any([self._batch_data, self._batch_id_column, self._batch_query_column]):

            # Validate batch arguments
            arg_info_matrix = []
            arg_info_matrix.append(["batch_data", self._batch_data, False, (str, DataFrame), True])
            arg_info_matrix.append(["batch_id_column", self._batch_id_column, False, (str), True])
            arg_info_matrix.append(["batch_query_column", self._batch_query_column, False, (str), True])
            _Validators._validate_missing_required_arguments(arg_info_matrix)

            # Validate argument types.
            _Validators._validate_function_arguments(arg_info_matrix)

            # Check if batch_data is not a string or not
            # if not, extract the table name string from the TeradataMl DataFrame
            if not isinstance(self._batch_data, str):
                self._batch_data = self._batch_data._table_name.replace("\"", "")

            return True
        
        return False
    
    def __display_status_check_message(self, batch=False):
        """ 
        DESCRIPTION:
            Internal method to display the status check message for Vector Store operations.

        PARAMETERS:
            batch:
                Optional Argument.
                Specifies whether to display the message for batch apis.
                Default Value: False
                Types: bool

        RETURNS:
            None

        RAISES:
            None

        EXAMPLES:
            # Display the status check message.
            >>> self.__display_status_check_message(batch=True)
        """
        print("Use the 'status()' api to check the status of the operation.")
        if batch:
            print("Use the 'get_batch_result()' api to retrieve the batch result.")

    def get_batch_result(self, api_name, **kwargs):
        """
        DESCRIPTION:
            Retrieves the batch result for the specified API.
            The API name can be one of the following:   
                * similarity-search
                * prepare-response
                * ask
            Applicable only for batch mode operations.

        PARAMETERS:
            api_name:
                Required Argument.
                Specifies the name of the API.
                Permitted Values:
                    * VSApi.SimilaritySearch
                    * VSApi.PrepareResponse
                    * VSApi.Ask
                Types: Enum(VSApi)

        RETURNS:
            * Pandas DataFrame containing the batch result for ask, prepare_response.
            * SimilaritySearch object for similarity_search.

        RAISES:
            TeradataMlException

        EXAMPLES:
            # Create an instance of the VectorStore class.
            >>> vs = VectorStore(name="vs")

            # Create a Vector Store.
            # Note this step is not needed if vector store already exists.
            >>> vs.create(embeddings_model="amazon.titan-embed-text-v1",
                          embeddings_dims=2048,
                          chat_completion_model="anthropic.claude-3-haiku-20240307-v1:0",
                          search_algorithm="HNSW",
                          top_k=10,
                          object_names="valid_passages",
                          key_columns="pid",
                          data_columns="passage",
                          vector_column="VectorIndex")

            # Perform batch similarity search in the Vector Store.
            >>> vs.similarity_search(batch_data="home_depot_train",
                                     batch_id_column="product_uid",
                                     batch_query_column="search_term")

            from teradatagenai import VSApi
            # Get the batch result for the similarity_search API.
            >>> res = vs.get_batch_result(api_name=VSApi.SimilaritySearch)

            # Perform batch prepare_response in the Vector Store.
            >>> prompt= "Structure response in question-answering format
                         Question: 
                         Answer:"
            >>> vs.prepare_response(batch_data="home_depot_train",
                                    batch_id_column="product_uid",
                                    batch_query_column="search_term",
                                    prompt=prompt)
            # Get the batch result for the prepare_response API.
            >>> res = vs.get_batch_result(api_name=VSApi.PrepareResponse)

            # Perform batch ask in the Vector Store.
            >>> vs.ask(batch_data="home_depot_train",
                       batch_id_column="product_uid",
                       batch_query_column="search_term",
                       prompt=prompt)
            # Get the batch result for the ask API.
            >>> res = vs.get_batch_result(api_name=VSApi.Ask)

        """
        # Initializing params
        self._api_name = api_name

        # Validating params
        arg_info_matrix = []
        arg_info_matrix.append(["api_name", self._api_name, False, (VSApi)])

        # Validate argument types.
        _Validators._validate_function_arguments(arg_info_matrix)

        response = UtilFuncs._http_request(self.__batch_url.format(self.__url, 
                                                                   f"{self._api_name.value}-batch",
                                                                   self._log),
                                           HTTPRequest.GET,
                                           headers=self.__headers,
                                           cookies={'session_id': self.__session_id})
        
        if self._api_name.value == "similarity-search":
            return _SimilaritySearch(self._process_vs_response(self._api_name.value, response), batch=True,
                                     return_type=kwargs.get("return_type"))
        else:
            data = self._process_vs_response(self._api_name.value, response)
            return VectorStore._convert_to_tdmldf(pd.DataFrame(data['response_list']))


    @staticmethod
    def _process_vs_response(api_name, response, success_status_code=None, raise_error=True):
        """
        DESCRIPTION:
            Process and validate the Vector Store service response.

        PARAMETERS:
            api_name:
                Required Argument.
                Specifies the name of the Vector Store method.
                Types: str

            response:
                Required Argument.
                Specifies the response recieved from Vector Store service.
                Types: requests.Response

            success_status_code:
                Optional Argument.
                Specifies the expected success status code for the corresponding
                Vector Store service.
                Default Value: None
                Types: int

            raise_error:
                Optional Argument.
                Specifies a boolean flag that decides whether to raise error or not.
                Default Values: True
                Types: bool

        RETURNS:
            Response object.

        RAISES:
            TeradataMlException, JSONDecodeError.

        EXAMPLES:
                >>> _process_vs_response("create", resp)
        """
        try:
            data = response.json()
            # Success status code ranges between 200-300.
            if (success_status_code is None and 200 <= response.status_code <= 303) or \
                    (success_status_code == response.status_code):
                if "message" in data:
                    if api_name not in ["similarity-search", "prepare-response", "ask"]:
                        print(data['message'])
                    return data['message']
                else:
                    return data
                return

            # teradataml API got an error response. Error response is expected as follows -
            # Success
            # Response:
            # {
            #     "message": "success string"
            # }
            # Failure
            # Response:
            # {
            #     "detail": "error message string"
            # }
            # Validation
            # Error:
            # {
            #     "detail": [
            #         {
            #             "loc": [
            #                 "string",
            #                 0
            #             ],
            #             "msg": "string",
            #             "type": "string"
            #         }
            #     ]
            # }
            # Extract the fields and raise error accordingly.
            if isinstance(data['detail'], str):
                error_description = data['detail']
            else:
                error_description = []
                for dict_ele in data['detail']:
                    error_msg = f"{dict_ele['msg']} for {dict_ele['loc'][1] if len(dict_ele['loc']) > 1 else dict_ele['loc'][0]}"
                    error_description.append(error_msg)
                error_description = ",".join(error_description)

            error_description = f'Response Code: {response.status_code}, Message:{error_description}'

            error_msg = Messages.get_message(MessageCodes.FUNC_EXECUTION_FAILED,
                                             api_name,
                                             error_description)
            if api_name == "status" and "Vector store" in error_msg and 'does not exist.' in error_msg:
                print("Vector Store does not exist or it is has been destroyed successfully.")
                return
            if raise_error:
                raise TeradataMlException(error_msg, MessageCodes.FUNC_EXECUTION_FAILED)

        # teradatagenai API may not get a Json API response in some cases.
        # So, raise an error with the response received as it is.
        except JSONDecodeError:
            error_msg = Messages.get_message(MessageCodes.FUNC_EXECUTION_FAILED,
                                             api_name,
                                             f'Response Code: {response.status_code}, Message: {response.text}')
            if raise_error:
                raise TeradataMlException(error_msg, MessageCodes.FUNC_EXECUTION_FAILED)
        except Exception as e:
            if raise_error:
                raise

    @staticmethod
    # TODO: https://teradata-pe.atlassian.net/browse/ELE-6100: Replace this with
    #  DataFrame.json() once implemented.
    def _convert_to_tdmldf(pdf, index=False):
        """
        DESCRIPTION:
            Converts pandas DataFrame to teradataml DataFrame.

        PARAMETERS:
            pdf:
                Required Argument.
                Specifies the pandas DataFrame to be converted to teradataml DataFrame.
                Types: pandas DF.

        RETURNS:
            teradataml DataFrame.

        RAISES:
            None

        EXAMPLES:
           VectorStore._convert_to_tdmldf(pdDf)
        """
        # Form the table name and return teradataml DataFrame.
        table_name = UtilFuncs._generate_temp_table_name(prefix="vs",
                                                         table_type=TeradataConstants.TERADATA_TABLE,
                                                         gc_on_quit=True)
        if len(pdf) > 0:
            copy_to_sql(pdf, table_name, index=index)
            return DataFrame(table_name)

    def status(self):
        """
        DESCRIPTION:
            Checks the status of the below operations:
               * create
               * destroy
               * update

        PARAMETERS:
            None

        RETURNS:
            Pandas DataFrame containing the status of vector store operations.

        RAISES:
            None

        EXAMPLES:
           # Create an instance of the VectorStore class.
           >>> vs = VectorStore(name="vs")
           # Example 1: Check the status of create operation.

           # Create VectorStore.
           # Note this step is not needed if vector store already exists.
           >>> vs.create(object_names="amazon_reviews_25",
                         description="vector store testing",
                         key_columns=['rev_id', 'aid'],
                         data_columns=['rev_text'],
                         vector_column='VectorIndex',
                         embeddings_model="amazon.titan-embed-text-v1")

           # Check status.
           >>> vs.status()
        """

        response = UtilFuncs._http_request(self.__common_url, HTTPRequest.GET,
                                           headers=self.__headers,
                                           cookies={'session_id': self.__session_id})
        status_op = self._process_vs_response("status", response)
        if status_op is None:
            return
        if 'status' in status_op and 'failed' in status_op['status'].lower():
            # The status API has the following output:
            # {'vs_name': 'vs_example1', 'status': 'create failed',
            # 'error': 'Error in function
            # TD_VectorNormalize: Number of elements do not match with embedding size'}
            # The 'status' key contains text like 'create failed', 'update failed'.
            # Hence extracting the word before 'failed' to get the operation which has failed.
            api_name = re.search(r"(\w+)\s+" + re.escape('failed'), status_op['status'].lower()).group(1)
            msg = status_op["error"] if 'error' in status_op else ""

            error_msg = Messages.get_message(MessageCodes.FUNC_EXECUTION_FAILED,
                                             api_name, f'Response Code: {response.status_code}, Message: {msg}')
            raise TeradataMlException(error_msg, MessageCodes.FUNC_EXECUTION_FAILED)
        return pd.DataFrame([self._process_vs_response("status", response)])

    def list_user_permissions(self):
        """
        DESCRIPTION:
            Lists the users and their corresponding permissions
            on the vector store.
            Notes:
                * Only admin users can use this method.
                * Refer to the 'Admin Flow' section in the
                  User guide for details.

        PARAMETERS:
            None

        RETURNS:
            teradataml DataFrame containing the users and the
            corresponding permissions on the vector store.

        RAISES:
            TeradataMlException

        EXAMPLES:
            # Create an instance of an already existing vector store.
            >>> vs = VectorStore(name="vs")

            # Example: List the user permissions on the vector store.
            >>> vs.list_user_permissions()
        """

        # Get the user permissions on the vector store.
        response = UtilFuncs._http_request(self.__list_user_permission_url,
                                           HTTPRequest.GET,
                                           headers=self.__headers,
                                           cookies={'session_id': self.__session_id})
        # Process the response and return the user permissions.
        data = self._process_vs_response("list_user_permissions", response)
        return VectorStore._convert_to_tdmldf(pd.DataFrame({"Users": data['authenticated_users'].keys(),
                            "Permissions": data['authenticated_users'].values()}))
    
    @property
    def revoke(self):
        """
        DESCRIPTION:
            Revoke the permission of the user on the vector store.
            Notes:
                * Only admin users can use this method.
                * Admin can revoke admin/user permssions of other users and
                  admins on the vector store.
                * Admin/User cannot revoke his own permssions.
                * Admin cannot revoke user permissions of another admin.
                  First the admin permissions needs to be revoked and
                  then the user permission can be revoked.
                * Refer to the 'Admin Flow' section in the
                  User guide for details.

        RETURNS:
            None

        RAISES:
            TeradataMlException

        EXAMPLES:
            # NOTE: It is assumed that vector store "vs" already exits.
            # Create an instance of the VectorStore class.
            >>> vs = VectorStore(name="vs")
            # Revoke 'admin' permission of user 'alice' on the vector store 'vs'.
            >>> vs.revoke.admin('alice')
            # Revoke 'user' permission of user 'alice' on the vector store 'vs'.
            >>> vs.revoke.user('alice')
        """
        return _Revoke(self)
    
    @property
    def grant(self):
        """
        DESCRIPTION:
            Grant permissions to the user on the vector store.
            Notes:
                * Only admin users can use this method.
                * Refer to the 'Admin Flow' section in the
                  User guide for details.

        RETURNS:
            None

        RAISES:
            TeradataMlException

        EXAMPLES:
            # NOTE: It is assumed that vector store "vs" already exits.
            # Create an instance of the VectorStore class.
            >>> vs = VectorStore(name="vs")
            # Grant 'admin' permission to the user 'alice' on the vector store 'vs'.
            >>> vs.grant.admin('alice')
            # Grant 'user' permission to the user 'alice' on the vector store 'vs'.
            >>> vs.grant.user('alice')
        """
        return _Grant(self)

class VSPattern:
    """
    Patterns are kind of regex which is used for combining names of tables or views
    matching the pattern string which can then be used for creating metadata based vector store.
    """
    def __init__(self,
                 name, 
                 log=False):
        """
        DESCRIPTION:
            Initialize the VSPattern class for metadata-based vector store.
            For metadata-based vector stores, the selection of tables/views can be huge.
            They can span multiple databases and it can become tedious to list them using
            "include_objects" and "exclude_objects".
            Patterns provide a way to select these tables/views and columns
            using simple regular expressions.

        PARAMETERS:
            name:
                Required Argument.
                Specifies the name of the pattern for vector store.
                Types: str

            log:
                Optional Argument.
                Specifies whether to enable logging.
                Default Value: False
                Types: bool

        RETURNS:
            None

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> from teradatagenai import VSPattern
            >>> pattern = VSPattern(pattern_name="metadata")
        """
        # Initialize variables.
        self._pattern_name = name
        self._enable_logging = log
        self._pattern_string = None

        # Validating name and enable_logging.
        arg_info_matrix = []
        arg_info_matrix.append(["name", self._pattern_name, False, (str), True])
        arg_info_matrix.append(["enable_logging", self._enable_logging, True, (bool)])

        # Validate argument types.
        _Validators._validate_function_arguments(arg_info_matrix)

        # As the rest call accepts 0, 1 converting it.
        self._enable_logging = 0 if not self._enable_logging else 1

        # Initialize URLs.
        self.__pattern_url = f'{vector_store_urls.patterns_url}/{self._pattern_name}'
        self.__common_pattern_url = f'{self.__pattern_url}?log_level={self._enable_logging}'

        # Call connect in case of CCP enabled tenant.
        # If non-ccp, connect should be explicitly called passing the required params.
        session_header = VSManager._generate_session_id()
        self.__session_id = session_header["vs_session_id"]
        self.__headers = session_header["vs_header"]
    
    @property
    def __create_pattern_url(self):
        """ Returns the URL for creating the pattern. """
        return f'{self.__pattern_url}?pattern_string={self._pattern_string}'

    def get(self):
        """
        DESCRIPTION:
            Gets the list of objects that matches the pattern name.
            Notes:
                * Only admin users can use this method.
                * Refer to the 'Admin Flow' section in the
                  User guide for details.

        PARAMETERS:
            None

        RETURNS:
            teradataml dataFrame containing the list of objects that matches the pattern name.

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> from teradatagenai import VSPattern
            >>> pattern = VSPattern(pattern_name="metadata")
            >>> pattern.create(pattern_string='SEMANTIC_DATA.CRICKET_%')
            >>> pattern.get()
        """
        response = UtilFuncs._http_request(self.__common_pattern_url, HTTPRequest.GET,
                                           headers=self.__headers,
                                           cookies={'session_id': self.__session_id})
        # Process the response
        data = VectorStore._process_vs_response("get_pattern", response)
        return VectorStore._convert_to_tdmldf(pd.DataFrame({'Object list': data['object_list']}))
        
    def create(self, pattern_string):
        """
        DESCRIPTION:
            Creates the pattern for metadata-based vector store.
            Notes:
                * Only admin users can use this method.
                * Refer to the 'Admin Flow' section in the
                  User guide for details.

        PARAMETERS:
            pattern_string:
                Required Argument.
                Specifies the pattern string to be used for creating the pattern.
                A pattern string can be formed by using SQL wildcards "%" or "_".
                For example:
                    * `SEMANTIC_DATA.CRICKET%` - This pattern string will internally fetch all tables and
                                                 views in the SEMANTIC_DATA database starting with CRICKET
                                                 at the time of vector store creation.
                    * `log__` - This pattern string will internally fetch all tables and views starting
                                with log and having two extra characters like `log_a` or `log12` in the
                                logged-in database at the time of vector store creation.
                    * `data_.%` - This pattern string will internally fetch all tables and views in all
                                  databases starting with data and having one extra character like
                                  `data1.t1`, `data2.v2`, `datax.train` at the time of vector store creation.
                Types: str

        RETURNS:
            None

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> from teradatagenai import VSPattern
            >>> pattern = VSPattern(pattern_name="metadata")
            >>> pattern.create(pattern_string='SEMANTIC_DATA.CRICKET_%')
        """
        # Validating pattern_string.
        arg_info_matrix = []
        arg_info_matrix.append(["pattern_string", pattern_string, False, (str), True])

        # Validate argument types.
        _Validators._validate_function_arguments(arg_info_matrix)

        # Assign pattern_string.
        self._pattern_string = pattern_string

        response = UtilFuncs._http_request(self.__create_pattern_url, HTTPRequest.POST,
                                           headers=self.__headers,
                                           cookies={'session_id': self.__session_id})
        # Process the response
        VectorStore._process_vs_response("create_pattern", response)

    def delete(self):
        """
        DESCRIPTION:
            Deletes the pattern.
            Notes:
                * Only admin users can use this method.
                * Refer to the 'Admin Flow' section in the
                  User guide for details.

        PARAMETERS:
            None

        RETURNS:
            None

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> from teradatagenai import VSPattern
            >>> pattern = VSPattern(pattern_name="metadata")
            >>> pattern.delete()
        """
        response = UtilFuncs._http_request(self.__common_pattern_url, HTTPRequest.DELETE,
                                           headers=self.__headers,
                                           cookies={'session_id': self.__session_id})
        # Process the response
        VectorStore._process_vs_response("delete_pattern", response)
