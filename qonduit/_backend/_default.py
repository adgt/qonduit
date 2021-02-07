import sys
import functools
import ipywidgets as widgets

def default(func):
    @functools.wraps(func)
    def resolve(*args, **kwargs):
        output = widgets.Output()
        output.append_stdout(f"No package is installed for `{func.__name__}`.\n")
        output.append_stdout(f"Try installing an optional dependency.\n")
        return output
        
    return resolve

def get_all_backends():
    # return all real backend providers (i.e. not this module)
    return [m.__name__ for m in sys.modules.values() if f'{__package__}.' in m.__name__ and m.__name__ != __name__]

def get_fully_qualified_api(symbol):
    return ".".join([symbol.__module__, symbol.__name__])

def get_implementation_api(symbol):
    return get_fully_qualified_api(symbol).replace('.', '_')

def get_implementation(backend, api_func):
    implemented_function_name = get_implementation_api(api_func)
    implementation = getattr(sys.modules[backend], implemented_function_name, api_func)
    return implementation

def resolve(backend, func, *args, **kwargs):
    implementation = get_implementation(backend, func)
    if implementation != func:
        return implementation(*args, **kwargs)        
    else:
        return func(*args, **kwargs)
    
def uses_iterable_results(func):
    def converter(*args, **kwargs):
        if len(args) > 0:
            data = args[0]
            if hasattr(data, 'keys'):
                return func(*args, **kwargs)
            else:
                backends = get_all_backends()
                for b in backends:
                    backend = sys.modules[b]
                    implementation = getattr(backend, 'to_iterable_results', None)
                    if implementation is not None:
                        iterable_data = implementation(data)
                        
                        # if this converted correctly, then use; otherwise, keep trying other backends
                        if hasattr(iterable_data, 'keys'):
                            updated_args = list(args)
                            updated_args[0] = iterable_data
                            args = tuple(updated_args)
                            return func(*args, **kwargs)
                        
        return func(*args, **kwargs)
    return converter

def circuit_type(klass):
    def decorator(func):
        def converter(*args, **kwargs):
            if len(args) > 0:
                arg_circuit = args[0]
                if not isinstance(arg_circuit, klass) and not isinstance(arg_circuit, str):
                    arg_circuit_type = arg_circuit.__class__
                                
                    backends = get_all_backends()
                    for b in backends:
                        backend = sys.modules[b]                
                        if getattr(backend, 'CIRCUIT_TYPE', None) is arg_circuit_type:
                            # check for explicit circuit type to target circuit type conversion function
                            implemented_function_name = f"to_{get_implementation_api(klass)}"
                            implementation = getattr(backend, implemented_function_name, func)
                            if implementation != func:
                                return func(implementation(*args, **kwargs))
                            else:
                                # use the default qasm converter
                                qasm_converter = getattr(backend, "to_qasm", func)
                                if qasm_converter != func:
                                    qasm = qasm_converter(*args, **kwargs)
                                    return func(qasm)
            return func(*args, **kwargs)
        return converter
    return decorator