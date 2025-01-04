# simpleWWW

Projekt wykonany na przedmiot Sieci Komputerowe

Projekt zakłada stworzenie prostego serwera WWW wykorzystującego gniazda sieciowe do obsługi żądań klientów, umożliwiając jednoczesny dostęp wielu użytkownikom dzięki zastosowaniu wątków lub procesów. Serwer będzie przetwarzał żądania HTTP, analizując metodę i ścieżkę, a następnie dostarczał pliki statyczne, takie jak .txt lub .html, z wyznaczonego katalogu, jeśli są dostępne. W przypadku braku żądanego pliku lub wystąpienia błędu, serwer zwróci odpowiednią odpowiedź, np. "404 Not Found".

Aplikacja zostanie napisana w Pythonie, korzystając z modułu socket do obsługi gniazd sieciowych. Komunikacja będzie odbywać się przez protokół TCP na wybranym porcie (np. 8080), a dzięki modułowi threading serwer będzie w stanie obsługiwać wielu klientów jednocześnie. Logika działania obejmie analizę nagłówków HTTP, wyszukiwanie plików w katalogu z zasobami oraz przesyłanie ich zawartości z odpowiednim kodem statusu lub informacją o błędzie.

Dodatkowe funkcje i założenia:

Konfiguracja portów i ścieżek: Serwer obsługuje wiele stron na różnych portach, zgodnie z ustawieniami w pliku konfiguracyjnym (config.json). Każdy serwer nasłuchuje na innym porcie i obsługuje inną stronę.

Logowanie: Serwer loguje otrzymane żądania i błędy, co ułatwia monitorowanie działania i debugowanie. Logi są wyświetlane na konsoli.

Obsługa różnych typów MIME: Serwer poprawnie obsługuje różne typy MIME, takie jak .html, .css, .js, .png, .jpg, .jpeg, .gif, co pozwala na serwowanie różnorodnych zasobów.

Obsługa metod HEAD: Serwer obsługuje metodę HEAD, umożliwiając uzyskanie nagłówków bez przesyłania treści.

Zabezpieczenia: Serwer zawiera podstawowe zabezpieczenia przed atakami typu Directory Traversal.

Wielkość bufora: Rozmiar bufora do odbierania danych wynosi 4096 bajtów, co pozwala na obsługę większych plików.
