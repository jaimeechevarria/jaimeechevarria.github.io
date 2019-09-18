---
layout: post
title: Aircraft Trajectory Optimization
summary: Analysis tool for estimation of optimal aircraft trajectories in air races.
categories: [Simulation, Optimization]
featured-img: rbar
mathjax: true
---

Red Bull Air Race is an international series of air races in which competitors have to navigate a challenging obstacle course in the fastest time possible. Pilots fly individually against the clock and have to complete tight turns through a slalom course consisting of pylons, known as "Air Gates", achieving speeds of up to 420 km/h and sustained accelerations of more than 10 G.

<figure>
    <p align="center"><img src="/assets/img/article_images/rbar_001.jpg" width="80%"></p>
    <figcaption><p align="center"><b>Figure 1</b> - Red Bull Air Race 2016 in Budapest</p></figcaption>
</figure>

<!-- &nbsp; -->

Participant teams usually spend a significant amount of time trying to predict optimal aircraft trajectories to follow for each track, in an effort to achieve the fastest possible lap times.

In early 2018 I started working in a personal project to develop an analysis tool which enabled a temporal-space study of optimal trajectories for different race tracks.

The problem is not trivial. Let’s start from the beginning.

<!-- &nbsp; -->

### What is the objective?

Races usually have two types of obstacles: Airgates of single or double pylons. Pilots are required to fly near the single pylons and between the double pylons, following a predetermined route as fast as possible.

<figure>
    <p align="center"><img src="/assets/img/article_images/rbar_002_003.jpg" width="80%"></p>    
    <figcaption><p align="center"><b>Figure 2</b> - Single pylon (left) and double pylons or gates (right)</p></figcaption>
</figure>

<!-- &nbsp; -->

There exist several restrictions to take into consideration, including the following:

* Pilots must fly through the double pylon air gates in level flight. This is, the aircraft has to be flying straight when passing through these airgates.
* Pilots must fly through the airgates while inside the altitude range indicated by the red bands in the pylons.
* Aircraft must never cross any safety line, which delimit the compulsory safety flight area.
* Aircraft must not surpass the acceleration limit of 10 G.
* Aircraft must not start the race with a velocity higher than 200 knots.

How could we approach this problem?

<!-- &nbsp; -->

### A simplistic approach

This is an optimization problem with several types of constraints. We need to find a way to simplify the problem in order to reduce complexity.

Let’s try a simple approach by making some hypotheses:

* Aircraft trajectories are **smooth** because the aircraft movement is always restricted by inertia. This means these trajectories can be approximated by some type of mathematical **curve**.
* This kind of air races usually take place in 2D planes, since aircraft fly most of the time at the same altitude. Let’s forget about the third degree of freedom for now.
* Aircraft longitudinal acceleration when flying straight is mostly dictated by the engine thrust and its **aerodynamic resistance**.
* Aerodynamic resistance grows exponentially with aircraft **lift**.
* When an aircraft is performing a turn, lift needs to be increased in order to maintain altitude.
Turning angle (**roll**) is dictated by the **curvature** of the aircraft trajectory.

Given this statements, a direct relation can be extrapolated between the trajectory local curvature and the aircraft acceleration at that location.

But what type of mathematical curve may an aircraft trajectory look like? One option are **cubic splines**.

<figure>
    <p align="center"><img src="/assets/img/article_images/rbar_003.png" width="80%"></p>    
    <figcaption><p align="center"><b>Figure 3</b> - Cubic spline</p></figcaption>
</figure>

A cubic spline is a spline constructed of piecewise third-order polynomials which pass through a set of $m$ control points. The second derivative of each polynomial is commonly set to zero at the endpoints, since this provides a boundary condition that completes the system of $m-2$ equations. This produces a so-called "natural" cubic spline and leads to a simple tridiagonal system which can be solved easily to give the coefficients of the polynomials [3].

These curves provide a good approximation of the real trajectories. Curves of higher order could approach the trajectories more precisely, but they unnecessarily increase the complexity of the optimization problem and increase the probability of convergence to a local minimum instead of a global minimum. Order 3 polynomials provide a good balance between complexity and precision.

Now, let's analyse the effect of turning angle (roll) in an aircraft lift while flying at the same altitude.

<figure>
    <p align="center"><img src="/assets/img/article_images/rbar_004.png" width="80%"></p>    
    <figcaption><p align="center"><b>Figure 4</b> - Effect of roll on lift during level flight</p></figcaption>
</figure>

When an aircraft is flying straight (case A in figure 4), it’s weight ($W$) needs to be compensated by the generated lift ($L$). However, when an aircraft is turning (case B in figure 4), lift needs to be increased in order to be able to compensate the weight. The lift component in the vertical axis compensates the aircraft weight. This component is $ L{\cdot}\cos \left (\varphi \right) $. An additional component is generated in the horizontal axis, $ L{\cdot}\sin \left (\varphi \right) $. This component represents a centripetal force which causes the aircraft trajectory to turn.

<figure>
    <p align="center"><img src="/assets/img/article_images/rbar_005.png" width="80%"></p>    
    <figcaption><p align="center"><b>Figure 5</b> - Centripetal force during a turn</p></figcaption>
</figure>

The radius of curvature is dictated by current velocity and the aircraft weight. The centripetal force in a moving body can be defined by

$$ \normalsize L{\cdot}\sin \left (\varphi \right) = m{\cdot}\frac{V^2}{R} \tag{1} $$

Where $R$ is the local radius of curvature. The lift component in the vertical axis needs to compensate the aircraft weight in order to maintain altitude.

$$ \normalsize L{\cdot}\cos \left (\varphi \right) = m{\cdot}g = W \tag{2} $$

These two equations can be combined to form

$$ \normalsize \varphi = \arctan \left(\frac{V^2}{R{\cdot}g} \right) \tag{3} $$

Given that

$$ \normalsize \cos \left(\arctan \left(x \right) \right) = \frac{1}{\sqrt{x^2 + 1}} \tag{4} $$

and that local curvature in a curve is defined as the inverse of the local radius

$$ \normalsize \kappa = \frac{1}{R} \tag{5} $$

then

$$ \normalsize \cos \left (\varphi \right) = \frac{1}{\sqrt{\left(\frac{V^2{\cdot}\kappa}{g} \right)^2 + 1}} \tag{6} $$

This equation will be useful when we derive another set of equations, corresponding to the longitudinal degree of freedom. Up until this point, the only mathematical concepts used where geometric and trigonometric relations, as well as the concept of force equilibrium and the definition of centripetal force.

Now we need to take into account the aerodynamic forces. We will model lift, $L$, and drag, $D$, forces using the following equations (more info in post []).

$$
\normalsize
\begin{gathered}
    L=q{\cdot}S{\cdot}C_L \\
    D=q{\cdot}S{\cdot}C_D \\
\end{gathered}
\tag{7}
$$

Where $q$ is the dynamic pressure, defined as $\frac{1}{2}{\cdot}\rho{\cdot}V^2$, being $\rho$ the air density and $V$ the total velocity of the aircraft. Variable $S$ corresponds to the wing reference surface. Variables $C_L$ and $C_D$ correspond to the lift coefficient and drag coefficient respectively. We will define those as

$$
\normalsize
\begin{gathered}
    C_L=C_{L_0} + C_{L_{\alpha}}{\cdot}\alpha \\
    C_D=C_{D_0} + K{\cdot}{C_L}^2 \\
\end{gathered}
\tag{8}
$$

Where $\alpha$ refers to the aircraft angle of attack, $C_{L_0}$ and ${C_{D_0}}$ refer to the lift and drag coefficients at zero angle of attack, and $C_{L_{\alpha}}$ and ${K}$ are aerodynamic parameters dependant on the specific aircraft.

Aicraft acceleration, $a$, can be modelled using Newton's first law of motion, having into account the vehicle mass, $m$.

$$
\normalsize m{\cdot}a = T - D \tag{9}
$$

We can discretize the trajectory of the aircraft along the spline in small sectors. Considering $V_i$ the velocity at the start of a sector, $V_{med}$ the velocity at the middle of the sector, and $l$ the length of the sector, combining equations (6-9) we can approximate the acceleration at each sector by:

$$
\normalsize a \approxeq \frac{\Delta V}{\Delta t} = \frac{2{\cdot}\left(V_{med} - V_i \right)}{\frac{l}{V_{med}}} = \frac{T - \frac{1}{2}{\cdot}\rho{\cdot}V_{med}^2{\cdot}S{\cdot}\left(C_{D_0} + K{\cdot}\left(\frac{m{\cdot}g}{\frac{1}{2}{\cdot}\rho{\cdot}V_{med}^2{\cdot}S{\cdot}\cos \left(\varphi \right)} \right)^2 \right)}{m} \tag{10}
$$

Where

$$ \normalsize \cos \left(\varphi \right) = \frac{1}{\sqrt{\left(\frac{V_{med}^2{\cdot}\kappa}{g} \right)^2 + 1}} \tag{11} $$

The solution of system of equations (10) and (11) for variable $V_{med}$ in order to find the medium velocity at each timestep reduces to a quartic function, which can be solved using Ferrari's formula.

$$ \normalsize a{\cdot}V_{med}^4 + b{\cdot}V_{med}^3 + c{\cdot}V_{med}^2 + d{\cdot}V_{med} + e = 0 \tag{12} $$

Where coefficients $a$, $b$, $c$, $d$ and $e$ result in

$$
\normalsize
\begin{aligned}
    4{\cdot}K{\cdot}l{\cdot}\kappa^2{\cdot}m^2 + C_{D_0}{\cdot}S^2{\cdot}l{\cdot}\rho^2 + 4{\cdot}S{\cdot}m{\cdot}\rho = a \\
    -4{\cdot}S{\cdot}V_i{\cdot}m{\cdot}\rho = b \\
    -2{\cdot}S{\cdot}T{\cdot}l{\cdot}\rho = c \\
    0 = d \\
    4{\cdot}K{\cdot}l{\cdot}g^2{\cdot}m^2 = e \\
\end{aligned}
\tag{13}
$$

Ferrari's formula uses the following relations which provide the analytic solution of the quartic equation [].

$$
\normalsize
\begin{aligned}
    \Delta = 256{\cdot}a^{3}{\cdot}e^{3}-192{\cdot}a^{2}{\cdot}b{\cdot}d{\cdot}e^{2}-128{\cdot}a^{2}{\cdot}c^{2}{\cdot}e^{2}+144{\cdot}a^{2}{\cdot}c{\cdot}d^{2}{\cdot}e-27{\cdot}a^{2}{\cdot}d^{4} \\
    +144{\cdot}a{\cdot}b^{2}{\cdot}c{\cdot}e^{2}-6{\cdot}a{\cdot}b^{2}{\cdot}d^{2}{\cdot}e-80{\cdot}a{\cdot}b{\cdot}c^{2}{\cdot}d{\cdot}e+18{\cdot}a{\cdot}b{\cdot}c{\cdot}d^{3}+16{\cdot}a{\cdot}c^{4}{\cdot}e \\
    -4{\cdot}a{\cdot}c^{3}{\cdot}d^{2}-27{\cdot}b^{4}{\cdot}e^{2}+18{\cdot}b^{3}{\cdot}c{\cdot}d{\cdot}e-4{\cdot}b^{3}{\cdot}d^{3}-4{\cdot}b^{2}{\cdot}c^{3}{\cdot}e+b^{2}{\cdot}c^{2}{\cdot}d^{2}
\end{aligned}
\tag{14}
$$

&nbsp;

$$
\normalsize
\begin{aligned}
    {\frac {8{\cdot}a{\cdot}c - 3{\cdot}b^{2}}{8{\cdot}a^{2}}} = p \\
    {\frac {b^{3} - 4{\cdot}a{\cdot}b{\cdot}c + 8{\cdot}a^{2}{\cdot}d}{8{\cdot}a^{3}}} = q
\end{aligned}
\tag{15}
$$

&nbsp;

$$
\normalsize
\begin{aligned}
    c^{2} - 3{\cdot}b{\cdot}d + 12{\cdot}a{\cdot}e = \Delta_{0} \\
    2{\cdot}c^{3} - 9{\cdot}b{\cdot}c{\cdot}d + 27{\cdot}b^{2}{\cdot}e + 27{\cdot}a{\cdot}d^{2}-72{\cdot}a{\cdot}c{\cdot}e = \Delta_{1}
\end{aligned}
\tag{16}
$$

&nbsp;

$$
\normalsize
\begin{aligned}
    {\sqrt[{3}]{\frac {\Delta _{1}+{\sqrt {\left| -27{\cdot}\Delta \right|}}}{2}}} = Q \\
    {\frac {1}{2}}{\sqrt {\left|-{\frac {2}{3}}\ p+{\frac {1}{3{\cdot}a}}\left(Q+{\frac {\Delta _{0}}{Q}}\right) \right|}} = S
\end{aligned}
\tag{17}
$$

&nbsp;

$$
\normalsize
\begin{aligned}
    -{\frac {b}{4{\cdot}a}}-S \pm {\frac {1}{2}}{\sqrt {-4{\cdot}S^{2}-2{\cdot}p+{\frac {q}{S}}}} = V_{med_{1,2}} \\
    -{\frac {b}{4{\cdot}a}}+S \pm {\frac {1}{2}}{\sqrt {-4{\cdot}S^{2}-2{\cdot}p-{\frac {q}{S}}}} = V_{med_{3,4}}
\end{aligned}
\tag{18}
$$

We are interested in the biggest real solution to the polynomic equation.

$$ \normalsize V_{med} = -{\frac {b}{4{\cdot}a}} + S + {\frac {1}{2}}{\sqrt {\left| -4{\cdot}S^{2}-2{\cdot}p-{\frac {q}{S}} \right|}} \tag{19} $$

## References

[1] Steven
[] https://en.wikipedia.org/wiki/Quartic_function