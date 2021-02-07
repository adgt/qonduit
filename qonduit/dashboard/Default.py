import ipywidgets as widgets
import qonduit.visualization.circuit as qxc
import qonduit.visualization.state as qxs
import qonduit.visualization.pulse as qxp
import qonduit.visualization.metrics as qxm
from .Circuit import Circuit

try:
    from pulsemaker import simulate
except ImportError:
    from warnings import warn
    def simulate(qiskit_schedule, backend_name):
        warn("Pulsemaker could not be imported, so pulses will not simulate", ImportWarning)

class Default(widgets.Tab):
    def __init__(self, circuit):
        super().__init__()
        cd = Circuit(circuit)
        self._circuit_dashboard = cd
        cd.observe(self.update_schedule_dashboard_circuit, names='circuit_qasm')
                    
        sd = qxp.design_schedule()
        self._schedule_dashboard = sd
        self._histogram_plot = qxm.plot_histogram({'0': 1})
        if hasattr(sd, '_plot_panel'): # knowledge of pulseviz
            sd_children = list(sd._plot_panel.children)
            sd_children.extend([self._histogram_plot])
            sd._plot_panel.children = sd_children
        elif hasattr(sd, 'children'): # generic
            sd_children = list(sd.children)
            sd_children.extend([self._histogram_plot])
            sd.children = sd_children
        sd.observe(self.update_histogram_plot, names='schedule')
        
        pd = qxp.design_pulse()
        self._pulse_dashboard = pd
               
        pd.observe(self.update_custom_pulse, names='pulse')
        
        self.children = [self._circuit_dashboard, self._schedule_dashboard, self._pulse_dashboard]
        self.set_title(0, 'Circuit Designer')
        self.set_title(1, 'Schedule Designer')
        self.set_title(2, 'Pulse Designer')   
        
        # Set size to accommodate current tabs
        self.layout.width = '1200px'
        self.layout.max_height = '560px'

    def update_schedule_dashboard_circuit(self, change):
        self._schedule_dashboard.circuit_qasm = change['new']
    
    def update_histogram_plot(self, change):
        counts = simulate(change['new'], self._schedule_dashboard._current_backend)
        self._histogram_plot.kwargs_widgets[0].value = counts
    
    def update_custom_pulse(self, change):
        self._schedule_dashboard.custom_pulse = change['new']
        