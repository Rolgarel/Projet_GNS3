# Projet_GNS3

Nous avons trois architectures des configurations réparties dans trois dossiers :
 - Le projet complet, comprend l'architecture de base décrite dans le sujet (14 routeurs)
 - Le projet réduit, comprend une version miniature du projet complet (6 routeurs)
 - Le projet testbgp, comprend trois routeurs et trois AS, il a été utilisé pour tester les communities

# Algorithmie

Le projet complet le modele reduit possèdent chacun un intent file au format Json, deux codes en python : un code de configuration et un code Telnet.

Le code de configuration et le fichier Json supportent les fonctionnalités suivantes :
  * Génération automatique des addresses
  * Configurations des interfaces
  * Mise en place de OSPF et RIP
  * Mise en place de eBGP et iBGP
  * OSPF Metric Optimisation
  * Drag and Drop bot
  * Mise en place des BGP Policies (tags des routes, definition des préférences, filtrage des routes)

Code Telnet :
Code minimaliste permettant d'envoyer des commandes à un routeur.