import ipywidgets as widgets
import traitlets as traitlets
import qonduit.visualization.circuit as qxc
import qonduit.visualization.state as qxs
import qiskit.quantum_info as qi

class Circuit(widgets.VBox, traitlets.HasTraits):
    circuit_qasm = traitlets.Unicode()
    
    def __init__(self, circuit):
        cv = qxc.design(circuit)
        self._circuit = circuit
        self._cv = cv
                    
        cv.observe(self.update_circuit, names='circuit_qasm')
        cv.width = 1000
        cv.height = 200
                
        plot_options = [method_name for method_name in dir(qxs) if 'plot_' in method_name]
        dropdown = widgets.Dropdown(
                        options=plot_options,
                        value=plot_options[0],
                        description='Plot:',
                    )
        dropdown.observe(self.update_plot_type, names='value')
        self.update_plot_type({'new': dropdown.value}) # call it once to initialize
        self._plot_type_dd = dropdown
        
        self._plot_panel = widgets.VBox([self._plot_type_dd, self._plot])
        super().__init__([self._cv, self._plot_panel])
        # Setting the width is required to have an image scale down appropriately and not create scroll bars.
        # Unfortunately, setting only the height will not have the same effect.
        self._plot_panel.layout.width = '400px'
    
    def update_plot_type(self, change):
        state = qi.Statevector.from_instruction(self._circuit.to_instruction())
        self._plot = getattr(qxs, change['new'])(state)
        if hasattr(self,'_plot_panel'):
            children = list(self._plot_panel.children)
            children[1] = self._plot
            self._plot_panel.children = children
            self._plot.update()
    
    def update_circuit(self, change):
        if "OPENQASM" in change['new']:
            self.circuit_qasm = change['new']
            self._circuit = self._circuit.from_qasm_str(change['new'])
            self._plot.kwargs_widgets[0].value = qi.Statevector.from_instruction(self._circuit.to_instruction())