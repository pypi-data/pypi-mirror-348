# -*- coding: utf-8 -*-
"""
Consolidated on Mon May 19 14:07:09 2025
This is the package with the wimby_jobcration model. This model estimates wind
farm job creation across all project stages using publicly available data and
models. The model was developed by Sam Klap in the framework of his master
thesis at Utrecht University and D2.9. of the Horizon Europe project WIMBY.
The main python implementation was performed by Andrei del Villar for D2.10, 
and Luis Ramirez Camargo made the necesary changes and additions so it could
be packaged.  
@author: Andrei del Villar, Luis Ramirez Camargo
"""


import pandas as pd


# Function to calculate statistics
def calculate_job_creation_statistics(input_data_str):
    """
    Calculate statistics for job creation by life stage and location type.
    Excludes rows with 'Derived from other sources = yes'.
    """
    input_data = pd.read_csv(input_data_str)
    input_data.columns = input_data.columns.str.strip()
    # Filter the data
    filtered_df = input_data[
        input_data["Derived from other sources"].str.lower() != "yes"
    ]

    # Initialize results dictionary
    stats = {}

    # Define job types and stages
    job_types = ["Direct", "Indirect", "Induced", "Total1"]
    life_stages = [
        "Development",
        "Construction",
        "Manufacturing",
        "O&M",
        "Decommissioning",
    ]

    # Calculate statistics
    for stage in life_stages:
        stage_data = filtered_df[filtered_df["Stage"] == stage]
        stats[stage] = {}
        for job in job_types:
            if job in stage_data.columns:
                column = pd.to_numeric(stage_data[job], errors="coerce")
                stats[stage][job] = {
                    "Minimum": column.min(),
                    "Maximum": column.max(),
                    "Mean": column.mean(),
                    "Median": column.median(),
                    "Sample Std Dev": column.std(ddof=1),
                }

    return stats


# This is the function 2 of deliverable D2.10 and the recomended to use in
# the WIMBY interactive map
def calculate_employment_factors_with_regression(
    turbine_capacity, onshore_offshore, statistics, country, number_of_turbines
):
    """
    Calculate job creation for a wind farm using regression results for direct
    jobs and mean values for indirect and induced jobs.
    Adds total row and columns for national/international classification and
    share of total jobs.
    Takes into account the number of turbines to scale the results.

    turbine_capacity: float value in MW installed capacity
    onshore_offshore: string  'onshore' or 'ofshore'
    statistics: data frame resulting from calculate_job_creation_statistics
    country: string ISO 2 NUTS1
    number_of_turbines: integer with the number of turbines in the farm
    """

    # Define regression equations
    def ef_construction(OS, EU=1):
        return 9.46 - (3.65 * OS) - (4.07 * EU)

    def ef_manufacturing(OS, EU=1):
        return 13.37 - (9.50 * OS)

    def ef_om(OS, TC, EU=1):
        return 19.38 + (0.92 * TC) - (15.74 * EU)

    def ef_decommissioning(OS, EU=1):
        return 2.82 - (2.11 * OS)

    # Initialize result dictionary
    employment_factors = {
        "Life Stage": [],
        "Direct Jobs": [],
        "Indirect Jobs": [],
        "Induced Jobs": [],
        "Total": [],
        "National/International": [],
        "Share (%)": [],
    }

    life_stages = [
        "Development",
        "Construction",
        "Manufacturing",
        "O&M",
        "Decommissioning",
    ]
    OS = 1 if onshore_offshore.lower() == "onshore" else 0

    # Classify countries with national manufacturing
    local_manufacturing_countries = ["DE", "ES", "DK", "PT", "IT", "UK", "PL"]

    # Iterate through stages
    for stage in life_stages:
        if stage not in statistics:
            print(f"No statistics available for stage: {stage}")
            continue

        stage_stats = statistics[stage]

        # Calculate direct jobs using regression or mean
        if stage == "Development":
            direct_jobs = stage_stats["Direct"][
                "Mean"
            ]  # No regression, use mean
        elif stage == "Construction":
            direct_jobs = ef_construction(OS)  # Regression for construction
        elif stage == "Manufacturing":
            direct_jobs = ef_manufacturing(OS)  # Regression for manufacturing
        elif stage == "O&M":
            direct_jobs = ef_om(OS, turbine_capacity)  # Regression for O&M
        elif stage == "Decommissioning":
            direct_jobs = ef_decommissioning(
                OS
            )  # Regression for decommissioning

        # Multiply direct jobs by the number of turbines
        direct_jobs *= number_of_turbines

        # Use mean for indirect and induced jobs
        indirect_jobs = stage_stats["Indirect"]["Mean"] * number_of_turbines
        induced_jobs = stage_stats["Induced"]["Mean"] * number_of_turbines

        # Calculate total jobs
        total_jobs = direct_jobs + indirect_jobs + induced_jobs

        # Determine National or International classification
        if (
            stage == "Manufacturing"
            and country not in local_manufacturing_countries
        ):
            national_or_international = "International"
        else:
            national_or_international = "National"

        # Append to results
        employment_factors["Life Stage"].append(stage)
        employment_factors["Direct Jobs"].append(direct_jobs)
        employment_factors["Indirect Jobs"].append(indirect_jobs)
        employment_factors["Induced Jobs"].append(induced_jobs)
        employment_factors["Total"].append(total_jobs)
        employment_factors["National/International"].append(
            national_or_international
        )
        employment_factors["Share (%)"].append(0)  # Placeholder, updated later

    # Calculate shares for each life stage
    total_jobs_overall = sum(employment_factors["Total"])
    employment_factors["Share (%)"] = [
        (total / total_jobs_overall) * 100 if total_jobs_overall > 0 else 0
        for total in employment_factors["Total"]
    ]

    # Add a row for totals
    total_row = {
        "Life Stage": "Total",
        "Direct Jobs": sum(employment_factors["Direct Jobs"]),
        "Indirect Jobs": sum(employment_factors["Indirect Jobs"]),
        "Induced Jobs": sum(employment_factors["Induced Jobs"]),
        "Total": sum(employment_factors["Total"]),
        "National/International": None,
        "Share (%)": 100.0,
    }

    # Convert results to DataFrame
    result_df = pd.DataFrame(employment_factors)
    result_df = pd.concat(
        [result_df, pd.DataFrame([total_row])], ignore_index=True
    )

    return result_df
