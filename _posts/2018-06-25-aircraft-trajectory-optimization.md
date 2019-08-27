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
