from express.properties.scalar import ScalarProperty


class ReactionEnergyBarrier(ScalarProperty):
    """
    Reaction energy barrier.
    """

    def __init__(self, name, raw_data, *args, **kwargs):
        super(ReactionEnergyBarrier, self).__init__(name, raw_data, *args, **kwargs)
        energies = [e or 0 for e in self.raw_data.get("reaction_energies", [])]
        energies = [energies[i] - energies[0] for i in range(len(energies))]
        self.value = sorted(energies, key=lambda e: abs(e), reverse=True)[0]
