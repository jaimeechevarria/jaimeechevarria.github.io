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

&nbsp;

Participant teams usually spend a significant amount of time trying to predict optimal aircraft trajectories to follow for each track, in an effort to achieve the fastest possible lap times.

In early 2018 I started working in a personal project to develop an analysis tool which enabled a temporal-space study of optimal trajectories for different race tracks.

The problem is not trivial. Let’s start from the beginning.

&nbsp;

### What is the objective?

Races usually have two types of obstacles: Airgates of single or double pylons. Pilots are required to fly near the single pylons and between the double pylons, following a predetermined route as fast as possible.

<figure>
    <p align="center"><img src="/assets/img/article_images/rbar_002_003.jpg" width="80%"></p>    
    <figcaption><p align="center"><b>Figure 2</b> - Single pylon (left) and double pylons or gates (right)</p></figcaption>
</figure>

&nbsp;

There exist several restrictions to take into consideration, including the following:

* Pilots must fly through the double pylon air gates in level flight. This is, the aircraft has to be flying straight when passing through these airgates.
* Pilots must fly through the airgates while inside the altitude range indicated by the red bands in the pylons.
* Aircraft must never cross any safety line, which delimit the compulsory safety flight area.
* Aircraft must not surpass the acceleration limit of 10 G.
* Aircraft must not start the race with a velocity higher than 200 knots.

&nbsp;

### How could we approach this problem?

This is an optimization problem with several types of constraints. We need to find a way to simplify the problem in order to reduce complexity.

Let’s try a simple approach by making some hypotheses:

* Aircraft trajectories are **smooth** because the aircraft movement is always restricted by inertia. This means these trajectories can be approximated by some type of mathematical **curve**.
* This kind of air races usually take place in 2D planes, since aircraft fly most of the time at the same altitude. Let’s forget about the third degree of freedom for now.
* Aircraft longitudinal acceleration when flying straight is mostly dictated by the engine thrust and its **aerodynamic resistance**.
* Aerodynamic resistance grows exponentially with aircraft **lift**.
* When an aircraft is performing a turn, lift needs to be increased in order to maintain altitude.
Turning angle (**roll**) is dictated by the **curvature** of the aircraft trajectory.

Given this statements, a direct relation can be extrapolated between the trajectory local curvature and the aircraft acceleration at that location.

But what type of mathematical curve may an aircraft trajectory look like? One option is **cubic splines**.



<img src="https://latex.codecogs.com/svg.latex?\Large&space;x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}" title="\Large x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}" />