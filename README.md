# 🧠 Quiz Wiedzy

## **📜 Opis projektu**
Stwórz interaktywny Quiz Wiedzy z graficznym interfejsem opartym na Tkinter, który umożliwia użytkownikom sprawdzenie swojej wiedzy w różnych dziedzinach. Aplikacja ma być zaprojektowana zgodnie ze wzorcem MVC (Model-View-Controller), z wykorzystaniem nowoczesnych zagadnień programowania w Pythonie takich jak dziedziczenie, praca z plikami JSON i CSV, wielowątkowość (timer) oraz modularna architektura projektu.

---

## **🎮 Funkcjonalności**
**📄 Wczytywanie pytań**:
- Dane wczytywane z pliku .json.
- Każde pytanie ma:
   - Tekst pytania
   - 4 odpowiedzi (A, B, C, D)
   - Wskaźnik poprawnej odpowiedzi
   - Kategorię tematyczną (np. Historia, Nauka, Kultura)

**🎲 Losowy wybór i kolejność pytań**:
- Za każdym razem losowa kolejność pytań.
- Możliwość wyboru kategorii lub quizu mieszanego.

**✅ Ocenianie odpowiedzi**:
- Informacja zwrotna (feedback) na temat poprawności po każdej odpowiedzi.
- Możliwość przejścia dalej dopiero po udzieleniu odpowiedzi.

**📊 Wyświetlanie wyników końcowych**:
- Podsumowanie: liczba poprawnych odpowiedzi, procent, możliwy komentarz („Świetnie!”, „Spróbuj ponownie”).

**💾 System zapisu wyników**:
- Możliwość zapisania wyników do pliku .csv:
- Imię gracza
- Data
- Wynik
- Czas quizu

**🕒 Limit czasu**:
- Możliwość ustawienia czasu (np. 15 sekund) na odpowiedź na każde pytanie.
- Timer odliczany w osobnym wątku (threading.Timer lub after() z Tkintera).
- Jeśli gracz nie odpowie – odpowiedź uznana za błędną.

**🖥️ Graficzny interfejs użytkownika (GUI)((:
- Zbudowany z użyciem Tkinter, zgodnie z modelem View w MVC.
- Widoki:
- Ekran startowy (z wyborem kategorii lub rozpoczęciem quizu)
- Ekran pytania
- Ekran końcowy z wynikiem
- Historia wyników (opcjonalnie)

---

## **🛠️ Technologie**
- **Python 3.8+**
- **Tkinter** – biblioteka do tworzenia graficznego interfejsu użytkownika.
- **JSON** – format do przechowywania i wczytywania pytań.
- **CSV** – opcjonalnie do zapisu wyników.

---

## **📋 Wymagania**
- Python 3.8 lub nowszy.
- Edytor kodu lub IDE (np. PyCharm, VS Code).
- Opcjonalnie: Wirtualne środowisko Python (`venv`).

---

## **📦 Instalacja**
1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/uzytkownik/quiz-wiedzy.git
   cd quiz-wiedzy

---

## **🔍 Dodatkowe ciekawe zagadnienia (zaawansowane Python)**:
- threading lub Tkinter.after() – implementacja licznika czasu
- Obsługa wyjątków przy wczytywaniu plików JSON
- Dekoratory do logowania interakcji gracza (np. zapisywanie czasu odpowiedzi)
- Enumy (Enum) dla reprezentacji stanów gry lub kategorii
- Unit testy dla modelu (np. testowanie oceniania odpowiedzi)
  
---

## **🚀 Pomysły na rozszerzenia (dla chętnych)**:
- Tryb multiplayer: quiz dla dwóch graczy na zmianę
- Tryb rankingowy: najlepsze wyniki z historii
- API do pobierania pytań z sieci (np. Open Trivia DB)
- Zmienna trudność: łatwe/średnie/trudne pytania


