# -*- coding: utf-8 -*-
"""ImplementacionSinLibrerias.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XAhXR3IM1vSEG2j1xa-iugRRnh-2sjWM

Se utilizará una base de datos de pacientes que han sufrido un derrame cerebral y otros que no. La finalidad es clasificar las caracteristicas para predecir correctamente si el paciente sufrio un derrame o no
"""

import pandas as pd
import numpy as np
from google.colab import drive
drive.mount('/content/drive')

data= pd.read_csv('/content/drive/MyDrive/ConcentracionCienciaDeDatos/Modulo2/full_data.csv',index_col=False)
data.head()

"""Modelo"""

clean= {'gender': {'Male': 0,'Female':1},'ever_married':{'Yes':1,'No':0},'Residence_type':{'Urban':1,'Rural':0},'smoking_status':{'smokes':2,'formerly smoked':1,'never smoked':0,'Unknown':0}}
data= data.replace(clean)

dx= data[['hypertension','heart_disease','smoking_status']].values
dy= data['stroke'].values
dx=dx[:300]
dy=dy[:300]

"""Regresion logistica, utilizando notacion matricial para la tecnica de gradiente descendiente.
W=[w1,w2,...,wm] 1xm \\
El vector w es el contiene nuestros pesos para cada x, en clase visto como los pesos θ. \\
B= cte \\
Visto en clase como θ cero \\
X= [Matriz] nxm \\
Y= [Vector] nx1 \
Considerando nuestra funcion log-loss vista en clase, los terminos para el gradiente descendiente quedarian:

$W= W - α dW^T$ donde: \\
$dW= (A-Y) X^T$ \\
$A= σ(W^T *X +B)$\\

$B= B - α dB$

"""

def sigmoide(X):
  return 1/(1+np.exp(-X))

ite= 100000
alpha=.008

dx=dx.T
dy= dy.reshape(1,dx.shape[1])
m=dx.shape[1]
n=dx.shape[0]

W= np.zeros((n,1))
B= 0
for i in range(ite):
  S= np.dot(W.T, dx ) + B
  A= sigmoide(S)

  logloss= -(1/m)*np.sum(dy* np.log(A) + (1-dy) *np.log(1-A))

  dW= (1/m)*np.dot(A-dy,dx.T)
  dB= (1/m)*np.sum(A-dy)

  W= W-alpha*dW.T 
  B= B-alpha*dB

  if (i%(ite/10)==0):
    print('Costo despues de',i, 'iteraciones, es:',logloss)

"""Calculo de exactitud del modelo."""

Z= np.dot(W.T,dx) + B
A= sigmoide(Z)

A= A>.5

A= np.array(A,dtype= 'int64')

prec= (1 - np.sum(np.absolute(A-dy))/dy.shape[1])
prec

"""Se obtiene un exactitud media de .69333, la cual considerando la implementación podría mejorar cambiando el método de optimización utilizado."""