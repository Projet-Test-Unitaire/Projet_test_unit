# Projet_test_unit

#### Utilisation du site:

Installer pytest:
- pip install pytest
Lancer server.py: 
- python server.py
Ouvrir un navigateur, dans la bar de recherche: 
- localhost:5000
Connectez-vous avec un des mails présents dans le fichier clubs.json; ex:
- john@simplylift.co
Vous verrez un nombre de points apparaitre, 3 points équivaut à 1 place. 
Selectionner un des festivals auquel vous souhaitez assister (Spring Festival ou Fall Classic) et cliquer sur le bouton 'Book Places' associé.
Vous pouvez saisir le nombre de places souhaitées puis cliquez sur 'Book'.
Si vous avez assez de points vous verrez s'afficher votre nouveau solde de points et le nombre de places restantes, cependant si vous n'avez pas assez de points vous n'aurez le droit qu'à un message: 'Vous n'avez pas assez de places !'

#### Les test unitaires fichier (test_server.py)

# [root : index]

test_home_page_returns_correct_html(client)
test_pages_return_correct_html(client)

Ces derniers vont tester que le serveur se lance correctement et que la page index s'ouvre bien

# [root : showSummary]

test_summary_print_on_email_valid(client)

Ce test vise à vérifier que lorsqu'un utilisateur (club) se connecte, il arrive bien sur la page showSummary du site si son email est valide; on s’assure qu’un Summary est affiché lorsqu'un secretary email (d’un club) est saisi dans le formulaire de la page index

# [root : showSummary] [param: (email)]

test_summary_print_on_email_invalid(client)

Vérifie que si l'utilisateur n'a pas d'email valide (pas d'email de club), ce dernier ne peut pas se connecter, on affiche alors un message: "Sorry, this email doesn't exist !"

# [route : book]

test_booking_valid_params(client)

Ce test s'assure qu'une page booking.html s'affiche pour un club ou une compétition valide, on utilise un find ici pour vérifier que la page booking.html s'affiche

# [route : book]

test_booking_invalid_params(client)

Ce test vérifie que l'interface utilisateur empêche la réservation d'un club ou d'une compétition non valide, si c'est le cas on renvoie un message d'erreur: "Something went wrong-please try again"

# [route : book/purchasePlaces][params : (email, compétition, club, points)]

test_but_success_decrement_point_to_point(client)

Un test pour s'assurer que lorsque l’User achète avec succès, les places sont correctement déduites du
concours et les points déduits d'un club. Pour cela nous faisons appel à notre fonction 
_book_place(client, placesToPurchase, newAvailiblePLaces=None, newAvailiblePoints=None)
dans notre fichier conftest.py, cette dernière s'assure de la décrémentation

# [route : book/purchasePlaces][params : ()]

test_error_msg_places(client)

Un test pour s'assurer qu'il affiche le message d'erreur souhaité lorsqu'il y a plus de 12 places
Pour cela nous faisons appel à notre fonction:
_book_place_failed(client, placesToPurchase, club, competition, error)
dans le fichier conftest.py, cette dernière renvoie un message d'erreur si le nombre de places est supérieur ou égal à 12:
"Invalid amount of requiered places"

# [route : book/purchasePlaces][params : ()]

test_error_msg_date(client)

Un test pour s'assurer qu'il affiche le message d'erreur souhaité lorsque la date d'une compétition est depassée
Pour cela nous faisons appel à notre fonction:
_book_place_failed(client, placesToPurchase, club, competition, error)
dans le fichier conftest.py, cette dernière renvoie un message d'erreur si la date est passée:
"Old date, booking impossible !"

# [route : book/purchasePlaces]

test_not_enough_points(client)

Un test pour s'assurer qu'il affiche le message d'erreur souhaité lorsque l'utilisateur s'engage à acheter
plus de places que les points disponibles
Pour cela nous faisons appel à notre fonction:
_book_place_failed(client, placesToPurchase, club, competition, error)
dans le fichier conftest.py, cette dernière renvoie un message d'erreur si la date est passée:
"'Not enought points !'"

# [route : dashboard]

test_but_success_decrement_point_to_3point(client)

Vérifie que nous avons bien modifié la valeur des points (selon le mail de Zayn) : L'échange actuel de 1 point = 1 place de compétition a été mis à jour de sorte que 3 points = 1 place de compétition
Pour cela nous faisons appel à notre fonction:
_book_place(client, placesToPurchase, newAvailiblePLaces=None, newAvailiblePoints=None)
dans le fichier conftest.py, cette dernière vérifie que le nouveau nombre de points s'actualise bien; ce qui est suffisant car la décrementation de 3 se fait déjà automatiquement grâce à notre fonction:
purchasePlaces()
du fichier server.py

# [route : logout]

test_logout(client)

Test unitaire pour logout, pour cela on fait appel à notre fonction:

du fichier conftest.py, cette dernière vérifie que l'utilisateur est bien déconnecté et qu'un message renseigne bien cette information:
"You're now disconnected"