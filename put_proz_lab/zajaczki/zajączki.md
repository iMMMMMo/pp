### Struktury i zmienne:

- `local_clock`: Zegar Lamporta lokalnego zajączka.
- `request_queue`: Kolejka żądań wyboru polany na imprezę, posortowana po znacznikach czasowych (priorytetach żądań).
- `last_msg_timestamps`: Wektor zegarów Lamporta ostatnio otrzymanych wiadomości od innych zajączków.

### Wiadomości:

- `REQ`: Żądanie wyboru polany na imprezę.
- `RELEASE`: Zwolnienie wybranej polany.
- `ACK`: Potwierdzenie otrzymania żądania.

### Opis

Algorytm pozwala na koordynację zajączków chcących zorganizować imprezę na jednej z P nierozróżnialnych polan. Każda polana może pomieścić S zajączków. Zegary Lamporta są używane do synchronizacji dostępu i zapewnienia spójności stanu.

## Procedura Algorytmu

1. **Inicjacja:**
   - Zajączek na S-tym miejscu jest liderem i decyduje kiedy impreza się zaczyna i kończy.
   - Każdy zajączek utrzymuje lokalny zegar Lamporta, który jest inkrementowany przy każdej akcji komunikacji.
   - Zajączek jest zidentyfikowany unikalnym identyfikatorem (PID).

2. **Wysyłanie żądania:**
   - Zajączek inkrementuje swój lokalny zegar Lamporta.
   - Wysyła żądanie REQ do innych zajączków, zawierając swój zaktualizowany zegar i identyfikator.

3. **Odbieranie żądania:**
   - Po otrzymaniu REQ, zajączek inkrementuje swój zegar Lamporta.
   - Dodaje żądanie do lokalnej kolejki request_queue, sortowanej według zegara Lamporta.
   - Wysyła ACK z powrotem, podbijając swój zegar.

4. **Sprawdzanie warunków wejścia na polanę:**
   - Zajączek czeka na ACK od wszystkich.
   - Sprawdza, czy suma zajączków w żądaniach na szczycie request_queue nie przekracza pojemności S.

5. **Organizacja imprezy:**
   - Jeśli warunki są spełnione, zajączki na szczycie kolejki mogą rozpocząć imprezę.

6. **Zakończenie imprezy:**
   - Po imprezie, zajączek lider wysyła komunikat RELEASE, aby powiadomić o zwolnieniu polany.


