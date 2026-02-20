# CirQ

Other languages:

- English
- [français](CirQ.md)

Developed by Google, [CirQ](https://quantumai.google/cirq) is an open-source quantum computing library to build, optimize, simulate and run quantum circuits. More specifically, CirQ allows to simulate circuits on particular qubit configurations, which can optimize a circuit for a certain qubit architecture. Information on the features can be found in the CirQ [documentation](https://quantumai.google/cirq) and [GitHub](https://github.com/quantumlib/Cirq). Like [Snowflurry](Snowflurry.md), CirQ can be used to run quantum circuits on the [MonarQ](MonarQ.md) quantum computer.

## Installation

The CirQ simulator is available on all of our clusters. To have access, you must load the [Python](Python_fr.md) language. Il est préférable de travailler dans un [environnement virtuel Python](Python_fr.md#Créer_et_utiliser_un_environnement_virtuel).

```
[name@server ~]$ module load python/3.11
[name@server ~]$ virtualenv --no-download --clear ~/ENV && source ~/ENV/bin/activate
[name@server ~]$ pip install --no-index --upgrade pip
[name@server ~]$ pip install --no-index cirq==1.4.1
[name@server ~]$ python -c "import cirq"
[name@server ~]$ pip freeze > cirq-1.4.1-reqs.txt

```

The last command creates the cirq-1.4.1-reqs.txt file which you can also use in a job script such as in the example below.

## Exécution sur une grappe

**File :** script.sh

```
#!/bin/bash
#SBATCH --account=def-someuser # Modify with your account name
#SBATCH --time=00:15:00        # Modify as needed
#SBATCH --cpus-per-task=1      # Modify as needed
#SBATCH --mem-per-cpu=1G       # Modify as needed

# Load modules dependencies.
module load StdEnv/2023 gcc python/3.11 

# Generate your virtual environment in $SLURM_TMPDIR.                                                                                           
virtualenv --no-download ${SLURM_TMPDIR}/env                                                                                                                   
source ${SLURM_TMPDIR}/env/bin/activate  

# Install CirQ and its dependencies.                                                                                                                                                                                                                                                                                  
pip install --no-index --upgrade pip                                                                                                                            
pip install --no-index --requirement ~/cirq-1.4.1-reqs.txt

# Edit with your CirQ program.                                                                                                                                                             
python cirq_example.py

```

You can then [submit your job to the scheduler](Scheduler.md).

## Use case: Bell states

Les états de Bell sont les états les plus simples qui permettent d'expliquer à la fois la superposition et l'intrication sur des qubits.
La bibliothèque [CirQ](https://github.com/quantumlib/Cirq) permet de construire un état de Bell comme ceci :

```
[name@server ~]$ python
python> import cirq
python> from cirq.contrib.svg import SVGCircuit
python> from cirq import H, CNOT

python> qubits = cirq.LineQubit.range(2)
python> circuit = cirq.Circuit(H.on(qubits[0]),CNOT.on(qubits[0],qubits[1]))
python> circuit.append(cirq.measure(qubits, key='m'))
python> SVGCircuit(circuit)

```

[![Representation of the circuit creating a Bell state](/mediawiki/images/thumb/6/6d/Bell_Circuit_CirQ.png/300px-Bell_Circuit_CirQ.png)](FileBell_Circuit_CirQpng.md)

This code builds and displays a circuit that prepares a Bell state. The H gate (Hadamard gate) creates an equal superposition of |0⟩ and |1⟩ on the first qubit while the CNOT gate (controlled X gate) creates an entanglement between the two qubits. This Bell state is therefore an equal superposition of the states |00⟩ and |11⟩. Simulating this circuit using CirQ allows you to visualize the results. In this diagram, the integer 3 represents the state |11⟩ since 3 is written 11 in binary.

```
[name@server ~]$ python
python> import matplotlib.pyplot as plt
python> s = cirq.Simulator().run(circuit, repetitions=1000)
python> counts = s.histogram(key='m')
python> cirq.plot_state_histogram(counts, plt.subplot())

```

[![Diagramme du résultat de 1000 simulations de l'état de Bell](/mediawiki/images/thumb/a/a1/Bell_Graph_CirQ.png/300px-Bell_Graph_CirQ.png)](FileBell_Graph_CirQpng.md)