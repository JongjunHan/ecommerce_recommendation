from model import light_model
from preprocessing import product_data, user_product
import pandas as pd
import numpy as np

def recommend_system(user_id, df_user_product, product_information):
    scores = pd.Series(light_model.predict(0, np.arange(user_id)))
    scores = list(pd.Series(scores.sort_values(ascending = False).index))

    scores1 = scores[0: 5]

    product_unique = df_user_product['product_id'].unique()

    product_to_idx = {v:k for k,v in enumerate(product_unique)}
    
    idx_to_product = {v : k for k, v in product_to_idx.items()}
    lfm_rec = [idx_to_product[i] for i in scores1]

    lfm_reco1 = product_information[product_information['product_id'] == lfm_rec[0]][['category_code', 'brand', 'price']][: 1]
    lfm_reco2 = product_information[product_information['product_id'] == lfm_rec[1]][['category_code', 'brand', 'price']][: 1]
    lfm_reco3 = product_information[product_information['product_id'] == lfm_rec[2]][['category_code', 'brand', 'price']][: 1]
    lfm_reco4 = product_information[product_information['product_id'] == lfm_rec[3]][['category_code', 'brand', 'price']][: 1]
    lfm_reco5 = product_information[product_information['product_id'] == lfm_rec[4]][['category_code', 'brand', 'price']][: 1]

    lfm_rec_product = pd.concat([lfm_reco1, lfm_reco2, lfm_reco3, lfm_reco4, lfm_reco5]).reset_index(drop = True)

    return lfm_rec_product