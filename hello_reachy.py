from reachy_mini import ReachyMini
from reachy_mini.motion.recorded_move import RecordedMoves
import time
import random
import pygame

# Pre-carica le librerie di movimenti
emotions = RecordedMoves("pollen-robotics/reachy-mini-emotions-library")
dances   = RecordedMoves("pollen-robotics/reachy-mini-dances-library")

# Animazioni del robot
print(emotions.list_moves())
print(dances.list_moves())

print("Connessione a Reachy Mini in simulazione...")
pygame.mixer.init()

# Lista di domande iniziali (che pesca con il random.choice())
domande_iniziali = ["Come stai?", "Come stai trascorrendo questa giornata?"]

# Lista di comandi uscita
comandi_uscita = ["stop", "fine", "basta", "non continuare", "fermiamoci qui", "fermiamoci", "fermo", "fermati qui", "non ho più voglia"]

# Inizio FUNZIONI
# Funzione 'parla' di Reachy
def parla(testo):
   print(f"\nReachy: {testo}")
   time.sleep(1)

# Funzione di risposta dell'utente
def ascolta(nome=None):
    if nome:
       return input(f"{nome}: ").strip().lower()
    else:
       return input("Utente: ").strip().lower()

# Funzione di saluto iniziale
def saluto_iniziale():
    move = emotions.get("proud2")
    mini.play_move(move)
    parla("Ciao! Io sono Reachy, il tuo compagno nelle attività di oggi, sono molto contento di conoscerti. Tu come ti chiami?")
    return ascolta()

# Funzione per fare la domanda e attendere la risposta dell'utente
def fai_domanda_e_aspetta(mini, domanda):  
    parla(domanda)
    return ascolta(nome)

# Funzione di controllo uscita: se l'utente scrive una delle parole presenti nella lista, il robot interrompe l'interazione
def controlla_uscita(risposta):
    return risposta in comandi_uscita

# Funzione in cui Reachy chiede di raccontare un ricordo legato alla canzone nel quiz musicale
def chiedi_ricordo(mini):
    move = emotions.get("curious1")
    mini.play_move(move)
    ricordo = fai_domanda_e_aspetta(
        mini,
        "Questa canzone è legata a qualche ricordo della tua gioventù? Se sì, ti va di raccontarmelo?")
    
    # Controlla se l'utente vuole interrompere
    if controlla_uscita(ricordo):
        return True
    
    # Se l'utente condivide, Reachy accoglie la risposta
    if not "no" in ricordo:
       move = emotions.get("grateful1")
       mini.play_move(move)

       parla("Ti ringrazio per aver condiviso con me questo ricordo.")
       parla("Ora possiamo continuare con il nostro gioco!")
    # Se l'utente non vuole condividere, Reachy continua con l'attività, senza insistenza e rassicurando
    else:
       parla("Va bene... non fa niente! Possiamo comunque continuare con l'attività.")
    return False

# Funzione del gioco associazione parola-categoria
def gioco_parole(mini, nome):
    parole_categorie = {
    "mela": ["frutta", "frutto"],
    "tulipano": ["fiore", "fiori"],
    "cane": ["animale", "animali"],
    "flamenco": ["ballo", "danza"],
    "collana": ["accessori", "accessorio"],
    "pesca": ["frutta", "frutto"],
    "gatto": ["animale", "animali"]
   }
    
    # Parola : indizio
    indizi_categorie = {
    "mela": "Si mangia alla fine di un pasto.",
    "tulipano": "Si trovano spesso nei giardini e sono molto colorati.",
    "cane": "Alcuni di loro hanno le ali, altri sono a quattro zampe e puoi trovarli anche negli zoo.",
    "flamenco": "Si può fare in coppia e a suon di musica.",
    "collana": "Li indossi per arricchire l'abbigliamento.",
    "pesca": "Si mangia alla fine di un pasto.",
    "gatto": "Alcuni di loro hanno le ali, altri sono a quattro zampe e puoi trovarli anche negli zoo."
   }
    
    # Parola : spiegazione
    recupero_categoria = {
    "mela": "La mela infatti ha i semi, per questo fa parte di questo gruppo!",
    "tulipano": "Il tulipano infatti fa parte di questo gruppo perchè ha i petali e profuma molto!",
    "cane": "Il cane è un animale a quattro zampe, abbaia e scodinzola, per questo fa parte di questo gruppo!",
    "flamenco": "Come il valzer e la baciata, il flamenco è un ballo, quindi fa parte di questa categoria!",
    "collana": "E' un oggetto che usiamo per abbellirci, per questo è un accessorio!",
    "pesca": "La pesca infatti ha un seme, per questo fa parte di questo gruppo!",
    "gatto": "Il gatto è un animale a quattro zampe, miagola e può fare molta compagnia, per questo fa parte di questo gruppo!",
   }

    # Stampa le regole del gioco e aspetta un secondo tra una frase e l'altra per dare il tempo all'utente per comprendere le regole
    move = emotions.get("helpful1")
    mini.play_move(move)

    parla("Bene! Ti dirò una parola e tu mi dovrai dire a quale categoria appartiene.")
    parla("E' tutto chiaro? Se non è chiaro, te lo rispiego senza problemi! E ricordati che puoi sempre scegliere quando interrompere l'attività, basta solo che me lo dica!")

    # L'utente ha capito?
    capito = ascolta(nome)

    # Controlla se l'utente vuole interrompere
    if controlla_uscita(capito):
       return True
    
    move = emotions.get("proud2")
    mini.play_move(move)

   # Se l'utente non ha capito, Reachy rispiega il gioco
    while "no" in capito:
        move = emotions.get("helpful2")
        mini.play_move(move)

        # Reachy rispiega le regole del gioco fornendo esempi. Aspetta un secondo tra una spiegazione e l'altra per dare il tempo all'utente di ascoltare e comprendere
        parla("Non c'è alcun problema, te lo rispiego subito.")
        parla("Ti dirò una parola e tu proverai a indovinare a quale categoria appartiene.")
        parla("Ad esempio: 'fragola' appartiene alla categoria 'frutta'. 'Collana' appartiene alla categoria 'accessori'.")
        parla("Puoi prenderti tutto il tempo che ti serve per rispondere e se non sei sicuro possiamo ragionare insieme!")
        parla("Adesso ti sembra più chiaro?")

        # L'utente ha capito?
        capito = ascolta(nome)

       # Controlla se l'utente vuole interrompere
        if controlla_uscita(capito):
           return True

    # Se l'utente ha capito, inizia il gioco
    parla(f"Perfetto {nome}! Allora possiamo iniziare.")

   # Contatore per controllare ogni quante risposte chiedere se continuare
    contatore = 0

   # Con un ciclo for, stampa una a una le parole dell'attività
    for parola in parole_categorie:

        risposta = fai_domanda_e_aspetta(
        mini,
        f"A quale categoria appartiene la parola {parola}?")

       # Controlla se l'utente vuole interrompere
        if controlla_uscita(risposta):
           return True

        categoria_corretta = parole_categorie[parola]

        spiegazione_categoria = recupero_categoria[parola]

        # Lista delle reazioni alla risposta corretta
        risposte_corrette = [f"Esatto, ottima risposta {nome}! Continua così!",
                            f"Stai andando alla grande {nome}! Hai risposto correttamente.",
                            f"Molto bene {nome}! Stai andando alla grande."]

        # Lista delle reazioni alla risposta sbagliata + spiegazione del perchè la risposta è sbagliata
        risposte_sbagliate_categoria = [f"Non ti preoccupare, non era facilissimo! La categoria che cercavo era {categoria_corretta[0]}. {spiegazione_categoria} Ma apprezzo molto il tuo impegno!",
                                       f"La risposta corretta è {categoria_corretta[0]}. {spiegazione_categoria} Ma non preoccuparti, stai andando molto bene!",
                                       f"Non ti preoccupare, la memoria a volta ci fa piccoli scherzi! La risposta corretta è {categoria_corretta[0]}. {spiegazione_categoria}"]

       # Se la risposta è corretta, stampa una frase random tra quelle della lista
        if risposta in categoria_corretta:
           move = emotions.get("success1")
           mini.play_move(move)

           parla(random.choice(risposte_corrette))

       # Al primo sbaglio, dà un indizio
        else:
            move = emotions.get("thoughtful1")
            mini.play_move(move)

            parla(f"Ti do un piccolo indizio... {indizi_categorie[parola]}")
            risposta = ascolta(nome)

           # Controlla se l'utente vuole interrompere
            if controlla_uscita(risposta):
                   return True

            if risposta in categoria_corretta:
               move = emotions.get("success1")
               mini.play_move(move)

               parla(random.choice(risposte_corrette))
           # Se la risposta è errata, stampa una frase random tra quelle della lista
            else:
                move = emotions.get("helpful1")
                mini.play_move(move)

                parla(random.choice(risposte_sbagliate_categoria))

        contatore += 1

       # Ogni due domande il robot chiede se continuare
        if contatore == 2:
            move = emotions.get("curious1")
            mini.play_move(move)
            scelta = fai_domanda_e_aspetta(
                mini,
                "Vuoi continuare con questa attività oppure cambiamo gioco? Ricordati sempre che possiamo fermarci quando vuoi.")

           # Controlla se l'utente vuole interrompere
            if controlla_uscita(scelta):
                return True

            # Se l'utente vuole cambiare attività, si torna al quiz musicale
            elif "camb" in scelta:
                move = emotions.get("helpful2")
                mini.play_move(move)

                parla(f"Certo {nome}, cambiamo attività! Ti propongo un quiz musicale molto divertente.")

                return quiz_musicale(mini, nome)

            else:
                parla("Molto bene, allora continuiamo!")

            # Il contatore ritorna a 0 e riparte con l'attività
            contatore = 0

    parla("Abbiamo terminato il gioco delle parole.")
    move = emotions.get("proud2")
    mini.play_move(move)

    return False

# Funzione del gioco associazione canzone-cantante
def quiz_musicale(mini, nome):
   # Dizionario chiave : valore -> canzone : cantante
    canzone_cantante = {
    "Triangolo": ["renato zero", "zero"],
    "Banane e lamponi": ["gianni morandi", "morandi"],
    "Ballo ballo": ["raffaella carrà", "la carrà"],
    "Se telefonando": ["mina", "mina mazzini"],
    "Almeno tu nell'universo": ["mia martini", "la martini"],
    "Il ballo del mattone": ["rita pavone", "la pavone"],
    "Sapore di sale": ["gino paoli", "paoli"],
    "Abbronzatissima": ["edoardo vianello", "vianello"]
    }

   # Canzone : indizio
    indizi_cantanti = {
    "Triangolo": "Il cognome è un numero.",
    "Banane e lamponi": "E' famoso per farsi mandare a prendere il latte.",
    "Ballo ballo": "E' famosa per il suo caschetto biondo.",
    "Se telefonando": "È una delle voci femminili italiane più belle e famose.",
    "Almeno tu nell'universo": "E' la sorella di Loredana Bertè.",
    "Il ballo del mattone": "Il suo cognome fa pensare alle piume.",
    "Sapore di sale": "Il cantante canta anche il brano 'Il cielo in una stanza'.",
    "Abbronzatissima": "Il cantante canta anche il brano 'I Watussi'."
    }

    move = emotions.get("helpful1")
    mini.play_move(move)

    # Stampa le regole del gioco e aspetta un secondo tra una frase e l'altra per dare il tempo all'utente per comprendere le regole
    parla("Bene! Ti dirò il titolo di una canzone e tu proverai a dirmi chi è il cantante.")
    parla("E' tutto chiaro? Se non è chiaro, te lo rispiego senza problemi! Ricordati che possiamo interrompere l'attività quando preferisci.")

    # L'utente ha capito?
    capito = ascolta(nome)

    # Controlla se l'utente vuole interrompere
    if controlla_uscita(capito):
        return True
    
    move = emotions.get("proud2")
    mini.play_move(move)

    # Se l'utente non ha capito, Reachy rispiega il gioco
    while "no" in capito:

        move = emotions.get("helpful2")
        mini.play_move(move)

        parla("Non c'è alcun problema, te lo rispiego subito.")

        # Reachy rispiega le regole del gioco fornendo esempi. Aspetta un secondo tra una spiegazione e l'altra per dare il tempo all'utente di ascoltare e comprendere
        parla("Ti dirò il titolo di una canzone e tu proverai ad associarla al suo cantante.")
        parla("Ad esempio: 'L'estate sta finendo' è cantata da Righeira. 'Tanti auguri' è cantata da Raffaella Carrà.")
        parla("Puoi prenderti tutto il tempo che ti serve per rispondere e se non sei sicuro possiamo ragionare insieme.")
        parla("Adesso ti sembra più chiaro?")

        # L'utente ha capito?
        capito = ascolta(nome)

        # Controlla se l'utente vuole interrompere
        if controlla_uscita(capito):
            return True
 
    parla(f"Perfetto {nome}! Iniziamo.")

    # Contatore per controllare ogni quante risposte chiedere se continuare
    contatore = 0

    # Variabile per gestire il ricordo dell'anziano
    ricordo_chiesto = False

    # Con un ciclo for, stampa una a una le canzoni dell'attività
    for canzone in canzone_cantante:

        risposta = fai_domanda_e_aspetta(
        mini,
        f"Chi è il cantante della canzone '{canzone}'?")

        # Controlla se l'utente vuole interrompere
        if controlla_uscita(risposta):
            return True

        cantante_corretto = canzone_cantante[canzone]

        # Lista delle reazioni alla risposta corretta
        risposte_corrette = [f"Esatto, ottima risposta {nome}!",
                                f"Stai andando alla grande {nome}! Hai risposto correttamente.",
                                f"Molto bene {nome}! Risposta corretta."]
        
        # Lista delle reazioni alla risposta errata
        risposte_sbagliate_cantante = [f"Non ti preoccupare {nome}, non era affatto facile. Il cantante che cercavo è {cantante_corretto[0]}, ma apprezzo il tuo tentativo!",
                                        f"Questa non era facilissima. La risposta corretta è {cantante_corretto[0]}, ma non preoccuparti, stai andando molto bene!",
                                        f"Non fa niente {nome}, la memoria a volte ci fa piccoli scherzi. La risposta corretta è {cantante_corretto[0]}."]

        # Se la risposta è corretta, stampa una frase random tra quelle della lista e Reachy chiede di condividere un ricordo alla prima canzone;
        # se non è corretta, parte l'indizio di Reachy
        if risposta in cantante_corretto:
            move = emotions.get("success1")
            mini.play_move(move)

            parla(random.choice(risposte_corrette))

            # Qui Reachy chiede se l'utente vuole condividere con lui un ricordo legato alla canzone
            if not ricordo_chiesto:
                if chiedi_ricordo(mini):
                    return True
                ricordo_chiesto = True

        # Se la risposta è sbagliata, Reachy dà un indizio
        else:
            move = emotions.get("thoughtful1")
            mini.play_move(move)

            parla(f"Ti do un piccolo indizio... {indizi_cantanti[canzone]}")
            risposta = ascolta(nome)

            # Controlla se l'utente vuole interrompere
            if controlla_uscita(risposta):
                return True

            # Se la risposta è corretta, stampa una frase random tra quelle della lista
            if risposta in cantante_corretto:
                move = emotions.get("success1")
                mini.play_move(move)

                parla(random.choice(risposte_corrette))

                # Anche dopo l'indizio, Reachy chiede di condividere un ricordo con lui se l'utente arriva alla risposta corretta
                if not ricordo_chiesto:
                    if chiedi_ricordo(mini):
                        return True
                    ricordo_chiesto = True

            # Se la risposta è errata, stampa una frase random tra quelle della lista
            else:
                move = emotions.get("helpful1")
                mini.play_move(move)
                parla(random.choice(risposte_sbagliate_cantante))

        contatore += 1

        # Ogni due domande chiede se continuare
        if contatore == 2:
            move = emotions.get("curious1")
            mini.play_move(move)
            scelta = fai_domanda_e_aspetta(
                mini,
                "Vuoi continuare con questa attività oppure cambiamo gioco? Ricordati sempre che possiamo fermarci quando vuoi.")

            # Controlla se l'utente vuole interrompere
            if controlla_uscita(scelta):
                return True

            # Se l'utente vuole cambiare attività, si ritorna al gioco parole
            elif "camb" in scelta:
                move = emotions.get("helpful2")
                mini.play_move(move)

                parla(f"Certo {nome}, cambiamo attività! Ti propongo un gioco con le parole molto divertente.")

                return gioco_parole(mini, nome)

            else:
               parla("Molto bene, allora continuiamo!")
          
            # Il contatore ritorna a 0 e riparte con l'attività
            contatore = 0

    parla("Abbiamo terminato il quiz musicale.")
    move = emotions.get("proud2")
    mini.play_move(move)

    return False

# Funzione di chiusura dell'interazione
def chiusura_interazione(mini, nome, interrotta=False):

    # I saluti differiscono se l'interazione viene interrotta dall'utente o se termina naturalmente
    if interrotta:
        saluti_interruzione = [
            f"Va bene {nome}, possiamo fermarci qui.",
            f"Nessun problema {nome}, interrompiamo l'attività.",
            f"Va benissimo {nome}, ci possiamo fermare qui.",
            f"Okay, adesso mi spengo, ma spero tu mi riaccenda presto!"]
      
        parla(random.choice(saluti_interruzione))
        parla("Ti auguro una splendida giornata. A presto!")
        move = emotions.get("loving1")
        mini.play_move(move)

    else:
        saluti_finali = [
            f"Mi sono divertito molto a trascorrere questo momento insieme a te {nome}.",
            f"Grazie per aver giocato con me {nome}. È stato davvero un piacere!",
            f"È stato bello passare un po' di tempo insieme {nome}."]

        parla(random.choice(saluti_finali))
        parla("Ti auguro una splendida giornata. A presto!")
        move = emotions.get("loving1")
        mini.play_move(move)

    # L'utente vede spegnimento in corso
    print("\n--- Spegnimento di Reachy in corso... ---")

with ReachyMini() as mini:

   # Inizio codice del progetto - programma principale
    print("\n--- INIZIO INTERAZIONE ---")

   # Il robot si attiva e inclina la testa in segno di saluto
    mini.goto_target(antennas=[0.5, 0.5], duration=0.5)

    # Chiama la funzione saluto_iniziale
    nome = saluto_iniziale()

   # Controlla se l'utente vuole interrompere
    if controlla_uscita(nome):
        chiusura_interazione(mini, "amico", True)
        exit()

    # Sceglie tra una delle domande della lista 'domande_iniziali'
    domanda = random.choice(domande_iniziali)

   # Presentazione di Reachy
    move = emotions.get("cheerful1")
    mini.play_move(move)

    stato = fai_domanda_e_aspetta(
        mini,
        f"E' un piacere conoscerti {nome}! {domanda}")

   # Controlla se l'utente vuole interrompere
    if controlla_uscita(stato):
        chiusura_interazione(mini, nome, True)
        exit()
  
   # Proposta dell'attività se l'utente risponde che sta bene
    if "bene" in stato and not "non" in stato:
        move = emotions.get("enthusiastic1")
        mini.play_move(move)

        risposta = fai_domanda_e_aspetta(
            mini,
            f"Mi fa piacere sentirlo! Ti va di fare un'attività insieme?")
       
       # Controlla se l'utente vuole interrompere
        if controlla_uscita(risposta):
            chiusura_interazione(mini, nome, True)
            exit()

   # Se l'utente risponde che oggi non sta bene 
    else:
        move = emotions.get("understanding1")
        mini.play_move(move)

        risposta = fai_domanda_e_aspetta(
        mini,
        "Mi dispiace che oggi non vada tanto bene... ti va di ravvivare un po' la giornata con un'attività da fare insieme?")

        # Controlla se l'utente vuole interrompere
        if controlla_uscita(risposta):
            chiusura_interazione(mini, nome, True)
            exit()
  
   # Se l'utente non vuole svolgere l'attività
    if "no" in risposta:
        move = emotions.get("understanding2")
        mini.play_move(move)

        # Reachy interrompe, senza insistere
        parla("Nessun problema! Capisco perfettamente... riposare è altrettanto importante. Sarà per un'altra volta, ma mi ha fatto molto piacere vederti oggi!")
        chiusura_interazione(mini, nome)
        exit()

   # Se l'utente vuole svolgere l'attività, propone una scelta tra due attività
    else:
        move = emotions.get("cheerful1")
        mini.play_move(move)

        scelta = fai_domanda_e_aspetta(
            mini,
            "Molto bene! Possiamo fare un piccolo gioco con le parole oppure un'attività legata alla musica. Quale preferisci tra i due?")
       
       # Controlla se l'utente vuole interrompere
        if controlla_uscita(scelta):
            chiusura_interazione(mini, nome, True)
            exit()

        # Da qui in poi, l'utente sceglie tra una delle due attività e vengono richiamate le funzioni dei giochi
        if  ("parole" in scelta or
             "primo" in scelta or
             "prima" in scelta):
            
            interrotta = gioco_parole(mini, nome)

        else:
            interrotta = quiz_musicale(mini, nome)

        chiusura_interazione(mini, nome, interrotta)