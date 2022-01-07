Ce repository contient le projet Hackathon 2022 de l'équipe Joanne - Simon - Mohamed

# Installation du projet - Développement

### Prérequis

* Installez Git : https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
* Installez Python (3.8 ou plus récent) : https://www.python.org/downloads/

### Installation du projet et de l'environnement

> NOTE : vous pouvez avoir recours à un environnement virtuel si vous le souhaitez, les instructions suivantes restent valables peu importe votre choix.
* Clonez le repo Git 
   ```sh
   git clone https://github.com/moussmo/testScalingo.git
   ```
* Placez vous dans le répertoire racine
   ```sh
   cd testScalingo/
   ```
* Installez les dependencies
   ```sh
   pip install -r requirements.txt
   ```

   
### Lancer l'application

* Assurez-vous d'être placé à la racine du projet
* Lancez l'app
```sh
python app.py
```

# Déploiement du projet

Nous avons choisi comme hébergeur Scalingo pour l'application, le guide suivant s'appuiera donc sur cet hébergeur en particulier.

### Prérequis

* Installez Git sur votre machine : https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
* Créez un compte Scalingo
> ASTUCE : il est possible de se connecter sur Scalingo directement avec un compte GitHub, ce qui simplifiera la liaison entre le code sur GitHub et son importation dans Scalingo
* Créez un repository GitHub mirroir (https://docs.github.com/en/repositories/creating-and-managing-repositories/duplicating-a-repository#mirroring-a-repository) du repository suivant : https://github.com/moussmo/testScalingo.git
> Cela permettra d'importer le projet GitHub directement dans Scalingo, ce qui est impossible si vous n'êtes pas le propriétaire du repository GitHub

### Création de l'application

Tout d'abord nous allons créer une application Scalingo
* Rendez-vous sur le dashboard de Scalingo, rubrique apps (https://dashboard.scalingo.com/apps) puis cliquez sur "Create an application"
![dashboard](images\scalingo_dashboard.png)
* Nommez l'application et appuyez sur "Create App"
![basic_info](images\scalingo_basic_info.png)
* Cliquez sur la méthode de synchronisation du code (GitHub à priori) ; sélectionnez votre repository mirroir et la branche qui vous intéresse; Assurez-vous que "enable automatic deploy" est cochée ; sélectionnez la branche "Production" ; Validez
![deployment](images\scalingo_deployment.png)
![github](images\scalingo_github.png)
![end](images\scalingo_end.png)
* Appuyez sur "Finish"

### Boot l'application

* Lorsque vous créez l'application et si le lien du dépôt GitHub joint est valide, elle est automatiquement déployée. 
* Si vous avez coché l'option 'Enable Automatic Deploy' comme suggéré plus haut, à chaque fois que vous 'pushez' vos commits sur votre branche, l'application est redéployée automatiquement.
* Vous pouvez déployer manuellement votre application en vous rendant dans l'onglet 'Deploy', partie 'Manuel Deployments' et en appuyant sur le bouton 'Trigger Deployment'.

* Scalingo vous offre des logs de déploiements dans l'onglet 'Deploy' partie 'History'. Parmi les messages d'erreurs les plus communs:
	* "Build Error: Invalid return code from buildpack*: 
	* "Missing Procfile": assurez-vous qu'un procfile est présent à la racine du projet.

### Fonctionnement du Buildpack de Scalingo
Scalingo se base sur un algorithme du nom de Buildpack afin de détecter les technologies utilisées dans le projet.
Afin que celui-ci détecte Python, il est nécessaire qu'il trouve 3 fichiers dans le projet: 
	* Pipfile.lock
	* requirements.txt
	* setup.py
	
Ces fichiers doivent être présents dans le dossier principal de l'app que vous déployez. C'est-à-dire si le dépôt Git que l'application utilise est de la forme:
	* projet
	* projet/server
	* projet/exemples
et que votre application se trouve dans le sous-dossier server, il faudra que ces 3 fichiers soient présents dans celui-ci. Il est aussi nécessaire qu'une variable d'environnement indique à Scalingo que l'application est située dans le sous-dossier. La variable d'envrionnement a comme nom: PROJECT-DIR

De plus, un fichier nommé procfile doit aussi être présent dans le dossier de l'application. L'application se base sur le fichier pour savoir quoi lancer au déploiement de l'application.