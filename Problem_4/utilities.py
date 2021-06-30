import skimage
import numpy as np
from skimage import io
from skimage.transform import resize
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def mixSounds(sound_list, weights):
	""" Return a sound array mixed in proportion with the ratios given by weights"""
	mixSound = np.zeros(len(sound_list[0]))
	i = 0
	for sound in sound_list:
		mixSound += sound*weights[i]
		i += 1
	return mixSound

def whitenMatrix(matrix):
	"""Whitening tranformation is applied to the images given as a matrix"""
	"""The transformation for the matrix X is given by E*D^(-1/2)*transpose(E)*X"""
	"""Where D is a diagonal matrix containing eigen values of covariance matrix of X"""
	"""E is the matrix containing eigen vectors of covariance matrix of X"""
	# Covariance matrix is approximated by this
	covMatrix = np.dot(matrix, matrix.T)/matrix.shape[1]
	# Doing the eigen decomposition of cavariance matrix of X 
	eigenValue, eigenVector = np.linalg.eigh(covMatrix)
	# Making a diagonal matrix out of the array eigenValue
	diagMatrix = np.diag(eigenValue)
	# Computing D^(-1/2)
	invSqrRoot = np.sqrt(np.linalg.pinv(diagMatrix))
	# Final matrix which is used for transformation
	whitenTrans = np.dot(eigenVector,np.dot(invSqrRoot, eigenVector.T))
	# whiteMatrix is the matrix we want after all the required transformation
	# To verify, compute the covvariance matrix, it will be approximately identity
	whiteMatrix = np.dot(whitenTrans, matrix)
	# print np.dot(whiteMatrix, whiteMatrix.T)/matrix.shape[1]
	return whiteMatrix