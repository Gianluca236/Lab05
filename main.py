import flet as ft

import automobile
from alert import AlertManager
from autonoleggio import Autonoleggio

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)

    in_marca = ft.TextField( label="Marca"  )
    in_modello = ft.TextField(label="Modello")
    in_anno = ft.TextField( label="Anno")

    count= ft.Text('0')
    count.value=0

    def incrementa(e):
        count.value = str(int(count.value) + 1)
        page.update()

    def decrementa(e):
        if count.value > '0':
            count.value = str(int(count.value) - 1)
            page.update()

    riga= ft.Row([in_marca, in_modello, in_anno , ft.IconButton(ft.Icons.REMOVE, on_click=decrementa , icon_color='red'),
                  count, ft.IconButton(ft.Icons.ADD, on_click=incrementa , icon_color='green')])


    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()


    def clicked_button(e):


        if in_anno.value.isalpha():
            alert.show_alert('Inserire valore numerico per anno')

        elif in_marca.value == "" :
            alert.show_alert('Inserire almeno un valore per marca')

        elif in_modello.value == "":
            alert.show_alert('Inserire almeno un valore per modello')

        elif in_anno.value == "":
            alert.show_alert('Inserire almeno un valore per anno')



        else:

            autonoleggio.aggiungi_automobile(str(in_marca.value), str(in_modello.value),
                                             in_anno.value, int(count.value))
            aggiorna_lista_auto()

            in_marca.value = ""
            in_modello.value = ""
            in_anno.value = ""

            page.update()


    btn = ft.ElevatedButton("Aggiungi auto", on_click=clicked_button)

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)



    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3

        ft.Text("Aggiungi automobile", size=20),
        riga,
        btn,

        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
