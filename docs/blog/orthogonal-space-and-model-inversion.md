> **Working draft, not part of the book. Delete this file once the post is published.**
> It lives here only so the draft travels with the material it describes. Nothing in the Sphinx
> build references it, and it is not meant to ship with the book.

# The orthogonal space is as useful as the predictive space

We build a model to predict an outcome from measurements. A latent variable model like PLS does that
by compressing many correlated inputs into a few components, and the usual write-up spends all its
attention on the component that tracks the response. The rest of the model, the systematic variation
that has nothing to do with the response, gets filtered out and described as a nuisance.

That leftover space has a use, and a name, and it turns out to have been discovered twice under two
different names by two groups of people solving two different problems. This post is about what it
is good for.

## Running the model backwards

Start with a small, old, well-worn data set: 30 cheddar cheeses, each with three measurements
(acetic acid, hydrogen sulfide, lactic acid) and a taste score from a panel. The forward question is
the ordinary one: given the three measurements, what taste do we predict?

Many design problems ask the reverse. We fix the taste we want, and solve for the measurements that
would produce it. That is called **model inversion**, and it is the basis of latent variable product
and process design, going back to Jaeckle and MacGregor (2000).

I hold out four cheeses, fit a two-component PLS model on the other 26, and invert it toward a taste
of 20.9, which is what one of the held-out cheeses actually scored.

```python
pls = PLS(n_components=2).fit(X, Y)
result = pls.invert(y_desired=20.9)

print(result.x_new.round(2).to_dict())
# {'Acetic': 5.52, 'H2S': 5.56, 'Lactic': 1.40}
print(result.null_space_dimension)        # 1
```

A recipe comes back. So far this is unremarkable.

The interesting part is the second line of output. The null space has dimension 1, which is the
model telling us that this is not *the* answer. It is one point on a whole line of answers.

## Many recipes, one target

Two components, one response. The target fixes one direction in the score space and leaves the other
free. Anything we do along that free direction changes the recipe without moving the prediction.

Stepping one unit either way along it:

| Row | Target taste | Acetic | H2S | Lactic | T² | SPE |
|---|---|---|---|---|---|---|
| Predicted at step -1 | 20.9 | 4.95 | 6.10 | 1.33 | 1.63 | 0.00 |
| Predicted at step 0 | 20.9 | 5.52 | 5.56 | 1.40 | 0.06 | 0.00 |
| Predicted at step +1 | 20.9 | 6.09 | 5.02 | 1.46 | 2.44 | 0.00 |

Read down the rows and the inputs move substantially. Acetic acid goes from about 5 to 6, hydrogen
sulfide falls from 6.10 to 5.02, lactic acid rises slightly. Every one of them still predicts a
taste of 20.9. This set of equally-good recipes is the **null space** of the inversion.

That is a practical result on its own. If three recipes all hit the target, we are free to choose
among them on something the model never saw: cost, supplier availability, energy, shelf life,
whichever raw material lot happens to be in the yard this week.

*Figure: the score plot, with the calibration cheeses, the direct-inversion solution, and the null
space drawn as a line through it. Parallel lines for other target tastes.*
(`pls/pls-model-inversion-null-space.png`)

## Why it is a line, and not a point

The geometry is worth a moment, because it makes everything that follows easier to see.

With two components the prediction is just a weighted sum of the two scores, ŷ = q₁t₁ + q₂t₂. So the
vector **q** of y-loadings is the *gradient* of the prediction in the score plot: the direction in
which predicted taste climbs fastest.

Think of the prediction as a hill over the score plot. **q** points straight uphill. Asking for a
specific taste is asking to stand at a specific height, and the set of points at one height on a
hill is a contour line. The null space is that contour: walk along it and your coordinates change
while your altitude does not.

Which gives the whole thing in one line. If a step Δt leaves the prediction unchanged, then

**q**ᵀΔt = 0

The free directions are exactly those perpendicular to the gradient. For these cheeses **q** =
(0.546, -0.262), so the contour has a slope of 2.08 in the score plot, and every design on that line
predicts the same taste.

*Figure: contours of predicted taste, perpendicular to the gradient q, drawn on equal axes so the
right angle is visible.* (`pls/pls-null-space-geometry.png`)

## The same space, arrived at from the other direction

Now forget inversion completely.

O-PLS (orthogonal projections to latent structures, Trygg and Wold, 2002) was invented for an
unrelated reason: to make a model easier to interpret. It takes the one X matrix and writes it as
two additive pieces plus a residual:

X = **t**ₚ**p**ₚᵀ + **T**ₒ**P**ₒᵀ + E

y = qₚ**t**ₚ + f

The first piece is *predictive*, the second is *Y-orthogonal*. The important line is the second one:
**T**ₒ does not appear in it. The orthogonal piece can be as large as it likes and the prediction
does not move.

For the cheese model, that orthogonal piece carries **18.3% of the sum of squares in X**, against
68.7% for the predictive piece and 13.0% left in the residual. Its score correlates with taste at
exactly zero. So nearly a fifth of the systematic variation in these three measurements does nothing
whatsoever to taste. That is not noise, and it is not a rounding error.

**That orthogonal space and the null space from the inversion are the same space.** García-Carrión
and co-authors proved it, for a single response, in the *Journal of Chemometrics* last year. Written
as unit vectors in the original three measurements, both come out as (0.948, -0.238, 0.211), and the
cosine between them is 1.0.

Two communities, solving two unrelated problems, with two different algorithms, named the same
geometry twice. One called it the space to filter away; the other called it the freedom to design
with.

## What the orthogonal space is for

This is the part I want to argue for, because the orthogonal space is usually presented as the part
you discard.

**It tells you what you do not have to control.** Variation along these directions is, by
construction, variation the response does not feel. If a plant is fighting to hold a measurement
steady and that measurement moves mostly along the orthogonal space, that effort is buying very
little. The predictive space tells you what to control. The orthogonal space tells you where you can
stop.

**It gives you alternatives at no cost to the target.** Every point along it hits the same number.
The freedom is real and it is free, in terms of the response. It is not free in every sense, and
that is the caveat to state plainly: in the table above, stepping away from the middle raised T²
from 0.06 to 1.63 and 2.44. The prediction does not change, but the support the data give that
design does. So the freedom is bounded, and T² is how we bound it.

**It is a robustness statement about incoming material.** Two lots of raw material that differ a lot
on paper may differ almost entirely along the orthogonal space, in which case they are
interchangeable for this product. Two others that look similar may differ along the predictive
direction and not be interchangeable at all. The distance that matters is not the distance in the
raw measurements.

## From points to regions

Everything above aimed at one target number. Real products are specified over a range, and that is
where this gets useful rather than merely elegant.

Each acceptable taste has its own null space, and those null spaces are parallel. Sweeping the
target across the acceptable range sweeps its line across the score plot, and the swept lines fill
out a region. Bound it in the other direction with the T² limit so we do not wander outside the
data, and the result is a **multivariate specification region**: the set of inputs we are prepared
to accept.

```python
t2_limit = pls.hotellings_t2_limit(0.95)   # 7.36

region = []
for target in np.linspace(20.0, 40.0, 5):        # the range of taste we accept
    for step in np.linspace(-6, 6, 2001):        # walk along that target's null space
        candidate = pls.invert(target, null_space_coordinates=[step])
        if candidate.hotellings_t2 <= t2_limit:
            region.append(candidate.x_new)
```

One warning that costs people real money: the min and max of that region are the *enclosing box*,
not the region. The region is a slanted band. A lot can sit inside all three individual ranges and
still fall outside the band, because what makes it acceptable is the combination, not each
measurement separately.

This shape of answer covers a lot of ground:

- **Incoming raw materials.** Which lots can I accept, and how do I use the ones I have?
- **Product and process transfer, and scale-up.** Which conditions on the new line reproduce the
  product from the old one?
- **Design space, in the QbD sense.** A defensible region rather than a single set point.
- **Choosing among equivalent recipes** on cost, availability, or environmental impact.

Jaeckle and MacGregor called this a *window of process operating conditions* in 2000, and moved
along the null space over a range that kept conditions within past experience, then applied
engineering judgement to pick a point in that window. Bounding by T² makes "within past experience"
a single testable number. Paris, Duchesne and Poulin (2021) compare model inversion against direct
mapping for exactly this and find neither wins in every case: inversion accepted more of the good
lots in their study, while direct mapping is simpler and leaves more freedom in the region's shape.

## The caveats worth stating

The equivalence is proved for a **single response**. With more than one response, inversion still
works, but the O-PLS shortcut does not carry over, since O-PLS separates one predictive component.
The null space then has dimension A - rank(Y): with three components and two responses, a line. The
multi-response equivalence is open work, noted as such by the authors.

And a moderate model is fine for this. The cheese model explains about 67% of the variation in
taste, which is unremarkable. The null space is a property of the model's geometry, not of how
accurately it predicts. A design far from the cheese that actually had that taste is not a failed
inversion: the inversion returns the smallest-norm solution, nature returned whatever it returned,
and the null space is precisely the reason both can carry the same predicted taste while sitting
some distance apart.

## Try it

Everything above runs. `PLS.invert()` and an `OPLS` estimator are in the open-source
`process_improve` library, and every number and figure in this post regenerates from public code on
a public data set.

The fully worked version, with the algebra, the geometry, the specification region, and a
multiple-response example on a solvents data set, is the "Using a PLS model backwards: model
inversion and the null space" section of my free textbook.

## References

- C. M. Jaeckle and J. F. MacGregor, "Industrial applications of product design through the
  inversion of latent variable models", *Chemometrics and Intelligent Laboratory Systems*, **50**
  (2000): 199-210.
- J. Trygg and S. Wold, "Orthogonal projections to latent structures (O-PLS)", *Journal of
  Chemometrics*, **16** (2002): 119-128, doi:10.1002/cem.695.
- A. Paris, C. Duchesne, and É. Poulin, "Establishing multivariate specification regions for
  incoming raw materials using projection to latent structure models", *Frontiers in Analytical
  Science*, **1** (2021): 729732.
- S. García-Carrión, F. Sartori, J. Borràs-Ferrís, P. Facco, M. Barolo, and A. Ferrer, "On the
  equivalence between null space and orthogonal space in latent variable regression modeling",
  *Journal of Chemometrics*, **39** (2025): e70057, doi:10.1002/cem.70057.
