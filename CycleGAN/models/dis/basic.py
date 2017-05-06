from keras.layers import Conv2D
from keras.layers import BatchNormalization, Activation, Input, Dropout
from keras.layers import LeakyReLU
from keras.models import Model

from ...utils.backend_utils import get_filter_dim

def basic_D(input_shape, ndf, n_layers=3, kw=4, dropout=0.0, use_sigmoid=False):
    padw = (kw-1)/2
    
    input = Input(input_shape)
    x = Conv2D(ndf, (kw,kw), strides=(2,2), padding='same')(input)
    x = LeakyReLU(0.2)(x)

    for i in range(n_layers-1):
        x = Conv2D(ndf*min(2**(i+1), 8), (kw,kw), strides=(2,2), padding='same')(x)
        x = BatchNormalization(axis=get_filter_dim())(x)
        if dropout > 0.: x = Dropout(dropout)(x)
        x = LeakyReLU(0.2)(x)

    x = Conv2D(ndf*min(2**(n_layers+1), 8), (kw,kw), strides=(1,1), padding='same')(x)
    x = BatchNormalization(axis=get_filter_dim())(x)
    x = LeakyReLU(0.2)(x)

    x = Conv2D(1, (kw,kw), strides=(1,1), padding='same')(x)
    if use_sigmoid:
        x = Activation('sigmoid')(x)

    model = Model(input, x)
    print('Model basic D:')
    model.summary()

    return model

