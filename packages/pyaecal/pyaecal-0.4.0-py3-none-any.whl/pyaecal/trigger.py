from .function import Function
import polars as pl
import logging

class Trigger(Function):
    def __init__(self):
        super().__init__()
        self.signals = []
        self.trigger_pre = ""
        self.pre_up = True
        self.trigger_post = ""
        self.post_up = True

    def set_trigger_pre(self, name, up=True):
        self.trigger_pre = name
        self.pre_up = up

    def set_trigger_post(self, name, up=True):
        self.trigger_post = name
        self.post_up = up

    def evaluate(self, data):
        """
        Evaluate the data to return two DataFrames:
        - One for points where trigger_pre changes according to pre_up (if set).
        - One for points where trigger_post changes according to post_up (if set).

        :param data: Polars DataFrame containing the trigger signals
        :return: Tuple of (pre_triggers_df, post_triggers_df) where each is a Polars DataFrame
        """
        pre_result = pl.DataFrame()
        post_result = pl.DataFrame()

        # Process trigger_pre if set
        if self.trigger_pre:
            if self.trigger_pre not in data.columns:
                logging.error(f"Trigger signal {self.trigger_pre} not found in data")
            else:
                data = self.__change(self.trigger_pre, data)
                if self.pre_up:
                    pre_condition = (
                        pl.col(f"{self.trigger_pre}_mod") > 0
                    )
                else:
                    pre_condition = (
                        pl.col(f"{self.trigger_pre}_mod") < 0
                    )
                pre_result = data.filter(pre_condition)
                pre_result = pre_result.drop([f"{self.trigger_pre}_mod"])
                if pre_result.is_empty():
                    logging.debug(f"No points found for trigger_pre ({self.trigger_pre})")

        # Process trigger_post if set
        if self.trigger_post:
            if self.trigger_post not in data.columns:
                logging.error(f"Trigger signal {self.trigger_post} not found in data")
            else:
                data = self.__change(self.trigger_post, data)
                if self.post_up:
                    post_condition = (
                        pl.col(f"{self.trigger_post}_mod") > 0
                    )
                else:
                    post_condition = (
                        pl.col(f"{self.trigger_post}_mod") < 0
                    )
                post_result = data.filter(post_condition)
                post_result = post_result.drop([f"{self.trigger_post}_mod"])
                if post_result.is_empty():
                    logging.debug(f"No points found for trigger_post ({self.trigger_post})")

        if not self.trigger_pre and not self.trigger_post:
            logging.debug("No triggers set (trigger_pre or trigger_post required)")

        return pre_result, post_result

    def __change(self, name, data):
        """
        Compute the change (difference) in the signal to detect transitions.

        :param name: Name of the signal column
        :param data: Polars DataFrame
        :return: DataFrame with an additional column for the signal change
        """
        # Compute the difference to detect changes
        data = data.with_columns(
            #(pl.col(name).shift(-1) - pl.col(name)).alias(f"{name}_mod")
            pl.col(name).cast(pl.Int32).sub(pl.col(name).shift(1).cast(pl.Int32)).alias(f"{name}_mod"),
            #(pl.col(name).shift(1) -pl.col(name)).cast(pl.Int32).alias(f"{name}_mod")
        )
        # Remove rows with NaN in the _mod column
        data = data.filter(pl.col(f"{name}_mod").is_not_null())
        return data