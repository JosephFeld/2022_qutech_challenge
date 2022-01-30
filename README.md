# Quantum Error Correction
#### David Vulakh, Anna Rose Osofsky, Jacob Prtizker, Joseph Feld

## Implementing a 3-qubit bit flip code

We implemented a 3-qubit error correcting code. This ended up being a nontrivial project since only 2-qubit gates involving qubit #2 can be done on the starmon-5, so we had to add SWAP gates to move qubits to position 2 as necessary.  

The standard 3-qubit code has 3 classically controlled X gates based on measurements, but the starmon-5 can only do a single round of measurement. Instead, we used CNOT gates and one measurement of the whole system at the end.  



## QPM Ordering

The QPM ([Quantum Parity Measurement](https://en.wikipedia.org/wiki/Parity_measurement)) is an important component of the 5-qubit error correcting code. We don't have enough qubits on the starmon-5 to implement the full 5-qubit code's parity measurement, so we investigated a simple case of 2 qubits: using a controlled X on the first qubit and a controlled Z on the second. These operations are commutative, so we can swap them without changing the actual logic. However, perhaps these could have an effect on the noise. Here are the results from our comparison:  

### CZ then CNOT circuit

![CZ then CNOT](circuit-CZ%20then%20CNOT.png)

#### Histograms

##### Round 1

![CZ then CNOT histogram](cz%20then%20cnot%20histo.PNG)

##### Round 2

![CZ then CNOT histogram](cz%20then%20cnot%20round%202%20histo.PNG)

### CNOT then CZ circuit

![CNOT then CZ](circuit-CNOT%20then%20CZ.png)

#### Histograms

##### Round 1

![CZ then CNOT histogram](cnot%20then%20cz%20histo.PNG)

##### Round 2

![CZ then CNOT histogram](CNOT%20then%20CZ%20round%202%20histo.PNG)

### Analysis

When we look at the incidence of the clearly incorrect results, the CZ then CNOT case does slightly better, but we doubt that it's statistically signifcant.  


## Bulk experiment running

In ```bulk_experiment.py```, you can define an experiment by putting the circuit in the definition of ```experiment()```. Then you can select the number of runs by setting the value of ```num_rums```. The script will then do that number of experiments and combine the results of all the experiments into one probability distribution. This allows you to get results with more statistical significance while still having the shot cap on an individual experiment.