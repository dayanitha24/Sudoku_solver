document.addEventListener('DOMContentLoaded', () => {
    const sudokuGrid = document.getElementById('sudoku-grid');

    for (let i = 0; i < 9; i++) {
        const subgrid = document.createElement('div');
        subgrid.classList.add('subgrid');

        for (let j = 0; j < 9; j++) {
            const input = document.createElement('input');
            input.type = 'number';
            input.min = 0;
            input.max = 9;
            input.placeholder = ''; 
            subgrid.appendChild(input);
        }

        sudokuGrid.appendChild(subgrid);
    }

    const solveButton = document.getElementById('solve-button');
    solveButton.addEventListener('click', async () => {
        const inputs = Array.from(sudokuGrid.querySelectorAll('input'));
        const grid = [];

        for (let i = 0; i < 9; i++) {
            const row = [];
            for (let j = 0; j < 9; j++) {
                const value = parseInt(inputs[i * 9 + j].value) || 0; 
                row.push(value);
            }
            grid.push(row);
        }
        
        try {
            const response = await fetch('http://127.0.0.1:5000/solve', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ grid })
            });

            const result = await response.json();
            displayResult(result.solved || null);
        } catch (error) {
            console.error('Error:', error);
            displayResult(null);
        }
    });
});

function displayResult(solvedGrid) {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '';

    if (solvedGrid) {
        for (let row of solvedGrid) {
            resultDiv.innerHTML += row.join(' ') + '<br>';
        }
    } else {
        resultDiv.innerHTML = 'No solution exists.';
    }
}
