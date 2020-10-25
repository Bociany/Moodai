# Moodai


Podaj skład drużyny:
- Kacper Staroń: AI, Back-end, Front-end, Połączenie z bazą danych, Połączenie front-endu i back-endu
- Aleksander Brzykcy: Front-end, Design, Grafika
- Dawid Mularczyk: Front-end, Design
- Mateusz Łoziński: Front-end, Design, Grafika
- Michał Kukiełka: Design, Grafika

# Na jakie potrzeby/problem odpowiada Wasze rozwiązanie: 
Na problem zabieganego użytkownika, który w dzisiejszych realiach zaniedbuje swój stan zdrowia psychicznego, na bieżąco informując go o jego postępach.

# W jakich językach programowania, technologiach powstawała wasza aplikacja:
- Back-end: Python 3, Flask do obsługi HTTP, SQLAlchemy i SQLite3 do bazy danych, OpenCV+Tensorflow do wykrywania twarzy, memcached do tymczasowego przechowywania tokenów autoryzacji
- Front-end: HTML, CSS, JavaScript. Chart.js do wyświetlania wykresów, Fullcalendar.io do obsługi kalendarzy, Webcam.js do obsługi kamery i przechwytywania.

# Opisz działanie Waszej aplikacji/narzędzia: 
Aplikacja za pomocą sztucznej inteligencji każdego dnia próbuje wykryć humor użytkownika. Użyktownik po zalogowaniu ma dostęp do zapisów jego samopoczucia z każdego dnia, jak i notatek zostawionych przez niego, oraz zapisanych wizyt. Aplikacja kontaktuje się z serwerem backend za pomocą API REST, działa również w trybie responsywnym na telefonach, co eliminuje wymóg osobnej aplikacji, a pozwala nam użyć strony jako aplikacji (Progressive Web App).

# Jak widzicie dalszy rozwój Waszego rozwiązania: 
Możemy zaangażować do tego psychologów, tworząc na podstawie Moodai platformę, która bezproblemowo i szybko łączy osobę o złym stanie z psychologiem. Możliwość informowania ich wraz z postępującymi dniami, informowanie o stanie zdrowia oraz swoim dniu, np. poprzez czat albo e-mail. Dalsza nauka sztucznej inteligencji przez zdjęcia wysyłane przez klientów, by zwiększyć szansę na jak najdokładniejsze przewidzenie.

# Jakie widzicie zagrożenia/ryzyka dla Waszego rozwiązania: 
Osoby korzystające z aplikacji mogą obawiać się tego, iż wdrożyciel przechwytuje ich zdjęcia, aby je potem wykorzystać bezprawnie.

# Dlaczego akurat Wy powinniście wygrać: 
Ze względu, iż z biegiem lat współczynnik samobójstw u młodych ludzi ciągle rośnie, dużo osób, ze względu na szybki bieg życia nie zwraca uwagi na swój stan psychiczny, co może prowadzić do różnych niemiłych konsekwencji, więc aplikacja która szybko pomoże katalogować stan użytkownika z dnia na dzień może być bardzo pomocna. Użyliśmy do tego sztucznej inteligencji bazującej na Tensorflow, która może być cały czas trenowana, aby współczynnik poprawnie wykrytych emocji był większy. Co pomoże zabieganemu użytkownikowi.
