# Case Study 04 — Build a GAN (Generative Adversarial Network)

## Objective

Build and train a GAN that generates images from random noise. Two networks
compete: a Generator that creates fake images and a Discriminator that tries to
tell real from fake. This adversarial dynamic produces increasingly realistic output.

## What We'll Use

| Component | Choice |
|-----------|--------|
| Architecture | DCGAN (Deep Convolutional GAN) |
| Dataset | MNIST digits or CelebA faces (depending on compute) |
| Framework | PyTorch |
| Visualization | Live-updating grid of generated images |

## Key Concepts

1. **Generator** — takes random noise vector (latent space) → produces an image
2. **Discriminator** — takes an image → outputs probability it's real
3. **Adversarial training** — G tries to fool D; D tries to catch G
4. **Mode collapse** — when G only produces one type of output
5. **Latent space** — the random input space; points near each other produce
   similar outputs
6. **Training instability** — GANs are notoriously finicky to train
7. **Convolutional layers** — spatial structure for image generation

## Steps

1. Define the Generator network (ConvTranspose2d layers)
2. Define the Discriminator network (Conv2d layers)
3. Set up adversarial loss (binary cross-entropy)
4. Write the alternating training loop (train D, then train G)
5. Generate sample images every N batches
6. Build live visualization: grid of generated images updating in real time
7. Train until convergence (or interesting chaos)
8. Explore the latent space: interpolate between points

## PEARC Booth Demo (Primary Use Case)

A big monitor showing a grid of generated images that starts as random noise
and gradually becomes recognizable over the course of minutes. Attendees walk up,
see the evolution. The grid refreshes every few seconds.

Technical: matplotlib animation or a simple web page (Flask + JavaScript) that
polls for new generated images.

## The Logistics Map Connection (Aspirational)

The logistics map x_{n+1} = r * x_n * (1 - x_n) exhibits:
- Stable fixed points (small r)
- Period doubling / bifurcation (increasing r)
- Chaos (r > ~3.57)
- Periodic windows within chaos

Potential connections to GANs/neural networks:
- **Training dynamics as a dynamical system** — GAN training can bifurcate
  between modes, oscillate, or become chaotic. The D/G loss curves sometimes
  exhibit period-doubling before mode collapse.
- **The bifurcation diagram as a visualization** — render it alongside GAN
  training metrics to show the audience "here's what chaos looks like in a
  simple system; here's what it looks like in a neural network."
- **Spiderweb diagrams** — could illustrate how an optimizer converges (or
  fails to converge) to a fixed point, analogous to how x_n settles or doesn't.
- **A neural network trained ON the logistics map** — train a small network
  to predict the next iterate x_{n+1} from x_n for various r values. Show
  that the network captures the bifurcation structure.

This is exploratory. The simplest version: include a logistics-map bifurcation
diagram slide to frame "what does learning instability look like?" before
showing GAN training dynamics.

## Status

🔲 Not started
