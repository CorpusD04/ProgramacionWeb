import { useState } from 'react'; // Importa el hook useState de React para manejar el estado

// Componente Square representa cada celda del tablero
function Square({ value, onSquareClick }) {
  return (
    <button className="square" onClick={onSquareClick}> 
      {value}
    </button>
  );
  //Botón que representa una casilla del tablero
  //
  // Muestra el valor de la casilla (X, O o vacío)
}

// Componente Board representa el tablero del juego
function Board({ xIsNext, squares, onPlay }) {
  // Maneja el clic en una casilla
  function handleClick(i) {
    if (calculateWinner(squares) || squares[i]) { // Si hay un ganador o la casilla ya está ocupada, no hacer nada
      return;
    }
    const nextSquares = squares.slice(); // Crea una copia del array de casillas
    if (xIsNext) {
      nextSquares[i] = 'X'; // Si es el turno de X, asigna 'X' a la casilla
    } else {
      nextSquares[i] = 'O'; // Si es el turno de O, asigna 'O' a la casilla
    }
    onPlay(nextSquares); // Actualiza el estado del tablero en el componente padre
  }

  const winner = calculateWinner(squares); // Calcula si hay un ganador
  let status;
  if (winner) {
    status = 'Winner: ' + winner; // Si hay un ganador, muestra quién ganó
  } else {
    status = 'Next player: ' + (xIsNext ? 'X' : 'O'); // Muestra quién juega a continuación
  }

  return (
    <>
      <div className="status">{status}</div> {/* Muestra el estado del juego */}
      <div className="board-row"> {/* Filas del tablero */}
        <Square value={squares[0]} onSquareClick={() => handleClick(0)} />
        <Square value={squares[1]} onSquareClick={() => handleClick(1)} />
        <Square value={squares[2]} onSquareClick={() => handleClick(2)} />
      </div>
      <div className="board-row">
        <Square value={squares[3]} onSquareClick={() => handleClick(3)} />
        <Square value={squares[4]} onSquareClick={() => handleClick(4)} />
        <Square value={squares[5]} onSquareClick={() => handleClick(5)} />
      </div>
      <div className="board-row">
        <Square value={squares[6]} onSquareClick={() => handleClick(6)} />
        <Square value={squares[7]} onSquareClick={() => handleClick(7)} />
        <Square value={squares[8]} onSquareClick={() => handleClick(8)} />
      </div>
    </>
  );
}

// Componente principal Game que gestiona la historia del juego y el estado global
export default function Game() {
  const [history, setHistory] = useState([Array(9).fill(null)]); // Guarda el historial de movimientos
  const [currentMove, setCurrentMove] = useState(0); // Guarda el índice del movimiento actual
  const xIsNext = currentMove % 2 === 0; // Determina si es el turno de X
  const currentSquares = history[currentMove]; // Obtiene el estado actual del tablero

  // Maneja la jugada y actualiza el historial
  function handlePlay(nextSquares) {
    const nextHistory = [...history.slice(0, currentMove + 1), nextSquares]; // Guarda solo el historial relevante
    setHistory(nextHistory);
    setCurrentMove(nextHistory.length - 1);
  }

  // Permite retroceder a un movimiento anterior
  function jumpTo(nextMove) {
    setCurrentMove(nextMove);
  }

  // Genera los botones para navegar en el historial de movimientos
  const moves = history.map((squares, move) => {
    let description;
    if (move > 0) {
      description = 'Go to move #' + move;
    } else {
      description = 'Go to game start';
    }
    return (
      <li key={move}>
        <button onClick={() => jumpTo(move)}>{description}</button>
      </li>
    );
  });

  return (
    <div className="game">
      <div className="game-board">
        <Board xIsNext={xIsNext} squares={currentSquares} onPlay={handlePlay} />
      </div>
      <div className="game-info">
        <ol>{moves}</ol> {/* Muestra la lista de movimientos */}
      </div>
    </div>
  );
}

// Función para determinar si hay un ganador
function calculateWinner(squares) {
  const lines = [
    [0, 1, 2], // Filas
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6], // Columnas
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8], // Diagonales
    [2, 4, 6],
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a]; // Devuelve el símbolo del jugador que ganó
    }
  }
  return null; // Si no hay ganador, devuelve null
}
