# MonarQ

Other languages:

- [Canadian English](MonarQ-ca.md)
- [English](MonarQ.md)
- français

| Nœud de connexion : https://monarq.calculquebec.ca |
| --- |

**MonarQ est actuellement en cours de maintenance et devrait être opérationnel en février 2026. En attendant, Calcul Québec peut offrir l'accès à une machine similaire mais plus petite, avec 6 qubits.**

MonarQ est un ordinateur quantique supraconducteur à 24 qubits développé à Montréal par [Anyon Systèmes](https://anyonsys.com/) et situé à l'[École de technologie supérieure](http://www.etsmtl.ca/). Pour plus d'informations sur les spécifications et les performances de MonarQ voir Spécifications techniques ci-dessous.

Le nom MonarQ est inspiré par la forme du circuit de qubits sur le processeur quantique qui rappelle le papillon monarque, symbole d’évolution et de migration. La majuscule Q rappelle la nature quantique de l’ordinateur et son origine québécoise. L'acquisition de MonarQ a été rendue possible grâce au soutien du [Ministère de l'Économie, de l'Innovation et de l'Énergie du Québec (MEIE)](https://www.economie.gouv.qc.ca/) et de [Développement Économique Canada (DEC)](https://dec.canada.ca/).

## Accéder à MonarQ

1. Pour commencer le processus d'accès à MonarQ, [remplir ce formulaire](https://forms.gle/zH1a3oB4SGvSjAwh7). Il doit être complété par le chercheur principal.
2. Vous devez [avoir un compte avec l'Alliance](https://alliancecan.ca/fr/services/calcul-informatique-de-pointe/portail-de-recherche/gestion-de-compte/demander-un-compte) pour avoir accès à MonarQ.
3. Rencontrez notre équipe pour discuter des spécificités de votre projet, des accès, et des détails de facturation.
4. Recevoir l'accès au tableau de bord MonarQ et générer votre jeton d'accès.
5. Pour démarrer, voir Premiers pas sur MonarQ ci-dessous.

Contactez notre équipe quantique à quantique@calculquebec.ca si vous avez des questions ou si vous souhaitez avoir une discussion plus générale avant de demander l'accès.

## Spécifications techniques

[![](/mediawiki/images/thumb/b/b8/QPU.png/300px-QPU.png)](FileQPUpng.md)

Cartographie des qubits

À l'instar des processeurs quantiques disponibles aujourd'hui, MonarQ fonctionne dans un environnement où le bruit reste un facteur significatif. Les métriques de performance, mises à jour à chaque calibration, sont accessibles via le portail Thunderhead. L'accès à ce portail nécessite une approbation d'accès à MonarQ.

On y retrouve, entre autres, les métriques suivantes :

- Processeur quantique de 24 qubits
- Porte un qubit avec fidélité de 99.8% et durée de 32ns
- Porte deux qubits avec fidélité de 96% et durée de 90ns
- Temps de cohérence de 4-10μs (en fonction de l'état)
- Profondeur maximale du circuit d'environ 350 pour des portes à un qubit et 115 pour des portes à deux qubits

## Logiciels de calcul quantique

Il existe plusieurs bibliothèques logicielles spécialisées pour faire du calcul quantique et pour développer des algorithmes quantiques. Ces bibliothèques permettent de construire des circuits qui sont exécutés sur des simulateurs qui imitent la performance et les résultats obtenus sur un ordinateur quantique tel que MonarQ. Elles peuvent être utilisées sur toutes les grappes de l’Alliance.

- [PennyLane](PennyLane.md), bibliothèque de commandes en Python
- [Snowflurry](Snowflurry.md), bibliothèque de commandes en Julia
- [Qiskit](Qiskit.md), bibliothèque de commandes en Python

Les portes logiques quantiques du processeur de MonarQ sont appelées par le biais d'une bibliothèque logicielle [Snowflurry](https://github.com/SnowflurrySDK/Snowflurry.jl), écrit en [Julia](https://julialang.org/). Bien que MonarQ soit nativement compatible avec Snowflurry, il existe un plugiciel [PennyLane-CalculQuébec](https://github.com/calculquebec/pennylane-snowflurry\) développé par Calcul Québec permettant d'exécuter des circuits sur MonarQ tout en bénéficiant des fonctionnalités et de l'environnement de développement offerts par [PennyLane](https://docs.alliancecan.ca/wiki/PennyLane).

## Premiers pas sur MonarQ

**Prérequis** : Assurez-vous d’avoir un accès à MonarQ ainsi que vos identifiants de connexion (*username*, *API token*). Pour toute question, écrivez à quantique@calculquebec.ca.

- **Étape 1 : Connectez-vous à [Narval](Narval_fr.md)**
  - MonarQ est uniquement accessible depuis Narval, une grappe de Calcul Québec. L’accès à Narval se fait à partir du nœud de connexion **narval.alliancecan.ca**.
  - Pour de l’aide concernant la connexion à Narval, consultez la page [SSH](SSH_fr.md).

- **Étape 2 : Créez l’environnement** 
  - Créez un environnement virtuel Python (3.11 ou ultérieur) pour utiliser PennyLane et le plugiciel [PennyLane-CalculQuébec](https://github.com/calculquebec/pennylane-snowflurry\). Ces derniers sont déjà installés sur Narval et vous aurez uniquement à importer les bibliothèques logicielles que vous souhaitez.

```
[name@server ~]$ module load python/3.11
[name@server ~]$ virtualenv --no-download --clear ~/ENV && source ~/ENV/bin/activate
[name@server ~]$ pip install --no-index --upgrade pip
[name@server ~]$ pip install --no-index --upgrade pennylane-calculquebec
[name@server ~]$ python -c "import pennylane; import pennylane_calculquebec"

```

- **Étape 3 : Configurez vos identifiants sur MonarQ et définissez MonarQ comme machine (*device*)**
  - Ouvrez un fichier Python .py et importez les dépendances nécessaires soit PennyLane et CalculQuebecClient dans l’exemple ci-dessous.
  - Créez un client avec vos identifiants. Votre jeton est disponible à partir du portail Thunderhead. Le *host* est **https://monarq.calculquebec.ca.**
  - Créez un *device* PennyLane avec votre client. Vous pouvez également mentionner le nombre de qubits (*wires*) à utiliser et le nombre d'échantillons ( *shots*).
  - Pour de l’aide, consultez [pennylane\_calculquebec](https://github.com/calculquebec/pennylane-calculquebec/blob/main/doc/getting_started.ipynb).

**Fichier :** my\_circuit.py

```
import pennylane as qml
from pennylane_calculquebec.API.client import CalculQuebecClient

my_client = CalculQuebecClient(host="https://monarq.calculquebec.ca", user="your username", access_token="your access token", project_id="your project_id")

dev = qml.device("monarq.default", client = my_client, wires = 3)

```

- **Étape 4 : Créez votre circuit**
  - Dans le même fichier Python vous pouvez maintenant coder votre circuit quantique

**Fichier :** my\_circuit.py

```
@qml.set_shots(1000)
@qml.qnode(dev)

def bell_circuit():
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1]) 
    qml.CNOT(wires=[1, 2])
 
    return qml.counts()

result = bell_circuit()
print(result)

```

- **Étape 5 : Exécutez votre circuit depuis l'ordonnanceur**
  - La commande `sbatch` est utilisée pour soumettre une tâche [`sbatch`](https://slurm.schedmd.com/sbatch.html).

```
$ sbatch simple_job.sh
Submitted batch job 123456

```

Avec un script Slurm ressemblant à ceci:

**File :** simple\_job.sh

```
#!/bin/bash
#SBATCH --time=00:15:00
#SBATCH --account=def-someuser # Votre username
#SBATCH --cpus-per-task=1      # Modifiez s'il y a lieu
#SBATCH --mem-per-cpu=1G 	  # Modifiez s'il y a lieu
python my_circuit.py

```

- Le résultat du circuit est écrit dans un fichier dont le nom commence par slurm-, suivi de l'ID de la tâche et du suffixe .out, par exemple *slurm-123456.out*.
- On retrouve dans ce fichier le résultat de notre circuit dans un dictionnaire `{'000': 496, '001': 0, '010': 0, '011': 0, '100': 0, '101': 0, '110': 0, '111': 504}`.
- Pour plus d’information sur comment soumettre des tâches sur Narval, voir [Exécuter des tâches](Running_jobs_fr.md).

## Questions courantes

- [Foire aux questions (FAQ)](https://docs.google.com/document/d/13sfHwJTo5tcmzCZQqeDmAw005v8I5iFeKp3Xc_TdT3U/edit?tab=t.0)

## Autres outils

- [Transpileur quantique](Transpileur_quantique.md)

## Applications

MonarQ est adapté aux calculs nécessitant de petites quantités de qubits de haute fidélité, ce qui en fait un outil idéal pour le développement et le test d'algorithmes quantiques. D'autres applications possibles incluent la modélisation de petits systèmes quantiques; les tests de nouvelles méthodes et techniques de programmation quantique et de correction d'erreurs; et plus généralement, la recherche fondamentale en informatique quantique.

## Soutien technique

Si vous avez des questions sur nos services quantiques, écrivez à quantique@calculquebec.ca.  
Les sessions sur l'informatique quantique et la programmation avec MonarQ sont [listées ici.](https://www.eventbrite.com/o/calcul-quebec-8295332683)