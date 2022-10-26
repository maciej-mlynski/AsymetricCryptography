Asymetria kryptograficzna ECDSA

Główne funkcjonalności narzędzia:

1. Generowanie liczby pseudo losowej. 

Na tym etapie generowane jest conajmniej kilka losowych liczb różnymi sposobami.
Na początku losowany jest n bitowy ciąg. Urzytkownik do wyboru ma 128 bitowy i 256 bitową entropie. 
Długość entropi przekłada się również na długość frazy seed, ale o tym później.

Nastepnie, wykorzystując metodę szyfrowania Xoroshiro128 losowana jest kolejna liczba.
Liczba ta jest instrukcją mieszania pierwszej entropi. Instrukcja ta jest bardzo podobna do metody generowania klucza publicznego w 
systemie DH (Diffie Helman), gdzie bity (0-1) decydują o tym, czy wykonać jedno lub 2 przekształcenia. W przypadku generowania liczby losowej postanowiłem jednak
aby decydwały o tym czy zamieszać poprzednią entropię (1), czy tez nie (0).

W kwesti generowania entropi, która jest kluczowa dla asymetri kryptograficznej mam jeszcze troche do dopracowania. Choćbym mieszał i mieszał liczbę
generowaną przez algorytm, to tak czy inaczej będzie to jedynie PSEUDO liczba losowa, którą przy wygenerowaniu odpowiedniej ilości liczb, będzie można w pewien sposób przewidzieć.
Usprawnienie tego etapu będzie prubą stworzenia prawdziwej liczby losowej. Zazwyczaj wykorzystywane do tego jest śledzenie myszki, o której poruszenie poproszony jest użytkownik.
Nie chce jednak iść w tradycyjne rozwiązania, więc myśle, że w przyszłości chciałbym żeby użytkownicy trochę o sobie opowiedzieli, może wybrali jakieś kolory, ulubione przedmiody, czy sport.


2. Metoda hashowania.

Metoda haszowania jest używana w wielu istotnych miejsach w mojej aplikacji. Haszowany będzie przede wszystkim klucz prywatny oraz każda inna entropia. 

Wybrałem metodę haszującą SHA 256. Dowolny ciąg znaków przepuszczony przez ten algorytm stworzy unikalny 256 bitowy hasz. Czy to wystarczy? Dla porównania dodam, że pod względem
bezpieczeństwa 256 bitowe klucz w modelu ECDSA jest porównywalny z 3072 bitowym kluczem dla modelu RSA. Poniżej zamieszczam ciekawe porównanie


3. Fraza Seed.

Fraza seed jest to nic innego jak przedstawienie wygenerowanej entropi w przyjazny dla użytkownika sposób. Zacznijmy od tego po co nam to wogóle jest? Fraza seed w moim projekcie
znajduje swoje zastosowanie w odzyskiwaniu klucza prywatnego. Dokładnie tak samo jak ma to miejsce w portfelach metamask. To co warto w tym miejscu dodać to fakt, że tak naprawde
fraza seed pomoże w odnalezieniu entropi jeszcze przed przejściem procesu mieszania (SHA - 256). Fraza jest więc generowana pomiędzy procesem entropi a metodą hashowania. jak to działa?


1. Entropia przedstawiana jest w postaci binarnej. (128 bitów lub 256 bitów)
2. Szukamy sumy sprawdzającej. Dla 128 bitowego klucza będą to pierwsze 4 bity, dla 256 bitów -> 8 bitów. *Bity o których mowa w przypadku sumy kontrolnej dotyczą stricte ostatecznej wersji klucza prywatnego (po zmieszaniu sha-256))
3. Dodajemy sumę sprawdzającą do entropi przedstawionej w bitach
4. Grupujemy bity tak aby w każdej z nich znajdowały się po 11 bitów
5. Podstawiając poszczególny do odpowiedniego równania jesteśmy w stanie uzyskać konkretne liczby z zakresu od 1 do 2048
6. Każda z liczb posiada swoją reprezentacje w postaci słowa, które mapowane jest słowami w standardzie BIP-39
7. Urzykownik otrzymuje frazę seed o ustalonej przez niego wcześneij długości. 128 bitowa entropia prezentuje 12 słów, a 256 bitowa aż 24 słowa
8. Słowa powinny zostać zapisane przez użytkownika na kartce

4. Klucz prywatny i publiczny

W tym miejscu dzieje się cała magia ECDSA (Elliptic Curve Digital Signature Algorithm). Dodam jeszcze, że używam konkretenj krzywej epiliptycznej o nazwie secp256k1.

Klucz prywatny to nic innego jak entropia przedstawiona w postaci hasha w modelu SHA-256.
Klucz publiczny tworzony jest na podstawie klucza prywatnego. Jest on w pewnym sensie instrukcją do jego storzenia. W przypadku ECDSA posiłkujemy się krzywą epiliptyczną, na której
wykonywane będą pewne transformacje. Punktem początkowym jest G, który opisuje kształt krzywej epiliptycznej. Następnie liczba ta przekształcana jest na podstawie klucza prywatnego. 
Jak wiadomo klucz w postaci hex, lub int mozemy przedstawic równeiż w postaci bitowej. Bity klucza będą decydować o tym, czy nasz punkt G będzie podwajany, czy też dodawany i podwajany.
Oczywiście nie chodzi tu o zwykłe podwajanie, czy dodawanie ale o operacje skalarne. Zaczynamy od prawej strony bitowego klucza prywatnego. Jeśli pierwszy bit od prawej jest równy 0
to punk G jest podwajany. Jeśli kolejny bit równa się jeden to w tym miejscu również wykonujemy metodę podwajania na poprzednio zmodyfikowanym punkcie G. Dopiero gdy pojawi się kolejna 1
w bitowym kluczu prywatny to wykonujemy metodę dodawania skalarnego / dodawania punktów. Poczym znowu dokonujemy metody podwajania skalarnego. Proces powatarzamy aż do ostatniej jedynki
od lewej. W wyniku skalarnych multiplikacji w resultacie otrzymujemy współrzędne klucza publicznego z czgo w łatwy sposób otrzymujemy klucz publiczny.


Jakie ma to zalety? Proces ten jest jednostronny, czyli łatwo jest wygenerować klucz publiczny z klucza prywatnego, jednak odwrócenie tego procesu wymaga ogromnej mocy oliczeniowej. 
Oczywiście im dłuższy klucz tym zadania dla hakerów jest cięższe. Zasada jest prosta: Dłuższy klucz = wiecej multiplikacji = ciężej go złamać.

5. Podpisywanie transakcji

W tym miejsu również wykożystujemy potęgę krzywej epiliptycznej oraz liczby pseudo losowe. Przyjrzyjmy się temu procesowi po kolei:

1. Wygenerowanie losowej entropi. Ważne aby liczba ta za każdym razem była od siebie inna. (NONCE - Number Used Only Once)
2. Entropia przepuszczana jest przez metodę hashowania SHA-256, a następnie wykorzystana w modelu ECDSA jako instrukcja mieszania punktu G. (Tak jak z kluczem prywatnym)
3. Z wygenerowanego punktu bierzemy jedynie współrzędną X
4. Generujemy kolejną entropie i również hashujemy ją metodą sha-256
5. Generujemy sygnaturę kryptograficzną poprzez podstawienie do odpowiedniego wzoru zmiennych:
- pierwsza zmieszana entropia
- druga zmienszana entropia
- klucz prywatny osoby wysyłającej wiadomość
- współrzędna x
- liczba n, która jest liczbą PRIME

Metoda podpisywania transakcji zwraca 3 wartości: Podpis, drugą mieszną entropie i współrzędne punktu stworzonego przez pierwszą zmieszaną entropie.
Wartości te mogą być publiczne o ile użytkownik ma ochotę ujawnić swoją prawdziwą twarz, a odbiorca nie chce zweryfikować nadawcy.
Wartości te nie mogą doprowadzić osób trzecich do klucza prywatnego.

* Podpisanie transakcji jest w moim projekcie dodatkiem, jednak jeśli chodzi o transakcje oparte o technologie blockchain jest fundamantalną kwestią, gdyż jest dowodem
transparętności.


6. Weryfikacja transakcji

W tym miejsu odbiorca transakcji może sprawdzić, czy nadawca jest tym za kogo się podaje. Do sprawdzenia potrzebne będą wszystkie wartości wynikowe metody podpisywania transakcji oraz
klucz publiczny osoby wysyłającej wiadomość. To właśnie te elementy podstawione do kolejnych multiplikacji ECDSA i wzorów doprowadzą nas do wygenerowania kolejnego punktu. 

Jeśli klucz publiczny osoby wysyłającej wiadomość jest taki jak być prawidłowy to współrzędne punktu w wyniku procesu weryfikacji powinien być identyczny jak klucz wysłany przez nadawce.


7. Szyfrowanie i odszyfrowywanie wiadomości.


Do szyfrowania tekstu wykorzystałem bibliotekę AES. Pozwala ona na zaszyfrowanie treści względem pewnego klucza. Klucz ten oczywiście nie może być znany osobom trzecim.
Ten sam klucz używany jest do zaszyfrowania i odszyfrowania wiadomości, co świadczy o jego symetryczności. To co jednak warto zaznaczyć to fakt, iż nie jest on nigdy wysyłany między
użytkownikami oraz za każdym razem jest inny. To co użytkownicy wysyłąją między sobą to oczywiście zaszyfrowana wiadomość oraz instrukcje jak mają ten klucz odnaleźć. 

Krótko o procesie wysyłania instrukcji do odnalezienie klucza odszyfrowującego wiadomość:

1. Tak jak wcześneij generowana jest losowa entropa zmieszana przez SHA-256. Nazwijmy tą liczbę K
2. Dokładnie tak jak wcześniej K w postaci bitowej jest instrukcją do przekształcenia punktu G. Nazwijmy go punktem R. 
3. Tworzymy teraz sekretną wartość poprzez skalarna multiplikacje liczby K przez wspołrzędne klucza publicznego odbiorcy (Nie przez punkt G tak jak było to w każdym poprzednim przypadku)
4. Wiadomość szyfrowana jest współrzędną X wygenerowanego punktu z pkt.3
5. Wysyłamy zaszyfrowaną wiadomośc wraz z punktem R. 


Wiadomość wraz z punktem R nie muszą być specjalnie chronione, ponieważ tylko odbiorca posiada klucz prywatny, dzięki któremu dokonując pewnych przekształceń na punkcie R może odszyfrować
wiadomość. Metoda, która pozwoli dojść do sekretnego klucza to tak jak wcześniej skalarna multiplikacja. Z tą różnicą, że instrukcją jest jak wspomniałem jego klucz prywatny, a
obiektem, który ma zostać przekształcony nie jest punkt G, a punkt R. Sekretny klucz to współrzędna X wygenerowanego punku.

* W tym miejsu chchaiłbym podzielić się jedną ze słabości mojego algorytmy. Tak jak generowanie kluczy oraz podpisywanie i weryfikacja transakcji jest stosunkowo transparętna, a tym 
samym ciężka do złamania przez hakerów tak samo szyfrowanie wiadomości już nie koniecznie. Co prawda metoda AES jest uważany za całkiem mocne zabezpieczenie, to tak czy inaczej nie zrobiłęm go sam.
Skorzystałem z dostępnej biblioteki. Muszę zatem zaufać, że twórcy nie zostawili żadnej furtki sobie czy hakerom. Na pewno jest to część, którą w najbliższej przyszłości chciałbym zrobić po swojemu.


8. Odzyskiwanie klucza prywatnego
Jak wcześniej wspomniałęm fraza seed jest odzwierciedleniem entropi, z której powstaje klucz prywatny. Zatem, dokonując pewnych przekształceń możemy umożliwić użytkownikom przypomnienie 
sekretengo klucza. Jako, że klucz prywatny jest potrzebny użytkownikowi w kilku miejscach, użytkownik zamiast klucza może skorzystać bezpośrednio z frazy seed. 



9. Plany usprawnienia

1. Napisanie własnego skryptu do szyfrowania wiadomości
2. Połaczenie z bazą danych, w której zapisywane będą hasze transakcji (nonce) wraz z kluczem publicznym tak aby nie było powtórzeń (Szansa na to jest jak 1/2**256 jednak dalej istnieje.
3. Napisanie skryptu do tworzenia prawdziwej liczby losowej, a nie pseudo losowej jak ma to miejsce obecnie.


10. Zagadka dla hakerów

Poniżej zostawiam dane dotyczące pewnej transakcji. Użytkownik A wysyła wiadomość do użytkownika B. Jak wspomniałem pewne informacje mogą być publiczne, a i tak nikt nie powinien złamaś szyfru.
Zadaniem dla chętnych jest odszyfrowanie wysłanej wiadomości, nie znając klucza prywatnego użytkowników, ani eskretnego klucza odszyfrowującego treść wiadomości. Jeśli Wam się uda
oznaczać to będzie tylko to że mój kod jest wdliwy i muszę jeszcze nad nim popracować. Jeśli dodatkowo bedziecie w stanie odgadnąć klucz prywatny któregoś lub obu z użytkowników
będzie to dla mnie jasny sygnał, że chyba nie powinienem brać się za tak skomplikowane tematy jakimi są asymetryczna kryptografia. Pozdrawiam

Klucz publiczny wysyłąjącego:
Klucz publiczny odbiorcy:
Współrzędne punktu R:
Zaszyfrowana wiadomość:

Oprócz tego sami mozecie zweryfikować czy wysyłający jest tym za kogo się podaje na pdstawie tych wartości:

sygnatura:
Zaszyfrowana entropia (k2):
Punku K:

Jeśli Punkt K, będzie równy wygenerowanenmu punktowi powstałemu z sygnatury, entropi k2 oraz kluczowa publicznego wysyłającego, będzie to oznaczać, że podany klucz publiczny jest prawidłowy.















