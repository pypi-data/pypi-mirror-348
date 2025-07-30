# VASPFlow

A Python package for VASP workflow automation and band structure analysis.

## Features

- Automated VASP input file generation
- Band structure analysis and plotting
- Spin splitting calculations
- Band gap analysis
- Support for various VASP features:
  - Structure relaxation
  - Spin-orbit coupling (SOC)
  - LDA+U
  - Magnetic calculations
  - DOS calculations
  - Wannier calculations
  - vdW corrections

## Installation

```bash
pip install vaspflow
```

## Usage

### Command Line Interface

The package provides two main commands: `workflow` for preprocessing and `analyzer` for postprocessing.

#### Workflow Command (Preprocessing)

```bash
# Generate VASP input files with relaxation and SOC
vaspflow workflow --relax --soc

# Full workflow with custom parameters
vaspflow workflow --relax --soc --ldau --ispin 2 --magmom "1.0,2.0" --name "Fe2O3" --nk 50 --nsw 200
```

#### Analyzer Command (Postprocessing)

```bash
# Calculate spin splitting for band 10
vaspflow analyzer --spinsplit --spin --nband 10

# Calculate band gap for occupied band 10
vaspflow analyzer --gap 10

# Output band structure with spin polarization
vaspflow analyzer --band --spin --kseg 61
```

### Python API

```python
from vaspflow import VaspInputHandler, VaspBandAnalyzer

# Initialize VASP input handler
input_handler = VaspInputHandler()
input_handler.is_relax = True
input_handler.is_soc = True
input_handler.setup_workflow()

# Initialize band analyzer
analyzer = VaspBandAnalyzer()
analyzer.spin_polarized = True
analyzer.read_kpoints()
analyzer.read_eigenval()
analyzer.write_band_structure()
analyzer.plot_band_structure()
```

## Output Files

- `band.dat`: Band structure data
- `band.png`: Band structure plot
- `spinsplit.dat`: Spin splitting data
- `spinsplit.png`: Spin splitting plot
- `gap.dat`: Band gap data

## Dependencies

- Python >= 3.6
- numpy
- matplotlib

## Documentation

For detailed documentation, please visit [documentation link].

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Dinghui Wang 