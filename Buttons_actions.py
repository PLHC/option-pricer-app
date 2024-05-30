import DB_interface
import BlackScholes
import BlackScholesHeatmap
import Display


def _compute(var):
    bsm_prices = BlackScholes.bsm_pricer(var)
    heatmaps = BlackScholesHeatmap.bs_heatmap(var)
    new_row_id, new_row_date = DB_interface.db_store_option_pricing(var, bsm_prices, heatmaps)

    return Display.ComputedPrices(new_row_date, new_row_id, var, bsm_prices, heatmaps)


def _compare_new_inputs_to_latest(var):
    latest_data = DB_interface.read_option_values(var.latest_computation_id)
    if (latest_data.volatility != var.volatility or
            latest_data.underlying_price != var.underlying_price or
            latest_data.exercise_price != var.exercise_price or
            latest_data.time_to_expiration != var.time_to_expiration or
            latest_data.annual_interest_rate != var.annual_interest_rate):
        return False
    else:
        return True


def load_next_previous(reading_id):
    db_data = DB_interface.read_option_values(reading_id)
    heatmaps, bsm_prices = DB_interface.db_data_repacking(db_data)
    return Display.ComputedPrices(db_data.date, reading_id, db_data, bsm_prices, heatmaps)


def recall_values(var, next_or_prev, col_call, col_put, col_inputs):
    following_id = DB_interface.find_next_id(var.id_pointer, next_or_prev)
    # if DB not empty and value is not the last or the first in DB
    if following_id > 0:
        var.id_pointer = following_id
    # if hitting the button on first and last in DB, keep current values on screen
    elif var.latest_computation_id != 0:
        if next_or_prev == 'next':
            following_id = var.id_pointer
        elif next_or_prev == 'prev':
            following_id = var.latest_computation_id

    stored_prices = load_next_previous(following_id)
    Display.prices_and_heatmaps(col_call, col_put, col_inputs, stored_prices)
    return


def compute_or_reload_latest(var, col_call, col_put, col_inputs):
    # reload latest if same as latest without storing it again
    if var.latest_computation_id != 0 and _compare_new_inputs_to_latest(var):
        computed_prices = load_next_previous(var.latest_computation_id)
    else:
        computed_prices = _compute(var)

    Display.prices_and_heatmaps(col_call, col_put, col_inputs, computed_prices)
    var.id_pointer = computed_prices.row_id
    var.latest_computation_id = computed_prices.row_id
    return


__all__ = ['load_next_previous', 'recall_values', 'compute_or_reload_latest']
