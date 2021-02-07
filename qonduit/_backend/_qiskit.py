from ._default import resolve as default_resolve, circuit_type, uses_iterable_results
import functools

def qiskit(func):
    @functools.wraps(func)
    def resolve(*args, **kwargs):
#         print("Hello qiskit")
        return default_resolve(__name__, func, *args, **kwargs)
        
    return resolve


try:
    from qiskit.circuit import QuantumCircuit as CIRCUIT_TYPE
    
    def to_qasm(circuit):
        return circuit.qasm()
        
    def from_qasm(circuit):
        if isinstance(circuit, CIRCUIT_TYPE):
            return circuit
        else:
            return CIRCUIT_TYPE.from_qasm_str(circuit)    
except ImportError:
    pass


try:
    from qiskit.visualization import (circuit_drawer, 
                                      plot_histogram,
                                      plot_bloch_multivector, 
                                      plot_state_city, 
                                      plot_state_hinton, 
                                      plot_state_paulivec, 
                                      plot_state_qsphere)
    import qiskit.quantum_info as qi
    from ipywidgets import interactive, fixed

    @circuit_type(CIRCUIT_TYPE)
    def qonduit_visualization_circuit_draw(circuit):
        return interactive(lambda: display(circuit_drawer(from_qasm(circuit))))
    
    @uses_iterable_results
    def qonduit_visualization_metrics_plot_histogram(data):
        return interactive(lambda data: display(plot_histogram(data)), data=fixed(data))
    
    def qonduit_visualization_state_plot_bloch_multivector(state):
        return interactive(lambda sv: display(plot_bloch_multivector(sv)), sv=fixed(state))
    
    def qonduit_visualization_state_plot_state_city(state):
        return interactive(lambda sv: display(plot_state_city(sv)), sv=fixed(state))

    def qonduit_visualization_state_plot_state_hinton(state):
        return interactive(lambda sv: display(plot_state_hinton(sv)), sv=fixed(state))
        
    def qonduit_visualization_state_plot_state_paulivec(state):
        return interactive(lambda sv: display(plot_state_paulivec(sv)), sv=fixed(state))
    
    def qonduit_visualization_state_plot_state_qsphere(state):
        return interactive(lambda sv: display(plot_state_qsphere(sv)), sv=fixed(state))
except ImportError:
    pass
