import logging
import os

from express.parsers.apps.vasp.parser import VaspParser
from express.parsers.crystal import CrystalParser
from express.parsers.molecule import MoleculeParser
from express.parsers.utils import lattice_basis_to_poscar
from express.properties import BaseProperty
from express.properties.non_scalar.symmetry import Symmetry
from express.properties.scalar.density import Density
from express.properties.scalar.elemental_ratio import ElementalRatio
from express.properties.scalar.p_norm import PNorm
from express.properties.scalar.volume import Volume
from express.properties.structural.inchi import Inchi
from express.properties.structural.inchi_key import InchiKey


class Material(BaseProperty):
    """
    Material class.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(Material, self).__init__(name, parser, *args, **kwargs)
        self.is_non_periodic = kwargs.get("is_non_periodic", False)

        cell_type = kwargs.get("cell_type", "original")
        structure_string = kwargs.get("structure_string")
        structure_format = kwargs.get("structure_format", "poscar")

        if not structure_string:
            if kwargs.get("is_initial_structure"):
                if isinstance(self.parser, VaspParser):
                    with open(os.path.join(self.parser.work_dir, "POSCAR")) as f:
                        structure_string = f.read()
                else:
                    basis = self.parser.initial_basis()
                    lattice = self.parser.initial_lattice_vectors()
                    structure_string = lattice_basis_to_poscar(lattice, basis)

            if kwargs.get("is_final_structure"):
                if isinstance(self.parser, VaspParser):
                    with open(os.path.join(self.parser.work_dir, "CONTCAR")) as f:
                        structure_string = f.read()
                else:
                    basis = self.parser.final_basis()
                    lattice = self.parser.final_lattice_vectors()
                    structure_string = lattice_basis_to_poscar(lattice, basis)

        if self.is_non_periodic:
            self.parser = MoleculeParser(
                structure_string=structure_string, structure_format=structure_format, cell_type=cell_type
            )
        else:
            self.parser = CrystalParser(
                structure_string=structure_string, structure_format=structure_format, cell_type=cell_type
            )

    @property
    def formula(self):
        return self.parser.reduced_formula()

    @property
    def unitCellFormula(self):
        return self.parser.formula()

    @property
    def derived_properties(self):
        derived_properties = []
        try:
            symmetry = Symmetry("symmetry", self.parser).serialize_and_validate()
            if self.is_non_periodic:
                inchi = Inchi("inchi", self.parser).serialize_and_validate()
                inchi_key = InchiKey("inchi_key", self.parser).serialize_and_validate()
                volume = None
                density = None
                derived_properties = [symmetry, inchi, inchi_key]
            else:
                inchi = None
                inchi_key = None
                volume = Volume("volume", self.parser).serialize_and_validate()
                density = Density("density", self.parser).serialize_and_validate()
                derived_properties = [volume, density, symmetry]
            derived_properties.extend(self._elemental_ratios())
            derived_properties.extend(self._p_norms())
        # TODO: Determine how to avoid an eternal pass when one derived property fails
        except Exception:
            logging.info("Derived properties array empty due to failure to calculate one (or more) values.")
            pass
        return sorted(derived_properties, key=lambda x: x["name"])

    @property
    def basis(self):
        return self.parser.basis()

    @property
    def lattice(self):
        return self.parser.lattice_bravais()

    def _serialize(self):
        """
        Serialize a material.

        Returns:
             dict
        """
        return {
            "_id": "",
            "name": self.name,
            "exabyteId": "",
            "hash": "",
            "formula": self.formula,
            "unitCellFormula": self.unitCellFormula,
            "lattice": self.lattice,
            "basis": self.basis,
            "derivedProperties": self.derived_properties,
            "creator": {"_id": "", "cls": "User", "slug": ""},
            "owner": {"_id": "", "cls": "Account", "slug": ""},
            "schemaVersion": "0.2.0",
        }

    def _elemental_ratios(self):
        """
        Returns a list of elemental ratios.

        Returns:
             list
        """
        elemental_ratios = []
        for element in self.parser.elemental_ratios().keys():
            elemental_ratio = ElementalRatio("elemental_ratio", self.parser, element=element).serialize_and_validate()
            elemental_ratios.append(elemental_ratio)
        return elemental_ratios

    def _p_norms(self):
        """
        Returns a list of p-norms.

        Reference:
            https://images.nature.com/full/nature-assets/npjcompumats/2016/npjcompumats201628/extref/npjcompumats201628-s1.pdf

        Returns:
            list
        """
        p_norms = []
        for degree in [0, 2, 3, 5, 7, 10]:
            p_norms.append(PNorm("p-norm", self.parser, degree=degree).serialize_and_validate())
        return p_norms
