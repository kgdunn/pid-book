# Judging and comparing experimental designs

You have five factors to study, you expect curvature in the response, and you have only so many
experimental runs to spend.

Your software offers the usual candidates, perhaps these six: a full factorial, a fractional
factorial, a central composite design (CCD), a Box-Behnken design (BBD), a definitive screening
design (DSD), and an OMARS (orthogonal minimally aliased response surface) design.

How do you compare them on metrics that show the trade-offs, rather than on a single headline score?
It is not necessarily the design with the fewest runs, nor the one with the highest efficiency
score, that fits your purpose.

A short roadmap. We look at each design through five lenses, in this order:

0. Feasibility: can the design fit the model at all?
1. Power: the chance of flagging a real effect.
2. Coefficient precision: how tightly the model's coefficients are estimated together (the D-based
   metrics).
3. Prediction variance: how large the prediction error is across the factor space (I-optimality for
   the average, G-optimality for the worst case).
4. Separability and degrees of freedom: how cleanly the terms can be told apart, and whether
   anything is left over to estimate the noise. These are two related checks, taken together as the
   last lens.

A consolidated table follows the five lenses, then two practical rules.

## The rules of a fair comparison

For illustration we fit a model with main effects and pure quadratics, and no two-factor
interactions: an intercept, five linear terms, and five pure quadratic terms, so eleven coefficients
in all.

A word on that choice, because it shapes everything below. A full response-surface model would also
carry the ten two-factor interactions (twenty-one coefficients). We leave them out so the smallest
designs are not disqualified for want of degrees of freedom before the comparison starts. That is an
assumption, not a fact. If interactions are present and we do not estimate them, the eleven
coefficients we keep are biased. How much, and for which designs, is the job of the alias matrix,
which we return to once the designs are on the table (lens 4). Read what follows with that one
caveat in mind: it favours the smaller designs to the degree that interactions are negligible.

Two more rules. We map each factor to the coded region from -1 to +1. And each design keeps its own
run count: we do not pad the smaller designs up to match the larger ones. So part of the question is
whether a larger design earns its extra runs.

So we are comparing where each design places its runs, and what those choices buy.

## 0. Feasibility: can the design fit the model at all?

Two of the six are ruled out at once. A two-level full or fractional factorial cannot estimate the
five quadratic terms. At two levels each squared column equals 1 at every factorial run, so all five
quadratic columns are identical to one another and to the intercept column. A pure two-level design
therefore estimates only six directions: the intercept and the five linear terms. The five
quadratics are completely aliased with the intercept, so not one of them, nor even their sum, can be
separated out.

Adding center points buys back exactly one of the missing directions. At a center run each squared
column is 0 while the intercept is still 1, so the intercept and the (now common) quadratic column
are no longer identical: a seventh direction appears, a single lumped curvature. Center points also
give an estimate of the noise variance, a check on drift between runs, and the degrees of freedom
for an overall curvature test. What they cannot do is tell the five quadratics apart. That single
curvature signal is the cue to add axial runs, which is how the central composite design is built.

So four designs remain: the 46-run Box-Behnken design (40 design runs plus 6 center runs), the
32-run central composite design, the 25-run OMARS design, and the 13-run DSD. We now compare these
four.

Those center-run counts are each design's standard specification rather than padding: the
Box-Behnken and central composite designs carry six center runs each, the OMARS and DSD one each.
The center runs set the pure-error degrees of freedom and steady the prediction variance near the
center of the region. One consequence is worth keeping in view when reading the table below: the
six-versus-one difference is itself part of the contrast, not a controlled-for constant. Some of the
larger designs' lower central prediction variance and extra residual degrees of freedom comes from
that extra replication, not only from where the non-center points sit.

A note on construction, since every number below depends on it. The 32-run CCD here is built on a
resolution-V half-fraction: a sixteen-run 2^(5-1) factorial in which no main effect or two-factor
interaction is aliased with another, plus ten face-centred axial runs at distance alpha = 1 and six
center runs. Keeping the axial runs on the faces (alpha = 1) holds every run inside the coded -1 to
+1 cube, so all the designs are compared over the same region. A rotatable CCD would push the axial
runs out to alpha = 2.0 (the rotatable distance for a sixteen-point cube, 16^(1/4)) and would score
better only by exploring a wider region.

One disclosure about the OMARS design used here. OMARS is a catalogue, not a single recipe: for a
given factor count it offers many designs of different sizes, each selected to keep the aliasing
among second-order terms minimal. The 25-run design in this comparison is not taken from that
catalogue. It is built by hand as two permuted conference-matrix foldovers, which gives it the
defining OMARS property (main effects orthogonal to every second-order term) but makes it one
constructed instance rather than a catalog-optimal member. A design pulled from the published OMARS
catalogue at this run size may score somewhat differently. All four designs, and every figure and
number below, regenerate from the open Python scripts in the book (built with the process_improve
library).

## 1. Power

Power is the probability of flagging a real effect when one is present: a low value means real
effects go undetected. We test at the 5% level. By the usual convention we assume each effect we are
trying to detect is the size of one noise standard deviation.

Being precise about what "effect" means here: it is the model coefficient. So a coefficient of one
standard deviation means the response shifts by two standard deviations across a factor's -1 to +1
range, a signal-to-noise ratio of 2. That is the default several design packages (for example
Stat-Ease Design-Expert) use for power, so these numbers are directly comparable to theirs; a larger
assumed effect would raise every value.

*Figure: power to detect a one-standard-deviation main effect and a one-standard-deviation quadratic
effect, four designs, five-factor model.*

The 13-run DSD has a 0.42 chance of catching a one-standard-deviation main effect and only 0.15 on a
quadratic of the same size. The three larger designs all reach 0.97 or above on main effects. On
curvature they separate: the 46-run Box-Behnken design reaches 0.82, while the 32-run CCD manages
only 0.32 and the 25-run OMARS design 0.46. The CCD carries axial runs placed specifically to
estimate curvature, so why does it trail the Box-Behnken design? Partly run count, and partly
placement. The Box-Behnken design spends more runs informing the quadratic terms; and the
face-centred CCD's axial runs sit at alpha = 1, on the cube faces, which gives less leverage on
curvature than axial points pushed further out would. Axial runs make the quadratics estimable; they
do not, on their own, make them powerfully tested.

One point in the DSD's favour, since its numbers look stark. A DSD is built for effect sparsity, not
for this saturated eleven-term fit. Its design intent (Jones and Nachtsheim, 2011) is to project
onto the few factors that turn out to be active and estimate their curvature cleanly, not to test
all five quadratics at once on thirteen runs. Judged on the full model it is being asked for
something it was not built to give; we hold it to the same model as the rest precisely to show that
trade-off, not to suggest the DSD is a poor design.

## 2. Coefficient precision: one score, two opposite rankings

Next, the precision with which the eleven coefficients are estimated together. This is what the
D-based metrics summarise. (D-optimality is the criterion: make the joint confidence region for all
coefficients as small as possible. D-efficiency is the metric derived from it.)

D-efficiency takes the determinant of the design's information matrix (a summary of how precisely
the whole set of coefficients is estimated), takes its p-th root to put it on a per-coefficient
footing (p = 11 coefficients), divides by the run count, and reports the result as a percentage. For
this absolute formula the 100% reference is a hypothetical orthogonal design, one with det(X'X) =
n^p. That ceiling is unreachable for a model with pure-quadratic terms inside the coded cube, since
the squared columns cannot be made orthogonal to the intercept. That is why all four designs sit in
the 28 to 40% band, well short of 100%, rather than because any of them is poor. A different
convention, relative D-efficiency, takes the D-optimal design as 100% instead, so check which one
your software reports.

On that per-run measure the 13-run DSD (39.9%) and the 25-run OMARS design (39.3%) come out highest,
above the 46-run Box-Behnken (30.5%) and 32-run CCD (28.0%) designs that estimate, test, and predict
more precisely overall. The reason is the division by the run count: D-efficiency measures
information per experiment, not total information.

The same per-coefficient determinant before dividing by the run count (the p-th root of det(X'X),
often reported in software) ranks the designs the other way: the 46-run Box-Behnken design highest
at 14.0 and the 13-run DSD lowest at 5.19. These two rows are not independent evidence; they are the
same determinant scaled by the run count either way. Multiply the per-run figure by the run count
and you recover it (46 x 30.5% = 14.0); divide by the run count and you get the per-run percentage
back.

The per-run percentage is not wrong. It answers a different question: the average value contributed
by each experimental run. It rewards a design for spending fewer of them.

## 3. Prediction variance: two views

We have covered power (1) and coefficient precision (2). Next is prediction.

Prediction variance is not equal everywhere. You expect it to be larger near the edges of the region
than at the center. The prediction variance at any future point inside the coded -1 to +1 region can
be calculated and summarised in a fraction-of-design-space (FDS) plot. The horizontal axis is the
fraction of the region, ordered from the points that are predicted most precisely (left) to those
predicted least precisely (right, typically the corners). The vertical axis is the prediction
variance. A low, flat curve is what you want.

*Figure: FDS curves for the four designs, scaled by run count (left) and unscaled, in noise-variance
units (right). The region is the cuboidal coded cube [-1, +1]^5.*

The two panels show the same curves on two scales. Scaled by the run count (left), the 13-run DSD
curve sits among the others. Unscaled, in raw noise-variance units (right), the DSD curve is the
highest and the 46-run Box-Behnken design has the lowest average prediction variance (0.18 versus
0.71 for the DSD). The scaled panel does not show the cost of running few experiments; the unscaled
panel is in the units you will actually live with as the experimenter.

One detail worth reading off the right-hand panel: the average and the worst case need not agree.
The Box-Behnken design is lowest on average and across most of the curve, but it places no runs at
the cube's corners, so at the worst fraction (the far right) the face-centred CCD edges it: the
CCD's maximum prediction variance is 0.77 versus the Box-Behnken's 0.84.

A caution on the worst case, because there are two versions of it. The numbers just quoted are
unscaled, in noise-variance units, which is what you obtain at the bench. The named worst-case
criterion, G-optimality, is defined on the scaled (per-run) curve instead, and on that footing the
ranking reverses: the 13-run DSD has the lowest scaled maximum (13.6) and the 46-run Box-Behnken the
highest (38.8), for the same reason the per-run D-efficiency favoured the small designs. So if the
worst spot matters, decide first which one you mean: the worst case at the bench (read the unscaled
right tail) or the worst case per experiment (the scaled G value).

## 4. Separability and degrees of freedom

Two designs can estimate the same model with the same precision and still differ in how cleanly they
pull the effects apart, and in how much they leave over to check themselves. Those are the two parts
of this last lens.

Degrees of freedom first. The residual degrees of freedom are the runs minus the coefficients: 35
for the 46-run Box-Behnken design, 21 for the CCD, 14 for the OMARS design, and just 2 for the
13-run DSD. They are what is left to estimate the noise variance and run any test at all. A
saturated design, with as many runs as coefficients and zero left over, fits its own data exactly
and can report no standard error, no test, no power. The DSD's two residual degrees of freedom are
why its power numbers in lens 1 are so low: there is almost nothing left to test against.

Separability is the other part. It is high when each coefficient can be estimated almost as if the
others were not in the model, and low when the terms overlap so that estimating one trades off
against another. You read it from two diagnostics. The first is the largest correlation between any
pair of model columns: near 0 is good. The second is the variance inflation factor (VIF) of each
coefficient: the factor by which that coefficient's variance is inflated by its correlation with the
other terms in the model, relative to an orthogonal design where it would equal 1. A VIF of 1 means
the term is estimated independently of the rest; a large VIF (a common rule of thumb flags values
above 5 to 10) means the term is entangled with others and hard to pin down. Both diagnostics are
computed on centered columns, so the quadratics' nonzero mean does not by itself inflate them; only
genuine correlation with the other terms does.

*Figure: a color map of the absolute correlation among the twenty model-effect columns for the four
designs, in three blocks (the five main effects, the five quadratics, and the ten two-factor
interactions the model omits), separated by lines.* The main-effect block is orthogonal to
everything for every design. Among the fitted terms (main effects and quadratics) the four are
nearly separable, the composite design's quadratics being the most entangled (0.75); but reading in
the omitted interactions, the OMARS and DSD designs show correlations up to 0.50, where their
quadratics meet the interactions left out.

Now the alias matrix promised earlier. The VIF measures overlap among the terms you fit. The alias
matrix measures overlap between those terms and the interactions you chose not to fit: if a dropped
interaction is really present, it biases the coefficients you kept, and the alias matrix says by how
much. This is where the DSD and OMARS designs earn their name. They keep every main effect clear of
the second-order terms, so a present interaction does not bias the main effects at all (their
main-effect alias is zero); that is what "minimally aliased" means. The price falls on the
quadratics, which an interaction can shift. The Box-Behnken and composite designs, by contrast, hold
even that bias at zero on this model. The table below carries one summary of it: the largest alias
coefficient for each design.

*Figure: the absolute alias matrix for the four designs, as a heatmap (rows: the eleven fitted
terms; columns: the ten omitted two-factor interactions).* It is zero everywhere for the Box-Behnken
and composite designs; for the OMARS and DSD designs the main-effect rows are zero and the bias sits
on the quadratic rows (up to 1.00 and 1.09).

## The four designs side by side

One table holds the whole comparison. Designs run largest to smallest; the arrow at the start of
each label says which direction is better. Power is quoted at delta = sigma, an effect of one noise
standard deviation, as defined in lens 1.

| Metric | BBD [n=46] | CCD [n=32] | OMARS [n=25] | DSD [n=13] |
|---|---|---|---|---|
| ↑ Residual degrees of freedom | 35 | 21 | 14 | 2 |
| ↑ Power, main effect at delta = sigma | 0.97 | 0.98 | 0.99 | 0.42 |
| ↑ Power, quadratic at delta = sigma | 0.82 | 0.32 | 0.46 | 0.15 |
| ↑ D-efficiency, per run | 30.5% | 28.0% | 39.3% | 39.9% |
| ↑ Information det(X'X)^(1/p) | 14.0 | 8.97 | 9.82 | 5.19 |
| ↓ Average prediction variance, sigma^2 | 0.18 | 0.31 | 0.51 | 0.71 |
| ↓ Maximum prediction variance, sigma^2 | 0.84 | 0.77 | 0.84 | 1.05 |
| ↓ Maximum scaled prediction variance, G | 38.8 | 24.6 | 20.9 | 13.6 |
| ↓ Maximum VIF | 1.20 | 3.20 | 1.00 | 1.05 |
| ↓ Maximum alias coefficient | 0.00 | 0.00 | 1.00 | 1.09 |

No design wins every row, which is the point. The per-run scores (D-efficiency, and the scaled
maximum G) put the two small designs on top; every quantity carried in real units, the unscaled
prediction variance, the power, the residual degrees of freedom, rewards the larger Box-Behnken
design. Which rows matter is set by what you will do with the result.

### Generating the table in one call

Every row above comes from a single function. Hand `process_improve`'s `evaluate_design` the coded
design matrix and the eleven-term model, and ask for the metrics you want (or `metric="all"`):

```python
import pandas as pd
from process_improve.experiments import evaluate_design

model = "A + B + C + D + E + I(A**2) + I(B**2) + I(C**2) + I(D**2) + I(E**2)"

metrics = evaluate_design(
    df,                                # coded design, columns A..E
    model=model,
    metric="all",
    effect_size=1.0, sigma=1.0,        # delta = sigma, for the power rows
    n_samples=120_000, random_seed=1,  # region sampling for the prediction variance
    include_vertices=True,             # add the cube corners, where the worst case sits
    fds_resolution=200,                # dense FDS curve for the plot
)
```

The returned object holds the power, D-efficiency, VIFs and alias matrix, and under its `fds` entry
the average and maximum prediction variance together with the dense FDS curve plotted earlier (whose
scaled column gives the per-run G value in the table). The region-sampling arguments (`n_samples`, `random_seed`,
`include_vertices`) and the dense curve (`fds_resolution`) are new in `process_improve` 1.44, so the
prediction-variance rows and the FDS figure reproduce from the same call rather than from a
hand-written integration over the region.

## Two practical rules

First, compare D-efficiency and run-count-scaled prediction variance only between designs with the
same run count. Across different run counts both favour the smaller design, so a larger-versus-smaller
decision belongs to the quantities carried in real units: average coefficient variance, unscaled
prediction variance, power, and the residual degrees of freedom you need to estimate the noise
variance and run any test at all.

Second, match the criterion to the use. Use the D-based metrics when the goal is estimating
coefficients, and I-optimality (the average prediction variance over the region) when the goal is
prediction. If the worst case matters, choose between its two forms: the unscaled maximum (the
far-right point of the unscaled FDS curve) for the variance at the bench, or G-efficiency proper,
defined on the scaled curve as the maximum run-count-scaled prediction variance, for the worst case
per experiment. These criteria often disagree, so let what you will do with the model shape the
choice.

It also helps to notice that these designs overlap. A DSD is a special case within the OMARS family,
and at the other end a face-centred CCD and a Box-Behnken design are themselves OMARS designs (their
main effects too are orthogonal to the second-order terms), so the four are better seen as points on
a spectrum than as wholly separate families.

*Figure: a spectrum of designs, rather than distinct families with fixed advantages.*

## Summary

A single efficiency score can place a 13-run design above a 46-run one precisely because it spends
fewer experiments. Hold the model and the region fixed, then choose on what the experiment has to
deliver: power to detect the effects that matter, prediction variance in real units, enough residual
degrees of freedom to test anything at all, and terms separable enough to attribute. And keep the
one assumption in view: this comparison sets the two-factor interactions aside, so it favours the
smaller designs to the extent that those interactions are negligible.

The fully worked comparison, with every design constructed and every number defined, is in the
"Judging and comparing experimental designs" chapter of my free textbook. Every figure and number
above regenerates from open Python scripts (built with the process_improve library).
