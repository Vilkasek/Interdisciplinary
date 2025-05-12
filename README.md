# Hydro Mazury - Water Monitoring Application

## Project Overview

Hydro Mazury is a desktop application for monitoring and analyzing water-related data in the Mazury region.

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/yourusername/hydro-mazury.git
cd hydro-mazury
```

2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python main.py
```

## Features

- View water level data
- View pollution levels
- View temperature data
- Generate PDF reports with historical and projected data

## Project Structure

- `main.py`: Main game/application loop
- `states/`: State management modules
- `utils/`: Utility classes and functions
- `assets/`: Graphics, fonts, and data files
- `reports/`: Generated PDF reports

## Data Format

The application expects a JSON file (`assets/data/hydro_data.json`) with the following structure:

```json
[
  {
    "year": 2023,
    "temperature": 16.8,
    "water_level": 2.9
  }
]
```

## Dependencies

- Pygame: Game framework
- ReportLab: PDF generation
- NumPy: Data analysis and projection

## Troubleshooting

- Ensure all dependencies are installed
- Check that the assets folder contains required graphics and fonts
- Verify the data JSON file is correctly formatted

## License

[Your License Here]

## Contributors

[Your Name or Team Names]
