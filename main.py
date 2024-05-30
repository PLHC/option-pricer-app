import streamlit as st
import Buttons_actions
import DB_interface

# App display options
st.set_page_config(
    page_title="Option Pricer",
    page_icon=":signal_strength:",
    layout="wide"
)
st.title("Black Scholes Option Pricer")
col_inputs, col_buttons, col_call, col_put = st.columns([15, 7, 30, 30], gap='large')

# Inputs to model
with col_inputs:
    st.number_input("Volatility (in percent)", key="volatility", min_value=0.01, step=1.0)
    st.number_input("Underlying price", key="underlying_price", min_value=0.0, step=1.0)
    st.number_input("Exercise price", key="exercise_price", min_value=0.0, step=1.0)
    st.number_input("Time to expiration (in days)", key="time_to_expiration", min_value=0.01, step=1.0)
    st.number_input("Annual interest rate (in percent)", key="annual_interest_rate", step=1.0)

# Initialization of DB id pointers and display of last computation at start
if 'id_pointer' not in st.session_state:
    st.session_state.id_pointer = DB_interface.max_id()
    st.session_state.latest_computation_id = st.session_state.id_pointer
    if st.session_state.id_pointer != 0:
        Buttons_actions.recall_values(st.session_state, 'next', col_call, col_put, col_inputs)

# Button commands
with (col_buttons):
    if st.button("Compute"):
        Buttons_actions.compute_or_reload_latest(st.session_state, col_call, col_put, col_inputs)

    if st.session_state.id_pointer != 0 and st.button("Previous"):
        Buttons_actions.recall_values(st.session_state, 'prev', col_call, col_put, col_inputs)

    if st.session_state.id_pointer != 0 and st.button("Next"):
        Buttons_actions.recall_values(st.session_state, 'next', col_call, col_put, col_inputs)
