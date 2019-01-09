.. _DOE-fractional-factorials:

Fractional factorial designs
===========================================

When there are many factors that we have identified as being potentially important, then the :math:`2^k` runs required for a full factorial can quickly become large and too costly to implement.

For example, you are responsible for a cell-culture bioreactor at a pharmaceutical company and there is a drive to minimize the production of an inhibiting by-product. Variables thought to be related with this by-product are: two types of **T** = temperature profile (:math:`T_{-}`: a slow ramp over time or :math:`T_{+}` a fast initial ramp then constant temperature), the **D** = dissolved oxygen at a low and high level, the **A** = agitation rate at a slow and faster speed, **P** = pH at a low and high level, and two blends of **S** = substrate type. These five factors, at two levels, require :math:`2^5 = 32` runs. It would take almost a year to collect the data at all the combinations of **T**, **D**, **A**, **P** and **S** if each experiment requires 10 days (typical in this industry), and if parallel reactors are not available.

Furthermore, we are probably interested in only the 5 main effects and 10 two-factor interactions (2fi). The remaining 10 three-factor interactions, 5 four-factor interactions, a single five-factor interaction are likely not too important either, at least initially. A full factorial would estimate 32 effects, even if we likely only interested in at most 16 of them (5 main effects + 10 of the 2fi's + 1 intercept).

Running a half fraction, or quarter fraction, of the full set will allow us to estimate the main effects and two-factor interactions (2fi) in many cases, at the expense of *confounding* the higher interactions. [We will explain exactly what is meant by that term *confounding* later on, but for now you can interpret it is as 'confused with'].

For many real systems it is the main effects that are mostly of interest, and at most two-factor interactions. Very very seldom do three-factor interactions occur, nor are they often of practical significance. As such, we are willing to allow some confounding (confusing) with these factors.

So let's move into this section where we show how to construct and analyze these :index:`fractional factorials <pair: fractional factorial; experiments>`, which are tremendously useful when :index:`screening <pair: screening designs; experiments>` many variables - especially for a first-pass at experimenting on a new system. They are used when you, as the experimenter, suspect that you have more factors on your list than are actually needed. Which ones can you eliminate?

.. toctree::
   :maxdepth: 2

   half-fractions
   Generators, defining-relationships, and blocking <generators-defining-relationships-blocking>
   highly-fractionated-designs
   design-resolution
   saturated-designs-for-screening
   design-foldover-and-projectivity
