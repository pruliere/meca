# Mécanique des solides et calcul avancé

Ce dépôt contient les scripts et documents vus lors du cours de master « Mécanique des solides et calcul avancé ».

## Prérequis et installation

Pour utiliser les scripts, il faut installer Python et Fedoo :

1. Installer **Miniconda** (ou **Anaconda**).
2. Ouvrir un terminal Anaconda (**Anaconda Prompt**), puis exécuter les commandes suivantes pour créer un environnement Python et installer Fedoo :

   ```shell
   conda create -n myEnv python=3.13
   conda activate myEnv
   pip install fedoo[all,gui]
   ```

## Utiliser l’éditeur IDLE

Ouvrir un terminal Anaconda, activer l’environnement, puis lancer IDLE :

```shell
conda activate myEnv
idle
```

## Installer Jupyter (optionnel)

Dans un terminal Anaconda où l’environnement `myEnv` est activé :

```shell
pip install jupyter
```

## Mettre à jour Fedoo

Dans un terminal Anaconda où l’environnement `myEnv` est activé :

```shell
pip install -U fedoo
```
