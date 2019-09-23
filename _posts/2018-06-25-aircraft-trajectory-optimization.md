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
    <p align="center"><img src="/assets/img/article_images/rbar_002.jpg" width="80%"></p>    
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

The trajectories can be approximated by bidimensional splines parametrized in two degrees of freedom $x$ and $y$. This is, there's a third degree polynomial defining $x{\left (t \right)}$, and a third degree polynomial defining $y{\left (t \right)}$. These curves provide a good approximation of the real trajectories. Curves of higher order could approach the trajectories more precisely, but they unnecessarily increase the complexity of the optimization problem and increase the probability of convergence to a local minimum instead of a global minimum. Order 3 polynomials provide a good balance between complexity and precision.


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

$$ \small L{\cdot}\sin \left (\varphi \right) = m{\cdot}\frac{V^2}{R} \tag{1} $$

Where $R$ is the local radius of curvature. The lift component in the vertical axis needs to compensate the aircraft weight in order to maintain altitude.

$$ \small L{\cdot}\cos \left (\varphi \right) = m{\cdot}g = W \tag{2} $$

These two equations can be combined to form

$$ \small \varphi = \arctan \left(\frac{V^2}{R{\cdot}g} \right) \tag{3} $$

Given that

$$ \small \cos \left(\arctan \left(x \right) \right) = \frac{1}{\sqrt{x^2 + 1}} \tag{4} $$

and that local curvature in a curve is defined as the inverse of the local radius

$$ \small \kappa = \frac{1}{R} \tag{5} $$

then

$$ \small \cos \left (\varphi \right) = \frac{1}{\sqrt{\left(\frac{V^2{\cdot}\kappa}{g} \right)^2 + 1}} \tag{6} $$

This equation will be useful when we derive another set of equations, corresponding to the longitudinal degree of freedom. 

Local curvature of a bidimensional spline, which is parametrized in two degrees of freedom $x{\left (t \right)}$ and $y{\left (t \right)}$, can be calculated using the following formula.

$$ \small \kappa{\left (t \right)} = \left| \frac{x'{\cdot}y''-y'{\cdot}x''}{\left(x'^2 + y'^2 \right)^{\frac{3}{2}}} \right| \tag{7}$$

Piecewise splines parametrized with third order polynomials are only continuous up until the first derivative. This means that there are discontinuities in the spline curvature at the control points joining each section of the spline. However this is not a problem for aerobatic planes, since their high manoeuvrability enables them to adapt closely to these trajectories even in the control point sections.

Up until this point, the only mathematical concepts used where geometric and trigonometric relations, as well as the concept of force equilibrium and the definitions of centripetal force and the curvature of a parametrized curve.

Now we need to take into account the aerodynamic forces. We will model lift, $L$, and drag, $D$, forces using the following equations (more info in post []).

$$
\small
\begin{gathered}
    L=q{\cdot}S{\cdot}C_L \\
    D=q{\cdot}S{\cdot}C_D \\
\end{gathered}
\tag{8}
$$

Where $q$ is the dynamic pressure, defined as $\frac{1}{2}{\cdot}\rho{\cdot}V^2$, being $\rho$ the air density and $V$ the total velocity of the aircraft. Variable $S$ corresponds to the wing reference surface. Variables $C_L$ and $C_D$ correspond to the lift coefficient and drag coefficient respectively. We will define those as

$$
\small
\begin{gathered}
    C_L=C_{L_0} + C_{L_{\alpha}}{\cdot}\alpha \\
    C_D=C_{D_0} + K{\cdot}{C_L}^2 \\
\end{gathered}
\tag{9}
$$

Where $\alpha$ refers to the aircraft angle of attack, $C_{L_0}$ and ${C_{D_0}}$ refer to the lift and drag coefficients at zero angle of attack, and $C_{L_{\alpha}}$ and ${K}$ are aerodynamic parameters dependant on the specific aircraft.

Aicraft acceleration, $a$, can be modelled using Newton's first law of motion, having into account the vehicle mass, $m$.

$$
\small m{\cdot}a = T - D \tag{10}
$$

We can discretize the trajectory of the aircraft along the spline in small sectors. Considering $V_i$ the velocity at the start of a sector, $V_{med}$ the velocity at the middle of the sector, and $l$ the length of the sector, combining equations (6-9) we can approximate the acceleration at each sector by:

$$
\small a \approxeq \frac{\Delta V}{\Delta t} = \frac{2{\cdot}\left(V_{med} - V_i \right)}{\frac{l}{V_{med}}} = \frac{T - \frac{1}{2}{\cdot}\rho{\cdot}V_{med}^2{\cdot}S{\cdot}\left(C_{D_0} + K{\cdot}\left(\frac{m{\cdot}g}{\frac{1}{2}{\cdot}\rho{\cdot}V_{med}^2{\cdot}S{\cdot}\cos \left(\varphi \right)} \right)^2 \right)}{m} \tag{11}
$$

Where

$$ \small \cos \left(\varphi \right) = \frac{1}{\sqrt{\left(\frac{V_{med}^2{\cdot}\kappa}{g} \right)^2 + 1}} \tag{12} $$

The solution of system of equations (10) and (11) for variable $V_{med}$ in order to find the medium velocity at each timestep reduces to a quartic equation, which can be solved using Ferrari's formula.

$$ \small a{\cdot}V_{med}^4 + b{\cdot}V_{med}^3 + c{\cdot}V_{med}^2 + d{\cdot}V_{med} + e = 0 \tag{13} $$

Where coefficients $a$, $b$, $c$, $d$ and $e$ result in

$$
\small
\begin{aligned}
    4{\cdot}K{\cdot}l{\cdot}\kappa^2{\cdot}m^2 + C_{D_0}{\cdot}S^2{\cdot}l{\cdot}\rho^2 + 4{\cdot}S{\cdot}m{\cdot}\rho = a \\
    -4{\cdot}S{\cdot}V_i{\cdot}m{\cdot}\rho = b \\
    -2{\cdot}S{\cdot}T{\cdot}l{\cdot}\rho = c \\
    0 = d \\
    4{\cdot}K{\cdot}l{\cdot}g^2{\cdot}m^2 = e \\
\end{aligned}
\tag{14}
$$

Ferrari's formula uses the following relations which provide the analytic solution of the quartic equation [].

$$
\small
\begin{aligned}
    \Delta = 256{\cdot}a^{3}{\cdot}e^{3}-192{\cdot}a^{2}{\cdot}b{\cdot}d{\cdot}e^{2}-128{\cdot}a^{2}{\cdot}c^{2}{\cdot}e^{2}+144{\cdot}a^{2}{\cdot}c{\cdot}d^{2}{\cdot}e-27{\cdot}a^{2}{\cdot}d^{4} \\
    +144{\cdot}a{\cdot}b^{2}{\cdot}c{\cdot}e^{2}-6{\cdot}a{\cdot}b^{2}{\cdot}d^{2}{\cdot}e-80{\cdot}a{\cdot}b{\cdot}c^{2}{\cdot}d{\cdot}e+18{\cdot}a{\cdot}b{\cdot}c{\cdot}d^{3}+16{\cdot}a{\cdot}c^{4}{\cdot}e \\
    -4{\cdot}a{\cdot}c^{3}{\cdot}d^{2}-27{\cdot}b^{4}{\cdot}e^{2}+18{\cdot}b^{3}{\cdot}c{\cdot}d{\cdot}e-4{\cdot}b^{3}{\cdot}d^{3}-4{\cdot}b^{2}{\cdot}c^{3}{\cdot}e+b^{2}{\cdot}c^{2}{\cdot}d^{2}
\end{aligned}
\tag{15}
$$

&nbsp;

$$
\small
\begin{aligned}
    {\frac {8{\cdot}a{\cdot}c - 3{\cdot}b^{2}}{8{\cdot}a^{2}}} = p \\
    {\frac {b^{3} - 4{\cdot}a{\cdot}b{\cdot}c + 8{\cdot}a^{2}{\cdot}d}{8{\cdot}a^{3}}} = q
\end{aligned}
\tag{16}
$$

&nbsp;

$$
\small
\begin{aligned}
    c^{2} - 3{\cdot}b{\cdot}d + 12{\cdot}a{\cdot}e = \Delta_{0} \\
    2{\cdot}c^{3} - 9{\cdot}b{\cdot}c{\cdot}d + 27{\cdot}b^{2}{\cdot}e + 27{\cdot}a{\cdot}d^{2}-72{\cdot}a{\cdot}c{\cdot}e = \Delta_{1}
\end{aligned}
\tag{17}
$$

&nbsp;

$$
\small
\begin{aligned}
    {\sqrt[{3}]{\frac {\Delta _{1}+{\sqrt {\left| -27{\cdot}\Delta \right|}}}{2}}} = Q \\
    {\frac {1}{2}}{\sqrt {\left|-{\frac {2}{3}}\ p+{\frac {1}{3{\cdot}a}}\left(Q+{\frac {\Delta _{0}}{Q}}\right) \right|}} = R
\end{aligned}
\tag{18}
$$

&nbsp;

$$
\small
\begin{aligned}
    -{\frac {b}{4{\cdot}a}}-R \pm {\frac {1}{2}}{\sqrt {-4{\cdot}R^{2}-2{\cdot}p+{\frac {q}{R}}}} = V_{med_{1,2}} \\
    -{\frac {b}{4{\cdot}a}}+R \pm {\frac {1}{2}}{\sqrt {-4{\cdot}R^{2}-2{\cdot}p-{\frac {q}{R}}}} = V_{med_{3,4}}
\end{aligned}
\tag{19}
$$

We are interested in the biggest real solution to the polynomic equation.

$$ \small V_{med} = -{\frac {b}{4{\cdot}a}} + R + {\frac {1}{2}}{\sqrt {\left| -4{\cdot}R^{2}-2{\cdot}p-{\frac {q}{R}} \right|}} \tag{20} $$

Equation 19 defines the medium velocity at each small section of the spline as a function of the initial velocity at that section, the arclength of the section, aircraft thrust, local curvature of the spline, aerodynamic parameters such as $C_{D_0}$, $S$ or $K$ and physical properties of the system such as air density, acceleration due to gravity and the mass of the aircraft. Therefore, an iterative process can be made in order to calculate the velocity along an entire bidimensional spline. This process is similar to an integration of this variable along the spline, and if the section arclength is set to be sufficiently small then the associated errors of the numerical iterative process would become negligible.

Using this pipeline one could perform an optimization process in which bidimensional splines are generated to pass through $m$ control points (race pylons) and a total time is calculated for each of those splines, modifying the spline in order to minimize this parameter. The optimization should be performed to find a global minimum, since the complexity of the problem would originate many local minimums which could be a problem if using a local optimizer.

The global optimizer I chose to solve this problem is a Genetic Algorithm. A genetic algorithm (GA) is a method for solving both constrained and unconstrained optimization problems based on a natural selection process that mimics biological evolution. The algorithm repeatedly modifies a population of individual solutions. At each step, the genetic algorithm randomly selects individuals from the current population and uses them as parents to produce the children for the next generation. Over successive generations, the population "evolves" toward an optimal solution. You can apply the genetic algorithm to solve problems that are not well suited for standard optimization algorithms, including problems in which the objective function is discontinuous, nondifferentiable, stochastic, or highly nonlinear [].

I implemented this pipeline in the numerical computing environment MATLAB®. The code is accessible [here]. I tested the tool with a simple track example, which can be seen in the figure below.

<figure>
    <p align="center"><img src="/assets/img/article_images/rbar_006.png" width="80%"></p>    
    <figcaption><p align="center"><b>Figure 6</b> - Track waypoints</p></figcaption>
</figure>

The track includes five control waypoints. In order to solve the problem it is necessary to impose a trajectory heading at each waypoint, where we can define the heading as $\arctan{\left(\frac{y'}{x'} \right)}$. This way, the order complexity of the problem reduces to the number of waypoints, $m$. The global minimum total time trajectory calculated by the tool can be observed in the following figures.

<figure>
    <p align="center"><img src="/assets/img/article_images/rbar_007.png" width="80%"></p>    
    <figcaption><p align="center"><b>Figure 7</b> - Trajectory solution</p></figcaption>
</figure>

<figure>
    <p align="center"><img src="/assets/img/article_images/rbar_008.png" width="80%"></p>    
    <figcaption><p align="center"><b>Figure 8</b> - Solution X parametrization</p></figcaption>
</figure>

<figure>
    <p align="center"><img src="/assets/img/article_images/rbar_009.png" width="80%"></p>    
    <figcaption><p align="center"><b>Figure 9</b> - Solution Y parametrization</p></figcaption>
</figure>

<figure>
    <p align="center"><img src="/assets/img/article_images/rbar_010.png" width="80%"></p>    
    <figcaption><p align="center"><b>Figure 10</b> - Flight distance along trajectory</p></figcaption>
</figure>

This approach can be used to provide first approximations of track time, but is not precise enough to be practical in real races. More elements can be added to improve the pipeline, such as adding the third degree of freedom of altitude, taking into account more aerodynamic coefficients like the lift coefficient due to angle of attack, $C_{L_\alpha}$, and modelling these coefficients as a function of velocity using look-up tables.

### Other approaches

The solution to this problem needs to take into account many elements. First of all the dynamics associated with a moving vehicle on Earth. In other hand the own vehicle aerodynamics and thrust dynamics, and their relations with the vehicle control surfaces. Also, the point constraints associated with the control points (roll limits, velocity limits...), as well as the path constraints requirements along the entire trajectory (max G-force limits, position constraints inside the safety flight zone...).

One could try to apply a deep reinforcement learning method, like Deep Q-Learning. The goal of Q-learning is to learn a policy, which tells an agent what action to take under what circumstances. It does not require a model of the environment, and it can handle problems with stochastic transitions and rewards, without requiring adaptations []. However, the degree of complexity of the problem in hand is excessively high for this method. The space of possible states and actions is huge, making it impractical to apply this technique to optimize the entire trajectory.

Other approach to this optimal control problem is based on a technique called **direct collocation**. Direct collocation methods work by approximating the state and control trajectories using polynomial splines []. These methods are sometimes referred to as direct transcription. This technique can be used to transcribe the aicraft dynamics and all constraints into a problem which can be solved using **nonlinear programming**. In mathematics, nonlinear programming (NLP) is the process of solving an optimization problem where some of the constraints or the objective function are nonlinear.

In order to implement this technique, I used the library **falcon.m** []. This library is a free optimal control tool developed at the Institute of Flight System Dynamics at the Institute of Flight System Dynamics of the Technical University of Munich (TUM). It provides a MATLAB class library which allows to set-up, solve and analyze optimal control problems using numerical optimization methods. The code is optimized for usability and performance and enables the solution of high fidelity real-life optimal control problems with ease.

### Dynamic model

A precise dynamic model is essential for this project. This section presents a more complete aerodynamic model which can be used to model the aircraft. Vehicle aerodynamics are modelled by taking into account forces and moments. On textbooks on aerodynamics [] it is shown that, for a body of given shape with a given orientation to the freestream flow, the forces and moments are proportional to the product of freestream mass density, $\rho$, the square of the freestream airspeed, $V$, and a characteristic area of the body. When modelling aircraft aerodynamics, the characteristic area of the body is typically selected as the wing reference surface, $S$. The product of the first two quantities has the dimensions of pressure and it is convenient to define the *dynamic pressure*, $q$, by

$$ \small q=\frac{1}{2} \cdot \rho \cdot V^2 \tag{21} $$

We are now in a position to write down the mathematical models for the magnitudes of the forces and moments. The forces and moments acting on the complete aircraft are defined in terms of dimensionless aerodynamic coefficients in equations 2 and 3 respectively. Moment nondimensionalization is usually performed with additional parameters like wingspan, $b$, or wing mean chord, $c$.

$$
\small
\begin{gathered}
    L=q \cdot S \cdot C_L \\
    D=q \cdot S \cdot C_D \\
    Y=q \cdot S \cdot C_Y
\end{gathered}
\tag{22}
$$

$$
\small
\begin{gathered}
    l=q \cdot S \cdot b \cdot C_l \\
    m=q \cdot S \cdot c \cdot C_m \\
    n=q \cdot S \cdot b \cdot C_n
\end{gathered}
\tag{23}
$$

The aircraft aerodynamic coefficients are, in practice, specified as functions of the aerodynamic angles, velocity, and altitude. In addition, control surface deflections and propulsion system effects cause changes in the coefficients. A control surface deflection, $\delta_s$, effectively changes the camber of a wing, which changes the lift, drag, and moment.

Aerodynamic angles is the name given to two different angles:

* The **angle of attack**, $\alpha$, specifies the angle between the chord line of the wing of a fixed-wing aircraft and the vector representing the relative motion between the aircraft and the atmosphere. It is the primary parameter in longitudinal stability considerations.

* The **sideslip angle**, $\beta$, specifies the angle made by the velocity vector to the longitudinal axis of the vehicle in the local horizontal plane (North/East). The sideslip angle is essentially the directional angle of attack of the airplane. It is the primary parameter in directional stability considerations.

Angle of attack and sideslip angle definitions are schematized in figure 11.

[figure]

Consequently, force and moment coefficients can be approximated respectively by equations 24 and 25 defined below.

$$
\small
\begin{gathered}
    C_L=C_{L_0} + C_{L_{\alpha}} \cdot \alpha \\
    C_D=C_{D_0} + K \cdot {C_L}^2 + C_{D_{\beta}} \cdot \beta \\
    C_Y=C_{Y_{\beta}} \cdot \beta + C_{Y_{\delta r}} \cdot \delta r
\end{gathered}
\tag{24}
$$

$$
\small
\begin{gathered}
    C_l=C_{l_{\beta}} \cdot \beta + C_{l_{\delta a}} \cdot \delta a + C_{l_{\delta r}} \cdot \delta r + \frac{b}{2V} \cdot (C_{l_p} \cdot p + C_{l_r} \cdot r) \\
    C_m=C_{m_0} + C_{m_{\alpha}} \cdot \alpha + C_{m_{\delta e}} \cdot \delta e + \frac{c}{2V} \cdot (C_{m_q} \cdot q + C_{m_{\dot{\alpha}}} \cdot \dot{\alpha}) \\
    C_n=C_{n_{\beta}} \cdot \beta + C_{n_{\delta a}} \cdot \delta a + C_{n_{\delta r}} \cdot \delta r + \frac{b}{2V} \cdot (C_{n_p} \cdot p + C_{n_r} \cdot r)
\end{gathered}
\tag{25}
$$

Where aerodynamic derivative $C_{x_y}$ provides information about the effect on the variable $x$ caused by a unitary increment in the variable $y$. Aerodynamic derivatives $C_{L_0}$ and $C_{D_0}$ are called zero angle of attack lift and parasite drag respectively, and they represent the lift and drag contribution which is not due to any other variable and is present even at zero angle of attack.

The coefficients shown in equations 24 and 25 are called aerodynamic coefficients or derivatives, and they can be classified into three different groups:

* **Stability derivatives** - $C_{L_0}, C_{L_{\alpha}}, C_{D_0}, K, C_{D_{\beta}}, C_{Y_{\beta}}, C_{l_{\beta}}, C_{m_0}, C_{m_{\alpha}}, C_{n_{\beta}}$.

* **Control derivatives** - $C_{Y_{\delta r}}, C_{l_{\delta a}}, C_{l_{\delta r}}, C_{m_{\delta e}}, C_{n_{\delta a}}, C_{n_{\delta r}}$.

* **Damping derivatives** - $C_{l_p}, C_{l_r}, C_{m_q}, C_{m_{\dot{\alpha}}}, C_{n_p}, C_{n_r}$. 

Note that terms concerning damping derivatives are always nondimensionalized in the moment coefficients equations. The nondimensionalization factor is dependant on the reference axis.



## References

[1] Steven

[] https://en.wikipedia.org/wiki/Quartic_function

[] https://www.mathworks.com/discovery/genetic-algorithm.html

[] https://en.wikipedia.org/wiki/Q-learning#Deep_Q-learning

[] Betts, J.T.

[] http://www.fsd.mw.tum.de/software/falcon-m/

[] A. M. Kuethe and C. Y. Chow.Foundations of Aerodynamics. Wiley, 1984.
