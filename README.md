# A-PathFinding-Visualizer-Game
This project is a visual representation of the A* pathfinding algorithm implemented using Pygame. The visualization allows users to interact with the grid to set start and end points and place obstacles, and then watch as the algorithm finds the shortest path.

Features
  Interactive Grid: Users can click to set the start and end points and create barriers on the grid.
  A Algorithm*: The project demonstrates how the A* algorithm efficiently finds the shortest path from the start point to the end point.
  Visualization: The grid and the pathfinding process are visualized in real-time, providing a clear understanding of how the algorithm   works.
Installation

Clone the repository:
  git clone https://github.com/yourusername/pathfinding-visualizer.git
  cd pathfinding-visualizer

Install Pygame:
  Ensure you have Python installed. Then install Pygame using pip:
    pip install pygame

Run the application:
  python main.py

How to Use

Left Click:
  First click sets the start point (orange).
  Second click sets the end point (turquoise).
  Subsequent clicks create barriers (black).
  
Right Click:
  Remove the start, end, or barrier by clicking on it.
  
Spacebar:
  Start the visualization of the A* algorithm.
  
Close:
  To exit the application, close the window.
  
Project Structure
  main.py: The main Python script containing the logic for the grid, nodes, and A* pathfinding algorithm.

How It Works
  Grid Creation: The grid is made up of nodes, each of which can be a start node, end node, barrier, or an empty space.

  Neighbour Calculation: Each node calculates its neighbours (up, down, left, right) unless there’s a barrier in the way.

  A Algorithm*: The algorithm uses a priority queue to explore nodes, calculating the shortest path from the start to the end by considering   the cost from the start node and the estimated cost to the end node (heuristic).

  Path Visualization: Once the algorithm finds the shortest path, it is displayed on the grid.

Dependencies
  Python 3.x
  Pygame: Used for creating the visual interface and handling user interactions.
