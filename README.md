# Projet_GNS3

Nous avons trois architectures des configurations réparties dans trois dossiers :
 - Le projet complet, comprend l'architecture de base décrite dans le sujet (14 routeurs)
 - Le projet réduit, comprend une version miniature du projet complet (6 routeurs)
 - Le projet testbgp, comprend trois routeurs et trois AS, il a été utilisé pour tester les communities

## Algorithmie

Le projet complet le modèle réduit possèdent chacun un intent file au format Json, deux codes en python : un code de configuration et un code Telnet.

Le code de configuration et le fichier Json supportent les fonctionnalités suivantes :
  * Génération automatique des adresses
  * Configurations des interfaces
  * Mise en place d'OSPF et RIP
  * Mise en place d'eBGP et iBGP
  * OSPF Metric Optimisation
  * Drag and Drop bot
  * Mise en place des BGP Policies (tags des routes, filtrage des routes)

Code Telnet :
Code minimaliste permettant d'envoyer des commandes à un routeur.

BGP policies : nous avons fait en sorte que les routes transmisent par les paires et les fournisseurs ne soient pas transmisent qu'à nous et à nos clients.
Une possibilité d'amélioration serait de bloquer la transmission de toutes les routes qui ne proviennent pas de nos clients et de définir nos LAN comme des clients.
Une autre possibilité d'amélioration serait de définir les préférences entre les AS.