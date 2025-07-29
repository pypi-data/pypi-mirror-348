# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

import pandas as pd
from IPython.display import display
from itables.widget import ITable


def display_table(df: pd.DataFrame):
    """
    Function to display the dataframe
    """

    try:
        dataframe_table = ITable(
            df=df,
            caption="Records",
            buttons=[{"extend": "csvHtml5", "text": "Download"}],
            classes="display nowrap compact violations_table",
            options={
                "columnDefs": [
                    # Enable search on all columns
                    {"searchable": True, "targets": "_all"},
                    # Enable sorting on all columns
                    {"orderable": True, "targets": "_all"},
                ],
            }
        )

        # Display table
        display(dataframe_table)
    except Exception as e:
        raise Exception(f"Failed to display dataframe table. Reason: {e}")


def display_message_with_frame(message: str, frame_width: int = 80, frame_char: str = '='):
    frame_border = frame_char*frame_width
    print(f"\n{frame_border}\n{message}\n{frame_border}\n")
