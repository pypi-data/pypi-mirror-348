# Copyright 2021-2025 Jean-Baptiste Delisle
# Licensed under the EUPL-1.2 or later

import numpy as np


def sam(
  x0,
  logprob,
  nsamples=100000,
  mu0=None,
  cov0=None,
  cov_update_interval=100,
  cov_update_law=lambda t: (100 / (t + 1)) ** (2 / 3),
  scale0=None,
  accept_rate_target=0.234,
  force_use_empirical_cov=False,
  print_level=1,
  print_interval=1000,
  print_inplace=True,
  **kwargs,
):
  r"""
  Adaptive Metropolis algorithm (Haario et al. 2001)
  with adaptive scaling (Andrieu & Thoms 2008).

  Parameters
  ----------
  x0 : (ndim,) ndarray
    Initial guess of the parameters.
  logprob(x, **kwargs) : function
    Log probability of the distribution to sample.
  nsamples: int
    Number of samples to draw.
  mu0 : (ndim,) ndarray
    Initial guess of the parameters' mean.
  cov0 : (ndim, ndim) ndarray
    Initial guess of the parameters' covariance matrix.
  cov_update_interval : int
    Interval at which to update the covariance matrix.
  cov_update_law(t) : function
    Update coefficient (between 0 and 1)
    as a function of time (should vanish as t -> nsamples)
  scale0 : float
    Initial scaling factor for the proposal distribution
    (by default 2.4/sqrt(ndim)).
  accept_rate_target : float
    Acceptance rate to target when rescaling the proposal distribution,
    if None, the scale is left unchanged.
  force_use_empirical_cov : bool
    Whether to force the use of the empirical covariance from the beginning.
    If this is not forced, we wait for the acceptance rate to reach at least
    0.1 before considering the empirical covariance to be correct.
  print_level : int
    0 (no printing)
    1 (print acceptance rate)
  print_interval : int
    Interval at which to print infos.
  print_inplace : bool
    Whether to print infos in place or one line after the other.
  **kwargs :
    Additional parameters for the logprob function.

  Returns
  -------
  samples : (nsamples+1, ndim) ndarray
    Array of parameters values for each sample.
  diagnositics : dict
    Dictionary of diagnostics, with the following keys:

      logprob : (nsamples+1,) ndarray
        Array of log probability for each sample.
      alpha : (nsamples,) ndarray
        Array of acceptance probability for each proposal.
      accept : (nsamples,) ndarray
        Array of acceptance for each proposal.
      mu : (ndim,) ndarray
        Final estimate of the mean.
      cov : (ndim, ndim) ndarray
        Final estimate of the covariance matrix.
      scale : float
        Final estimate of the proposal scale.
      use_empirical_cov: bool
        Whether the empirical covariance matrix was used or not.
  """

  nsamples = int(nsamples)
  ndim = len(x0)
  # Init state
  x = x0
  lpx = logprob(x, **kwargs)
  # Init chain
  histx = np.empty((nsamples + 1, ndim))
  histlpx = np.empty(nsamples + 1)
  histalpha = np.empty(nsamples)
  histaccept = np.empty(nsamples, dtype=bool)
  histx[0] = x
  histlpx[0] = lpx
  # Init covariance matrix
  mu = x0.copy() if mu0 is None else mu0.copy()
  if cov0 is None:
    C = np.identity(ndim)
  else:
    if cov0.shape != (ndim, ndim):
      raise Exception(f'Incompatible shapes for x0 ({ndim}) and cov0 {cov0.shape}.')
    C = cov0
  scale = 2.4 / np.sqrt(ndim) if scale0 is None else scale0
  # SVD decomposition of C (more robust than Cholesky)
  _, s, v = np.linalg.svd(C)
  sqCT = np.sqrt(s)[:, None] * v
  use_empirical_cov = force_use_empirical_cov
  # Init printing
  print_fmt = (
    '{}Step {{:{:d}d}}, acceptance rate (since last printing): {{:.4f}}'.format(
      '\r' if print_inplace else '', 1 + int(np.log10(nsamples))
    )
  )
  print_end = ' ' if print_inplace else None

  # Big loop
  for t in range(1, nsamples + 1):
    # Proposal of new point (y)
    y = x + np.random.normal(scale=scale, size=ndim).dot(sqCT)
    # Compute proposal probability
    lpy = logprob(y, **kwargs)
    # Do we accept the proposal
    alpha = np.exp(min(0.0, lpy - lpx))
    accept = np.random.random() < alpha
    if accept:
      x = y
      lpx = lpy
    # Save state in chain
    histx[t] = x
    histlpx[t] = lpx
    histalpha[t - 1] = alpha
    histaccept[t - 1] = accept
    # Update covariance matrix
    if t % cov_update_interval == 0:
      gamma = cov_update_law(t)
      # Update mean
      mudt = np.mean(histx[t + 1 - cov_update_interval : t + 1], axis=0)
      dmu = mudt - mu
      mu += gamma * dmu
      # Update cov
      Cdt = np.cov(histx[t + 1 - cov_update_interval : t + 1], rowvar=False)
      dmu.shape = (ndim, 1)
      C = (1.0 - gamma) * C + gamma * Cdt + gamma * (1.0 - gamma) * dmu.dot(dmu.T)
      if not use_empirical_cov:
        mean_accept = np.mean(histaccept[t - cov_update_interval : t])
        if mean_accept > 0.1:
          use_empirical_cov = True
        else:
          coef = (mean_accept + 0.025) / 0.125
          C *= coef * coef
          sqCT *= coef
      if use_empirical_cov:
        # SVD decomposition of C (more robust than Cholesky)
        _, s, v = np.linalg.svd(C)
        sqCT = np.sqrt(s)[:, None] * v
      # Adapt scale
      if accept_rate_target is not None and use_empirical_cov:
        mean_alpha = np.mean(histalpha[t - cov_update_interval : t])
        scale *= (
          (mean_alpha + 0.25 * accept_rate_target) / (1.25 * accept_rate_target)
        ) ** gamma
    # Print infos
    if print_level and t % print_interval == 0:
      print(
        print_fmt.format(t, np.mean(histaccept[t - print_interval : t])), end=print_end
      )
  if print_level and print_inplace and nsamples >= print_interval:
    print()
  return (
    histx,
    {
      'logprob': histlpx,
      'alpha': histalpha,
      'accept': histaccept,
      'mu': mu,
      'cov': C,
      'scale': scale,
      'use_empirical_cov': use_empirical_cov,
    },
  )


def um(
  x0,
  logprob,
  nsamples=100000,
  scale_update_interval_per_dim=100,
  scale0=None,
  accept_rate_target=0.234,
  print_level=1,
  print_interval=1000,
  print_inplace=True,
  **kwargs,
):
  r"""
  Univariate Metropolis algorithm.

  Parameters
  ----------
  x0 : (ndim,) ndarray
    Initial guess of the parameters.
  logprob(x, **kwargs) : function
    Log probability of the distribution to sample.
  nsamples: int
    Number of samples to draw.
  scale_update_interval_per_dim : int
    Interval at which to update the scale (once multiplied with ndim).
  scale0 : (ndim,) ndarray or None
    Initial scaling factor for the proposal distribution
    (by default 2.4/sqrt(ndim)).
  accept_rate_target : float
    Acceptance rate to target when rescaling the proposal distribution,
    if None, the scale is left unchanged.
  print_level : int
    0 (no printing)
    1 (print acceptance rate)
  print_interval : int
    Interval at which to print infos.
  print_inplace : bool
    Whether to print infos in place or one line after the other.
  **kwargs :
    Additional parameters for the logprob function.

  Returns
  -------
  samples : (nsamples+1, ndim) ndarray
    Array of parameters values for each sample.
  diagnositics : dict
    Dictionary of diagnostics, with the following keys:

      logprob : (nsamples+1,) ndarray
        Array of log probability for each sample.
      kdim : (nsamples,) ndarray
        Array of proposal directions.
      alpha : (nsamples,) ndarray
        Array of acceptance probability for each proposal.
      accept : (nsamples,) ndarray
        Array of acceptance for each proposal.
      scale : (ndim,)
        Final estimate of the proposal scale.
  """

  nsamples = int(nsamples)
  ndim = len(x0)
  # Init state
  x = x0
  lpx = logprob(x, **kwargs)
  # Init chain
  histx = np.empty((nsamples + 1, ndim))
  histlpx = np.empty(nsamples + 1)
  histkdim = np.empty(nsamples)
  histalpha = np.empty(nsamples)
  histaccept = np.empty(nsamples, dtype=bool)
  histx[0] = x
  histlpx[0] = lpx
  # Init scale
  scale = np.full(ndim, 2.4 / np.sqrt(ndim)) if scale0 is None else scale0
  scale_update_interval = scale_update_interval_per_dim * ndim
  # Init printing
  print_fmt = (
    '{}Step {{:{:d}d}}, acceptance rate (since last printing): {{:.4f}}'.format(
      '\r' if print_inplace else '', 1 + int(np.log10(nsamples))
    )
  )
  print_end = ' ' if print_inplace else None

  # Big loop
  for t in range(1, nsamples + 1):
    # Proposal of new point (y)
    kdim = np.random.randint(ndim)
    y = x.copy()
    y[kdim] += np.random.normal(scale=scale[kdim])
    # Compute proposal probability
    lpy = logprob(y, **kwargs)
    # Do we accept the proposal
    alpha = np.exp(min(0.0, lpy - lpx))
    accept = np.random.random() < alpha
    if accept:
      x = y
      lpx = lpy
    # Save state in chain
    histx[t] = x
    histlpx[t] = lpx
    histkdim[t - 1] = kdim
    histalpha[t - 1] = alpha
    histaccept[t - 1] = accept
    # Update scale
    if t % scale_update_interval == 0:
      for kdim in range(ndim):
        inds = np.where(histkdim[t - scale_update_interval : t] == kdim)[0]
        if inds.size < 100:
          continue
        inds += t - scale_update_interval
        mean_alpha = np.mean(histalpha[inds])
        scale[kdim] *= (mean_alpha + accept_rate_target) / (2 * accept_rate_target)
    # Print infos
    if print_level and t % print_interval == 0:
      print(
        print_fmt.format(t, np.mean(histaccept[t - print_interval : t])), end=print_end
      )
  if print_level and print_inplace and nsamples >= print_interval:
    print()
  return (
    histx,
    {
      'logprob': histlpx,
      'kdim': histkdim,
      'alpha': histalpha,
      'accept': histaccept,
      'scale': scale,
    },
  )


def covis(
  mu,
  cov,
  logprob,
  nsamples=100000,
  print_level=1,
  print_interval=1000,
  print_inplace=True,
  **kwargs,
):
  """
  Importance sampling using a multivariate normal sampling distribution.

  The covis sampler generates samples from a normal distribution
  with mean `mu` and covariance `cov`.
  For each sample, the target distribution `logprob` is evaluated
  and a weight is deduced which allows to estimate integrals
  over the target distribution (e.g. the evidence).
  The parameters `mu` and `cov` should be chosen such that the sampling
  distribution is close to the target distribution.

  Parameters
  ----------
  mu : (ndim,) ndarray
    Mean of the sampling distribution.
  cov :  (ndim, ndim) ndarray
    Covariacne of the sampling distribution
  logprob(x, **kwargs) : function
    Log probability of the distribution to sample.
  nsamples: int
    Number of samples to draw.
  print_level : int
    0 (no printing)
    1 (print step)
  print_interval : int
    Interval at which to print infos.
  print_inplace : bool
    Whether to print infos in place or one line after the other.
  **kwargs :
    Additional parameters for the logprob function.

  Returns
  -------
  samples : (nsamples, ndim) ndarray
    Array of parameters values for each sample.
  logweights : (nsamples,) ndarray
    Array of samples log weight.
  diagnositics : dict
    Dictionary of diagnostics, with the following keys:

      logsamp : (nsamples,) ndarray
        Array of log probability of each sample for the sampling distribution.
      logprob : (nsamples,) ndarray
        Array of log probability of each sample for the target distribution.
      logevidence : float
        Log evidence of the target distribution.
  """

  ndim = mu.size
  if cov.shape != (ndim, ndim):
    raise Exception(f'Incompatible shapes for mu ({ndim}) and cov {cov.shape}.')

  # SVD decomposition of cov (more robust than Cholesky)
  _, s, v = np.linalg.svd(cov)
  sqCT = np.sqrt(s)[:, None] * v
  logdet2piC = np.sum(np.log(2 * np.pi * s))

  # Init arrays
  histx = np.empty((nsamples, ndim))
  histlsampx = np.empty(nsamples)
  histlpx = np.empty(nsamples)
  histlw = np.empty(nsamples)

  # Init printing
  print_fmt = '{}Step {{:{:d}d}}'.format(
    '\r' if print_inplace else '', 1 + int(np.log10(nsamples))
  )
  print_end = ' ' if print_inplace else None

  # Big loop
  for k in range(nsamples):
    # Generate sample
    ux = np.random.normal(size=ndim)
    x = mu + ux.dot(sqCT)
    # Compute sampling probabilty
    histlsampx[k] = -(logdet2piC + np.sum(ux * ux)) / 2
    # Compute target probability
    histlpx[k] = logprob(x, **kwargs)
    # Log weight
    histlw[k] = histlpx[k] - histlsampx[k]
    if print_level and (k + 1) % print_interval == 0:
      print(print_fmt.format(k + 1), end=print_end)
  if print_level and print_inplace and nsamples >= print_interval:
    print()

  # Compute log evidence
  # Find max log weight to avoid under/overflows
  maxlw = np.max(histlw)
  lZ = maxlw + np.log(np.sum(np.exp(histlw - maxlw)) / nsamples)

  return (histx, histlw, {'logsamp': histlsampx, 'logprob': histlpx, 'logevidence': lZ})
