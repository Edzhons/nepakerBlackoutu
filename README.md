# 🎲 Nepaķer Blackoutu

**Autori:**  
- Nensija Betija Aukmane – Vizuālais noformējums (Figma)  
- Edžus Krūmiņš – Dizaina implementācija, spēles loģikas izstrāde

---

## 🧠 Par projektu

Šī ir Python valodā izstrādāta interaktīva dzeršanas spēle, kas izmanto `tkinter` grafisko interfeisu un ļauj spēlētājiem:

- Mest metamo kauliņu
- Saņemt izaicinājumus (no 6 grūtības līmeņiem)
- Pieņemt izaicinājumu vai iedzert šotu
- Sekot līdzi savam **repekta līmenim** un **dzēruma procentam**
- Sasniegt **uzvaru**, sasniedzot 100% respektu, vai **zaudēt**, piedzeroties līdz blackoutam

Spēle tiek atskaņota pilnekrāna režīmā un tai ir vairākas interaktīvas izvēlnes, tostarp:

- **Noteikumi**
- **Jauna spēle**
- **Autori**
- **Iziet**

---

## 📦 Funkcijas

- 🎲 Metamo kauliņu loģika
- 🧾 Izaicinājumi, kas lasāmi no ārējiem `.txt` failiem
- 🍻 Šotu izvēle un dzeršana
- 📊 Statistikas joslas: piedzēršanās un respekta mērītājs
- 💀 Spēles beigas (uzvara vai zaudējums)
- 📑 Statistika par katru spēli
- 🔁 Iespēja sākt spēli no jauna

---

## 🖥️ Tehnoloģijas

- Python 3
- Tkinter GUI
- `ttk` dizaina komponentes
- Attēlu apstrāde ar `PhotoImage`
- Ievades/izvades operācijas ar `os`, `shutil`, `ctypes`, `subprocess`

---

## 📂 Failsistēmas struktūra

- **`images/`**: Šajā mapē ir visi spēles attēli, piemēram, logotipi, ikonas un fona attēli.
- **`challenges/`**: Šeit ir tekstu faili, kuros tiek definēti izaicinājumi ar dažādiem grūtības līmeņiem.
- **`nepakerBlackoutu.py`**: Galvenais spēles fails, kurš satur visu spēles loģiku un vizuālo noformējumu.
- **`README.md`**: Šis dokuments ar spēles aprakstu un instrukcijām.
- **`nepakerBlackoutu.exe`**: Jau gatavs .exe fails, ko var atvērt un spēlēt spēli.
---

## 🚀 Palaišana

1. Pārliecinies, ka tev ir Python 3 uzstādīts.
2. Instalē nepieciešamos attēlu failus un izaicinājumu tekstus atbilstošās mapēs (`images/`, `challenges/`)
3. Palaid `nepakerBlackoutu.py`:

```bash
python nepakerBlackoutu.py
```
Alternatīvi, vari instalēt nepakerBlackoutu.exe un palaist to.

---
## 📜 Licence

Šis projekts tiek izplatīts bez konkrētas licences. Tomēr, ja vēlies izmantot, mainīt vai izplatīt šo projektu, tev jānorāda autoru vārdi un jāsaņem atļauja no autora.

Visas tiesības uz šo projektu pieder autoriem. Projekts tiek piedāvāts bez jebkādas garantijas vai atbildības.

---
