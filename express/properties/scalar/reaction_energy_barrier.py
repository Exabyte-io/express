from express.properties.scalar import ScalarProperty


class ReactionEnergyBarrier(ScalarProperty):
    """
    Reaction energy barrier.
    """

    def __init__(self, name, raw_data, *args, **kwargs):
        super(ReactionEnergyBarrier, self).__init__(name, raw_data, *args, **kwargs)
        energies = self.raw_data.get("reaction_energies", [])
        self.value = sorted(energies, key=lambda e: abs(e or 0), reverse=True)[0]
