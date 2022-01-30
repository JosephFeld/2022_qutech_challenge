import logging
import os

from projectq import MainEngine
from projectq.setups import linear
from projectq.ops import H, Rx, Rz, CNOT, CZ, Measure, All

from quantuminspire.credentials import get_authentication
from quantuminspire.api import QuantumInspireAPI
from quantuminspire.projectq.backend_qx import QIBackend

# Return engine
def login():
    QI_URL = os.getenv('API_URL', 'https://api.quantum-inspire.com/')

    authentication = get_authentication()

    print("setting up api")

    qi_api = QuantumInspireAPI(QI_URL, authentication)

    print("setting up backend")

    projectq_backend = QIBackend(quantum_inspire_api=qi_api)

    print("setting up engine")

    engine = MainEngine(backend=projectq_backend)  # create default compiler (simulator back-end)

    return projectq_backend, engine

def naive_qpm(projectq_backend, engine):

    qubits = engine.allocate_qureg(5)
    q1 = qubits[0]
    q2 = qubits[1]

    H | q1  # apply a Hadamard gate
    CNOT | (q1, q2)
    H | q1
    All(Measure) | qubits  # measure the qubits

    engine.flush()  # flush all gates (and execute measurements)

    print("Measured {}".format(','.join([str(int(q)) for q in qubits])))
    print('Probabilities: %s' % (projectq_backend.get_probabilities(qubits),))
    print(projectq_backend.cqasm())

if __name__ == "__main__":

    try:
        backend, engine = login()

        print("logged on")

        naive_qpm(backend, engine)
    except Exception as e:
        print(e)

    k = input("press enter to finish")