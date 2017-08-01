import string

import numpy as np

from express.parsers.formats.xml import BaseXMLParser

SPIN_MAP = {
    1: 'up',
    2: 'down'
}


class VaspXMLParser(BaseXMLParser):
    """
    Vasp XML parser class.

    Args:
        xml_file_path (str): path to the xml file.
    """

    def __init__(self, xml_file_path):
        super(VaspXMLParser, self).__init__(xml_file_path)

    def eigenvalues_at_kpoints(self):
        """
        Returns eigenvalues for all kpoints.

        Returns:
             list

        Example:
            [
                {
                    'kpoint': [-0.5, 0.5, 0.5],
                    'weight': 9.5238095E-002,
                    'eigenvalues': [
                        {
                            'energies': [-1.4498446E-001, ..., 4.6507387E-001],
                            'occupations': [1, ... , 0],
                            'spin': 0.5
                        }
                    ]
                },
                ...
            ]
        """
        kpoints_list = self.root.find('kpoints').find('.//varray[@name="kpointlist"]')
        kpoints_weight = self.root.find('kpoints').find('.//varray[@name="weights"]')
        eigenvalues, occupations = self._parse_eigenvalues_occupations()

        eigenvalues_at_kpoints = []
        for kp_id, (kpoint, weight) in enumerate(zip(kpoints_list, kpoints_weight)):
            eigenvalues_at_kpoint = {
                "kpoint": map(float, kpoint.text.split()),
                "weight": float(weight.text),
                "eigenvalues": []
            }
            for spin in eigenvalues:
                eigenvalues_at_kpoint['eigenvalues'].append({
                    'energies': eigenvalues[spin][kp_id],
                    'occupations': occupations[spin][kp_id],
                    'spin': 0.5 if spin == 0 else -0.5
                })
            eigenvalues_at_kpoints.append(eigenvalues_at_kpoint)

    def _parse_eigenvalues_occupations(self):
        """
        Extracts eigenvalues and occupations for each spin and kpoint.

        Returns:
            tuple: a tuple of the eigenvalues and occupations for each spin and kpoint.
        """
        eigenvalues = {}
        occupations = {}
        eigenvalues_tag = self.root.findall('calculation')[-1].find('eigenvalues/array/set')
        for id_spin, eigen_spin in enumerate(eigenvalues_tag):
            eigenvalues[id_spin] = {}
            occupations[id_spin] = {}
            for id_kpt, eigen_kpt in enumerate(eigen_spin):
                kpt_data = np.array([list(map(float, _.text.split())) for _ in eigen_kpt])
                eigenvalues[id_spin][id_kpt] = kpt_data[:, 0]
                occupations[id_spin][id_kpt] = kpt_data[:, 1]
        return eigenvalues, occupations

    def fermi_energy(self):
        """
        Extracts fermi energy.

        Returns:
            float
        """
        tag = self.root.findall('calculation')[-1].find('dos/i')
        return float(tag.text)

    def nspins(self):
        """
        Extracts the number of number of spin components.

        Returns:
             int
        """
        tag = self.root.find('parameters').find('.//separator[@name="electronic spin"]').find('.//i[@name="ISPIN"]')
        return int(tag.text)

    def dos(self, combined=True):
        """
        Extracts density of states. DOS value for each atom with the same element and orbit number will be added
        together and packed in a dictionary. The result containing energy levels, total DOS and partial DOS for each
        element will be returned.

        Args:
            combined (bool): If True, PDOS value for the same elements will be added together.

        Returns:
            dict

        Example:
            {
                'energy': [-1.0, 0, 1.0],
                'total': [0.013, 0.124, 0.923],
                'partial': [
                    {
                        'element': 'C',
                        'electronicState': 's-up',
                        'value': [0.00015, 0.000187, 0.000232, 0.000287, 0.000355, 0.000437]
                    },
                    {
                        'element': 'C',
                        'electronicState': 'p-up',
                        'value': [6.87e-06, 8.5e-06, 1.0e-05, 1.3e-05, 1.63e-05, 2.01e-05]
                    },
                ]
            }
        """
        energy_levels, total_dos, partial_dos_values, partial_dos_infos, electronic_states = self._extract_dos()
        if combined:
            combined_pdos_values = []
            combined_pdos_infos = []
            for atom_type in set(self.atom_names()):
                for elec_state in electronic_states:
                    matched_pdos = []
                    for pdos_idx, pdos_info_item in enumerate(partial_dos_infos):
                        if pdos_info_item['electronicState'] == elec_state and atom_type == pdos_info_item['element']:
                            matched_pdos.append(partial_dos_values[pdos_idx])
                    combined_pdos_values.append(np.sum(matched_pdos, axis=0).tolist())
                    combined_pdos_infos.append({
                        'element': atom_type,
                        'electronicState': elec_state,
                        'spin': 0.5 if 'up' in elec_state else -0.5
                    })
            partial_dos_values, partial_dos_infos = combined_pdos_values, combined_pdos_infos
        return {
            'energy': energy_levels.tolist(),
            'total': total_dos.tolist(),
            'partial': partial_dos_values,
            'partial_info': partial_dos_infos
        }

    def atom_names(self):
        """
        Parses atoms information and returns name of atoms.

        Returns:
            list: list of atom names.
        """
        return [atom.find('c').text.strip() for atom in self.root.find('atominfo/array/set').findall('rc')]

    def _extract_dos(self):

        """
        Extracts density of states (total and partial) from xml output.

        Returns:
            tuple: energy levels, total dos, partial dos and electronic states values
        """
        dos_root = self.root.findall('calculation')[-1].find('dos')
        tdos_root = dos_root.find('total').find('array').find('set').find('set').findall('r')
        tot_dos = np.array([map(float, tdos.text.split()) for tdos in tdos_root])
        energy_levels = tot_dos[:, 0]
        total_dos = tot_dos[:, 1]
        partial_dos_values, partial_dos_infos, electronic_states = self._partial_dos(dos_root)
        return energy_levels, total_dos, partial_dos_values, partial_dos_infos, electronic_states

    def _partial_dos(self, dos_root):
        """
        Parses partial DOS for each element with its orbit value. DOS value for each atom with the same element and
        orbit number will be added together and packed in a dictionary.

        Args:
            dos_root (xml.etree.ElementTree.Element): dos root Element instance of ElementTree XML class.

        Returns:
            dict: a dictionary containing partial DOS values for each element.
                Example:
                    [
                        {
                            'element': 'C',
                            'electronicState': 's-down',
                            'value': [0.00015, 0.000187, 0.000232, 0.000287, 0.000355, 0.000437]
                        },
                        {
                            'element': 'Ti',
                            'electronicState': 'p-up',
                            'value': [6.87e-06, 8.5e-06, 1.0e-05, 1.3e-05, 1.63e-05, 2.01e-05]
                        }
                    ]
        """
        partial_dos_values = []
        partial_dos_infos = []
        electronic_states = set()
        if dos_root.find('partial') is not None:
            orbit_symbols = [orbit.text.strip() for orbit in dos_root.find('partial/array').findall('field')[1:]]
            partial_root = dos_root.find('partial/array/set')
            for atom_id, atom in enumerate(partial_root):
                for spin_id, spin in enumerate(atom):
                    pdos_spin = np.array([map(float, pdos.text.split()[1:]) for pdos in spin.findall('r')])
                    for column_id, column in enumerate(pdos_spin.T):
                        # if number of spins are more than 1
                        elec_state = '{0}-{1}'.format(orbit_symbols[column_id], SPIN_MAP[spin_id + 1]) if len(
                            atom) > 1 else orbit_symbols[column_id - 1]
                        electronic_states.add(elec_state)
                        partial_dos_values.append(column.tolist())
                        partial_dos_infos.append({
                            'element': self.atom_names()[atom_id],
                            'index': atom_id,
                            'electronicState': elec_state,
                            'spin': 0.5 if spin_id == 0 else -0.5
                        })
        return partial_dos_values, partial_dos_infos, electronic_states

    def lattice(self):
        """
        Extract lattice.

        Returns:
            dict

        Example:
            {
                'vectors': {
                    'a': [-0.561154473, -0.000000000, 0.561154473],
                    'b': [-0.000000000, 0.561154473, 0.561154473],
                    'c': [-0.561154473, 0.561154473, 0.000000000],
                    'alat': 1.0
                }
             }
        """
        vectors = {}
        for idx, vector in enumerate(
                self._parse_varray(self.root.find('structure[@name="finalpos"]/crystal/varray[@name="basis"]'))):
            vectors.update({
                string.ascii_lowercase[idx]: vector.tolist()
            })
        vectors.update({'alat': 1.0})

        return {
            'vectors': vectors
        }

    def basis(self):
        """
        Extract basis.

        Returns:
            dict

        Example:
            {
                'units': 'crystal',
                'elements': [{'id': 1, 'value': 'Si'}, {'id': 2, 'value': 'Si'}],
                'coordinates': [{'id': 1, 'value': [0.0, 0.0, 0.0]}, {'id': 2, 'value': [0.0, 0.0, 0.0]}]
             }
        """
        elements, coordinates = [], []
        for idx, vector in enumerate(
                self._parse_varray(self.root.find('structure[@name="finalpos"]/varray[@name="positions"]'))):
            elements.append({
                'id': idx,
                'value': self.atom_names()[idx]
            })
            coordinates.append({
                'id': idx,
                'value': vector.tolist()
            })

        return {
            'units': 'crystal',
            'elements': elements,
            'coordinates': coordinates
        }

    def _parse_varray(self, varray):
        """
        Parses varray elements.

        Example:
            <varray name="positions" >
                <v>       0.00000000       0.69512316       0.69512316 </v>
                <v>       0.50000000       0.80487684       0.19512316 </v>
                <v>       0.00000000       0.30487684       0.30487684 </v>
                <v>       0.50000000       0.19512316       0.80487684 </v>
                <v>       0.50000000       0.50000000       0.50000000 </v>
                <v>       0.00000000       0.00000000      -0.00000000 </v>
            </varray>

        Args:
            varray: varray xml element.

        Returns:
            ndarray: a matrix containing all the values found in the varray.
        """
        return np.array([v.text.split() for v in varray.findall('v')], dtype=np.float) if varray else np.array([])

    def stress_tensor(self):
        """
        Extracts stress tensor.

        Returns:
            list
        """
        return self._parse_varray(self.root.findall('calculation')[-1].find('.//varray[@name="stress"]'))

    def atomic_forces(self):
        """
        Extracts atomic forces.

        Returns:
            list
        """
        return self._parse_varray(self.root.findall('calculation')[-1].find('.//varray[@name="forces"]'))
