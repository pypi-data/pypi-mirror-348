

import pydot

def build_graph_from_yaml(data):
    graph = pydot.Dot(graph_type='digraph', rankdir='LR')

    # Crear nodos de tarea
    for task in data.get('tasks', []):
        graph.add_node(pydot.Node(task['name'], shape='box', style='filled', fillcolor='lightblue'))

    # Crear nodos de mensajes
    for msg in data.get('messages', []):
        graph.add_node(pydot.Node(msg['name'], shape='ellipse', style='filled', fillcolor='lightgreen'))

    # Crear nodos de HALs
    for hal in data.get('hal', []):
        graph.add_node(pydot.Node(hal['name'], shape='diamond', style='filled', fillcolor='lightyellow'))

    # Crear relaciones
    for task in data.get('tasks', []):
        tname = task['name']
        for pub in task.get('publishes', []):
            graph.add_edge(pydot.Edge(tname, pub, label='publishes'))
        for sub in task.get('subscribes', []):
            graph.add_edge(pydot.Edge(sub, tname, label='subscribes'))
        for use in task.get('uses', []):
            graph.add_edge(pydot.Edge(tname, use, label='uses'))

    return graph