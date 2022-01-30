#!/usr/bin/env python

import logging
import random
import math
import os

from projectq import MainEngine
from projectq.setups import linear
from projectq.ops import H, Rx, Rz, CNOT, CZ, Measure, All, StatePreparation

from quantuminspire.credentials import get_authentication
from quantuminspire.api import QuantumInspireAPI
from quantuminspire.projectq.backend_qx import QIBackend

QI_URL = os.getenv('API_URL', 'https://api.quantum-inspire.com/')

authentication = get_authentication()
qi_api = QuantumInspireAPI(QI_URL, authentication)

projectq_backend = QIBackend(quantum_inspire_api=qi_api)

engine = MainEngine(backend=projectq_backend)  # create default compiler (simulator back-end)

qubits = engine.allocate_qureg(5)
q1 = qubits[0]
q2 = qubits[-1]

# Prepare a random state
StatePreparation([(x := random.uniform(0, 1)), (y := math.sqrt(1 - x*x))]) | q2
print(f"original state: {x} {y}")

H | q1
CZ | (q1, q2)
H | q1
All(Measure) | qubits  # measure the qubits

engine.flush()  # flush all gates (and execute measurements)

print("Measured {}".format(','.join([str(int(q)) for q in qubits])))
print('Probabilities: %s' % (projectq_backend.get_probabilities(qubits),))
print(projectq_backend.cqasm())

