import json
import datetime
import matplotlib.pyplot as plt
import pyfiglet
from termcolor import colored

# Funzione per creare un banner iniziale
def create_banner(text, color, font='slant'):
    ascii_art = pyfiglet.figlet_format(text, font=font)
    colored_art = colored(ascii_art, color)
    return colored_art

text = 'Stop smooking!!'
color = 'green'

# Funzione per caricare i dati dal file
def load_data(file_name):
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Funzione per salvare i dati sul file
def save_data(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

# Funzione per aggiungere un'entrata nel diario giornaliero
def add_entry(data, date, count):
    if date in data:
        data[date] += count
    else:
        data[date] = count
    save_data('diary.json', data)

# Funzione per calcolare statistiche
def calculate_statistics(data):
    total_days = len(data)
    total_cigarettes = sum(data.values())
    if total_days > 0:
        average_per_day = total_cigarettes / total_days
    else:
        average_per_day = 0
    return total_days, total_cigarettes, average_per_day

# Funzione per mostrare messaggi motivazionali
def motivational_message(days_smoke_free):
    messages = [
        "Ottimo lavoro! Continua così!",
        "Ogni giorno senza fumo è un passo verso una vita più sana!",
        "Sei fantastico! Non mollare!",
        "La tua salute ti ringrazierà. Continua così!"
    ]
    print(messages[days_smoke_free % len(messages)])
    
# Funzione per creare un grafico a barre
def plot_smoking_data(data):
    dates = list(data.keys())
    cigarettes = list(data.values())
    
    plt.figure(figsize=(10, 5))
    plt.bar(dates, cigarettes, color='skyblue')
    plt.xlabel('Data')
    plt.ylabel('Numero di sigarette fumate')
    plt.title('Grafico giornaliero delle sigarette fumate')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Main
def main():
    ascii_art = create_banner(text, color)
    print(ascii_art)
    print
    
    data = load_data('diary.json')
    today = datetime.date.today().isoformat()
    
    print("\nBenvenuto nel tuo diario per smettere di fumare!")
    print("Cosa vuoi fare oggi?")
    print("\n1. Aggiungi il numero di sigarette fumate oggi")
    print("\n2. Visualizza le statistiche")
    print("\n3. Mostra il grafico delle sigarette fumate")
    
    choice = input("\nInserisci la tua scelta: ")
    
    if choice == '1':
        count = int(input("\nQuante sigarette hai fumato oggi? "))
        add_entry(data, today, count)
        print("\nEntrata aggiunta con successo!")
    elif choice == '2':
        total_days, total_cigarettes, average_per_day = calculate_statistics(data)
        print(f"\nTotale giorni registrati: {total_days}")
        print(f"\nTotale sigarette fumate: {total_cigarettes}")
        print(f"\nMedia sigarette al giorno: {average_per_day:.2f}")
        
        # Calcola giorni consecutivi senza fumare
        last_date = None
        days_smoke_free = 0
        for date in sorted(data.keys(), reverse=True):
            if data[date] == 0:
                days_smoke_free += 1
            else:
                break
        
        motivational_message(days_smoke_free)
    elif choice == '3':
        plot_smoking_data(data)
        print("")
    else:
        print("Scelta non valida. Riprova!")

if __name__ == "__main__":
    main()
