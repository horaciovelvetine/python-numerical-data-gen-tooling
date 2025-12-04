from dataclasses import dataclass

from ...models import DependencyTier


@dataclass
class Dependency:
    """
    Describes the position of a containing facility in the overall dependency hierarchy of a particular installation or at a particular site. The 'tier': Primary, Secondary, Tertiary (P, S, T) designates the layer this facility exists in, while the value (1, 2, 3, or any combination of these values) describes the facilities in the next (ascending) layer which this dependency supports. E.g. an S2 supports all P2 facilities, and a T123 would suppoer all S1, S2, and S3 facilities.
    """

    tier: DependencyTier
    support_number: list[int]

    def depends_on(self, other: "Dependency") -> bool:
        """
        Determines if this dependency chain ('self') depends on another ('other').

        The dependency rules are:
        1. The 'other' DependencyChain must be a higher tier in the hierarchy
           (e.g., Secondary depends on Tertiary, Primary depends on Secondary, etc.).
           Lower index means lower tier (Primary < Secondary < Tertiary).
        2. There must be at least one overlapping support number between self and other,
           meaning self's support_number must share at least one value with other's support_number.

        Returns:
            True if 'self' depends on 'other' according to the rules above, else False.
        """
        tier_order = {"Primary": 0, "Secondary": 1, "Tertirary": 2}
        self_tier_index = tier_order[self.tier.value]
        other_tier_index = tier_order[other.tier.value]
        # 'other' must be above 'self' in the hierarchy (higher index)
        if other_tier_index <= self_tier_index:
            return False
        # There must be at least one common support number
        if not any(num in other.support_number for num in self.support_number):
            return False
        return True

    def value(self) -> str:
        """
        Returns the short string representation of the dependency chain,
        e.g., 'S3' for tier=Secondary, support_number=[3].
        """
        key = self.tier.key()
        number_str = "".join(str(n) for n in self.support_number)
        return f"{key}{number_str}"
