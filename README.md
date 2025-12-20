# Single-Phase Transformer Calculator

A comprehensive PyQt6 desktop application for analyzing single-phase transformer characteristics, including impedance calculations, voltage regulation, and efficiency analysis.

## Features

- **Input Page**: Enter transformer ratings, open-circuit test data, and short-circuit test data
- **Impedances Page**: View calculated impedance parameters referred to both primary and secondary sides
- **Voltage Regulation Page**: Analyze voltage regulation at different power factors (unity, 0.8 lagging, 0.8 leading)
- **Efficiency Page**: Calculate transformer efficiency, copper losses, and core losses
- **Info Page**: Course and project information

## Requirements

- Python 3.8 or higher
- PyQt6
- Virtual environment (recommended)

## Installation

### Quick Start (Windows)

#### Option 1: Double-click to Run (Easiest)

1. Install dependencies once:
```powershell
python -m venv .venv
.\.venv\Scripts\pip.exe install -r requirements.txt
```

2. Double-click `run_transformer_calculator.bat` to launch the application

#### Option 2: Manual Setup

1. Create the virtual environment (only once):
```powershell
python -m venv .venv
```

2. Activate the environment:
```powershell
.\.venv\Scripts\Activate.ps1
```

If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

3. Install dependencies and run:
```powershell
pip install -r requirements.txt
python main.py
```

### Alternative (Command Prompt)

```cmd
.venv\Scripts\activate.bat
pip install -r requirements.txt
python main.py
```

### Run without activating

You can call the virtual environment's Python directly:
```powershell
.\.venv\Scripts\pip.exe install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

## Usage

1. Launch the application using any of the methods above
2. Navigate to the **Input** tab
3. Enter the transformer specifications:
   - Power Rating (VA)
   - Primary and Secondary Voltages (V)
   - Open Circuit Test data (Voc, Ioc, Poc)
   - Short Circuit Test data (Vsc, Isc, Psc)
4. Click **Calculate** to compute all parameters
5. View results in the respective tabs:
   - **Impedances**: Series and shunt impedance parameters
   - **Voltage Regulation**: Voltage drop analysis at various power factors
   - **Efficiency**: Power losses and efficiency calculations

## Technical Details

### Calculations Performed

- **Turns ratio** (a = V1/V2)
- **Equivalent impedance** (Zeq, Req, Xeq) referred to primary and secondary
- **Excitation parameters** (Yφ, Gφ, Bφ, Rc, Xm)
- **Voltage regulation** at unity PF, 0.8 lagging PF, and 0.8 leading PF
- **Transformer losses** (copper loss, core loss)
- **Efficiency** at rated load

### Images Required

The application expects the following images in the root directory:
- `img1.jpeg` - Input page transformer diagram
- `img2.jpeg` - Primary-side equivalent circuit
- `img3.jpeg` - Secondary-side equivalent circuit
- `img4.jpeg` - Voltage regulation phasor diagram
- `img5.jpeg` - Efficiency and losses diagram

## Project Information

**Course**: EEE-3003 - Electromechanical Energy Conversion

**Group Members**:
- 220702705 - Ahmed Mahmoud Elsayed Hussein
- 220702084 - Gökdeniz Günde

**Lecturers**:
- Doç. Dr. Akın Taşcıkaraoğlu
- Arş. Gör. Ali Can Erüst

## Troubleshooting

- **Execution policy error**: Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- **Missing virtual environment**: Recreate with `python -m venv .venv`
- **GUI doesn't appear**: Run `python main.py` from terminal and check for error messages
- **Image not found warnings**: Ensure all required image files (img1-5.jpeg) are in the root directory

## License

Educational project for course EEE-3003.