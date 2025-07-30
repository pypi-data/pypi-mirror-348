
def get_df_returns_from_prices(df_prices):
    df_returns = df_prices.pct_change().fillna(0)
    df_returns.columns = [f"return: {col}" for col in df_returns.columns]
    return df_returns

def get_df_cumreturns_from_prices(df_prices):
    df_cumreturns = (df_prices / df_prices.iloc[0] - 1) * 100
    df_cumreturns.columns = [f"cumreturn: {col}" for col in df_cumreturns.columns]
    return df_cumreturns