import curses
from whoosh.qparser import QueryParser, FuzzyTermPlugin
from rich.console import Console
from rich.table import Table

class SearcherMenu:
    def __init__(self, index, word):
        self.index = index
        self.word = word
        self.i = 0
        self.selected = 3
        self.nResults = 0
        self.resutls = []


    def getPasswords(self, word:str):
        self.console = Console()

        with self.index.searcher() as searcher:

            # Verify if there is a word
            if word != "":
                # Setup searcher
                # TODO: Agregar mas buscadores ya que Fuzzy no es preciso ahora mismo
                queryParser = QueryParser("tags", self.index.schema)
                queryParser.add_plugin(FuzzyTermPlugin())

                # Query the word in db
                query = queryParser.parse(word)
                results = searcher.search(query)
            else:
                results =[]
                for document in searcher.documents():
                    results.append(document)

            console = Console()
            # Put passwords in a table
            table = Table('Contraseña' , 'Tags')
            for result in results:
                table.add_row(result["password"], result["tags"])

            console.print(table)


    def cyclicIndex(self, current, end, increment):
        start = 3
        end = end-1 + start
        newIndex = current + increment

        if newIndex > end:
            return start
        elif newIndex < start:
            return end
        return newIndex

    def searchAndDisplay(self, word: str):
        # Prefix to improve results
        prefix = "~3"
        with self.index.searcher() as searcher:
            # Setup searcher
            queryParser = QueryParser("tags", self.index.schema)
            queryParser.add_plugin(FuzzyTermPlugin())

            # Query the word in db
            query = queryParser.parse(word+prefix)
            results = searcher.search(query)
           
            # Poner las contraseñas en una tabla 
            table = Table('Contraseña' , 'Tags')
            for result in results:
                table.add_row(result["password"], result["tags"])
            
            # Transformar los resultados a otro tipo para hacer el retorno mas facil.
            self.resutls = []
            for result in results:
                aux = {"id": result["id"], "password": result["password"], "tags": result["tags"]}
                self.resutls.append(aux)

            # Cambiar de color la eleccion
            curses.start_color()
            curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
            curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
            
            # Descomponemos la tabla en strings
            self.i = 0

            # Ver si hay o no resultados
            self.nResults = len(results)
            if self.nResults == 0:
                self.stdscr.addstr(self.i, 0, "No hay resultados.", curses.color_pair(2))
                return

            renderLines = self.console.render_lines(table)
            for line in renderLines:
                aux = "".join(segment.text for segment in line)

                if self.selected == self.i:
                    self.stdscr.addstr(self.i, 0, aux, curses.color_pair(1))
                else:
                    self.stdscr.addstr(self.i, 0, aux, curses.color_pair(2))

                self.i += 1

    def run(self):
       
        # Handlers para el menu interactivo
        self.stdscr = curses.initscr()
        curses.curs_set(0)  # Oculta el cursor
        self.stdscr.clear()
        self.console = Console()

        self.searchAndDisplay(self.word)
        self.stdscr.addstr(self.i+1, 0, "Presiona Esc para salir")
        self.stdscr.addstr(self.i+2, 0, "Presione ('↓/↑', 'Tab/BTab', '(/)', '[/]') para navegar entre opciones")
        self.stdscr.addstr(self.i+3, 0, "Presione Enter para aceptar su busqueda.")
        self.stdscr.addstr(self.i+4, 0, f"Búsqueda: {self.word}")
        self.stdscr.refresh()

        resultIndex = -1
        while True:
            key = self.stdscr.getch()

            if key == 27:  # Tecla Esc
                break
            elif key == curses.KEY_DOWN or key == 353 or key == ord('(') or key == ord('['): # Seleccionar hacia abajo
                self.selected = self.cyclicIndex(self.selected, self.nResults, -1)
            elif key == curses.KEY_UP or key == 9 or key == ord(')') or key == ord(']'): # Seleccionar hacia arriba
                self.selected = self.cyclicIndex(self.selected, self.nResults, 1)
            elif key == curses.KEY_ENTER or key == 10:
                resultIndex = self.selected-3
                break
            elif key == -1:  # No se presionó ninguna tecla
                continue
            elif key == 127:  # Tecla Borrar
                self.word = self.word[:-1]
            else:
                self.word += chr(key)

            # Hago la busqueda segun la palabra guardada
            self.stdscr.clear()
            self.searchAndDisplay(self.word)
            self.stdscr.addstr(self.i+1, 0, "Presiona Esc para salir")
            self.stdscr.addstr(self.i+2, 0, "Presione ('↓/↑', 'Tab/BTab', '(/)', '[/]') para navegar entre opciones")
            self.stdscr.addstr(self.i+3, 0, "Presione Enter para aceptar su busqueda.")
            self.stdscr.addstr(self.i+4, 0, f"Búsqueda: {self.word}")
            self.stdscr.refresh()


        # Cierro el menu intractivo
        curses.endwin()

        if resultIndex != -1:
            with self.index.searcher() as searcher:
                return self.resutls[resultIndex]
        else:
            return []
