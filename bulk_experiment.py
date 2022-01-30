import logging
import os

from projectq import MainEngine
from projectq.setups import linear
from projectq.ops import H, Rx, Rz, CNOT, CZ, Measure, All

from quantuminspire.credentials import get_authentication
from quantuminspire.api import QuantumInspireAPI
from quantuminspire.projectq.backend_qx import QIBackend

import matplotlib.pyplot as plt

# h = ry pi/2, rx pi

# same as rz pi, ry pi/2

# Return engine
def login(authentication):


    print("setting up api")

    qi_api = QuantumInspireAPI(QI_URL, authentication)

    print("setting up backend")

    projectq_backend = QIBackend(quantum_inspire_api=qi_api)

    print("setting up engine")

    engine = MainEngine(backend=projectq_backend)  # create default compiler (simulator back-end)

    return projectq_backend, engine

#returns probabilities
def experiment(projectq_backend, engine):

    qubits = engine.allocate_qureg(5)
    q1 = qubits[0]
    q2 = qubits[1]


    H | q1  # apply a Hadamard gate
    CNOT | (q1, q2)
    H | q1


    #H | q1

    All(Measure) | qubits  # measure the qubits

    engine.flush()  # flush all gates (and execute measurements)

    #print("Measured {}".format(','.join([str(int(q)) for q in qubits])))
    #print('Probabilities: %s' % (projectq_backend.get_probabilities(qubits),))
    #print(projectq_backend.cqasm())

    return projectq_backend.get_probabilities(qubits)

if __name__ == "__main__":

    QI_URL = os.getenv('API_URL', 'https://api.quantum-inspire.com/')

    authentication = get_authentication()

    num_runs = 1

    try:


        results = []

        for run_index in range(num_runs):
            print("doing run #{}".format(run_index))

            backend, engine = login(authentication)

            print("logged on")

            probs = experiment(backend, engine)

            print(probs)

            results.append(probs)

        #plt.hist([x['00000'] for x in results])
        #plt.show()

        total_results = {}

        for key in results[0]:
            total_results[key] = sum(x[key] for x in results)/num_runs

        print(total_results)



    except Exception as e:
        print(e)

    k = input("press enter to finish")