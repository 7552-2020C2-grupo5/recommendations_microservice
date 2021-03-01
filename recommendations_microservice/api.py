"""API module."""
import logging

from flask_restx import Api

from recommendations_microservice import __version__
from recommendations_microservice.namespaces import default_namespace, token_namespace

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


api = Api(prefix="/v1", version=__version__, validate=True)
api.add_namespace(default_namespace, path='/recommendations')
api.add_namespace(token_namespace, path='/token')


@api.errorhandler
def handle_exception(error: Exception):
    """When an unhandled exception is raised"""
    message = "Error: " + getattr(error, 'message', str(error))
    return {'message': message}, getattr(error, 'code', 500)
