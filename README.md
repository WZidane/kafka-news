# Application Kafka News

Lancer tous les conteneurs Docker ainsi que les scripts pour faire créer les topics et faire fonctionner la récupération des flux RSS, voici les différentes commandes :

- docker compose up -d --build


- Attendre que tous les conteneurs se lancent.


- Attendre que Kafka se lance complètement (vérifier avec la commande docker logs kafka-1)


- docker compose run --rm stream python create_topic.py


- docker compose run --rm stream python lemonde_script.py


- docker compose run --rm stream python 20minutes_script.py

Les deux commandes précédentes permettent de lancer les scripts qui vont récupérer les flux rss toutes les 5 minutes.

Il est possible que Kafdrop ne fonctionne pas malgré avoir été lancé, il faut alors attendre quelques minutes avant d’effectuer cette commande : docker restart kafdrop.
L’installation est alors opérationnelle, il ne reste plus qu’à se rendre sur l’outil Kafdrop et sur l’application Kafka News disponibles à ces adresses : 

- Kafdrop : http://localhost:9000/
- Kafka News : http://localhost:5000/
