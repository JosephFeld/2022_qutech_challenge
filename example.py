import logging
import os

from projectq import MainEngine
from projectq.setups import linear
from projectq.ops import H, Rx, Rz, CNOT, CZ, Measure, All

from quantuminspire.credentials import get_authentication
from quantuminspire.api import QuantumInspireAPI
from quantuminspire.projectq.backend_qx import QIBackend

def sample_code():


    QI_URL = os.getenv('API_URL', 'https://api.quantum-inspire.com/')

    authentication = get_authentication()
    qi_api = QuantumInspireAPI(QI_URL, authentication)

    projectq_backend = QIBackend(quantum_inspire_api=qi_api)

    engine = MainEngine(backend=projectq_backend)  # create default compiler (simulator back-end)

    qubits = engine.allocate_qureg(5)
    q1 = qubits[0]
    q2 = qubits[-1]

    H | q1  # apply a Hadamard gate
    CNOT | (q1, q2)
    All(Measure) | qubits  # measure the qubits

    engine.flush()  # flush all gates (and execute measurements)

    print("Measured {}".format(','.join([str(int(q)) for q in qubits])))
    print('Probabilities: %s' % (projectq_backend.get_probabilities(qubits),))
    print(projectq_backend.cqasm())

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sample_code()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
