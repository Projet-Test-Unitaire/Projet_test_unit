

# Lancer le fichier : 
# locust -f ./locustfile.py --host http://127.0.0.1:5000 --users 500 --spawn-rate 500
#La version web se trouve sur :
# Regarder l'onglet Charts de http://localhost:8089 | Et non pas sur http://0.0.0.0:8089 (ò_ò)

#Commentaire utile du fichier de base : 

# La classe HttpUser est une instance de HttpSession qui fournit un client de test. 
# Comme pour les unit tests, le client permettra de faire la requête sur l’URL de votre choix.

# Lorsqu'un test démarre, Locust créera une instance de cette classe pour chaque User qu'il simule, et chacun de ces Users s'exécutera dans son propre thread.

# Locust considère que chaque méthode contenant @task est une tâche à lancer.

from locust import HttpUser, task, between
from locust.user import wait_time

from server import loadClubs, loadCompetitions

class PerfTest(HttpUser):
    wait_time = between(1, 5)

    @task
    def speed_index(self):
        self.client.get(url="/")
    
    @task
    def speed_showSummary(self):
        payload = {"email":"admin@irontemple.com"}
        self.client.post("/showSummary", data=payload)
    
    @task
    def speed_book(self):
        self.client.get("/book/Grand Canyon/Iron Temple")

    @task #A corriger , meme si c'est pas vraiment demander sur le sujet
    def speed_purchasePlaces(self):
        self.client.get(url="/")
        payload = {"email":"admin@irontemple.com"}
        self.client.post("/showSummary", data=payload)
        payload = {"club":"Iron Temple", "competition":"Grand Canyon", "places": 1}
        self.client.post("/purchasePlaces",data= payload)

    @task
    def speed_logout(self):
        self.client.get("/logout")
        
    @task
    def speed_dashboard(self):
         self.client.get("/pointsDiplay")
        