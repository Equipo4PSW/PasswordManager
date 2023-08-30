import curses

def buscar_en_tiempo_real(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Escribe tu búsqueda (presiona 'q' para salir):")
    stdscr.refresh()
    
    entrada = ""
    seleccionado = None
    opciones = ["manzana", "banana", "naranja", "uva", "sandía", "pera", "kiwi", "melon"]
    
    while True:
        key = stdscr.getch()

        if key == ord("q"):
            break
        elif key == 10:  # Enter key
            if seleccionado is not None and 0 <= seleccionado < len(resultados):
                break
        elif key == curses.KEY_UP:
            seleccionado = max(0, seleccionado - 1) if seleccionado is not None else 0
        elif key == curses.KEY_DOWN:
            seleccionado = min(len(resultados) - 1, seleccionado + 1) if seleccionado is not None else 0
        elif key == curses.KEY_BACKSPACE or key == 127:  # Backspace
            entrada = entrada[:-1]
            seleccionado = None
        else:
            entrada += chr(key)
            seleccionado = None

        stdscr.clear()
        stdscr.addstr(0, 0, "Escribe tu búsqueda (presiona 'q' para salir):")
        stdscr.addstr(1, 0, f"Búsqueda: {entrada}")

        resultados = [opcion for opcion in opciones if entrada.lower() in opcion.lower()]
        
        if resultados:
            stdscr.addstr(2, 0, "Resultados:")
            for i, resultado in enumerate(resultados, start=3):
                if i - 2 == seleccionado:
                    stdscr.addstr(i, 2, f"> {i - 2}. {resultado}")
                else:
                    stdscr.addstr(i, 2, f"  {i - 2}. {resultado}")
        else:
            stdscr.addstr(2, 0, "No se encontraron resultados.")

        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(buscar_en_tiempo_real)
