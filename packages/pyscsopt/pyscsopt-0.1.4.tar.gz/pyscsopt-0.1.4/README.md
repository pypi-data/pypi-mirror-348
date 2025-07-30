# pySCSOpt: Self-Concordant Smooth Optimization in Python

<p align="center">
    <a style="text-decoration:none !important;" href="https://arxiv.org/abs/2309.01781" alt="arXiv" target="_blank"><img src="https://img.shields.io/badge/paper-arXiv-red" /></a>
    <a style="text-decoration:none !important;" href="https://opensource.org/licenses/apache-2-0" alt="License" target="_blank"><img src="https://img.shields.io/badge/license-Apache 2.0-blue.svg" /></a>
</p>

This package is a Python port of most parts of the Julia package [SelfConcordantSmoothOptimization.jl](https://github.com/adeyemiadeoye/SelfConcordantSmoothOptimization.jl). It includes:

- Proximal L-BFGS-SCORE (a limited-memory version of ProxQNSCORE of the Julia package)
- Proximal GGN-SCORE
- Proximal Gradient-SCORE
- Proximal Newton-SCORE
- Smoothing and regularization (utility) functions

NB: The Julia package remains the main implementation and is more feature-complete for now (with the exemption of the "limited-memory" QN).

## Installation

Install with pip:

```sh
pip install pyscsopt
```

## Usage

See the [`examples/`](https://github.com/adeyemiadeoye/pySCSOpt/tree/main/examples) directory for a usage example. The main entry point is the `pyscsopt` package.

For more information on how to set up problems (especially choosing regularizers), see Julia's [SelfConcordantSmoothOptimization.jl](https://github.com/adeyemiadeoye/SelfConcordantSmoothOptimization.jl).

## Tests

Run tests with:

```sh
pytest pyscsopt/test/
```

## Citation

If you use this package for research, please cite:

```bibtex
@article{adeoye2023self,
  title={Self-concordant Smoothing for Large-Scale Convex Composite Optimization},
  author={Adeoye, Adeyemi D and Bemporad, Alberto},
  journal={arXiv preprint arXiv:2309.01781},
  year={2024}
}
```
