from enum import Enum

class DependencyTier(Enum):
    """
    DependencyTier designates the position of a given dependency within the hierarchy
    of facility dependencies. It is used to define and communicate the supporting
    infrastructure structure for facilities—specifying whether a system or component
    is primary, secondary, or tertiary in terms of its support relationships. This
    classification is essential for understanding and analyzing dependency chains
    among facilities.
    """

    Primary = "Primary"
    Secondary = "Secondary"
    Tertirary = "Tertirary"

    def key(self):
        """Return just the first letter based on the value"""
        return self.value[0]
