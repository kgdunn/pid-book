# Backlog

Working backlog for the book. Items prefixed `- [ ]` are open; `- [x]` are
done (kept for archive). Migrating these to GitHub Issues is slow; this file
remains the canonical short-form list.

## Site, build, and publishing

### Open

- [ ] TOC main page shows cover and 6 main TOC items instead of full TOC
- [ ] Sparkline figure in Ch1 displays at the wrong place
- [ ] Search is bad: "t-test", "paired test" produce poor results
- [ ] Cannot search for phrases at the moment
- [ ] Search does not work properly (general)
- [ ] Make images clickable to reveal code
- [ ] Add JavaScript like <https://www.scipy-lectures.org/index.html>
- [ ] Use ACE editor for HTML code snippets — <https://ace.c9.io/#nav=embedding>
- [ ] Investigate Sigil for e-book — <https://sigil-ebook.com/about/>
- [ ] Get a textbook cover for the book
- [ ] Provide "click to copy" for permalinks
- [ ] Add page title in HTML header for mobile
- [ ] How can the slides be embedded in the HTML book?
- [ ] Link to other resources from the book (code links, slide PDFs, etc.)

### Done

- [x] Check out Skyepack for publisher
- [x] Fix typo in feedback header
- [x] Add a "Provide feedback" link
- [x] Embedded R scripts in the book
- [x] Add LearnChE link to openmv.net
- [x] Show the index in HTML (it was missing)
- [x] Datasets: put the tab header in the HTML template
- [x] Add a main header to `base.html` for all dataset pages
- [x] Republish with the new dataset links added
- [x] Fix extension to handle YouTube in LaTeX
- [x] Change openmv.net URLs

## Content

### Open

- [ ] Give a paired-test example in Chapter 2
- [ ] Add more images from the Dofasco case study
- [ ] Add the "boards" data to the R package, then improve the boxplot example
      in Chapter 1 — <https://learnche.org/pid/data-visualization/data-visualization#box-plots>
- [ ] DOE / RSM chapter redone using the MOOC example
- [ ] Add the test and exam questions from the last 2–3 years
- [ ] Add assignment questions
- [ ] Add 4C3 OOI version questions
- [ ] Add an RSM website section
- [ ] Note that datasets are part of the PID R package

### Enrichment

- [ ] At the end of the Least Squares section: nonlinear regression

### Preface acknowledgements

- MacGregor
- Andy Hrymak
- Emily Nichols

### Index

- Add a line: "Please email me if there is an index entry that you would like
  to see here"
- Index entries: "randomization"; "random"

## RST / source cleanup

- [ ] Figures must have captions. To enforce that the caption stays on the
      same page, use `.. figure::` and not `.. image::`. When referencing
      figures, use `:figref:` (a directive to be created) so figures can be
      cross-referenced. Starting point:
      <https://github.com/jterrace/sphinxtr/blob/master/extensions/numsec.py>
- [ ] Right now all cross-referencing is by page number. Sometimes pages,
      sometimes section numbers are more appropriate. Fix this.
- [ ] Hyperlink handling in the print version: when referring to another
      section with a hyperlink, the print reader needs the section number
      (e.g. "(Section 3.2)"). Make this update automatically rather than by
      hand.
- [ ] Ensure page references are given for links
- [ ] For external websites, decide whether to add the URL after the hyperlink
      for print readers, or collect URLs in the References section.
      Example: ``Canadian life tables from 2002 (`Statistics Canada website
      <https://www.statcan.gc.ca/bsolc/olc-cel/olc-cel?catno=84-537-XIE&lang=eng>`_)``
      — the print reader sees only "Statistics Canada website".
- [ ] `*x*-axis` → `:math:`x`-axis`
- [ ] `make linkcheck`
- [ ] Negative numbers like `-5.5` must be formatted as `:math:`
- [ ] Use `\cdot` in units like `mol.K-1`
- [ ] Consistency with `|x|` and roman vs italic `x`s

## HTML publishing checklist

- [ ] Check figure aspect ratios
- [ ] MathJax renders OK
- [ ] Cross-reference links to sections work
- [ ] Links to the index work
- [ ] Search results are reasonable

## Tooling links to investigate

- Better referencing: <https://github.com/sphinx-doc/sphinx/issues/326>
- Sea-level fitting example dataset:
  <https://www.epa.gov/climate-indicators/climate-change-indicators-sea-level>
- Better search results plugin:
  <https://github.com/TimKam/sphinx-pretty-searchresults>
- Custom admonition styling (centered, uppercase title):

  ```latex
  \makeatletter
  % Update all the admonitions we use to be centered  (not all shown here)
  \renewcommand{\py@noticestart@warning}{\py@heavybox\begin{center}}
  \renewcommand{\py@noticeend@warning}{\end{center}\py@endheavybox}
  \makeatother

  \renewenvironment{notice}[2]{
    \def\py@noticetype{#1}
    \csname py@noticestart@#1\endcsname
    % Make the admonition type be upper case and on its own line
    \strong{\MakeUppercase{#2}} \\
  }{\csname py@noticeend@\py@noticetype\endcsname}
  ```

---

## Reference material: MOOC discussions

The material below is verbatim Q&A from Coursera and LinkedIn threads, kept
here as raw source for future exercises and worked examples in the book.

### DoE success factors (LinkedIn discussion, Phil Kay)

> Phil Kay — Enabling Excellence in Analytics
>
> **3 most important factors for DoE success?** What, in your experience, are
> the most important factors for DoE to be successful in a company? I'm
> thinking at an organisation level, rather than what it takes for an
> individual to be successful. What does it take for DoE to become the
> default approach to experimentation within a company?

**Phil Kay:** Yes, there is often a "guru". They will often tell you that
their process is unique and only they are capable of understanding it. Gurus
have told me "DoE is great but I know this process and I know that, for
reasons you wouldn't understand, DoE will not work here." Then, after a lot
of persuasion, a designed experiment is run and it proves very useful in
understanding the process. The guru replies "yes, well I could have told that
before you did the DoE". (!)

I have exaggerated a bit there. But there will probably always be gurus.
They need to be persuaded that DoE augments and relies upon their expertise,
it does not replace them. How do some companies create a culture that brings
the gurus along on the journey of using DoE?

**Jonathan Smyth-Renshaw:** I see a gap between the DOE statistical packages
and the needs of business. I use Plackett and Burman 8-run, which is very
good for industrial experiments, but it is not in the packages, so I use
Excel and build a model, which is not statistically great, but in the
industrial setting it works. I have raised this a number of times but no one
listens.

**Josef Betschart:** If only a guru is leading DoE, your success is very
limited. I strongly recommend doing it in teams — not only because a team
has more knowledge of a process, but it also has wider access to key people
and has a better lobby.

**Seamus Clifford:** Main barriers and solutions I have come across:

1. Companies do not want to give up production time for the experiment due
   to production deadlines and cost. A cost–benefit analysis and timely
   experimental pre-planning helps make the argument.
2. Lack of knowledge of DOE and what it can do. We always present the
   technique to the client and demonstrate clearly what single-factor
   experimentation cannot do that DOE can.
3. We do an exercise with the client involving a problem statement, a
   process / product factor analysis and a factor sensitivity analysis (VMEA
   — variation mode and effect analysis). This draws a clear line between
   the tacit knowledge the client already has and the new knowledge that
   will be created (helpful when IP arises from the work).

Once a client company sees a successful outcome from DOE, it becomes more
acceptable.

**George S. Baggs:** I've seen hesitation from people that fear failure if
they use this 'different' approach. Unequivocal support from senior
management is a must, and clear understanding that the company expects these
techniques to be used.

**Phil Kay (closing):** From what Josef and Seamus have said, it is not
enough just to have individual experts/champions. You need a larger group of
people who are inspired by learning from each other and from examples
outside of the organisation.

### Mixture design (Coursera)

Source: <https://www.coursera.org/learn/experimentation/discussions/all/threads/Uqm0xMSpEeeFcw6gQymyng?sort=createdAtDesc>

**Question:** I would like to optimize the diet for an organism. The diet
consists of five main components (= five factors). These factors add up to
96.9% of the diet. The remaining 3.1% are constant between the diets. In
contrast to examples presented in the course, this is a mixed design
problem: when changing one factor I automatically have to change another
(because all factors have to make up 96.9% and the mass has to stay the
same). It is basically like baking a cake with five ingredients.

I would like to design a pre-screening to identify which of the factors has
the largest influence on my response (e.g. growth of the organisms). Maybe a
half-factorial design with five factors and at least two levels. Next I might
continue with three parameters to further optimize the diet. I have a lot of
books for mixed design / design for formulation, and there is an R package
(`mixep`) for the design of such experiments. However, I find transferring
the knowledge from this course difficult to such a question.

**Answer:** You are definitely in the area of mixture design for your
particular application. As you rightly point out, in those designs, when you
change one factor, you need to also alter the others. The ratios change, and
you have the constraint that everything must sum to 100%.

The topics covered in this course have as a prerequisite that you can adjust
the factors A, B, C, etc. all independently of each other. That is not the
case with mixture designs. So it is not surprising that you came to the
conclusion that "transferring the knowledge from this course is difficult to
such a question."

I will also apologize here for not ever making that clear at the very start
of this course. It is mentioned at the end of the textbook chapter, where a
very superficial example is given.

Not all is lost: many of the concepts from this course are applicable in
mixture designs, once you recognize the constraint in the system.

### Three-level factors (Coursera)

Source: <https://www.coursera.org/learn/experimentation/discussions/all/threads/hkhGQcruEee2MhJYIYQTJg>

**Question:** What if a factor has three instead of two levels? How would
you approach such a system? Will this be covered in one of the courses or a
particular R code? For example, a factor that contains morning, evening and
night.

**Answer:** Hi Wyona, at its simplest, three levels can, for example, be
coded as $-1, 0, +1$ if they are numeric and the spacing between them is
equidistant.

In the case of morning, evening and night, you might still be able to code
them that way if it is simply a matter of interpreting the results. You
might find night > evening > morning, for example (you can rank the 3
levels).

But perhaps it can't be ranked, or ranking is meaningless and the factor
simply has 3 (unrelated) states. Then you can add two artificial factors,
A and B. With these 2 factors you can create 4 combinations, though you only
need 3:

- $A=-1$ and $B=-1$ represents morning
- $A=+1$ and $B=-1$ represents evening
- $A=-1$ and $B=+1$ represents night
- $A=+1$ and $B=+1$ is not used

### Confounded effects with opposite signs (Coursera)

Source: <https://www.coursera.org/learn/experimentation/discussions/all/threads/qzotObslEeeb_xL-a3Jo7A>

**Question:** Is it possible for a main effect to be confounded with an
interaction term with the opposite sign, thus making it look like the effect
is unimportant? For example, in the 7-factor resolution-III example in video
4H, after the initial analysis we remove factors B, D, and F because they
have relatively small effects. But since those factors are all confounded
with three two-factor interactions each, don't we run the risk of
accidentally removing important factors that seem small due to confounding?

Quick example: factor B is confounded with AD, CF, and EG. If we made up
some values such as B = +20, AD = -10, CF = -7, EG = -3, then B would look
like 0 and not significant even though the "pure" value of B is very
significant. How do we prevent this from happening?

**Answer:** Yes — there is a real concern, especially with resolution-III
systems (main effects confounded with two-factor interactions). It can
cancel out the main effect, but it can also go the other way and make a
factor appear important when it is actually one or some of the confounded
factors. That is the risk of a resolution-III system, and it is better that
you know that risk up front.

What can you practically do about it?

1. Choose your allocation of factors so that confounding is benign. For
   example, if B is confounded with AC, pick A and C to be factors that
   you know cannot actually interact to affect the outcome. (E.g. with
   A = tire pressure, C = windows open/closed, and y = gas mileage, those
   simply cannot interact.)
2. Choose another experimental setup, such as a resolution-IV design, when
   you suspect two-factor interactions of a similar magnitude to the main
   effects. Or consider a Definitive Screening Design (<https://yint.org/dsdesign>).

There is a chicken-and-egg situation: you don't know up front if the effects
are similar in magnitude until you do the experiments. A bit of single-factor
experimentation can help. It is also why we said not to spend all your
budget on experiments in one go: do some, get a feeling, learn, and repeat.

### Coded values 1.38 vs 1.41 (Coursera)

Source: <https://www.coursera.org/learn/experimentation/discussions/all/threads/Agsw3IdfEeeNeRJP10SOQA?sort=createdAtDesc>

**Question:** Why do the coded values for price range from −1.38 to 1.38, as
opposed to −1.41 to 1.41 as in throughput? Why ±1.38 and not, say, ±1.42?
Would using ±1.38 vs ±1.41 materially affect the conclusion?

**Answer:** We aim for a coded value of $\pm 1.41$ and calculate what the
real-world values would be. But it might not be possible to actually
implement that real-world value. Take an example (see video 5G at 11:30):
factor T, centre point 339K, range = 342 − 336 = 6K. Real-world 342K is +1
in coded units: $\dfrac{342 - 339}{0.5 \times 6} = \dfrac{3}{3} = +1$.

To aim for a coded value of $+1.41$, that corresponds to $T = 343.2K$. In
practice we cannot achieve that, because the system can only implement
integer Kelvin. The closest integer is 343K, which in coded units is 1.33.
Not exact, but close.

### A/B testing sample size (Coursera)

Source: <https://www.coursera.org/learn/experimentation/discussions/all/threads/ha45NHhvEeeBRg5FFlUzqg>

**Question:** What is the minimum sample size per experimental run needed
to draw statistically significant conclusions in MVT (multivariate
testing)?

**Answer:** It cannot be answered in a general way: it depends on the
system. With website sales/marketing it can take a long time to see a
noticeable effect (lots of noise). For example, in 100 customers at
condition $-1$, 7% might purchase, vs. 10% at condition $+1$. Repeat the
experiment and you might see 9% vs. 8.5%. There isn't a clear signal, so
you have to acquire many customers and wait for clarity to show up.

But in some (often engineering) systems you see a clear signal right away
with little noise — especially when you have good control. Then you might
just need 1 experiment at each condition.

We intentionally don't cover this topic in the course, because it is left
to your detailed knowledge of the system (noise level, repeatability, etc.)
to judge whether you are getting significant results.

### Local vs global RSM optima (Coursera)

Source: <https://www.coursera.org/learn/experimentation/discussions/all/threads/diWGQcbPEeemvAoyMa4lng>

**Question:** The procedure of finding the optimum was illustrated. The
example of Mount Fuji triggered this question: we see a local optimum on
the mountain next to the real highest top. How do we make sure we are
finding the global maximum? If experiments are located around the local
optimum we may never find the real top of the mountain.

**Answer:** The method shown in the course is not a global optimization
method: we cannot guarantee you will avoid a local optimum. However, when
we run these experiments and optimize, we operate over the range of
interest of the factors. There could be a better optimum outside the
range, but it might not be accessible. On systems we have run experiments
on before, we might have built up knowledge about the smoothness of the
surface and the likelihood that multiple optima exist.

Starting from another position can potentially identify another optimum
that was not discovered the first time, but there is no guarantee, and it
is expensive — especially if you automate the response-surface routine. If
you do it manually (sitting in the middle of the data and using your
brain), you can steer it into another direction when you encounter a saddle
point.

In engineering systems, complete areas are often off-limits (e.g. for
safety reasons). So while there might be a better optimum there, it is
technically unachievable. Use the experience of people who have worked
with the systems before. Look back at historical data — sometimes a system
moves into a whole new set of conditions for the factors by mistake or due
to an accident, and a better optimum is noticed.

### Steepest ascent from highest point (RSM)

**Question:** For RSM, why do we not initiate the path of steepest ascent
from the point with the highest outcome ($y$) value, instead of from the
baseline point?

**Answer:** Strictly speaking, the direction of steepest ascent is a ratio
of gradients:

$$\dfrac{\Delta x_A}{\Delta x_B} = \dfrac{b_A}{b_B}
= \dfrac{\partial y / \partial x_A}{\partial y / \partial x_B}$$

— the partial derivatives at the $(0, 0)$ tangent plane. This ratio is exact
at the origin. At the point of highest outcome, the partial derivatives have
to take the value of the other variable(s) into account, so the ratio will
only be approximate. I suspect you won't be off by very much if you start at
the point of the highest outcome, but I haven't tested it thoroughly.

### Nelder–Mead vs RSM

The Nelder–Mead algorithm moves around the response surface in a way that
reminds you of the 4C approach. As with RSM (Response Surface Method)
learned in 4C, we never actually know what the true function $f(x)$ is.

Distinctions:

- Use Nelder–Mead when you just want to get to an optimum, no matter how,
  without really understanding the process.
- The RSM approach in 4C is more subtle: we place a premium on doing a
  minimum number of function evaluations. Nelder–Mead, as the animations
  show, simply does a brute-force investigation, and can easily lead to over
  100 function evaluations in 2 variables.
- 4G makes a big deal about derivatives. Nelder–Mead doesn't even try to
  approximate derivative information to assist its search. In 4C, by
  calculating a search direction $\dfrac{\Delta x_A}{\Delta x_B} = \dfrac{b_A}{b_B}$
  we are approximating a slope going up the steepest direction (gradient).
  That estimate of the derivatives is how RSM gains an advantage in fewer
  steps.
- Termination: Nelder–Mead terminates when the simplex size gets small and
  the function values are close to each other. RSM is more subtle: we fit
  quadratic surfaces and use that local model at the optimum to assert we
  have achieved our goal.

There's a place for both, mostly distinguished by how much prior knowledge
you have about the system and the cost of function evaluations.
