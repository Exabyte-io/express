import numpy as np
from typing import Tuple
from copy import deepcopy
from express.properties.utils import eigenvalues
from express.properties.non_scalar import NonScalarProperty

PRECISION_MAP = {
    # decimal places
    "ibz_kpts": 4,
    "eigenvalues": 4,
}


class BandGaps(NonScalarProperty):
    """
    The minimum energy difference between the highest occupied (valence) band and the lowest unoccupied ( conduction)
    band, extracted from the k-mesh of electronic eigenvalues (default) or the bandstructure. Can be direct - when
    the difference is between the energy points at the same point in reciprocal space, and indirect - when the
    difference between two inequivalent points. The flavor defines the type of band_gap computation. It could be done
    either using 'mesh' or 'path'.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(BandGaps, self).__init__(name, parser, *args, **kwargs)

        self.values = None
        self.nspins = self.safely_invoke_parser_method("nspins")
        self.ibz_k_points = self.safely_invoke_parser_method("ibz_k_points")
        self.fermi_energy = self.safely_invoke_parser_method("fermi_energy")
        self.band_gaps_direct = self.safely_invoke_parser_method("band_gaps_direct")
        self.band_gaps_indirect = self.safely_invoke_parser_method("band_gaps_indirect")
        self.eigenvalues_at_kpoints = self.safely_invoke_parser_method("eigenvalues_at_kpoints")

        if self.band_gaps_direct is not None and self.band_gaps_indirect is not None:
            self.values = [
                self._serialize_band_gaps(self.band_gaps_direct, "direct"),
                self._serialize_band_gaps(self.band_gaps_indirect, "indirect"),
            ]

    def _serialize(self) -> dict:
        return {
            "name": self.name,
            "values": self.values if self.values else self.get_band_gaps_from_mesh(),
            "eigenvalues": self._eigenvalues() if not self.values else [],
        }

    def _serialize_band_gaps(self, gap: float, gap_type: str, spin: float = 1 / 2) -> dict:
        return {
            "type": gap_type,
            "units": self.manifest["defaults"]["units"],
            "value": gap,
            "spin": spin,
        }

    def get_band_gaps_from_mesh(self) -> list:
        """
        Compute direct and indirect band gaps for all available spins
        """
        occupations, eigenvalue_mesh = self._get_bands_info()

        gap_types = ["direct", "indirect"]
        computed_gaps = []

        for s in range(self.nspins):
            for gap_type in gap_types:
                computed_gaps.append(
                    self.compute_on_mesh(
                        eigenvalue_mesh=eigenvalue_mesh, occupations=occupations, spin_channel=s, gap_type=gap_type
                    )
                )
        return computed_gaps

    def compute_on_mesh(
        self,
        eigenvalue_mesh: np.ndarray,
        occupations: np.ndarray,
        spin_channel: int = 0,
        gap_type: str = "indirect",
        absolute_eigenvalues: bool = True,
    ) -> dict:
        """
        Calculates the band gap on the material's mesh for a given gap type and spin channel.

        Args:
            eigenvalue_mesh:      3D array of eigenvalues with indices in following order: spin, kpoint, eigenvalue
            occupations:          2D array of number of occupied bands per spin and k-point (order: spin, kpoint)
            spin_channel:         spin index (0 -> 1/2, 1 -> -1/2)
            gap_type:             band gap type, either direct or indirect
            absolute_eigenvalues: whether to unshift the eigenvalues (applies to band edge values only)

        Returns:
            band gap dictionary
        """
        ev_k = eigenvalue_mesh[spin_channel, :, 0]  # valence band of current spin channel
        ec_k = eigenvalue_mesh[spin_channel, :, 1]  # conduction band of current spin channel
        occ_k = occupations[spin_channel]  # band occupations for current spin channel
        spin = 1 / 2 * (-1) ** spin_channel  # spin value

        gap, k_val, k_cond = BandGaps._find_gap(occ_k, ev_k, ec_k, gap_type=gap_type)
        result = self._serialize_band_gaps(gap=gap, gap_type=gap_type, spin=spin)

        # value for shifting back eigenvalues (see also _get_bands_info)
        e_fermi = self.fermi_energy if absolute_eigenvalues else 0

        precision = PRECISION_MAP["ibz_kpts"]

        if k_val is not None and k_cond is not None:
            result.update(
                {
                    "kpointValence": self._round(self.ibz_k_points[k_val], precision),
                    "kpointConduction": self._round(self.ibz_k_points[k_cond], precision),
                    "eigenvalueValence": ev_k[k_val] + e_fermi,
                    "eigenvalueConduction": ec_k[k_cond] + e_fermi,
                }
            )
        return result

    def _get_bands_info(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Extracts bands information:
            - number of kpoints (nk) - int
            - number of spins (ns) - int
            - eigenvalue mesh (e_skn) of valence and conduction band shifted by Fermi energy - 3D array
            - number of occupied bands per spin and k-point (occ_sk) - 2D array

        Note: spin indices correspond to spin value as follows (see also utils.eigenvalues function)
              index       value
              s = 0  <->  1/2
              s = 1  <-> -1/2

        Returns:
            tuple: bands information containing e_skn and occ_sk explained above.

        """
        nk = len(self.ibz_k_points)
        ns = self.nspins
        e_skn = np.array([[eigenvalues(self.eigenvalues_at_kpoints, k, s) for k in range(nk)] for s in range(ns)])
        e_skn -= self.fermi_energy
        occ_sk = (e_skn < 0.0).sum(2)
        # select highest occupied and lowest unoccupied bands
        e_skn = np.array([[e_skn[s, k, occ_sk[s, k] - 1 : occ_sk[s, k] + 1] for k in range(nk)] for s in range(ns)])
        return occ_sk, e_skn

    @staticmethod
    def _find_gap(
        occupations: np.ndarray, valence_band: np.ndarray, conduction_band: np.ndarray, gap_type: str = "indirect"
    ) -> Tuple[float, int, int]:
        """
        Computes the difference in energy between the highest valence band and the lowest conduction band.

        Args:
            occupations:     numbers of occupied bands per k-point.
            valence_band:    eigenvalues of valence band per k-point.
            conduction_band: eiganvalues of conduction band per k-point.
            gap_type:        band gap type, either direct or indirect.

        Returns:
            tuple: a (gap, k1, k2) tuple where k1 and k2 are the indices of the valence and conduction k-points.
        """
        if np.ptp(occupations) > 0:
            # Some band must be crossing fermi-level. Hence, we return zero for band gap and the actual k-points
            kv = kc = occupations.argmax()
            return 0.0, kv, kc
        if gap_type == "direct":
            direct_gaps = conduction_band - valence_band
            k = direct_gaps.argmin()
            return direct_gaps[k], k, k
        kv = valence_band.argmax()
        kc = conduction_band.argmin()
        return conduction_band[kc] - valence_band[kv], kv, kc

    def _eigenvalues(self) -> list:
        """
        Extract eigenvalues around Fermi level.
        i.e., last two values in occupation 1 and first two values in occupation 0.

        Returns:
             dict
        """
        precision = PRECISION_MAP["eigenvalues"]
        eigens_at_kpoints = deepcopy(self.eigenvalues_at_kpoints)
        for eigens_at_kpoint in eigens_at_kpoints:
            eigens_at_kpoint["kpoint"] = self._round(eigens_at_kpoint["kpoint"], precision)
            for eigens_at_spin in eigens_at_kpoint["eigenvalues"]:
                eigens_at_spin["energies"] = self._round(eigens_at_spin["energies"], precision)
                eigens_at_spin["occupations"] = self._round(eigens_at_spin["occupations"], precision)
                # occupations are empty in case of QE GW, hence sending all values.
                if len(eigens_at_spin["occupations"]) == 0:
                    continue
                start = max(0, len(eigens_at_spin["occupations"]) - eigens_at_spin["occupations"][::-1].index(1.0) - 2)
                end = min(len(eigens_at_spin["occupations"]), eigens_at_spin["occupations"].index(0.0) + 2)
                eigens_at_spin["energies"] = eigens_at_spin["energies"][start:end]
                eigens_at_spin["occupations"] = eigens_at_spin["occupations"][start:end]
        return eigens_at_kpoints
