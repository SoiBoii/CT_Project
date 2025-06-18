# Pygame Simulations

This repository contains three Pygame-based simulations:

1.  **Cloth Simulator**: A physics-based simulation demonstrating cloth dynamics with gravity, wind, and tearing.
2.  **Conway's Game of Life**: An implementation of the classic cellular automaton with various preset patterns.
3.  **Simulation Selector**: A simple launcher to choose between the two simulations.

-----

## Features

### Cloth Simulator

  * **Realistic Physics**: Simulates gravity and damping for natural cloth movement.
  * **Interactive Control**: Drag cloth points with the mouse.
  * **Pinning**: Pin points to the screen by right-clicking.
  * **Wind Effects**: Toggle wind to see the cloth sway.
  * **Tearing**: The cloth can tear if stretched beyond a certain limit.
  * **Resettable**: Reset the cloth to its initial state.

### Conway's Game of Life

  * **Classic Rules**: Implements Conway's original rules for cellular automation.
  * **Interactive Grid**: Click to toggle cells between live and dead states.
  * **Simulation Control**: Start, stop, and reset the simulation.
  * **Adjustable Framerate**: Cycle through different simulation speeds.
  * **Preset Patterns**: Easily place famous Game of Life patterns like:
      * Glider
      * Blinker
      * Gosper Glider Gun
      * Toad
      * Beacon
      * Pulsar
      * Lightweight Spaceship (LWSS)
      * AND Gate
      * OR Gate
      * NOT Gate
  * **Fullscreen Mode**: Toggle fullscreen for an immersive experience.

### Simulation Selector

  * **User-Friendly Interface**: Simple buttons to launch either simulation.

-----

## Getting Started

### Prerequisites

Make sure you have Python installed on your system. This project was developed with Python 3.x.

You'll also need the `pygame` and `numpy` libraries.

### Installation

1.  **Save the files**:
    Save the first code block as `cloth_simulator.py`.
    Save the second code block as `game_of_life.py`.
    Save the third code block as `main.py`.

2.  **Install dependencies**:
    Open your terminal or command prompt and run the following command:

    ```bash
    pip install pygame numpy
    ```

### Running the Simulations

To start the application, navigate to the directory where you saved the files in your terminal or command prompt and run:

```bash
python main.py
```

This will launch the **Simulation Selector**, from which you can choose which simulation to run.

-----

## How to Play

### Cloth Simulator

Once the Cloth Simulator window appears:

  * **Drag Points**: Click and drag any point on the cloth with the **left mouse button** to move it.
  * **Pin/Unpin Points**: **Right-click** on a point to toggle its pinned state (red points are pinned). Pinned points remain fixed.
  * **Pause/Resume**: Press the **SPACEBAR** to pause or resume the simulation.
  * **Reset Cloth**: Press **R** to reset the cloth to its initial configuration.
  * **Toggle Wind**: Press **W** to turn wind effects on or off.
  * **Toggle Gravity**: Press **G** to turn gravity on or off.

### Conway's Game of Life

Once the Game of Life window appears:

  * **Toggle Cells**: Click on any cell in the grid to toggle its state (alive or dead).
  * **Start/Stop Simulation**: Click the **"Start/Stop"** button at the top to begin or pause the simulation.
  * **Reset Grid**: Click the **"Reset"** button to clear the grid.
  * **Change Framerate**: Click the **"Framerate"** button to cycle through different simulation speeds (1, 5, 10, 15, 30 FPS). The current FPS will be displayed on the button.
  * **Place Presets**: Click on any of the **preset buttons** (e.g., "Glider", "Gosper Gun") and then click on the grid where you want to place the pattern.
  * **Toggle Fullscreen**: Press **F** to switch between windowed and fullscreen modes.

-----

## Project Structure

```
.
├── main.py        # Launches the simulation selector
├── cloth_simulator.py      # Implements the cloth simulation
└── game_of_life.py         # Implements Conway's Game of Life
```

-----

## License

This project is open-source and available for use and modification.
