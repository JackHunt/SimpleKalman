'''
 Copyright (c) 2016, Jack Miles Hunt
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
 * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
 * Neither the name of Jack Miles Hunt nor the
      names of contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL Jack Miles Hunt BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import numpy as np

class LinearKalmanFilter:
    def __init__(self, transition, control, errorCov, measurement, measureErrCov, mu, sigma):
        self.__transition = transition #Transition matrix.
        self.__control = control #Control matrix.
        self.__errorCov = errorCov #Error covariance.
        self.__measurement = measurement
        self.__measureErrorCov = measureErrCov #Measurement error covariance.
        self.__mu = mu
        self.__sigma = sigma

    def __predict(self, u):
        self.__mu = self.__transition.dot(self.__mu) + self.__control.dot(u)
        self.__sigma = self.__transition.dot(self.__sigma).dot(self.__transition.T) + self.__errorCov

    def __update(self, z):
        tmp = self.__measurement.dot(self.__sigma).dot(self.__measurement.T) + self.__measureErrorCov
        K = self.__sigma.dot(self.__measurement.T).dot(np.linalg.inv(tmp))
        self.__mu = self.__mu + K.dot(z - self.__measurement.dot(self.__mu))
        tmp = K.dot(self.__measurement)
        self.__sigma = (np.identity(tmp.shape[0]) - tmp).dot(self.__sigma)

    def processPoint(self, z, u):
        self.__predict(u)
        self.__update(z)
        return (self.__mu, self.__sigma)
