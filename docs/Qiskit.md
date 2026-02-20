# Qiskit

Other languages:

- [English](Qiskit.md)
- français

[Qiskit](https://docs.quantum.ibm.com/) est une bibliothèque de programmation quantique à code source ouvert développée en Python par IBM. Comme [PennyLane](PennyLane.md) et [Snowflurry](Snowflurry.md), elle permet de construire, simuler et exécuter des circuits quantiques.

## Installation

1. Chargez les dépendances de Qiskit.

```
[name@server ~]$ module load StdEnv/2023 gcc python/3.11 symengine/0.11.2

```

2. Créez et activez un [environnement virtuel Python](Python_fr.md#Créer_et_utiliser_un_environnement_virtuel).

```
[name@server ~]$ virtualenv --no-download --clear ~/ENV && source ~/ENV/bin/activate

```

3. Installez une version spécifique de Qiskit.

```
(ENV) [name@server ~] pip install --no-index --upgrade pip
(ENV) [name@server ~] pip install --no-index qiskit==X.Y.Z  qiskit_aer==X.Y.Z

```

où `X.Y.Z` représente le numéro de la version, par exemple `1.4.0`. Pour installer la plus récente version disponible sur nos grappes, n'indiquez pas de version. Ici, nous n'avons importé que `qiskit` et `qiskit_aer`. Vous pouvez ajouter d'autres logiciels Qiskit en fonction de vos besoins en suivant la structure `qiskit_package==X.Y.Z` où `qiskit_package` représente le logiciel voulu, par exemple `qiskit-finance`. Les wheels présentement disponibles sont listés sur la page [Wheels Python](Available_Python_wheels_fr.md).

4. Validez l’installation de Qiskit.

```
(ENV)[name@server ~] python -c 'import qiskit'

```

5. Gelez l'environnement et les dépendances.

```
(ENV)[name@server ~] pip freeze --local > ~/qiskit_requirements.txt

```

## Exécuter Qiskit sur une grappe

**File :** script.sh

```
#!/bin/bash
#SBATCH --account=def-someuser #indiquez le nom de votre compte
#SBATCH --time=00:15:00        #modifiez s'il y a lieu
#SBATCH --cpus-per-task=1      #modifiez s'il y a lieu
#SBATCH --mem-per-cpu=1G       #modifiez s'il y a lieu

# Chargez les dépendances des modules.
module load StdEnv/2023 gcc python/3.11 symengine/0.11.2 

# Générez l'environnement virtuel dans $SLURM_TMPDIR.                                                                                                         
virtualenv --no-download ${SLURM_TMPDIR}/env                                                                                                                   
source ${SLURM_TMPDIR}/env/bin/activate  

# Installez Qiskit et ses dépendances.                                                                                                                                                                                                                                                                                    
pip install --no-index --upgrade pip                                                                                                                            
pip install --no-index --requirement ~/qiskit_requirements.txt

#Modifiez le programme Qiskit.                                                                                                                                                                       
python qiskit_example.py

```

Vous pouvez ensuite [soumettre votre tâche à l'ordonnanceur](Running_jobs_fr.md).

## Utiliser Qiskit avec MonarQ (à venir)

## Exemple d'utilisation : États de Bell

Nous allons créer le premier état de Bell sur [Narval](Narval.md) en simulation. Il faut d'abord importer les modules nécessaires.

```
   from qiskit_aer import AerSimulator
   from qiskit import QuantumCircuit
   from qiskit.visualization import plot_histogram

```

Ensuite, nous définissons le circuit. Nous appliquons une porte Hadamard afin de créer un état de superposition sur le premier qubit et nous appliquons ensuite une porte CNOT pour intriquer le premier et le deuxième qubit.

```
   circuit = QuantumCircuit(2)
   circuit.h(0)
   circuit.cx(0,1)
   circuit.measure_all()

```

Nous précisons le simulateur que nous voulons utiliser. `AerSimulator` étant le simulateur par défaut. Nous obtenons le dénombrement des états finaux des qubits après 1000 mesures.

```
   simulator = AerSimulator()
   result = simulator.run(circuit, shots=1000).result()
   counts = result.get_counts()
   print(counts)
   {'00': 489, '11': 535}

```

Nous affichons un histogramme des résultats avec la commande

```
   plot_histogram(counts)

```
[![](/mediawiki/images/thumb/a/a3/Qiskit_counts.png/300px-Qiskit_counts.png)](FileQiskit_countspng.md)

Histogramme des résultats de 1000 mesures sur le premier état de Bell