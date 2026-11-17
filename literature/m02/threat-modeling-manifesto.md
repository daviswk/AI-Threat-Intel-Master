---
title: "Threat Modeling Manifesto"
publisher: "Threat Modeling Manifesto working group"
source_url: https://www.threatmodelingmanifesto.org/
retrieved: 2026-11-17
sha256: 9ff3837689c36fd52c8f22fd8d1deda13b35c6fa826a74c5f4c1a7bfe19de8e5
converter: markdownify 1.2.3
source_format: html
licence: "CC BY 4.0"
module: 2
verified: true
---
### What is threat modeling?

Threat modeling is analyzing representations of a system to highlight concerns about security and privacy characteristics.

At the highest levels, when we threat model, we ask [four key questions](https://github.com/adamshostack/4QuestionFrame "“Shostack's 4 Question Frame for Threat Modeling” by Adam Shostack, a member of the Threat Modeling Manifesto group."):

1. What are we working on?
2. What can go wrong?
3. What are we going to do about it?
4. Did we do a good enough job?

### Why threat model?

When you perform threat modeling, you begin to recognize what can go wrong in a system. It also allows you to pinpoint design and implementation issues that require mitigation, whether it is early in or throughout the lifetime of the system. The output of the threat model, which are known as threats, informs decisions that you might make in subsequent design, development, testing, and post-deployment phases.

### Who should threat model?

You. Everyone. Anyone who is concerned about the privacy, safety, and security of their system.

### How should I use the Threat Modeling Manifesto?

Use the Manifesto as a guide to develop or refine a methodology that best fits your needs. We believe that following the guidance in the Manifesto will result in more effective and more productive threat modeling. In turn, this will help you to successfully develop more secure applications, systems, and organizations and protect them from threats to your data and services. The Manifesto contains ideas, but is not a how-to, and is methodology-agnostic.

The Threat Modeling Manifesto follows a similar format to that of the [Agile Manifesto](https://agilemanifesto.org/ "The “Manifesto for Agile Software Development” created in 2001 identifies software development values and principles, some of which align with this Threat Modeling Manifesto.") by identifying the two following guidelines:

* **Values**: A value in threat modeling is something that has relative worth, merit, or importance. That is, while there is value in the items on the right, we value the items on the left more.
* **Principles**: A principle describes the fundamental truths of threat modeling. There are three types of principles: (i) fundamental, primary, or general truths that enable successful threat modeling, (ii) patterns that are highly recommended, and (iii) anti-patterns that should be avoided.

# Values

We have come to value:

* **A culture of finding and fixing design issues** over checkbox compliance.
* **People and collaboration** over processes, methodologies, and tools.
* **A journey of understanding** over a security or privacy snapshot.
* **Doing threat modeling** over talking about it.
* **Continuous refinement** over a single delivery.

# Principles

We follow these principles:

* **The best use of threat modeling is to improve the security and privacy of a system through early and frequent analysis.**
* **Threat modeling must align with an organization’s development practices and follow design changes in iterations that are each scoped to manageable portions of the system.**
* **The outcomes of threat modeling are meaningful when they are of value to stakeholders.**
* **Dialog is key to establishing the common understandings that lead to value, while documents record those understandings, and enable measurement.**

These patterns benefit threat modeling:

##### Systematic Approach

Achieve thoroughness and reproducibility by applying security and privacy knowledge in a structured manner.

##### Informed Creativity

Allow for creativity by including both craft and science.

##### Varied Viewpoints

Assemble a diverse team with appropriate subject matter experts and cross-functional collaboration.

##### Useful Toolkit

Support your approach with tools that allow you to increase your productivity, enhance your workflows, enable repeatability and provide measurability.

##### Theory into Practice

Use successfully field-tested techniques aligned to local needs, and that are informed by the latest thinking on the benefits and limits of those techniques.

These anti-patterns inhibit threat modeling:

##### Hero Threat Modeler

Threat modeling does not depend on one’s innate ability or unique mindset; everyone can and should do it.

##### Admiration for the Problem

Go beyond just analyzing the problem; reach for practical and relevant solutions.

##### Tendency to Overfocus

Do not lose sight of the big picture, as parts of a model may be interdependent. Avoid exaggerating attention on adversaries, assets, or techniques.

##### Perfect Representation

It is better to create multiple threat modeling representations because there is no single ideal view, and additional representations may illuminate different problems.

# About

Our intention for the Threat Modeling Manifesto is to share a distilled version of our collective threat modeling knowledge in a way that should inform, educate, and inspire other practitioners to adopt threat modeling as well as improve security and privacy during development.

We developed this Manifesto after years of experience thinking about, performing, teaching, and developing the practice of, Threat Modeling. We have diverse backgrounds as industry professionals, academics, authors, hands-on experts, and presenters. We bring together varied perspectives on threat modeling. Our ongoing conversations, which focus on the conditions and approaches that lead to the best results in threat modeling, as well as how to correct when we fail, continue to shape our ideas.

We provide a [PDF version](https://github.com/Threat-Modeling-Manifesto/threat-modeling-manifesto/releases/download/1/threat-modeling-manifesto.pdf) of the manifesto and this website is also [print friendly](javascript:window.print();).

You can always find the current version of this manifesto at <https://www.threatmodelingmanifesto.org/>.

This work is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).

### Authors

The working group of the Threat Modeling Manifesto consists of individuals with years of experience threat modeling for security or privacy.

* [Zoe Braiterman](https://twitter.com/zbraiterman)
* [Adam Shostack](https://adam.shostack.org/)
* [Jonathan Marcil](https://twitter.com/jonathanmarcil)
* [Stephen de Vries](https://iriusrisk.com/)
* [Irene Michlin](https://twitter.com/IreneMichlin)
* [Kim Wuyts](https://twitter.com/wuytski)
* [Robert Hurlbut](https://twitter.com/RobertHurlbut)
* [Brook S.E. Schoenfield](https://twitter.com/BrkSchoenfield)
* [Fraser Scott](https://twitter.com/zeroXten)
* [Matthew Coles](https://twitter.com/coles_matthewj)
* [Chris Romeo](https://twitter.com/edgeroute)
* [Alyssa Miller](https://twitter.com/AlyssaM_InfoSec)
* [Izar Tarandach](https://twitter.com/izar_t)
* [Avi Douglen](https://twitter.com/sec_tigger)
* [Marc French](https://twitter.com/appsecdude)

The working group would like to thank Loren Kohnfelder and Sheila Kamath for their technical edit review and expert feedback on the document content and structure.

### Resources

* [New manifesto offers CISOs an agile guide to threat modeling](https://www.scmagazine.com/news/threat-hunting/new-manifesto-offers-cisos-an-agile-guide-to-threat-modeling) article by Derek B. Johnson, SC Magazine
* [The Threat Modeling Manifesto – Part 1](https://appsec.buzzsprout.com/1730684/8122585) on the Application Security Podcast
* [The Threat Modeling Manifesto – Part 2](https://appsec.buzzsprout.com/1730684/8122584) on the Application Security Podcast
* [Threat Modeling Manifesto defines the foundation of threat modeling](https://www.old.linddun.org/post/threat-modeling-manifesto-defines-the-foundation-of-threat-modeling) article by Kim Wuyts, LINDDUN privacy
* [Twitter list of all the authors](https://twitter.com/i/lists/1320580732327137280) by Jonathan Marcil
* [Security Pros Push for More Pervasive Threat Modeling](https://www.darkreading.com/application-security/security-pros-push-for-more-pervasive-threat-modeling/d/d-id/1339506) article by Robert Lemos, DARKReading
* [Threat modeling gets its manifesto: Map out your app sec risk first](https://techbeacon.com/security/threat-modeling-gets-its-manifesto-how-map-out-your-app-sec-risk) article by John P. Mello Jr., TechBeacon
* [How Matters As Much As What & Why](https://www.linkedin.com/pulse/how-matters-much-what-why-brook-schoenfield/) LinkedIn article by Brook Schoenfield
* [A threat modelling experience](https://www.youtube.com/watch?v=ARjlRFQN7XM&t=1855) talk by Brook S.E. Schoenfield, OWASP BeNeLux-Day 2020
* [Continuous Threat Modeling for Development Teams](https://www.youtube.com/watch?v=ARjlRFQN7XM&t=3665) talk by Izar Tarandach, OWASP BeNeLux-Day 2020
* [Using the Threat Modeling Manifesto to Get Your Team Going](https://web.archive.org/web/20240423212853/securityintelligence.com/posts/using-threat-modeling-manifesto-to-get-going/) By Irene Michlin
* [The Threat Modeling Manifesto Posters](https://agilestationery.com/products/threat-modeling-manifesto-poster) on Agile Stationery
* [Threat Model Diversity](https://brookschoenfield.com/?p=360) by Brook Schoenfield
* [Boost Pipeline Efficiency with Threat Modeling](https://www.devseccon.com/blog/boost-pipeline-efficiency-with-threat-modeling-secadvent-day-3) by Alyssa Miller
* [Privacy. Privacy by design. Privacy engineering.](https://www.devseccon.com/blog/privacy-glitter-and-unicorns-secadvent-day-2) by Kim Wuyts
* [Threat Modeling Manifesto Panel](https://www.youtube.com/watch?v=CZxPZ-G3Gys), Open Security Summit 2020
* [Using the Threat Modeling Manifesto to Build an Enterprise Threat Modeling Program](https://www.youtube.com/watch?v=jeHL8PXtezc) by Chris Romeo, LASCON 2021
* [Threat Modeling Manifesto in a Mobile First World](https://www.youtube.com/watch?v=jgcO23RmSw4) by Chris Romeo at DevSecOps Bunch
* [Threat Modeling: A Manifesto And Some Code](https://www.youtube.com/watch?v=9Fu6BKMJnvw) by Matthew Coles and Izar Tarandach at DevSecOps - London Gathering
