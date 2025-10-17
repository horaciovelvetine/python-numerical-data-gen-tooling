# python-numerical-data-gen-tooling

Toolkit for generating random numerical data for use as a part of (The Data Mine)[https://datamine.purdue.edu/] and specifically for the SpaceCOM J4 Project via the (Data Mine of the Rockies)[https://www.dataminerockies.org/].

Questions about this project can be directed to: [James Tillman (@horaciovelvetine)](mailto:James.Tillman@colorado.edu) [Eva Pavlik](mailto:Eva.Pavlik@colorado.edu) [Vedant Sharma](mailto:Sharm792@purdue.edu)

## Requirements:

- Generate **n** rows of numerical data of either int or float type(s), and both.

### Inputs:

- Min
- Max
- Mean
- Distribution
- Standard Deviation 

### Distribution(s)

The provided information dictates distributions in a `Percentage of data in range of time` format, in multiple places across the spreadsheet, so typical statistical distribution may not be the best approach. See the notes for the individual fields below and handle however you think works best.

### Fields:

#### Age:

Range is 0-80 in years, distributed:

- 50% 20-40 years
- 20% 10-20 years
- 20% 41 years+
- 10% less than 10 years

From: `Facility Condition Index`

#### Remaining Service Life:

- **calc:** Life Expectancy - Age = Remaining Service Life

- Life Expectancy can be found in the `key` tab of the "Simulate Data - US Space Templace" excel spreadsheet
- The `key` tab contained some life expectancy data which has been included in 2 lists containing the relevant data for convenience:
  - `./const/facility_life_expectancy.py`
  - `./const/systems_life_expectancy.py`
- Theres a note "Current date - age" in the `Facility Condition Index` tab but it was unclear what the intention of this note was. 

#### Condition Index:

Range = 1-99:

- 7% below 50
- 5% above 85,
- Remainder distributed between 50-85
- Mean value of 70

#### Condition Index (time series):

From the spreadsheet: "Calculate 10 years of prior Condition data collected at monthly intervals. Create Condition Indices regressing backwards along decay function up to a maximum (at time of initial installation) at ""99"""

- **calc**: A=P\*(1-R)^t

#### Facility Number:

Unclear if this truly a numerical piece of data or if these are known designations. For now leave this as a possible future need.