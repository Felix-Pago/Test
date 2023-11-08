import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from felix_library.components.context_parser.context_parser import ContextParser
from felix_library.interfaces.context_parser.context_parser_interface import ContextParserInterface

from app.bootstrap.bootstrapper import boostrap
from app.bootstrap.env_flags_variables import ENV_FLAGS_VARIABLES
from app.components.components import Components

load_dotenv()

context_parser: ContextParserInterface = ContextParser(ENV_FLAGS_VARIABLES)
components: Components = Components(context_parser.get_context_variable('env'),
                                    context_parser.get_context_variable('config_path'),
                                    context_parser.get_context_variable('google_application_credentials'))
app: FastAPI = boostrap(components)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=int(os.environ.get('PORT', 8080)),
                reload=context_parser.get_context_variable('reload'))
