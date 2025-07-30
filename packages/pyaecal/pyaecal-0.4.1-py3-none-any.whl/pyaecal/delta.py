#  Copyright (c) 2017-2021 Jeorme Douay <jerome@far-out.biz>
#  All rights reserved.

import polars as pl
import logging
from .trigger import Trigger


class Delta(Trigger):
    """
    Generate Table before and after shifting
    All the columns supplied in the data for process will be used.
    At the beginning of the shift, the columns will be added '_pre',
    at the end of the shift '_post'.
    Associates each pre-trigger with the next post-trigger based on offset time and calculates time difference.
    Handles cases where post-triggers may be missing for some pre-triggers.
    """

    def __init__(self):
        super().__init__()

    def evaluate(self, data):
        """
        Evaluate the data to associate each pre-trigger with the next post-trigger and calculate time difference.
        Matches each pre-trigger with the first post-trigger that occurs after it based on offset time.
        Includes pre-triggers without matching post-triggers, with null values for post columns.

        :param data: Polars DataFrame containing the trigger signals
        :return: Polars DataFrame with merged pre/post triggers and time differences
        """
        # Get pre and post trigger results
        pre_triggers, post_triggers = super().evaluate(data)

        print(pre_triggers)
        print(post_triggers)
        
        # Initialize result DataFrame
        result = pl.DataFrame()

        # Check if pre_triggers is empty
        if pre_triggers.is_empty():
            logging.debug("No pre-triggers found in data")
            return result

        # Ensure offsets are sorted
        pre_triggers = pre_triggers.sort("offset")
        post_triggers = post_triggers.sort("offset") if not post_triggers.is_empty() else post_triggers

        # Add suffixes to distinguish pre and post columns
        pre_triggers = pre_triggers.select([
            pl.col(col).alias(f"{col}_pre") if col != "offset" else pl.col("offset").alias("offset_pre")
            for col in pre_triggers.columns
        ])

        if not post_triggers.is_empty():
            post_triggers = post_triggers.select([
                pl.col(col).alias(f"{col}_post") if col != "offset" else pl.col("offset").alias("offset_post")
                for col in post_triggers.columns
            ])

        # If no post-triggers, return pre-triggers with null post columns
        if post_triggers.is_empty():
            logging.debug("No post-triggers found; returning pre-triggers with null post columns")
            # Create null columns for post-triggers
            post_columns = {f"{col}_post": pl.lit(None) for col in pre_triggers.columns if col != "offset_pre"}
            result = pre_triggers.with_columns(**post_columns, time_diff=pl.lit(None))
            return result

        # Convert to lists for iteration to find pairs
        pre_offsets = pre_triggers["offset_pre"].to_list()
        post_offsets = post_triggers["offset_post"].to_list()

        # Find valid pairs: each pre-trigger matches with the first post-trigger where offset_post >= offset_pre
        pre_indices = []
        post_indices = []
        post_index = 0
        for pre_idx, pre_offset in enumerate(pre_offsets):
            # Find the first post_offset >= pre_offset
            while post_index < len(post_offsets) and post_offsets[post_index] < pre_offset:
                post_index += 1
            if post_index < len(post_offsets):
                pre_indices.append(pre_idx)
                post_indices.append(post_index)
                post_index += 1  # Ensure each post-trigger is used only once
            else:
                pre_indices.append(pre_idx)  # Include pre-trigger even if no post-trigger

        # Create result DataFrame
        if pre_indices:
            result = pre_triggers[pre_indices]
            
            # Add post-trigger data for matched pairs
            if post_indices:
                post_selected = post_triggers[post_indices]
                # Align post data with pre data
                post_data = pl.DataFrame({
                    col: post_selected[col] if i < len(post_indices) else pl.lit(None)
                    for i, col in enumerate(post_selected.columns)
                }, schema=post_selected.schema)
                result = result.hstack(post_data)
            else:
                # No post-triggers matched; add null columns
                post_columns = {col: pl.lit(None) for col in post_triggers.columns}
                result = result.with_columns(**post_columns)

            # Calculate time difference where post-trigger exists
            result = result.with_columns(
                pl.when(pl.col("offset_post").is_not_null())
                .then(pl.col("offset_post") - pl.col("offset_pre"))
                .otherwise(pl.lit(None))
                .alias("time_diff")
            )

        # Log results
        if result.is_empty():
            logging.debug("No pre-triggers found after pairing")
        else:
            paired_count = result.filter(pl.col("offset_post").is_not_null()).height
            unpaired_count = result.filter(pl.col("offset_post").is_null()).height
            logging.debug(f"Found {paired_count} paired pre/post trigger events, {unpaired_count} unpaired pre-triggers")

        return result