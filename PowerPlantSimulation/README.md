Overview
This project simulates fluid flow through various equipment such as pumps, pipes, control valves (CVs), and fans. It computes the output properties (temperature, pressure, and flow rate) of a fluid (in this case, lube oil) as it passes through different components. The calculations are based on physical principles, such as fluid dynamics and thermodynamics, using specified material properties and equipment specifications.

Code Structure
The code is organized into classes and functions that encapsulate the properties and behaviors of the system components:

Classes
Properties

This class defines the basic properties of the fluid (temperature, pressure, and flow rate).
The __str__() method returns these properties as a dictionary for easy access.
Equipment

This class inherits from Properties and includes methods for different types of equipment:
pump: Simulates a pump's effect on the fluid, including pressure increase and temperature change.
fan: Simulates a fan's effect, primarily focusing on pressure changes.
cv: Represents a control valve's impact, calculating pressure drops and minor temperature changes.
pipe: Calculates the pressure drop, temperature change, and flow rate in a pipe, considering factors like length, diameter, roughness, and fluid properties.
Material Properties
A dictionary materials contains the properties of different fluids, including water, lube oil, and fuel gas. For each fluid, properties like density (rho), viscosity (miu), and specific heat capacity (cp) are defined.

Main Function
The main() function orchestrates the flow through the system:

Pump 1: The fluid first passes through a pump, increasing its pressure.
Pipe 1: The pressurized fluid then flows through a pipe, experiencing a pressure drop due to friction.
CV 1: The fluid then flows through a control valve, where further pressure drops occur.
Pipe 2: Finally, the fluid flows through another pipe segment.
The results from each component are printed, showing the output properties of the fluid after each stage.

Usage
To run the simulation, execute the script. The output will display the fluid properties (temperature, pressure, and flow rate) at each stage of the process. The input conditions and specifications for each equipment can be modified in the main() function and respective class methods.

Assumptions and Limitations
The code assumes steady-state flow and incompressible fluids.
The default fluid is lube oil, but other fluids can be tested by modifying the materials dictionary.
Equipment efficiencies, roughness values, and other parameters can be adjusted as needed.
Dependencies
This code uses standard Python libraries such as math for mathematical calculations. No external dependencies are required.

Future Enhancements
Adding support for compressible fluids.
Extending the range of equipment (e.g., compressors, heat exchangers).
Including more complex flow networks with multiple branches and junctions.
Adding error handling and validation for input parameters.