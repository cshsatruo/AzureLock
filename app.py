import streamlit as st
import random

st.set_page_config(page_title="Blue Lock – pełna wersja", layout="centered")

umiejetnosci = [
    "Kaiser", "Rin", "DonLorenzo", "Sae", "Aiku",
    "Barou", "Shidou", "Nagi", "Isagi"
]

st.title("Blue Lock – Kwalifikacje")

if "gracze" not in st.session_state:
    st.session_state.gracze = []
    st.session_state.umiejetnosci = umiejetnosci.copy()
    st.session_state.stage = 0

if st.session_state.stage == 0:
    liczba = st.number_input("Podaj liczbę graczy:", min_value=1, max_value=len(umiejetnosci), step=1)
    if st.button("Zatwierdź liczbę graczy"):
        st.session_state.liczba_graczy = liczba
        st.session_state.stage = 1

if st.session_state.stage == 1:
    gracze = []
    st.subheader("Wprowadź imiona graczy:")
    for i in range(st.session_state.liczba_graczy):
        imie = st.text_input(f"Gracz {i+1}", key=f"gracz_{i}")
        gracze.append({"imie": imie.strip(), "umiejetnosc": None})
    if st.button("Losuj umiejętności"):
        los = random.sample(st.session_state.umiejetnosci, len(gracze))
        for i, g in enumerate(gracze):
            g["umiejetnosc"] = los[i]
        st.session_state.gracze = gracze
        st.session_state.stage = 2

if st.session_state.stage >= 2:
    st.subheader("Przydzielone umiejętności:")
    for i, g in enumerate(st.session_state.gracze, 1):
        st.write(f"{i}. {g['imie']} → {g['umiejetnosc']}")

    if st.checkbox("Czy są gracze bez umiejętności?"):
        wybrani = st.multiselect(
            "Zaznacz graczy bez umiejętności:",
            options=[f"{i+1}. {g['imie']}" for i, g in enumerate(st.session_state.gracze)]
        )
        if st.button("Wylosuj ponownie dla wybranych"):
            indeksy = [int(s.split(".")[0]) - 1 for s in wybrani]
            zwrocone = [st.session_state.gracze[i]["umiejetnosc"] for i in indeksy]
            for i in indeksy:
                st.session_state.gracze[i]["umiejetnosc"] = None

            przydzielone = [g["umiejetnosc"] for i, g in enumerate(st.session_state.gracze) if i not in indeksy]
            pozostale = [u for u in umiejetnosci if u not in przydzielone]
            random.shuffle(pozostale)

            for i in indeksy:
                if pozostale:
                    st.session_state.gracze[i]["umiejetnosc"] = pozostale.pop()

if "pokaz_druzyny" not in st.session_state:
    st.session_state.pokaz_druzyny = False
if "kapitan1" not in st.session_state:
    st.session_state.kapitan1 = False
if "kapitan2" not in st.session_state:
    st.session_state.kapitan2 = False

if st.button("🔁 Losuj drużyny"):
    random.shuffle(st.session_state.gracze)
    polowa = len(st.session_state.gracze) // 2
    st.session_state.druzyna1 = st.session_state.gracze[:polowa]
    st.session_state.druzyna2 = st.session_state.gracze[polowa:]
    st.session_state.pokaz_druzyny = True

if st.session_state.pokaz_druzyny:
    st.subheader("🏆 Drużyny")

    st.session_state.kapitan1 = st.checkbox("Losować kapitana dla Drużyny 1", key="kap1")
    st.session_state.kapitan2 = st.checkbox("Losować kapitana dla Drużyny 2", key="kap2")

    def wypisz_druzyne(nazwa, druzyna, losuj_kapitana):
        st.markdown(f"### {nazwa}")
        kapitan = random.choice(druzyna) if losuj_kapitana else None
        for g in druzyna:
            ozn = " (KAPITAN)" if g == kapitan else ""
            st.write(f"{g['imie']} – {g['umiejetnosc']}{ozn}")

    wypisz_druzyne("Drużyna 1", st.session_state.druzyna1, st.session_state.kapitan1)
    wypisz_druzyne("Drużyna 2", st.session_state.druzyna2, st.session_state.kapitan2)


    st.info("Kwalifikacje do Blue Lock zakończone.")
