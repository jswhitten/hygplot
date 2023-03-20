# hygplot

hygplot is a Python-based interactive 3D star map visualization tool that uses Plotly to display the positions, colors, and names of stars in a user-friendly interface. The star data is retrieved from the HYG Database, and the stars are color-coded based on their spectral types.

## Features

- Interactive 3D star map
- Star sizes based on absolute magnitude
- Star colors based on spectral type
- Star name labels

## Installation

To install [Program Name], please follow these steps:

1. Clone the repository:

git clone [https://github.com/jswhitten/hygplot.git](https://github.com/jswhitten/hygplot.git)

2. Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate # On Windows, use "venv\Scripts\activate"

3. Install the required dependencies:

pip install -r requirements.txt

4. Run the program:

python main.py

5. Open the generated HTML file with your preferred web browser to view the 3D star map.

## Dependencies

- Python 3.7+
- Plotly
- Pandas

## Acknowledgments

- The HYG Database: [https://github.com/astronexus/HYG-Database](https://github.com/astronexus/HYG-Database)