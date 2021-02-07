# __all__ = ['_cirq', '_qiskit']
from ._default import default
from ._cirq import cirq
from ._qiskit import qiskit
from ._quirk import quirk
from ._pulsemaker import pulsemaker
# from ._default import resolve as default_resolve

# @qiskit
# @cirq
# def to_qasm(func):
#     def resolve(*args, **kwargs):
#         return default_resolve(__name__, func, *args, **kwargs)
    
#     return resolve
    