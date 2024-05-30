import BlackScholes
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle


class HeatmapOutput:
    def __init__(self, call_heatmap, put_heatmap, call_serialized, put_serialized):
        self.call_heatmap = call_heatmap
        self.put_heatmap = put_heatmap
        self.call_serialized = call_serialized
        self.put_serialized = put_serialized


def generate_heatmap(df):
    fig, ax = plt.subplots()
    cax = ax.matshow(df, cmap='inferno')

    color_bar = fig.colorbar(cax)
    fig.patch.set_facecolor('#121212')
    color_bar.ax.yaxis.set_tick_params(color='white', labelcolor='white', labelsize=8)

    ax.set_xticks(np.arange(len(df.columns)))
    ax.set_xticklabels(df.columns)
    ax.xaxis.set_ticks_position('bottom')
    plt.xticks(rotation=295, font='sans serif', fontsize=8, color='white')
    ax.set_xlabel('Underlying price')
    ax.xaxis.label.set_color('white')

    ax.set_yticks(np.arange(len(df.index)))
    ax.set_yticklabels(df.index)
    plt.yticks(font='sans serif', fontsize=8, color='white')
    ax.set_ylabel('Volatility')
    ax.yaxis.label.set_color('white')
    return fig


def _bs_computations(volatility_range, underlying_price_range, var):
    call_df = pd.DataFrame(index=volatility_range, columns=underlying_price_range)
    put_df = call_df.copy()

    for vol in volatility_range:
        for price in underlying_price_range:
            var = BlackScholes.BSPricerInput(vol, price, var.exercise_price, var.time_to_expiration,
                                             var.annual_interest_rate)
            options_prices = BlackScholes.bsm_pricer(var)
            call_df.at[vol, price] = options_prices.call_price
            put_df.at[vol, price] = options_prices.put_price

    call_df.index = call_df.index.astype(int)
    put_df.index = put_df.index.astype(int)
    call_df.columns = call_df.columns.astype(int)
    put_df.columns = put_df.columns.astype(int)
    return call_df.astype(float), put_df.astype(float)


def bs_heatmap(var, volatility_range=10, underlying_price_range=10):
    # centering the range around truncated volatility and underlying price
    volatility = var.volatility // 1
    underlying_price = var.underlying_price // 1

    index_range = np.arange(volatility + volatility_range + 1,
                            max(volatility - volatility_range, 0),
                            -volatility_range / 10)

    column_range = np.arange(max(underlying_price - underlying_price_range, 0),
                             underlying_price + underlying_price_range + 1,
                             underlying_price_range / 10)

    call_df, put_df = _bs_computations(index_range, column_range, var)

    return HeatmapOutput(generate_heatmap(call_df),
                         generate_heatmap(put_df),
                         pickle.dumps(call_df),
                         pickle.dumps(put_df))


__all__ = ['HeatmapOutput', 'bs_heatmap', 'generate_heatmap']
