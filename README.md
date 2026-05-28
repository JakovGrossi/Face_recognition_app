# Face Recognition App

Aplikacija za prepoznavanje i registraciju lica u stvarnom vremenu putem web kamere. Ovo je prvi projekt autora iz područja računalnog vida (Computer Vision).

Kod i pokretanje se nalaze u `main.py`, arhitektura modela u `recognizer.py`, rad s bazom podataka u `database.py`, dok je logički tijek aplikacije smješten u `actions.py`.

## Kako aplikacija radi

* **Detekcija i embedding:** Model koristi **MTCNN** za lociranje lica, dok **InceptionResnetV1 (vggface2)** iz `facenet-pytorch` paketa generira normalizirane vektore značajki lica.
* **Baza podataka:** Sustav koristi **SQLite3** za lokalnu pohranu korisničkih podataka, pri čemu se slike lica spremaju u JPEG formatu, a pripadajući vektorski zapisi (embeddings) kao BLOB objekti.
* **Prepoznavanje:** Proces prepoznavanja temelji se na izračunu **skalarnog produkta (dot product)** između vektora lica u trenutnom kadru i onih pohranjenih u bazi. Prag pouzdanosti (threshold) definiran je na vrijednosti **0.7**.

## Glavne funkcije

* **Registracija korisnika (1):** Nakon unosa imena, aplikacija vodi korisnika kroz proces snimanja 5 različitih poza glave (ravno, lijevo, desno, gore, dolje). Za svaku pozu se bilježe 64 validna okvira kako bi se osigurala visoka točnost i robusnost modela.
* **Prepoznavanje uživo (2):** Pokreće se video stream u stvarnom vremenu; aplikacija detektira lica, iscrtava bounding box i ispisuje ime prepoznate osobe uz postotak podudarnosti. Ukoliko prepoznato lice ne prelazi zadani prag, označava se kao *"Unknown"*.
* **Brisanje korisnika (3):** Unosom imena pokreće se kaskadno brisanje, čime se iz baze trajno uklanjaju korisnički zapis, sve povezane slike i odgovarajući vektori značajki.

---

Želite li da vam pomognem s nekim drugim aspektom dokumentacije ovog projekta ili možda s pripremom `requirements.txt` datoteke?# Face Recognition App

Aplikacija za prepoznavanje i registraciju lica u stvarnom vremenu putem web kamere. Ovo je prvi projekt autora iz područja računalnog vida (Computer Vision).

Kod i pokretanje se nalaze u `main.py`, arhitektura modela u `recognizer.py`, rad s bazom podataka u `database.py`, dok je logički tijek aplikacije smješten u `actions.py`.

### Kako aplikacija radi

*  **Detekcija i embedding:** Model koristi **MTCNN** za lociranje lica, dok **InceptionResnetV1 (vggface2)** iz `facenet-pytorch` paketa generira normalizirane vektore značajki lica.


* **Baza podataka:** Sustav koristi **SQLite3** za lokalnu pohranu korisničkih podataka, pri čemu se slike lica spremaju u JPEG formatu, a pripadajući vektorski zapisi (embeddings) kao BLOB objekti.
* **Prepoznavanje:** Proces prepoznavanja temelji se na izračunu **skalarnog produkta (dot product)** između vektora lica u trenutnom kadru i onih pohranjenih u bazi. Prag pouzdanosti (threshold) definiran je na vrijednosti **0.7**.

### Glavne funkcije

* **Registracija korisnika (1):** Nakon unosa imena, aplikacija vodi korisnika kroz proces snimanja 5 različitih poza glave (ravno, lijevo, desno, gore, dolje). Za svaku pozu se bilježe 64 validna okvira kako bi se osigurala visoka točnost i robusnost modela.
* **Prepoznavanje uživo (2):** Pokreće se video stream u stvarnom vremenu; aplikacija detektira lica, iscrtava bounding box i ispisuje ime prepoznate osobe uz postotak podudarnosti. Ukoliko prepoznato lice ne prelazi zadani prag, označava se kao *"Unknown"*.
* **Brisanje korisnika (3):** Unosom imena pokreće se kaskadno brisanje, čime se iz baze trajno uklanjaju korisnički zapis, sve povezane slike i odgovarajući vektori značajki.
