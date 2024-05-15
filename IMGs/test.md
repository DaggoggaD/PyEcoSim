<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="">
    <img src="PyEcoSim.png" id="readme-top" alt="Logo" width="150" height="150" style="border-radius: 25px">
  </a>

  <h3 align="center">PyEcoSim</h3>

  <p align="center">
    Simulating an evolving ecosystem :fallen_leaf:
    <br />
    <a href="https://github.com/DaggoggaD/PyEcoSim"><strong>Explore the docs »</strong></a>
    <br />
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project


PyEcoSim is a simple environment simulator featuring evolving cells with up to 10 neurons each.
The objective of this application is to explore and understand natural selection by choosing only the top performers and allowing them to reproduce.

The simulation is composed of cycles, lasting 30 seconds each. The environment is filled with 20 cells and 300 food objects.

In the first generation the genome of each individual is randomized. At the end of the cycle the cells that managed to collect the most food survive and duplicate.
This process is prone to mutations, allowing small genetic modifications each time.

To allow a better grasp of the subject, the simulation variables were tweaked to show significant changes in less than 30 generations, as shown in the graph below.

Cells can also have the ability to show cannibalistic tendencies, by killing other individuals and eating their food. Depending on the food bonus granted by this practice, cannibalism can have a huge impact on the simulation.
In this project meat grants at least +30 food, as opposed to a maximum of 20 given by greens.

### Built With
The whole project is written in Python, using Pygame as the game UI.


<!-- GETTING STARTED -->
## Getting Started
### Download
* Via EXE: Download the folder `Executables` and run main.exe. <br> Currently, this does not allow modification to the simulation settings;
* Via Python: Download the repository and run `main.py`;
  (To change the simulation settings head to `GlobalVar.py` and change the desired values.
  Standard neurons connections can be changed in `CellClass.py`;)
The simulation will now be up and running.

### Prerequisites
To run this program with python, the necessary libraries are:
* json
* random
* copy
* pygame
* matplotlib
* shapely

The exe installation does not require any external packages.

<!-- USAGE EXAMPLES -->
## Usage
#### Cell informations
To inspect a cell's brain click on the cell. A graphic represantation of it's neurons and connections will be drawn on the right panel.
It's staistics will also be drawn below the brain UI.
#### 
