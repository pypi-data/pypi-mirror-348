from ohlcutils.config import load_config as load_ohlc_config
from ohlcutils.data import load_symbol

load_ohlc_config("/home/psharma/.tradingapi/ohlcutils.yaml", force_reload=True)
from ohlcutils.data import load_symbol
from ohlcutils.enums import Periodicity
from ohlcutils.indicators import (average_band, bextrender, calc_sr,
                                  calculate_beta, calculate_beta_adjusted_bars,
                                  calculate_ratio_bars, degree_slope,
                                  get_heikin_ashi, hilega_milega, range_filter,
                                  srt, supertrend, t3ma, trend, vwap)

# md = load_symbol(
#     "INFY_STK___",
#     days=10000,
#     src=Periodicity.DAILY,
#     dest_bar_size="5D",
#     label="right",
#     target_weekday="Tuesday",
#     adjust_for_holidays=True,
#     adjustment="fbd",
# )
md = load_symbol("NSENIFTY_IND___", days=300, dest_bar_size="5D", label="left")
md = load_symbol("NSENIFTY_IND___", days=300, dest_bar_size="1D")
md = load_symbol("EICHERMOT_STK___", dest_bar_size="1D")
tr = trend(md)
md_benchmark = load_symbol(
    "NSENIFTY_IND___",
    days=10000,
    src=Periodicity.DAILY,
    dest_bar_size="1W",
    label="left",
    adjust_for_holidays=True,
    adjustment="fbd",
)

beta = calculate_beta(md, md_benchmark)
ratio_bars = calculate_ratio_bars(md, md_benchmark)
beta_bars = calculate_beta_adjusted_bars(md, md_benchmark)
haikin = get_heikin_ashi(md)
slope = degree_slope(md, 252, method="regression")
avg_band = average_band(md)
tr = trend(md)
rng_filter = range_filter(md)
new_ma = t3ma(md)
extrender = bextrender(md)
vwap_md = vwap(md)
hm = hilega_milega(md)
st = supertrend(md)
sr = calc_sr(md)
strength_ratio = srt(md)
print(sr.tail())
