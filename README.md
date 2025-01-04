#simpleWWW

Projekt wykonany na przedmiot Sieci Komputerowe

Projekt zakłada stworzenie prostego serwera WWW wykorzystującego gniazda sieciowe do obsługi żądań klientów, umożliwiając jednoczesny dostęp wielu użytkownikom dzięki zastosowaniu wątków lub procesów. Serwer będzie przetwarzał żądania HTTP, analizując metodę i ścieżkę, a następnie dostarczał pliki statyczne, takie jak .txt lub .html, z wyznaczonego katalogu, jeśli są dostępne. W przypadku braku żądanego pliku lub wystąpienia błędu, serwer zwróci odpowiednią odpowiedź, np. "404 Not Found".
Aplikacja zostanie napisana w Pythonie, korzystając z modułu socket do obsługi gniazd sieciowych. Komunikacja będzie odbywać się przez protokół TCP na wybranym porcie (np. 8080), a dzięki modułowi threading serwer będzie w stanie obsługiwać wielu klientów jednocześnie. Logika działania obejmie analizę nagłówków HTTP, wyszukiwanie plików w katalogu z zasobami oraz przesyłanie ich zawartości z odpowiednim kodem statusu lub informacją o błędzie.
