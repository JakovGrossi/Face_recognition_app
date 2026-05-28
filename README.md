# Face Recognition App

Prvi projekt iz computer vision-a za prepoznavanje i registraciju lica u stvarnom vremenu preko web kamere. 

Kod i pokretanje se nalaze u `main.py`, arhitektura modela u `recognizer.py`, rad s bazom u `database.py`, a logika aplikacije u `actions.py`.

## Kako aplikacija radi
    * Detekcija i embedding: Model koristi MTCNN za lociranje lica i InceptionResnetV1 (vggface2) za izradu normaliziranih vektora iz `facenet-pytorch` paketa[cite: 1].
    * Baza podataka: SQLite3 lokalno sprema ID korisnika, slike lica u JPEG formatu i njihove embeddinge u obliku BLOB podataka.
    * Prepoznavanje: Usporedba lica se radi preko skalarnog produkta (dot product) između trenutnog kadra s kamere i embeddinga iz baze. Prag (threshold) za prepoznavanje je postavljen na 0.7.

## Glavne funkcije
    * Registracija korisnika (1): Korisnik unosi ime, nakon čega aplikacija traži 5 poza glave (ravno, lijevo, desno, gore, dolje). Za svaku pozu se sprema po 64 validna okvira radi veće robusnosti.
    * Prepoznavanje uživo (2): Otvara se video stream, aplikacija detektira lica, crta pravokutnik i ispisuje ime prepoznate osobe uz postotak sličnosti. Ako je rezultat ispod praga, lice se označava kao "Unknown".
    * Brisanje korisnika (3): Unosom imena briše se korisnik iz tablice te se kaskadno uklanjaju svi njegovi povezani kadrice i vektori iz baze.
