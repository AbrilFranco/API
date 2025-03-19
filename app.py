from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from queue import Queue


app = Flask(__name__)
CORS(app)

# Ruta para cargar el archivo index.html
@app.route('/')
def index():
    return render_template('index.html')

# BFS normal
def bfs(estado_inicial, estado_final):
    queue = Queue()
    queue.put([estado_inicial])
    visited = set()

    while not queue.empty():
        path = queue.get()
        state = path[-1]

        if state == estado_final:
            return path

        if tuple(state) not in visited:
            visited.add(tuple(state))

            for i in range(len(state) - 1):
                new_state = state[:]
                new_state[i], new_state[i + 1] = new_state[i + 1], new_state[i]
                queue.put(path + [new_state])

    return None

# BFS recursivo
def bfs_recursivo(queue, estado_final, visited):
    if queue.empty():
        return None
    
    path = queue.get()
    state = path[-1]

    if state == estado_final:
        return path

    if tuple(state) not in visited:
        visited.add(tuple(state))

        for i in range(len(state) - 1):
            new_state = state[:]
            new_state[i], new_state[i + 1] = new_state[i + 1], new_state[i]
            queue.put(path + [new_state])

    return bfs_recursivo(queue, estado_final, visited)

def resolver_bfs_recursivo(estado_inicial, estado_final):
    queue = Queue()
    queue.put([estado_inicial])
    visited = set()
    return bfs_recursivo(queue, estado_final, visited)

# DFS
def dfs(estado_inicial, estado_final, path=None, visited=None):
    if path is None:
        path = [estado_inicial]
    if visited is None:
        visited = set()

    state = path[-1]
    if state == estado_final:
        return path

    visited.add(tuple(state))

    for i in range(len(state) - 1):
        new_state = state[:]
        new_state[i], new_state[i + 1] = new_state[i + 1], new_state[i]

        if tuple(new_state) not in visited:
            new_path = dfs(estado_inicial, estado_final, path + [new_state], visited)
            if new_path:
                return new_path

    return None

@app.route('/resolver_puzzle', methods=['POST'])
def resolver_puzzle():
    data = request.get_json()
    estado_inicial = list(map(int, data.get("estado_inicial", [])))
    estado_final = list(map(int, data.get("estado_final", [])))

    resultado = {
        "bfs": bfs(estado_inicial, estado_final),
        "bfs_recursivo": resolver_bfs_recursivo(estado_inicial, estado_final),
        "dfs": dfs(estado_inicial, estado_final)
    }
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)




