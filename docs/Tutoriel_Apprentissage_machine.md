# Tutoriel Apprentissage machine

Other languages:

- [English](Tutoriel_Apprentissage_machine.md)
- français

Cette page constitue un guide de démarrage servant à porter une tâche d'apprentissage automatique (Machine Learning) sur une de nos grappes.

## Étape 1: Enlever tout affichage graphique

Modifiez votre programme afin qu'il n'utilise pas d'affichage graphique. Tout résultat graphique devra être écrit sur le disque dans un fichier, et visualisé sur votre ordinateur personnel, une fois la tâche terminée. Par exemple, si vous affichez des graphiques avec matplotlib, vous devez [enregistrer les graphiques sous forme de fichiers, au lieu de les afficher à l'écran](https://stackoverflow.com/questions/4706451/how-to-save-a-figure-remotely-with-pylab).

## Étape 2: Archivage d'un ensemble de données

Les stockages partagés sur nos grappes ne sont pas optimisés pour gérer un grand nombre de petits fichiers (ils sont plutôt optimisés pour les très gros fichiers). Assurez-vous que l'ensemble de données dont vous aurez besoin pour votre entraînement se trouve dans un fichier archive (tel que "tar"), que vous transférerez sur votre nœud de calcul au début de votre tâche. **Si vous ne le faites pas, vous risquez de causer des lectures de fichiers à haute fréquence du noeud de stockage vers votre nœud de calcul, nuisant ainsi à la performance globale du système**. Si vous voulez apprendre davantage sur la gestion des grands ensembles de fichiers, on vous recommande la lecture de [cette page](https://docs.alliancecan.ca/wiki/Handling_large_collections_of_files/fr).

En supposant que les fichiers dont vous avez besoin sont dans le dossier mydataset:

```
$ tar cf mydataset.tar mydataset/*

```

La commande ci-haut ne compresse pas les données. Si vous croyez que ce serait approprié, vous pouvez utiliser tar czf.

## Étape 3: Préparation de l'environnement virtuel

[Créez un environnement virtuel](Python_fr.md#Cr.C3.A9er_et_utiliser_un_environnement_virtuel) dans votre espace home.

Pour les détails d'installation et d'utilisation des différents frameworks d'apprentissage machine, référéz-vous à notre documentation:

- [PyTorch](PyTorch_fr.md)
- [TensorFlow](TensorFlow_fr.md)

## Étape 4: Tâche interactive (salloc)

Nous vous recommandons d'essayer votre tâche dans une [tâche interactive](Running_jobs_fr.md#T.C3.A2ches_interactives) avant de la soumettre avec un script (section suivante). Vous pourrez ainsi diagnostiquer plus rapidement les problèmes. Voici un exemple de la commande pour soumettre une tâche interactive:

```
$ salloc --account=def-someuser --gres=gpu:1 --cpus-per-task=3 --mem=32000M --time=1:00:00

```

Une fois dans la tâche:

- Activez votre environnement virtuel Python
- Tentez d'exécuter votre programme
- Installez les paquets manquants s'il y a lieu. Les noeuds de calcul n'ayant d'accès à Internet, vous devrez faire l'installation à partir d'un noeud de connexion. Référez-vous à notre [documentation sur les environnements virtuels Python](Python_fr.md#Cr.C3.A9er_et_utiliser_un_environnement_virtuel) pour plus de détails.
- Notez les étapes qui ont été nécessaires pour faire fonctionner le votre programme

**Maintenant est un bon moment pour vérifier que votre tâche lit et écrit le plus possible dans le stockage local au nœud de calcul ($SLURM\_TMPDIR), et le moins possible sur les [systèmes de fichiers partagés (home, scratch, project)](Storage_and_file_management_fr.md).**

## Étape 5: Tâche scriptée (sbatch)

Vous devez [soumettre vos tâches](Running_jobs_fr.md#Soumettre_des_t.C3.A2ches_avec_sbatch) à l'aide de scripts sbatch, afin qu'elles puissent être entièrement automatisées. Les tâches interactives servent uniquement à préparer et à déboguer des tâches qui seront ensuite exécutées entièrement et/ou à grande échelle en utilisant sbatch.

### Éléments importants d'un script sbatch

1. Compte sur lequel les ressources seront "facturées"
2. Ressources demandées:
   1. Nombre de CPU, suggestion: 6
   2. Nombre de GPU, suggestion: 1 (**Utilisez un (1) seul GPU, à moins d'être certain que votre programme en utilise plusieurs. Par défaut, TensorFlow et PyTorch utilisent un seul GPU.**)
   3. Quantité de mémoire, suggestion: 32000M
   4. Durée (Maximum Béluga: 7 jours, Graham et Cedar: 28 jours)
3. Commandes *bash*:
   1. Préparation de l'environnement (modules, virtualenv)
   2. Transfert des données vers le noeud de calcul
   3. Lancement de l'exécutable

### Exemple de script

**File :** ml-test.sh

```
#!/bin/bash
#SBATCH --gres=gpu:1       # Request GPU "generic resources"
#SBATCH --cpus-per-task=3  # Refer to cluster's documentation for the right CPU/GPU ratio
#SBATCH --mem=32000M       # Memory proportional to GPUs: 32000 Cedar, 47000 Béluga, 64000 Graham.
#SBATCH --time=0-03:00     # DD-HH:MM:SS

module load python/3.6 cuda cudnn

SOURCEDIR=~/ml-test

# Prepare virtualenv
source ~/my_env/bin/activate
# You could also create your environment here, on the local storage ($SLURM_TMPDIR), for better performance. See our docs on virtual environments.

# Prepare data
mkdir $SLURM_TMPDIR/data
tar xf ~/projects/def-xxxx/data.tar -C $SLURM_TMPDIR/data

# Start training
python $SOURCEDIR/train.py $SLURM_TMPDIR/data

```

### Morcellement d'une longue tâche

Nous vous recommandons de morceler vos tâches en blocs de 24 heures. Demander des tâches plus courtes améliore votre priorité. En créant une chaîne de tâches, il est possible de dépasser la limite de 7 jours sur Béluga.

1. Modifiez votre script de soumission (ou votre programme) afin que votre tâche puisse être interrompue et continuée. Votre programme doit pouvoir accéder au *checkpoint* le plus récent. (Voir l'exemple de script ci-dessous.)
2. Vérifiez combien d'epochs (ou d'itérations) peuvent être effectuées à l'intérieur de 24 heures.
3. Calculez combien de blocs de 24 heures vous aurez besoin: n\_blocs = n\_epochs\_total / n\_epochs\_par\_24h
4. Utilisez l'argument --array 1-<n\_blocs>%1 pour demander une chaine de n\_blocs tâches.

Le script de soumission ressemblera à ceci:

**File :** ml-test-chain.sh

```
#!/bin/bash
#SBATCH --array=1-10%1   # 10 is the number of jobs in the chain
#SBATCH ...

module load python/3.6 cuda cudnn

# Prepare virtualenv
...

# Prepare data
...

# Get most recent checkpoint
CHECKPOINT_EXT='*.h5'  # Replace by *.pt for PyTorch checkpoints
CHECKPOINTS=~/scratch/checkpoints/ml-test
LAST_CHECKPOINT=$(find $CHECKPOINTS -maxdepth 1 -name "$CHECKPOINT_EXT" -print0 | xargs -r -0 ls -1 -t | head -1)

# Start training
if [ -z "$LAST_CHECKPOINT" ]; then
    # $LAST_CHECKPOINT is null; start from scratch
    python $SOURCEDIR/train.py --write-checkpoints-to $CHECKPOINTS ...
else
    python $SOURCEDIR/train.py --load-checkpoint $LAST_CHECKPOINT --write-checkpoints-to $CHECKPOINTS ...
fi

```