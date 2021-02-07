from ._default import resolve as default_resolve, circuit_type, uses_iterable_results
import functools

def cirq(func):
    @functools.wraps(func)
    def resolve(*args, **kwargs):
        print("Hello cirq")
        return default_resolve(__name__, func, *args, **kwargs)
    
    return resolve

try:
    from cirq import Circuit as CIRCUIT_TYPE
    from cirq.contrib.qasm_import import circuit_from_qasm
    from cirq.study.result import Result
    
    def to_qasm(circuit):
        return circuit.to_qasm()
        
    def from_qasm(circuit):
        if isinstance(circuit, CIRCUIT_TYPE):
            return circuit
        else:
            return circuit_from_qasm(circuit)
        
    def to_iterable_results(data):
        if isinstance(data, Result):
            key = list(data.measurements.keys())[0]
            return data.histogram(key=key)
        else:
            return data
        
    @circuit_type(CIRCUIT_TYPE)
    def qonduit_visualization_circuit_draw(circuit):
        print(from_qasm(circuit))
        return
except ImportError:
    pass

try:
    from cirq.study.visualize import plot_state_histogram
    from ipywidgets import interactive, fixed
        
    def qonduit_visualization_metrics_plot_histogram(data):
        return interactive(lambda data: display(plot_state_histogram(data)), data=fixed(data))    
except ImportError:
    pass
