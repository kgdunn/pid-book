"""Build a minimal DOE knowledge graph from the chapter text in ../doe_extracted_text.txt.

Nodes and edges are written by hand from that text; each node carries the book section that
teaches it, checked against a pid-book checkout (this repository by default, or the path given).
Outputs doe_kg.json and doe_kg.cypher next to this script.

Run with: python build_kg.py [path-to-pid-book]
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

BOOK = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
OUT = Path(__file__).parent
CHAPTER = "design-analysis-experiments"

# Where each node is taught: a book label, or a file when the section has no label.
REFS = {
    "terms": "file:design-analysis-experiments.rst",
    "usage": "file:examples-of-how-designed-experiments-are-used.rst",
    "refs": "DOE_references",
    "learn": "DOE_learning_about_systems",
    "causal": "DOE-yield-pressure-impurity-correlation",
    "single": "DOE_expts_with_single_variable",
    "random": "DOE-randomization",
    "cost": "DOE-COST-approach",
    "ff": "DOE-two-level-factorials",
    "me": "DOE-two-level-factorials-main-effects",
    "ie": "DOE-two-level-factorials-interaction-effects",
    "ls": "DOE-analysis-by-least-squares",
    "orth": "DOE_orthogonality",
    "pareto": "DOE-Pareto-plot",
    "rep": "DOE-replicate_points",
    "eff": "DOE-COST-vs-factorial-efficiency",
    "ex3": "file:full-factorial-designs/example-design-and-analysis-of-a-three-factor-experiment.rst",
    "summary": "file:full-factorial-designs/summary-so-far.rst",
    "frac": "DOE-fractional-factorials",
    "half": "DOE-half-fractions",
    "gen": "DOE-generators",
    "blkgen": "DOE-Generators-for-blocking",
    "high": "DOE-highly-fractionated-designs",
    "res": "DOE-design-resolution",
    "tradeoff": "DOE_design_trade_off_BHH_272",
    "sat": "DOE-saturated-screening-designs",
    "fold": "DOE-foldover-designs",
    "proj": "file:fractional-factorial-designs/design-foldover-and-projectivity.rst",
    "block": "DOE-Blocking-and-confounding",
    "rsm": "DOE-RSM",
    "ccd": "DOE_central_composite_designs",
    "evop": "DOE-EVOP",
    "general": "DOE-general-approach",
    "ext": "file:extended-topics-related-to-designed-experiments.rst",
    "constr": "DOE-handling-constraints",
    "opt": "DOE-optimal-designs",
    "dsd": "DOE-definitive-screening-designs",
    "mix": "DOE-mixture-designs",
}

# (id, name, type, ref, definition, aliases)
N = [
    # --- Learning about systems
    ("experiment", "Experiment", "Concept", "terms", "Intentionally disturbing a system by changing factors, to learn cause and effect.", []),
    ("run", "Run", "Concept", "terms", "One experiment in a set: eight experiments are eight runs.", ["experimental run"]),
    ("response", "Response", "Concept", "terms", "The measured outcome of a run, written y. It must always be measurable in some way.", ["outcome", "response variable", "y"]),
    ("qualitative_outcome", "Qualitative outcome", "Concept", "terms", "An outcome described in categories, such as pass or fail, or a colour.", []),
    ("objective", "Objective", "Concept", "terms", "An outcome together with what you want of it: maximize, minimize, or keep the same.", ["goal"]),
    ("factor", "Factor", "Concept", "terms", "The thing you can change to influence the outcome.", ["variable", "input"]),
    ("numeric_factor", "Numeric factor", "Concept", "terms", "A factor with ordered, measured values, such as 15 mL or 30 mL of water.", ["quantitative factor", "continuous factor"]),
    ("categorical_factor", "Categorical factor", "Concept", "terms", "A factor with a few values that have no order, such as soil A or soil B.", ["qualitative factor"]),
    ("level", "Level", "Concept", "ff", "A setting of a factor in a design, such as its low (-1) or high (+1) value.", ["low level", "high level"]),
    ("cause_and_effect", "Cause and effect", "Concept", "learn", "A change in a factor that produces a change in the response; shown only by intentional manipulation.", ["causality"]),
    ("happenstance_data", "Happenstance data", "Concept", "learn", "Everyday operating data, collected without intentional changes; it cannot show cause and effect.", ["operating data"]),
    ("feedback_control", "Feedback control", "Concept", "learn", "Control systems keep operation in a small zone, so the data they produce carry little information.", []),
    ("correlation", "Correlation", "Concept", "causal", "Two variables moving together: necessary, but not sufficient, for causality.", []),
    ("learning_cycle", "Learning cycle", "Concept", "learn", "Conjecture, expected consequences, experiment and data, then a new or revised conjecture.", ["iterative learning"]),
    ("conjecture", "Conjecture", "Concept", "learn", "A hypothesis believed true, whose consequences an experiment tests.", ["hypothesis"]),
    ("troubleshooting", "Troubleshooting", "Concept", "learn", "Experimenting to fix a problem, which also teaches you about the system.", []),
    ("disturbance", "Disturbance", "Concept", "block", "A variable that affects y but is not of interest: operators, ambient conditions, equipment, lab analyses, time.", []),
    ("controlled_disturbance", "Controlled disturbance", "Concept", "block", "A disturbance held constant for all runs, so its effect cancels out.", []),
    ("time_effect", "Time-dependent effect", "Concept", "block", "Slow changes such as catalyst deactivation or fouling that affect the response over time.", ["drift"]),
    # --- One factor at two levels, and randomization
    ("randomization", "Randomization", "Concept", "random", "Running experiments in random order so unknown disturbances cannot systematically affect the response.", ["random order"]),
    ("independence", "Independence", "Concept", "random", "The assumption behind t-based confidence intervals; randomization guarantees it.", []),
    ("randomization_test", "Randomization test", "Method", "random", "Compare the observed difference with the differences from every possible reassignment of the A and B labels.", ["permutation test"]),
    ("pairing", "Pairing", "Method", "single", "Running two experiments on the same subject and analysing their difference, so a shared disturbance cancels.", []),
    ("two_group_comparison", "Comparing two conditions", "Method", "single", "Comparing condition A with B using a pooled variance and a confidence interval for the difference.", ["A versus B test"]),
    ("pooled_variance", "Pooled variance", "Concept", "single", "A combined variance estimate from two groups, used in the z-value for their difference.", []),
    ("indicator_variable", "Indicator variable", "Concept", "single", "A 0/1 variable that codes condition A or B in a least squares model.", ["dummy variable"]),
    ("confidence_interval", "Confidence interval", "Concept", "single", "A range for an effect; the effect is statistically significant when the interval does not span zero.", []),
    ("t_distribution", "t-distribution", "Concept", "single", "The reference distribution for a difference or a coefficient divided by its standard error.", []),
    ("null_hypothesis", "Null hypothesis", "Concept", "random", "The assumption that there is no difference between A and B.", []),
    ("statistical_significance", "Statistical significance", "Concept", "single", "An effect larger than the noise, judged by its confidence interval.", []),
    ("practical_significance", "Practical significance", "Concept", "single", "Whether an effect is large enough to matter, judged from the interval's width and the process variance.", []),
    # --- One factor at a time
    ("cost", "Changing one single variable at a time", "Method", "cost", "Changing one factor at a time: an inefficient way to experiment that can stop at a suboptimal point.", ["COST", "OFAT", "one factor at a time"]),
    ("false_optimum", "False optimum", "Concept", "cost", "A point that looks best when factors are changed one at a time, but is not the optimum.", ["suboptimal solution"]),
    ("order_dependence", "Order dependence", "Concept", "cost", "With COST the result depends on which factor is changed first.", []),
    ("designed_experiment", "Designed experiment", "Concept", "cost", "A planned set of runs that changes several factors together, in random order, so the result does not depend on run order.", ["DOE", "design of experiments", "experimental design"]),
    # --- Full factorials
    ("full_factorial", "Full factorial", "DesignType", "ff", "Every combination of the factors' two levels: 2^k runs for k factors.", ["2^k factorial", "two-level factorial"]),
    ("coding", "Coding", "Concept", "ls", "Centering and scaling a factor: (value - center)/(range/2), so low is -1 and high is +1.", ["coded units", "centering and scaling"]),
    ("standard_order", "Standard order", "Concept", "ff", "Writing runs with the first factor's sign alternating fastest and the last slowest.", ["Yates order"]),
    ("operating_range", "Choosing the factor range", "Guideline", "ff", "Choose low and high at the edges of normal operation, not at the extreme values a factor could take.", []),
    ("cube_plot", "Cube plot", "Plot", "ff", "The design drawn as a square or cube with the response written at each corner.", []),
    ("main_effect", "Main effect", "Concept", "me", "The average change in y when a factor moves from its low to its high level.", ["effect"]),
    ("interaction", "Interaction", "Concept", "ie", "When the effect of one factor depends on the level of another. Interactions are symmetric.", ["interaction effect"]),
    ("two_factor_interaction", "Two-factor interaction", "Concept", "ie", "The interaction of two factors, such as T x S.", ["2fi"]),
    ("three_factor_interaction", "Three-factor interaction", "Concept", "ex3", "The interaction of three factors; seldom large in real systems.", ["3fi"]),
    ("interaction_plot", "Interaction plot", "Plot", "ie", "The response against one factor, a line per level of another; lines that are not parallel show interaction.", []),
    ("half_range_effect", "Effect over half the range", "Concept", "ex3", "This book reports an effect as the change over half the factor's range; Box, Hunter and Hunter report double.", []),
    ("least_squares_model", "Least squares model", "Method", "ls", "y = Xb + e, fitted with b = (X'X)^-1 X'y. It works even when the design was not run exactly as planned.", ["linear model", "regression"]),
    ("model_matrix", "Model matrix X", "Concept", "ls", "One row per run and one column per model term, with a column of ones for the intercept.", ["X matrix", "design matrix"]),
    ("orthogonality", "Orthogonality", "Property", "orth", "The columns of X are independent, so X'X is diagonal and each coefficient is estimated and read on its own.", ["orthogonal design"]),
    ("intercept", "Intercept", "Concept", "ls", "The model's constant b0; for a coded factorial, the average of the runs and the predicted center point.", ["b0"]),
    ("coefficient", "Coefficient", "Concept", "ls", "The change in y for a one-unit change in a coded factor, that is, over half its range.", ["parameter", "slope"]),
    ("hierarchy_rule", "Keep the parent main effects", "Guideline", "summary", "If an interaction is significant, keep in the model every main effect that it is made of.", ["model hierarchy"]),
    ("interpret_with_interaction", "Read main effects with their interactions", "Guideline", "summary", "A main effect cannot be interpreted on its own when it takes part in a significant interaction.", []),
    ("robustness", "Robustness", "Concept", "summary", "A small effect means y is insensitive to that factor: y is robust to changes in it.", []),
    ("degrees_of_freedom", "Degrees of freedom", "Concept", "rep", "Runs minus estimated parameters; needed to estimate the standard error.", []),
    ("replicate", "Replicate", "Concept", "rep", "A complete repeat of a run: setup, running the experiment and measuring the result.", ["replication"]),
    ("repeat_measurement", "Repeat measurement", "Concept", "rep", "Measuring one sample twice; it estimates only measurement error and is not a true replicate.", []),
    ("center_point", "Center point", "Concept", "rep", "A run with every factor at coded 0. It tests curvature and adds degrees of freedom without breaking orthogonality.", ["centre point", "baseline run"]),
    ("standard_error", "Standard error", "Concept", "rep", "The noise estimate from the residuals; for a coefficient, SE(b) = sqrt(S_E^2 / sum x^2).", []),
    ("pareto_plot", "Pareto plot", "Plot", "pareto", "Absolute coefficients in sorted order, intercept left out; significance judged by eye. Needs coded factors.", []),
    ("se_significance", "Significance from standard errors", "Method", "rep", "Report each effect with its standard error; it is significant when effect +/- c_t x SE excludes zero.", []),
    ("refit", "Refit without small effects", "Method", "rep", "Drop clearly small effects to gain degrees of freedom, then estimate the error and check the residuals.", ["model reduction"]),
    ("residual_analysis", "Residual analysis", "Method", "rep", "Residuals plotted in run order, against fitted values, and on a q-q plot.", ["residual plots"]),
    ("factorial_efficiency", "Factorial efficiency", "Property", "eff", "A factorial estimates a main effect with half the variance of COST: each observation works twice.", []),
    ("missing_values", "Missing values", "Concept", "ext", "Lost responses. Drop high-order terms so the model can still be fitted by least squares.", []),
    ("off_target_run", "Off-target run", "Concept", "ext", "A run set to a level other than planned. Code its actual value and fit by least squares; X is then almost orthogonal.", []),
    # --- Fractional factorials
    ("fractional_factorial", "Fractional factorial", "DesignType", "frac", "A fraction of a full factorial: 2^(k-p) runs for k factors.", ["2^(k-p) design"]),
    ("half_fraction", "Half fraction", "DesignType", "half", "Half of a full factorial: 2^(k-1) runs.", []),
    ("quarter_fraction", "Quarter fraction", "DesignType", "high", "A quarter of a full factorial: 2^(k-2) runs.", []),
    ("complementary_fraction", "Complementary half fraction", "DesignType", "gen", "The other half of a full factorial, made by flipping the sign of the generator.", []),
    ("saturated_design", "Saturated design", "DesignType", "sat", "A design with one run per estimated term, such as 7 factors in 8 runs; usually resolution III.", []),
    ("plackett_burman", "Plackett-Burman design", "DesignType", "sat", "A screening design in any multiple of 4 runs from 12: 12, 16, 20, 24, ...", ["PB design"]),
    ("confounding", "Confounding", "Concept", "half", "Two effects cannot be separated, so their coefficient estimates their sum.", ["confusing"]),
    ("alias", "Alias", "Concept", "half", "An effect confounded with another: A is an alias of BC.", ["aliasing"]),
    ("alias_structure", "Alias structure", "Concept", "gen", "The list of aliases of every effect in a design.", ["confounding pattern"]),
    ("collinearity", "Collinearity", "Concept", "half", "Identical columns in X, so X'X cannot be inverted.", []),
    ("generator", "Generator", "Concept", "gen", "Assigning an extra factor to an interaction column, such as D = ABC.", ["generating relation"]),
    ("word", "Word", "Concept", "high", "A product of factor letters equal to I, such as ABD.", []),
    ("defining_relation", "Defining relation", "Concept", "gen", "All the words equal to I, found from the products of the generators: 2^p words.", ["defining relationship"]),
    ("identity_column", "Identity column I", "Concept", "gen", "The column of ones. Any factor times itself is I.", []),
    ("alias_calculation", "Finding aliases", "Method", "gen", "Multiply an effect by the defining relation to list what it is aliased with.", []),
    ("reassign_letters", "Reassign factors to letters", "Guideline", "high", "Choose which real factor gets which letter to obtain the least harmful confounding.", []),
    ("resolution", "Resolution", "Property", "res", "The length of the shortest word in the defining relation, written as a Roman numeral.", ["design resolution"]),
    ("resolution_iii", "Resolution III", "Property", "res", "Main effects are aliased with two-factor interactions. Good for screening.", []),
    ("resolution_iv", "Resolution IV", "Property", "res", "Main effects are clear of two-factor interactions, which are aliased with each other. Good for characterizing.", []),
    ("resolution_v", "Resolution V", "Property", "res", "Two-factor interactions are clear of each other. Good for optimizing.", []),
    ("trade_off_table", "Trade-off table", "Concept", "tradeoff", "Resolution against number of factors and runs (Box, Hunter and Hunter, p 272).", []),
    ("projectivity", "Projectivity", "Property", "proj", "A design of resolution R contains a full factorial in any R - 1 factors.", []),
    ("foldover", "Foldover", "Method", "fold", "Running a second fraction with signs switched, then analysing both fractions together.", []),
    ("single_factor_foldover", "Single-factor foldover", "Method", "fold", "Switch the signs of one factor to de-alias it and its two-factor interactions.", ["switch one sign"]),
    ("full_foldover", "Full foldover", "Method", "fold", "Switch all signs to raise a resolution III design to resolution IV.", ["switch all signs"]),
    ("sequential_experimentation", "Sequential experimentation", "Concept", "general", "Experiments are run in stages, each designed from what the last one revealed.", []),
    ("screening", "Screening", "Concept", "sat", "Finding the few important factors among many candidates.", []),
    ("effect_sparsity", "Few large effects", "Concept", "frac", "Main effects matter most, then two-factor interactions; three-factor interactions are seldom large.", ["effect hierarchy", "sparsity of effects"]),
    # --- Blocking
    ("blocking", "Blocking", "Method", "block", "Running the experiment in groups so a known disturbance affects the response without misleading the results.", []),
    ("block", "Block", "Concept", "block", "A group of runs made under one level of a disturbance, such as one batch of material. Runs within a block are randomized.", []),
    ("block_generator", "Block generator", "Concept", "blkgen", "The interaction the block effect is confounded with, such as block = ABC.", []),
    ("block_on_highest", "Block on the highest interaction", "Guideline", "blkgen", "Confound the block effect with the highest-order interaction, which is expected to be small.", []),
    # --- Response surface methods
    ("rsm", "Response surface methods", "Method", "rsm", "A sequential way to move a process towards its optimum by fitting and climbing local models.", ["RSM", "response surface methodology"]),
    ("response_surface", "Response surface", "Concept", "rsm", "The unknown surface of y over the factors' space.", []),
    ("steepest_ascent", "Steepest ascent", "Method", "rsm", "Move all factors together in proportion to their coefficients: delta x_i = (b_i / b_A) delta x_A.", ["path of steepest ascent"]),
    ("steepest_descent", "Steepest descent", "Method", "rsm", "Steepest ascent in the opposite direction, to minimize y.", []),
    ("step_size", "Step size", "Concept", "rsm", "Big enough to change the response in a few runs, small enough not to jump over the optimum.", []),
    ("last_best_point", "Return to the last best point", "Guideline", "rsm", "When the response drops, go back to the best run and fit a new factorial around it.", []),
    ("curvature", "Curvature", "Concept", "rsm", "A bend in the response surface; every optimum has it, and a linear model cannot describe it.", ["nonlinearity"]),
    ("curvature_check", "Checking for curvature", "Method", "rsm", "Compare the model's predicted center point, b0, with the measured center point.", []),
    ("quadratic_model", "Quadratic model", "Concept", "ccd", "A model with squared terms such as b_TT x_T^2, to describe curvature.", ["second-order model"]),
    ("ccd", "Central composite design", "DesignType", "ccd", "A factorial plus center points plus axial points; fits a quadratic model.", ["CCD"]),
    ("axial_point", "Axial point", "Concept", "ccd", "A run on one factor's axis, (2^k)^0.25 coded units from the center: 1.41 for 2 factors, 1.68 for 3.", ["star point"]),
    ("box_behnken", "Box-Behnken design", "DesignType", "res", "A three-level design for quadratic models, named as another design to research.", []),
    ("contour_plot", "Contour plot", "Plot", "rsm", "Lines of equal predicted response, used to choose where to run next.", []),
    ("optimum", "Optimum", "Concept", "rsm", "The settings with the best response. The surface is flat there.", []),
    ("plateau", "Response levels off", "Diagnostic", "rsm", "Successive steps give little improvement.", []),
    ("equal_jumps", "Two equal steps", "Diagnostic", "rsm", "The response stays about the same for two steps: you have jumped over the optimum.", []),
    ("overshoot", "Response drops", "Diagnostic", "rsm", "The response falls, sometimes fast, after a step: you overshot the optimum.", []),
    ("big_interactions", "Interactions as large as main effects", "Diagnostic", "rsm", "Interaction terms similar to or larger than the main effects.", []),
    ("center_mismatch", "Center point far from prediction", "Diagnostic", "rsm", "The measured center point differs from b0 by much more than the noise.", []),
    ("near_optimum", "Near an optimum", "Concept", "rsm", "The region where the surface bends, so a linear model no longer points the way.", []),
    ("multiple_responses", "Several responses", "Concept", "rsm", "Two or more outcomes that trade off, such as production rate and energy.", ["multi-objective"]),
    ("single_combined_response", "Combine into one response", "Method", "rsm", "Rewrite the outcomes as one y, such as total cost or net profit.", []),
    ("overlay_surfaces", "Overlay the response surfaces", "Method", "rsm", "Superimpose the contours of each response so the trade-offs can be seen.", []),
    ("categorical_in_rsm", "Categorical factors in RSM", "Guideline", "rsm", "Fix a categorical factor, optimize the rest, then try its other value.", []),
    ("evop", "Evolutionary operation", "Method", "evop", "Small, repeated factorial perturbations on a full-scale process to keep it at its moving optimum.", ["EVOP"]),
    ("process_drift", "Process drift", "Concept", "evop", "The optimum moves as heat exchangers foul, catalyst deactivates, and raw materials change.", []),
    # --- General approach
    ("phase_screening", "Phase 1: screening", "Phase", "general", "Put as many factors as possible into as few runs as possible, with a saturated or Plackett-Burman design.", []),
    ("phase_sequential", "Phase 2: sequential runs", "Phase", "general", "Add runs to the first ones: foldover, projectivity, and fractions of higher resolution.", []),
    ("phase_optimize", "Phase 3: optimization", "Phase", "general", "Explore the response surface of the important factors, then add curvature terms near the optimum.", []),
    ("phase_maintain", "Phase 4: maintain the optimum", "Phase", "general", "Keep hunting for the moving optimum with evolutionary operation.", []),
    ("budget_rule", "Spend 25% first", "Guideline", "general", "Spend no more than 20% to 25% of time and budget on the first group of experiments.", []),
    ("after_the_experiment", "The best time to run an experiment", "Guideline", "general", "The best time to run an experiment is after the experiment: you always learn what you wish you had done.", []),
    ("first_run_center", "Run the center point first", "Guideline", "general", "The first run often fails while you learn the protocol; make it a center point, which the analysis does not need.", []),
    # --- Extended topics
    ("constraint", "Constraint", "Concept", "constr", "A region where the process may not operate, for safety or physical reasons.", ["limit", "infeasible region"]),
    ("lost_orthogonality", "Lost orthogonality", "Concept", "constr", "Moving a run to obey a constraint makes X no longer orthogonal and shrinks the region the design spans.", []),
    ("optimal_design", "Optimal design", "DesignType", "opt", "Runs chosen by a computer to optimize a criterion, for a model you specify, subject to constraints.", ["computer-generated design"]),
    ("candidate_set", "Candidate set", "Concept", "opt", "Every allowed combination of factor levels, from which an optimal design picks its runs.", ["candidate points"]),
    ("exchange_algorithm", "Candidate exchange algorithm", "Method", "opt", "Swap candidate points into and out of the design until the criterion is best.", []),
    ("optimality_criterion", "Optimality criterion", "Concept", "opt", "The quantity an optimal design optimizes, such as the determinant of X'X.", []),
    ("d_optimal", "D-optimality", "Criterion", "opt", "Maximize det(X'X): minimize the general variance of the parameters.", []),
    ("a_optimal", "A-optimality", "Criterion", "opt", "Minimize trace((X'X)^-1): the average variance of the parameters.", []),
    ("g_optimal", "G-optimality", "Criterion", "opt", "Minimize the maximum variance of the predictions.", []),
    ("v_optimal", "V-optimality", "Criterion", "opt", "Minimize the average variance of the predictions.", ["I-optimality"]),
    ("specify_model", "Specify the model first", "Guideline", "opt", "An optimal design needs the model before the runs; in a factorial the model is implicit.", []),
    ("augmentation", "Adding runs to a design", "Method", "opt", "Add the runs that most improve the criterion, for example most increase det(X'X), to fix or extend a design.", ["augmentation"]),
    ("dsd", "Definitive screening design", "DesignType", "dsd", "A three-level screening design, a type of optimal design, that can also estimate second-order effects.", ["DSD"]),
    ("mixture_design", "Mixture design", "DesignType", "mix", "A design for components whose proportions add to 100%.", []),
    ("mixture_constraint", "Proportions sum to one", "Concept", "mix", "Mixture components cannot change independently, because sum x_i = 1.", []),
    ("simplex", "Simplex", "Concept", "mix", "The triangular region of a three-component mixture: pure components at the corners.", []),
    # --- Worked examples
    ("ex_cost_bioreactor", "Bioreactor by COST", "Example", "cost", "Changing temperature then substrate one at a time stops at 69.5% yield, short of the optimum.", []),
    ("ex_tea", "The lady tasting tea", "Example", "random", "Fisher's illustration of randomization: is her score better than chance?", []),
    ("ex_brittleness", "Brittleness in TK104 and TK107", "Example", "random", "The randomization test (79.6%) and the t-test (79.3%) agree.", []),
    ("ex_two_factor", "Conversion vs T and S", "Example", "ff", "A 2^2 factorial in temperature and substrate: y = 61.5 - 5 x_T - 3 x_S - 0.5 x_T x_S.", []),
    ("ex_handwashing", "Washing hands", "Example", "ie", "Hot water enhances soap, and soap enhances hot water: an interaction.", []),
    ("ex_pollutant", "Pollutant from a molding plant", "Example", "ex3", "A 2^3 factorial in chemical, temperature and stirring; a large chemical x speed interaction.", []),
    ("ex_yield_pressure", "Yield, pressure and impurity", "Example", "causal", "Pressure correlates with yield only because operators raise it when impurity causes froth.", []),
    ("ex_7_factor_screen", "Seven factors in eight runs", "Example", "high", "A 2^(7-4) design with D = AB, E = AC, F = BC, G = ABC; A, C and G matter.", []),
    ("ex_8_factor", "Eight factors in 16 runs", "Example", "high", "A 2^(8-4) design of resolution IV.", []),
    ("ex_raw_material_blocks", "Two batches of raw material", "Example", "block", "A 2^3 factorial split into two blocks of 4, with the batch confounded with ABC.", []),
    ("ex_rsm_profit", "Climbing to maximum profit", "Example", "rsm", "Factorials, steepest ascent and a central composite design find the profit optimum near 343 K and 1.6 g/L.", []),
    ("ex_fruit_punch", "Fruit punch mixture", "Example", "mix", "The cheapest blend that still tastes right, with a region of high acidity excluded.", []),
    ("ex_cell_culture", "Cell-culture bioreactor", "Example", "frac", "Five factors at 10 days a run: a full factorial would take almost a year.", []),
    # --- Questions the chapter answers
    ("q_narrow_factors", "Which of eight factors matter?", "Question", "usage", "Narrow a list of plausible factors and rank their effects.", []),
    ("q_after_screening", "Three factors left: what next?", "Question", "usage", "How to run the rest of the experiments after screening.", []),
    ("q_old_data", "What do these old results show?", "Question", "usage", "Interpret existing experimental data and choose where to operate.", []),
    ("q_two_goals", "Long shelf life with less energy?", "Question", "usage", "Find settings that keep one outcome good while improving another.", []),
    ("q_unsafe_corner", "High temperature and pressure together are unsafe", "Question", "usage", "Plan an experiment when part of the region cannot be run.", []),
    # --- References
    ("ref_fisher", "R. A. Fisher, The Design of Experiments", "Reference", "refs", "The source of randomization and of factorial experimentation, from the 1930s.", []),
    ("ref_bhh", "Box, Hunter and Hunter, Statistics for Experimenters", "Reference", "refs", "The main reference for this chapter.", ["BHH"]),
    ("ref_box_hunter_1961", "Box and Hunter, 2^(k-p) fractional factorial designs (1961)", "Reference", "refs", "The papers that set out fractional factorials and resolution.", []),
    ("ref_box_1957", "Box, Evolutionary operation (1957)", "Reference", "refs", "The paper that introduced evolutionary operation.", []),
    ("ref_st_john_draper", "St. John and Draper, D-optimality (1975)", "Reference", "opt", "A review of D-optimal designs.", []),
    ("ref_jones_2011", "Jones and Nachtsheim, definitive screening (2011)", "Reference", "dsd", "The paper that introduced definitive screening designs.", []),
]

# (source, relation, target)
E = [
    # learning
    ("experiment", "PART_OF", "learning_cycle"), ("conjecture", "PART_OF", "learning_cycle"),
    ("experiment", "SHOWS", "cause_and_effect"), ("happenstance_data", "CONTRASTS_WITH", "experiment"),
    ("happenstance_data", "CANNOT_SHOW", "cause_and_effect"), ("feedback_control", "CAUSES", "happenstance_data"),
    ("correlation", "CONTRASTS_WITH", "cause_and_effect"), ("troubleshooting", "IS_A", "experiment"),
    ("experiment", "HAS", "response"), ("experiment", "HAS", "factor"), ("experiment", "HAS", "objective"),
    ("objective", "USES", "response"), ("qualitative_outcome", "IS_A", "response"),
    ("numeric_factor", "IS_A", "factor"), ("categorical_factor", "IS_A", "factor"), ("factor", "HAS", "level"),
    ("categorical_factor", "CONTRASTS_WITH", "numeric_factor"), ("run", "PART_OF", "experiment"),
    ("designed_experiment", "IS_A", "experiment"), ("designed_experiment", "USES", "randomization"),
    ("controlled_disturbance", "IS_A", "disturbance"), ("time_effect", "IS_A", "disturbance"),
    ("disturbance", "AFFECTS", "response"),
    # randomization and two conditions
    ("randomization", "PROTECTS_AGAINST", "disturbance"), ("randomization", "GUARANTEES", "independence"),
    ("t_distribution", "REQUIRES", "independence"), ("randomization_test", "TESTS", "null_hypothesis"),
    ("randomization_test", "AGREES_WITH", "t_distribution"), ("pairing", "PROTECTS_AGAINST", "disturbance"),
    ("blocking", "PROTECTS_AGAINST", "disturbance"), ("pairing", "CONTRASTS_WITH", "blocking"),
    ("two_group_comparison", "USES", "pooled_variance"), ("two_group_comparison", "USES", "confidence_interval"),
    ("two_group_comparison", "USES", "t_distribution"), ("two_group_comparison", "AGREES_WITH", "least_squares_model"),
    ("least_squares_model", "USES", "indicator_variable"), ("confidence_interval", "DECIDES", "statistical_significance"),
    ("practical_significance", "CONTRASTS_WITH", "statistical_significance"),
    ("practical_significance", "USES", "confidence_interval"),
    # COST
    ("cost", "LEADS_TO", "false_optimum"), ("cost", "SUFFERS_FROM", "order_dependence"),
    ("cost", "CANNOT_ESTIMATE", "interaction"), ("cost", "CONTRASTS_WITH", "designed_experiment"),
    ("full_factorial", "IS_A", "designed_experiment"), ("factorial_efficiency", "CONTRASTS_WITH", "cost"),
    # factorials
    ("full_factorial", "HAS_PROPERTY", "orthogonality"), ("full_factorial", "HAS_PROPERTY", "factorial_efficiency"),
    ("full_factorial", "USES", "coding"), ("full_factorial", "USES", "standard_order"),
    ("full_factorial", "USES", "randomization"), ("full_factorial", "ESTIMATES", "main_effect"),
    ("full_factorial", "ESTIMATES", "interaction"), ("operating_range", "APPLIES_TO", "level"),
    ("cube_plot", "SHOWS", "main_effect"), ("cube_plot", "SHOWS", "full_factorial"),
    ("interaction_plot", "SHOWS", "interaction"), ("two_factor_interaction", "IS_A", "interaction"),
    ("three_factor_interaction", "IS_A", "interaction"), ("main_effect", "MEASURED_AS", "half_range_effect"),
    ("coefficient", "MEASURED_AS", "half_range_effect"), ("least_squares_model", "ESTIMATES", "coefficient"),
    ("least_squares_model", "USES", "model_matrix"), ("least_squares_model", "HAS", "intercept"),
    ("orthogonality", "PROPERTY_OF", "model_matrix"), ("coding", "MAKES", "orthogonality"),
    ("hierarchy_rule", "APPLIES_TO", "interaction"), ("interpret_with_interaction", "APPLIES_TO", "main_effect"),
    ("robustness", "MEANS_SMALL", "main_effect"),
    ("replicate", "ADDS", "degrees_of_freedom"), ("center_point", "ADDS", "degrees_of_freedom"),
    ("center_point", "KEEPS", "orthogonality"), ("repeat_measurement", "CONTRASTS_WITH", "replicate"),
    ("degrees_of_freedom", "NEEDED_FOR", "standard_error"), ("standard_error", "NEEDED_FOR", "se_significance"),
    ("se_significance", "USES", "confidence_interval"), ("se_significance", "USES", "t_distribution"),
    ("pareto_plot", "REQUIRES", "coding"), ("pareto_plot", "SHOWS", "coefficient"),
    ("pareto_plot", "CONTRASTS_WITH", "se_significance"), ("refit", "ADDS", "degrees_of_freedom"),
    ("refit", "LEADS_TO", "residual_analysis"), ("missing_values", "REMEDIED_BY", "least_squares_model"),
    ("off_target_run", "REMEDIED_BY", "least_squares_model"), ("off_target_run", "IS_A", "lost_orthogonality"),
    # fractional factorials
    ("fractional_factorial", "IS_A", "designed_experiment"), ("fractional_factorial", "FRACTION_OF", "full_factorial"),
    ("half_fraction", "IS_A", "fractional_factorial"), ("quarter_fraction", "IS_A", "fractional_factorial"),
    ("saturated_design", "IS_A", "fractional_factorial"), ("complementary_fraction", "IS_A", "half_fraction"),
    ("half_fraction", "CAN_AUGMENT_TO", "full_factorial"), ("complementary_fraction", "COMPLETES", "half_fraction"),
    ("fractional_factorial", "CAUSES", "confounding"), ("fractional_factorial", "USES", "generator"),
    ("fractional_factorial", "HAS_PROPERTY", "resolution"), ("fractional_factorial", "HAS_PROPERTY", "projectivity"),
    ("fractional_factorial", "RELIES_ON", "effect_sparsity"), ("confounding", "CAUSES", "collinearity"),
    ("alias", "DESCRIBES", "confounding"), ("alias_structure", "LISTS", "alias"),
    ("generator", "DEFINES", "defining_relation"), ("defining_relation", "MADE_OF", "word"),
    ("word", "EQUALS", "identity_column"), ("alias_calculation", "USES", "defining_relation"),
    ("alias_calculation", "PRODUCES", "alias_structure"), ("reassign_letters", "CHANGES", "alias_structure"),
    ("resolution", "MEASURED_FROM", "defining_relation"), ("resolution", "SUMMARIZES", "alias_structure"),
    ("resolution_iii", "IS_A", "resolution"), ("resolution_iv", "IS_A", "resolution"), ("resolution_v", "IS_A", "resolution"),
    ("resolution_iii", "SUITED_TO", "screening"), ("resolution_iv", "SUITED_TO", "phase_sequential"),
    ("resolution_v", "SUITED_TO", "phase_optimize"), ("saturated_design", "HAS_PROPERTY", "resolution_iii"),
    ("trade_off_table", "RELATES", "resolution"), ("trade_off_table", "RELATES", "fractional_factorial"),
    ("projectivity", "DERIVED_FROM", "resolution"), ("projectivity", "COLLAPSES_TO", "full_factorial"),
    ("saturated_design", "SUITED_TO", "screening"), ("plackett_burman", "SUITED_TO", "screening"),
    ("plackett_burman", "CONTRASTS_WITH", "saturated_design"), ("saturated_design", "ANALYSED_BY", "pareto_plot"),
    ("single_factor_foldover", "IS_A", "foldover"), ("full_foldover", "IS_A", "foldover"),
    ("foldover", "IS_A", "sequential_experimentation"), ("single_factor_foldover", "REMOVES", "confounding"),
    ("full_foldover", "RAISES", "resolution"), ("resolution_iii", "CAN_AUGMENT_TO", "resolution_iv"),
    ("saturated_design", "CAN_AUGMENT_TO", "full_foldover"),
    # blocking
    ("blocking", "USES", "block"), ("blocking", "USES", "block_generator"), ("block_generator", "IS_A", "generator"),
    ("block_on_highest", "APPLIES_TO", "block_generator"), ("block_on_highest", "RELIES_ON", "effect_sparsity"),
    ("blocking", "CAUSES", "confounding"), ("block", "USES", "randomization"),
    ("full_factorial", "SPLIT_BY", "blocking"), ("complementary_fraction", "USED_AS", "block"),
    # RSM
    ("rsm", "IS_A", "sequential_experimentation"), ("rsm", "MAPS", "response_surface"),
    ("rsm", "SEEKS", "optimum"), ("rsm", "USES", "full_factorial"), ("rsm", "USES", "steepest_ascent"),
    ("steepest_descent", "IS_A", "steepest_ascent"), ("steepest_ascent", "USES", "coefficient"),
    ("steepest_ascent", "USES", "step_size"), ("steepest_ascent", "CONTRASTS_WITH", "cost"),
    ("last_best_point", "APPLIES_TO", "steepest_ascent"), ("optimum", "HAS", "curvature"),
    ("near_optimum", "HAS", "curvature"), ("curvature_check", "USES", "center_point"),
    ("curvature_check", "USES", "intercept"), ("curvature_check", "DETECTS", "curvature"),
    ("plateau", "INDICATES", "near_optimum"), ("equal_jumps", "INDICATES", "near_optimum"),
    ("overshoot", "INDICATES", "near_optimum"), ("big_interactions", "INDICATES", "curvature"),
    ("center_mismatch", "INDICATES", "curvature"), ("curvature", "REMEDIED_BY", "quadratic_model"),
    ("overshoot", "REMEDIED_BY", "last_best_point"), ("ccd", "ESTIMATES", "quadratic_model"),
    ("ccd", "USES", "axial_point"), ("ccd", "USES", "center_point"), ("full_factorial", "CAN_AUGMENT_TO", "ccd"),
    ("box_behnken", "ESTIMATES", "quadratic_model"), ("contour_plot", "SHOWS", "response_surface"),
    ("contour_plot", "LOCATES", "optimum"), ("multiple_responses", "REMEDIED_BY", "single_combined_response"),
    ("multiple_responses", "REMEDIED_BY", "overlay_surfaces"), ("overlay_surfaces", "USES", "contour_plot"),
    ("categorical_in_rsm", "APPLIES_TO", "categorical_factor"), ("categorical_in_rsm", "APPLIES_TO", "rsm"),
    ("evop", "IS_A", "sequential_experimentation"), ("evop", "TRACKS", "optimum"), ("process_drift", "REMEDIED_BY", "evop"),
    ("evop", "USES", "replicate"), ("process_drift", "IS_A", "time_effect"),
    # general approach
    ("phase_screening", "PRECEDES", "phase_sequential"), ("phase_sequential", "PRECEDES", "phase_optimize"),
    ("phase_optimize", "PRECEDES", "phase_maintain"), ("phase_screening", "USES", "saturated_design"),
    ("phase_screening", "USES", "plackett_burman"), ("phase_screening", "IS_A", "screening"),
    ("phase_sequential", "USES", "foldover"), ("phase_sequential", "USES", "projectivity"),
    ("phase_optimize", "USES", "rsm"), ("phase_maintain", "USES", "evop"),
    ("budget_rule", "APPLIES_TO", "sequential_experimentation"), ("after_the_experiment", "APPLIES_TO", "sequential_experimentation"),
    ("first_run_center", "APPLIES_TO", "center_point"), ("first_run_center", "APPLIES_TO", "phase_screening"),
    # extended
    ("constraint", "CAUSES", "lost_orthogonality"), ("constraint", "REMEDIED_BY", "optimal_design"),
    ("optimal_design", "IS_A", "designed_experiment"), ("optimal_design", "USES", "candidate_set"),
    ("optimal_design", "USES", "exchange_algorithm"), ("optimal_design", "OPTIMIZES", "optimality_criterion"),
    ("optimal_design", "REQUIRES", "specify_model"), ("d_optimal", "IS_A", "optimality_criterion"),
    ("a_optimal", "IS_A", "optimality_criterion"), ("g_optimal", "IS_A", "optimality_criterion"),
    ("v_optimal", "IS_A", "optimality_criterion"), ("d_optimal", "USES", "model_matrix"),
    ("full_factorial", "HAS_PROPERTY", "d_optimal"), ("augmentation", "USES", "d_optimal"),
    ("augmentation", "IS_A", "sequential_experimentation"), ("lost_orthogonality", "REMEDIED_BY", "augmentation"),
    ("dsd", "IS_A", "optimal_design"), ("dsd", "SUITED_TO", "screening"), ("dsd", "CONTRASTS_WITH", "saturated_design"),
    ("mixture_design", "IS_A", "designed_experiment"), ("mixture_design", "REQUIRES", "mixture_constraint"),
    ("mixture_design", "USES", "simplex"), ("mixture_design", "USES", "d_optimal"),
    ("mixture_constraint", "CONTRASTS_WITH", "full_factorial"), ("constraint", "APPLIES_TO", "mixture_design"),
    # examples
    ("ex_cost_bioreactor", "ILLUSTRATES", "cost"), ("ex_cost_bioreactor", "ILLUSTRATES", "false_optimum"),
    ("ex_tea", "ILLUSTRATES", "randomization"), ("ex_brittleness", "ILLUSTRATES", "randomization_test"),
    ("ex_brittleness", "ILLUSTRATES", "two_group_comparison"), ("ex_two_factor", "ILLUSTRATES", "main_effect"),
    ("ex_two_factor", "ILLUSTRATES", "least_squares_model"), ("ex_handwashing", "ILLUSTRATES", "interaction"),
    ("ex_pollutant", "ILLUSTRATES", "full_factorial"), ("ex_pollutant", "ILLUSTRATES", "two_factor_interaction"),
    ("ex_yield_pressure", "ILLUSTRATES", "happenstance_data"), ("ex_yield_pressure", "ILLUSTRATES", "correlation"),
    ("ex_7_factor_screen", "ILLUSTRATES", "saturated_design"), ("ex_7_factor_screen", "ILLUSTRATES", "alias_structure"),
    ("ex_7_factor_screen", "ILLUSTRATES", "single_factor_foldover"), ("ex_8_factor", "ILLUSTRATES", "resolution_iv"),
    ("ex_raw_material_blocks", "ILLUSTRATES", "blocking"), ("ex_rsm_profit", "ILLUSTRATES", "rsm"),
    ("ex_rsm_profit", "ILLUSTRATES", "curvature_check"), ("ex_rsm_profit", "ILLUSTRATES", "ccd"),
    ("ex_fruit_punch", "ILLUSTRATES", "mixture_design"), ("ex_cell_culture", "ILLUSTRATES", "fractional_factorial"),
    # questions
    ("q_narrow_factors", "ANSWERED_BY", "screening"), ("q_after_screening", "ANSWERED_BY", "phase_sequential"),
    ("q_after_screening", "ANSWERED_BY", "rsm"), ("q_old_data", "ANSWERED_BY", "least_squares_model"),
    ("q_two_goals", "ANSWERED_BY", "multiple_responses"), ("q_unsafe_corner", "ANSWERED_BY", "constraint"),
    # references
    ("randomization", "INTRODUCED_IN", "ref_fisher"), ("cost", "CRITICIZED_IN", "ref_fisher"),
    ("trade_off_table", "INTRODUCED_IN", "ref_bhh"), ("half_range_effect", "CONTRASTS_WITH", "ref_bhh"),
    ("resolution", "INTRODUCED_IN", "ref_box_hunter_1961"), ("evop", "INTRODUCED_IN", "ref_box_1957"),
    ("d_optimal", "REVIEWED_IN", "ref_st_john_draper"), ("dsd", "INTRODUCED_IN", "ref_jones_2011"),
    ("learning_cycle", "INTRODUCED_IN", "ref_bhh"), ("ex_tea", "INTRODUCED_IN", "ref_fisher"),
]


# The edges above were written in the text's own verbs; fold them into a small vocabulary.
# relation -> (new relation, swap direction)
FOLD = {
    "HAS": ("PART_OF", True), "PROPERTY_OF": ("HAS_PROPERTY", True), "MADE_OF": ("PART_OF", True),
    "NEEDED_FOR": ("REQUIRES", True), "RELIES_ON": ("REQUIRES", False), "FRACTION_OF": ("PART_OF", False),
    "DEFINES": ("PART_OF", False), "CONTRASTS_WITH": ("COMPARED_WITH", False), "AGREES_WITH": ("COMPARED_WITH", False),
    "PROTECTS_AGAINST": ("PREVENTS", False), "REMOVES": ("PREVENTS", False), "KEEPS": ("PREVENTS", False),
    "AFFECTS": ("CAUSES", False), "GUARANTEES": ("CAUSES", False), "MAKES": ("CAUSES", False),
    "ADDS": ("CAUSES", False), "RAISES": ("CAUSES", False), "SUFFERS_FROM": ("CAUSES", False), "LEADS_TO": ("CAUSES", False),
    "TESTS": ("SHOWS", False), "DECIDES": ("SHOWS", False), "DETECTS": ("SHOWS", False), "LOCATES": ("SHOWS", False),
    "MEASURED_FROM": ("SHOWS", False), "SUMMARIZES": ("SHOWS", False), "LISTS": ("SHOWS", False),
    "DESCRIBES": ("SHOWS", False), "MAPS": ("SHOWS", False), "PRODUCES": ("SHOWS", False), "RELATES": ("SHOWS", False),
    "SEEKS": ("SHOWS", False), "TRACKS": ("SHOWS", False), "CANNOT_ESTIMATE": ("CANNOT_SHOW", False),
    "MEASURED_AS": ("USES", False), "EQUALS": ("USES", False), "DERIVED_FROM": ("USES", False),
    "ANALYSED_BY": ("USES", False), "SPLIT_BY": ("USES", False), "USED_AS": ("USES", False), "OPTIMIZES": ("USES", False),
    "MEANS_SMALL": ("APPLIES_TO", False), "CHANGES": ("APPLIES_TO", False),
    "INTRODUCED_IN": ("CITED_IN", False), "CRITICIZED_IN": ("CITED_IN", False), "REVIEWED_IN": ("CITED_IN", False),
}
# Edges whose folded form would read wrongly: replaced (or dropped, with None) one by one.
OVERRIDE = {
    ("optimum", "HAS", "curvature"): ("optimum", "HAS_PROPERTY", "curvature"),
    ("near_optimum", "HAS", "curvature"): ("near_optimum", "HAS_PROPERTY", "curvature"),
    ("center_point", "KEEPS", "orthogonality"): ("center_point", "PREVENTS", "lost_orthogonality"),
    ("off_target_run", "IS_A", "lost_orthogonality"): ("off_target_run", "CAUSES", "lost_orthogonality"),
    ("complementary_fraction", "COMPLETES", "half_fraction"): ("complementary_fraction", "PART_OF", "full_factorial"),
    ("refit", "LEADS_TO", "residual_analysis"): ("refit", "PRECEDES", "residual_analysis"),
    ("happenstance_data", "CANNOT_SHOW", "cause_and_effect"): ("happenstance_data", "CANNOT_SHOW", "cause_and_effect"),
    ("saturated_design", "CAN_AUGMENT_TO", "full_foldover"): None,  # a design cannot augment to a method
    ("projectivity", "COLLAPSES_TO", "full_factorial"): None,  # said in its definition
    ("half_range_effect", "CONTRASTS_WITH", "ref_bhh"): ("half_range_effect", "CITED_IN", "ref_bhh"),
}


def fold(edges: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    """Fold each edge into the small vocabulary, keeping the first copy of any duplicate."""
    out = []
    for edge in edges:
        if edge in OVERRIDE:
            edge = OVERRIDE[edge]
            if edge is None:
                continue
        else:
            s, r, t = edge
            if r in FOLD:
                r, swap = FOLD[r]
                edge = (t, r, s) if swap else (s, r, t)
        if edge not in out:
            out.append(edge)
    return out


def label_files() -> dict[str, str]:
    """Map every RST label in the chapter to the file that defines it, in the current book."""
    found = {}
    for rst in (BOOK / CHAPTER).rglob("*.rst"):
        for label in re.findall(r"^\.\. _([^:]+):", rst.read_text(encoding="utf-8"), flags=re.M):
            found[label] = str(rst.relative_to(BOOK))
    return found


def main() -> None:
    labels = label_files()
    ids = [n[0] for n in N]
    assert len(ids) == len(set(ids)), [i for i, c in Counter(ids).items() if c > 1]
    nodes, missing = [], []
    for nid, name, ntype, ref, definition, aliases in N:
        target = REFS[ref]
        if target.startswith("file:"):
            label, path = None, f"{CHAPTER}/{target[5:]}"
            if not (BOOK / path).exists():
                missing.append(f"{nid}: {path}")
        else:
            label, path = target, labels.get(target)
            if path is None:
                missing.append(f"{nid}: label {target}")
        nodes.append({"id": nid, "name": name, "type": ntype, "definition": definition,
                      "aliases": aliases, "book_label": label, "book_file": path})
    if missing:  # checked before writing, so a failed build leaves the last good output in place
        sys.exit(f"{len(missing)} book references do not resolve in {BOOK}; build against a checkout of "
                 f"pid-book main:\n  " + "\n  ".join(missing))
    known = set(ids)
    bad = [e for e in E if e[0] not in known or e[2] not in known]
    assert not bad, bad
    assert len(E) == len(set(E)), "duplicate edge"
    E[:] = fold(E)
    used = {e[0] for e in E} | {e[2] for e in E}
    orphans = sorted(known - used)
    edges = [{"source": s, "type": r, "target": t} for s, r, t in E]
    (OUT / "doe_kg.json").write_text(json.dumps({"nodes": nodes, "edges": edges}, indent=1), encoding="utf-8")

    def q(s: str | None) -> str:
        return "null" if s is None else json.dumps(s)

    lines = ["// DOE knowledge graph, built from pid-book PR #22. Load into an empty database.",
             "CREATE CONSTRAINT doe_node_id IF NOT EXISTS FOR (n:DOE) REQUIRE n.id IS UNIQUE;"]
    for n in nodes:
        lines.append(f"CREATE (:DOE:{n['type']} {{id: {q(n['id'])}, name: {q(n['name'])}, "
                     f"definition: {q(n['definition'])}, aliases: {json.dumps(n['aliases'])}, "
                     f"book_label: {q(n['book_label'])}, book_file: {q(n['book_file'])}}});")
    for s, r, t in E:
        lines.append(f"MATCH (a:DOE {{id: {q(s)}}}), (b:DOE {{id: {q(t)}}}) CREATE (a)-[:{r}]->(b);")
    (OUT / "doe_kg.cypher").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"{len(nodes)} nodes, {len(edges)} edges, {len({e[1] for e in E})} edge types")
    print("node types:", dict(Counter(n[2] for n in N).most_common()))
    print("edge types:", dict(Counter(e[1] for e in E).most_common()))
    print("orphans:", orphans or "none")
    print("book references: all resolve")


if __name__ == "__main__":
    main()
