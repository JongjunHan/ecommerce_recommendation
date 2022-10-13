import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.model_selection import train_test_split

def user_product(fpath):
    df = pd.read_parquet(fpath)

    df['cart'] = np.where(df['event_type'] == 'view', 1, 0)
    df['view'] = np.where(df['event_type'] == 'cart', 1, 0)
    df['purchased'] = np.where(df['event_type'] == 'purchase', 1, 0)

    df = df[('event_type', 'user_id', 'product_id', 'price', 'view', 'cart', 'purchased')]

    bins = list(range(0, 3000, 300))
    bins_label = [x / 300 for x in bins]
    df['price_label'] = pd.cut(df['price'], bins, right = False, labels = bins_label[: -1])

    df_product = df.groupby('product_id')['view', 'cart', 'purchased'].sum()
    df_product['rating_value'] = (df_product['purchased'] + df['cart'] * 0.7 + df_product['view'] * 0.1) / (df_product['purchased'] + df_product['cart'] + df_product['view'])

    df_rating = df_product['rating_value']
    df_event_rating = pd.merge(df, df_rating, on = 'product_id', how = 'outer')
    df_event_rating = df_event_rating[['event_type', 'user_id', 'product_id', 'price_label', 'rating_value']]

    df_pl0 = df_event_rating[df_event_rating['price_label'] == 0]
    df_pl1 = df_event_rating[df_event_rating['price_label'] == 1]
    df_pl2 = df_event_rating[df_event_rating['price_label'] == 2]
    df_pl3 = df_event_rating[df_event_rating['price_label'] == 3]
    df_pl4 = df_event_rating[df_event_rating['price_label'] == 4]
    df_pl5 = df_event_rating[df_event_rating['price_label'] == 5]
    df_pl6 = df_event_rating[df_event_rating['price_label'] == 6]
    df_pl7 = df_event_rating[df_event_rating['price_label'] == 7]
    df_pl8 = df_event_rating[df_event_rating['price_label'] == 8]

    pl0 = round(df_pl0[df_pl0['event_type'] == 'purchase'].shape[0] / df_pl0.shape[0], 4) * 100
    pl1 = round(df_pl1[df_pl0['event_type'] == 'purchase'].shape[0] / df_pl1.shape[0], 4) * 100
    pl2 = round(df_pl2[df_pl0['event_type'] == 'purchase'].shape[0] / df_pl2.shape[0], 4) * 100
    pl3 = round(df_pl3[df_pl0['event_type'] == 'purchase'].shape[0] / df_pl3.shape[0], 4) * 100
    pl4 = round(df_pl4[df_pl0['event_type'] == 'purchase'].shape[0] / df_pl4.shape[0], 4) * 100
    pl5 = round(df_pl5[df_pl0['event_type'] == 'purchase'].shape[0] / df_pl5.shape[0], 4) * 100
    pl6 = round(df_pl6[df_pl0['event_type'] == 'purchase'].shape[0] / df_pl6.shape[0], 4) * 100
    pl7 = round(df_pl7[df_pl0['event_type'] == 'purchase'].shape[0] / df_pl7.shape[0], 4) * 100
    pl8 = round(df_pl8[df_pl0['event_type'] == 'purchase'].shape[0] / df_pl8.shape[0], 4) * 100

    df_event_rating['price_label'] = df_event_rating['price_label'].replace(0, pl0)
    df_event_rating['price_label'] = df_event_rating['price_label'].replace(1, pl1)
    df_event_rating['price_label'] = df_event_rating['price_label'].replace(2, pl2)
    df_event_rating['price_label'] = df_event_rating['price_label'].replace(3, pl3)
    df_event_rating['price_label'] = df_event_rating['price_label'].replace(4, pl4)
    df_event_rating['price_label'] = df_event_rating['price_label'].replace(5, pl5)
    df_event_rating['price_label'] = df_event_rating['price_label'].replace(6, pl6)
    df_event_rating['price_label'] = df_event_rating['price_label'].replace(7, pl7)
    df_event_rating['price_label'] = df_event_rating['price_label'].replace(8, pl8)

    df_event_rating['price_label'] = df_event_rating['price_label'].astype(float)

    df_event_rating['event_type'] = df_event_rating['event_type'].replace('view', 0.1)
    df_event_rating['event_type'] = df_event_rating['event_type'].replace('cart', 0.7)
    df_event_rating['event_type'] = df_event_rating['event_type'].replace('purchase', 1)

    df_event_rating['event'] = pd.to_numeric(df_event_rating['event_type'])

    df_event_rating['rating'] = df_event_rating['price_label'] * df_event_rating['rating_value'] * df_event_rating['event_type']

    df_user_product = df_event_rating[['user_id', 'product_id', 'rating']]

    return df_user_product


def product_data(fpath):
    df = pd.read_parquet(fpath)
    product_information = df[['product_id', 'category_code', 'brand', 'price']]

    return product_information


def sparse_matrix_split(fpath, n):
    df = pd.read_parquet(fpath)

    user_unique = df['user_id'].unique()
    product_unique = df['product_id'].unique()
  
    user_to_idx = {v:k for k,v in enumerate(user_unique)}
    product_to_idx = {v:k for k,v in enumerate(product_unique)}

    temp_user_data = df['user_id'].map(user_to_idx.get).dropna()
   
    if len(temp_user_data) == len(df): 
        df['user_id'] = temp_user_data
    
    temp_product_data = df['product_id'].map(product_to_idx.get).dropna()
  
    if len(temp_product_data) == len(df):
        df['product_id'] = temp_product_data

    shape = (len(user_to_idx), len(product_to_idx))

    df_train , df_test = train_test_split(df, test_size = n)
    df_train = df_train.reset_index(drop = True)
    df_test = df_test.reset_index(drop = True)

    csr_train = csr_matrix((df_train.rating, (df_train.user_id, df_train.product_id)), shape = shape)
    csr_test = csr_matrix((df_test.rating, (df_test.user_id, df_test.product_id)), shape = shape)

    return csr_train, csr_test