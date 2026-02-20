# TamIA

Other languages:

- [English](TamIA.md)
- français

| Disponibilité : 31 mars 2025 |
| --- |
| Nœud de connexion : tamia.alliancecan.ca |
| Nœud d'automatisation : robot.tamia.ecpia.ca |
| Collection Globus : TamIA's Globus v5 Server |
| Nœud de copie (rsync, scp, sftp,...) : tamia.alliancecan.ca |
| Portail : https://portail.tamia.ecpia.ca/ |

tamIA est une grappe dédiée aux besoins de la communauté scientifique canadienne en matière d'intelligence artificielle. tamIA est située à [l'Université Laval](http://www.ulaval.ca/) et est co-gérée avec [Mila](https://mila.quebec/) et [Calcul Québec](https://calculquebec.ca/). Son nom rappelle le [tamia](https://fr.wikipedia.org/wiki/Tamia), un mammifère rongeur présent en Amérique du Nord.

Cette grappe fait partie de [l'environnement de calcul pancanadien de l’IA (ECPIA)](https://alliancecan.ca/fr/services/calcul-informatique-de-pointe/environnement-informatique-pancanadien-de-lia-eipia)

## Particularités

- Notre politique veut que les nœuds de calcul de tamIA n'aient pas accès à l'internet. Pour y faire exception, veuillez joindre le [soutien technique](Technical_support_fr.md) en expliquant ce dont vous avez besoin et pourquoi.
- Notez que l'outil `crontab` n'est pas offert.
- Notez que l'environnement de développement intégré *[VSCode](https://code.visualstudio.com/)* est ***interdit*** sur les noœuds ***frontaux*** (*login nodes*) en raison de sa lourde charge. Il est encore autorisé sur les nœuds de calcul.
- Chaque tâche devrait être d'une durée d’au moins une heure (au moins cinq minutes pour les tâches de test) et vous ne pouvez pas avoir plus de 1000 tâches (en exécution et en attente) à la fois.
- La durée maximale d'une tâche est d'une journée (24 heures).
- Chaque tâche doit utiliser tous les GPUs des serveurs alloués, soit 4 pour les h100 et 8 pour les h200.

## Accès

Pour accéder à la grappe de calcul, chaque chercheuse ou chercheur doit [compléter une demande d'accès dans la CCDB](https://ccdb.alliancecan.ca/me/access_services). L'accès effectif à la grappe peut prendre jusqu'à une heure après avoir complété la demande d'accès. Puis, une [déclaration de l'utilisation envisagée de l'intelligence artificielle](https://ccdb.alliancecan.ca/paice/general_access_to_paice_systems) doit être soumise.

Les chercheuses principales et chercheurs principaux admissibles sont membres d'un RAP de type AIP (préfixe `aip-`).

La procédure pour parrainer d'autres chercheuses et chercheurs est la suivante:

- Sur la **[page d'accueil de la CCDB](https://ccdb.alliancecan.ca/)**, consulter la table *Projet avec allocation de ressources*;
- Chercher le RAPI du projet `aip-` et cliquer dessus pour être redirigé vers la page de gestion du RAP;
- En bas de la page de gestion du RAP, cliquer sur **Gérer l'appartenance aux projets**;
- Dans la section *Ajouter des membres*, entrer le CCRI du membre à ajouter.

La grappe de calcul est accessible uniquement à partir du Canada.

## Stockage

| HOME Système de fichiers Lustre | Cet espace est petit et ne peut pas être agrandi : vous devrez utiliser votre espace project pour les grands besoins en stockage. Petits quotas fixes par utilisateur Il n'y a actuellement aucune sauvegarde automatique. (Planifié pour le printemps 2026) |
| --- | --- |
| SCRATCH Système de fichiers Lustre | Grand espace pour stocker les fichiers temporaires pendant les calculs Pas de système de sauvegarde automatique Grands quotas fixes par utilisateur Il y a une purge automatique des vieux fichiers dans cet espace. |
| PROJECT Système de fichiers Lustre | Cet espace est conçu pour le partage de données entre membres d'un groupe et pour le stockage de beaucoup de données. Grands quotas ajustables par projet Il y a une sauvegarde automatique une fois par jour. |

Au tout début de la présente page, un tableau indique plusieurs adresses de connexion. Pour les transferts de données par [Globus](Globus_fr.md), il faut utiliser le **Point de chute Globus**. Par contre, pour les outils comme [rsync](Transferring_data_fr.md#rsync) et [scp](Transferring_data_fr.md#SCP), il faut utiliser l'adresse du **Nœud de copie**.

## Réseautique haute performance

Le réseau [InfiniBand](https://fr.wikipedia.org/wiki/Bus_InfiniBand) [NDR de Nvidia](https://www.nvidia.com/en-us/networking/quantum2/) relie tous les nœuds de la grappe. Chaque GPU est connecté à un port NDR200 via une carte Nvidia ConnectX-7. Chaque serveur a donc 4 ou 8 ports NDR200 de connectés sur la fabrique Infiniband.

Le réseau Infiniband est non bloquant pour les serveurs de calculs et est composé de 2 étages de commutateurs disposés dans une topologie "fat-tree". Le stockage et les nœuds de calcul sont reliés via 4 ou 8 connexions à 400Gb/s au cœur du réseau.

## Caractéristiques des nœuds

| nœuds | cœurs | mémoire disponible | CPU | stockage | GPU |
| --- | --- | --- | --- | --- | --- |
| 12 | 64 | 1024GB | 2 x Intel Xeon Gold 6448Y 2,1 GHz, 32C | 1 x SSD de 7.68TB | 8 x NVIDIA HGX H200 SXM 141GB HBM3 700W, connectés via NVLink |
| 53 | 48 | 512GB | 2 x Intel Xeon Gold 6442Y 2,6 GHz, 24C | 1 x SSD de 7.68TB | 4 x NVIDIA HGX H100 SXM 80GB HBM3 700W, connectés via NVLink |
| 8 | 64 | 512GB | 2 x Intel Xeon Gold 6438M 2.2G, 32C/64T | 1 x SSD de 7.68TB | Aucun |

### Environnements logiciels disponibles

[L'environnement logiciel standard StdEnv/2023](Standard_software_environments_fr.md) est l'environnement par défaut sur tamIA.

### Tâches GPU

Les tâches sont assignées sur les nœuds complets. Utilisez une des options Slurm suivantes :

Pour une tâche sur un nœud avec GPU H100 : `--gpus=h100:4`

Pour une tâche sur un nœud avec GPU H200 : `--gpus=h200:8`

Pour les tâches avec plusieurs nœuds, utiliser `--gpus-per-nodes=h100:4` ou `--gpus-per-nodes=h200:8`.

## Suivi de vos tâches

Depuis le [portail](https://portail.tamia.ecpia.ca/), vous pourrez suivre vos tâches de calcul GPU comme CPU **en temps réel** ou celles passées afin de maximiser l'utilisation des ressources et diminuer vos temps d'attente dans la file.

Vous pourrez notamment visualiser pour une tâche :

- l'utilisation des cœurs de calcul;
- la mémoire utilisée;
- l'utilisation de GPU.

Il est important d'utiliser les ressources allouées et de rectifier vos demandes lorsque les ressources de calcul sont peu ou pas utilisées.
Par exemple, si vous demandez quatre cœurs (CPU) mais n'en utilisez qu'un seul, vous devez ajuster votre fichier de soumission en conséquence.