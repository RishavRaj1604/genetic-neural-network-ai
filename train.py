from tensorflow.keras.datasets import mnist, cifar10
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping

early_stopper = EarlyStopping(patience=5)

def get_cifar10():
    nb_classes = 10
    batch_size = 64
    input_shape = (3072,)

    (x_train, y_train), (x_test, y_test) = cifar10.load_data()

    x_train = x_train.reshape(50000, 3072).astype('float32') / 255
    x_test = x_test.reshape(10000, 3072).astype('float32') / 255

    y_train = to_categorical(y_train, nb_classes)
    y_test = to_categorical(y_test, nb_classes)

    return nb_classes, batch_size, input_shape, x_train, x_test, y_train, y_test


def get_mnist():
    nb_classes = 10
    batch_size = 128
    input_shape = (784,)

    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    x_train = x_train.reshape(60000, 784).astype('float32') / 255
    x_test = x_test.reshape(10000, 784).astype('float32') / 255

    y_train = to_categorical(y_train, nb_classes)
    y_test = to_categorical(y_test, nb_classes)

    return nb_classes, batch_size, input_shape, x_train, x_test, y_train, y_test


def compile_model(network, nb_classes, input_shape):
    model = Sequential()

    for i in range(network['nb_layers']):
        if i == 0:
            model.add(Dense(network['nb_neurons'], activation=network['activation'], input_shape=input_shape))
        else:
            model.add(Dense(network['nb_neurons'], activation=network['activation']))

        model.add(Dropout(0.2))

    model.add(Dense(nb_classes, activation='softmax'))

    model.compile(
        loss='categorical_crossentropy',
        optimizer=network['optimizer'],
        metrics=['accuracy']
    )

    return model


def train_and_score(network, dataset):
    if dataset == 'cifar10':
        nb_classes, batch_size, input_shape, x_train, x_test, y_train, y_test = get_cifar10()
    else:
        nb_classes, batch_size, input_shape, x_train, x_test, y_train, y_test = get_mnist()

    model = compile_model(network, nb_classes, input_shape)

    model.fit(
        x_train, y_train,
        batch_size=batch_size,
        epochs=10000,
        verbose=0,
        validation_data=(x_test, y_test),
        callbacks=[early_stopper]
    )

    score = model.evaluate(x_test, y_test, verbose=0)

    return score[1]
