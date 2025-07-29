from enum import Enum

class Message(str,Enum):
    UNEXPECTED_ERROR_MSG = 'Something went wrong while processing your request. Please try again later.'
    PORTAL_ACCESS_RESTRICTED_MSG = 'You are not authorized to access this portal.'
    PROCESS_SUCCESS_MSG = 'Process executed successfully.'
    NO_RESULTS_FOUND_MSG = 'No records were found matching your request.'
    INVALID_REQUEST_PARAMS_MSG = 'Please review the required fields and try again.'
    SERVER_NETWORK_ACCESS_ERROR_MSG = 'Error making the server accessible on the network.'
    HEXAGONAL_SERVICE_CREATED_MSG = 'The hexagonal service structure was created.'
    PYCACHE_CLEANUP_SUCCESS_MSG = 'All __pycache__ have been removed.'