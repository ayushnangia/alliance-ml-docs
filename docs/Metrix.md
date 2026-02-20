# Metrix

Other languages:

- English
- [français](Metrix.md)

# Summary

[![](/mediawiki/images/thumb/7/71/Aper%C3%A7u_de_la_page_d%27accueil_du_portail.png/900px-Aper%C3%A7u_de_la_page_d%27accueil_du_portail.png)](FileAperçu_de_la_page_daccueil_du_portailpng.md)

The Metrix portal is a website for Alliance users. It collects information on compute nodes and management servers, to interactively generate data that allow users to track their resource usage (CPU, GPU, memory, filesystem) in real time.

| Rorqual | https://metrix.rorqual.alliancecan.ca |
| --- | --- |
| Narval | https://portail.narval.calculquebec.ca |
| Nibi | https://portal.nibi.sharcnet.ca |

**Filersystem performance**

Here you have the graphs for bandwidth and metadata operations, along with viewing options (last week, last day and last hour).

**Login nodes**

CPU, memory, system load, and network usage statistics are presented, with viewing options (last week, last day, and last hour).

**Scheduling**

This tab shows statistics for the cluster's allocated cores and GPUs, with viewing options (last week, last day, and last hour).

**Scientific software**

These graphs show the software with CPU cores and GPUs that are more frequently used.

**Data transfer nodes**

Bandwidth statistics for data transfer nodes are presented under this tab.

# User summary

Under this tab, you find your quotas for various filesystems, followed by your 10 last tasks. You can select a task by its number to see the details. Also, by clicking on (More Details), you are redirected to the *Task statistics* tab, where all your tasks are listed.

[![](/mediawiki/images/thumb/9/9a/Home.png/900px-Home.png)](FileHomepng.md)

[![](/mediawiki/images/thumb/b/b9/Scratch.png/900px-Scratch.png)](FileScratchpng.md)

[![](/mediawiki/images/thumb/9/92/Project.png/900px-Project.png)](FileProjectpng.md)

[![](/mediawiki/images/thumb/d/d4/Portail_utilisateur_10_derni%C3%A8res_t%C3%A2ches.png/900px-Portail_utilisateur_10_derni%C3%A8res_t%C3%A2ches.png)](FilePortail_utilisateur_10_dernières_tâchespng.md)

# Task statistics

The first block shows your current usage (CPU core, memory, and GPUs). These statistics represent the average resources used by all currently running tasks. You can easily compare the resources allocated to you with those you actually use.

[![](/mediawiki/images/thumb/0/01/Utilisation_en_cours.png/900px-Utilisation_en_cours.png)](FileUtilisation_en_courspng.md)

You then have access to an average of the last few days, presented in the form of a graph.

[![](/mediawiki/images/thumb/e/ea/Coeur_CPU_M%C3%A9moire.png/900px-Coeur_CPU_M%C3%A9moire.png)](FileCoeur_CPU_Mémoirepng.md)

You then have a representation of your activity on the filesystems. On the left, the graph shows the number of disk write commands you have performed. (*input/output operations per second (IOPS)*) On the right, you see the amount of data transferred to the servers over a given period. (Bandwidth)

[![](/mediawiki/images/thumb/b/b9/Syst%C3%A8me_de_fichier.png/900px-Syst%C3%A8me_de_fichier.png)](FileSystème_de_fichierpng.md)

The next section shows all the tasks you have already started, which are currently running or pending. In the top left corner, you can filter tasks by their status (OOM, completed, running, etc.). In the top right corner, you can search by job ID or by name. Finally, in the bottom right corner, there is an option to quickly navigate between pages by performing multiple jumps.

[![](/mediawiki/images/thumb/8/8f/Vos_t%C3%A2ches_top-2.png/900px-Vos_t%C3%A2ches_top-2.png)](FileVos_tâches_top-2png.md)

[![](/mediawiki/images/thumb/9/9f/Vos_t%C3%A2ches_bottom-2.png/900px-Vos_t%C3%A2ches_bottom-2.png)](FileVos_tâches_bottom-2png.md)

## CPU task page

At the top, you see the task name, its number, your username, and the status. Details of your submission script are displayed by clicking on Voir le script de la tâche. If the task was launched in interactive mode, the submission script will not be available.

[![](/mediawiki/images/thumb/7/75/D%C3%A9tails_sur_la_t%C3%A2che-2.png/900px-D%C3%A9tails_sur_la_t%C3%A2che-2.png)](FileDétails_sur_la_tâche-2png.md)

Le répertoire de travail et la commande de soumission sont accessibles en cliquant sur Voir la commande de soumission.

[![](/mediawiki/images/thumb/1/15/Commande_de_soumission-3.png/900px-Commande_de_soumission-3.png)](FileCommande_de_soumission-3png.md)

La prochaine section est dédiée aux informations de l'ordonnanceur. Vous pouvez accéder à la page de suivi de votre compte CPU en cliquant sur le numéro de votre compte.

[![](/mediawiki/images/thumb/3/33/Information_ordonnanceur-2.png/900px-Information_ordonnanceur-2.png)](FileInformation_ordonnanceur-2png.md)

Dans la section **Ressources** vous pouvez obtenir un aperçu initial de l'utilisation des ressources de votre tâche en comparant les colonnes **Alloués** et **Utilisés** pour les différents paramètres listés.

[![](/mediawiki/images/thumb/6/67/Ressources.png/900px-Ressources.png)](FileRessourcespng.md)

Le graphique **CPU** vous permet de visualiser, dans le temps, des cœurs CPUs que vous avez demandés. À droite, vous pouvez sélectionner/désélectionner les différents cœurs selon vos besoins. Notez que pour des tâches très courtes, ce graphique n'est pas disponible.

[![](/mediawiki/images/thumb/f/f1/Ressources_utilis%C3%A9es_d%C3%A9tails-2.png/900px-Ressources_utilis%C3%A9es_d%C3%A9tails-2.png)](FileRessources_utilisées_détails-2png.md)

Le graphique **Mémoire** vous permet de visualiser, dans le temps, l'utilisation de la mémoire que vous avez demandée.

[![](/mediawiki/images/thumb/6/63/M%C3%A9moire.png/900px-M%C3%A9moire.png)](FileMémoirepng.md)

Le graphique **Process and threads** vous permet d'observer différents paramètres liés aux processus et aux fils d'exécution. Idéalement, pour une tâche multifils (multithreading), l'addition du paramètre **Running threads** et **Sleeping threads** ne devrait pas dépasser de 2 fois le nombre de cœurs demandé. Cela dit, il est tout à fait normal d'avoir quelques processus en mode **dormant** (*Sleeping threads*) pour certain type de programmes (java, Matlab, logiciels commercial ou programmes complexes). Vous avez aussi en paramètre les applications du programme exécutées au fil du temps.

[![](/mediawiki/images/thumb/8/8f/Process_and_threads.png/900px-Process_and_threads.png)](FileProcess_and_threadspng.md)

Les graphiques suivants représentent l'utilisation du système de fichier pour la tâche en cours et non du nœud au complet. À gauche, une représentation du nombre d’opérations d’entrée/sortie par seconde (IOPS) est affichée. À droite, le graphique illustre le débit de transfert de données entre la tâche et le système de fichiers au fil du temps. Ce graphique permet d’identifier les périodes d’activité intense ou de faible utilisation du système de fichiers.

[![](/mediawiki/images/thumb/d/d2/Syst%C3%A8me_de_fichier_-2.png/900px-Syst%C3%A8me_de_fichier_-2.png)](FileSystème_de_fichier_-2png.md)

Resource statistics for the entire node may be inaccurate if the node is shared by multiple users. The graph on the left shows the evolution of the bandwidth used by the task over time, in relation to software, licenses, etc. The graph on the right shows the evolution of the network bandwidth used by a task or a set of tasks via the Infiniband network, over time. We can observe periods of massive data transfer (e.g., reading/writing on a filesystem (Lustre), MPI communication between nodes).

Le graphique de gauche illustre l’évolution du nombre d’opérations d’entrée/sortie par seconde (IOPS) effectuées sur le disque local au fil du temps. Celui de droite montre l’évolution de la bande passante utilisée sur le disque local au fil du temps, c’est-à-dire la quantité de données lues ou écrites par seconde.

[![](/mediawiki/images/thumb/a/ab/IOPS%2C_bande_passante.png/900px-IOPS%2C_bande_passante.png)](FileIOPS_bande_passantepng.md)

Use of local disk space

[![](/mediawiki/images/thumb/f/f2/Espace_utilis%C3%A9_sur_le_disque_local.png/900px-Espace_utilis%C3%A9_sur_le_disque_local.png)](FileEspace_utilisé_sur_le_disque_localpng.md)

Capacity used

[![](/mediawiki/images/thumb/f/f4/Puissance.png/900px-Puissance.png)](FilePuissancepng.md)

## Page d'une tâche CPU (vecteur de tâches, *job array*)

La page d'une tâche CPU dans un vecteur de tâches est identique à celle d'une tâche CPU régulière, à l'exception de la section *Other jobs in the array*. Le tableau liste les autres numéros de tâches faisant partie du même vecteur de tâches, ainsi que des informations sur leur statut, leur nom, leur heure de début et leur heure de fin.

[![](/mediawiki/images/thumb/6/67/CPU_job_array.png/900px-CPU_job_array.png)](FileCPU_job_arraypng.md)

## Page d'une tâche GPU

En haut de page, vous avez le nom de la tâche, son numéro et votre nom d'utilisateur ainsi que le statut. Les détails de votre script de soumission s'affichent en cliquant sur Voir le script de la tâche. Si vous avez lancé une tâche interactive, le script de soumission n'est pas disponible.

[![](/mediawiki/images/thumb/b/b5/D%C3%A9tail_de_la_t%C3%A2che.png/900px-D%C3%A9tail_de_la_t%C3%A2che.png)](FileDétail_de_la_tâchepng.md)

Le répertoire et la commande de soumission sont accessibles en cliquant sur Voir la commande de soumission.

[![](/mediawiki/images/thumb/c/c8/Commande_de_soumission-GPU.png/900px-Commande_de_soumission-GPU.png)](FileCommande_de_soumission-GPUpng.md)

La section suivante est réservée aux informations de l'ordonnanceur. Vous pouvez accéder à la page de votre compte GPU en cliquant sur le numéro de votre compte.

[![](/mediawiki/images/thumb/6/6a/Information_ordonnanceur-GPU.png/900px-Information_ordonnanceur-GPU.png)](FileInformation_ordonnanceur-GPUpng.md)

Dans la section **Ressources** vous pouvez obtenir un premier aperçu de l'utilisation des ressources de votre tâche en comparant les colonnes **Alloués** et **Utilisés** pour les différents paramètres listés.

[![](/mediawiki/images/thumb/0/01/Ressources-GPU.png/900px-Ressources-GPU.png)](FileRessources-GPUpng.md)

Le graphique **CPU** vous permet de visualiser l'utilisation des cœurs CPUs demandés au fil du temps. À droite, vous pouvez sélectionner/désélectionner les différents cœurs selon vos besoins. Notez que pour des tâches très courtes, ce graphique n'est pas disponible.

[![](/mediawiki/images/thumb/d/d7/CPU_ressources_utilis%C3%A9s_d%C3%A9tails.png/900px-CPU_ressources_utilis%C3%A9s_d%C3%A9tails.png)](FileCPU_ressources_utilisés_détailspng.md)

Le graphique **Mémoire** vous permet de visualiser l'utilisation dans le temps de la mémoire que vous avez demandée pour les CPU.

[![](/mediawiki/images/thumb/8/86/M%C3%A9moire-GPU.png/900px-M%C3%A9moire-GPU.png)](FileMémoire-GPUpng.md)

Le graphique **Process and threads** vous permet d'observer différents paramètres liés aux processus et aux fils d'exécution.

[![](/mediawiki/images/thumb/b/b1/Processes_and_threads-GPU.png/900px-Processes_and_threads-GPU.png)](FileProcesses_and_threads-GPUpng.md)

Les graphiques suivants représentent l'utilisation du système de fichier pour la tâche en cours et non du nœud au complet. À gauche, une représentation du nombre d’opérations d’entrée/sortie par seconde (IOPS) est affichée. À droite, le graphique illustre le débit de transfert de données entre la tâche et le système de fichiers au fil du temps. Ce graphique permet d’identifier les périodes d’activité intense ou de faible utilisation du système de fichiers.

[![](/mediawiki/images/thumb/f/f4/Systeme_de_fichiers-GPU.png/900px-Systeme_de_fichiers-GPU.png)](FileSysteme_de_fichiers-GPUpng.md)

Le graphique GPU représente votre utilisation des GPU. Le paramètre *Streaming Multiprocessors* (SM) active indique le pourcentage de temps pendant lequel le GPU exécute un warp (un groupe de *threads* consécutifs) dans la dernière fenêtre d’échantillonnage. Cette valeur devrait idéalement se situer autour de 80 %. Pour le *SM occupancy* (défini comme le rapport entre le nombre de warps affectés à un SM et le nombre maximal de warps qu’un SM peut gérer), une valeur autour de 50 % est généralement attendue. Concernant le paramètre *Tensor*, la valeur devrait être la plus élevée possible. Idéalement, votre code devrait exploiter cette partie du GPU, optimisée pour les multiplications et convolutions de matrices multidimensionnelles. Enfin, pour les opérations en virgule flottante (*Floating Point*) FP64, FP32 et FP16, vous devriez observer une activité significative sur un seul de ces types, selon la précision utilisée par votre code.

[![](/mediawiki/images/thumb/1/12/GPU_cycles_de_calcul_utilis%C3%A9.png/900px-GPU_cycles_de_calcul_utilis%C3%A9.png)](FileGPU_cycles_de_calcul_utilisépng.md)

À gauche, vous avez un graphique indiquant la mémoire utilisée par le GPU. À droite, un graphique des cycles d'accès du GPU à la mémoire, représentant le pourcentage de cycles pendant lesquels l’interface mémoire de l’appareil est active pour envoyer ou recevoir des données.

[![](/mediawiki/images/thumb/9/9d/M%C3%A9moire_GPU.png/900px-M%C3%A9moire_GPU.png)](FileMémoire_GPUpng.md)

Le graphique de puissance GPU affiche l’évolution de la consommation énergétique (en watts) du GPU au fil du temps.

[![](/mediawiki/images/thumb/c/ce/Puissance_GPU.png/900px-Puissance_GPU.png)](FilePuissance_GPUpng.md)

À gauche, la bande passante GPU sur le bus PCIe (ou **PCI Express**, pour *Peripheral Component Interconnect Express*). À droite, bande passante GPU sur le bus NVlink. Le bus NVLink est une technologie développée par NVIDIA pour permettre une communication ultra-rapide entre plusieurs GPU.

[![](/mediawiki/images/thumb/7/74/Bande_passante-GPU.png/900px-Bande_passante-GPU.png)](FileBande_passante-GPUpng.md)

Pour les statistiques des ressources du nœud au complet, sachez quelles peuvent être imprécises si le nœud est partagé entre plusieurs utilisateurs. Le graphique de gauche, illustre l'évolution de la bande passante utilisée par la tâche au fil du temps, en lien avec les logiciels, les licences, etc. Le graphique de droite représente l’évolution de la bande passante réseau utilisée par une tâche ou un ensemble de tâches via le réseau Infiniband, au fil du temps. On peut y observer les périodes de transfert massif de données (ex. : lecture/écriture sur un système de fichiers (Lustre), communication MPI entre nœuds).

[![](/mediawiki/images/thumb/0/0d/Ressources_du_noeud.png/900px-Ressources_du_noeud.png)](FileRessources_du_noeudpng.md)

Le graphique de gauche illustre l’évolution du nombre d’opérations d’entrée/sortie par seconde (IOPS) effectuées sur le disque local au fil du temps. Celui de droite montre l’évolution de la bande passante utilisée sur le disque local au fil du temps, c’est-à-dire la quantité de données lues ou écrites par seconde.

[![](/mediawiki/images/thumb/0/0c/IOPS.png/900px-IOPS.png)](FileIOPSpng.md)

Use of local disk space

[![](/mediawiki/images/thumb/c/ca/Espace_utilis%C3%A9.png/900px-Espace_utilis%C3%A9.png)](FileEspace_utilisépng.md)

Capacity used

[![](/mediawiki/images/thumb/a/a8/Puissance_utilis%C3%A9.png/900px-Puissance_utilis%C3%A9.png)](FilePuissance_utilisépng.md)

# Account statistics

La section **Statistique d'un compte** regroupe l'utilisation de votre groupe dans deux sous-sections: CPU et GPU.

[![](/mediawiki/images/thumb/6/69/Portail_Utilisateur_vos_comptes.png/900px-Portail_Utilisateur_vos_comptes.png)](FilePortail_Utilisateur_vos_comptespng.md)

## CPU account statistics

Vous y trouverez la somme des demandes de votre groupe pour les cœurs CPU, ainsi que leur utilisation correspondante au cours des derniers mois. Vous pouvez également suivre l'évolution de votre priorité, qui varie en fonction de votre utilisation.

[![](/mediawiki/images/thumb/6/66/Utilisation_du_compte.png/900px-Utilisation_du_compte.png)](FileUtilisation_du_comptepng.md)

This graph shows the applications that are used more frequently.

[![](/mediawiki/images/thumb/3/3b/Application_used_CPU.png/900px-Application_used_CPU.png)](FileApplication_used_CPUpng.md)

Vous pouvez consulter ici l'utilisation des ressources par chacun des utilisateurs de votre groupe.

[![](/mediawiki/images/thumb/5/50/Utilisation_d%C3%A9taill%C3%A9e_par_utilisateur.png/900px-Utilisation_d%C3%A9taill%C3%A9e_par_utilisateur.png)](FileUtilisation_détaillée_par_utilisateurpng.md)

This graph shows the CPU cores wasted by each user, over time.

[![](/mediawiki/images/thumb/4/40/Coeur_CPU_gaspill%C3%A9.png/900px-Coeur_CPU_gaspill%C3%A9.png)](FileCoeur_CPU_gaspillépng.md)

Vous pouvez consulter ici l’utilisation de la mémoire par chacun des utilisateurs de votre groupe.

[![](/mediawiki/images/thumb/4/4b/M%C3%A9moire_compte.png/900px-M%C3%A9moire_compte.png)](FileMémoire_comptepng.md)

This graph shows the memory wasted by each user.

[![](/mediawiki/images/thumb/c/ce/M%C3%A9moire_gaspill%C3%A9e.png/900px-M%C3%A9moire_gaspill%C3%A9e.png)](FileMémoire_gaspilléepng.md)

Vous avez ensuite une représentation de votre activité sur les systèmes de fichiers. À gauche, le graphique montre le nombre de commandes d’écriture sur disque que vous avez effectuées. (input/output operations per second (IOPS)) À droite, vous voyez la quantité de données transférées vers les serveurs sur une période donnée. (Bande passante)

[![](/mediawiki/images/thumb/9/9f/Syst%C3%A8me_de_fichier_compte.png/900px-Syst%C3%A8me_de_fichier_compte.png)](FileSystème_de_fichier_comptepng.md)

Vous avez une liste des dernières tâches qui ont été effectuées pour l'ensemble du groupe.

[![](/mediawiki/images/thumb/1/11/T%C3%A2ches_en_cours-1.png/900px-T%C3%A2ches_en_cours-1.png)](FileTâches_en_cours-1png.md)

[![](/mediawiki/images/thumb/7/79/T%C3%A2che_en_cours-2.png/900px-T%C3%A2che_en_cours-2.png)](FileTâche_en_cours-2png.md)

## GPU account statistics

Here you can see the total GPU requests for your group, along with their usage over the past few months. You can also track your priority, which varies based on your usage.

[![](/mediawiki/images/thumb/8/82/Utilisation_compte_GPU_d%C3%A9tails.png/900px-Utilisation_compte_GPU_d%C3%A9tails.png)](FileUtilisation_compte_GPU_détailspng.md)

This graph shows the software that are more frequently used.

[![](/mediawiki/images/thumb/b/be/Application_utilis%C3%A9_compte_GPU.png/900px-Application_utilis%C3%A9_compte_GPU.png)](FileApplication_utilisé_compte_GPUpng.md)

Here you see the resources used by each user in your group.

[![](/mediawiki/images/thumb/1/18/GPU_utilis%C3%A9_par_utilisateur_compte_GPU.png/900px-GPU_utilis%C3%A9_par_utilisateur_compte_GPU.png)](FileGPU_utilisé_par_utilisateur_compte_GPUpng.md)

This graph shows the quantity of GPUs wasted by each user.

[![](/mediawiki/images/thumb/a/a2/GPU_gaspill%C3%A9_compte_GPU.png/900px-GPU_gaspill%C3%A9_compte_GPU.png)](FileGPU_gaspillé_compte_GPUpng.md)

Here you see the CPU allocated and used by your GPU tasks.

[![](/mediawiki/images/thumb/4/4d/CPU_compte_GPU.png/900px-CPU_compte_GPU.png)](FileCPU_compte_GPUpng.md)

This graph shows the CPUs wasted by your GPU tasks.

[![](/mediawiki/images/thumb/7/75/Coeur_CPU_gaspill%C3%A9_compte_GPU.png/900px-Coeur_CPU_gaspill%C3%A9_compte_GPU.png)](FileCoeur_CPU_gaspillé_compte_GPUpng.md)

Here you see the memory used by each user in your group.

[![](/mediawiki/images/thumb/7/71/M%C3%A9moire_compte_GPU.png/900px-M%C3%A9moire_compte_GPU.png)](FileMémoire_compte_GPUpng.md)

This graph shows the memory wasted by each user.

[![](/mediawiki/images/thumb/2/21/M%C3%A9moire_gaspill%C3%A9e_GPU.png/900px-M%C3%A9moire_gaspill%C3%A9e_GPU.png)](FileMémoire_gaspillée_GPUpng.md)

Vous avez ensuite une représentation de votre activité sur les systèmes de fichiers. À gauche, le graphique montre le nombre de commandes d’écriture sur disque que vous avez effectuées. (input/output operations per second (IOPS)) À droite, vous voyez la quantité de données transférées vers les serveurs sur une période donnée. (Bande passante)

[![](/mediawiki/images/thumb/b/be/Syst%C3%A8me_de_fichier_GPU.png/900px-Syst%C3%A8me_de_fichier_GPU.png)](FileSystème_de_fichier_GPUpng.md)

Here you see the last tasks that were run by your group.

[![](/mediawiki/images/thumb/1/11/T%C3%A2ches_en_cours-1.png/900px-T%C3%A2ches_en_cours-1.png)](FileTâches_en_cours-1png.md)

[![](/mediawiki/images/thumb/7/79/T%C3%A2che_en_cours-2.png/900px-T%C3%A2che_en_cours-2.png)](FileTâche_en_cours-2png.md)

# Cloud statistics

Le premier tableau « Vos instances » présente l'ensemble des machines virtuelles associées à un compte. La colonne « Saveur » fait référence au [type de machine virtuelle](Virtual_machine_flavors_fr.md). La colonne « UUID » correspond à un identifiant unique attribué à chaque machine virtuelle.

[![](/mediawiki/images/thumb/0/05/Tableau_vos_instances.png/900px-Tableau_vos_instances.png)](FileTableau_vos_instancespng.md)

Then, each virtual machine has its own usage statistics (CPU cores, memory, disk bandwidth, IOPS and network bandwidth) that can be shown for the last month, week, day or hour.

[![](/mediawiki/images/thumb/3/3e/Coeurs_CPU.png/900px-Coeurs_CPU.png)](FileCoeurs_CPUpng.md)

[![](/mediawiki/images/thumb/8/87/M%C3%A9moire_cloud.png/900px-M%C3%A9moire_cloud.png)](FileMémoire_cloudpng.md)

[![](/mediawiki/images/thumb/8/88/Bande_passante_disque_cloud.png/900px-Bande_passante_disque_cloud.png)](FileBande_passante_disque_cloudpng.md)

[![](/mediawiki/images/thumb/8/81/IOPS_disque.png/900px-IOPS_disque.png)](FileIOPS_disquepng.md)

[![](/mediawiki/images/thumb/1/1e/Bande_passante_r%C3%A9seau_cloud.png/900px-Bande_passante_r%C3%A9seau_cloud.png)](FileBande_passante_réseau_cloudpng.md)