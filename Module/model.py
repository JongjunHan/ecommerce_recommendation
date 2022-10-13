from lightfm import LightFM
from lightfm import evaluation
from preprocessing import csr_train, csr_test

def modeling(n):
    light_model = LightFM(loss = 'warp', no_components = 20)

    light_model.fit(csr_train, spochs = n, num_threads = 2)

    return light_model


def precision_at_k(light_model, k):
    k = k
    precision = evaluation.precision_at_k(light_model, csr_test, k = k).mean()

    return print('Test precision at k = {} : {: .4f}'.format(k, precision))