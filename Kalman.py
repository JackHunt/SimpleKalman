import numpy as np

class LinearKalmanFilter:
    def __init__(self, transition, control, errorCov, measureErrCov, mu, sigma):
        self.__transition = transition #Transition matrix.
        self.__control = control #Control matrix.
        self.__errorCov = errorCov #Error covariance.
        self.__measureErrorCov = measureErrCov #Measurement error covariance.
        self.__mu = mu
        self.__sigma = sigma

    def __predict(self, u):
        self.__mu = self.__transition.dot(self.__mu) + self.__control.dot(u)
        self.__sigma = self.__transition.dot(self.__sigma).dot(self.__transition.T) + self.__errorCov

    def __update(self, z):
        tmp = self.__control.dot(self.__sigma).dot(self.__control.T) + self.__measureErrorCov
        K = self.__sigma.dot(self.__control.T).dot(np.linalg.inv(tmp))
        self.__mu = self.__mu + K.dot(z - self.__control.dot(self.__mu))
        tmp = K.dot(self.__control)
        self.__sigma = (np.identity(tmp.shape[0]) - tmp).dot(self.__sigma)

    def processPoint(self, z, u):
        self.__predict(u)
        self.__update(z)
        return (self.__mu, self.__sigma)
