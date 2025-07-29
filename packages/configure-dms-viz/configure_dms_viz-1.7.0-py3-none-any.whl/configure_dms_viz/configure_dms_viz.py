import os
import json
import click
import pandas as pd
from pandas.api.types import is_numeric_dtype
from .pdb_utils import get_structure, check_chains, check_wildtype_residues


# Check that the mutation data is in the correct format
def format_mutation_data(mut_metric_df, metric_col, condition_col, alphabet):
    """Check that the mutation data is in the correct format.

    This data should be a pandas.DataFrame with the following columns:
    - reference_site: The site number in the reference sequence
    - wildtype: The wildtype amino acid at the site
    - mutant: The mutant amino acid at the site
    - metric_col: The metric to visualize
    - condition_col: The condition to group on if there are multiple measurements per mutation

    Parameters
    ----------
    mut_metric_df: pandas.DataFrame
        A dataframe containing site- and mutation-level data for visualization.
    metric_col: str
        The name of the column the contains the metric for visualization.
    condition_col: str
        The name of the column the contains the condition if there are multiple measurements per mutation
    alphabet: list
        A list of the amino acid names corresponding to the mutagenized residues.

    Returns
    -------
    pandas.DataFrame
        The mutation dataframe with the site column renamed to reference_site if necessary.
    """

    # Ensure that the site column is called 'reference_site' and rename if necessary
    if "reference_site" not in set(mut_metric_df.columns):
        if "site" in set(mut_metric_df.columns):
            mut_metric_df = mut_metric_df.rename(columns={"site": "reference_site"})
        else:
            raise ValueError(
                "The mutation dataframe is missing either the site or reference_site column designating reference sites."
            )

    # Check that the rest of the necessary columns are present in the mut_metric dataframe
    required_columns = {
        "reference_site",
        "wildtype",
        "mutant",
        metric_col,
    }
    if condition_col is not None:
        required_columns.add(condition_col)
    missing_mutation_columns = required_columns - set(mut_metric_df.columns)
    if missing_mutation_columns:
        raise ValueError(
            f"The following columns do not exist in the mutation dataframe: {list(missing_mutation_columns)}"
        )

    # Check that all mutant and wildtype residue names are in the provided alphabet
    mut_metric_alphabet = set(
        mut_metric_df.mutant.to_list() + mut_metric_df.wildtype.to_list()
    )
    missing_amino_acids = mut_metric_alphabet - {aa for aa in alphabet}
    if missing_amino_acids:
        raise ValueError(
            f"Some of the wildtype or mutant amino acid names are not in the provided alphabet, i.e., {missing_amino_acids}"
        )

    # Check that there is only one measurement per mutation if there isn't a condition column
    if condition_col is None:
        if mut_metric_df[["reference_site", "wildtype", "mutant"]].duplicated().any():
            raise ValueError(
                "Duplicates measurements per mutation were found in the mutation dataframe, please specify a condition column."
            )

    # Check if there are any NaN values in the metric column
    if mut_metric_df[metric_col].isna().any():
        # Echo a warning to the user
        click.secho(
            message="\nWarning: NaN values were found in the metric column. These rows will be filtered out.",
            fg="red",
        )
        # Drop the rows with NaN values in the metric column
        mut_metric_df = mut_metric_df.dropna(subset=[metric_col])

    # Group by reference_site and filter groups where all mutants are the same as wildtype
    sites_with_only_wildtype = mut_metric_df.groupby("reference_site").filter(
        lambda x: (x["mutant"] == x["wildtype"].iloc[0]).all()
    )

    # Check if there are any such sites
    if not sites_with_only_wildtype.empty:
        # Echo a warning to the user
        click.secho(
            message="\nWarning: There are sites where there are no mutations, in other words, only the wildtype residue is present in the mutation column for that site. These rows will be filtered out.",
            fg="red",
        )
        # Drop the rows where there are no mutations
        mut_metric_df = mut_metric_df[
            ~mut_metric_df["reference_site"].isin(
                sites_with_only_wildtype["reference_site"]
            )
        ]

    return mut_metric_df


# Check that the sitemap data is in the correct format
def format_sitemap_data(sitemap_df, mut_metric_df, included_chains):
    """Check that the sitemap data is in the correct format.

    This data should be a pandas.DataFrame with the following columns:
    - reference_site: (numeric or string) The site number in the reference sequence that
        corresponds to the reference site in the mutation dataframe
    - sequential_site: (numeric) The order of the site in the protein sequence and
        on the x-axis of the visualization
    - protein_site: [Optional] (numeric or string) The site number in the protein structure if
        different from the reference site. This can include insertion codes and
        therefore can be a string.

    Parameters
    ----------
    mut_metric_df: pandas.DataFrame
        A dataframe containing site- and mutation-level data for visualization.
    sitemap_df: pandas.DataFrame
        A dataframe mapping sequential sites to reference sites to protein sites.
    included_chains: list
        A list of the protein chains to include in the visualization.

    Returns
    -------
    pandas.DataFrame
    """

    # Check that required columns are present in the sitemap data
    missing_sitemap_columns = {"sequential_site", "reference_site"} - set(
        sitemap_df.columns
    )
    if missing_sitemap_columns:
        raise ValueError(
            f"The following columns do not exist in the sitemap: {list(missing_sitemap_columns)}"
        )

    # Check that the reference sites are the same between the sitemap and mut_metric dataframe
    missing_reference_sites = set(mut_metric_df.reference_site.tolist()) - set(
        sitemap_df.reference_site.tolist()
    )
    if missing_reference_sites:
        raise ValueError(
            f"There are reference sites in the mutation dataframe missing from your sitemap e.g. {list(missing_reference_sites)[0:10]}..."
        )

    # Check that the reference sites are unique for each value of sequential site
    duplicated_reference_sites = sitemap_df[sitemap_df["reference_site"].duplicated()]
    if not duplicated_reference_sites.empty:
        raise ValueError(
            f"Duplicated reference sites found: {duplicated_reference_sites['reference_site'].tolist()}"
        )

    # Check if the sequential sites are a numeric type as they need to be for ordering the x-axis
    if not is_numeric_dtype(sitemap_df["sequential_site"]):
        # Try to coerce the sequential sites into a numeric type
        try:
            sitemap_df["sequential_site"] = pd.to_numeric(sitemap_df["sequential_site"])
        except ValueError as err:
            raise ValueError(
                "The sequential_site column of the sitemap is not numeric and cannot be coerced into a numeric type."
            ) from err

    # If the protein site isn't specified, assume that it's the same as the reference site
    if "protein_site" not in sitemap_df.columns:
        click.secho(
            message="\n'protein_site' column is not present in the sitemap. Assuming that the reference sites correspond to protein sites.\n",
            fg="yellow",
        )
        sitemap_df["protein_site"] = sitemap_df["reference_site"].apply(lambda y: y)
        # Check how many of the protein sites are thrown out
        num_empty_protein_sites = (sitemap_df["protein_site"] == "").sum()
        if num_empty_protein_sites > 0.10 * len(sitemap_df):
            click.secho(
                message=f"Warning: more than 10% ({num_empty_protein_sites}) of reference sites can't be converted into protein sites. Check if the supplied reference sites are in the correct format. Otherwise, you might need to supply protein sites in another column.",
                fg="red",
            )

    # If the sitemap doesn't already have a column for chains, add it
    if "chains" not in sitemap_df.columns:
        # Add the included chains to the sitemap dataframe if there are any
        sitemap_df["chains"] = sitemap_df["protein_site"].apply(
            lambda y: included_chains
        )

    # Drop the columns that aren't needed for the visualization
    sitemap_df = sitemap_df[
        ["reference_site", "protein_site", "sequential_site", "chains"]
    ]

    # If a column is of type float, convert it to an integer
    for col in sitemap_df.columns:
        if sitemap_df[col].dtype == "float64":
            sitemap_df[col] = sitemap_df[col].astype(int)

    return sitemap_df


# Join the additional dataframes to the main dataframe
def join_additional_data(mut_metric_df, join_data):
    """Join additional dataframes to the main mutation dataframe.

    The additional dataframes should have the following columns:
    - reference_site: The site number in the reference sequence that
        corresponds to the reference site in the mutation dataframe
    - wildtype: The wildtype amino acid at the site
    - mutant: The mutant amino acid at the site

    *Note that there currently this data should apply to all site and should
    be identical between conditions. Otherwise, there will be an
    error about duplicate data.*

    Parameters
    ----------
    mut_metric_df: pandas.DataFrame
        A dataframe containing site- and mutation-level data for visualization.
    join_data: list of pandas.DataFrame
        A list of dataframes to join to the main mutation dataframe.

    Returns
    -------
    pandas.DataFrame
        The updated mut_metric_df with the joined dataframes.

    """
    for df in join_data:
        # Check that the necessary columns are present, first the reference_sites
        if "reference_site" not in set(df.columns):
            if "site" in set(df.columns):
                df.rename({"site": "reference_site"})
            else:
                raise ValueError(
                    "One of the join dataframes is missing either the site or reference_site column designating reference sites."
                )
        # Now check for the other necessary columns
        missing_join_columns = {"reference_site", "wildtype", "mutant"} - set(
            df.columns
        )
        if missing_join_columns:
            raise ValueError(
                f"The following columns do not exist in the join dataframe: {missing_join_columns}"
            )

        # Before merging, make sure that there aren't more than one measurement per merge condition
        if df[["reference_site", "wildtype", "mutant"]].duplicated().any():
            raise ValueError(
                "Duplicates measurements per mutation were found in join dataframe, merge cannot be performed"
            )

        # Before merging, remove any columns present in both dataframes
        duplicate_columns = [
            col
            for col in df.columns
            if col
            in (set(mut_metric_df.columns) - {"reference_site", "wildtype", "mutant"})
        ]
        if duplicate_columns:
            df = df.drop(duplicate_columns, axis=1)
            click.secho(
                message=f"\nWarning: duplicate column names exist between mutation dataframe and join dataframe. Dropping {duplicate_columns} from join data.\n",
                fg="red",
            )

        # Merge this dataframe with the main dataframe
        mut_metric_df = mut_metric_df.merge(
            df, on=["reference_site", "wildtype", "mutant"], how="left"
        )

        return mut_metric_df


# Check the filter columns are in the main dataframe and formatted correctly
def check_filter_columns(mut_metric_df, filter_cols):
    """Check the filter columns are in the main dataframe and formatted correctly.

    Parameters
    ----------
    mut_metric_df: pandas.DataFrame
        A dataframe containing site- and mutation-level data for visualization.
    filter_cols: dict
        A dictionary of column names and values to filter the dataframe by.

    Returns
    -------
    list of str
        The names of the filter columns to add to the dataframe.
    """
    # Get the current names of the columns
    filter_column_names = [col for col in filter_cols.keys()]

    # Make sure the filter columns are actually in the dataframe at this point
    missing_filter_columns = set(filter_column_names) - set(mut_metric_df.columns)
    if missing_filter_columns:
        raise ValueError(
            f"The filter column(s): {missing_filter_columns} are not present in the data."
        )

    # Make sure that filter columns are numeric
    for col in filter_column_names:
        try:
            pd.to_numeric(mut_metric_df[col])
        except ValueError as err:
            raise ValueError(
                f"The column {col} contains values that cannot be coerced into numbers."
            ) from err

    # Make sure that the filter columns don't have spaces in them
    for col in filter_column_names:
        if " " in col:
            raise ValueError(f"There is a space in {col}. Please remove this.")

    return filter_column_names


# Check the tooltip columns are in the main dataframe and formatted correctly
def check_tooltip_columns(mut_metric_df, tooltip_cols):
    """Check the tooltip columns are in the main dataframe and formatted correctly

    Parameters
    ----------
    mut_metric_df: pandas.DataFrame
        A dataframe containing site- and mutation-level data for visualization.
    tooltip_cols: dict
        A dictionary of column names and values use as tooltips in the visualization.

    Returns
    -------
    list of str
        The names of the tooltip columns to add to the dataframe.
    """
    # Get the current names of the columns
    tooltip_column_names = [col for col in tooltip_cols.keys()]

    # Make sure the tooltip columns are actually in the dataframe at this point
    missing_tooltip_columns = set(tooltip_column_names) - set(mut_metric_df.columns)
    if missing_tooltip_columns:
        raise ValueError(
            f"The tooltip column(s): {missing_tooltip_columns} are not present in the data."
        )

    return tooltip_column_names


def make_experiment_dictionary(
    mut_metric_df,
    metric_col,
    sitemap_df,
    structure,
    join_data=None,
    filter_cols=None,
    filter_limits=None,
    heatmap_limits=None,
    tooltip_cols=None,
    metric_name=None,
    condition_col=None,
    condition_name=None,
    included_chains="polymer",
    excluded_chains="none",
    alphabet="RKHDEQNSTYWFAILMVGPC-*",
    colors=None,
    negative_colors=None,
    check_pdb=True,
    exclude_amino_acids=None,
    description=None,
    title=None,
    floor=None,
    summary_stat=None,
):
    """Take site-level and mutation-level measurements and format into
    a dictionary that can be used to create a JSON file for the visualization.

    Parameters
    ---------
    mut_metric_df: pandas.DataFrame
        A dataframe containing site- and mutation-level data for visualization.
    metric_col: str
        The name of the column the contains the metric for visualization.
    structure: str
        An RCSB PDB ID (i.e. 6UDJ) or the path to a file with a *.pdb extension.
    sitemap_df: pandas.DataFrame or None
        A dataframe mapping sequential sites to reference sites to protein sites.
    metric_name: str or None
        Rename the metric column to this name if desired. This name shows up in the plot.
    condition_col: str or None
        The name of the column the contains the condition if there are multiple measurements per mutation.
    condition_name: str or None
        Rename or format the condition column if desired.
    join_data: list or None
        A list of pandas.dataFrames to join to the main dataframe by mutation/condition.
    filter_cols: dict or None
        A dictionary of column names and formatted names to designate as filters.
    filter_limits: dict or None
        A dictionary of the desired min and max values for each filter column slider range.
    heatmap_limits: list or None
        A list of the desired min, max, and center values for the metric to be used for the heatmap's color scale.
    tooltip_cols: dict or None
        A dictionary of column names and formatted names to designate as tooltips.
    included_chains: str or None
        If not mapping data to every chain, a space separated list of chain names (i.e. "C F M G J P").
    excluded_chains: str or None
        A space separated string of chains that should not be shown on the protein structure (i.e. "B L R").
    alphabet: str
        The amino acid labels in the order the should be displayed on the heatmap.
    colors: list or None
        A list of colors that will be used for each condition in the experiment.
    colors: list or None
        A list of colors that will be used for the negative end of the scale for each condition in the experiment.
    check_pdb: bool
        Check that the chains and wildtype residues are in the structure.
    exclude_amino_acids: list or None
        Amino acids that should be excluded from the summary statistics.
    description: str or None
        A short description of the dataset to show in the tool.
    title: str or None
        A short title to appear above the plot.
    floor: bool or None
        If True, the floor of the metric will be set to 0 by default.
    summary_stat: str or None
        The default summary statistic to display on the plot.

    Returns
    -------
    dict
        A dictionary containing a single dataset for visualization to convert into a JSON file.
    """

    # Make sure the chain names are valid and not just whitespace
    if not included_chains.strip():
        included_chains = "polymer"
    if not excluded_chains.strip():
        excluded_chains = "none"

    # Make sure that there is no overlap between the included and excluded chains
    if set(included_chains.split(" ")) & set(excluded_chains.split(" ")):
        raise ValueError(
            "The included and excluded chains cannot have any overlap. Please remove the overlapping chains."
        )

    # Check that the necessary columns are present in the mut_metric dataframe and format
    mut_metric_df = format_mutation_data(
        mut_metric_df, metric_col, condition_col, alphabet
    )

    # If there is no sitemap dataframe, create a default one
    if sitemap_df is None:
        click.secho(
            message="Warning: No sitemap dataframe was provided. Creating a default sitemap.\n If no site map is provided, the reference sites will be sorted but may appear out of order.",
            fg="yellow",
        )
        reference_sites = sorted(list(set(mut_metric_df["reference_site"].to_list())))
        sitemap_df = pd.DataFrame(
            {
                "reference_site": reference_sites,
                "sequential_site": range(1, len(reference_sites) + 1),
            }
        )

    # Check that the necessary columns are present in the sitemap dataframe and format
    sitemap_df = format_sitemap_data(sitemap_df, mut_metric_df, included_chains)

    # Keep track of the required columns to cut down on the final total data size
    cols_to_keep = ["reference_site", "wildtype", "mutant", metric_col]

    # Join the additional data to the main dataframe if there is any
    if join_data:
        mut_metric_df = join_additional_data(mut_metric_df, join_data)

    # Add the condition column to the required columns if it's not None
    if condition_col:
        cols_to_keep.append(condition_col)

    # Check that the heatmap limits are in the correct format
    if heatmap_limits:
        # Check that the values are all able to be coerced into numbers
        for value in heatmap_limits:
            try:
                pd.to_numeric(value)
            except ValueError as err:
                raise ValueError(
                    f"The heatmap limit '{value}' cannot be coerced into a number."
                ) from err
        # Only the center of the scale is provided
        if len(heatmap_limits) == 1:
            click.secho(
                message="One value was provided for heatmap limits, this will be the center value of the scale.\n",
                fg="green",
            )
        # The min and max are provided
        elif len(heatmap_limits) == 2:
            click.secho(
                message="Two values were provided for heatmap limits, these will be the min and max of the scale.\n",
                fg="green",
            )
            # Check that the values are in the correct order
            if heatmap_limits[0] > heatmap_limits[1]:
                raise ValueError(
                    "The heatmap limits are not specified correctly. The min value must be less than the max value."
                )
        # The min, center, and max are provided
        elif len(heatmap_limits) == 3:
            click.secho(
                message="Three values were provided for heatmap limits, these will be the min, center, and max of the scale.\n",
                fg="green",
            )
            # Check that the values are in the correct order
            if not heatmap_limits[0] < heatmap_limits[1] < heatmap_limits[2]:
                raise ValueError(
                    "The heatmap limits are not specified correctly. The min value must be less than the max value and the center value must be in between."
                )
        else:
            raise ValueError(
                "The heatmap limits must be a list of one, two, or three values."
            )

    # Add the filter columns to the required columns
    if filter_cols:
        cols = check_filter_columns(mut_metric_df, filter_cols)
        cols_to_keep += cols
        if filter_limits:
            filter_limits_cols = [col for col in filter_limits.keys()]
            # Check that the columns are in the filter columns
            missing_filter_limits_cols = set(filter_limits_cols) - set(cols)
            if missing_filter_limits_cols:
                raise ValueError(
                    f"The following columns do not exist in the filter columns: {list(missing_filter_limits_cols)}"
                )
            for limit_col, values in filter_limits.items():
                # Check that the ranges specified are numeric
                for value in values:
                    try:
                        pd.to_numeric(value)
                    except ValueError as err:
                        raise ValueError(
                            f"The '{limit_col}' filter limit or default value '{value}' cannot be coerced into a number."
                        ) from err

                # If there are two values, then these are just the min and max
                if len(values) == 2:
                    click.secho(
                        message="Warning: you've only provided a min and max for the slides. It's HIGHLY recommended that you provide a default value as well.",
                        fg="red",
                    )
                    # Check that the values are in the correct order
                    if values[0] > values[2]:
                        raise ValueError(
                            f"The '{limit_col}' filter limits are not specified correctly. The min value must be less than the max value."
                        )
                # If there are three values, the this is the min, default, and max
                elif len(values) == 3:
                    # Check that the values are in the correct order
                    if values[0] >= values[1] >= values[2]:
                        raise ValueError(
                            f"The '{limit_col}' filter limits are not specified correctly. The min value must be less than the max value and the default must be in between."
                        )
                # If the length isn't 2 or 3, then raise an error
                else:
                    raise ValueError(
                        f"The '{limit_col}' filter limits are not specified correctly. Please specify both the min and max values."
                    )

                # Check that the specified limits are within the range of the data
                if values[0] < mut_metric_df[limit_col].min():
                    # If the min is less than the min of the data, set it to the min of the data
                    click.secho(
                        message=f"Warning: The '{limit_col}' filter limit '{values[0]}' is less than the minimum value of {mut_metric_df[limit_col].min()}. Setting the min value to {mut_metric_df[limit_col].min()}.\n",
                        fg="red",
                    )
                    filter_limits[limit_col][0] = mut_metric_df[limit_col].min()
                if values[-1] > mut_metric_df[limit_col].max():
                    # If the max is greater than the max of the data, set it to the max of the data
                    click.secho(
                        message=f"Warning: The '{limit_col}' filter limit '{values[1]}' is greater than the maximum value of {mut_metric_df[limit_col].max()}. Setting the max value to {mut_metric_df[limit_col].max()}.\n",
                        fg="red",
                    )
                    filter_limits[limit_col][1] = mut_metric_df[limit_col].max()
        else:
            # Warn the user that it's recommended that they provide filter limits
            click.secho(
                message="Warning: It's highly recommended that you provide filter limits and a default value for the sliders.\n",
                fg="red",
            )
    # Add the tooltip columns to required columns
    if tooltip_cols:
        cols_to_keep += check_tooltip_columns(mut_metric_df, tooltip_cols)

    # If there are excluded amino acids, check that they're in the alphabet
    if exclude_amino_acids:
        # Strip out the white space
        exclude_amino_acids = [aa.strip() for aa in exclude_amino_acids]
        missing_amino_acids = set(exclude_amino_acids) - set(alphabet)
        if missing_amino_acids:
            raise ValueError(
                f"Some of the excluded amino acids are not in the provided alphabet, i.e., {missing_amino_acids}"
            )

    # Subset the mutation dataframe down to the required columns
    mut_metric_df = mut_metric_df[list(set(cols_to_keep))]

    # Determine whether the structure is a PDB ID or a local file
    _, ext = os.path.splitext(structure)

    if ext == ".pdb":
        # PDB is local, load it in as a string
        with open(structure, "r") as f:
            pdb = f.read()
    else:
        pdb = structure

    # Get a list of the conditions and map these to the colors
    if colors is None:
        colors = ["#0072B2", "#CC79A7", "#4C3549", "#009E73"]
    if condition_col:
        conditions = sorted(list(set(mut_metric_df[condition_col])))
        if len(conditions) > len(colors):
            raise ValueError(
                f"There are {len(conditions)} conditions, but only {len(colors)} color(s) specified. Please specify more colors."
            )
        for color in colors:
            # Check that the colors are valid HEX format
            if not color.startswith("#") or len(color) != 7:
                raise ValueError(
                    f"The color '{color}' is not valid. Please use a hex format color code."
                )
        condition_colors = {
            condition: colors[i] for i, condition in enumerate(conditions)
        }
    else:
        conditions = []
        condition_colors = {"default": colors[0]}

    # Format the negative colors for each condition
    if negative_colors is not None:
        if condition_col:
            if len(negative_colors) != len(colors):
                raise ValueError(
                    f"There are {len(conditions)} conditions, but only {len(negative_colors)} negative color(s) specified. Please specify more colors."
                )
            for color in negative_colors:
                # Check that the colors are valid HEX format
                if not color.startswith("#") or len(color) != 7:
                    raise ValueError(
                        f"The negative color '{color}' is not valid. Please use a hex format color code."
                    )
            negative_condition_colors = {
                condition: negative_colors[i] for i, condition in enumerate(conditions)
            }
        else:
            negative_condition_colors = {"default": negative_colors[0]}
    else:
        negative_condition_colors = None

    # Rename the metric column to the metric name
    if metric_name:
        mut_metric_df = mut_metric_df.rename(columns={metric_col: metric_name})
        metric_col = metric_name

    # Rename the condition column to the condition name
    if condition_name:
        mut_metric_df = mut_metric_df.rename(columns={condition_col: condition_name})
        condition_col = condition_name

    # Check that the floor is a valid value
    if floor is not None:
        if not isinstance(floor, bool):
            raise ValueError("The floor value must be a boolean.")

    # Check that the summary statistic is a valid value
    if summary_stat is not None:
        if summary_stat not in ["sum", "mean", "median", "max", "min"]:
            raise ValueError(
                "The summary statistic must be one of 'sum', 'mean', 'median', 'max', or 'min'."
            )

    # Check that the chains and wildtype residues are in the structure
    if check_pdb:
        if included_chains != "polymer":
            check_chains(get_structure(structure), included_chains.split(" "))
        # Check that the wildtype residues are in the structure
        perc_matching, perc_missing, count_matching, count_missing = (
            check_wildtype_residues(
                get_structure(structure), mut_metric_df, sitemap_df, excluded_chains
            )
        )
        # Alert the user about the missing and matching residues
        if perc_matching < 0.5:
            color = "red"
            message = f"Warning: Fewer than {perc_matching*100:.2F}% {count_matching} of the wildtype residues in the data match the corresponding residues in the structure."
        else:
            color = "yellow"
            message = f"About {perc_matching*100:.2F}% {count_matching} of the wildtype residues in the data match the corresponding residues in the structure."
        click.secho(message=message, fg=color)
        if perc_missing >= 0.5:
            color = "red"
            message = f"Warning: {perc_missing*100:.2F}% {count_missing} of the data sites are missing from the structure."
        else:
            color = "yellow"
            message = f"About {perc_missing*100:.2F}% {count_missing} of the data sites are missing from the structure."
        click.secho(message=message, fg=color)

    # Make a dictionary holding the experiment data
    experiment_dict = {
        "mut_metric_df": json.loads(mut_metric_df.to_json(orient="records")),
        "sitemap": sitemap_df.set_index("reference_site").to_dict(orient="index"),
        "metric_col": metric_col,
        "condition_col": condition_col,
        "conditions": conditions,
        "condition_colors": condition_colors,
        "negative_condition_colors": negative_condition_colors,
        "alphabet": [aa for aa in alphabet],
        "pdb": pdb,
        "dataChains": included_chains.split(" "),
        "excludeChains": excluded_chains.split(" "),
        "filter_cols": filter_cols,
        "filter_limits": filter_limits,
        "heatmap_limits": heatmap_limits,
        "tooltip_cols": tooltip_cols,
        "excludedAminoAcids": exclude_amino_acids,
        "description": description,
        "title": title,
        "floor": floor,
        "summary_stat": summary_stat,
    }

    return experiment_dict


# ============================== Command Line Interface ============================== #


class ListParamType(click.ParamType):
    name = "list"

    def convert(self, value, param, ctx):
        try:
            if isinstance(value, list):
                return value
            elif isinstance(value, str):
                return [x.strip() for x in value.split(",")]
        except ValueError:
            self.fail(f"{value} is not a valid list", param, ctx)


class DictParamType(click.ParamType):
    name = "dict"

    def convert(self, value, param, ctx):
        try:
            return json.loads(value.replace("'", '"'))
        except ValueError:
            self.fail(f"{value} is not a valid dictionary", param, ctx)


@click.group()
def cli():
    pass


@cli.command("format")
@click.option(
    "--input",
    type=click.Path(exists=True),
    required=True,
    help="Path to a csv with site- and mutation-level data to visualize on a protein structure.",
)
@click.option(
    "--metric",
    type=str,
    required=True,
    help="The name of the column that contains the metric for visualization.",
)
@click.option(
    "--structure",
    type=str,
    required=True,
    help="An RCSB PDB ID (i.e. 6UDJ) or the path to a file with a *.pdb extension.",
)
@click.option(
    "--sitemap",
    type=click.Path(exists=True),
    required=False,
    default=None,
    help="Path to a csv with a mapping of sequential sites to reference sites to protein sites.",
)
@click.option(
    "--name",
    type=str,
    required=True,
    help="The name of the experiment. This will be used when concatenating multiple experiments.",
)
@click.option(
    "--output",
    type=click.Path(),
    required=True,
    help="Path to save the *.json file containing the data for the visualization tool.",
)
@click.option(
    "--metric-name",
    type=str,
    required=False,
    default=None,
    help="Optionally, the name that should show up for your metric in the plot.",
)
@click.option(
    "--condition",
    type=str,
    required=False,
    default=None,
    help="The name of the column that contains the condition to group on if there are multiple measurements per experiment.",
)
@click.option(
    "--condition-name",
    type=str,
    required=False,
    default=None,
    help="Optionally, the name that should show up for your condition column in the plot.",
)
@click.option(
    "--filter-cols",
    type=DictParamType(),
    required=False,
    default=None,
    help="Optionally, a space separated list of columns to use as filters in the visualization. Example: \"{'effect': 'Functional Effect', 'times_seen': 'Times Seen'}\"",
)
@click.option(
    "--filter-limits",
    type=DictParamType(),
    required=False,
    default=None,
    help="Optionally, a space separated list of columns to use as filters in the visualization. Example: \"{'effect': [min, max], 'times_seen': [min, max]}\"",
)
@click.option(
    "--heatmap-limits",
    type=ListParamType(),
    required=False,
    default=None,
    help='Optionally, a list of the min, center, and max values for the metric to be used for the heatmap\'s color scale. Example: "[min, center, max]"',
)
@click.option(
    "--tooltip-cols",
    type=DictParamType(),
    required=False,
    default=None,
    help="Optionally, a space separated list of columns to use as tooltips in the visualization. Example: \"{'times_seen': '# Obsv', 'effect': 'Func Eff.'}\"",
)
@click.option(
    "--join-data",
    type=ListParamType(),
    required=False,
    default=None,
    help='Optionally, a csv file with additional data to join to the mutation data. Example: "path/to/join_data.csv, path/to/join_data2.csv"',
)
@click.option(
    "--included-chains",
    type=str,
    required=False,
    default="polymer",
    help='Optionally, a space separated list of chains to include in the visualization. Example: "A B C"',
)
@click.option(
    "--excluded-chains",
    type=str,
    required=False,
    default="none",
    help='A space separated list of chains to exclude from the visualization. Example: "A B C"',
)
@click.option(
    "--alphabet",
    type=str,
    required=False,
    default="RKHDEQNSTYWFAILMVGPC-*",
    help="A string of amino acids to use as the alphabet for the visualization. The order is the order in which the amino acids will be displayed on the heatmap.",
)
@click.option(
    "--colors",
    type=ListParamType(),
    required=False,
    default=["#0072B2", "#CC79A7", "#4C3549", "#009E73"],
    help='A list of colors to use for the conditions in the visualization. Example: "#0072B2, #CC79A7, #4C3549, #009E73"',
)
@click.option(
    "--negative-colors",
    type=ListParamType(),
    required=False,
    default=None,
    help="A list of colors to use for the negative end of the scale for each condition in the visualization. If not provided, it will be the inverse of the positive colors.",
)
@click.option(
    "--check-pdb",
    type=bool,
    required=False,
    default=True,
    help="Whether to report summary statistics on how wiltype residues and chains line up with the provided structure",
)
@click.option(
    "--exclude-amino-acids",
    type=ListParamType(),
    required=False,
    default=None,
    help="Amino acids that should be excluded from the summary statistics",
)
@click.option(
    "--description",
    type=str,
    required=False,
    default=None,
    help="Add a short description of the dataset to show in the tool.",
)
@click.option(
    "--title",
    type=str,
    required=False,
    default=None,
    help="A short title to appear above the plot.",
)
@click.option(
    "--floor",
    type=bool,
    required=False,
    default=None,
    help="If True, the floor of the metric will be set to 0 by default.",
)
@click.option(
    "--summary-stat",
    type=str,
    required=False,
    default=None,
    help="The default summary statistic to display on the plot.",
)
def format(
    input,
    sitemap,
    metric,
    condition,
    structure,
    name,
    output,
    metric_name,
    condition_name,
    filter_cols,
    filter_limits,
    heatmap_limits,
    tooltip_cols,
    join_data,
    included_chains,
    excluded_chains,
    alphabet,
    colors,
    negative_colors,
    check_pdb,
    exclude_amino_acids,
    description,
    title,
    floor,
    summary_stat,
):
    """Command line interface for creating a JSON file for visualizing protein data"""
    click.secho(
        message=f"\nFormatting data for visualization using the '{metric}' column from '{input}'...",
        fg="green",
    )

    # Read in the main mutation data
    mut_metric_df = pd.read_csv(input)

    # Split the list of join data files and read them in as a list
    if join_data:
        join_data_dfs = [pd.read_csv(file) for file in join_data]
        click.secho(
            message=f"\nJoining data from {len(join_data)} dataframe.", fg="green"
        )
    else:
        join_data_dfs = None

    # Read in the sitemap data
    if sitemap is not None:
        sitemap_df = pd.read_csv(sitemap)
        click.secho(message=f"\nUsing sitemap from '{sitemap}'.", fg="green")
    else:
        sitemap_df = None

    # Create the dictionary to save as a json
    experiment_dict = make_experiment_dictionary(
        mut_metric_df,
        metric,
        sitemap_df,
        structure,
        join_data_dfs,
        filter_cols,
        filter_limits,
        heatmap_limits,
        tooltip_cols,
        metric_name,
        condition,
        condition_name,
        included_chains,
        excluded_chains,
        alphabet,
        colors,
        negative_colors,
        check_pdb,
        exclude_amino_acids,
        description,
        title,
        floor,
        summary_stat,
    )

    # Write the dictionary to a json file
    with open(output, "w") as f:
        json.dump({name: experiment_dict}, f, sort_keys=True)

    click.secho(
        message=f"\nSuccess! The visualization JSON was written to '{output}'",
        fg="green",
    )


# Register this function to the main `cli` command group
@cli.command("join")
@click.option(
    "--input",
    type=ListParamType(),
    required=True,
    help="List of JSON files to be joined. Example: 'path/to/file1.json, path/to/file2.json'",
)
@click.option(
    "--output",
    type=click.Path(),
    required=True,
    help="Path to save the combined JSON file.",
)
@click.option(
    "--description",
    type=click.Path(exists=True, readable=True, file_okay=True),
    help="Path to the markdown file to include as a global description.",
    required=False,
)
def join_command(input, output, description):
    """Join command that combines multiple JSON specification files into one."""

    # Initialize an empty dictionary to store the combined data
    combined_data = {}

    # Handle markdown description
    if description:
        # Ensure that the file has a .md extension
        if not description.endswith(".md"):
            click.secho(
                "The description file is not a markdown file. Ensure it has a .md extension.",
                fg="red",
            )
            return

        try:
            with open(description, "r") as md_file:
                markdown_content = md_file.read()
                combined_data["markdown_description"] = markdown_content
        except Exception as e:
            click.secho(
                f"Failed to read description markdown file. Error: {str(e)}", fg="red"
            )
            return

    for file_path in input:
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                combined_data.update(data)
        except Exception as e:
            click.secho(
                f"Failed to process file {file_path}. Error: {str(e)}", fg="red"
            )
            return

    # Raise an error if names of the datasets aren't unique
    combined_data_keys = list(combined_data.keys())
    if len(combined_data_keys) != len(set(combined_data_keys)):
        raise ValueError("Names of the datasets are not unique.")

    try:
        # Write the combined data to the specified output file
        with open(output, "w") as f:
            json.dump(combined_data, f, sort_keys=True)
    except Exception as e:
        click.secho(f"Failed to write to output file. Error: {str(e)}", fg="red")
        return

    click.secho(
        message=f"\nSuccess! {len(input)} JSON files were merged and saved to '{output}'",
        fg="green",
    )
