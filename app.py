from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

def initialize_sudoku_graph():
    """Initialize the graph for Sudoku as an adjacency list."""
    vertices = 81  # 9x9 grid has 81 cells
    graph = [[] for _ in range(vertices)]

    for i in range(9):
        for j in range(9):
            index = i * 9 + j

            # Same row neighbors
            for col in range(9):
                if col != j:
                    graph[index].append(i * 9 + col)

            # Same column neighbors
            for row in range(9):
                if row != i:
                    graph[index].append(row * 9 + j)

            # Same 3x3 subgrid neighbors
            row_start = (i // 3) * 3
            col_start = (j // 3) * 3
            for row in range(row_start, row_start + 3):
                for col in range(col_start, col_start + 3):
                    if row != i or col != j:
                        graph[index].append(row * 9 + col)

    return graph

def is_safe_sudoku(graph, vertex, color, c):
    """Check if it's safe to place the number in the given cell."""
    for neighbor in graph[vertex]:
        if color[neighbor] == c:
            return False
    return True

def sudoku_coloring_util(graph, grid, color, vertex, vertices):
    """Backtracking utility to solve the Sudoku using graph coloring."""
    if vertex == vertices:  # All cells are filled
        return True

    # If the cell already has a value, move to the next cell
    if grid[vertex // 9][vertex % 9] != 0:
        return sudoku_coloring_util(graph, grid, color, vertex + 1, vertices)

    for c in range(1, 10):
        if is_safe_sudoku(graph, vertex, color, c):
            color[vertex] = c  # Assign the number

            if sudoku_coloring_util(graph, grid, color, vertex + 1, vertices):
                return True  # If it leads to a solution, return True

            color[vertex] = 0  # Backtrack

    return False  # No valid solution found

def solve_sudoku(grid):
    """Solve the Sudoku puzzle using graph coloring."""
    graph = initialize_sudoku_graph()
    vertices = 81  # Total cells
    color = [0] * vertices  # Track numbers assigned to each cell

    # Pre-fill the color array with given numbers
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                color[i * 9 + j] = grid[i][j]

    if not sudoku_coloring_util(graph, grid, color, 0, vertices):
        return None  # No solution exists

    # Return the solved grid
    return [[color[i * 9 + j] for j in range(9)] for i in range(9)]

@app.route('/solve', methods=['POST'])
def solve():
    """Handle the /solve endpoint."""
    data = request.json
    grid = data.get('grid')

    if grid and len(grid) == 9 and all(len(row) == 9 for row in grid):
        solved_grid = solve_sudoku(grid)
        if solved_grid:
            return jsonify({'solved': solved_grid}), 200
        else:
            return jsonify({'error': 'No solution exists.'}), 400

    return jsonify({'error': 'Invalid input. Must be a 9x9 grid.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
