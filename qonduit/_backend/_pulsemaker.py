from ._default import resolve as default_resolve, circuit_type
import functools

def pulsemaker(func):
    @functools.wraps(func)
    def resolve(*args, **kwargs):
        return default_resolve(__name__, func, *args, **kwargs)
        
    return resolve

try:
    from pulsemaker import ScheduleDesigner, PulseDesigner, plot_pulse_schedule
    from ipywidgets import interactive, fixed
    
    def qonduit_visualization_pulse_design_schedule():
        scheduleDesigner = ScheduleDesigner()
        return scheduleDesigner

    def qonduit_visualization_pulse_design_pulse():
        pulseDesigner = PulseDesigner()
        return pulseDesigner

    def qonduit_visualization_pulse_plot_pulse_schedule(phases, freqs, pulses, samples):
        return plot_pulse_schedule(phases, freqs, pulses, samples)
except ImportError:
    pass
