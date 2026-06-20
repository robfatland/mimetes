---
marp: true
theme: default
paginate: true
header: "![w:135](../03_research_mechanics/cloudbank_logo.png)&nbsp; Building a GAN with PyTorch"
---

<!-- _header: "" -->
<!-- _paginate: false -->
<!-- _footer: "" -->

![w:500](../03_research_mechanics/cloudbank_logo.png)

# Building a GAN with PyTorch

**CloudBank Cloud Clinic August 2026**

Using: PyTorch, adversarial training, generative models

---

## What Is a GAN?

Two neural networks playing a game:

- **Generator (G):** takes random noise → produces fake images
- **Discriminator (D):** takes an image → decides real or fake

G tries to fool D. D tries to catch G. Both get better.

---

## The Adversarial Dynamic

```
Random noise z ──→ [Generator] ──→ Fake image
                                        ↓
Real image ──────────────────────→ [Discriminator] ──→ Real/Fake?
```

- If D wins: G's loss goes up, G adjusts to make better fakes
- If G wins: D's loss goes up, D adjusts to be more skeptical
- At equilibrium: G produces images indistinguishable from real

---

## Why This Is Interesting

- GANs can generate **new data that never existed**
- Faces, artwork, satellite imagery, molecular structures
- The adversarial framework is elegant: no explicit formula for "what looks real"
- Instead: "real" is defined by whatever fools a trained critic

---

## The Generator

```python
class Generator(nn.Module):
    def __init__(self, latent_dim=100):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(latent_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 512),
            nn.ReLU(),
            nn.Linear(512, 28*28),
            nn.Tanh(),  # output pixels in [-1, 1]
        )

    def forward(self, z):
        return self.net(z).view(-1, 1, 28, 28)
```

---

## The Discriminator

```python
class Discriminator(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Flatten(),
            nn.Linear(28*28, 512),
            nn.LeakyReLU(0.2),
            nn.Linear(512, 256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, 1),
            nn.Sigmoid(),  # probability: real or fake
        )

    def forward(self, img):
        return self.net(img)
```

---

## The Training Loop (Alternating)

```python
for epoch in range(epochs):
    for real_images, _ in dataloader:
        # Train Discriminator
        z = torch.randn(batch_size, latent_dim)
        fake = generator(z)
        d_loss = -torch.mean(torch.log(D(real)) + torch.log(1 - D(fake)))
        d_loss.backward(); d_opt.step()

        # Train Generator
        z = torch.randn(batch_size, latent_dim)
        fake = generator(z)
        g_loss = -torch.mean(torch.log(D(fake)))
        g_loss.backward(); g_opt.step()
```

---

## Watching It Learn (PEARC Demo)

Every N batches, sample from G and display a grid:

- **Epoch 1:** random static
- **Epoch 5:** blurry blobs vaguely digit-shaped
- **Epoch 20:** recognizable digits with artifacts
- **Epoch 50+:** crisp, diverse digits

The booth monitor shows this progression live.

---

## Training Dynamics and Chaos

GANs are notoriously unstable:

- **Mode collapse** — G only produces one digit
- **Oscillation** — D and G alternate dominance
- **Divergence** — losses explode

This connects to dynamical systems theory (bifurcation, chaos).

---

## The Logistics Map Connection

The logistics map x_{n+1} = r·x·(1-x) shows:

- Fixed points → bifurcation → period doubling → chaos

GAN training shows analogous dynamics:

- Convergence → oscillation → mode collapse → instability

Same mathematical framework, different systems.

---

## What We Learned Across Three Case Studies

| Case Study | Core Skill |
|-----------|-----------|
| 01: Fine-tune | Transfer learning, reuse existing models |
| 02: From scratch | The full training loop, what learning looks like |
| 04: GAN | Adversarial training, generative models, instability |

Progression: consume a model → build a model → build two competing models.

---

## Questions? Compliments?

**Repository:** github.com/robfatland/mimetes
**Contact:** help@cloudbank.org
