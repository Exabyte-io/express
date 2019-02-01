import os
import numpy as np

from express.parsers import BaseParser
from express.parsers.utils import find_file
from express.parsers.apps.vasp import settings
from express.parsers.mixins.ionic import IonicDataMixin
from express.parsers.apps.vasp.formats.txt import VaspTXTParser
from express.parsers.apps.vasp.formats.xml import VaspXMLParser
from express.parsers.mixins.reciprocal import ReciprocalDataMixin
from express.parsers.mixins.electronic import ElectronicDataMixin
from express.parsers.apps.vasp.settings import NEB_DIR_PREFIX, NEB_STD_OUT_FILE


class VaspParser(BaseParser, IonicDataMixin, ElectronicDataMixin, ReciprocalDataMixin):
    """
    Vasp parser class.
    """

    def __init__(self, *args, **kwargs):
        super(VaspParser, self).__init__(*args, **kwargs)
        self.work_dir = self.kwargs["work_dir"]
        self.stdout_file = self.kwargs["stdout_file"]
        self.txt_parser = VaspTXTParser(self.work_dir)
        self.xml_parser = VaspXMLParser(find_file(settings.XML_DATA_FILE, self.work_dir))

    def _get_outcar_content(self):
        """
        Returns the content of OUTCAR file.

        Returns:
            str
        """
        outcar_content = ''
        outcar_path = os.path.join(self.work_dir, "OUTCAR")
        if os.path.exists(outcar_path):
            with open(outcar_path) as f:
                outcar_content = f.read()
        return outcar_content

    def total_energy(self):
        """
        Returns total energy.

        Reference:
            func: express.parsers.mixins.electronic.ElectronicDataMixin.total_energy
        """
        return self.txt_parser.total_energy(self._get_file_content(self.stdout_file))

    def fermi_energy(self):
        """
        Returns fermi energy.

        Reference:
            func: express.parsers.mixins.electronic.ElectronicDataMixin.fermi_energy
        """
        return self.xml_parser.fermi_energy()

    def nspins(self):
        """
        Returns the number of spins.

        Reference:
            func: express.parsers.mixins.electronic.ElectronicDataMixin.nspins
        """
        return self.xml_parser.nspins()

    def eigenvalues_at_kpoints(self):
        """
        Returns eigenvalues for all kpoints.

        Reference:
            func: express.parsers.mixins.electronic.ElectronicDataMixin.eigenvalues_at_kpoints
        """
        return self.xml_parser.eigenvalues_at_kpoints()

    def ibz_k_points(self):
        """
        Returns ibz_k_points.

        Note:
            The function assumes that kpoints extracted from parsed source are inside the irreducible wedge of the
            Brillouin zone. Without checking whether it is the case or not.

        Reference:
            func: express.parsers.mixins.reciprocal.ReciprocalDataMixin.ibz_k_points
        """
        return np.array([eigenvalueData["kpoint"] for eigenvalueData in self.eigenvalues_at_kpoints()])

    def dos(self):
        """
        Returns density of states.

        Reference:
            func: express.parsers.mixins.electronic.ElectronicDataMixin.dos
        """
        return self.xml_parser.dos(combined=True)

    def final_basis(self):
        """
        Returns final basis.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.final_basis
        """
        return self.xml_parser.final_basis()

    def final_lattice_vectors(self):
        """
        Returns final lattice vectors.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.final_lattice_vectors
        """
        return self.xml_parser.final_lattice_vectors()

    def convergence_electronic(self):
        """
        Extracts convergence electronic.

        Reference:
            func: express.parsers.mixins.electronic.ElectronicDataMixin.convergence_electronic
        """
        outcar = self._get_outcar_content()
        stdout = self._get_file_content(self.stdout_file)
        try:
            atom_names = self.xml_parser.atom_names()
        except:
            print "atom_names can not be extracted"
            atom_names = []
        return self.txt_parser.convergence_electronic(outcar, stdout, atom_names)

    def convergence_ionic(self):
        """
        Extracts convergence ionic.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.convergence_ionic
        """
        outcar = self._get_outcar_content()
        stdout = self._get_file_content(self.stdout_file)
        return self.txt_parser.convergence_ionic(outcar, stdout, self.xml_parser.atom_names())

    def stress_tensor(self):
        """
        Returns stress tensor.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.stress_tensor
        """
        return self.xml_parser.stress_tensor()

    def pressure(self):
        """
        Returns pressure.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.pressure
        """
        return self.txt_parser.pressure(self._get_outcar_content())

    def total_force(self):
        """
        Returns total force.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.total_force
        """
        return self.txt_parser.total_force(self._get_outcar_content())

    def atomic_forces(self):
        """
        Returns forces that is exerted on each atom by its surroundings.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.atomic_forces
        """
        return self.xml_parser.atomic_forces()

    def total_energy_contributions(self):
        """
        Extracts total energy contributions.

        Reference:
            func: express.parsers.mixins.electronic.ElectronicDataMixin.total_energy_contributions
        """
        return self.txt_parser.total_energy_contributions(self._get_outcar_content())

    def zero_point_energy(self):
        """
        Returns zero point energy.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.zero_point_energy
        """
        return self.txt_parser.zero_point_energy(self._get_outcar_content())

    def magnetic_moments(self):
        """
        Returns magnetic moments.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.magnetic_moments
        """
        return self.txt_parser.magnetic_moments(os.path.join(self.work_dir, "OUTCAR"))

    def _get_neb_image_dirs(self, prefix="0"):
        """
        Returns the sorted list of NEB image directories.

        Args:
            prefix (str): image directory prefix.

        Returns:
             list[str]
        """
        paths = []
        for root, dirs, files in os.walk(self.work_dir):
            for dir_ in [d for d in dirs if str(d).startswith(prefix)]:
                path = os.path.join(root, dir_)
                paths.append({"path": path, "index": int(dir_)})
            break
        return map(lambda p: p["path"], sorted(paths, key=lambda p: p["index"]))

    def _get_neb_image_stdout_files(self, prefix="0", output_file="stdout"):
        """
        Returns the paths to NEB image standard output files.

        Note: only image 01 writes to the usual stdout file, other images write to `stdout` inside image directory.

        Args:
            prefix (str): image directory prefix.
            output_file (str): output file name.

        Returns:
             list[str]
        """
        files = []
        for path in self._get_neb_image_dirs(prefix):
            file_ = self.stdout_file if os.path.basename(path) == "01" else os.path.join(path, output_file)
            files.append(file_)
        return files

    def reaction_energies(self):
        """
        Returns reaction energies.

        Returns:
             list
        """
        energies = []
        for path in self._get_neb_image_stdout_files(NEB_DIR_PREFIX, NEB_STD_OUT_FILE):
            energies.append(self.txt_parser.total_energy(self._get_file_content(path)))
        return [energies[i] - energies[0] for i in range(len(energies))]

    def reaction_coordinates(self):
        """
        Returns reaction coordinates.

        Note: it is assumed that initial and final directories contain CONTCAR file.

        Returns:
             list
        """
        structures = []
        for path in self._get_neb_image_dirs():
            with open(os.path.join(path, "CONTCAR")) as f:
                structures.append(f.read())
        return self.reaction_coordinates_from_poscars(structures)
