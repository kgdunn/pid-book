> **Working draft, not part of the book. Delete this file once the post is published.**
> It lives here only so the draft travels with the material it describes. Nothing in the Sphinx
> build references it, and it is not meant to ship with the book.

# The part of the model you filter out

Fit a PLS model and the write-up goes to the component that tracks the response. The rest, the
systematic variation in the inputs that has nothing to do with the outcome, gets filtered away as a
nuisance.

It is not a nuisance. And it has been discovered twice, by two communities solving two different
problems.

## Run the model backwards

Thirty cheddar cheeses, each measured for acetic acid, hydrogen sulfide and lactic acid, each given a
taste score by a panel. The forward question is "what taste do these measurements imply?" The design
question is the reverse: "which measurements would give me the taste I have chosen?" That is **model
inversion**, and it goes back to Jaeckle and MacGregor (2000).

The answer is not one recipe. It is a whole line of them, every one of which the model says will hit
the target. Product designers call that line the **null space**.

```python
result = pls.invert(y_desired=20.9)
result.x_new                 # {'Acetic': 5.52, 'H2S': 5.56, 'Lactic': 1.40}
result.null_space_dimension  # 1, so this is one point on a line of answers
```

## The same line, from the other side

O-PLS was built for an unrelated reason: to make a model easier to read, by splitting the inputs into
the part that drives the response and the part that does not. That second piece is the **orthogonal
space**.

García-Carrión and co-authors proved this year that, for a single response, the two are the same
linear space. In the cheese model both come out as the same unit vector in the inputs,
(0.948, -0.238, 0.211), with a cosine of 1.0 between them. One geometry, named twice.

## Why the leftover is worth having

For these cheeses the orthogonal piece carries **18.3% of the variation in the inputs and contributes
exactly nothing to the predicted taste**. Not a rounding error, and not noise: systematic variation
with no effect on the outcome.

That buys two things.

**Robustness.** Inputs can move a long way in those directions without shifting the target. It tells
you what you do not have to control tightly.

**Alternatives.** Many recipes, one outcome. The freedom is yours to spend on cost, safety,
availability, or anything else the model never saw.

Widen the target from a point to a range and the line becomes a region: a multivariate specification.
That is how you judge an incoming lot, transfer a product between sites, or state a design space.

One thing to watch. Report that region as one range per input and you have described a box, not the
region. In the cheese example all eight corners of that box satisfy every one of the three ranges, and
not one of them is an acceptable lot. Six predict a taste outside the window. The other two predict a
perfectly good taste from a recipe far outside anything the data support.

## The caveat that keeps it useful

The direction of that line is estimated, and often poorly. Refitting the cheese model on bootstrap
resamples, the null space sits a median of 21 degrees away from the reported direction, and beyond 45
degrees in 15% of resamples. The inverted *point* holds up well. The *direction* does not.

So design at the solution with reasonable confidence, and treat a long walk along the line as
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
