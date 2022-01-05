Ce repository contient le projet Hackathon 2022 de l'équipe Joanne - Simon - Mohamed

# Installation du projet - Production

Nous avons choisi comme hébergeur Scalingo pour l'application, le guide suivant s'appuiera donc sur cet hébergeur en particulier.

### Prérequis

* Installez Git sur votre machine : https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
* Créez un compte Scalingo
> ASTUCE : il est possible de se connecter sur Scalingo directement avec un compte GitHub, ce qui simplifiera la liaison entre le code sur GitHub et son importation dans Scalingo
* Créez un repository GitHub mirroir (https://docs.github.com/en/repositories/creating-and-managing-repositories/duplicating-a-repository#mirroring-a-repository) du repository suivant : https://github.com/moussmo/testScalingo.git
> Cela permettra d'importer le projet GitHub directement dans Scalingo, ce qui est impossible si vous n'êtes pas le propriétaire du repository GitHub

### Importer le projet GitHub dans Scalingo

Tout d'abord nous allons créer une application Scalingo
* Rendez-vous sur le dashboard de Scalingo, rubrique apps (https://dashboard.scalingo.com/apps) puis cliquez sur "Create an application"
> !Screenshot!
* Nommez l'application et appuyez sur "Create App"
> !Screenshot!
* Cliquez sur la méthode de synchronisation du code (GitHub à priori) ; sélectionnez votre repository mirroir ; Assurez-vous que "enable automatic deploy" est cochée ; sélectionnez la branche "Production" ; Validez
> !Screenshot!
* Appuyez sur "Finish"

### Boot l'application

!Mohammed si tu veux expliquer!

# Installation du projet - Développement

### Prérequis

* Installez Git : https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
* Installez Python (!Faut donner une version!) : https://www.python.org/downloads/

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
python main.py
```

