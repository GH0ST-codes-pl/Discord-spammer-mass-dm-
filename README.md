# Discord Mass DM Advertiser (Selfbot)
**Created by GH0ST-codes-pl**

[English](#english) | [Polski](#polski)

---

<a name="english"></a>
## 🇺🇸 English

A multi-functional Discord Selfbot for Mass Direct Messaging and sending single targeted messages.

**⚠️ DISCLAIMER: Selfbots are against Discord ToS. Use at your own risk. The creator is not responsible for any bans.**

### Features
- **Mass DM**: Scrapes members from a server and sends them messages.
- **Single User DM**: Send messages to a specific user ID.
- **Spam Mode**: Send multiple messages to a single user.
- **Image Support**: Send images along with text.
- **Header Caching**: Optimized performance preventing rate-limits.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/GH0ST-codes-pl/Discord-spammer-mass-dm-.git
    cd Discord-spammer-mass-dm-
    ```

2.  **Install Dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    # Linux/termux
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
    *(On Windows use `.venv\Scripts\activate`)*

3.  **Configuration:**
    Open `data/tokens.txt` and paste your Discord tokens (one per line).

### Usage
Run the bot:
```bash
python main.py
```

Follow the on-screen prompts:
1.  **Delay**: Time in seconds between messages (e.g., `2`).
2.  **Image Path**: Path to an image file (optional, press Enter to skip).
3.  **Mode**:
    - `[1] Single User`: Target one specific user. You can specify the **Amount** of messages to spam.
    - `[2] Mass DM`: Prompts for a server Invite Code to join and scrape members.

---

<a name="polski"></a>
## 🇵🇱 Polski

Wielofunkcyjny Selfbot Discord do masowego wysyłania wiadomości prywatnych (DM) oraz targetowania pojedynczych użytkowników.

**⚠️ UWAGA: Selfboty są niezgodne z Regulaminem Discorda. Używasz na własną odpowiedzialność. Twórca nie odpowiada za blokady kont.**

### Funkcje
- **Mass DM**: Pobiera listę użytkowników z serwera i wysyła im wiadomości.
- **Single User DM**: Wysyłanie wiadomości do konkretnego ID użytkownika.
- **Tryb Spam**: Możliwość wysłania wielu wiadomości do jednej osoby.
- **Wysyłanie Zdjęć**: Obsługa załączników graficznych.
- **Cache Nagłówków**: Zoptymalizowane działanie zapobiegające blokowaniu zapytań.

### Instalacja

1.  **Pobierz repozytorium:**
    ```bash
    git clone https://github.com/GH0ST-codes-pl/Discord-spammer-mass-dm-.git
    cd Discord-spammer-mass-dm-
    ```

2.  **Zainstaluj Biblioteki:**
    Zalecane jest użycie środowiska wirtualnego.
    ```bash
    # Linux/Termux
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
    *(Na Windows użyj `.venv\Scripts\activate`)*

3.  **Konfiguracja:**
    Otwórz plik `data/tokens.txt` i wklej swoje tokeny Discord (każdy w nowej linii).

### Użycie
Uruchom bota:
```bash
python main.py
```

Postępuj zgodnie z instrukcjami w terminalu:
1.  **Delay**: Czas (w sekundach) między wiadomościami.
2.  **Image Path**: Ścieżka do pliku ze zdjęciem (opcjonalne, wciśnij Enter by pominąć).
3.  **Mode**:
    - `[1] Single User`: Wysyłanie do jednego użytkownika. Możesz określić **Ilość** (Amount) powtórzeń.
    - `[2] Mass DM`: Zapyta o Kod Zaproszenia (Invite) do serwera, aby do niego dołączyć i pobrać listę osób.
