# PennyLane

Other languages:

- English
- [français](PennyLane.md)

[PennyLane](https://pennylane.ai/) is an open-source software platform for differentiable quantum computing that was launched in 2018 by Xanadu, a quantum technology company based in Toronto, Canada. It allows quantum circuits to be designed and run on a variety of quantum simulators and hardware. PennyLane is designed to facilitate the simulation, optimization, and training of hybrid quantum algorithms, which combine classical and quantum processing. [The first version was published as an open-source project on GitHub.](https://github.com/calculquebec/pennylane-snowflurry)

[![](/mediawiki/images/thumb/3/3c/Pennylane_Snowflurry-Diagram1.png/300px-Pennylane_Snowflurry-Diagram1.png)](FilePennylane_Snowflurry-Diagram1png.md)

## Features

PennyLane offers several features to facilitate research and development in differentiable quantum computing.

## Unified quantum interface

PennyLane provides a unified quantum interface that allows you to design quantum circuits and run them on different quantum simulators and hardware. PennyLane supports several popular quantum simulators, such as [Qiskit](Qiskit.md), [CirQ](CirQ.md), Strawberry Field, and QuTip. PennyLane also supports several quantum hardware, including Xanadu, IBM, Rigetti and IonQ quantum devices.

Calcul Québec has developed a [PennyLane-CalculQuebec plugin](https://github.com/calculquebec/pennylane-snowflurry\) that uses the PennyLane interface to design and run quantum circuits on [MonarQ](MonarQ.md).

### Integration with machine learning libraries

PennyLane seamlessly integrates with popular machine learning libraries such as [TensorFlow](TensorFlow.md) and [PyTorch](PyTorch.md), allowing you to use machine learning tools to build hybrid quantum machine learning models and optimize quantum circuits.

### Quantum circuit optimization

Using differentiable optimization techniques and combining classical and quantum differentiation methods, PennyLane optimizes quantum circuit parameters to solve a variety of problems

### Visualization tools

PennyLane provides visualization tools to help understand how quantum circuits work.

### Community and development

PennyLane is an open-source project with an active community of developers and users. The project is constantly updated with new features and improvements, and anyone can contribute to the development of the platform.

## Using PennyLane with MonarQ

[MonarQ](MonarQ.md) is designed to be programmed with [Snowflurry](Snowflurry.md), a Julia-based software library developed by Anyon Systems. However, with the PennyLane-CalculQuebec plugin, PennyLane circuits can be created using Snowflurry in the background. This allows circuits to be run on [MonarQ](MonarQ.md) while still benefiting from the features and development environment offered by PennyLane. See the [PennyLane-CalculQuebec documentation for installation and usage guides](https://github.com/calculquebec/pennylane-snowflurry\).

A [quantum transpiler](Transpileur_quantique_fr.md) is also available to optimize PennyLane circuits on MonarQ.

## Creating a virtual environment

[Let’s create a virtual environment](Python.md#Creating_and_using_a_virtual_environment) to use PennyLane.

```
[name@server ~]$ module load python/3.11
[name@server ~]$ virtualenv --no-download --clear ~/ENV && source ~/ENV/bin/activate
[name@server ~]$ pip install --no-index --upgrade pip
[name@server ~]$ pip install --no-index pennylane==X.Y.Z
[name@server ~]$ python -c "import pennylane"

```

where X.Y.Z is the version number.

You can also put the last three commands in a pennylane-reqs.txt file and call the file inside a session with the commands

```
[name@server ~]$ module load python/3.11
[name@server ~]$ pip install --no-index -r pennylane-reqs.txt

```

## Running PennyLane on a cluster

**File :** script.sh

```
#!/bin/bash
#SBATCH --account=def-someuser # use the name of your account
#SBATCH --time=00:15:00        # change if needed
#SBATCH --cpus-per-task=1      # change if needed
#SBATCH --mem-per-cpu=1G       # change if needed

# Load modules dependencies.
module load StdEnv/2023 gcc python/3.11 

# Generate the virtual environment in $SLURM_TMPDIR.                                                                                                         
virtualenv --no-download ${SLURM_TMPDIR}/env                                                                                                                   
source ${SLURM_TMPDIR}/env/bin/activate  

# Install Pennylane and its dependencies.                                                                                                                                                                                                                                                                                    
pip install --no-index --upgrade pip                                                                                                                            
pip install --no-index --requirement ~/pennylane_requirements.txt

# Modify your PennyLane program.                                                                                                                                                                       
python pennylane_example.py

```

You can now [submit the job to the scheduler](Scheduler.md).

## Use case: Bell states

Let's start by creating the virtual environment, as described above.

We will then generate the first Bell state using PennyLane.

```
   import pennylane as qml

```
```
  #  Define the quantum circuit to generate the first Bell state.
   def bell_circuit():
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])

```
```
  # Define the quantum circuit simulator.
   dev = qml.device('default.qubit', wires=2)

```
```
  # Define the quantum circuit as a QNode function. 
   @qml.qnode(dev)
   def generate_bell_state():
    bell_circuit()
    return qml.state()

```
```
  # Generate and display the first Bell state.
   bell_state_0 = generate_bell_state()
  print("First Bell State :", bell_state_0)
  Premier état de Bell :[0.70710678+0.j 0.        +0.j 0.        +0.j 0.70710678+0.j]

```

## References

- [PennyLane official website](https://pennylane.ai\)
- [PennyLane documentation on GitHub](https://github.com/PennyLaneAI/pennylane\)
- [PennyLane-CalculQuebec](https://github.com/calculquebec/pennylane-snowflurry\)