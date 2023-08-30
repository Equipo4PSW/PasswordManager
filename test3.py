from rich.console import Console
from rich.table import Table

console = Console()

table = Table()
table.add_column("Columna 1")
table.add_column("Columna 2")
table.add_row("Valor 1", "Valor 2")

    

render_lines = console.render_lines(table)
for line in render_lines:
        print("".join(segment.text for segment in line))
    # for segments in line:
    #     print(segments)
# for x in render_lines:
#     print(x)

# def getStr(list):
#     print("".join(segment.text for segment in list))
    # for ele in list:
        # print(type(ele))
        # print(ele.render())
        # print(ele)


# seg = Segment("hola", style="bold")
# print(seg)
# for ele in render_lines:
#     getStr(ele)
# getStr(render_lines[0])
# getStr(seg)

# for line in table_lines:
#     print(line)
# lines = table.__rich_console__(console=console, options=console.options)
# for x in lines:
#     print(x)

# console.print(table)
# console.print(table.__str__())
