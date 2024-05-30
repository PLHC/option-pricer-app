from numpy import log, sqrt, exp
from scipy.stats import norm


class BSPricerOutput:
    def __init__(self, call_price, put_price):
        self.call_price = call_price
        self.put_price = put_price


class BSPricerInput:
    def __init__(self, volatility, underlying_price, exercise_price, time_to_expiration, annual_interest_rate):
        self.volatility = volatility
        self.underlying_price = underlying_price
        self.exercise_price = exercise_price
        self.time_to_expiration = time_to_expiration
        self.annual_interest_rate = annual_interest_rate


def bsm_pricer(var):
    volatility = var.volatility / 100
    time_to_expiration_in_days = var.time_to_expiration / 365
    annual_interest_rate = var.annual_interest_rate / 100

    d1 = ((log(var.underlying_price / var.exercise_price) +
           time_to_expiration_in_days * (annual_interest_rate + 0.5 * volatility ** 2)) /
          (volatility * sqrt(time_to_expiration_in_days)))
    d2 = d1 - volatility * sqrt(time_to_expiration_in_days)

    n1_put = norm.cdf(-d1)
    n1_call = norm.cdf(d1)
    n2_put = norm.cdf(-d2)
    n2_call = norm.cdf(d2)

    call_price = (var.underlying_price * n1_call -
                  var.exercise_price * (exp(-annual_interest_rate * time_to_expiration_in_days)) * n2_call)
    put_price = (var.exercise_price * (exp(-annual_interest_rate * time_to_expiration_in_days)) * n2_put -
                 var.underlying_price * n1_put)

    return BSPricerOutput(call_price, put_price)


__all__ = ['BSPricerOutput', 'BSPricerInput','bsm_pricer']
