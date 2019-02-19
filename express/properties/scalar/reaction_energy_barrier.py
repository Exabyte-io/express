from express.properties.scalar import ScalarProperty


class ReactionEnergyBarrier(ScalarProperty):
    """
    Reaction energy barrier.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(ReactionEnergyBarrier, self).__init__(name, parser, *args, **kwargs)
        energies = self.parser.reaction_energies()
        self.value = sorted(energies, key=lambda e: abs(e or 0), reverse=True)[0]
