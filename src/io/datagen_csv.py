import os
import pandas as pd
import random
import json
from datetime import datetime

from main import get_random_facility_data_nums
from const.facility_life_expectancy import FacilityLifeExpectancy


# Generate N random facilities: return DataFrame
def gen_facility_set(n: int = 100) -> pd.DataFrame:
    facilities = []
    facility_names = [f.title for f in FacilityLifeExpectancy]


    # Current issue I'm having is with the time series field which is a list of dicts
    # I feel like I need to convert that to a JSON string for proper CSV storage
    # IDK if pandas has built-in support for that or not
    for _ in range(n):
        title = random.choice(facility_names)
        facility_obj = get_random_facility_data_nums(title)
        facility_dict = facility_obj.to_dict()

        # Convert the time series list/dict → JSON string for CSV storage
        facility_dict["condition_time_series"] = json.dumps(
            facility_dict.pop("time_series")
        )

        facilities.append(facility_dict)

    return pd.DataFrame(facilities)

def set_save_csv(
    n: int = 100,
    folder: str = "outputs",
    filename: str | None = None,
    append: bool = True,
):
    """
    Generate facility data and save to a CSV.
    - If append=True then append to persistent CSV.
    - If append=False then create a new timestamped CSV.

    Args:
        n: number of rows to generate
        folder: output directory
        filename: the base CSV filename (ignored if append=False)
        append: whether to append or create timestamped file
    """

    os.makedirs(folder, exist_ok=True)

    # If append=False → create timestamped new file like your original version
    if not append:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        final_filename = filename or f"spacecom_facility_data_{timestamp}.csv"
    else:
        # Append mode uses stable filename
        final_filename = filename or "spacecom_facility_data.csv"

    filepath = os.path.join(folder, final_filename)

    # Generate batch of facility rows
    df = gen_facility_set(n)

    # Check if file exists to decide whether to write header
    file_exists = os.path.isfile(filepath)

    df.to_csv(
        filepath,
        mode="a" if append else "w",
        index=False,
        header=not (append and file_exists),
    )

    print(
        f"{'Appended' if append else 'Generated'} {n} facility records → {filepath}"
    )

    return filepath

if __name__ == "__main__":
    # Default: 100 rows to CSV
    set_save_csv(n=100, append=True)
