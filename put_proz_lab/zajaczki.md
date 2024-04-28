
**Struktury i zmienne:**
- `local_clock`: Zegar Lamporta lokalnego zajączka.
- `request_queue`: Kolejka żądań wyboru polany na imprezę, posortowana po znacznikach czasowych (priorytetach żądań).
- `last_msg_timestamps`: Wektor zegarów Lamporta ostatnio otrzymanych wiadomości od innych zajączków.

**Wiadomości:**
- `REQ`: Żądanie wyboru polany na imprezę.
- `RELEASE`: Zwolnienie wybranej polany.
- `ACK`: Potwierdzenie otrzymania żądania.

**Szkic algorytmu:**
1. Zajączki wysyłają żądania `REQ` wyboru polany do innych zajączków, inkrementując swoje lokalne zegary Lamporta.
2. Po otrzymaniu `REQ` od innego zajączka, zajączek dodaje żądanie do kolejki `request_queue`, wysyła `ACK` do nadawcy, inkrementując swój lokalny zegar Lamporta, i aktualizuje odpowiednią pozycję wektora `last_msg_timestamps` poprzez porównanie znacznika czasowego wiadomości z lokalnym zegarem Lamporta.
3. Po otrzymaniu `RELEASE` od innego zajączka, zajączek usuwa żądanie z kolejki `request_queue`.
4. Zajączki sprawdzają warunki `(W1)` i `(W2)`:
   - `(W1)`: Własne żądanie znajduje się na szczycie kolejki żądań.
   - `(W2)`: Od wszystkich innych zajączków otrzymały wiadomości o starszych znacznikach czasowych.
5. Jeśli warunki `(W1)` i `(W2)` są spełnione, zajączek wybiera polanę na imprezę, wysyła `RELEASE` do wszystkich innych zajączków i organizuje imprezę na wybranej polanie.

**Szczegółowy opis algorytmu**  dla zajączka 'z' przy wyborze jednej z 'p' nierozróżnialnych polan, na której mieści się 's' zajączków:

1. Po otrzymaniu sygnału startu organizacji imprezy, zajączek 'z' inkrementuje swój lokalny zegar Lamporta.
2. Zajączek 'z' wysyła żądania `REQ` wyboru polany na imprezę do wszystkich innych zajączków, aktualizując swój lokalny zegar Lamporta o wartość 1.
3. Po wysłaniu każdego żądania `REQ`, zajączek 'z' oczekuje na potwierdzenie (`ACK`) od każdego innego zajączka.
4. Po otrzymaniu `ACK` od innego zajączka, zajączek 'z' aktualizuje swoje lokalne zegary Lamporta, inkrementując je o 1.
5. Zajączek 'z' umieszcza własne żądanie w kolejce `request_queue`.
6. Po otrzymaniu `REQ` od innego zajączka, zajączek 'z' dodaje żądanie do swojej kolejki `request_queue`, a następnie wysyła `ACK` w odpowiedzi, inkrementując swój lokalny zegar Lamporta o 1 i aktualizując odpowiednią pozycję wektora `last_msg_timestamps`.
7. Po otrzymaniu `RELEASE` od innego zajączka, zajączek 'z' usuwa żądanie z kolejki `request_queue` oraz aktualizuje swój lokalny zegar Lamporta o 1.
8. Zajączek 'z' sprawdza warunki `(W1)` i `(W2)`:
   - `(W1)`: Własne żądanie jest na szczycie kolejki żądań.
   - `(W2)`: Od wszystkich innych zajączków otrzymał wiadomości o starszych znacznikach czasowych.
9. Jeśli warunki `(W1)` i `(W2)` są spełnione, zajączek 'z' wybiera jedną z polan na imprezę, wysyła `RELEASE` do wszystkich innych zajączków i organizuje imprezę na wybranej polanie.
10. Po zakończeniu imprezy, zajączek 'z' informuje o tym wszystkie inne zajączki, a następnie wraca do stanu oczekiwania na kolejną organizację imprezy.