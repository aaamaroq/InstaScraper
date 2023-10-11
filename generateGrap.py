import json
import random
from pyvis.network import Network
import community as community_louvain
import networkx as nx

# Carga el archivo JSON
with open("relaciones.json", "r") as file:
    relaciones = json.load(file)

# Inicializa el gráfico
graph = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

# Inicializa el grafo para el algoritmo de Louvain
G = nx.Graph()

# Añade los nodos y las aristas al grafo para el algoritmo de Louvain
for clave, valores in relaciones.items():
    if clave != "adrian.mrq":
        G.add_node(clave)
        for valor in valores:
            if valor != "adrian.mrq":
                G.add_node(valor)
                G.add_edge(clave, valor)

# Encuentra las comunidades utilizando el algoritmo de Louvain
partition = community_louvain.best_partition(G)

# Función para generar un color aleatorio en formato hexadecimal
def random_color():
    r = random.randint(100, 200)
    g = random.randint(100, 200)
    b = random.randint(100, 200)
    return f"#{r:02x}{g:02x}{b:02x}"

# Asigna un color aleatorio a cada grupo
colors = {}
for group in set(partition.values()):
    colors[group] = random_color()

# Añade los nodos y las aristas al gráfico con el color correspondiente a su grupo
for clave, valores in relaciones.items():
    if clave != "adrian.mrq":
        group_color = colors[partition[clave]]
        graph.add_node(clave, color=group_color)
        if valor != "adrian.mrq":
            for valor in valores:
                graph.add_node(valor, color=colors[partition[valor]])
                graph.add_edge(clave, valor)



# Guarda el gráfico en un archivo HTML
graph.show_buttons(filter_=["physics"])  # Habilitar botones, incluido el zoom
graph_file = "relaciones.html"
graph.write_html(graph_file)