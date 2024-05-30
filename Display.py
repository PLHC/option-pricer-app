import pandas as pd
import streamlit as st


class ComputedPrices:
    def __init__(self,
                 date,
                 row_id,
                 input_variables,
                 bs_pricer_output,
                 heatmaps_serialized):
        self.date = date
        self.row_id = row_id
        self.volatility = input_variables.volatility
        self.underlying_price = input_variables.underlying_price
        self.exercise_price = input_variables.exercise_price
        self.time_to_expiration = input_variables.time_to_expiration
        self.annual_interest_rate = input_variables.annual_interest_rate
        self.call_price = bs_pricer_output.call_price
        self.put_price = bs_pricer_output.put_price
        self.call_heatmap = heatmaps_serialized.call_heatmap
        self.put_heatmap = heatmaps_serialized.put_heatmap


def prices_and_heatmaps(col_call, col_put, col_inputs, cp):
    with col_call:
        st.header("Call price: {0:.2f}".format(cp.call_price))
        st.pyplot(cp.call_heatmap)

    with col_put:
        st.header("Put price: {0:.2f}".format(cp.put_price))
        st.pyplot(cp.put_heatmap)

    with col_inputs:
        st.subheader("Currently displayed: ")
        st.markdown("Computed on: {0}".format(cp.date))
        current_display_table = pd.DataFrame(index=['Volatility',
                                                    'Underlying price',
                                                    'Exercise price',
                                                    'Time to expiration',
                                                    'Interest rate'],
                                             data=["{0:.2f}%".format(cp.volatility),
                                                   "{0:.2f}".format(cp.underlying_price),
                                                   "{0:.2f}".format(cp.exercise_price),
                                                   "{0:.2f} days".format(cp.time_to_expiration),
                                                   "{0:.2f}%".format(cp.annual_interest_rate)]
                                             )

        st.markdown(current_display_table.style.hide(axis="columns").to_html(), unsafe_allow_html=True)


__all__ = ["ComputedPrices", "prices_and_heatmaps"]
