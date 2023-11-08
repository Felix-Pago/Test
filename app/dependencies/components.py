from fastapi import Depends
from felix_library.components.context_parser.context_parser import \
    ContextParser
from felix_library.interfaces.context_parser.context_parser_interface import \
    ContextParserInterface

from app.bootstrap.env_flags_variables import ENV_FLAGS_VARIABLES
from app.components.components import Components


def get_context_parser() -> ContextParserInterface:
    return ContextParser(ENV_FLAGS_VARIABLES)


def get_components(context_parser: ContextParserInterface = Depends(get_context_parser)) -> Components:
    components: Components = Components(context_parser.get_context_variable('env'),
                                        context_parser.get_context_variable('config_path'),
                                        context_parser.get_context_variable('google_application_credentials'))
    return components
