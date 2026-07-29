> **Working draft, not part of the book. Delete this file once the post is published.**
> It lives here only so the draft travels with the material it describes. Nothing in the Sphinx
> build references it, and it is not meant to ship with the book.

# Run the model backwards

Every model you fit points one way. Measurements go in, a prediction comes out. Give it the acid
content of a cheese and it tells you what the tasting panel will say.

Turn it around and you get the question people actually have. Not "what will this taste like?" but
"what should I make so that it tastes like this?"

That reversal has a name, **model inversion**, and it goes back to Jaeckle and MacGregor in 2000. It
works. What surprises people is what comes back.

## One target, many recipes

Ask a fitted model for the inputs that give a chosen quality and it hands you a whole line of recipes.
Every point on that line is a different set of inputs, and every point predicts exactly the target you
asked for.

Picture the prediction as a hill standing over the space of your inputs. Some directions take you
uphill quickly. Asking for a specific outcome is asking to stand at a specific height, and the set of
points at one height is a contour line. Walk along the contour and your position changes while your
altitude does not. Different inputs, same predicted result.

![The null space in the score plot](../../figures/pls/pls-model-inversion-null-space.png)

In the cheddar-cheese example from the book, 18.3% of everything that varies in the three inputs moves
you along that contour and doesn't change the predicted taste. That variation is systematic and
repeatable, well beyond anything measurement noise would account for, and it has no bearing on the
outcome.

It is worth having, twice over. It tells you what you do not have to control tightly. And it means the
model has handed you a choice: many recipes reach the target, so you can make additional choices based
on safety, costs, whichever raw material you can actually get this week, alternatives suited to
regional preferences and regulations, process robustness, and so on. The model never saw those
concerns and does not need to.

## Two fields found it, and gave it two names

People inverting models to design products called that freedom the **null space**.

Chemometricians had arrived at the same place from an unrelated direction. They wanted models that were
easier to read, so they separated the inputs into the part that drives the response and the part that
does not, and called the second the **orthogonal space**. For them it was housekeeping: the leftover,
filtered out to tidy the model up.

It is the same space. García-Carrión and co-authors proved it last year for a single response. One
piece of geometry, discovered twice by two communities solving two different problems, one of them
filtering out what the other was designing with.

## Now write it down as a specification

Widen the target from a number to a range and the contour sweeps out a region: the set of all inputs
you would accept. That is what a specification is.

So write that region down the way specifications are usually written, as an acceptable range for each
input.

![The specification region, and the box of three ranges around it](../../figures/pls/pls-specification-region.png)

The region is a thin slanted slice. A list of ranges describes the box around it. In the cheese
example, every one of the eight corners of that box sits inside all three ranges, however not one of
them is a lot you would accept. Showing once again that with multivariate systems, the process moves
within a smaller embedded subspace.

## One realization of many

Equally interesting when inverting is to refit your model many times, in a bootstrap manner. Doing
this shows where your designs sit, but also where they could possibly have sat.

![Left panel only: the null space from each of 2000 refits of the model](../../figures/pls/pls-null-space-bootstrap.png)

So take a walk along your contours, but recognize it is just one realization of many potential
options.

## Read the chapter

The worked example, the geometry, the specification region and the uncertainty analysis are written up
in full, with every figure reproducible from the code in the text:

**[Using a PLS model backwards: model inversion and the null
space](https://learnche.org/pid/latent-variable-modelling/projection-to-latent-structures/pls-model-inversion-and-the-orthogonal-space)**

`PLS.invert()` and the `OPLS` estimator are in
[process-improve](https://pypi.org/project/process-improve/).

---

C. M. Jaeckle and J. F. MacGregor, "Industrial applications of product design through the inversion of
latent variable models", *Chemometrics and Intelligent Laboratory Systems*, **50** (2000): 199-210.

S. García-Carrión, F. Sartori, J. Borràs-Ferrís, P. Facco, M. Barolo and A. Ferrer, "On the equivalence
between null space and orthogonal space in latent variable regression modeling", *Journal of
Chemometrics*, **39** (2025): e70057.
[doi:10.1002/cem.70057](https://doi.org/10.1002/cem.70057) (open access)
