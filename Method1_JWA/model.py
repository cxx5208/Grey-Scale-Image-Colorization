import keras.backend as K
import tensorflow as tf
from keras.layers import Input, Conv2D, BatchNormalization, UpSampling2D ,MaxPool2D,Conv2DTranspose,Add
from keras.models import Model
from keras.regularizers import l2
from tensorflow.python.keras.utils.multi_gpu_utils import multi_gpu_model
from keras.utils.vis_utils import plot_model

from config import img_rows, img_cols, num_classes, kernel

l2_reg = l2(1e-3)

def resBlock(input_layer, n_filters):
    net = Conv2D(n_filters, kernel_size=3,activation = 'relu', strides=1, padding = 'same', kernel_initializer = 
'he_normal')(input_layer)
    net=BatchNormalization()(net)
    net = Conv2D(n_filters, kernel_size=3,activation = 'relu', strides=1, padding = 'same', kernel_initializer = 
'he_normal')(net)
    net=BatchNormalization()(net)
    net = Conv2D(n_filters, kernel_size=3,activation = 'relu', strides=1, padding = 'same', kernel_initializer = 
'he_normal')(net)
    net=BatchNormalization()(net)
    net = Add()([net, input_layer])
    #net = tf.nn.relu(net)
    return net 
def convBlock(input_layer, n_filters):
    net = Conv2D(n_filters, kernel_size=3,activation = 'relu', strides=1, padding = 'same', kernel_initializer = 
'he_normal')(input_layer)
    net=BatchNormalization()(net)
    return net 
def desconv(input_layer, n_filters):
    net = Conv2DTranspose(n_filters, kernel_size=3,activation = 'relu', strides=2, padding = 'same', 
kernel_initializer = 'he_normal')(input_layer)
    return net 
    
def upBlock(input_layer, n_filters):
    net = UpSampling2D(2)(input_layer)
    net = Conv2D(n_filters, kernel_size=2,activation = 'relu', strides=1, padding = 'same', kernel_initializer = 
'he_normal')(net)
    return net
def convBlock1(input_layer, n_filters):
    net = Conv2D(n_filters, kernel_size=3,activation = 'relu', strides=2, padding = 'same', kernel_initializer = 'he_normal')(input_layer)
    net=BatchNormalization()(net)
    return net





def build_model():
#encoder1
    inputs = Input(shape=(img_rows, img_cols, 1))
    net = Conv2D(32, kernel_size=3,activation = 'relu', strides=1, padding = 'same', kernel_initializer = 
'he_normal')(inputs)
    net=BatchNormalization()(net)
    net = resBlock(net, 32)
    net = convBlock(net, 32)
    skip1 = net
   
    net = convBlock1(net, 64)
    net = resBlock(net, 64)
    net = convBlock(net, 64)
    skip2 = net
    
    net = convBlock1(net, 128)
    net = resBlock(net, 128)
    net = convBlock(net, 128)
    skip3 = net
    
    net = convBlock1(net, 256)
    net = resBlock(net, 256)
    net = convBlock(net, 256)
    skip4 = net
    #net = MaxPooling2D(pool_size=(2, 2), strides=2, padding='valid')(net)
   #BRIDGE
    net = convBlock(net, 512)
    net = resBlock(net, 512)
    net = convBlock(net,512)
    print(net.shape)
 # UPsampling

#   net = desconv(net, 512)
#   net = upBlock(net,256 )
    
    
    net = convBlock(net, 256)
    net = resBlock(net, 256)
    net = Add()([net, skip4])
    net = convBlock(net, 256)
    
#     net = desconv(net, 256)
    net = upBlock(net,128 )
   
    net = convBlock(net, 128)
    net = resBlock(net, 128)
    net = Add()([net, skip3])
    net = convBlock(net, 128)
    
#     net = desconv(net, 128)
    net = upBlock(net,64)
    
    
    net = convBlock(net, 64)
    net = resBlock(net, 64)
    net = Add()([net, skip2])
    net = convBlock(net, 64)
    
#     net = desconv(net, 64)
    net = upBlock(net,32 )
    
    
    net = convBlock(net, 32)
    net = resBlock(net, 32)
    net = Add()([net, skip1])
    net = convBlock(net, 32)
#     net = slim.conv2d(net, n_classes, kernel_size=[1, 1], stride=[1, 1], activation_fn=None)
    net = Conv2D(num_classes, kernel_size=1,activation = 'softmax', strides=1, padding = 'same', kernel_initializer = 
'he_normal')(net)
    model = Model(inputs=inputs, outputs=net)
    
    return model


if __name__ == '__main__':
    with tf.device("/cpu:0"):
        encoder_decoder = build_model()
    print(encoder_decoder.summary())
    plot_model(encoder_decoder, to_file='encoder_decoder.svg', show_layer_names=True, show_shapes=True)

    parallel_model = multi_gpu_model(encoder_decoder, gpus=None)
    print(parallel_model.summary())
    plot_model(parallel_model, to_file='parallel_model.svg', show_layer_names=True, show_shapes=True)

    K.clear_session()
