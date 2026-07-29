> **Working draft, not part of the book. Delete this file once the post is published.**
> It lives here only so the draft travels with the material it describes. Nothing in the Sphinx
> build references it, and it is not meant to ship with the book.

# The part of the model you filter out

Picture the prediction from your model as a hill standing over the space of inputs. Moving in some
directions takes you uphill fast; moving in others barely changes your altitude at all. The steepest
way up has a name in a PLS model: it is the vector of y-loadings.

Now ask for a specific outcome. You are asking to stand at a specific height on that hill, and the
set of points at one height is a contour line. Walk along the contour and your position changes while
your altitude does not. Different inputs, same predicted result.

That contour is the thing this post is about. It is real, it is useful, and in most write-ups it is
the part that gets filtered out and called a nuisance.

## Run the model backwards

The forward question is the ordinary one: given these measurements, what quality do we predict? The
design question is the reverse: which measurements would give me the quality I have chosen? That is
**model inversion**, and it goes back to Jaeckle and MacGregor (2000).

The answer is not one recipe. Fixing the target puts you on the contour, and every point on it is a
recipe the model says will hit the target. Product designers call that line the **null space**.

The algebra is one line. If a step in the scores leaves the prediction unchanged, then

**q**ᵀ Δ**t** = 0

The free directions are exactly the ones perpendicular to the gradient. Perpendicular to steepest
ascent means along the contour, which is what the hill already told us.

## The same line, from the other side

O-PLS was built for an unrelated reason: to make a model easier to read, by splitting the inputs into
the part that drives the response and the part that does not. That second piece is the **orthogonal
space**.

García-Carrión and co-authors proved this year that, for a single response, the two are the same
linear space. Inverting a PLS model and fitting an O-PLS model give the same direction, to numerical
precision. One geometry, discovered twice by two communities solving two different problems.

## Why the leftover is worth having

In the cheddar-cheese example from the book, the orthogonal piece carries **18.3% of the variation in
the inputs and contributes nothing at all to the predicted taste**. Not a rounding error, and not
noise: systematic variation with no effect on the outcome.

That buys two things.

**Robustness.** Inputs can move a long way in those directions without shifting the target. It tells
you what you do not have to control tightly.

**Alternatives.** Many recipes, one outcome. The freedom is yours to spend on cost, safety,
availability, or anything else the model never saw.

Widen the target from a point to a range and the contour sweeps out a region: a multivariate
specification. That is how you judge an incoming lot, transfer a product between sites, or state a
design space.

One thing to watch. Report that region as one acceptable range per input and you have described a
box, not the region. The region is a thin slanted slice through that box. In the cheese example every
single corner of the box satisfies all three ranges, and not one of them is a lot you would accept.

## The caveat that keeps it useful

The direction of the contour is estimated, and often poorly. Refit the cheese model on bootstrap
resamples and the null space typically lands about 20 degrees away from the direction the full data
set reports. The inverted *point* holds up well. The *direction* does not.

So design at the solution with reasonable confidence, and treat a long walk along the contour as
something to re-check on a refitted model before acting on it.

## Try it

`PLS.invert()` and the `OPLS` estimator are in
[process-improve](https://pypi.org/project/process-improve/). The worked example, the geometry and the
uncertainty analysis are written up in the book:
[PLS model inversion and the orthogonal space](https://learnche.org/pid/latent-variable-modelling/projection-to-latent-structures/pls-model-inversion-and-the-orthogonal-space).

---

S. García-Carrión, F. Sartori, J. Borràs-Ferrís, P. Facco, M. Barolo and A. Ferrer, "On the
equivalence between null space and orthogonal space in latent variable regression modeling",
*Journal of Chemometrics*, **39** (2025): e70057.
[doi:10.1002/cem.70057](https://doi.org/10.1002/cem.70057) (open access)
