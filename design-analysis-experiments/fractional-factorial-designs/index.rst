.. _DOE-fractional-factorials:

Fractional factorial designs
===========================================

When there are many factors that we have identified as being potentially important, then the :math:`2^k` runs required for a full factorial can quickly become large and too costly to implement.

For example, you are responsible for a cell-culture bioreactor at a pharmaceutical company and there is a drive to minimize the production of an inhibiting  by-product. Variables known to be related with this by-product are: the temperature profile (:math:`T_{-}`: a fast initial ramp then constant temperature or :math:`T_{+}` a slow ramp over time), the dissolved oxygen, the agitation rate, pH, substrate type. These five factors, at two levels, require :math:`2^5 = 32` runs. It would take almost a year to collect the data when each experiment requires 10 days (typically in this industry), and parallel reactors are not available.

Furthermore, we are probably interested in only the 5 main effects and 10 two-factor interactions. The remaining 10 three-factor interactions, 5 four-factor interactions, a single five-factor interaction are likely not too important, at least initially. A full factorial would estimate 32 effects, even if we likely only interested in at most 16 of them (5 + 10 + 1 intercept).

Running a half fraction, or quarter fraction, of the full set will allow us to estimate the main effects and two-factor interactions (2fi) in many cases, at the expense of confounding the higher interactions. For many real systems it is these main effects that are mostly of interest. In this section we show how to construct and analyze these :index:`fractional factorials <pair: fractional factorial; experiments>`, which are tremendously useful when :index:`screening <pair: screening designs; experiments>` many variables - especially for a first-pass at experimenting on a new system.


.. toctree::
   :maxdepth: 2

   half-fractions
   Generators, defining-relationships, and blocking <generators-defining-relationships-blocking>
   highly-fractionated-designs
   design-resolution
   saturated-designs-for-screening
   design-foldover-and-projectivity