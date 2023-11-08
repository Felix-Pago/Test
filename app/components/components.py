import os
from pathlib import Path
from threading import Lock
from typing import Any, Dict, Optional

from felix_library.components.configuration.configuration import Configuration
from felix_library.components.firestore.firestore import Firestore
from felix_library.components.http.http import Http
from felix_library.components.logger.logger import Logger
from felix_library.components.posthog.posthog import Posthog
from felix_library.components.pubsub.pubsub import PubSub
from felix_library.components.redis.redis import Redis
from felix_library.components.secret_manager.secret_manager import SecretManager
from felix_library.components.telemetry.telemetry import Telemetry

from felix_library.entities.secret_manager.secret_manager_properties import SecretManagerProperties
from felix_library.exceptions.component_error import ComponentError
from felix_library.exceptions.initialization_error import InitializationError

from felix_library.interfaces.configuration.configuration_interface import ConfigurationInterface
from felix_library.interfaces.firestore.firestore_interface import FirestoreInterface
from felix_library.interfaces.http.http_interface import HttpInterface
from felix_library.interfaces.posthog.posthog_interface import PosthogInterface
from felix_library.interfaces.pubsub.pubsub_interface import PubSubInterface
from felix_library.interfaces.redis.redis_interface import RedisInterface
from felix_library.interfaces.secret_manager.secret_manager_interface import SecretManagerInterface
from felix_library.interfaces.telemetry.telemetry_interface import TelemetryInterface

from felix_library.components.logger.custom_formatter import CustomFormatter


class ComponentsMeta(type):
    _instances: Dict = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Components(metaclass=ComponentsMeta):

    def __init__(self, env: str, config_path: str, google_application_credentials: Optional[str]) -> None:
        self.__env: str = env
        root_dir: str = str(Path(__file__).resolve().parents[2])
        self.__config_path: str = os.path.join(root_dir, config_path)
        self.__google_application_credentials: Optional[str] = google_application_credentials
        self.__components: Dict[str, Any] = self.bootstrap_components()

    def bootstrap_components(self) -> Dict[str, Any]:
        if self.__env == 'test':
            raise InitializationError('Test env is not supported, please use base test instead')
        if self.__env == 'development':
            return self.__get_env_agnostic_components()
        elif self.__env == 'sandbox':
            return self.__get_env_agnostic_components()
        elif self.__env == 'production':
            return self.__get_env_agnostic_components()

        raise InitializationError('Non valid env was provided to the components bootstrap process')

    def __get_env_agnostic_components(self) -> Dict[str, Any]:
        configuration: ConfigurationInterface = Configuration(
            self.__env,
            self.__config_path)
        logger: Logger = Logger(
            configuration.get_configuration('service_name', str),
            self.__env,
            self.__google_application_credentials,
            configuration.get_configuration('log_file', str),
            configuration.get_configuration('log_format', str),
            configuration.get_configuration('log_level', str),
            custom_formatter=CustomFormatter(configuration.get_configuration('log_format', str)))
        http: HttpInterface = Http(
            logger.get_logger('http'))
        firestore: FirestoreInterface = Firestore(
            self.__google_application_credentials,
            logger.get_logger('firestore'))
        secret_manager: SecretManagerInterface = SecretManager(
            SecretManagerProperties(
                configuration.get_configuration('service_name', str),
                configuration.get_configuration('secret_manager_project_id', str),
                configuration.get_configuration('secret_manager_path', str),
                configuration.get_configuration('secret_manager_cache_size', int),
                configuration.get_configuration('secret_manager_cache_ttl', int),
                logger.get_logger('secret_manager'),
                self.__google_application_credentials))
        posthog: PosthogInterface = Posthog(
            secret_manager.get('posthog_project_api_key'),
            secret_manager.get('posthog_personal_api_key'),
            configuration.get_configuration('posthog_debug', bool),
            configuration.get_configuration('posthog_disabled', bool))
        pubsub: PubSubInterface = PubSub(
            self.__google_application_credentials,
            configuration.get_configuration('pubsub_project_id', str),
            logger.get_logger('pubsub'))
        redis: RedisInterface = Redis(
            configuration.get_configuration('redis_host', str),
            configuration.get_configuration('redis_port', int),
            configuration.get_configuration('redis_username', str),
            secret_manager.get('redis_password'),
            configuration.get_configuration('redis_ssl_connection', bool),
            configuration.get_configuration(
                'redis_ssl_cert_reqs', Optional[str], has_none_value=True),
            logger.get_logger('redis'))
        telemetry: TelemetryInterface = Telemetry(
            self.__google_application_credentials,
            configuration.get_configuration('cloud_tracer_project_id', str),
            configuration.get_configuration('service_name', str),
            self.__env)

        return {
            'configuration': configuration,
            'logger': logger,
            'http': http,
            'firestore': firestore,
            'secret_manager': secret_manager,
            'posthog': posthog,
            'redis': redis,
            'telemetry': telemetry,
            'pubsub': pubsub,
        }

    def get_component(self, component_name: str) -> Any:
        if component_name in self.__components:
            return self.__components[component_name]
        raise ComponentError(component_name)
