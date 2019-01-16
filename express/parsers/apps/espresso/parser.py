import os
import numpy as np

from express.parsers import BaseParser
from express.parsers.utils import find_file
from express.parsers.apps.espresso import settings
from express.parsers.mixins.ionic import IonicDataMixin
from express.parsers.mixins.reciprocal import ReciprocalDataMixin
from express.parsers.mixins.electronic import ElectronicDataMixin
from express.parsers.apps.espresso.formats.txt import EspressoTXTParser
from express.parsers.apps.espresso.formats.xml import EspressoXMLParser


class EspressoParser(BaseParser, IonicDataMixin, ElectronicDataMixin, ReciprocalDataMixin):
    """
    Espresso parser class.
    """

    def __init__(self, *args, **kwargs):
        super(EspressoParser, self).__init__(*args, **kwargs)
        self.work_dir = self.kwargs["work_dir"]
        self.stdout_file = self.kwargs["stdout_file"]
        self.txt_parser = EspressoTXTParser(self.work_dir)
        self.xml_parser = EspressoXMLParser(find_file(settings.XML_DATA_FILE, self.work_dir))

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
        return self.txt_parser.dos()

    def basis(self):
        """
        Returns basis.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.basis
        """
        return self.xml_parser.basis()

    def lattice_vectors(self):
        """
        Returns lattice.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.lattice_vectors
        """
        return self.xml_parser.lattice_vectors(reciprocal=False)

    def convergence_electronic(self):
        """
        Extracts convergence electronic.

        Reference:
            func: express.parsers.mixins.electronic.ElectronicDataMixin.convergence_electronic
        """
        return self.txt_parser.convergence_electronic(self._get_file_content(self.stdout_file))

    def convergence_ionic(self):
        """
        Returns convergence ionic.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.convergence_ionic
        """
        return self.txt_parser.convergence_ionic(self._get_file_content(self.stdout_file))

    def stress_tensor(self):
        """
        Returns stress tensor.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.stress_tensor
        """
        return self.txt_parser.stress_tensor(self._get_file_content(self.stdout_file))

    def pressure(self):
        """
        Returns pressure.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.pressure
        """
        return self.txt_parser.pressure(self._get_file_content(self.stdout_file))

    def total_force(self):
        """
        Returns total force.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.total_force
        """
        return self.txt_parser.total_force(self._get_file_content(self.stdout_file))

    def atomic_forces(self):
        """
        Returns forces that is exerted on each atom by its surroundings.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.atomic_forces
        """
        return self.txt_parser.atomic_forces(self._get_file_content(self.stdout_file))

    def total_energy_contributions(self):
        """
        Extracts total energy contributions.

        Reference:
            func: express.parsers.mixins.electronic.ElectronicDataMixin.total_energy_contributions
        """
        return self.txt_parser.total_energy_contributions(self._get_file_content(self.stdout_file))

    def zero_point_energy(self):
        """
        Returns zero point energy.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.zero_point_energy
        """
        return self.txt_parser.zero_point_energy(self._get_file_content(self.stdout_file))

    def phonon_dos(self):
        """
        Returns phonon dos.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.phonon_dos
        """
        return self.txt_parser.phonon_dos()

    def phonon_dispersions(self):
        """
        Returns phonon dispersions.

        Reference:
            func: express.parsers.mixins.ionic.IonicDataMixin.phonon_dispersions
        """
        return self.txt_parser.phonon_dispersions()

    def _get_neb_image_paths_via_prefix(self, prefix, output_file, outdir):
        """
        Returns the paths to images' output files.

        Args:
            prefix (str): image directory prefix.
            output_file (str): output file name.
            outdir (str): outdir name.

        Returns:
             list[str]
        """
        paths = []
        for root, dirs, files in os.walk(os.path.join(self.work_dir, outdir)):
            for dir_ in [d for d in dirs if str(d).startswith(prefix)]:
                path = os.path.join(root, dir_, output_file)
                paths.append({"path": path, "index": int(dir_.replace(prefix, ""))})
            break
        return map(lambda p: p["path"], sorted(paths, key=lambda p: p["index"]))

    def reaction_energies(self, prefix="__prefix___", output_file="PW.out", outdir="outdir"):
        """
        Returns reaction energies.

        Args:
            prefix (str): image directory prefix.
            output_file (str): output file name.
            outdir (str): outdir name.

        Returns:
             list
        """
        energies = []
        for path in self._get_neb_image_paths_via_prefix(prefix, output_file, outdir):
            energies.append(self.txt_parser.total_energy(self._get_file_content(path)))
        return energies
