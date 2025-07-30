# flake8: noqa: I003
import inspect
from typing import Any, Callable
from azure.functions import HttpRequest, HttpResponse, Context, FunctionApp
from fabric.functions.fabric_class import FabricLakehouseClient, FabricSqlConnection, UserDataFunctionContext
from .ensure_formatted_returntype import ensure_formatted_returntype
from .add_timeout import add_timeout
from .remove_unused_binding_params import remove_unused_binding_params
from .add_parameters import add_parameters
from .log_error import log_error
from fabric.internal.fabric_lakehouse_files_client import FabricLakehouseFilesClient

from .function_parameter_keywords import REQ_PARAMETER, CONTEXT_PARAMETER, UNUSED_FABRIC_CONTEXT_PARAMETER


def configure_fabric_function_builder(udf: FunctionApp, wrap) -> Callable[..., Any]:   
    def decorator(func):
        sig = inspect.signature(func)
        
        # Update function parameters to include a request object for validation
        params = []
        params.append(inspect.Parameter(REQ_PARAMETER, inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=HttpRequest))
        params.append(inspect.Parameter(UNUSED_FABRIC_CONTEXT_PARAMETER, inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=UserDataFunctionContext))
        
        # Udf params to be parsed from the request
        udfParams = []
        for param in sig.parameters.values():
            # Ensure bindings are still there
            if _is_typeof_fabricitem_input(param.annotation) or _is_typeof_userdatafunctioncontext_input(param.annotation):
                params.append(inspect.Parameter(param.name, inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=param.annotation))
            # Separate out basic parameters to parse later
            if param.name != REQ_PARAMETER and param.name != CONTEXT_PARAMETER:
                udfParams.append(inspect.Parameter(param.name, inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=_get_cleaned_type_and_wrap_str(param)))
        sig = sig.replace(parameters=tuple(params)).replace(return_annotation=str)
        func.__signature__ = sig
        annotations = {}
        # Update annotations to ensure it uses the cleaned type
        for param in params:
            annotations[param.name] = param.annotation
        # Update return annotation of func to be HttpResponse
        # We should catch if they don't have a return type during metadata generation, but good to double check here
        if 'return' in func.__annotations__:
            annotations['old_return'] = func.__annotations__['return']
        
        annotations['return'] = HttpResponse
        func.__annotations__ = annotations
        
        # Add wrapper for function to handle ensure all return values are parsed to HttpResponse
        user_func = add_timeout(func)
        user_func = log_error(user_func)
        user_func = remove_unused_binding_params(user_func)
        user_func = ensure_formatted_returntype(user_func)

        # Add parameters to the function
        user_func = add_parameters(user_func, udfParams)
        fb = udf._validate_type(user_func)
        udf._function_builders.append(fb)

        return wrap(fb, user_func)
    return decorator

def _is_typeof_fabricitem_input(obj):
    # Check to see if parameter is anything we might return from a fabric binding
    return obj == FabricSqlConnection or obj == FabricLakehouseFilesClient or obj == FabricLakehouseClient

def _is_typeof_userdatafunctioncontext_input(obj):
    # Check to see if parameter is anything we might return from a fabric binding
    return obj == UserDataFunctionContext

def _get_cleaned_type_and_wrap_str(param):
    if hasattr(param.annotation,'__origin__'): 
        return param.annotation.__origin__
    else:
        return param.annotation