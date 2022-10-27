import numpy as np

from copy import deepcopy
from express import settings
from express.properties.utils import eigenvalues
from express.properties.non_scalar import NonScalarProperty


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
                self._serialize_band_gaps(self.band_gaps_indirect, "indirect")
            ]

    def _serialize(self):
        return {
            'name': self.name,
            'values': self.values if self.values else [self.compute_on_mesh(type_) for type_ in ["direct", "indirect"]],
            'eigenvalues': self._eigenvalues() if not self.values else []
        }

    def _serialize_band_gaps(self, gap, type_):
        return {
            'type': type_,
            'units': self.manifest["defaults"]["units"],
            'value': gap
        }

    def compute_on_mesh(self, type_="indirect"):
        """
        Calculates the band gap on the material's mesh.

        Args:
            type_ (str): band gap type, either direct or indirect.

        Returns:
            dict
        """
        nk, ns, N_sk, e_skn = self._get_bands_info()
        ev_sk, ec_sk = self._get_valence_conduction_bands(e_skn)

        if ns == 1:
            gap, k1, k2 = self._find_gap(N_sk[0], ev_sk[0], ec_sk[0], type=type_)
        else:
            gap, k1, k2 = self._find_gap(N_sk.ravel(), ev_sk.ravel(), ec_sk.ravel(), type=type_)
            k1 = divmod(k1, nk)[1]
            k2 = divmod(k2, nk)[1]

        result = self._serialize_band_gaps(gap, type_)
        if k1 is not None and k2 is not None:
            result.update({
                "kpointValence": self._round(self.ibz_k_points[k1]),
                "kpointConduction": self._round(self.ibz_k_points[k2]),
                "eigenvalueValence": self._get_eigenvalues_from_band(e_sk=ev_sk, k=k1),
                "eigenvalueConduction": self._get_eigenvalues_from_band(e_sk=ec_sk, k=k2),
            })
        #print(result)
        return result

    def _get_bands_info(self):
        """
        Extracts bands information:
            - number of kpoints (nk) - int
            - number of spins (ns) - int
            - eigenvalue mesh (e_skn) - 3D array
            - number of occupied bands per spin and k-point (N_sk) - 2D array

        Returns:
            tuple: bands information containing nk, ns, e_skn and N_sk explained above.

        """
        nk = len(self.ibz_k_points)
        ns = self.nspins
        e_skn = np.array([[eigenvalues(self.eigenvalues_at_kpoints, k, s) for k in range(nk)] for s in range(ns)])
        e_skn -= self.fermi_energy
        N_sk = (e_skn < 0.0).sum(2)
        # select highest occupied and lowest unoccupied bands
        e_skn = np.array([[e_skn[s, k, N_sk[s, k] - 1:N_sk[s, k] + 1] for k in range(nk)] for s in range(ns)])
        return nk, ns, N_sk, e_skn

    def _get_valence_conduction_bands(self, e_skn):
        """
        Extracts valence and conduction bands.

        Returns:
            tuple: ev_sk (valence) and ec_sk (conduction) bands.
        """
        ev_sk = e_skn[:, :, 0]  # valence band
        ec_sk = e_skn[:, :, 1]  # conduction band
        return ev_sk, ec_sk

    def _find_gap(self, N_k, ev_k, ec_k, type="indirect"):
        """
        Computes the difference in energy between the highest valence band and the lowest conduction band.

        Args:
            N_k (ndarray): numbers of occupied bands.
            ev_k (ndarray): valence band.
            ec_k (ndarray): conduction band.
            type (str): band gap type, either direct or indirect.

        Returns:
            tuple: a (gap, k1, k2) tuple where k1 and k2 are the indices of the valence and conduction k-points.
        """
        if N_k.ptp() > 0:
            # Some band must be crossing fermi-level. Hence we return zero for band gap and the actual k-points
            kv = kc = np.argmax(N_k)
            return 0.0, kv, kc
        if type == "direct":
            gap_k = ec_k - ev_k
            k = gap_k.argmin()
            return gap_k[k], k, k
        kv = ev_k.argmax()
        kc = ec_k.argmin()
        return ec_k[kc] - ev_k[kv], kv, kc

    def _eigenvalues(self):
        """
        Extracts eigenvalues around Fermi level, i.e. last two values in occupation 1 and first two values in occupation 0.

        Returns:
             dict
        """
        eigens_at_kpoints = deepcopy(self.eigenvalues_at_kpoints)
        for eigens_at_kpoint in eigens_at_kpoints:
            eigens_at_kpoint["kpoint"] = self._round(eigens_at_kpoint["kpoint"])
            for eigens_at_spin in eigens_at_kpoint["eigenvalues"]:
                eigens_at_spin["energies"] = self._round(eigens_at_spin["energies"])
                eigens_at_spin["occupations"] = self._round(eigens_at_spin["occupations"])
                # occupations are empty in case of QE GW, hence sending all values.
                if len(eigens_at_spin["occupations"]) == 0: continue
                start = max(0, len(eigens_at_spin["occupations"]) - eigens_at_spin["occupations"][::-1].index(1.0) - 2)
                end = min(len(eigens_at_spin["occupations"]), eigens_at_spin["occupations"].index(0.0) + 2)
                eigens_at_spin["energies"] = eigens_at_spin["energies"][start:end]
                eigens_at_spin["occupations"] = eigens_at_spin["occupations"][start:end]
        return eigens_at_kpoints

    def _round(self, array):
        return np.round(array, settings.PRECISION).tolist()

    def _get_eigenvalues_from_band(self, e_sk, k, absolute=True):
        """
        Returns the absolute or shifted eigenvalue for a given k-point

        Args:
            e_sk: eigenvalue per spin and k-point (2D-array)
            k: index for k-point of interest
            absolute: whether to return absolute eigenvalues, i.e. without Fermi energy shift (default: True)

        Returns:
            List containing the eigenvalue (n_spin == 1) or eigenvalues (per spin) of the band e_sk at k-point k
        """
        n_spin = e_sk.shape[0]
        e_fermi = self.fermi_energy if absolute else 0

        return [e_sk[s, k] + e_fermi for s in range(n_spin)]

