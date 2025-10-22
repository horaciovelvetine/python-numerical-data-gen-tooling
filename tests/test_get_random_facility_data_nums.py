"""
Tests for get_random_facility_data_nums method.

These tests verify that the generated Facility data conforms to the
specifications defined in the README.md:
- Age: 0-80 years with specified distribution
- Condition Index: 1-99 with specified distribution  
- Remaining Service Life: Life Expectancy - Age >= RSL >= 0
- Time series: Generated correctly
- All numeric values are reasonable
"""

import sys
import pytest
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import get_random_facility_data_nums
from models.facility import Facility
from const.facility_life_expectancy import FacilityLifeExpectancy


class TestGetRandomFacilityDataNums:
    """Test suite for get_random_facility_data_nums function."""

    # Test with a variety of facility types
    @pytest.mark.parametrize(
        "facility_title",
        [
            "Data Center",
            "Admin Office",
            "Heating - Cooling Plant",
            "Equipment Pad",
            "Ground Terminal T1",
        ],
    )
    def test_returns_facility_object(self, facility_title):
        """Test that the function returns a Facility object."""
        result = get_random_facility_data_nums(facility_title)
        assert isinstance(result, Facility)
        assert result.title == facility_title

    def test_invalid_facility_title_raises_error(self):
        """Test that an invalid facility title raises ValueError."""
        with pytest.raises(ValueError, match="Unexpected facility title"):
            get_random_facility_data_nums("Invalid Facility Name")

    @pytest.mark.parametrize(
        "facility_title",
        [
            "Data Center",
            "Admin Office",
            "Heating - Cooling Plant",
        ],
    )
    def test_age_in_valid_range(self, facility_title):
        """Test that generated age is within valid range (0-80 years)."""
        result = get_random_facility_data_nums(facility_title)
        assert 0 <= result.age_in_years <= 80
        assert isinstance(result.age_in_years, int)

    @pytest.mark.parametrize(
        "facility_title",
        [
            "Data Center",
            "Admin Office",
            "Heating - Cooling Plant",
        ],
    )
    def test_condition_index_in_valid_range(self, facility_title):
        """Test that condition index is in range 1-99."""
        result = get_random_facility_data_nums(facility_title)
        assert 1 <= result.condition_index <= 99
        assert isinstance(result.condition_index, (int, float))

    @pytest.mark.parametrize(
        "facility_title",
        [
            "Data Center",
            "Admin Office",
            "Heating - Cooling Plant",
        ],
    )
    def test_remaining_service_life_is_reasonable(self, facility_title):
        """
        Test that remaining service life is reasonable.

        According to README: RSL = Life Expectancy - Age
        RSL should be >= 0 and <= Life Expectancy
        """
        result = get_random_facility_data_nums(facility_title)
        assert result.estimated_remaining_service_life >= 0
        assert result.estimated_remaining_service_life <= result.expected_service_life
        # RSL should roughly be Life Expectancy - Age (allowing for decay calculations)
        max_possible_rsl = result.expected_service_life - result.age_in_years
        # RSL could be less due to poor condition/high decay
        assert result.estimated_remaining_service_life <= max_possible_rsl

    @pytest.mark.parametrize(
        "facility_title",
        [
            "Data Center",
            "Admin Office",
            "Heating - Cooling Plant",
        ],
    )
    def test_time_series_exists_and_has_structure(self, facility_title):
        """Test that time series is generated with correct structure."""
        result = get_random_facility_data_nums(facility_title)
        assert result.time_series is not None
        assert isinstance(result.time_series, dict)

        # Should have 'year' and 'months' keys
        assert "year" in result.time_series
        assert "months" in result.time_series

        # Both should be dictionaries
        assert isinstance(result.time_series["year"], dict)
        assert isinstance(result.time_series["months"], dict)

        # Should have some data
        assert len(result.time_series["months"]) > 0

    @pytest.mark.parametrize(
        "facility_title",
        [
            "Data Center",
            "Admin Office",
            "Heating - Cooling Plant",
        ],
    )
    def test_facility_attributes_match_definition(self, facility_title):
        """Test that facility attributes match the FacilityLifeExpectancy definition."""
        result = get_random_facility_data_nums(facility_title)
        facility_def = FacilityLifeExpectancy.find_by_title(facility_title)

        assert result.title == facility_def.title
        assert result.expected_service_life == facility_def.life_expectancy
        assert result.facility_key == facility_def.key

    @pytest.mark.parametrize(
        "facility_title",
        [
            "Data Center",
            "Admin Office",
            "Heating - Cooling Plant",
        ],
    )
    def test_to_dict_returns_valid_dictionary(self, facility_title):
        """Test that to_dict() returns a properly formatted dictionary."""
        result = get_random_facility_data_nums(facility_title)
        result_dict = result.to_dict()

        assert isinstance(result_dict, dict)

        # Check all required keys exist
        required_keys = [
            "title",
            "expected_service_life",
            "facility_key",
            "age_in_years",
            "condition_index",
            "time_series",
            "estimated_remaining_service_life",
        ]
        for key in required_keys:
            assert key in result_dict

        # Verify types
        assert isinstance(result_dict["title"], str)
        assert isinstance(result_dict["expected_service_life"], int)
        assert isinstance(result_dict["facility_key"], int)
        assert isinstance(result_dict["age_in_years"], int)
        assert isinstance(result_dict["condition_index"], (int, float))
        assert isinstance(result_dict["time_series"], dict)
        assert isinstance(result_dict["estimated_remaining_service_life"], (int, float))

    def test_age_distribution_over_multiple_samples(self):
        """
        Test age distribution over 1000 samples.

        Expected distribution per README:
        - 50%: 20-40 years
        - 20%: 10-20 years
        - 20%: 41+ years
        - 10%: <10 years

        Note: Using Heating - Cooling Plant (60 year life expectancy) to test
        distribution properly, as Data Center (40 years) has limited 41+ range.
        """
        facility_title = "Heating - Cooling Plant"
        samples = 1000
        ages = []

        for _ in range(samples):
            result = get_random_facility_data_nums(facility_title)
            ages.append(result.age_in_years)

        # Count ages in each bucket
        under_10 = sum(1 for age in ages if age < 10)
        ten_to_twenty = sum(1 for age in ages if 10 <= age <= 20)
        twenty_to_forty = sum(1 for age in ages if 20 <= age <= 40)
        over_forty = sum(1 for age in ages if age >= 41)

        # Convert to percentages
        under_10_pct = (under_10 / samples) * 100
        ten_to_twenty_pct = (ten_to_twenty / samples) * 100
        twenty_to_forty_pct = (twenty_to_forty / samples) * 100
        over_forty_pct = (over_forty / samples) * 100

        # Allow for some variance (±7%) due to randomness
        tolerance = 7

        assert (
            abs(under_10_pct - 10) <= tolerance
        ), f"<10 years: expected ~10%, got {under_10_pct:.1f}%"
        assert (
            abs(ten_to_twenty_pct - 20) <= tolerance
        ), f"10-20 years: expected ~20%, got {ten_to_twenty_pct:.1f}%"
        assert (
            abs(twenty_to_forty_pct - 50) <= tolerance
        ), f"20-40 years: expected ~50%, got {twenty_to_forty_pct:.1f}%"
        assert (
            abs(over_forty_pct - 20) <= tolerance
        ), f"41+ years: expected ~20%, got {over_forty_pct:.1f}%"

    def test_condition_index_distribution_over_multiple_samples(self):
        """
        Test condition index distribution over 1000 samples.

        Expected distribution per README:
        - 7%: below 50 (1-49)
        - 5%: above 85 (86-99)
        - 88%: between 50-85
        - Mean value of ~70
        """
        facility_title = "Data Center"
        samples = 1000
        condition_indices = []

        for _ in range(samples):
            result = get_random_facility_data_nums(facility_title)
            condition_indices.append(result.condition_index)

        # Count condition indices in each bucket
        below_50 = sum(1 for ci in condition_indices if ci < 50)
        between_50_85 = sum(1 for ci in condition_indices if 50 <= ci <= 85)
        above_85 = sum(1 for ci in condition_indices if ci > 85)

        # Convert to percentages
        below_50_pct = (below_50 / samples) * 100
        between_50_85_pct = (between_50_85 / samples) * 100
        above_85_pct = (above_85 / samples) * 100

        # Calculate mean
        mean_ci = sum(condition_indices) / len(condition_indices)

        # Allow for some variance due to randomness
        tolerance = 4

        assert (
            abs(below_50_pct - 7) <= tolerance
        ), f"Below 50: expected ~7%, got {below_50_pct:.1f}%"
        assert (
            abs(between_50_85_pct - 88) <= tolerance
        ), f"50-85: expected ~88%, got {between_50_85_pct:.1f}%"
        assert (
            abs(above_85_pct - 5) <= tolerance
        ), f"Above 85: expected ~5%, got {above_85_pct:.1f}%"

        # Mean should be around 70 (±5)
        assert (
            65 <= mean_ci <= 75
        ), f"Mean condition index: expected ~70, got {mean_ci:.1f}"

    def test_age_does_not_exceed_life_expectancy(self):
        """Test that generated age never exceeds facility life expectancy."""
        # Test with various facilities
        for facility in FacilityLifeExpectancy:
            result = get_random_facility_data_nums(facility.title)
            assert result.age_in_years <= facility.life_expectancy, (
                f"{facility.title}: age {result.age_in_years} exceeds "
                f"life expectancy {facility.life_expectancy}"
            )

    def test_time_series_contains_current_condition(self):
        """Test that time series months dict contains the current condition index."""
        facility_title = "Data Center"
        result = get_random_facility_data_nums(facility_title)

        # The current month's condition should be in the time series
        months_data = result.time_series["months"]
        assert len(months_data) > 0

        # At least one value should be close to current condition index
        # (the current month should match exactly)
        values = list(months_data.values())
        assert result.condition_index in values or any(
            abs(v - result.condition_index) < 0.01 for v in values
        )

    def test_consistent_data_generation(self):
        """Test that multiple calls generate different but valid data."""
        facility_title = "Data Center"

        # Generate multiple facilities
        facilities = [get_random_facility_data_nums(facility_title) for _ in range(10)]

        # All should be valid
        for facility in facilities:
            assert isinstance(facility, Facility)
            assert 0 <= facility.age_in_years <= 80
            assert 1 <= facility.condition_index <= 99
            assert facility.estimated_remaining_service_life >= 0

        # They should have some variation (not all identical)
        ages = [f.age_in_years for f in facilities]
        conditions = [f.condition_index for f in facilities]

        # At least some values should be different
        assert len(set(ages)) > 1 or len(set(conditions)) > 1

    @pytest.mark.parametrize(
        "facility_title",
        [
            "Equipment Pad",  # 20 year life expectancy
            "Antenna support building",  # 30 year life expectancy
            "Data Center",  # 40 year life expectancy
            "Heating - Cooling Plant",  # 60 year life expectancy
        ],
    )
    def test_different_life_expectancies_handled_correctly(self, facility_title):
        """Test that facilities with different life expectancies are handled correctly."""
        result = get_random_facility_data_nums(facility_title)
        facility_def = FacilityLifeExpectancy.find_by_title(facility_title)

        # Age should not exceed life expectancy
        assert result.age_in_years <= facility_def.life_expectancy

        # Expected service life should match definition
        assert result.expected_service_life == facility_def.life_expectancy

        # Remaining service life should be reasonable
        assert result.estimated_remaining_service_life >= 0
        assert result.estimated_remaining_service_life <= facility_def.life_expectancy
