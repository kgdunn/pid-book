Box plots
==========

.. youtube:: https://www.youtube.com/watch?v=LumUy2F_DRc&list=PLHUnYbefLmeOPRuT1sukKmRyOVd4WSxJE&index=2

:index:`Box plots <pair: box plot; visualization>` are an efficient summary of one variable (univariate chart), but can also be used effectively to compare like variables that are in the same units of measurement.

The box plot shows the so-called *five-number summary* of a univariate data series: 

1. Minimum sample value
2. 25th `percentile <https://en.wikipedia.org/wiki/Percentile>`_ (1st `quartile <https://en.wikipedia.org/wiki/Quartile>`_)
3. 50th percentile (median)
4. 75th percentile (3rd quartile)
5. Maximum sample value

The 25th percentile is the value below which 25% of the observations in the sample are found. The distance from the 3rd to the 1st quartile is also known as the interquartile range (IQR) and represents the data's spread, similar to the standard deviation.

The following data are thickness measurements of 2-by-6 boards, taken at six locations around the edge. Here is a sample of the measurements and a summary of the first 100 boards (created in ``R``):

.. code-block:: text


  > all.boards <- read.csv('http://openmv.net/file/six-point-board-thickness.csv')
  > boards <- all.boards[1:100, 2:7]
  > boards 
  

	    Pos1 Pos2 Pos3 Pos4 Pos5 Pos6
	1   1761 1739 1758 1677 1684 1692
	2   1801 1688 1753 1741 1692 1675
	3   1697 1682 1663 1671 1685 1651
	4   1679 1712 1672 1703 1683 1674
	5   1699 1688 1699 1678 1688 1705
        ....
	96  1717 1708 1645 1690 1568 1688
	97  1661 1660 1668 1691 1678 1692
	98  1706 1665 1696 1671 1631 1640
	99  1689 1678 1677 1788 1720 1735
	100 1751 1736 1752 1692 1670 1671

  > summary(boards)
         Pos1           Pos2           Pos3           Pos4           Pos5           Pos6
    Min.  :1524   Min.  :1603   Min.  :1594   Min.  :1452   Min.  :1568   Min.  :1503
    1st Qu.:1671   1st Qu.:1657   1st Qu.:1654   1st Qu.:1667   1st Qu.:1662   1st Qu.:1652
    Median :1680   Median :1674   Median :1672   Median :1678   Median :1673   Median :1671
    Mean   :1687   Mean   :1677   Mean   :1677   Mean   :1679   Mean   :1674   Mean   :1672
    3rd Qu.:1705   3rd Qu.:1688   3rd Qu.:1696   3rd Qu.:1693   3rd Qu.:1685   3rd Qu.:1695
    Max.  :1822   Max.  :1762   Max.  :1763   Max.  :1788   Max.  :1741   Max.  :1765
	
  > boxplot(boards)	


.. _visualization_boxplot_example:

The following box plot is a graphical summary of these numbers.

.. image:: ../figures/visualization/boxplot-for-two-by-six-100-boards.png
	:align: right
	:scale: 40
	:width: 900px
	:alt: fake width

Some variations for the box plot are possible:

- Show outliers as dots, where an outlier is most commonly defined as any point 1.5 IQR distance units away from the box. The box's upper bound is at the 25th percentile, and the boxes lower bound is at the 75th percentile.
- The whiskers on the plots are drawn *at most* 1.5 IQR distance units away from the box, however, if the whisker is to be drawn beyond the bound of the data vector, then it is redrawn at the edge of the data instead (i.e. it is clamped, to avoid it exceeding).
- Use the mean instead of the median [*not too common*].
- Use the 2% and 98% percentiles rather than the upper and lower hinge values.
