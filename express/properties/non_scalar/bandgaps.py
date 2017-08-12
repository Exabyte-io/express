import numpy as np

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

    def __init__(self, name, raw_data, *args, **kwargs):
        super(BandGaps, self).__init__(name, raw_data, *args, **kwargs)
        self.nspins = self.raw_data["nspins"]
        self.ibz_k_points = self.raw_data["ibz_k_points"]
        self.fermi_energy = self.raw_data["fermi_energy"]
        self.band_gaps_direct = self.raw_data["band_gaps_direct"]
        self.band_gaps_indirect = self.raw_data["band_gaps_indirect"]
        self.eigenvalues_at_kpoints = self.raw_data["eigenvalues_at_kpoints"]

        self.values = None
        if self.band_gaps_direct and self.band_gaps_indirect:
            self.values = [
                self._serialize_band_gaps(self.band_gaps_direct, "direct"),
                self._serialize_band_gaps(self.band_gaps_indirect, "indirect")
            ]

    def _serialize(self):
        return {
            'name': self.name,
            'values': self.values if self.values else [self.compute_on_mesh(type_) for type_ in ["direct", "indirect"]]
        }

    def _serialize_band_gaps(self, gap, type_):
        return {
            'type': type_,
            'units': self.esse.get_schema_default_values(self.name)["units"],
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
            k1 = divmod(k1, nk)
            k2 = divmod(k2, nk)

        result = self._serialize_band_gaps(gap, type_)
        if k1 is not None and k2 is not None:
            result.update({
                'kpointValence': self.ibz_k_points[k1[1] if isinstance(k1, tuple) else k1].tolist(),
                'kpointConduction': self.ibz_k_points[k2[1] if isinstance(k2, tuple) else k2].tolist()
            })
        return result

    def _get_bands_info(self):
        """
        Extracts bands information:
            - number of kpoints (nk)
            - number of spins (ns)
            - eigenvalue mesh (e_skn)
            - number of occupied bands (N_sk)

        Returns:
            tuple: bands information containing nk, ns, e_skn and N_sk explained above.

        """
        nk = len(self.ibz_k_points)
        ns = self.nspins
        e_skn = np.array([[eigenvalues(self.eigenvalues_at_kpoints, k, s) for k in range(nk)] for s in range(ns)])
        e_skn -= self.fermi_energy
        N_sk = (e_skn < 0.0).sum(2)
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
