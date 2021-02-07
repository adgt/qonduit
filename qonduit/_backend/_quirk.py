from ._default import resolve as default_resolve, circuit_type
import functools

def quirk(func):
    @functools.wraps(func)
    def resolve(*args, **kwargs):
        return default_resolve(__name__, func, *args, **kwargs)
        
    return resolve

try:
    from pyQuirk import Quirk
    from ipywidgets import interactive, fixed

    def qonduit_visualization_circuit_design(circuit):
        quirk = Quirk()
        quirk.update_circuit(circuit)
        return quirk
except ImportError:
    pass
