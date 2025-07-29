# Copyright 2021-2025 Jean-Baptiste Delisle
# Licensed under the EUPL-1.2 or later

import numpy as np
from samsam import acf, covis, logprior, sam, um

n = 4
nsamples = 100000


def generate_mucov(seed=0):
  np.random.seed(seed)
  mu = np.random.normal(0, 10, n)
  cov = np.identity(n) + np.random.normal(0, 1e-2, n**2).reshape((n, n))
  cov = (cov + cov.T) / 2
  return (mu, cov)


def logprob(x, x_mu, x_cov):
  r = x - x_mu
  return -0.5 * (r @ np.linalg.inv(x_cov) @ r + np.linalg.slogdet(2 * np.pi * x_cov)[1])


def test_sam():
  mu, cov = generate_mucov()
  x0 = np.zeros(n)
  samples, _ = sam(x0, logprob, nsamples=nsamples, x_mu=mu, x_cov=cov)
  samples = samples[nsamples // 4 :: 10]
  samp_mu = np.mean(samples, axis=0)
  samp_cov = np.cov(samples, rowvar=False)

  assert np.max(np.abs(samp_mu - mu)) < 0.1
  assert np.max(np.abs(samp_cov - cov)) < 0.1


def test_um():
  mu, cov = generate_mucov()
  x0 = np.zeros(n)
  samples, _ = um(x0, logprob, nsamples=nsamples, x_mu=mu, x_cov=cov)
  samples = samples[nsamples // 4 :: 10]
  samp_mu = np.mean(samples, axis=0)
  samp_cov = np.cov(samples, rowvar=False)

  assert np.max(np.abs(samp_mu - mu)) < 0.1
  assert np.max(np.abs(samp_cov - cov)) < 0.1


def test_covis():
  mu, cov = generate_mucov()
  mu0 = mu + np.random.normal(0, 0.1, n)
  cov0 = 0.9 * cov + np.random.normal(0, 1e-3, n**2).reshape((n, n))
  cov0 = (cov0 + cov0.T) / 2

  _, _, diags = covis(mu0, cov0, logprob, nsamples=nsamples, x_mu=mu, x_cov=cov)

  assert abs(diags['logevidence']) < 1e-3
