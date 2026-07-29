> **Working draft, not part of the book. Delete this file once the post is published.**
> It lives here only so the draft travels with the material it describes. Nothing in the Sphinx
> build references it, and it is not meant to ship with the book.

# Run the model backwards

Every model you fit points one way. Measurements go in, a prediction comes out. Give it the acid
content of a cheese and it tells you what the tasting panel will say.

Turn it around and you get the question people actually have. Not "what will this taste like?" but
"what should I make so that it tastes like this?"

That reversal has a name, **model inversion**, and it goes back to Jaeckle and MacGregor in 2000. What
surprises people is not that it works. It is what comes back.

## The answer is not a recipe. It is a set of them.

Ask a fitted model for the inputs that give a chosen quality and it does not hand you one recipe. It
hands you a line of them. Every point on that line is a different set of inputs, and every point
predicts exactly the target you asked for.

Picture the prediction as a hill standing over the space of your inputs. Some directions take you
uphill quickly. Asking for a specific outcome is asking to stand at a specific height, and the set of
points at one height is a contour line. Walk along the contour and your position changes while your
altitude does not. Different inputs, same predicted result.

![The null space in the score plot](../../figures/pls/pls-model-inversion-null-space.png)

In the cheddar-cheese example from the book, 18.3% of everything that varies in the three inputs moves
you along that contour and changes the predicted taste not at all. That is not noise, and not a
rounding error. It is systematic, repeatable variation with no bearing on the outcome.

It is worth having, twice over. It tells you what you do not have to control tightly. And it means the
model has handed you a choice: many recipes reach the target, so you spend the difference on cost, on
safety, on whichever raw material you can actually get this week. The model never saw those concerns
and does not need to.

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
input, one line each. Entirely reasonable, and it is easy to show what it costs.

![The specification region, and the box of three ranges around it](../../figures/pls/pls-specification-region.png)

The region is a thin slanted slice. A list of ranges describes the box around it. In the cheese
example, every one of the eight corners of that box sits inside all three ranges, and not one of them
is a lot you would accept. Six would taste wrong. The other two would taste fine, but nothing
resembling them has ever been made, so the model carries no evidence about them at all.

Every corner satisfies the specification as written. Not one of them is acceptable.

## The part that is not in the theory

One caveat does not come out of the algebra, so we went looking for it.

The line is exactly what the algebra says it is, for a given model. But the model came from data, and
if you refit it on resampled data the line pivots. It typically lands about twenty degrees away from
the one your model reported. Its starting point barely moves at all.

The two things inversion tells you are therefore not equally firm. Where the design sits, the data
support. Which way you may walk from it, they largely do not. Design at the solution and the ground is
firm; take a long walk along the freedom and it is worth refitting the model first.

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
