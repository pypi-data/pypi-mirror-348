#!/usr/bin/env python3
import argparse
import numpy as np
import os
import subprocess
from typing import List, Tuple, Optional, Dict, Any
import shutil
from pathlib import Path
import warnings
import matplotlib.pyplot as plt

class VaspInputHandler:
    def __init__(self):
        # Default values
        self.name = "default"
        self.isif = 3
        self.is_constrained = False
        self.dim = 3
        self.is_relax = False
        self.is_ldau = False
        self.is_magnetic = False
        self.is_soc = True
        self.is_hse = False
        self.is_wannier = False
        self.is_dos = False
        self.is_vdw = False
        self.is_summary = True
        self.is_band = True
        self.max_l = 2
        self.is_pbesol = False
        self.ismear = -5
        self.ispin = 1
        self.is_kpt_manual = False
        self.nk = 40
        self.nsw = 100
        
        # Job parameters
        self.queue = "default"
        self.cores = 40
        self.modules = "oneapi/2023.2.0 vasp/cstr_rlx wanniertools/2.4.1 wannier90/1.2"
        
        # System parameters
        self.n_atoms = 0
        self.n_types = 0
        self.enmax = 0.0
        self.ecut = 0
        
        # Magnetic parameters
        self.saxis = np.array([0,0,1], dtype=int)
        self.magmom = []
        self.soc_magmom = []
        
        # LDA+U parameters
        self.ldau_l = []
        self.ldau_u = []
        
        # Task list
        self.task_list = ["stdscf", "stdband"]
        
    def read_poscar(self) -> None:
        """Read POSCAR file and extract system information"""
        if not os.path.exists("POSCAR"):
            raise FileNotFoundError("POSCAR file not found!")
            
        with open("POSCAR", 'r') as f:
            # Skip first 5 lines
            for _ in range(5):
                f.readline()
            
            # Read atom types
            atom_types = f.readline().split()
            self.n_types = len(atom_types)
            
            # Read number of atoms
            atom_counts = [int(x) for x in f.readline().split()]
            self.n_atoms = sum(atom_counts)
            
    def create_potcar(self) -> None:
        """Create POTCAR file from atomic species in POSCAR"""
        if os.path.exists("POTCAR"):
            print("POTCAR file already exists.")
            return
            
        with open("POSCAR", 'r') as f:
            # Skip first 5 lines
            for _ in range(5):
                f.readline()
            atom_types = f.readline().split()
            
        # Create POTCAR
        with open("POTCAR", 'w') as outfile:
            for atom in atom_types:
                potcar_path = f"/home/hongchang/software/potpaw/pbe/{atom}/POTCAR"
                if os.path.exists(potcar_path):
                    with open(potcar_path, 'r') as infile:
                        outfile.write(infile.read())
                else:
                    raise FileNotFoundError(f"POTCAR for {atom} not found at {potcar_path}")
                    
        # Get ENMAX and calculate ENCUT
        with open("POTCAR", 'r') as f:
            for line in f:
                if "ENMAX" in line:
                    enmax = float(line.split()[2].split(';')[0])
                    self.enmax = max(self.enmax, enmax)
                    
        self.ecut = int((1.5 * self.enmax) / 10.0 + 1) * 10
        
    def create_incar(self, task_name: str) -> None:
        """Create INCAR file for a specific task"""
        incar_path = os.path.join(task_name, "INCAR")
        os.makedirs(os.path.dirname(incar_path), exist_ok=True)
        
        with open(incar_path, 'w') as f:
            # Common parameters
            f.write(f"SYSTEM = {self.name}\n")
            f.write("ISTART = 0\n")
            f.write("ICHARG = 2\n")
            f.write(f"ENCUT = {self.ecut}\n")
            f.write("PREC = High\n")
            f.write("LWAVE = .FALSE.\n")
            f.write("LCHARG = .TRUE.\n")
            f.write("ADDGRID = .TRUE.\n")
            f.write(f"ISMEAR = {self.ismear}\n")
            f.write("SIGMA = 0.02\n")
            f.write("NELM = 200\n")
            f.write("EDIFF = 1E-7\n")
            f.write("NCORE = 4\n")
            
            # Task-specific parameters
            if task_name == "relax":
                f.write(f"NSW = {self.nsw}\n")
                f.write("IBRION = 1\n")
                f.write(f"ISIF = {self.isif}\n")
                f.write("EDIFFG = -0.002\n")
                if self.is_constrained:
                    f.write("110\n110\n000\n")
                if self.is_pbesol:
                    f.write("GGA = PS\n")
                    
            elif task_name in ["socscf", "socband"]:
                f.write("LSORBIT = .TRUE.\n")
                f.write("LORBIT = 11\n")
                
            # Add magnetic parameters if needed
            if self.is_magnetic:
                f.write(f"ISPIN = {self.ispin}\n")
                f.write(f"SAXIS = {self.saxis[0]:.3f} {self.saxis[1]:.3f} {self.saxis[2]:.3f}\n")
                if self.magmom:
                    f.write(f"MAGMOM = {' '.join(map(str, self.magmom))}\n")
                f.write("GGA_COMPAT = .FALSE.\n")
                
            # Add LDA+U parameters if needed
            if self.is_ldau:
                f.write("LDAU = .TRUE.\n")
                f.write("LDATYPE = 2\n")
                f.write(f"LDAUL = {' '.join(map(str, self.ldau_l))}\n")
                f.write(f"LDAUU = {' '.join(map(str, self.ldau_u))}\n")
                f.write(f"LMAXMIX = {6 if self.max_l > 2 else 4}\n")
                
            # Add vdW parameters if needed
            if self.is_vdw:
                f.write(f"IVDW = {self.ivdw}\n")
                
    def create_kpoints(self, task_name: str) -> None:
        """Create KPOINTS file for a specific task"""
        kpoints_path = os.path.join(task_name, "KPOINTS")
        
        if self.is_kpt_manual:
            with open(kpoints_path, 'w') as f:
                f.write("KPT\n")
                f.write("0\n")
                f.write("Gamma\n")
                f.write(f"{self.kpt_list}\n")
                f.write("0.0 0.0 0.0\n")
        else:
            # Use vaspkit to generate KPOINTS
            if task_name in ["stdband", "socband"]:
                subprocess.run(f"echo -e '30{self.dim}' | vaspkit", shell=True)
                os.rename("KPATH.in", kpoints_path)
                with open(kpoints_path, 'r') as f:
                    content = f.read()
                with open(kpoints_path, 'w') as f:
                    f.write(content.replace("20", str(self.nk)))
            else:
                subprocess.run("echo -e '102\n 2\n 0.04' | vaspkit", shell=True)
                os.rename("KPOINTS", kpoints_path)
                
    def create_job_script(self) -> None:
        """Create job submission script"""
        with open("job", 'w') as f:
            f.write(f"#BSUB -q {self.queue}\n")
            f.write(f"#BSUB -n {self.cores}\n")
            f.write(f"#BSUB -J {self.name}\n")
            f.write("#BSUB -e err\n")
            f.write("#BSUB -o out\n\n")
            f.write(f"module load {self.modules}\n")
            
            # Add task-specific commands
            if self.is_relax:
                f.write("cd ./relax\n")
                f.write("mpirun vasp_std > log\n")
                if self.is_soc:
                    f.write("\nfor i in stdscf stdband socscf socband\ndo\n\tcp CONTCAR ../$i/POSCAR\ndone\n")
                else:
                    f.write("\nfor i in stdscf stdband\ndo\n\tcp CONTCAR ../$i/POSCAR\ndone\n")
                f.write("cd ../stdscf\n")
            else:
                f.write("cd ./stdscf\n")
                
            f.write("mpirun vasp_std > log\n")
            
            if self.is_soc:
                f.write("cp CHGCAR ../socscf\n\n")
                f.write("cd ../socscf\n")
                f.write("mpirun vasp_ncl > log\n")
                
            if self.is_band:
                f.write("cp CHGCAR ../stdband\n\n")
                f.write("cd ../stdband\n")
                f.write("mpirun vasp_std > log\n")
                
            if self.is_band and self.is_soc:
                f.write("cp CHGCAR ../socband\n\n")
                f.write("cd ../socband\n")
                f.write("mpirun vasp_ncl > log\n")
                
    def setup_workflow(self) -> None:
        """Set up the complete VASP workflow"""
        # Check if directories already exist
        if any(os.path.exists(d) for d in self.task_list):
            warnings.warn("Some task directories already exist. Files will be overwritten.")
            
        # Read POSCAR and create POTCAR
        self.read_poscar()
        self.create_potcar()
        
        # Update task list based on options
        if self.is_relax:
            self.task_list.append("relax")
        if self.is_soc:
            self.task_list.extend(["socscf", "socband"])
        if self.is_dos:
            self.task_list.append("dos")
        if self.is_dos and self.is_soc:
            self.task_list.append("socdos")
        if self.is_wannier and self.is_soc:
            self.task_list.append("wan")
            
        # Create directories and input files
        for task in self.task_list:
            os.makedirs(task, exist_ok=True)
            shutil.copy("POSCAR", os.path.join(task, "POSCAR"))
            shutil.copy("POTCAR", os.path.join(task, "POTCAR"))
            self.create_incar(task)
            self.create_kpoints(task)
            
        # Create job script
        self.create_job_script()
        
        # Print summary if requested
        if self.is_summary:
            self.print_summary()
            
    def print_summary(self) -> None:
        """Print summary of the setup"""
        print("=================== Summary ===================")
        print(f"Created directories: {', '.join(self.task_list)}")
        print(f"Loaded modules: {self.modules}")
        print("\nPOTCAR elements:")
        with open("POTCAR", 'r') as f:
            for line in f:
                if line.startswith('TIT'):
                    print(line.strip())
        
        if self.is_vdw:
            print(f"\nIVDW = {self.ivdw}")
            
        if self.is_ldau:
            print("\nLDA+U parameters:")
            print("LDAU = .TRUE.")
            print("LDATYPE = 2")
            print(f"LDAUL = {' '.join(map(str, self.ldau_l))}")
            print(f"LDAUU = {' '.join(map(str, self.ldau_u))}")
            print(f"LMAXMIX = {6 if self.max_l > 2 else 4}")
            
        if self.is_magnetic:
            print("\nMagnetic parameters:")
            print(f"ISPIN = {self.ispin}")
            print(f"SAXIS = {self.saxis}")
            print(f"MAGMOM = {self.magmom}")
            print("GGA_COMPAT = .FALSE.")
            
        print("\n================== Warning ===================")
        print("This script only generates VASP input files!")
        print("Please carefully check all input files before running!")
        print("=============================================")

class VaspBandAnalyzer:
    def __init__(self):
        self.ef = 0.0
        self.nk = 0
        self.nb = 0
        self.b1 = np.zeros(3)
        self.b2 = np.zeros(3)
        self.b3 = np.zeros(3)
        self.kpoints = []
        self.eigenvalues_up = []
        self.eigenvalues_dn = []
        self.spin_polarized = False
        self.fermi_energy = None
        self.kseg=-1
        self.band = False
        self.ss = False

    def read_kpoints(self) -> None:
        """Read KPOINTS file and extract k-points information"""
        # Read k-points from KPOINTS file
        kpoints = []
        with open("KPOINTS", 'r') as f:
            # Skip first 4 lines
            f.readline()
            kseg = int(f.readline().split()[0])
            if self.band:
                if self.kseg == -1:
                    self.kseg = kseg
                for _ in range(2):
                    f.readline()
            elif self.ss:
                if self.kseg==-1:
                    self.kseg = int(np.sqrt(kseg))
                f.readline()
            
            # Read k-points
            for line in f:
                if line.strip():  # Skip empty lines
                    try:
                        k1, k2, k3 = map(float, line.split()[:3])
                        kpoints.append([k1, k2, k3])
                    except (ValueError, IndexError):
                        continue
        
        self.kpoints = np.array(kpoints)
        self.nk = len(kpoints)
        
        # Read reciprocal lattice vectors from OUTCAR
        reci_vectors = []
        with open("OUTCAR", 'r') as f:
            found_reci = False
            count = 0
            for line in f:
                if 'reciprocal lattice vectors' in line:
                    found_reci = True
                    continue
                if found_reci:
                    if count < 3:
                        try:
                            # Extract the last three numbers from the line
                            values = line.split()
                            if len(values) >= 3:
                                b1, b2, b3 = map(float, values[-3:])
                                reci_vectors.append([b1, b2, b3])
                                count += 1
                        except (ValueError, IndexError):
                            continue
                    else:
                        break
        
        if len(reci_vectors) == 3:
            self.b1 = np.array(reci_vectors[0]) * 2 * np.pi
            self.b2 = np.array(reci_vectors[1]) * 2 * np.pi
            self.b3 = np.array(reci_vectors[2]) * 2 * np.pi
        else:
            raise ValueError("Could not find reciprocal lattice vectors in OUTCAR")

    def read_eigenval(self) -> None:
        """Read EIGENVAL file and extract eigenvalues"""
        if not self.fermi_energy:
            # Get Fermi energy from OUTCAR
            with open("OUTCAR", 'r') as f:
                for line in f:
                    if "E-fermi" in line:
                        self.ef = float(line.split()[2])
                        break
        else:
            self.ef = self.fermi_energy

        with open("EIGENVAL", 'r') as f:
            # Skip header
            for _ in range(5):
                f.readline()
            
            # Read number of electrons, k-points and bands
            line = f.readline().split()
            self.nk = int(line[1])
            self.nb = int(line[2])
            f.readline()  # Skip empty line

            # Initialize arrays
            self.kpoints = np.zeros((self.nk, 3))
            self.eigenvalues_up = np.zeros((self.nk, self.nb))
            if self.spin_polarized:
                self.eigenvalues_dn = np.zeros((self.nk, self.nb))

            # Read eigenvalues
            for ik in range(self.nk):
                line = f.readline().split()
                self.kpoints[ik] = [float(x) for x in line[:3]]
                
                for ib in range(self.nb):
                    line = f.readline().split()
                    if self.spin_polarized:
                        self.eigenvalues_up[ik, ib] = float(line[1])
                        self.eigenvalues_dn[ik, ib] = float(line[2])
                    else:
                        self.eigenvalues_up[ik, ib] = float(line[1])
                
                if ik < self.nk - 1:
                    f.readline()  # Skip empty line

    def calculate_spin_splitting(self) -> np.ndarray:
        """Calculate spin splitting for each band at each k-point"""
        if not self.spin_polarized:
            raise ValueError("Spin splitting calculation requires spin-polarized calculation")
        return self.eigenvalues_up - self.eigenvalues_dn

    def calculate_band_gap(self, nocc: int) -> Tuple[float, np.ndarray]:
        """Calculate band gap for occupied band nocc"""
        gap = self.eigenvalues_up[:, nocc] - self.eigenvalues_up[:, nocc-1]
        return np.min(gap), gap

    def direct_to_cartesian(self, k_direct: np.ndarray) -> np.ndarray:
        """Convert direct coordinates to Cartesian coordinates"""
        return (k_direct[0] * self.b1 + 
                k_direct[1] * self.b2 + 
                k_direct[2] * self.b3)

    def write_spin_splitting(self, output_file: str = "spinsplit.dat", 
                           selected_band: Optional[int] = None,
                           kseg: Optional[int] = None) -> None:
        """Write spin splitting data to file"""
        if not self.spin_polarized:
            raise ValueError("Spin splitting calculation requires spin-polarized calculation")

        spinsplit = self.calculate_spin_splitting()
        maxspinsplit = np.max(np.abs(spinsplit))
        
        
        with open(output_file, 'w') as f:
            f.write("#k1 k2 k3 kx ky kz nb ss(eV) abs(ss)\n")
            krange=-1
            print(self.kseg)
            if kseg is not None:
                kseg_it = kseg
            else:
                kseg_it = self.kseg
            for ik in range(self.nk):
                k_cart = self.direct_to_cartesian(self.kpoints[ik])
                krange_temp = np.max(np.abs(k_cart))
                krange =  krange_temp if krange_temp > krange else krange
                if selected_band is not None:
                    if 0 < selected_band <= self.nb:
                        f.write(f"{self.kpoints[ik][0]:8.4f} {self.kpoints[ik][1]:8.4f} "
                               f"{self.kpoints[ik][2]:8.4f} {k_cart[0]:8.4f} {k_cart[1]:8.4f} "
                               f"{k_cart[2]:8.4f} {selected_band:4d} "
                               f"{spinsplit[ik,selected_band-1]:10.6f} "
                               f"{abs(spinsplit[ik,selected_band-1]):10.6f}\n")
                else:
                    for ib in range(self.nb):
                        f.write(f"{self.kpoints[ik][0]:8.4f} {self.kpoints[ik][1]:8.4f} "
                               f"{self.kpoints[ik][2]:8.4f} {k_cart[0]:8.4f} {k_cart[1]:8.4f} "
                               f"{k_cart[2]:8.4f} {ib+1:4d} "
                               f"{spinsplit[ik,ib]:10.6f} {abs(spinsplit[ik,ib]):10.6f}\n")
                
                if kseg_it and (ik + 1) % kseg_it == 0:
                    f.write("\n")
        with open("spinsplit.gnu", "w") as f:
            f.write(f"""set encoding iso_8859_1
set terminal  png truecolor enhanced font ", 60" size 1920, 1680
set output 'spinsplit.png'
set palette defined (-{maxspinsplit} "#194eff", 0 "white", {maxspinsplit} "red" )
set style data linespoints
set size 0.8, 1
set origin 0.1, 0
unset ztics
unset key
set pointsize 0.8
set pm3d
set view map
set border lw 3
set xlabel "kx"
set ylabel "ky"
#set xrange [ -{krange} : {krange} ]
#set yrange [ -{krange} : {krange} ]
set pm3d interpolate 4,4
set title "spinsplit"
splot 'spinsplit.dat' u 4:5:8 w pm3d
""")

    def write_band_gap(self, nocc: int, output_file: str = "gap.dat") -> None:
        """Write band gap data to file"""
        min_gap, gaps = self.calculate_band_gap(nocc)
        
        with open(output_file, 'w') as f:
            f.write("#k1 k2 k3 kx ky kz gap(eV)\n")
            for ik in range(self.nk):
                k_cart = self.direct_to_cartesian(self.kpoints[ik])
                f.write(f"{self.kpoints[ik][0]:8.4f} {self.kpoints[ik][1]:8.4f} "
                       f"{self.kpoints[ik][2]:8.4f} {k_cart[0]:8.4f} {k_cart[1]:8.4f} "
                       f"{k_cart[2]:8.4f} {gaps[ik]:10.6f}\n")
                
    def write_band_structure(self, output_file: str = "band.dat") -> None:
        """Write band structure data to file"""
        # Calculate k-point distances
        k_distances = np.zeros(self.nk)
        for ik in range(1, self.nk):
            k_cart_prev = self.direct_to_cartesian(self.kpoints[ik-1])
            k_cart_curr = self.direct_to_cartesian(self.kpoints[ik])
            k_distances[ik] = k_distances[ik-1] + np.linalg.norm(k_cart_curr - k_cart_prev)
        
        with open(output_file, 'w') as f:
            f.write("#k-distance k1 k2 k3 kx ky kz nb energy(eV)\n")
            
            if self.spin_polarized:
                # Write spin-up bands
                for ib in range(self.nb):
                    for ik in range(self.nk):
                        f.write(f"{k_distances[ik]:10.6f} {self.eigenvalues_up[ik,ib]-self.ef:10.6f}\n")
                    f.write("\n")  # Add empty line between bands
                
                # Write spin-down bands
                for ib in range(self.nb):
                    for ik in range(self.nk):
                        f.write(f"{k_distances[ik]:10.6f} {self.eigenvalues_dn[ik,ib]-self.ef:10.6f}\n")
                    f.write("\n")  # Add empty line between bands
            else:
                # Write non-spin-polarized bands
                for ib in range(self.nb):
                    for ik in range(self.nk):
                        f.write(f"{k_distances[ik]:10.6f} {self.eigenvalues_up[ik,ib]-self.ef:10.6f}\n")
                    f.write("\n")  # Add empty line between bands
            
            # Write high-symmetry points information
            if self.kseg > 0:
                f.write("\n# High-symmetry points:\n")
                for i in range(0, self.nk, self.kseg):
                    if i < self.nk:
                        f.write(f"# {i//self.kseg + 1}: {k_distances[i]:10.6f}\n")

    def plot_band_structure(self, output_file: str = "band.png") -> None:
        """Plot band structure"""
        # Calculate k-point distances
        k_distances = np.zeros(self.nk)
        for ik in range(1, self.nk):
            k_cart_prev = self.direct_to_cartesian(self.kpoints[ik-1])
            k_cart_curr = self.direct_to_cartesian(self.kpoints[ik])
            k_distances[ik] = k_distances[ik-1] + np.linalg.norm(k_cart_curr - k_cart_prev)
        
        # Create figure
        plt.figure(figsize=(10, 8))
        
        if self.spin_polarized:
            # Plot spin-up bands
            for ib in range(self.nb):
                plt.plot(k_distances, self.eigenvalues_up[:, ib] - self.ef, 'b-', linewidth=1)
            # Plot spin-down bands
            for ib in range(self.nb):
                plt.plot(k_distances, self.eigenvalues_dn[:, ib] - self.ef, 'r-', linewidth=1)
        else:
            # Plot non-spin-polarized bands
            for ib in range(self.nb):
                plt.plot(k_distances, self.eigenvalues_up[:, ib] - self.ef, 'k-', linewidth=1)
        
        # Add high-symmetry points
        if self.kseg > 0:
            for i in range(0, self.nk, self.kseg):
                if i < self.nk:
                    plt.axvline(x=k_distances[i], color='gray', linestyle='--', alpha=0.5)
        
        # Set labels and title
        plt.xlabel('Wave Vector')
        plt.ylabel('Energy (eV)')
        plt.title('Band Structure')
        
        # Add horizontal line at Fermi level
        plt.axhline(y=0, color='k', linestyle='--', alpha=0.5)
        
        # Set y-axis limits
        ymin = min(np.min(self.eigenvalues_up - self.ef), 
                  np.min(self.eigenvalues_dn - self.ef) if self.spin_polarized else np.inf)
        ymax = max(np.max(self.eigenvalues_up - self.ef),
                  np.max(self.eigenvalues_dn - self.ef) if self.spin_polarized else -np.inf)
        plt.ylim(ymin - 0.5, ymax + 0.5)
        
        # Save figure
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()

def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description='VASP Workflow Automation and Band Structure Analysis Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate VASP input files with relaxation and SOC
  vaspflow workflow --relax --soc

  # Calculate spin splitting for band 10
  vaspflow analyzer --spinsplit --spin --nb 10

  # Calculate band gap for occupied band 10
  vaspflow analyzer --gap 10

  # Output band structure with spin polarization
  vaspflow analyzer --band --spin

  # Full workflow with custom parameters
  vaspflow workflow --relax --soc --ldau --ispin 2 --magmom "1.0,2.0" --name "Fe2O3" --nk 50 --nsw 200
"""
    )

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Workflow subparser
    workflow_parser = subparsers.add_parser('workflow', help='Generate VASP input files')
    workflow_group = workflow_parser.add_argument_group('Workflow Options')
    workflow_group.add_argument('--relax', "-r", action='store_true',
                              help='Include structure relaxation')
    workflow_group.add_argument('--soc', action='store_true',
                              help='Include SOC calculations')
    workflow_group.add_argument('--ldau', action='store_true',
                              help='Enable LDA+U')
    workflow_group.add_argument('--ldauu', type=str,
                              help='Space-separated list of LDA+U U values (e.g., "1.0 2.0")')
    workflow_group.add_argument('--ldaul', type=str,
                              help='Space-separated list of LDA+U L values (e.g., "2 2")')
    workflow_group.add_argument('--ispin', type=int, choices=[1, 2],
                              help='Set ISPIN (1: non-spin-polarized, 2: spin-polarized)')
    workflow_group.add_argument('--magmom', type=str,
                              help='Space-separated list of magnetic moments (e.g., "1.0 2.0")')
    workflow_group.add_argument('--dos', action='store_true',
                              help='Calculate DOS')
    workflow_group.add_argument('--wan', action='store_true',
                              help='Enable Wannier calculations')
    workflow_group.add_argument('--vdw', action='store_true',
                              help='Enable vdW corrections')
    workflow_group.add_argument('--name', type=str,
                              help='Set system name')
    workflow_group.add_argument('--nk', type=int,
                              help='Set number of k-points')
    workflow_group.add_argument('--nsw', type=int,
                              help='Set number of ionic steps')
    workflow_group.add_argument('--queue', type=str, default="default",
                              help='Set job queue name')
    workflow_group.add_argument('--cores', type=int, default=40,
                              help='Set number of CPU cores')
    workflow_group.add_argument('--modules', type=str, 
                              help='Set required modules')

    # Analyzer subparser
    analyzer_parser = subparsers.add_parser('analyzer', help='Analyze VASP calculation results')
    analyzer_group = analyzer_parser.add_argument_group('Analysis Options')
    analyzer_group.add_argument('--band', action='store_true',
                              help='Output band structure')
    analyzer_group.add_argument('--spinsplit', action='store_true',
                              help='Calculate spin splitting')
    analyzer_group.add_argument('--nband', type=int,
                              help='Selected band number for analysis')
    analyzer_group.add_argument('--kseg', type=int,
                              help='Number of k-points per segment')
    analyzer_group.add_argument('--gap', action="store_true",
                              help='Calculate band gap')
    analyzer_group.add_argument('--efermi', type=float,
                              help='Set Fermi energy manually')
    analyzer_group.add_argument('--spin', action='store_true',
                              help='Enable spin-polarized analysis')

    return parser

def main():
    """Main entry point for the command line interface"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == 'workflow':
            # Initialize VASP input handler
            input_handler = VaspInputHandler()
            
            # Set input handler parameters from arguments
            input_handler.is_relax = args.relax
            input_handler.is_soc = args.soc
            input_handler.is_ldau = args.ldau
            input_handler.is_magnetic = args.ispin == 2
            input_handler.is_dos = args.dos
            input_handler.is_wannier = args.wan
            input_handler.is_vdw = args.vdw
            
            if args.name:
                input_handler.name = args.name
            if args.nk:
                input_handler.nk = args.nk
            if args.nsw:
                input_handler.nsw = args.nsw
            if args.queue:
                input_handler.queue = args.queue
            if args.cores:
                input_handler.cores = args.cores
            if args.modules:
                input_handler.modules = args.modules
            if args.ldauu:
                input_handler.ldau_u = [float(x) for x in args.ldauu.split()]
            if args.ldaul:
                input_handler.ldau_l = [int(x) for x in args.ldaul.split()]
            if args.ispin:
                input_handler.ispin = args.ispin
            if args.magmom:
                input_handler.magmom = [float(x) for x in args.magmom.split()]
                
            # Set up VASP workflow
            input_handler.setup_workflow()
            
        elif args.command == 'analyzer':
            # Initialize band analyzer
            analyzer = VaspBandAnalyzer()
            analyzer.spin_polarized = args.spin
            analyzer.fermi_energy = args.efermi
            
            if args.spinsplit:
                analyzer.ss=True
                analyzer.spin_polarized = True
                analyzer.read_kpoints()
                analyzer.read_eigenval()
                analyzer.write_spin_splitting(selected_band=args.nband)
                print(f"Spin splitting data written to spinsplit.dat")
                
            if args.gap:
                analyzer.gap=True
                analyzer.read_kpoints()
                analyzer.read_eigenval()
                analyzer.write_band_gap(args.gap)
                print(f"Band gap data written to gap.dat")
                
            if args.band:
                analyzer.band=True
                analyzer.read_kpoints()
                analyzer.read_eigenval()
                analyzer.write_band_structure()
                analyzer.plot_band_structure()
                print(f"Band structure data written to band.dat")
                print(f"Band structure plot saved to band.png")
                
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main()) 