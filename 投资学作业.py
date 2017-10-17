import tushare as ts
import pandas as pd


# 002555三七互娱, 002558巨人网络， 603019中科曙光， 600283钱江水利
def get_all_data(code):
    daily_price = ts.get_hist_data(str(code), start='2016-01-01', end='2016-12-31')['close']
    # return daily_price
    # print(daily_price)
    daily_price = pd.DataFrame([daily_price, pd.Series()]).T
    daily_price.columns = ['price', 'daily_return']
    # print(daily_price.count('index')['price'])

    # print(daily_price.ix[2,0])
    for i in range(daily_price.count('index')['price']):
        if i == 0: continue
        daily_price.ix[i, 1] = (daily_price.ix[i, 0] - daily_price.ix[(i - 1), 0]) / daily_price.ix[(i - 1), 0]
    # print(daily_price)
    # daily_price.ix[0, daily_price] = 0
    daily_return_mean = daily_price.loc[:, 'daily_return'].mean()
    daily_return_std = daily_price.loc[:, 'daily_return'].std()
    annualized_return = (daily_price.loc['2016-12-30', 'price'] - daily_price.loc['2016-01-04', 'price']) / \
                        daily_price.loc['2016-01-04', 'price']

    monthly_price = ts.get_hist_data(str(code), start='2016-01-01', end='2016-12-31', ktype='M')['close']
    monthly_price = pd.DataFrame([monthly_price, pd.Series()]).T
    monthly_price.columns = ['price', 'monthly_return']
    for i in range(monthly_price.count('index')['price']):
        if i == 0: continue
        monthly_price.ix[i, 1] = (monthly_price.ix[i, 0] - monthly_price.ix[(i - 1), 0]) / monthly_price.ix[(i - 1), 0]
    monthly_return_mean = monthly_price.loc[:, 'monthly_return'].mean()
    monthly_return_std = monthly_price.loc[:, 'monthly_return'].std()
    # d_mean, d_std, m_mean, m_std, IRR, daily_P, monthly_P = get_all_data('002555')
    #print(daily_return_mean, daily_return_std, monthly_return_mean, monthly_return_std, annualized_return)
    return daily_return_mean, daily_return_std, monthly_return_mean, monthly_return_std, annualized_return


def compute_correlation(code1, code2):
    daily_price1 = ts.get_hist_data(str(code1),start = '2016-01-01',end = '2016-12-31')['close']
    daily_price2 = ts.get_hist_data(str(code2),start = '2016-01-01',end = '2016-12-31')['close']
    monthly_price1 = ts.get_hist_data(str(code1),start = '2016-01-01',end = '2016-12-31',ktype='M')['close']
    monthly_price2 = ts.get_hist_data(str(code2),start = '2016-01-01',end = '2016-12-31',ktype='M')['close']
    daily_correlation = daily_price1.corr(daily_price2)
    monthly_correlation = monthly_price1.corr(monthly_price2)
    return daily_correlation, monthly_correlation

print("三七互娱：",get_all_data('002555'))
print("巨人网络：",get_all_data('002558'))
print("中科曙光：",get_all_data('603019'))
print("钱江水利：",get_all_data('600283'))
print("同行业相关性：",compute_correlation('002555','002558'))
print("不同行业相关性：",compute_correlation('603019','600283'))