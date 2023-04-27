import pandas as pd
import os
import requests
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder


def clean_data(path):
    df = pd.read_csv(path)
    df['b_day'] = pd.to_datetime(df['b_day'], format='%m/%d/%y')
    df['draft_year'] = pd.to_datetime(df['draft_year'], format='%Y')
    df['team'].fillna('No Team', inplace=True)
    df['height'] = df['height'].apply(lambda x: x.split(' / ')[1]).astype(float)
    df['weight'] = df['weight'].apply(lambda x: x.split(' / ')[1][0:-3]).astype(float)
    df['salary'] = df['salary'].apply(lambda x: x[1:]).astype(float)
    df['country'] = df['country'].apply(lambda x: 'USA' if x == 'USA' else 'Not-USA')
    df['draft_round'] = df['draft_round'].apply(lambda x: x.replace('Undrafted', '0'))
    return df


def feature_data(df: pd.DataFrame):
    ds_version = pd.to_datetime(df['version'].apply(lambda x: '20' + x[-2:]), format='%Y')
    df['age'] = ds_version.apply(lambda x: x.strftime('%Y')).astype(int) - df['b_day'].apply(
        lambda x: x.strftime('%Y')).astype(int)
    df['experience'] = ds_version.apply(lambda x: x.strftime('%Y')).astype(int) - df['draft_year'].apply(
        lambda x: x.strftime('%Y')).astype(int)
    df['bmi'] = df['weight'] / df['height'] ** 2
    df = df.drop(['version', 'b_day', 'draft_year', 'weight', 'height'], axis=1)
    for col in df.columns:
        if df[col].nunique() >= 50 and col not in ['bmi', 'salary']:
            df = df.drop(col, axis=1)
    return df


def multicol_data(df: pd.DataFrame):
    numeric_cols = df.select_dtypes(include='number').drop(columns='salary').columns
    df_corr = df[numeric_cols].corr().abs()
    high_corr = df_corr[(df_corr > 0.5)]
    np.fill_diagonal(high_corr.values, np.nan)
    select_cols = list(high_corr.dropna(axis=1, how='all').columns)
    select_cols.append('salary')
    sal_corr = df[select_cols].corr().abs()
    drop_col = sal_corr['salary'].sort_values(ascending=True).index[0]
    return df.drop(axis=1, columns=drop_col)


def transform_data(df):
    num_feat_df = df.drop(columns='salary').select_dtypes('number')
    cat_feat_df = df.drop(columns='salary').select_dtypes('object')
    y = df['salary']
    scaler = StandardScaler()
    df_scale = pd.DataFrame(columns=num_feat_df.columns, data=scaler.fit_transform(num_feat_df))
    encoder = OneHotEncoder()
    encoder.fit(cat_feat_df)
    col_list = [y for x in encoder.categories_ for y in x]
    df_encode = pd.DataFrame(data=encoder.transform(cat_feat_df).toarray(), columns=col_list)
    X = pd.concat([df_scale, df_encode], axis=1)
    return X, y


# Checking ../Data directory presence
if not os.path.exists('../Data'):
    os.mkdir('../Data')

# Download data if it is unavailable.
if 'nba2k-full.csv' not in os.listdir('../Data'):
    print('Train dataset loading.')
    url = "https://www.dropbox.com/s/wmgqf23ugn9sr3b/nba2k-full.csv?dl=1"
    r = requests.get(url, allow_redirects=True)
    open('../Data/nba2k-full.csv', 'wb').write(r.content)
    print('Loaded.')

data_path = "../Data/nba2k-full.csv"


# write your code here

df_cleaned = clean_data(data_path)
df_featured = feature_data(df_cleaned)
df = multicol_data(df_featured)
X, y = transform_data(df)

answer = {
    'shape': [X.shape, y.shape],
    'features': list(X.columns),
    }
print(answer)
