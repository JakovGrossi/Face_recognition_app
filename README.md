# Face Recognition App

Prvi projekt iz computer vision-a, prepoznavanje i registracija lica u stvarnom vremenu putem web kamere. 

Kod i pokretanje se nalaze u `main.py`, arhitektura u `recognizer.py`, baza u `database.py`, logika u `actions.py`.

### Opis

* **Detekcija i embedding:** Model koristi **MTCNN** za lociranje lica, dok **InceptionResnetV1 (vggface2)** iz `facenet-pytorch` paketa generira normalizirane vektore značajki lica.


* **Baza podataka:** Sustav koristi **SQLite3** za lokalnu pohranu korisničkih podataka, pri čemu se slike lica spremaju u JPEG formatu, a pripadajući vektorski zapisi (embeddings) kao BLOB objekti.
* **Prepoznavanje:** Proces prepoznavanja temelji se na izračunu **skalarnog produkta (dot product)** između vektora lica u trenutnom kadru i onih pohranjenih u bazi. Prag pouzdanosti (threshold) definiran je na vrijednosti **0.7**.

### Glavne funkcije

* **Registracija korisnika (1):** Nakon unosa imena, aplikacija vodi korisnika kroz proces snimanja 5 različitih poza glave (ravno, lijevo, desno, gore, dolje). Za svaku pozu se bilježe 64 okvira.
* **Prepoznavanje uživo (2):** Pokreće se video stream u stvarnom vremenu; aplikacija detektira lica, iscrtava bounding box i ispisuje ime prepoznate osobe uz postotak podudarnosti. Ukoliko prepoznato lice ne prelazi zadani prag, označava se kao *"Unknown"*.
* **Brisanje korisnika (3):** Unosom imena pokreće se kaskadno brisanje.
