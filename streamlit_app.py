import streamlit as st
import time
import pandas as pd

# --- KONFIGURACJA TESTU ---
TIME_LIMIT_MINUTES = 10
TOTAL_TIME_SECONDS = TIME_LIMIT_MINUTES * 60

# --- BAZA PYTAŃ ---
questions_db = [
    # --- C# ADVANCED ---
    {
        "category": "C# Advanced",
        "question": "Dlaczego `Span<T>` nie może być polem w klasie (class field)?",
        "options": [
            "A. Ponieważ jest to typ referencyjny zarządzany przez GC.",
            "B. Ponieważ jest to `ref struct` i musi być alokowany tylko na stosie (stack-only).",
            "C. Ponieważ nie implementuje interfejsu `IEnumerable<T>`.",
            "D. Może być polem w klasie, jeśli klasa jest oznaczona jako `sealed`."
        ],
        "answer": "B"
    },
    {
        "category": "C# Advanced",
        "question": "Co się stanie, jeśli w metodzie `async` zwracającej `Task` wyrzucisz wyjątek przed pierwszym wystąpieniem `await`?",
        "options": [
            "A. Wyjątek zostanie opakowany w zwracany Task (Task.Faulted).",
            "B. Wyjątek zostanie rzucony synchronicznie do metody wywołującej.",
            "C. Wyjątek zostanie zignorowany (swallowed) przez maszynę stanów.",
            "D. Kompilator nie pozwoli na taki kod."
        ],
        "answer": "B"
    },
    {
        "category": "C# Advanced",
        "question": "W kontekście Entity Framework Core, na czym polega problem 'Cartesian Explosion'?",
        "options": [
            "A. Na zbyt dużej liczbie migracji w folderze projektu.",
            "B. Na wycieku pamięci przy użyciu `AsNoTracking()`.",
            "C. Na generowaniu złączeń (JOIN) dla wielu kolekcji `Include`, co powoduje wykładniczy wzrost liczby zwracanych wierszy.",
            "D. Na błędzie przy próbie zapisu grafu obiektów z cyklicznymi referencjami."
        ],
        "answer": "C"
    },

    # --- REACT & TYPESCRIPT ---
    {
        "category": "React & TS",
        "question": "Jaka jest kluczowa różnica między `useMemo` a `useCallback`?",
        "options": [
            "A. `useMemo` służy do efektów ubocznych, a `useCallback` do renderowania.",
            "B. `useMemo` memoizuje wynik wywołania funkcji, a `useCallback` memoizuje samą instancję funkcji.",
            "C. `useCallback` działa tylko w komponentach klasowych.",
            "D. Nie ma różnicy, to aliasy tej samej funkcji."
        ],
        "answer": "B"
    },
    {
        "category": "React & TS",
        "question": "Co robi typ `Omit<T, K>` w TypeScript?",
        "options": [
            "A. Tworzy nowy typ, wybierając tylko właściwości K z T.",
            "B. Tworzy nowy typ, usuwając właściwości K z typu T.",
            "C. Sprawia, że wszystkie właściwości typu T stają się opcjonalne.",
            "D. Tworzy unię typów T i K."
        ],
        "answer": "B"
    },
    {
        "category": "React & TS",
        "question": "W Redux Toolkit, dlaczego możemy pisać kod wyglądający na mutowalny (np. `state.value = 123`) w reducerach?",
        "options": [
            "A. Redux Toolkit wyłącza sprawdzanie niemutowalności w trybie produkcyjnym.",
            "B. Używa pod spodem biblioteki Immer, która wykorzystuje Proxy do śledzenia zmian i tworzenia nowej kopii stanu.",
            "C. Jest to nowa funkcja JavaScript ES2022.",
            "D. To błąd, nie wolno tak pisać nawet w Redux Toolkit."
        ],
        "answer": "B"
    },
    {
        "category": "React & TS",
        "question": "Jak TanStack Query (React Query) domyślnie traktuje dane, gdy użytkownik przełącza się między oknami przeglądarki (window focus)?",
        "options": [
            "A. Nic nie robi, czeka na ręczne odświeżenie.",
            "B. Czyści cache natychmiast.",
            "C. Oznacza dane jako 'stale' i automatycznie ponawia pobieranie (refetch) w tle.",
            "D. Pobiera dane tylko jeśli cache jest starszy niż 5 minut."
        ],
        "answer": "C"
    },

    # --- ARCHITECTURE (DDD, CQRS, SOLID) ---
    {
        "category": "Architecture",
        "question": "W DDD, jaka jest główna zasada dotycząca modyfikacji danych wewnątrz Agregatu?",
        "options": [
            "A. Można modyfikować dowolną encję w agregacie bezpośrednio z serwisu aplikacyjnego.",
            "B. Modyfikacje mogą zachodzić tylko poprzez metody korzenia agregatu (Aggregate Root), aby zapewnić spójność niezmienników.",
            "C. Agregaty służą tylko do odczytu, do zapisu używamy DTO.",
            "D. Każda encja w agregacie musi mieć publiczne settery."
        ],
        "answer": "B"
    },
    {
        "category": "Architecture",
        "question": "W Modular Monolith, jak powinna wyglądać komunikacja między dwoma niezależnymi modułami?",
        "options": [
            "A. Poprzez bezpośrednie wstrzykiwanie DbContextu jednego modułu do drugiego.",
            "B. Poprzez publiczne interfejsy (Public API) modułu lub asynchronicznie przez zdarzenia (Events).",
            "C. Poprzez wspólną bazę danych i widoki SQL.",
            "D. Moduły nie powinny się komunikować."
        ],
        "answer": "B"
    },
    {
        "category": "Architecture",
        "question": "Która zasada SOLID mówi o tym, że 'klasy nie powinny być zmuszane do implementowania interfejsów, których nie używają'?",
        "options": [
            "A. Single Responsibility Principle.",
            "B. Liskov Substitution Principle.",
            "C. Interface Segregation Principle.",
            "D. Dependency Inversion Principle."
        ],
        "answer": "C"
    },

    # --- MESSAGING & TOOLS (Kafka, Docker, Wolverine, Dapr) ---
    {
        "category": "Messaging & Tools",
        "question": "W Apache Kafka, co się stanie, gdy dodasz nowego konsumenta do grupy konsumenckiej (Consumer Group), która ma mniej członków niż partycji w topicu?",
        "options": [
            "A. Nowy konsument będzie bezczynny.",
            "B. Nastąpi rebalans (Rebalance) i nowy konsument przejmie część partycji.",
            "C. Kafka rzuci wyjątek o duplikacji ID.",
            "D. Nowy konsument otrzyma kopię wszystkich wiadomości od początku."
        ],
        "answer": "B"
    },
    {
        "category": "Messaging & Tools",
        "question": "Jaka jest główna cecha biblioteki WolverineFx w porównaniu do MediatR?",
        "options": [
            "A. WolverineFx nie wspiera wzorca Mediator.",
            "B. WolverineFx wykorzystuje generowanie kodu (Roslyn source generators) w czasie kompilacji/uruchomienia, aby uniknąć narzutu Reflection.",
            "C. WolverineFx działa tylko z RabbitMQ.",
            "D. WolverineFx jest biblioteką frontendową."
        ],
        "answer": "B"
    },
    {
        "category": "Messaging & Tools",
        "question": "W architekturze opartej o DAPR, w jaki sposób Twoja aplikacja zazwyczaj komunikuje się z komponentami Dapr (np. State Store)?",
        "options": [
            "A. Poprzez bezpośrednie połączenie TCP do bazy danych.",
            "B. Poprzez sidecar (HTTP/gRPC) działający obok aplikacji.",
            "C. Poprzez wstrzyknięcie biblioteki DLL Dapr do jądra systemu.",
            "D. Dapr zastępuje Kubernetes i przejmuje ruch sieciowy."
        ],
        "answer": "B"
    },
    {
        "category": "Messaging & Tools",
        "question": "Co robi instrukcja `COPY . .` w pliku Dockerfile?",
        "options": [
            "A. Kopiuje pliki z kontenera na hosta.",
            "B. Kopiuje pliki z bieżącego katalogu kontekstu budowania (host) do katalogu roboczego obrazu.",
            "C. Duplikuje warstwę obrazu.",
            "D. Kopiuje pliki z repozytorium Git."
        ],
        "answer": "B"
    },

    # --- NICE TO HAVE (1 question each) ---
    {
        "category": "Nice to Have",
        "question": "Telerik UI for React: Czym jest KendoReact w kontekście zależności?",
        "options": [
            "A. Jest wrapperem na jQuery.",
            "B. To zestaw natywnych komponentów React, które nie mają zależności od jQuery.",
            "C. Wymaga zainstalowania Angulara.",
            "D. To silnik renderujący po stronie serwera."
        ],
        "answer": "B"
    },
    {
        "category": "Nice to Have",
        "question": "SignalR: Co to jest 'Hub'?",
        "options": [
            "A. Fizyczne urządzenie sieciowe.",
            "B. Klasa po stronie serwera, która zarządza połączeniami, grupami i wysyłaniem wiadomości do klientów.",
            "C. Klient JavaScript do łączenia się z WebSocket.",
            "D. Baza danych dla wiadomości real-time."
        ],
        "answer": "B"
    },
    {
        "category": "Nice to Have",
        "question": "MongoDB: Czym różni się dokument w MongoDB od wiersza w SQL?",
        "options": [
            "A. Dokumenty mają sztywny schemat, wiersze nie.",
            "B. Dokumenty to struktury BSON (binarny JSON), mogą być zagnieżdżone i nie muszą mieć identycznego schematu w ramach kolekcji.",
            "C. Dokumenty nie mają klucza głównego.",
            "D. Nie ma różnicy."
        ],
        "answer": "B"
    },
    {
        "category": "Nice to Have",
        "question": "SQL (Postgres/MSSQL): Jaka jest różnica między `UNION` a `UNION ALL`?",
        "options": [
            "A. `UNION` łączy wyniki i usuwa duplikaty (wolniejsze), `UNION ALL` łączy wszystko jak leci (szybsze).",
            "B. `UNION` jest tylko dla liczb, `UNION ALL` dla tekstów.",
            "C. `UNION ALL` usuwa duplikaty.",
            "D. `UNION` sortuje wyniki, `UNION ALL` losuje kolejność."
        ],
        "answer": "A"
    },
    {
        "category": "Nice to Have",
        "question": "xUnit: Jak w xUnit oznacza się test, który przyjmuje parametry (Data Driven Test)?",
        "options": [
            "A. `[Test]` i `[TestCase]`",
            "B. `[Fact]`",
            "C. `[Theory]` i `[InlineData]` (lub `[MemberData]`)",
            "D. `[TestMethod]` i `[DataRow]`"
        ],
        "answer": "C"
    },
    {
        "category": "Nice to Have",
        "question": "Auth (Keycloak/JWT): Co zawiera 'payload' w tokenie JWT?",
        "options": [
            "A. Tylko podpis cyfrowy.",
            "B. Zaszyfrowane hasło użytkownika.",
            "C. Claims (roszczenia) - czyli dane o użytkowniku i uprawnieniach (niezaszyfrowane, tylko zakodowane Base64).",
            "D. Klucz prywatny serwera."
        ],
        "answer": "C"
    },
    {
        "category": "Nice to Have",
        "question": "Grafana: Do czego służy 'Data Source' w Grafanie?",
        "options": [
            "A. Do generowania wykresów kołowych.",
            "B. Jest to backend, z którego Grafana pobiera metryki (np. Prometheus, InfluxDB, SQL).",
            "C. To miejsce, gdzie Grafana zapisuje swoje logi.",
            "D. To wtyczka do eksportu PDF."
        ],
        "answer": "B"
    },
    {
        "category": "API Design",
        "question": "OpenAPI (Swagger): Co definiuje sekcja 'components/schemas'?",
        "options": [
            "A. Listę endpointów API.",
            "B. Modele danych (obiekty) używane w żądaniach i odpowiedziach, pozwalające na ich reużywalność.",
            "C. Konfigurację serwera.",
            "D. Dane autoryzacyjne."
        ],
        "answer": "B"
    },
    {
        "category": "C# Advanced",
        "question": "Co oznacza słowo kluczowe `volatile` w C#?",
        "options": [
            "A. Że zmienna może być null.",
            "B. Że pole może być modyfikowane przez wiele wątków i kompilator/CPU nie powinien optymalizować odczytów (cache'ować w rejestrach).",
            "C. Że zmienna jest stała.",
            "D. Że zmienna jest zapisywana na dysku."
        ],
        "answer": "B"
    },
    {
        "category": "React & TS",
        "question": "Co robi Vite w trybie deweloperskim (dev server), co odróżnia go od Webpacka?",
        "options": [
            "A. Bundluje całą aplikację przy każdym zapisie.",
            "B. Używa natywnych modułów ES (ESM) w przeglądarce, serwując pliki na żądanie bez pełnego bundlowania.",
            "C. Kompiluje kod do C++.",
            "D. Nie obsługuje TypeScript."
        ],
        "answer": "B"
    },
    {
        "category": "Architecture",
        "question": "W CQRS, co to jest 'Eventual Consistency' (spójność ostateczna)?",
        "options": [
            "A. Błąd w systemie, który należy naprawić.",
            "B. Sytuacja, w której model odczytu (Read Model) może przez chwilę nie być zaktualizowany względem modelu zapisu, ale z czasem osiągnie spójność.",
            "C. Gwarancja, że dane są zawsze spójne w momencie zapisu.",
            "D. Mechanizm transakcji rozproszonych."
        ],
        "answer": "B"
    }
]

# --- LOGIKA APLIKACJI ---

st.set_page_config(page_title="Senior Dev Test", layout="centered")

# Inicjalizacja stanu
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'test_started' not in st.session_state:
    st.session_state.test_started = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'test_finished' not in st.session_state:
    st.session_state.test_finished = False

def finish_test():
    st.session_state.test_finished = True

# --- EKRAN STARTOWY ---
if not st.session_state.test_started:
    st.title("Rekrutacja Wewnętrzna: Senior C# & React")
    st.markdown(f"""
    ### Zasady testu:
    *   **Rola:** Senior C# & React Developer
    *   **Liczba pytań:** {len(questions_db)}
    *   **Czas:** {TIME_LIMIT_MINUTES} minut (zegar tyka bezlitośnie!)
    *   **Zakres:** C#, .NET, React, TS, Architektura, Cloud, Tools.
    
    Test sprawdza głęboką wiedzę, a nie umiejętność Googlowania. Powodzenia!
    """)
    
    if st.button("ROZPOCZNIJ TEST"):
        st.session_state.test_started = True
        st.session_state.start_time = time.time()
        st.rerun()

# --- EKRAN WYNIKÓW ---
elif st.session_state.test_finished:
    st.title("Koniec Testu")
    
    score = st.session_state.score
    total = len(questions_db)
    percentage = (score / total) * 100
    
    # Sprawdzenie czasu
    end_time = time.time()
    duration = end_time - st.session_state.start_time
    time_penalty = False
    
    if duration > TOTAL_TIME_SECONDS + 10: # 10s buforu
        st.error(f"PRZEKROCZONO CZAS! Twój czas: {int(duration//60)}m {int(duration%60)}s. Limit: {TIME_LIMIT_MINUTES}m.")
        st.warning("Wynik może nie zostać uznany.")
        time_penalty = True
    else:
        st.success(f"Ukończono w czasie: {int(duration//60)}m {int(duration%60)}s")

    st.metric(label="Twój Wynik", value=f"{score} / {total}", delta=f"{percentage:.1f}%")
    
    if percentage >= 80 and not time_penalty:
        st.balloons()
        st.success("Poziom: SENIOR / ARCHITECT. Gratulacje!")
    elif percentage >= 60:
        st.info("Poziom: MID / REGULAR. Dobra robota, ale są braki w zaawansowanych tematach.")
    else:
        st.error("Poziom: JUNIOR. Wymagana nauka z zakresu architektury i internals.")

    with st.expander("Zobacz szczegółowe odpowiedzi"):
        for i, q in enumerate(questions_db):
            user_ans = st.session_state.answers.get(i, "Brak")
            correct = q['answer']
            color = "green" if user_ans == correct else "red"
            st.markdown(f"**{i+1}. {q['question']}**")
            st.markdown(f":{color}[Twoja odp: {user_ans}] | Poprawna: {correct}")
            st.divider()
            
    if st.button("Zrestartuj (dla kolejnego kandydata)"):
        st.session_state.clear()
        st.rerun()

# --- EKRAN TESTU ---
else:
    # Sprawdzanie czasu w tle (przy każdej interakcji)
    elapsed = time.time() - st.session_state.start_time
    remaining = TOTAL_TIME_SECONDS - elapsed
    
    if remaining <= 0:
        st.error("CZAS MINĄŁ!")
        finish_test()
        st.rerun()

    # Pasek postępu i Timer
    col1, col2 = st.columns([3, 1])
    with col1:
        progress = (st.session_state.current_question / len(questions_db))
        st.progress(progress, text=f"Pytanie {st.session_state.current_question + 1} z {len(questions_db)}")
    with col2:
        st.metric("Pozostały czas", f"{int(remaining//60)}:{int(remaining%60):02d}")

    # Wyświetlanie pytania
    q_index = st.session_state.current_question
    q_data = questions_db[q_index]

    st.subheader(f"[{q_data['category']}]")
    st.markdown(f"#### {q_data['question']}")

    # Formularz odpowiedzi
    # Używamy klucza unikalnego dla pytania, aby radio button się resetował
    answer = st.radio(
        "Wybierz odpowiedź:",
        q_data['options'],
        key=f"q_{q_index}",
        index=None
    )

    # Przycisk Dalej
    if st.button("Zatwierdź i Dalej", type="primary"):
        if answer is None:
            st.warning("Musisz wybrać odpowiedź!")
        else:
            # Zapisz odpowiedź (tylko literę A, B, C, D)
            selected_letter = answer[0]
            st.session_state.answers[q_index] = selected_letter
            
            # Sprawdź poprawność
            if selected_letter == q_data['answer']:
                st.session_state.score += 1
            
            # Przejdź dalej
            if st.session_state.current_question < len(questions_db) - 1:
                st.session_state.current_question += 1
                st.rerun()
            else:
                finish_test()
                st.rerun()
