# Vyhledávání na Google

"""
Autor: Yuriy Tafiy
Email: jtafij@gmail.com
Telefon: 773 656 759
"""


# Importování knihoven Flask a googlesearch
import os
from flask import Flask, render_template, request, send_file
from googlesearch import search

# Inicializace aplikace Flask
app = Flask(__name__)

# Hlavní stránka s vyhledávacím formulářem
@app.route('/')
def index():
    return render_template('Vyhledavani_stranka.html')

# Zobrazení výsledků vyhledávání
@app.route('/results', methods=['POST'])
def results():
    # Získání hodnoty z vyhledávacího pole
    dotaz = request.form.get('dotaz')
    if dotaz:
        # Pokud bylo vyplněno vyhledávací pole, provede se vyhledání na Google
        vysledky_hledani = vyhledat_na_google(dotaz)
        # Vrátíme šablonu s výsledky vyhledávání
        return render_template('Vysledky_hledani.html', dotaz=dotaz, vysledky_hledani=vysledky_hledani)
    else:
        # Pokud pole 'dotaz' není vyplněno, přesměrujeme na stránku s chybovou hláškou
        return render_template('Chyba.html')

# Stažení výsledků vyhledávání do souboru
@app.route('/download', methods=['POST'])
def download_results():
    dotaz = request.form.get('dotaz')
    if dotaz:
        # Pokud bylo vyplněno vyhledávací pole, provede se vyhledání na Google
        vysledky_hledani = vyhledat_na_google(dotaz)
        # Uložení výsledků do souboru
        file_path = ulozit_vysledky_do_souboru(vysledky_hledani)
        # Odeslání souboru uživateli ke stažení
        return send_file(file_path, as_attachment=True)
    else:
        # Pokud pole 'dotaz' není vyplněno, přesměrujeme na stránku s chybovou hláškou
        return render_template('Chyba.html')

# Funkce pro vyhledání výsledků na Google
def vyhledat_na_google(dotaz):
    vysledky = []
    for vysledek in search(dotaz, num=20, stop=20):
        vysledky.append(vysledek)
    return vysledky

# Funkce pro uložení výsledků do souboru
def ulozit_vysledky_do_souboru(vysledky):
    # Cesta k souboru s výsledky
    file_path = os.path.join(os.path.dirname(__file__), 'search_results.txt')
    # Otevření souboru pro zápis
    with open(file_path, 'w') as soubor:
        for vysledek in vysledky:
            soubor.write(vysledek + '\n')
    return file_path

# Spuštění aplikace
if __name__ == '__main__':
    app.run(debug=True)