---
title: "NIST SP 800-160 Vol. 1 Rev. 1, Engineering Trustworthy Secure Systems (Appendix D, Trustworthy Secure Design, and Appendix E, Principles for Trustworthy Secure Design)"
publisher: "NIST"
source_url: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-160v1r1.pdf
retrieved: 2026-11-17
sha256: eced250e47e542698ddfd5e72bd7feae14268e72a1e9ea49af9984c0e01ff7b8
converter: pymupdf4llm 2.1
source_format: pdf
pages: "86-117"
licence: "US government work (NIST)"
module: 1
verified: true
---
Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 November 2022 

# **Appendix D.  Trustworthy Secure Design** 

This appendix discusses the approach and considerations for applying technical<sup>63</sup> concepts of a trustworthy secure system design. The concepts described provide a balanced and integrated approach that optimally protects against asset loss. The discussions include the design approach for trustworthy systems (Section D.1), authorized and intended behaviors and outcomes of the system (Section D.2), security design order of precedence (Section D.3), and functional design and trade space considerations (Section D.4). 

A principled system design strengthens trustworthiness claims [2]. The concepts in this appendix and the principles in Appendix E provide a sound basis for reasoning about a system and enable the demonstration of system trustworthiness. Applying concepts and principles and using other enablers (e.g., standards, specifications, design patterns, security policy models, cryptographic algorithms, security protocols, strength of mechanism, and known adversities) should be planned for, appropriately scoped, and revisited throughout the system life cycle and engineering effort. 

Finally, trustworthiness and assurance needs and considerations also inform trustworthy secure design. <u>Appendix F</u> provides further discussion of the concepts of trustworthiness and assurance. 

## **TRUSTWORTHY SECURE DESIGN** 

Trustworthy secure design is a means to provide stakeholders with the confidence that their conflicting capability needs, concerns, priorities, and constraints are satisfied. 

# **D.1. Design Approach for Trustworthy Systems** 

The design approach for engineering trustworthy secure systems is intended to establish and maintain the ability to deliver system capabilities at an acceptable level of performance<sup>64</sup> while minimizing the occurrence and extent of loss. This approach provides a system structure for optimal employment of the engineered features and devices. The system design must provide the intended behaviors and outcomes, avoid the unintended behaviors and outcomes, prevent loss, and limit loss when it occurs. A trustworthy secure design includes a situational awareness capability and margin<sup>65</sup> to account for adversity due to the unknowns and uncertainty inherent in the system and in its operational environment. The situational awareness capability helps to determine accountability for the actions of all users and entities (e.g., audit, logging, event 

> 63 Note that human factor elements of trust are not discussed. A system may be trustworthy, but a user may not trust it. Similarly, a user may trust an untrustworthy system. 

> 64 An acceptable level of performance lies between the minimum threshold of acceptability and the objective of maximum performance. This level may vary across operational or system states and modes (e.g., patrolling in clear weather versus severe weather conditions), may vary across contingency conditions (e.g., normal, degraded), and may be subject to operational priorities (e.g., search and rescue, manhunt). 

> 65 The term _margin_ refers to a spare amount, measure, or degree allowed or given for contingencies or special situations. The allowances are carried to account for uncertainties and risks. Two types of margins are used in systems engineering: design margin and operational margin. See the design principle of _<u>Loss Margins</u>_ <u>.</u> 

70 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 

November 2022 

recording) and detect pending and actual failure (e.g., by crossing the threshold of the margins that have been established). The design principle of _<u>Anomaly Detection</u>_ embodies this capability. 

The design approach includes the following elements:<sup>66</sup> 

- Define the intended behaviors and outcomes for the system<sup>67</sup> 

- Identify the system states and conditions that reflect the intended behaviors and outcomes 

- Identify the system states and conditions that potentially lead to loss in the system 

- Select and alter the system design to prevent loss to the extent practicable (preferred) and limit the loss that does occur (where, when, and to the extent necessary and practicable) 

- Iterate the above elements to address how the functions that serve to prevent or limit loss may fail due to intentional or unintentional reasons 

Figure 15 illustrates the steps in the design approach in the context of the Systems Security Engineering Framework described in <u>Chapter Four.</u> 



**Fig. 15.** Design Approach in a Systems Security Engineering Framework 

The approach to trustworthy design includes both preemptive and reactive aspects. These mutually reinforcing aspects provide the protection needed to achieve only the authorized and intended behaviors and outcomes. The preemptive aspect results in system features and system actions taken to prevent and limit loss before the loss occurs, while the reactive aspect results in system actions to limit loss and its effects once a loss has occurred. Figure 16 illustrates a balanced design strategy that includes preemptive and reactive aspects. 

> 66 These steps are useful in applying a system control concept for any loss-relevant emergent property (e.g., safety, resilience). 

> 67 This flow iterates through systems engineering as the system is decomposed. Subsequent iterations would apply within the elements that comprise the system of interest (i.e., the subsystems, assemblies, and components). 

71 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 

November 2022 



**Fig. 16.** Balanced Design Strategy for Achieving Trustworthy Secure Systems 

The preemptive aspect recognizes the conditions under which loss may occur and addresses the scenarios before loss occurs (i.e., what can happen). If the loss does occur, the results are limited due to system features and actions taken in advance. The preemptive aspect is independent of any specific knowledge of attacks and attacker objectives, instead focusing on what is possible in the system’s life cycle. The reactive aspect recognizes the limits of certainty about what can happen, and that new, unanticipated, and otherwise unforeseen adverse consequences will occur despite proactive planning and instituting of means and methods to control loss and the extent of its consequences. The reactive aspect promotes informed operational decision-making after the system is in use and a loss condition occurs, proactively providing an operations capability to address the loss condition and handle the loss. The reactive aspect complements the preemptive 

72 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 November 2022 

aspect by providing an informed basis and means for an external entity (e.g., a human operator or system) to act when failures occur. Essentially, the reactive aspect is a proactive engineering activity about providing a reactive capability. 

An effective design will optimize protection against loss to the extent practical while recognizing that losses will occur irrespective of the protections put in place. Optimization decisions across preemptive and reactive approaches must consider assets, stakeholders, concerns, and objectives. Achieving a proper mix requires establishing security objectives and conducting requirements elicitation and analysis to unambiguously ascertain the scope of security in terms of addressing failure and the associated consequences in its preemptive and reactive aspects. 

# **D.2. Design Considering Emergence** 

A system is expected to deliver the required capabilities as authorized, as intended, and at the specified level of performance. It should not deliver unauthorized or unintended capabilities. One cause of unintended behaviors and outcomes lies with the concept of _emergence_ . Emergence refers to the behaviors and outcomes that result from how individual system elements compose to form the system beyond the collection of behaviors and outcomes of the individual system elements. This composition is covered in the design principle of _<u>Structured Decomposition and Composition</u>_ and illustrated in Figure 2. 

Some emergence is desired and productive; other emergence is not desired or productive, creating unknown, unforeseen, or adverse effects.<sup>68</sup> Engineering trustworthy secure systems seeks to deliver only desired emergence. Trustworthiness judgments are based on the expectation that the system can satisfy the stated capability needs. To achieve this, the design must address emergence at all levels of system abstraction in terms of how the system is decomposed into its constituent elements and how those system elements compose to produce the system. This is covered in the design principle of _<u>Compositional Trustworthiness</u>_ <u>.</u> 

## **SECURITY IS EMERGENT** 

The objective of security is to achieve only authorized and intended system behaviors and outcomes. This requires a fundamental understanding of how individual system elements are composed into the system as a whole. Systems are designed from that basis of understanding to limit emergent behaviors and outcomes that are not specified (including desired and undesired unspecified behaviors and outcomes). 

> 68 Emergence may be described in terms of properties exhibited by entities only when attributed to the whole, not to any individual constituent element. 

73 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 November 2022 

# **D.3. Security Design Order of Precedence** 

The security design order of precedence (SecDOP)<sup>69</sup> is a design approach with the objective of minimizing the system design basis for loss potential. SecDOP emphasizes the importance of establishing a secure structural context for the employment of engineered features and devices. Using a principled engineering approach, the SecDOP eliminates susceptibility, hazard, and vulnerability to the extent practicable, thereby eliminating the associated risk. For those cases in which susceptibility, hazard, or vulnerability cannot be eliminated, the SecDOP reduces the potential of experiencing a loss to an acceptable level within the constraints of cost, schedule, and performance. The SecDOP identifies design alternatives in order of decreasing effectiveness, thus enabling a maximized return on investment. 

The SecDOP alternatives are: 

# • **Eliminate the potential for loss through design selection** 

Susceptibility, hazard, and vulnerability are eliminated by selecting a design or material alternative that completely removes susceptibility, hazard, and vulnerability and, thus, prevents loss. 

   - _Example:_ The design selected for a system function of interest results in the minimum number of external interfaces to other systems and the minimum number of internal interfaces that provide the required functions. Since every interface presents a potential for susceptibility, hazard, and vulnerability, a design selection with the minimum number of interfaces results in less susceptibility, hazard, and vulnerability than a design that includes additional and unnecessary internal and external interfaces. 

   - _Note:_ The design selection also considers the need to accommodate mechanisms that provide mediated access and trusted communication as these engineered features and devices are necessary for a secure system. 

- **Reduce the potential for loss through design alteration** 

If adopting an alternative design or material to eliminate susceptibility, hazard, and vulnerability is not feasible, consider design changes or material selections that would reduce the frequency, potential, severity, and/or extent of loss caused by the susceptibility, hazard, or vulnerability. 

- _Example:_ The selected design has interfaces and, therefore, has inherent susceptibilities, hazards, and vulnerabilities, both with respect to interactions with the environment and with respect to interactions within the system. The potential for loss can be reduced by altering design to segment functionality that interacts with external entities and influences from functionality strictly within system boundaries. 

- _Note:_ The design alteration also considers the need to accommodate mechanisms that provide mediated access and trusted communication, as these engineered features and devices are necessary for a secure system. 

> 69 The security design order of precedence is inspired by the System Safety Design Order of Precedence, an optimized design approach for system safety described in [34]. 

74 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 November 2022 

# • **Incorporate engineered features or devices to control the potential for loss** 

If preventing, limiting, or reducing the potential for loss through design alteration and material selection is not feasible or adequate, employ engineered features and devices to control loss associated with susceptibility, hazard, and vulnerability. In general, engineered features actively disrupt the loss scenario sequence and interactions, and devices reduce the potential, severity, and extent of loss. 

Two general types of engineered features and devices employed to address the potential for loss associated with the system function of interest are: 

   - _Mandatory security features and devices:_ Mandatory security features and devices apply foundational security principles to the interfaces. For example, each interface must have mediated access to control access to and use of the capability and data provided by the interface. 

   - _Function-specific features and devices:_ Function-specific security features and devices protect against a loss associated with the design’s ability to meet functional requirements and performance parameters. Engineered features such as redundant data and control flows and redundant system elements can supplement the design selection to achieve the required protection. The system may also have engineered features that enable external entities to intervene in the system to address the potential, severity, or extent of loss. 

- **Provide visibility and feedback to external entities** 

If design alteration, material selection, and engineered features and devices are not feasible or do not adequately lower the frequency, potential, severity, or extent of loss caused by the susceptibility, hazard, or vulnerability, employ engineered detection and feedback systems and warning devices to alert external entities to the presence of a susceptible, hazardous, or vulnerable condition; the occurrence of an event that will lead to a loss; or an actual loss event. External entities include operational personnel, monitoring systems, or other systems capable of responding. 

   - _Example:_ Anomaly detection features can be used to provide situational awareness data and warnings to system users. 

   - _Note:_ The visibility and feedback provided is not of value if the external entities are not able to respond appropriately. For example, the visibility and feedback must be provided in a timely manner and be in a form that can be interpreted correctly. 

- **Incorporate signage, procedures, training, and proper equipment** 

Incorporate procedures, training, signage, and proper equipment where design alternatives, design changes, and engineered features and devices are not feasible and warning devices cannot adequately lessen the potential, severity, or extent of loss caused by the hazard, susceptibility, or vulnerability. Procedures and training include proper warnings and cautions and may prescribe the use of equipment. The use of signage, procedures, training, and equipment as the only means to reduce the potential, severity, or extent of loss should be avoided. 

75 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 

November 2022 

- _Example:_ Procedures and training address the proper use of the system function of interest, the use of mediated access functions, and the relevant warnings, cautions, and warning systems. 

## **ON USING SECURITY CONTROLS** 

Common practice in some communities is to select and overlay systems with security controls (i.e., management, operational, and technical safeguards or countermeasures) as a primary means to address security concerns [67] [68]. But as observed in [69], “Poor systems security engineering is very difficult to mitigate by overlaying security controls, whereas security controls overlaid on a sound, secure design can be quite effective.” 

The Security Design Order of Precedence, as part of a systems engineering practice, helps to ensure a proper integration of _technical_ controls and _operational_ controls. 

# **D.4. Functional Design Considerations** 

This section describes the functional design considerations for trustworthy secure systems. These considerations include (1) assured functions that provide control enforcement, control decision, and control infrastructure; (2) design criteria for mechanisms; (3) security function failure analysis; (4) situational awareness; and (5) trade space considerations. 

# **D.4.1. Roles for Security-Relevant Control** 

All functions have the potential to influence behaviors and outcomes beyond themselves and are relevant to security.<sup>70</sup> However, some functions have dedicated security purposes (e.g., functions that support audit capabilities). Examples include the protection control functions. 

Protection control functions enforce or contribute to the control of or otherwise directly influence system or system element behaviors and outcomes. These functions may be characterized and evaluated by using the following designations: 

- _Protection Control Decision Functions:_ These functions make authorization decisions or take other actions for protection control enforcement functions. For example, a function that decides to grant or deny access to a resource based on a request (e.g., from a protection control enforcement function). 

- _Protection Control Enforcement Functions:_ These functions enforce a constraint to ensure that the system or system element exhibits only authorized and intended behaviors or 

> 70 Historically, the term _security relevance_ has been used in secure system design and evaluation to differentiate the role of system functions that either singularly or in combination exhibit a behavior, produce an outcome, or provide a capability to enforce authorized and intended system behaviors or outcomes. However, from the security perspective (Section 3.8) and the possibility of loss due to weaknesses and defects in any system function, all functions have loss-related concerns and, thus, protection concerns. 

76 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 

November 2022 

outcomes. For example, a protection control enforcement function enforces a decision to grant or deny access to a resource. 

- _Protection Control Infrastructure Functions:_ These functions support and help protection control enforcement and control decision functions fulfill their purposes. The functions also provide data or services or perform operations upon which protection control enforcement and decision functions depend. For example, a protection control infrastructure function includes secure storage, secure communication, and anomaly detection mechanisms. 

Other functions, including control functions for other purposes besides protection, can potentially adversely affect the correct operation of the protection control functions. For the purposes of secure design and evaluation, the functions are designated _other system functions_ . Ideally, these functions should be non-interfering. This non-interference objective may be achieved through assurance with constraints on the requirements, architecture, design, and use of these functions. 

System functions can be mapped to one or more protection control decision functions, protection control enforcement functions, or protection control infrastructure functions, or other system functions for the purpose of secure design and evaluation. The distinction guides and informs a principled design to limit interference among functions with confidence. Such confidence can be achieved by employing _<u>Trustworthy System Control</u>_ <u>, applying the design criteria described in Section D.4.2, and optimally placing a function in the system architecture to limit the side effects</u> and interactions that may interfere with the protection control functions. 

System analyses can determine the extent to which functions may interfere with other functions, including identifying any needed actions to increase assurance (Appendix F). For example, to satisfy a specific size or form-factor constraint, a system function mapped to a system function designated as “other” may occupy the same privilege domain as control enforcement, control decision, or control infrastructure functions, thereby elevating the privilege of that system function. If the size or form-factor constraint does not exist, it would be prudent to allocate that system function elsewhere to avoid giving the function elevated privilege. This would increase the assurance that the enforcement, decision, and infrastructure functions are isolated from the other parts of the system and would not be adversely impacted by their behavior or provide an avenue for attack. 

# **D.4.2. Essential Design Criteria for Mechanisms** 

To effectively achieve the objectives of trustworthy secure design, mechanisms (i.e., engineered features and devices) must satisfy four essential design criteria. They must be non-bypassable, evaluatable, always invoked, and tamper-proof [35]. Generally, a design for any control function that provides protection should adhere to these criteria.<sup>71</sup> Table 3 briefly describes the essential design criteria. 

> 71 The argument that any control function should be non-bypassable, evaluatable, always invoked, and tamper-proof follows from an in-depth examination of Systems Theoretic Process Analysis (STPA) as described in [36], specifically the discussions on why controls may fail and how to address failure. 

77 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 November 2022 

**Table 3.** Essential Design Criteria for Mechanisms 

|**ESSENTIAL DESIGN**<br>**CRITERIA**|**DESCRIPTION**|
|---|---|
|**NON-BYPASSABLE**|The mechanism must not be circumventable.|
|**EVALUATABLE**|The mechanism must be sufficiently small and simple enough to be assessed to produce<br>adequate confidence in the protection provided, the constraint (or control objective)<br>enforced, and the correct implementation of the mechanism. The assessment includes the<br>analysis and testing needed. (Clear Abstractions, Reduced Complexity, andStructured<br>Decomposition and Composition)|
|**ALWAYS INVOKED**|The protection provided by a mechanism or feature that is not always invoked is not<br>continuous, and, therefore, a loss may occur while the mechanism or feature is suspended<br>or turned off. (Continuous Protection)|
|**TAMPER-PROOF**|The mechanism or feature and the data that the mechanism or feature depends on cannot<br>be modified in an unauthorized manner.|



The design criteria described above are based on the generalized reference monitor concept. The reference monitor concept<sup>72</sup> is an abstract model of the necessary and sufficient properties that must be achieved by any mechanism that performs an access mediation control function [21] [37]. The reference monitor concept is a foundational access control concept for assured system design. It is defined as a trustworthy abstract machine that mediates all accesses to objects by subjects [38]. As a concept for an abstract machine, the reference monitor does not address any specific implementation. A reference validation mechanism, which includes a combination of hardware and software, realizes the reference monitor concept to provide the access mediation foundation for a trustworthy secure system. 

The generalized reference monitor concept and the four essential design criteria can be used effectively as the design basis for individual system elements, collections of elements, networks, and systems where intentional and unintentional adversity can prevent the realization of a loss. The reference monitor concept drives the need for rigor in engineering activities commensurate with the trust to be placed in the system or its constituent system elements.<sup>73</sup> The concept describes an abstract model of the necessary properties that must be realized by any mechanism that claims to achieve a constraint or set of constraints and the basis for determining the extent to which the properties are satisfied. A mechanism that achieves successful constraint has two parts: (1) a means to decide whether to constrain or not constrain and (2) enforcement of the decision. Enforcement of the decision must sufficiently: 

- Enforce constraints to achieve only the authorized and intended system behaviors and outcomes 

- Provide self-protection against targeted attacks on the mechanism enforcing the decision (including applying the essential design criteria) 

> 72 The reference monitor concept is described in the _<u>Trustworthy System Control</u>_ principle in <u>Appendix E.</u> 

> Conceptually, the reference monitor concept can be extended to any control function that is to enforce a system constraint [39]. 

78 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 

November 2022 

• Be absent of self-induced, emergent, erroneous, unsafe, and non-assured control actions 

The protection characteristics for mechanisms must account for but not depend on having detailed knowledge of the capability, means, and methods of an adversary. 

# **D.4.3. Security Function Failure Analysis** 

The design principle of _<u>Protective Failure</u>_ states that a failure of a particular system element should neither result in an unacceptable loss nor invoke another loss scenario. The failure of a security function is of special concern, given the need for security functions to always be invoked and operating correctly. Consequently, failure analyses must be performed during system design to determine the impacts of security function failure on the system capabilities. 

Failure analyses consider the assets that may be impacted by security function failure and the associated loss consequences. Failure analyses also consider the function allocation to system elements and the way the system function and element combination interacts with other system function and element combinations, independent of specific events and conditions that might lead to the failure. The principles for trustworthy secure design in <u>Appendix E serve to guide and</u> inform the analyses. 

The outcomes of the security function failure analyses also drive assurance levels and objectives, as well as the fidelity and rigor of architecture, design, and implementation methods employed to achieve those objectives. Assurance considerations are discussed in Appendix F. 

## **THE SCIENCE BEHIND SECURITY** 

“Each of these [design] requirements [for mechanisms] is significant, for without them, the mechanism cannot be considered secure. The [need to be tamperproof] is obvious, since if the reference validation mechanism can be tampered with, its validity is destroyed, as is any hope of achieving security through it. The [third] requirement of always invoking the reference validation mechanism simply states that if the reference validation is (or must be) suspended for some group of programs, then those programs must be considered part of the security apparatus and be [tamper-proof and evaluatable]. The [evaluatable] requirement is equally important. It states that because the reference validation mechanism is the security mechanism in the system, it must be possible to ascertain that it works correctly in all cases and is always invoked. If this cannot be achieved, then there is no way to know that the reference validation correctly takes place in all cases, and therefore there is no basis for certifying a system as secure.” 

**-- James P. Anderson** 

The Anderson Report [37] 

79 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 November 2022 

# **D.4.4. Situational Awareness** 

_Situational awareness_ is a foundational security means objective. That is, to achieve other security objectives, situational awareness is necessary and must be accounted for in design. For example: 

- Mediating access requires situational awareness in cases where rules for granting access involve timing, sequence, state, and other conditions about the system and prior access. 

- Preventing and limiting loss are informed by comprehensive data and information about system states and conditions ( _<u>Anomaly Detection</u>_ <u>).</u> 

Situational awareness requires the ability to accurately detect, capture, record, and analyze the needed characteristics and details of the system’s behaviors and actions at a frequency and with the granularity necessary to act and/or inform external entities for subsequent action to be taken.<sup>74</sup> False positives and false negatives are to be avoided to the extent practicable. 

Given the potential consequences of compromises of situational awareness capabilities and wrongful attribution, the mechanisms used must meet the essential design criteria (Section D.4.2) with the appropriate rigor. The system audit logs and other system records often need stringent protection, such as using _<u>Distributed Privilege</u>_ for access and storing the logs and records in a separate subsystem ( _<u>Domain Separation</u>_ <u>).</u> 

# **D.4.5. Trade Space Considerations** 

System design involves trade space decisions. Decision-making about protecting assets is guided by a determination of valuation that informs asset criticality and priority (e.g., assessing the positive effect in achieving objectives and the negative effect for any loss associated with an asset). The criticality and priority based on valuation are used in investment decisions on the type, rigor, and expected effectiveness of protection ( _<u>Commensurate Protection</u>_ <u>). Decisions may</u> also be guided by the costs and benefits from different design options. 

The costs associated with a trustworthy secure design approach include the cost to acquire, develop, integrate, operate, and sustain the security features; the cost of the security features and functions in terms of their system performance impact; the cost of security services used by the system; the cost of developing and managing life cycle documentation and training; and the cost of obtaining and maintaining the target level of assurance. 

The cost of analysis to substantiate the trustworthiness claims of certain design choices is also an important trade space factor. Given two equally effective design options, the more attractive of the two options may be the one that has a lower relative cost to obtain the assurance needed to demonstrate satisfaction of trustworthiness claims. In all cases, assess the cost of system security at the system level; and consider trustworthiness objectives and the cost that is driven by the assurance activities necessary to achieve the trustworthiness objectives. Trustworthiness design 

> 74 Common organizational actions include (1) responses to security-relevant anomalies, such as remedial training for users or replacing the right system component responsible for undesired system behaviors, and (2) audits of system activities, including assessing for suspicious patterns of access that indicate insider threats and to satisfy accountability regulations, such as those required of financial institutions. 

80 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 November 2022 

principles such as _<u>Commensurate Rigor</u>_ and _<u>Commensurate Trustworthiness</u>_ inform the trade space analysis. 

The benefits of a design option are determined by its effectiveness in providing the required protection capability, the trustworthiness that can be placed on it, and the loss potential associated with it, given the value, criticality, exposure, and importance of the assets protected. An optimal balance between cost and benefit may be realized by using a less costly combination of engineering activities and system features and functions rather than the use of a single costprohibitive activity or security feature or function. Moreover, an adverse performance impact may preclude some security options. 

## **CONSERVATION OF RISK** 

“The law of conservation of energy states that energy can neither be created nor destroyed, only change in form. This law has many important implications in engineering, including implying the impossibility of creating a perpetual motion machine … There is a parallel pseudo-principle that is often offered in a half-joking maxim – risk can neither be created nor destroyed, only moved around. It is not universally true [but] it is worthwhile considering the pseudoprinciple because often, a change to a design often does end up ‘squeezing the risk balloon,’ only to discover that the risk appears elsewhere, perhaps in an unexpected place in the system, which could cause the defended system to be less secure than the engineering intended.” 

### **-- O. Sami Saydjari** 

_Engineering Trustworthy Secure Systems_ [62] 

81 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 November 2022 

# **Appendix E.  Principles for Trustworthy Secure Design** 

This appendix describes the design principles that serve as the foundation for engineering trustworthy secure systems.<sup>75</sup> The principles provide a basis for reasoning about a system. They should not be applied as _rules_ to be complied with, nor should they be prioritized, sequenced, or ordered for prescriptive application or used as a basis for making judgments on conformance. 

The use of the design principles is subject to various priorities and constraints that may restrict or preclude their application within a specific context.<sup>76</sup> The principles may conflict with other principles, and that conflict must be understood. In practice, the principles can be satisfied or implemented in various and often equally effective ways. The use of specific principles may change in response to changes and variances in requirements, architecture, design, and risk acceptability. Therefore, their application should be planned for, appropriately scoped, and revisited throughout the engineering effort. 

## **KEY SECURITY OBJECTIVE** 

An important objective for security is the reduction of uncertainty regarding the occurrence and effects of adverse events. Reducing the uncertainty of adverse events is achieved by eliminating hazards, susceptibility, and vulnerability to the extent possible. Where elimination cannot occur, their effects should be controlled to the extent possible. Applying the design principles for trustworthy secure systems is a means of achieving the elimination and control of the hazards, susceptibility, and vulnerability that lead to adverse events [39]. 

The principles for trustworthy secure design are representative of the practices of the safety, security, reliability, survivability, and resilience communities and the specialty engineering disciplines associated with those communities. Collectively, the goals of these practices represent the _end objectives_ that the system must satisfy for trustworthy control of adverse effects. The principles are grounded in research, development, and application experience starting with the early incorporation of mechanisms into trusted operating systems to today’s components, environments, and systems and are expected to remain universally applicable for new, emerging, and maturing approaches. The concepts and theorems from the disciplines of computer science, computer engineering, systems engineering, control systems, fault/failure tolerance, software engineering, and mathematics – as employed across the communities and specialties – constitute the means to achieve the end objectives.<sup>77</sup> The principles for trustworthy secure design are listed in Table 4. 

> 75 NIST acknowledges the significant contributions of the Naval Postgraduate School Center for Information Systems Security Studies and Research and The MITRE Corporation in providing content for this appendix. The content was informed by the research reports of the principal investigators from those organizations [21] [39]. 

> 76 Engineering judgment considerations for the application of the principles for trustworthy secure systems are described in [39]. 

> 77 For example, trustworthiness requires that mechanisms be evaluatable (Section D.4.2). Consequently, many principles deal with reducing and managing complexity and creating systems that can be more easily evaluated. See [41] for discussions on how systems may be too complex to be analyzed for adequate assurance. 

82 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 November 2022 

**Table 4.** Principles for Trustworthy Secure Design 

|**DESIGN PRINCIPLE**|**DESIGN PRINCIPLE**|
|---|---|
|Anomaly Detection|Least Privilege|
|Clear Abstractions|Least Sharing|
|Commensurate Protection|Loss Margins|
|Commensurate Response|Mediated Access|
|Commensurate Rigor|Minimal Trusted Elements|
|Commensurate Trustworthiness|Minimize Detectability|
|Compositional Trustworthiness|Protective Defaults|
|Continuous Protection|Protective Failure|
|Defense in Depth|Protective Recovery|
|Distributed Privilege|Reduced Complexity|
|Diversity (Dynamicity)|Redundancy|
|Domain Separation|Self-Reliant Trustworthiness|
|Hierarchical Protection|Structured Decomposition and Composition|
|Least Functionality|Substantiated Trustworthiness|
|Least Persistence|Trustworthy System Control|



# **E.1. Anomaly Detection** 

**Principle:** Any salient anomaly in the system or its environment is detected in a timely manner that enables effective response action. 

_Note:_ The purpose of anomaly detection is to identify the need to take corrective action to address a loss condition that has occurred or that will occur if conditions that affect the system behavior are allowed to persist. Anomaly detection is critical to achieving loss control objectives to prevent and limit loss and its adverse effects. The detection of such anomalies requires monitoring system behaviors and outcomes to determine when any deviations from the design intent occur. It also requires monitoring conditions in the environment to identify or forecast those conditions that can cause an anomaly in the system if corrective action is not taken. 

The “timely manner” aspect of anomaly detection reflects the urgency to detect emerging loss conditions as early as possible. Early detection increases response action options, such as graduated response options, and ensures that response actions have sufficient time to have an effect. When the determination of response involves humans in the loop, early detection enables a more reasoned judgment of proper response. 

Anomaly detection can be implemented at varying levels of abstraction (e.g., system, sub-system, assembly, function, mechanism) and may occur in periodic, aperiodic, or event-driven manners. The basis for anomaly detection within the system is the expectation that the system behaviors, outcomes, and interactions produced are expected to remain consistent, adhere to some norm, or are deterministic across all system states and modes. The types of anomalies include those associated with the results of system behavior; state consistency; continuity of function; integrity, correctness, and trustworthiness of system elements; system configuration; and the abuse or misuse of the system. 

The basis for anomaly detection in the environment differs from that in the system because the environment is not under the control of the system. The environment presents a wide range of adversity to the system, and the system is designed to achieve its design intent within defined bounds of 

83 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 

November 2022 

environmental conditions. Those bounds can be treated as the “norm” for anomaly detection, whereby environmental conditions that are trending beyond the norm or that reflect conditions outside of the norm may result in an adverse effect on the system, thus requiring a planned response to prepare for an impending difficulty or crisis. 

Anomaly detection requires capturing data to support all intended response actions for a detected anomaly, including attribution-related data. Consequently, the fidelity in data describing the anomaly must be commensurate with the consequences of the loss scenarios associated with the anomaly and of wrong responses in addressing the detected anomaly. The responses taken will often rely on attribution to uniquely identifiable entities that may be responsible for undesired actions, behaviors, or outcomes. For non-human entities, corrective actions may include component replacements, repairs, or other corrections. For human entities, these may include training, remediation, or disciplinary actions. Wrongful attribution may have undesired consequences, such as the cost of unnecessarily repairing the wrong system element while an undesired condition persists or the wrongful termination of an individual. Attribution rigor is driven by the needed proof that an entity is responsible for an anomaly. 

Three aspects of anomaly detection are necessary to provide criteria for an appropriate response action or set of actions: 

- _Basis for Correctness:_ A system model provides a basis against which actual behavior and outcomes can be compared to confidently enable conclusions that an anomaly exists or to determine or forecast that an anomaly is about to occur. System models include normal, contingency, degraded, and other system states/modes of operation and account for the adversity to which the system is subjected. 

- _Data Collection:_ Systems capture self-awareness data in the form of health, status, test, and other data indicative of actual behavior and outcomes, including traceability to support attribution. Terms for data collection include instrumentation, monitoring, logging, auditing, self-tests, and built-in tests. 

- _Data Interpretation:_ The interpretation of data allows for conclusions of unacceptable or suspicious events that have happened (e.g., halt or failure condition), that are progressing (e.g., approaching a threshold of failure condition), or that can be expected to happen (i.e., in the absence of change, the failure condition will occur), including tracing to responsible entities to inform appropriate responses to events. 

Caution must be taken with the use of design features that may hinder anomaly detection. Poorly designed lines of defense for defense in depth have been found to conceal emerging dangerous system states and conditions, especially from human observers [40]. The system design must minimize the difference between estimated system states and conditions and actual system states and conditions. 

Two approaches to anomaly detection are: 

- _Self-Anomaly Detection:_ An entity has no dependency on another entity to detect an anomaly within the scope of its intended design. Self-anomaly detection usually involves an axiomatic or environmentally enforced assumption about its integrity. Typically, trusted elements have the capability for self-anomaly detection. This means that at the highest level of trustworthiness, an entity must be able to assess its internal state and functionality to a meaningful extent at various stages of execution. The detected anomalies must correlate to the trustworthiness assumptions placed on the entity. 

- _Dependent Anomaly Detection:_ An entity-of-interest is dependent on another entity for some or all anomalies that are detected. When an entity-of-interest relies on another entity for any portion of the assessment, that entity must be at least as trustworthy as the entity-of-interest. 

**References:** [20] [40] [43] 

84 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 November 2022 

# **E.2. Clear Abstractions** 

**Principle:** The abstractions used to characterize the system are simple, well-defined, accurate, precise, necessary, and sufficient. 

_Note:_ Abstractions can help manage the complexity of the system [24]. Clarity in the abstract representations of the system facilitates an accurate understanding of the system and how the system functions to deliver the required capability. Clear abstractions also reduce the potential for misunderstanding or misinterpretation of what is represented by the abstraction. Applying the principle of clear abstractions means that a system has simple, well-defined interfaces and functions that provide a consistent and intuitive view of the data and how it is managed. The elegance (e.g., accuracy, precision, simplicity, necessity, sufficiency) of the system interfaces – combined with a precise definition of the functional behavior of the interfaces – promotes ease of analysis, inspection, and testing, as well as the correct and secure use of the system. Examples that reflect the application of this principle include avoidance of redundant, unused interfaces; information hiding;<sup>78</sup> and avoidance of semantic overloading of interfaces or their parameters (e.g., not using one function to provide different functionality, depending on how it is used). 

It is important to ensure that the proper rigor is applied in the development of system abstractions during design. Clarity in the abstract representation of the system requires the use of well-defined syntax and semantics with elaboration as needed to ensure that the representations are well-defined, precise, necessary, and sufficient. Clear abstractions promote confidence in analysis, verification, and the correct use of the system. Abstractions can be achieved using models, including Systems Modeling Languages. 

**References:** [2] [20] [21] [24] 

# **E.3. Commensurate Protection** 

**Principle:** The strength and type of protection provided to a system element are commensurate with the most significant adverse effect that results from a failure of that element. 

_Note:_ The strength and effectiveness of the protection for a system element must be proportional to the need. As the need increases, the protection of that element should also increase to the same degree. Need is derived from the most significant adverse effect associated with the system element or the trust that is placed in the element. The protection can come in the form of the system element’s own self-protection, from protections provided by the system architecture, or from protection provided by other elements. The needed strength of protection is independent of these design choices (or others, such as distributed versus centralized design), a concept sometimes referred to as secure distributed composition [2]. Furthermore, confidence in the effectiveness of the protections provided to a system element should also increase commensurate to the need. This is addressed by the principle of _<u>Commensurate Rigor</u>_ <u>.</u> 

**References:** [2] [21] 

# **E.4. Commensurate Response** 

**Principle:** The system design matches the aggressiveness of an engineered response action’s effect to the needed immediacy to control the effects of each loss scenario. 

> 78 The term _information hiding_ , also called representation-independent programming, is a design discipline to ensure that the internal representation of information in one system component is not visible to another system component invoking or calling the first component, such that the published abstraction is not influenced by how the data may be managed internally. 

85 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 November 2022 

_Note:_ The selected response to a detected anomaly considers three factors to determine the effect that the response has on the loss and the system: 

- The effectiveness and aggressiveness of the engineered response to directly address the anomaly and to prevent or limit the loss 

- The direct, residual, or side effect of the response on the system 

- The opportunities that remain to take other response actions should the selected response fail to achieve the intended result 

Responses can be achieved by a combination of manual, semi-automated, fully automated, or autonomous means. However, the response action is distinct from the determination that a response is necessary and from the notification or signaling that invokes the response action. 

Commensurate responses require consideration of the response-effect-consequence relationship associated with a specific loss. Ideally, for any given need for a response, a single action taken will be effective to resolve the loss concern and will have no associated adverse effect. Practically, due to complexity and the limits of certainty, the response action may not have the desired effect, may compound the problem, or may cause another problem. The balance required is one that determines if, when, and how a response action should be taken to be initially more aggressive or initially less aggressive. The severity of the problem and the time available for an effective response dictate a strategy for a continuum of responses, characterized by two extremes: 

- _Graduated Response:_ A graduated response is initially the least aggressive or impactful action possible to prevent the loss from continuing or escalating and does so with consideration of the possible side effects associated with the response action. The graduated response allows for taking increasingly more aggressive action should the loss situation persist or escalate. 

- _Ungraduated Response:_ An ungraduated response is the most aggressive and impactful action to prevent the loss from continuing or escalating and does so without consideration of the potential side effects associated with the response action. The ungraduated response recognizes the severity of the loss as justifying the most aggressive action, even if that option provides no alternatives should it fail to have the intended or desired effect or if it causes other losses to occur. 

Without early observability of potential loss, the option for a graduated response may not exist. A commensurate response is aided by early detection, which in turn increases the options for a graduated response. 

**References:** [40] 

# **E.5. Commensurate Rigor** 

**Principle:** The rigor associated with the conduct of an engineering activity provides the confidence required to address the most significant adverse effect that can occur. 

_Note:_ Rigor determines the scope, depth, and detail of an engineering activity. Rigor is a means of providing confidence in the results of a completed engineering activity. Generally, an increase in rigor translates to an increase in confidence in the results of the activity. Further, increased confidence reduces the uncertainty that can also reduce risk or provide a better understanding of what to address to achieve risk reduction. The relationship between rigor and the criticality of data and information used to make decisions is recognized by systems analysis practices [4]. 

The principle of commensurate rigor helps to ensure that the concept of rigor is included as an equal factor in the trade space of capability, adverse effect, cost, and schedule in the planning and conduct of engineering activities, method and tool selection, and personnel selection. An increase in rigor may 

86 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 November 2022 

translate into an increase in the cost of personnel, methods, and tools required to complete rigorous engineering activities or an increase in schedule to accomplish the activities with the expected rigor. Any increased cost that may occur can be justified by acquiring confidence about system performance to limit loss while also addressing the system’s ability to deliver the capability. Therefore, the rigor associated with an engineering activity should be commensurate with the significance of the most adverse effect associated with the activity. 

**References:** [2] [4] 

# **E.6. Commensurate Trustworthiness** 

**Principle:** A system element is trustworthy to a level commensurate with the most significant adverse effect that results from a failure of that element. 

_Note:_ A trusted element continuously exhibits properties of trust during the time that it is depended upon by other system elements. The degree of trustworthiness needed for a trusted element is determined by those entities that depend on the element. Some basis is required to support decisions about trust and trustworthiness. The basis includes expressing the trust that is to be placed in a system element, expressing the trustworthiness that is exhibited by the element, and comparing the trustworthiness of different system elements. This principle is particularly relevant when considering systems and elements with complex chains of trust dependencies. 

**References:** [4] [20] 

# **E.7. Compositional Trustworthiness** 

**Principle:** The system design is trustworthy for each aggregate composition of interacting system elements. 

_Note:_ The trustworthiness of an aggregate of composed system elements cannot be assumed based on the trustworthiness assertions of each individual element in the aggregate. Further, the trustworthiness of an aggregate of composed trustworthy system elements cannot be assumed to be equal to the trustworthiness of the least trustworthy element in the aggregate. By definition, a system is a combination of interacting system elements. Each system function results from the emergent behavior of a composed set of system elements. Similarly, the trustworthiness of a composed set of system elements is an emergent property of the composition. Therefore, the trustworthiness of the composed set of system elements (i.e., aggregate) for a given system function must be determined by treating the aggregate as a single discrete element. The compositional trustworthiness principle addresses how an argument can be made for system-level trustworthiness given how the constituent elements of the system compose to form the system and do so by adhering to the composition principles. 

**References:** [2] [4] [36] [42] 

# **E.8. Continuous Protection** 

**Principle:** The protection provided for a system element must be effective and uninterrupted during the time that the protection is required. 

_Note:_ The protection capability must be uninterrupted across all relevant system states, modes, and transitions for there to be assurance that the system can be effective in delivering the required capability while controlling loss. Continuous protection requires adherence to the following principles: 

87 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 

November 2022 

- _<u>Trustworthy System Control:</u>_ Every controlled action is constrained by the mechanism, and the mechanism can protect itself from tampering. Sufficient assurance of the correctness and completeness of the mechanism can be ascertained from analysis and testing. 

- _<u>Protective Failure</u>_ and _<u>Protective Recovery:</u>_ A protective state is preserved during error, fault, failure, and successful attack, as well as during the recovery of assets or of recovery to normal, degraded, or alternative operational modes. 

Continuous protection applies to all configurations, states, and modes of the system, as well as the transitions between those configurations, states, and modes. The system design must ensure that protections are coordinated and composed in a non-conflicting and mutually supportive manner across the non-behavioral aspects of the system structure and the behavioral aspects of system function and data flow. 

While the design for continuous protection applies for the entire time that the protection is required, the protection capability is sometimes intentionally disabled (e.g., Battleshort<sup>79</sup> intentional override). The intentional disabling/override of protection is an exception case and, therefore, does not violate this principle. That is, the principle of continuous protection applies only for the entirety of time that the protection is required and not knowingly and intentionally disabled.<sup>80</sup> 

**References:** [21] 

# **E.9. Defense In Depth** 

**Principle:** Loss is prevented or minimized by employing multiple coordinated mechanisms. 

_Note:_ The coordinated deployment of multiple protective mechanisms for a system helps to avoid single points of failure. The principle of defense in depth has three pillars: 

- Multiple lines of defenses or barriers should be placed along loss scenario sequences. 

- Loss control should not rely on a single defensive element. 

- The successive barriers should be diverse in nature and include technical, operational, and organizational barriers [52]. 

Defense in depth requires the use of coordinated mechanisms (active) within an architectural structure (passive) that achieves the depth characteristic.<sup>81</sup> Ideally, the initial lines of defense prevent loss, while subsequent lines of defense block loss scenario escalation and/or contain loss and potential consequences when needed. A defense-in-depth strategy examines loss scenarios for those points of opportunity to prevent or contain loss. It also leverages the opportunities to use active or passive mechanisms or constraints to meet loss control objectives. 

The coordination of defense-in-depth mechanisms (i.e., combinations of structural, data, and control flow coordination) in conjunction with other design principles (e.g., _<u>Anomaly Detection</u>_ <u>,</u> _<u>Commensurate Response</u>_ <u>) reflects a design strategy to satisfy the specified loss control objectives.</u> 

While defense in depth distributes the protection capability to many components, a defense-in-depth strategy may also consider a distributed composition to a line of defense. A protection capability provided by a single system component is a potential single point of failure or bottleneck to system performance. It 

> 79 Battleshort is the capability to bypass normal interlocks in mission-critical equipment (e.g., equipment that must not be shut down or the mission function will fail) during battle conditions [51]. 

> 80 However, the inclusion of a capability for intentionally disabling/overriding protection requires additional control features, devices, and associated analysis for the enforcement of constraints to prevent the inadvertent actuation of the override capability. 

> 81 While the discussion in this section is limited to the machine, defense in depth may involve a combination of technical, operational, and organizational elements. Additional discussion on defense in depth can be found in [52]. 

88 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 November 2022 

may also raise other concerns. A distributed composition of a defense layer may provide additional options within the coordination of layers. 

Defense in depth is, in part, a form of the principle of _<u>Protective Failure</u>_ <u>. It helps satisfy the objective that</u> a failure of a system element should not result in an unacceptable loss. However, it does not satisfy the objective that a failure of a system element should not invoke another loss scenario. 

**References:** [2] [21] [40] [47] 

# **E.10. Distributed Privilege** 

**Principle:** Multiple authorized entities act in a coordinated manner before an operation on the system is allowed to occur. 

_Note:_ Distributed privilege<sup>82</sup> is a means to require agreement and coordination from multiple entities when performing an operation, thereby preventing a single entity from acting alone. Distributed privilege separates, divides, or in some other manner distributes the privileges required to perform an operation among multiple entities. This distribution includes a set of rules, conditions, and constraints that describe how multiple entities must interact through positive actions before a requested operation can proceed and be completed. The rules, conditions, and constraints may reflect combinations of the following: 

- _Simultaneous Actions:_ Multiple different authorized entities execute a command within a specified time window. 

- _Sequenced Actions:_ Multiple different entities interact within a linear sequence of actions where each successive action is enabled only by the successful completion of a prior action. 

- _Parallel Actions:_ Multiple entities execute sequences concurrently, and success is achieved either by a consensus of the results of each concurrent action or by voting among the participants. 

Defeating distributed privilege requires collusion to take an unauthorized or improper action. In the case of an attack, distributed privilege forces the adversary to target all of the entities to whom privilege is distributed. 

**References:** [21] [46] 

# **E.11. Diversity (Dynamicity)** 

**Principle:** The system design delivers the required capability through structural, behavioral, or data or control flow variation. 

_Note:_ A system design that incorporates diversity helps to avoid common mode failures and introduces unpredictability to adversaries, thus complicating the planning and execution of where, when, and how to target their attacks. While the system behaviors that result from a design may be unpredictable from the viewpoint of the adversary, the design itself must be predictable and verifiable in achieving only the intended outcomes. The options for diversity include variety in the system structural and architectural design elements, the system functional and behavioral elements, the interfaces and interconnections between interfaces, the data and control flow, and the technology and component selection. Diversity can reside in: 

- Fixed or static characteristics of the system (e.g., multiple instances of a system element, multiple communication channels) 

> 82 Saltzer and Schroeder [46] originally named this the separation of privilege. It is also equivalent to separation of duty. 

89 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 

November 2022 

- Variable or dynamic characteristics of the system (e.g., reconfiguration, relocation, refresh of system elements; random routing of data over different communication channels from source to destination; the ability to change aspects of the system behavior, structure, data, or configuration in a random but nonetheless verifiable manner) 

A design approach that includes diversity in structure, configuration, communications, protocols, and similar or dissimilar system elements (e.g., N-version, heterogeneity) increases uncertainty due to the increased complexity of the design and the behaviors and outcomes that stem from emergent effects, side effects, and feature interaction. This drives the need for confidence that the design approach will deliver only the authorized and intended functional behavior, produce only the authorized and intended outcomes, and do so in a manner that allows for control over side effects, emergence, and feature interaction. 

Diversity options include intentionally designed regular or irregular changes in the system (e.g., implementing the concept of dynamicity). A design incorporating dynamicity can (1) complicate the attack planning of an adversary, (2) reduce the potential for non-adversarial adversity to have an effect on the system, (3) provide the margin to deliver a required capability while reducing actual losses, and (4) protect against the effects of an attack. Dynamic change may refer to either shifting the target or shifting the behaviors of a target in performing its activities (e.g., frequency hopping complicates attempts to intercept or jam signals within wireless communications). 

The uncertainty and diminished predictability associated with the employment of diversity and dynamicity in design can be problematic where it impedes or prevents having confidence that the system will function and produce outcomes only as authorized and intended. It is important to differentiate where the uncertainty lies: (1) uncertainty in how the system achieves an end objective (i.e., the means to an end) or (2) uncertainty that an objective will be achieved (i.e., achieving the end). A design that employs diversity and dynamicity must be based on acquiring confidence that the system will produce only the desired results despite uncertainty in knowing exactly how the desired results are achieved. This constitutes a design trade that is specific to diversity- and dynamicity-based designs. Diversity may have a cost (e.g., hardware, software, maintenance, training, assurance) greater than the value or effectiveness that it provides. 

**References:** [20] [47] [45] 

# **E.12. Domain Separation** 

**Principle:** Domains with distinctly different protection needs are physically or logically separated. 

_Note:_ The separation of domains enables enhanced control and, therefore, protection of system function and the flow of data. Control relative to separated domains limits the extent to which an entity or domain is influenced by or is able to influence some other entity or domain, thereby enhancing the protection of a domain. This is achieved through the control of information flow and data between domains as well as control over the use of a system capability between domains. 

The differing protection needs that are used to define domains may be thought of in terms of protecting the domain from influence by external entities (i.e., susceptibility) and protecting external entities from erroneous behavior that occurs within the domain (i.e., containment). This distinction may include separating critical functions from less critical functions, such as separating the flight control functions of a transport aircraft from the environmental control functions that maintain a safe environment for the cargo and passengers being transported. 

Historically, domain separation has been used to enforce the separation of roles or privileges. For example, a system may separate an “administrative” or “supervisor” domain from “user” domains. The 

90 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 November 2022 

administrative domain is accessible only by system administrators with proper privileges, and distinctly administrative functions may only be executed by administrators from the administrative domain. Similarly, data intended to be accessed only by administrators and administrative functions (e.g., system configurations) is stored and accessed only within that domain, ensuring needed protection of the data. 

Domain separation requires a domain to be contained within its own protected subsystem so that elements of the domain are only directly accessible by procedures or functions of the protected subsystem. The concept of isolation enables the implementation of domain separation. Isolation limits the extent to which one domain can influence or can be influenced by other entities. The challenge is that the system elements within domains must at times interact with other elements and the environment to deliver a capability. Every interface that results from design decisions can diminish domain separation while achieving requirements for a system capability. External requests for resources or functions within protected subsystems are arbitrated at these interfaces. Firewall, data diodes, and cross-domain solutions (CDS) are examples of mechanisms that enable varying degrees of control over the interactions between separated domains. 

Encryption is another mechanism often used to provide domain separation. For example, communication between distinct subsystems within a domain may be encrypted with a key that is known only to the subsystems within the domain. Where a common storage module or subsystem is used for multiple domains, encryption may be used to limit information access to the domain that owns the key to decrypt. 

**References:** [21] [43] 

# **E.13. Hierarchical Protection** 

**Principle:** A system element need not be protected from more trustworthy elements. 

_Note:_ Hierarchical protection is a simplifying assumption for trade decisions to help determine where emphasis is placed in providing protection and the extent of the protection effectiveness. The simplifying assumption introduces susceptibilities to system elements that are dependent on more trustworthy elements. The assumption relies on validated trust assertions about the more trustworthy element and acceptable uncertainty associated with behavior outside of the scope of the validated trust assertions. For example, systems may include a human element, which is often the more trustworthy element. The assertions of the trusted human are violated for the malicious insider threat. The extent to which any element is considered trustworthy has limits, and beyond those limits, the element should not be assumed to remain trustworthy. In the degenerate case of the most trustworthy system element, it must protect itself from all other elements. For example, if an operating system kernel is deemed the most trustworthy component in a system, then it must protect itself from the less trustworthy applications it supports. However, the applications do not need to protect themselves from the operating system kernel. 

**References:** [2] [43] 

# **E.14. Least Functionality** 

**Principle:** Each system element has the capability to accomplish its required functions but no more. 

_Note:_ Susceptibility and vulnerability increase unnecessarily when a system element provides more functionality than is needed to achieve its intended purpose. Least functionality reduces the potential for susceptibility and vulnerability and reduces the scope of analysis of the system element’s trustworthiness and loss potential. The strictest interpretation of least functionality is to prohibit any system element functions that are not required. Where that is not possible or practical, the unnecessary functions of the system element should be disabled, disarmed, or put into a “safe” mode that prevents the functions from 

91 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 

November 2022 

being used. In all other cases, mediated access can be used to prevent access to and use of the unneeded functions. 

An example of when it may not be possible or practical to avoid unnecessary functions is the use of commercial off-the-shelf (COTS) components. COTS components typically contain functions beyond those required to fulfill their intended purpose. In such cases, the components should be configured to enable only the functions that are required to fulfill their purpose and prohibit or restrict functions that are not required to fulfill their purpose. 

# **References:** [2] [21] 

# **E.15. Least Persistence** 

**Principle:** System elements and other resources are available, accessible, and able to fulfill their design intent only for the time for which they are needed. 

_Note:_ Least persistence reduces susceptibility. It limits the extent to which functions, resources, data, and information remain present, accessible, and usable when not required, thereby reducing the opportunity for their inadvertent or unauthorized use, modification, or activation. 

The broadest interpretation of least persistence is to not install, instantiate, or apply power to system elements and resources until needed and to completely remove system elements or power from system elements and resources when they are no longer required. When it is not possible or practical to do so, those system elements and resources should be fully disabled, disarmed, or put into safe mode to prevent their ability to function or be used. Finally, when it is not possible to disable, disarm or put into safe mode, access to those elements and resources should be mediated to constrain the time and duration of their use ( _<u>Mediated Access</u>_ ). 

Three conditions must be satisfied for an active system element or resource to be usable, and two of these conditions apply to non-active elements or resources: 

- _Presence (active and non-active):_ The system element or resource must be installed, loaded, residing in memory (software), and configured. 

- _Accessible (active and non-active):_ The system element or resource must be invoked, interacted with, or operated on. 

- _Able to Function (active):_ The system element or resource must be able to execute (i.e., powered on, enabled, or armed) to deliver a service or perform a function. 

Least persistence is reflected in concepts such as sanitizing, erasing, and clearing memory and/or storage locations; disabling, removing, and disconnecting network ports, system interfaces, and the services provided by system interfaces; powering off and unplugging hardware when not needed; and instantiating software just before need and de-instantiating after it is no longer needed. Least persistence has added benefits that include simplifying the processes of: 

- Cleansing the system element to remove corrupted aspects or side effects 

- Re-establishing the system element to a known state (i.e., a refresh) 

- Minimizing the time in which system elements are exposed to the environment, to attack, and to erroneous behavior 

Where system elements or resources are removed and then restored as needed, there must be a trusted representation of the system element and a trusted ability to instantiate that system element within the time constraints for its use. 

92 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 November 2022 

# **References:** [53] 

# **E.16. Least Privilege** 

**Principle:** Each system element is allocated privileges that are necessary to accomplish its specified functions but no more. 

_Note:_ System elements can be implemented by entities such as hardware, firmware, software, and personnel. By design, the system must be able to limit the scope of a system element’s actions. This has two desirable effects: (1) the impact of a failure, corruption, or misuse of the element is minimized, and (2) the analysis of the system element is simplified. A design driven by least privilege considerations results in a sufficiently fine granularity of privilege decomposition and the ability for the fine-grained allocation of privileges to human and machine elements. 

The application of the principle of least privilege means allocating to a system element only the privileges that are necessary to permit that element to perform the functions required of it. This could include a need to modify, delete, use, or configure a resource, or to authorize, start/enable, or stop/disable a process [20]. 

Least privilege can inform the use of other principles such as the employment of _<u>Domain Separation</u>_ and _<u>Structured Decomposition and Composition</u>_ . That is, the system modules can be designed so that only the system elements encapsulated by the module are directly accessed or operated on by the functions within the module, thus aiding the implementation of least privilege. 

**References:** [2] [20] [21] [46] 

# **E.17. Least Sharing** 

**Principle:** System resources are shared among system elements only when necessary and among as few elements as possible.<sup>83</sup> 

_Note:_ Sharing via common mechanism and other means can increase the susceptibility of system resources (e.g., data, information, system variables, interfaces, functions, services) to unauthorized access, disclosure, use, or modification and can adversely affect the capabilities provided by the system. According to Saltzer and Schroeder [46], “Every shared mechanism (especially one involving shared variables) represents a potential information path between users and must be designed with great care to be sure it does not unintentionally compromise security.” A design that employs least sharing helps reduce the adverse consequences that can result from sharing system functions, state, resources, and variables among different system elements. A system element that corrupts a shared state or shared variables has the potential to corrupt other elements whose behavior is dependent on the state. Minimized sharing also helps to simplify the design and implementation [54]. 

Two criteria provide the basis for applying the principle of least sharing: (1) share only if absolutely necessary, and (2) minimize sharing if allowed. The first criterion is a trade decision that weighs the cost and benefit of sharing resources against the increased exposure that results from the sharing. The second criterion is a constraint on the extent of sharing. 

**References:** [2] [21] [46] [54] [55] 

> 83 The historically well-known security design principle _least common mechanism_ is an instance of least sharing. The principle of least common mechanism is described in [55]. 

93 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 November 2022 

# **E.18. Loss Margins** 

**Principle:** The system is designed to operate in a state space sufficiently distanced from the threshold at which loss occurs. 

_Note:_ Margins refer to the difference between a conservative threshold at which the system is expected to operate while subjected to adversity and the point at which the adversity results in failure. Loss margins are created by engineered features put in place to maintain operational conditions and the associated adversity level at some distance (i.e., conservative threshold) from the estimated critical adversity threshold or loss-triggering threshold. Loss margins also allow for increased time to (1) detect the need for a response action ( _<u>Anomaly Detection</u>_ <u>), (2) determine what the response action should be</u> ( _<u>Commensurate Response</u>_ <u>), and (3) complete the selected response action. When there is uncertainty</u> about the effectiveness of the response action, loss margins need to allow time to evaluate response effectiveness, determine any additional actions needed, and complete any selected actions. 

Uncertainty may derive from the operational environment, the design and realization of the system, the utilization and sustainment of the system, and the adversity presenting itself to the system. Loss margins are effective in addressing uncertainty about how and when a loss-triggering event occurs. Specifically, loss margins are effective in addressing uncertainty associated with: 

- Intelligently designed and executed attacks, including attacks that persist and evolve over time 

- Unknown, unquantified, and underappreciated susceptibilities, threats, vulnerabilities, hazards, and associated risks 

For designs that incorporate loss margins, uncertainty about adversity makes determining the losstriggering thresholds difficult. Loss margins for design should be determined with a balance between certainty (i.e., what has happened and can happen again) and uncertainty (i.e., what has not happened but can happen, or what has happened but can also happen in a different way). Loss scenarios that include loss escalation and an estimation of the critical threshold for loss occurrence are helpful in making design decisions that incorporate loss margins. Loss scenarios also help to determine the limits of adversitydriven decisions due to uncertainty in knowledge about the adversity (i.e., the adversity is insufficiently known or understood or is just unknown). 

Sensitivity analyses must inform the determination of loss margins. Other factors for computing loss margins include system complexity, the use of newer technology or older technology in new ways, and the degree of new environments being introduced. An additional factor is the ability to complete comprehensive and effective testing. Limitations on system test coverage and effectiveness for actual, simulated, or emulated adversity necessitate larger margins to account for the remaining uncertainty. The size of the margin may be reduced over time as unknown and underappreciated loss scenarios are uncovered and corrected. The size of the margin may also need to be increased over time as a malicious adversity capability matures in sophistication. 

**References:** [6] [23] [40] [45] [56] [57] [63] 

# **E.19. Mediated Access** 

**Principle:** All access to and operations on system elements are mediated. 

_Note:_ Mediated access is a foundational principle in the design of secure systems. The purpose of mediated access is to: 

- Place limits on access to and use of the system 

- Reduce the possibility of loss escalation 

94 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 

November 2022 

- Reduce the extent to which loss escalates and propagates 

Mediated access is based on the interaction between an entity and a target system element and has two aspects: 

- _Access to the System Element_ : The requesting entity only has authorized access to a target system element. 

- _Use of the System Element:_ The requesting entity is only allowed to perform authorized operations on the target system element. 

Mediated access has two parts: (1) a policy-based access mediation decision and (2) the enforcement of the access mediation decision. The access mediation decision may include conditional constraints that further restrict access (e.g., role, time of day, system state or mode, or duration of operation). If access is not sufficiently mediated, there is no possibility of limiting how system elements (including human and machine elements) interact to ensure that only authorized behaviors and intended outcomes result. 

Mediated access is achieved by an access mediation control mechanism. Seminal computer security work has defined the reference validation mechanism as the generalized form of any mechanism that is an implementation of the reference monitor concept (Section D.4.2). The reference monitor provides the design assurance basis for demonstrating the trustworthiness of a mediated access control mechanism. The essential design criteria (Section D.4.2) provide a refinement to extend the generalized reference monitor concept. Mediated access may enforce the constraints described in the principles of _<u>Distributed Privilege</u>_ , _<u>Least Privilege</u>_ , and _<u>Least Sharing</u>_ . 

As a predominant security function, mediating access may result in performance bottlenecks if not designed and implemented correctly. The use of a least common mechanism is one means to help reduce bottlenecks, an approach referred to as _efficiently mediated access_ [21]. 

**References:** [2] [21] [37] [40] [46] [58] 

# **E.20. Minimal Trusted Elements** 

**Principle:** A system has as few trusted system elements as practicable. 

_Note:_ Minimizing trusted system elements is a cost-benefit trade space consideration employed for the functional allocation of trust within the system. The need for trust is tied to the function provided by a system element, and that need is independent of any distribution of trust across multiple elements in the architecture. The trade decision is, therefore, how best to allocate trust to system elements given the functions they provide and how the elements are best distributed throughout the architecture where distribution is a justified need. Minimizing trusted system elements is one consideration in making that decision. 

Trusted elements are generally costlier to construct due to increased rigor in engineering processes and activities. They also require more analysis to qualify their trustworthiness. Minimizing the number of trusted system elements reduces the cost of analysis (i.e., decreases the size, scope, and complexity of the analysis). When the minimization of trusted system elements considers the principle of _<u>Commensurate Protection</u>_ , the cost-effectiveness of the analysis is also ensured (i.e., cost of the analysis is justified by the extent of trust required). 

Historically, the analysis of interactions between trusted system elements and untrusted system elements is one of the most important aspects of the trust-based verification of system security performance. If these interactions are unnecessarily complex, the security of the system will also be more difficult to ascertain than one whose internal trust relationships are simple and elegantly constructed. In general, fewer trusted components will result in fewer internal trust relationships and a simpler system. 

95 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 November 2022 

**References:** [2] [20] [43] [44] 

# **E.21. Minimize Detectability** 

**Principle:** The design of the system minimizes the detectability of the system as much as practicable. 

_Note:_ A system that is not discoverable, observable, or trackable by an adversarial threat or exposed to such a threat is less prone to a targeted attack. Minimizing detectability drives engineering design decisions to eliminate or reduce exposures such as unnecessary interfaces, access points, footprints, and emanations, thereby reducing susceptibility to adversarial threat actions. Interfaces and access points have the effect of exposing the system to intentional adversity (i.e., attacks) and unintentional adversity (i.e., faults, errors, incidents, accidents). Yet interfaces and access points are necessary to compose system elements to deliver required capabilities, and duplicating interfaces and access points is needed to avoid single points of failure. System design must balance the need for interfaces with the susceptibility that results from the interface being exposed, discovered, and observed. Every interface, whether internal or external, constitutes an exposure that must be considered. 

Minimizing detectability reduces the ability of an adversary to observe and discover information about the system to craft and execute attacks. This includes detecting a system’s location, presence, and movement (e.g., due to emissions, signatures, or footprints). Ways by which a system may be detected include heat emission, electronic magnetic (EM) emissions, sound, vibrations, reflecting radar waves or light, response to stimulus (e.g., a response to an Internet Control Message Protocol [ICMP] echo request or “ping”), and software traces and thrown exceptions. Specific forms or means to minimize detectability include camouflage, stealth, low probability of intercept/low probability of detect (LPI/LPD) waveforms (for radios), and frequency hopping. 

**References:** [53] [59] [60] 

# **E.22. Protective Defaults** 

**Principle:** The default configuration of the system provides maximum protection effectiveness. _Note:_ The configuration of the system includes the parameters for system functions, data, interfaces, and resources that determine how the system behaves and the outcomes it produces. Protective defaults guarantee that the “as shipped” system configuration and parameters prioritize the achievement of loss control objectives over the ability to deliver a required system capability and performance without dependence on human intervention. Protective defaults require conscientious action to establish the system configuration and parameters that deliver the required capability and performance in a manner that provides _<u>Commensurate Protection</u>_ against loss. Protective default configurations for systems include constituent subsystems, components, and mechanisms. The principles of _<u>Protective Failure</u>_ , _<u>Protective Recovery</u>_ <u>, and</u> _<u>Continuous Protection</u>_ parallel this principle to provide the ability to detect and recover from failure. 

**References:** [2] [21] [46] 

# **E.23. Protective Failure** 

**Principle:** A failure of a system element neither results in an unacceptable loss nor invokes another loss scenario. 

96 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 

November 2022 

_Note:_ Protective failure, a generalization of the concepts of fail secure and fail safe, is the aspect of continuous protection that ensures that a protection capability is not interrupted during a failure and that the effect of the failure is constrained. Two aspects of protective failure must be satisfied to achieve the intended effect: 

- _Avoid Single Points of Failure:_ The failure of a single system element should not lead to unacceptable loss. Unacceptable loss should only occur in the case of multiple independent malfunctions – a safety principle known as single failure criterion. The principle of _<u>Defense in Depth</u>_ can help achieve this aspect of protective failure. 

- _Avoid Propagation of New Failure:_ If unmitigated, failures in the system can result in propagating, cascading, or rippling effects on the system. These effects can be addressed if the remaining protections remain effective to prevent the originating failure from causing additional failures. 

Protective failure applies to discrete system elements, aggregates of system elements, and systems abstraction. Protective failure seeks to limit a failure’s effect to the extent practicable and, in doing so, minimize introducing new loss possibilities. Protective failure can limit the extent to which a failure is able to advance loss scenarios associated with the failure, including cascading losses; trigger a different loss scenario; or create a new loss scenario. Efforts to avoid or limit failures may themselves degrade system performance, which is a form of failure. Thus, system designers may need to consider trade spaces between possible adverse effects and system performance. 

**References:** [2] [21] [40] [47] [45] 

# **E.24. Protective Recovery** 

**Principle:** The recovery of a system element does not result in nor lead to unacceptable loss. 

_Note:_ Protective recovery is an aspect of _<u>Continuous Protection</u>_ that ensures that a protection capability is not interrupted during recovery from actual or impending failure. Protective recovery is applied to discrete system elements, aggregates of system elements, and the system. To the extent practicable, any recovery from impending or actual failure to resume normal, degraded, contingency or alternative operation, or the recovery of other asset losses should not (1) advance the loss scenario that is the target of the recovery, (2) trigger other loss scenarios, or (3) create new loss scenarios. The practicable aspect of this principle recognizes that for some recovery efforts to be successful, they may degrade system performance, which is a form of loss. Protective recovery is an aspect of the response strategy for the system. Thus, graduated and ungraduated considerations of _<u>Commensurate Response</u>_ apply to best suit expediency in the need for a protective recovery. 

**References:** [2] [6] [20] [21] 

# **E.25. Reduced Complexity** 

**Principle:** The system design is as simple as practicable. 

_Note:_ Engineered systems are often complex. Some degree of complexity in the system design is inherent, unavoidable, and must be accepted. The objective of this principle is to ensure that the design reflects the extent to which complexity can be reasonably minimized (i.e., avoid unnecessary complexity). 

Complexity can be found in the system structure, interfaces, dependencies, data and control flows, and the interaction of the system with its operational environment. Complexity derives from how the system is decomposed into its individual and aggregates of constituent elements (e.g., subsystems, assemblies), and from how those elements compose through their behaviors and interactions to comprise the functional system. 

97 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 

November 2022 

A more complex design increases uncertainty. Such uncertainty leads to errors and hinders acquiring confidence in the understanding of the design. A complex design is also more prone to erroneous interpretation when conducting the engineering activities of analysis, implementation, and verification throughout the system life cycle [45]. Thus, reduced design complexity contributes to confidence in the technical understanding of the design, enabling more informed trade decisions and decreasing uncertainty in the design and the subsequent realization of the design as a system. 

Complexity also increases the difficulty in identifying and assessing loss scenarios, susceptibilities, and vulnerabilities. Conclusions about the nature and effect of vulnerabilities can be reached with a higher degree of assurance in cases of reduced design complexity in contrast to cases where the design is overly complex. 

The principle of reduced complexity may also be referred to as the principle of simplification or least common mechanism. 

**References:** [2] [40] [45] [46] [47] 

# **E.26. Redundancy** 

**Principle:** The system design delivers the required capability by replication of system functions or elements. 

_Note:_ Redundancy employs multiples of the same system elements, data and control flows, or paths to avoid single points of failure. Redundancy requires a strategy for how multiple system elements are used individually or in combination (e.g., load-balancing, fail-over, concurrently, backup, voting, agreement, consensus). 

Redundant solutions are susceptible to common mode failure (i.e., a single event that results in the same or equivalent elements failing in the same manner). _<u>Diversity</u>_ is a means to address the concerns of common mode failure. 

**References:** [2] [20] [45] [47] 

# **E.27. Self-Reliant Trustworthiness** 

**Principle:** The trustworthiness of a system element is achieved with minimal dependence on other elements. 

_Note:_ In the ideal case, the trustworthiness of a system element occurs when the claim of trustworthiness is not dependent on protection from another system element. If an element is dependent on other elements to satisfy its trustworthiness claims, then that element’s trustworthiness is susceptible to any loss or degradation of the protection capability provided by the other element. The considerations for the extent to which a system element exhibits self-reliant trustworthiness include: 

- The trustworthiness objective for the capability 

- The trustworthiness of the system element in providing the capability 

- The extent to which the capability provided by a system element is dependent on another element 

- The extent to which the trustworthiness associated with a capability is dependent on another system element 

An argument for self-reliant trustworthiness can be applied at the discrete system element level, at the level of an aggregate of elements, at the system level, or at the system of systems level. In all cases, the distinction between the capability provided and the trustworthiness responsibility for that capability must 

98 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 November 2022 

be preserved (e.g., self-reliant trustworthiness cannot be claimed if the protection assertions for trust are allocated to and dependent on some other entity). Similarly, when a system capability is distributed across multiple system elements, self-reliant trustworthiness requires that the trust expectations for the capability be properly allocated across the elements that comprise the distributed capability. 

The judgment that a system element is self-reliantly trustworthy is based on the element’s ability to satisfy a specific set of requirements and associated assumptions. An element that is self-reliantly trustworthy for one set of requirements and assumptions is not necessarily self-reliantly trustworthy for other sets of requirements and assumptions. Any change in the requirement, the satisfaction of the requirement, or in the assumptions associated with the requirement requires reassessment to determine that the element remains self-reliantly trustworthy. 

**References:** [2] 

# **E.28. Structured Decomposition and Composition** 

**Principle:** System complexity is managed through the structured decomposition of the system and the structured composition of the constituent elements to deliver the required capability. 

_Note:_ The structured decomposition of the system and the subsequent composition of the system elements are guided and informed by the concepts of modularity, layering, and partially ordered dependencies. 

Modularity is the system design technique to _divide and conquer_ – that is, sub-divide the system into smaller, well-defined cohesive components and assemblies that are referred to as modules. Modularity serves to isolate functions and data structures into well-defined logical units. Modular decomposition can include the allocation of policies to systems in a network, the allocation of system policies to layers, the separation of system applications into processes with distinct address spaces, and the separation of processes into subjects with distinct privileges based on hardware-supported privilege domains. Modular design may also extend to consider trust, trustworthiness, privilege, and policy. 

Layering is the grouping of modules into a relational structure with well-defined interfaces, function, data, and control flow so that the dependencies graph among layers is linearly or partially ordered such that higher layers are dependent only on lower layers [2]. Partially ordered dependencies among modules (e.g., if module A depends on module B, then module B cannot depend on module A) and system layering contribute significantly to system design simplicity and coherence. While a partial ordering of all functions and processes may not be possible, the inherent problems of circularity can be more easily managed if the circular dependencies are constrained to occur within layers and minimized within each layer. Partially ordered dependencies also facilitate system testing and analysis and enable a strong form of loose coupling (i.e., minimizing interdependencies among modules). 

Modularity and layering are effective in managing the complexity of the composed system. They provide the means to decompose the system into discrete and aggregate elements to better comprehend the system in terms of its structure, flows, relationships, and how the system delivers the required capability. The structured composition of the constituent elements must also adhere to the principle of _<u>Compositional Trustworthiness</u>_ to provide a basis to support claims about how the system is composed based on the application of modularity, layering, and partially ordered dependencies to achieve authorized and intended behaviors and outcomes. 

**References:** [2] [20] [46] [48] [49] 

99 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 November 2022 

# **E.29. Substantiated Trustworthiness** 

**Principle:** System trustworthiness judgments are based on evidence that the criteria for trustworthiness have been satisfied. 

_Note:_ Trustworthiness should not be assumed but rather substantiated through evidence that clearly shows the extent to which an entity is worth being trusted. This helps to ensure that an entity is never trusted beyond the extent to which it is worthy of trust. The approach to substantiated trustworthiness requires _<u>Commensurate Rigor</u>_ with cautious mistrust (i.e., system elements are assumed to be guilty until proven innocent).<sup>84</sup> 

Substantiated trustworthiness is characterized by a design mentality in which all components involved in the design context (i.e., a system element and the elements with which it interacts) are treated with a mutually suspicious mindset [2] [20]. Such mutual suspicion reflects cautious mistrust – the feeling or thought that something undesired, unwanted, or unexpected is possible or can happen. The design for every system element should reflect a lack of trust in interacting elements or itself. This suspicion assumes element non-performance and addresses the following cases: 

- _Interacting element suspicion (mutual suspicion):_ The system element-of-interest design is based on the non-performance of the elements it interacts with and how their non-performance can influence the element-of-interest’s behavior and outcomes. Designing to mutual suspicion is reinforced by applying the principle of _<u>Least Privilege</u>_ to all entities (so that an element executes with only the privileges needed, mitigating harm that may be created) while applying the principle of _<u>Least Persistence</u>_ so that each element is minimally exposed. 

- _Self-suspicion:_ The design for the system element-of-interest must consider its own non-performance independent of any external influence. Designing to self-suspicion may involve self-monitoring and built-in actions, including built-in testing at the initiation of the element. 

This approach forces the system designer to assume that things will not go right and to rigorously seek evidence that demonstrates the effectiveness of the design when things go wrong. Considerations for system element non-performance include: 

- An expectation that elements will behave and produce outcomes that are inconsistent with their design intent 

- The constraints, assumptions, and preconditions that are associated with achieving threshold performance 

- Intentional and unintentional events and conditions, typically referred to by terms like fault, error, failure, and compromise 

**References:** [2] [21] [50] 

# **E.30. Trustworthy System Control** 

**Principle:** The design for system control functions conforms to the properties of the generalized reference monitor. 

_Note:_ The trustworthy system control principle reflects the generalization of the reference monitor concept to provide a uniform design assurance basis for trustworthy system control mechanisms or constraint-enforcing mechanisms that compose to provide system control functions. 

> 84 Adapted from a statement made by John Rushby, SRI International, about the need for software to be treated as “guilty until proven innocent” at a Layered Assurance Workshop (LAW). 

100 

Engineering Trustworthy Secure Systems 

NIST SP 800-160v1r1 November 2022 

The reference monitor concept (Section D.4.2) is a foundational access control concept for secure system design. It is defined as a trustworthy abstract machine that mediates all accesses to objects by subjects [38]. As a concept for an abstract machine, the reference monitor does not address any specific implementation. A reference validation mechanism, which is a combination of hardware and software, realizes the reference monitor concept to provide the access mediation foundation for a secure system [37]. 

The reference monitor concept has several criteria that provide design assurance of its realization as a reference validation mechanism: 

- The reference validation mechanism must be tamper-proof to ensure that its integrity and validity are not destroyed. 

- The reference validation mechanism must always be invoked, and if it cannot be, then the group of programs for which it provides validation services must be considered part of the reference validation mechanism and be subject to the first and third requirements. 

- The reference validation mechanism must be subject to rigorous analysis and tests, the completeness of which can be assured (with the purpose of ascertaining that the reference validation mechanism works correctly in all cases). 

For trustworthy system control, a fourth criterion of non-bypassability is added (Section D.4.2). 

Successful achievement of these criteria will prevent the interference of outside entities on a protection mechanism or controller. Specifically: 

- A protection mechanism or feature should not be circumventable (i.e., the mechanism should be nonbypassable). 

- A protection mechanism or feature should be evaluatable (i.e., sufficiently small and simple enough to be assessed to produce adequate confidence in the protection provided, the constraint or control objective enforced, and the correct implementation of the mechanism [ _<u>Reduced Complexity</u>_ <u>]).</u> 

- A protection mechanism or feature is always invoked, providing continuous protection. 

- A protection mechanism or feature must be tamper-proof (i.e., neither the protection functions nor the data that the functions depend on can be modified without authorization). 

Trustworthy system control also encompasses control, safety, and security concepts to establish a system capability that sufficiently: 

- Enforces constraints to achieve only the authorized and intended system behaviors and outcomes 

- Provides self-protection against targeted attacks on the system 

- Is absent of self-induced emergent, erroneous, unsafe, and non-secure control actions 

Such a system capability underlies the loss control objectives and transforms the approach for design to not rely on having detailed knowledge of the capability, means, and methods of an adversary. This design approach can be employed in attack-dependent or attack-independent manners based on the limits of certainty for what is known with confidence about the adversary. 

Trustworthy system control serves well as the design basis for individual system elements, collections of elements, networks, and systems where intentional and unintentional adversity can prevent the achievement of the loss control objectives. The principle also drives the need for rigor in engineering activities commensurate to the trust placed in the system elements. 

**References:** [21] [35] [37] [38] 

101 

