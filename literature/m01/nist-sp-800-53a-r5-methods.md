---
title: "NIST SP 800-53A Rev. 5, Assessing Security and Privacy Controls in Information Systems and Organizations (chapters 1-3, start of the AC family, and the assessment-method appendices)"
publisher: "NIST"
source_url: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53Ar5.pdf
retrieved: 2026-11-17
sha256: 75665570048b969ad465a4f4f1db425ce505c374951c2c64e462949c6b21be47
converter: pymupdf4llm 2.1
source_format: pdf
pages: "10-60,718-733"
licence: "US government work (NIST)"
module: 1
verified: true
---
NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

## **Executive Summary** 

Security and privacy control assessments are not about checklists, simple pass/fail results, or generating paperwork to pass inspections or audits. Rather, control assessments are the principal vehicle used to verify that selected security and privacy controls are implemented and meeting stated goals and objectives. Special Publication (SP) 800-53A, _Assessing Security and Privacy Controls in Information Systems and Organizations_ , facilitates security control assessments and privacy control assessments conducted within an effective risk management framework. A major design objective for SP 800-53A is to provide an assessment framework and initial starting point for assessment procedures that are flexible enough to meet the needs of different organizations while providing consistency in conducting control assessments. Control assessment results provide organizational officials with: 

- Evidence of the effectiveness of implemented controls, 

- An indication of the quality of the risk management processes, and 

- Information about the security and privacy strengths and weaknesses of systems that are supporting organizational missions and business functions. 

The findings identified by assessors are used to determine the overall effectiveness of security and privacy controls associated with systems and their environments of operation and to provide credible and meaningful inputs to the organization’s risk management process. A wellexecuted assessment helps determine the validity of the controls contained in the organization’s security and privacy plans and subsequently employed in organizational systems and environments of operation.  Control assessments facilitate a cost-effective approach to managing risk by identifying weaknesses or deficiencies in systems, thus enabling the organization to determine appropriate risk responses in a disciplined manner that is consistent with organizational mission and business needs. 

SP 800-53A is a companion guideline to [SP 800-53] _Security and Privacy Controls for Systems and Organizations_ . Each publication provides guidance for implementing specific steps in the Risk Management Framework (RMF).<sup>1</sup> SP 800-53 and [SP 800-53B] address the Select step of the RMF and provide guidance on security and privacy control selection (i.e., determining the controls needed to manage risks to organizational operations and assets, individuals, other organizations, and the Nation). SP 800-53A addresses the Assess and Monitor steps of the RMF and provides guidance on the security and privacy control assessment processes. SP 800-53A also includes guidance on how to build effective assessment plans and how to analyze and manage assessment results. 

SP 800-53A provides a process that allows organizations to tailor the assessment procedures outlined in the guidance. Tailoring involves customizing the assessment procedures to match the characteristics of the system and its environment of operation more closely. The tailoring process described in this guidance gives organizations the flexibility needed to avoid assessment approaches that are unnecessarily complex or costly while simultaneously meeting the assessment requirements and risk management principles established in the RMF. Tailoring decisions are left to the discretion of the organization to maximize flexibility in developing assessment plans – applying the results of risk assessments to determine the extent, rigor, and level of intensity of the assessments needed to provide sufficient assurance about the security and privacy posture of the system. 

> 1 [SP 800-37], _Risk Management Framework for Information Systems and Organizations: A System Life Cycle Approach for Security and Privacy,_ provides guidance on applying the RMF to systems and organizations. 

viii 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

## **Table of Contents** 

|**CHAPTER ONE **INTRODUCTION ............................................................................................................... 1|
|---|
|1.1 PURPOSE AND APPLICABILITY.......................................................................................................... 1|
|1.2 TARGET AUDIENCE............................................................................................................................ 4|
|1.3 RELATED PUBLICATIONS AND ASSESSMENT PROCESSES............................................................... 4|
|1.4 ORGANIZATION OF THIS PUBLICATION........................................................................................... 5|
|**CHAPTER TWO** THE FUNDAMENTALS ..................................................................................................... 6|
|2.1 ASSESSMENTS WITHIN THE SYSTEM DEVELOPMENT LIFE CYCLE.................................................. 6|
|2.2 CONTROL STRUCTURE AND ORGANIZATION.................................................................................. 7|
|2.3 BUILDING AN EFFECTIVE ASSURANCE CASE.................................................................................... 8|
|2.4 ASSESSMENT PROCEDURES: ASSESSMENT OBJECTS, METHODS AND OBJECTIVES................... 11|
|**CHAPTER THREE** THE PROCESS ............................................................................................................. 19|
|3.1 PREPARE FOR SECURITY AND PRIVACY CONTROL ASSESSMENTS............................................... 19|
|3.2 DEVELOP SECURITY AND PRIVACY ASSESSMENT PLANS.............................................................. 23|
|3.3 CONDUCT SECURITY AND PRIVACY CONTROL ASSESSMENTS..................................................... 30|
|3.4 ANALYZE ASSESSMENT REPORT RESULTS..................................................................................... 32|
|3.5 ASSESS SECURITY AND PRIVACY CAPABILITIES.............................................................................. 34|
|**CHAPTER FOUR** SECURITY AND PRIVACY ASSESSMENT PROCEDURES ................................................. 37|
|4.1 ACCESS CONTROL............................................................................................................................ 40|
|4.2 AWARENESS AND TRAINING........................................................................................................ 118|
|4.3 AUDIT AND ACCOUNTABILITY...................................................................................................... 128|
|4.4 ASSESSMENT, AUTHORIZATION, AND MONITORING................................................................. 160|
|4.5 CONFIGURATION MANAGEMENT................................................................................................ 177|
|4.6 CONTINGENCY PLANNING............................................................................................................ 215|
|4.7 IDENTIFICATION AND AUTHENTICATION.................................................................................... 243|
|4.8 INCIDENT RESPONSE ............................................................................................................... 275|
|4.9 MAINTENANCE ........................................................................................................................ 298|
|4.10 MEDIA PROTECTION .............................................................................................................. 316|
|4.11 PHYSICAL AND ENVIRONMENTAL PROTECTION....................................................................... 330|
|4.12 PLANNING ............................................................................................................................. 361|
|4.13 PROGRAM MANAGEMENT .................................................................................................... 372|
|4.14 PERSONNEL SECURITY ........................................................................................................... 401|
|4.15 PERSONALLY IDENTIFIABLE INFORMATION PROCESSING AND TRANSPARENCY................... 412|
|4.16 RISK ASSESSMENT ................................................................................................................. 426|
|4.17 SYSTEM AND SERVICES ACQUISITION....................................................................................... 441|
|4.18 SYSTEM AND COMMUNICATIONS PROTECTION...................................................................... 522|
|4.19 SYSTEM AND INFORMATION INTEGRITY................................................................................... 599|
|4.20 SUPPLY CHAIN RISK MANAGEMENT.......................................................................................... 665|
|**REFERENCES**........................................................................................................................................ 684|
|**APPENDIX A** GLOSSARY ....................................................................................................................... 689|
|**APPENDIX B** ACRONYMS ..................................................................................................................... 705|
|**APPENDIX C** ASSESSMENT METHOD DESCRIPTIONS........................................................................... 707|
|**APPENDIX D** PENETRATION TESTING .................................................................................................. 715|
|**APPENDIX E** ASSESSMENT REPORTS ................................................................................................... 718|
|**APPENDIX F** ONGOING ASSESSMENT AND AUTOMATION ................................................................. 721|



ix 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

### **CHAPTER ONE** 

# **INTRODUCTION** 

THE NEED TO ASSESS SECURITY AND PRIVACY CONTROL EFFECTIVENESS 

Today’s systems<sup>2</sup> are complex assemblages of technology (i.e., hardware, software, and firmware), processes, and people working together to provide organizations with the capabilities to process, store, and transmit information in a timely manner in support of various mission and business functions. The degree to which organizations have come to depend upon systems to conduct routine, important, and critical mission and business functions means that the protection of the underlying systems and environments of operation is paramount to the success of the organization. The selection of appropriate security and privacy controls for a system is an important task that can have significant implications on the operations and assets of an organization as well as the welfare of individuals. Security controls are the safeguards or countermeasures prescribed for a system or an organization to protect the confidentiality, integrity, and availability of its system and information and to manage information security risk. Privacy controls are the administrative, technical, and physical safeguards employed within a system or an organization to manage privacy risks and ensure compliance with applicable privacy requirements.<sup>3</sup> 

Once employed within a system, security and privacy controls are assessed to determine their overall effectiveness (i.e., the extent to which the controls are implemented correctly, operating as intended, and producing the desired outcome with respect to meeting the security and privacy requirements for the system and the organization). Understanding the overall effectiveness of implemented security and privacy controls is essential in determining the risk to the organization’s operations and assets, individuals, other organizations, and the Nation resulting from the use of the system. 

## **1.1 PURPOSE AND APPLICABILITY** 

The purpose of this publication is to provide guidelines for building effective security and privacy assessment plans, as well as a comprehensive set of procedures for assessing the effectiveness of security and privacy controls employed in systems and organizations. The guidelines apply to the security and privacy controls defined in [SP 800-53] (as amended), _Security and Privacy Controls for Information Systems and Organizations_ . The guidelines have been developed to help achieve more secure systems by: 

- Enabling more consistent, efficient, comparable, and repeatable assessments of security and privacy controls with reproducible results; 

- Promoting a better understanding of the risks to organizational operations, organizational assets, individuals, other organizations, and the Nation resulting from the operation and use of systems; 

- Facilitating more cost-effective assessments of security and privacy controls; and 

> 2 A system is a discrete set of information resources organized expressly for the collection, processing, maintenance, use, sharing, dissemination, or disposition of information. 

> 3 OMB Circular A-130 [OMB A-130] defines security and privacy controls. 

CHAPTER ONE 

PAGE 1 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

- Creating more complete, reliable, and trustworthy information for organizational officials to support risk management decisions, reciprocity of assessment results, information sharing, and compliance with federal laws, Executive Orders, directives, regulations, and policies. 

This publication satisfies the requirements of Office of Management and Budget (OMB) Circular A-130 [OMB A-130] and the provisions of the Federal Information Security Modernization Act [FISMA]. The security and privacy guidelines in this publication are applicable to federal systems other than those systems designated as national security systems, as defined in 44 U.S.C., Section 3542. The guidelines have been broadly developed from a technical perspective to complement similar guidelines for national security systems and may be used for such systems with the approval of appropriate federal officials exercising policy authority over such systems.<sup>4</sup> 

Organizations use this publication in conjunction with approved information security program plans, privacy program plans, system security plans, and privacy plans in developing assessment plans for producing and compiling the information necessary to determine the effectiveness of the security and privacy controls employed in the system and organization. The guidance in this publication has been developed with the intention of enabling organizations to tailor the basic assessment procedures provided. The assessment procedures are used as a starting point for and as input to the assessment plan. In developing effective security and privacy assessment plans, organizations take into consideration existing information about the controls to be assessed (e.g., results from assessments of risk; platformspecific dependencies in the hardware, software, or firmware; and any assessment procedures needed as a result of organization-specific controls not included in [SP 800-53]).<sup>5</sup> 

The selection of appropriate assessment procedures and the rigor, intensity, and scope of the assessment depend on the following factors: 

- The security categorization of the system;<sup>6</sup> 

- The privacy risk assessment for the system; 

> 4 In accordance with the provisions of [FISMA] and OMB policy, whenever the interconnection of federal systems to systems operated by state/local/tribal governments, contractors, or grantees involves the processing, storage, or transmission of federal information, the information security standards and guidelines described in this publication apply. Specific information security requirements and the terms and conditions of the system interconnections are expressed in Memoranda of Understanding (MOU) and Interconnection Security Agreements (ISAs) established by participating organizations. For additional guidance on managing the security of information exchanges, see NIST [SP <u>800-47], Revision 1,</u> _Managing the Security of Information Exchanges_ . 

> 5 For example, detailed test scripts may need to be developed for the specific operating system, network component, middleware, or application employed within the system to adequately assess certain characteristics of a particular security or privacy control. Such test scripts are at a lower level of detail than provided by the assessment procedures contained in this guidance and are, therefore, beyond the scope of this publication. 

6 For national security systems, security categorization is accomplished in accordance with CNSS Instruction 1253 <u>[CNSSI 1253]. For other than national security systems, security categorization is accomplished in accordance with</u> Federal Information Processing Standard (FIPS) 199 [FIPS 199], NIST [SP 800-37], NIST [SP 800-60 Vol 1], NIST [SP 800- <u>60 Vol 2], and the Controlled Unclassified Information (CUI) Registry [NARA CUI] as managed by the National Archives</u> and Records Administration. 

CHAPTER ONE 

PAGE 2 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

- The security and privacy controls from [SP 800-53] as identified in the approved information security program plans, privacy program plans, security plans, and privacy plans;<sup>7</sup> and 

- The assurance requirements that the organization intends to meet in determining the overall effectiveness of the security and privacy controls. 

The assessment process is an information-gathering activity of the as-implemented state of the system or common controls, not a security- or privacy-producing activity. Organizations determine the most cost-effective implementation of the assessment process by applying the results of risk assessments, considering the maturity and quality level of the organization’s risk management processes, and taking advantage of the flexibility in the concepts described in this publication. The use of SP 800-53A as a starting point in the process of defining procedures for assessing the security and privacy controls in systems and organizations promotes the consistent application of security and privacy controls and offers the needed flexibility to customize the assessment based on organizational policies and requirements, known threat and vulnerability information, operational considerations, system and platform dependencies, and tolerance for risk.<sup>8</sup> The information produced during control assessments can be used by an organization to: 

- Identify potential problems or shortfalls in the organization’s implementation of the Risk Management Framework, 

- Identify security- and privacy-related weaknesses and deficiencies in the system and in the environment in which the system operates, 

- Prioritize risk response decisions and associated risk response activities,<sup>9</sup> 

- Confirm that identified security- and privacy-related weaknesses and deficiencies in the system and in the environment of operation have been addressed, 

- Support monitoring activities and information security and privacy situational awareness, 

- Facilitate all types of system authorization decisions,<sup>10</sup> and 

- Inform budgetary decisions and the capital investment process. 

Organizations are not expected to employ all of the assessment methods and assessment objects contained within the assessment procedures identified in this publication for the associated security and privacy controls deployed within or available for inheritance by organizational systems. Rather, organizations have the inherent flexibility to determine the level of effort needed and the assurance required for a particular assessment (e.g., which assessment methods and assessment objects are most useful in obtaining the desired results). Determination of the level of effort and required assurance is made based on what is 

> 7 The security and privacy controls for the system and organization are documented in the system security plans and privacy plans after the initial selection and tailoring of the controls, as described in [SP 800-53] and [CNSSI 1253]. The Program Management controls are documented in information security program plans and privacy program plans, as described in SP 800-53. 

> 8 In this publication, the term risk is used to mean risk to organizational operations (i.e., mission, functions, image, and reputation), organizational assets, individuals, other organizations, and the Nation. 

> 9 <u>[SP 800-39] provides additional information about the types of risk response.</u> 

- 10 Types of authorization decisions are described in [SP 800-37], Appendix F. 

CHAPTER ONE 

PAGE 3 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

necessary to accomplish the assessment objectives in the most cost-effective manner and with sufficient confidence to support the subsequent determination of the resulting mission or business risk (i.e., risk management). Organizations balance the resources expended on the deployment of security and privacy controls (i.e., safeguards and countermeasures implemented for security and privacy protection) with the resources expended to determine overall control effectiveness, both initially and on an ongoing basis through continuous monitoring programs. 

## **1.2 TARGET AUDIENCE** 

This publication is intended to serve a diverse group of system and information security and privacy professionals, including: 

- Individuals with system development responsibilities (e.g., program managers, system designers and developers, systems integrators, information security engineers and privacy engineers); 

- Individuals with information security and privacy assessment and monitoring responsibilities (e.g., Inspectors General, system evaluators, assessors, independent verifiers/validators, auditors, analysts, system owners, common control providers); 

- Individuals with system, security, privacy, risk management, and oversight responsibilities (e.g., authorizing officials, chief information officers, senior information security officers,<sup>11</sup> senior agency officials for privacy/chief privacy officers, system managers, information security and privacy managers); and 

- Individuals with information security and privacy implementation and operational responsibilities (e.g., system owners, common control providers, information owners/stewards, mission and business owners, system administrators, system security officers, system privacy officers). 

## **1.3 RELATED PUBLICATIONS AND ASSESSMENT PROCESSES** 

SP 800-53A is designed to support [SP 800-37], _Risk Management Framework for Information Systems and Organizations: A System Life Cycle Approach for Security and Privacy_ . In particular, the assessment procedures contained in this publication and the guidelines provided for developing security and privacy assessment plans for organizational systems directly support the assessment and monitoring activities that are integral to the risk management process. The integral activities include providing near real-time security- and privacy-related information to organizational officials regarding the ongoing security and privacy state of their systems and organizations. 

Organizations are encouraged to take advantage of the control assessment results and associated assessment documentation, artifacts, and evidence available for system components from previous assessments, including independent third-party testing, evaluation, and validation.<sup>12</sup> Product testing, evaluation, and validation may be conducted on 

> 11 At the federal _agency_ level, the role is known as the Senior Agency Information Security Officer. Organizations may also refer to the role as the _Senior Information Security Officer_ or the _Chief Information Security Officer_ . 

> 12 Assessment results can be obtained from many activities that occur routinely during the system development life cycle. For example, assessment results are produced during the testing and evaluation of new system components 

CHAPTER ONE 

PAGE 4 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

cryptographic modules and general-purpose information technology products, such as operating systems, database systems, firewalls, intrusion detection systems, web browsers, web applications, smart cards, biometrics devices, personal identity verification devices, network devices, and hardware platforms using national and international standards. If a system component product is identified as providing support for the implementation of a particular control in [SP 800-53], then evidence produced during the product testing, evaluation, and validation processes (e.g., security or privacy specifications, analyses and test results, validation reports, and validation certificates)<sup>13</sup> is used to the extent that it is applicable. The applicable product testing evidence can be combined with the assessmentrelated evidence obtained from the application of the assessment procedures in this publication to cost-effectively produce the information necessary to determine whether the security and privacy controls are effective in their application. 

## **1.4 ORGANIZATION OF THIS PUBLICATION** 

The remainder of this publication is organized as follows: 

- **<u>Chapter Two</u>** describes the fundamental concepts associated with security and privacy control assessments, including the integration of assessments into the system development life cycle, the importance of an organization-wide strategy for conducting security and privacy control assessments, the development of effective assurance cases to help increase grounds for confidence in the effectiveness of the security and privacy controls being assessed, and the format and content of assessment procedures. 

- **<u>Chapter Three</u>** describes the process of assessing the security and privacy controls in organizational systems and their environments of operation, including the activities carried out by organizations and assessors to prepare for security and privacy control assessments; the development of security assessment plans; the conduct of security and privacy control assessments; the analysis, documentation, and reporting of assessment results; and the post-assessment report analysis and follow-on activities carried out by organizations. 

- **<u>Chapter Four</u>** provides a catalog of security and privacy assessment procedures that can be used to develop plans for assessing security controls. 

- **Supporting appendices** provide detailed assessment-related information, including general references, definitions and terms, acronyms, a description of assessment methods, penetration testing guidelines, content of security and privacy assessment reports, and automation support for ongoing assessments. 

during system upgrades or system integration activities. Organizations can take advantage of previous assessment results whenever possible, to reduce the overall cost of assessments and to make the assessment process more efficient. 

> 13 Organizations review the available information from component information technology products to determine what security and privacy controls are implemented by the product, if those controls meet the intended control requirements of the system under assessment, if the configuration of the product and the environment in which the product operates are consistent with the environmental and product configuration stated by the vendor and/or developer, and if the assurance requirements stated in the developer/vendor specification satisfy the assurance requirements for assessing those controls. Meeting the above criteria provides a sound rationale that the product is suitable and meets the intended security and privacy control requirements of the system under assessment. 

CHAPTER ONE 

PAGE 5 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

### **CHAPTER TWO** 

# **THE FUNDAMENTALS** 

BASIC CONCEPTS ASSOCIATED WITH SECURITY AND PRIVACY CONTROL ASSESSMENTS 

This chapter describes the basic concepts associated with assessing the security and privacy controls in organizational systems and the environments in which those systems operate, including the integration of assessments into the system development life cycle, the importance of an organization-wide strategy for conducting assessments, the development of effective assurance cases to help increase grounds for confidence in the effectiveness of security and privacy controls, and the format and content of assessment procedures. A fundamental design objective for SP 800-53A is to provide a flexible assessment framework and a starting point for assessment procedures to be used by different organizations and systems while providing a repeatable approach to facilitate consistency in conducting control assessments. 

## **2.1 ASSESSMENTS WITHIN THE SYSTEM DEVELOPMENT LIFE CYCLE** 

Security and privacy assessments can be carried out throughout system development life cycle phases<sup>14</sup> to increase grounds for confidence that the security and privacy controls employed within or inherited by a system are effective in their application. The guidance in this publication provides a comprehensive set of assessment procedures to support security and privacy assessment activities throughout the system development life cycle. For example, security and privacy assessments are routinely conducted during the development/acquisition and implementation phases of the life cycle. Conducting assessments during the development/acquisition and implementation phases helps ensure that the required controls for the system are designed and developed consistent with risk management goals, correctly implemented, and consistent with the established organizational information security and privacy architecture before the system enters the operations and maintenance phase. Security and privacy assessments conducted in pre-operational system development life cycle phases include design and code reviews, application scanning, regression testing, and ensuring that applicable privacy laws and policies are adhered to and that privacy protections are embedded in the design of the system. 

Security- and privacy-related weaknesses and deficiencies identified early in the system development life cycle can be resolved more quickly and cost-effectively than deficiencies identified in subsequent phases of the life cycle. Early identification of security- and privacyrelated weaknesses and deficiencies in the selected security and privacy controls facilitates determination and implementation of appropriate risk responses and allows for effectiveness of control implementations to be validated during system design and testing. 

Security and privacy assessments are also conducted during the operations and maintenance phase of the life cycle to ensure that the controls continue to be effective in the operational environment and protect against constantly evolving risks. Organizations assess all security and privacy controls employed within and inherited by the system during the initial system 

> 14 There are typically five phases in a generic system development life cycle: (i) initiation, (ii) development/acquisition, (iii) implementation, (iv) operations and maintenance, and (v) disposition (disposal). 

CHAPTER TWO 

PAGE 6 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

authorization. Following the initial authorization, the organization assesses all implemented security and privacy controls on an ongoing basis in accordance with its Information Security Continuous Monitoring (ISCM) strategy and privacy continuous monitoring strategy.<sup>15</sup> The ongoing assessment and monitoring of controls use the assessment procedures defined in this publication. The frequency of such assessments and monitoring is determined by the organization, system owner, and/or common control provider and is approved by the authorizing official. Finally, at the end of the life cycle, security and privacy assessments are conducted to ensure that important organizational information, including personally identifiable information, are purged from the system prior to disposal and organizational retention schedules are adhered to. 

## **2.2 CONTROL STRUCTURE AND ORGANIZATION** 

Organizations are encouraged to develop a broad-based, organization-wide strategy for conducting security and privacy assessments to facilitate more cost-effective and consistent assessments across the inventory of systems. Maximizing the number of common controls employed within an organization significantly reduces the costs of development, implementation, and assessment of security and privacy controls; allows organizations to centralize and automate control assessments and amortize the cost of those assessments across all systems in the organization; and increases the consistency of security and privacy control implementations. 

##### **THE BENEFIT OF IMPLEMENTATION AND ASSESSMENT OF COMMON CONTROLS AND SHARING** **<mark>ASSESSMENT RESULTS</mark>** 

<mark>An organization-wide approach to identifying common controls early in the application of the RMF facilitates a more global strategy for assessing those common controls and sharing assessment results with system owners and authorizing officials. The sharing of assessment results among key organizational officials across system boundaries has many important benefits, including:</mark> 

- <mark>Providing the capability to review assessment results for all systems and to make mission and business-related decisions on risk mitigation activities according to organizational priorities, the security categorization of the systems, and risk assessment results;</mark> 

- <mark>Providing a more global view of systemic weaknesses and deficiencies occurring in systems across the organization and an opportunity to develop organization-wide solutions to information security and privacy problems; and</mark> 

- <mark>Increasing the organization’s knowledge base regarding threats, vulnerabilities, privacy risks, and</mark> strategies for more cost-effective solutions to common information security and privacy problems. 

Organizations can also promote a more focused and cost-effective assessment process by developing specific assessment procedures that are tailored to their specific environments of operation and requirements (instead of relegating assessment procedure development tasks to individual control assessors or assessment teams) and by providing organization-wide tools, 

> 15 <u>[SP 800-137] provides guidance on the continuous monitoring of security controls as part of an ISCM Program.</u> Continuous monitoring can be applied effectively to privacy controls consistent with the concepts, techniques, and principles described in SP 800-137. Senior Agency Officials for Privacy (SAOPs)/Chief Privacy Officers (CPOs) provide guidance on the ongoing monitoring of privacy controls. NIST Interagency Report 8011 [NISTIR 8011], _Automation Support for Security Control Assessments_ , provides guidance on methods to automate the assessment process. 

CHAPTER TWO 

PAGE 7 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

templates, and techniques to support more consistent assessments throughout the organization.<sup>16</sup> 

The roles responsible for conducting control assessments may include system owners, common control providers, system security and privacy officers, independent assessors, auditors, and Inspectors General with oversight by the authorizing official(s).<sup>17</sup> There is also significant involvement in the assessment process of other parties within the organization who have a vested interest in the outcome of assessments. Other interested parties include mission and business owners and information owners/stewards (when those roles are filled by someone other than the system owner). It is imperative that system owners and common control providers identify and coordinate with other parties in the organization that have an interest in control assessments to help ensure that the organization’s core missions and business functions are adequately addressed in the assessment of security and privacy controls. 

##### **CAUTIONARY NOTE** 

<mark>Organizations carefully consider the potential impacts of employing the assessment procedures defined in this publication when assessing the security and privacy controls in</mark> _<mark>operational</mark>_ <mark>systems. Certain assessment procedures – particularly those that directly impact the operation or function of the hardware, software, or firmware components of a system – may inadvertently affect the routine processing, transmission, or storage of information that supports organizational missions or business functions. For example, a critical system component may be taken offline for assessment purposes, or a component may suffer a fault or failure during the assessment process. Organizations take the necessary precautions to ensure that organizational missions and business functions continue to be supported by systems and that any potential impacts to operational effectiveness resulting from assessment activities</mark> are considered in advance. 

## **2.3 BUILDING AN EFFECTIVE ASSURANCE CASE** 

Building an effective assurance case<sup>18</sup> for security and privacy control effectiveness is a process that involves compiling evidence from a variety of activities conducted during the system development life cycle that the controls employed in the system are implemented correctly, operating as intended, and producing the desired outcome with respect to meeting the security and privacy requirements of the system and the organization and presenting the evidence in a manner that decision makers are able to use effectively in making risk-based decisions about the operation or use of the system (i.e., to manage risk). The evidence described above comes from 

> 16 Organizations may also provide security and privacy control assessment plans, including tailored assessment procedures, to external service providers who are operating systems on behalf of those organizations. In addition, tailored control and privacy assessment plans can recommend supporting templates, tools, and techniques and also be further tailored to the contract with the service provider, helping to make assessments more consistent and to maximize the reuse of assessment-related artifacts. The reuse of artifacts can improve security and privacy through uniformity and reduce/eliminate contracting ambiguity, resulting in reduced costs and risk to the organization. 

> 17 In accordance with [OMB A-130], an independent evaluation of privacy program and practices is not required. However, an organization may choose to employ independent privacy assessments at the organization’s discretion. 

> 18 An assurance case is a body of evidence organized into an argument demonstrating that some claim about a system holds (i.e., is assured). An assurance case is needed when it is important to show that a system exhibits some complex property, such as safety, security, privacy, or reliability. 

CHAPTER TWO 

PAGE 8 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

the implementation of the security and privacy controls in the system and inherited by the system (i.e., common controls) and from the assessments of that implementation. Ideally, the assessor builds on previously developed materials that started with the specification of the organization’s information security and privacy needs and was further developed during the design, development, and implementation of the system. The materials developed while implementing security and privacy throughout the life cycle of the system provide the initial evidence for an assurance case. 

During the assessment process, assessors obtain the evidence needed to allow the appropriate organizational officials to make objective determinations about the effectiveness of the security and privacy controls and the overall security and privacy state of the system. The assessment evidence needed to make such determinations can be obtained from a variety of sources, including information technology product and system assessments and – in the case of privacy assessments – documentation such as privacy impact assessments and Privacy Act system of record notices. Product assessments (also known as product testing, evaluation, and validation) are typically conducted by independent, third-party testing organizations. Assessments examine the security and privacy functions of products and established configuration settings. Assessments can be conducted to demonstrate compliance with industry, national, or international information security and privacy standards and developer/vendor claims. Since many information technology products are assessed by commercial testing organizations and then subsequently deployed in millions of systems, product assessments can be carried out at a greater level of depth and provide deeper insights into the security and privacy capabilities of the particular products. 

System and common control assessments are typically conducted by system developers, system integrators, system owners, common control providers, assessors, auditors, Inspectors General, and organizational information security and privacy personnel. The assessors or assessment teams bring together available information about the system or common control, such as the results from individual component product assessments, information in the system security and privacy plans, other system/common control documentation, or previous assessment results, and conduct additional system-level or common control assessments using a variety of methods and techniques. System and common control assessments are used to compile and evaluate the evidence needed by organizational officials to determine how effectively the security and privacy controls employed in systems mitigate risks to organizational operations and assets, individuals, other organizations, and the Nation. The results of assessments conducted using system-specific and organization-specific assessment procedures derived from the guidelines in this publication contribute to compiling the necessary evidence to determine security and privacy control effectiveness in accordance with the assurance requirements documented in security and privacy plans. 

#### **_Assurance Evidence from Developmental and Operational Activities_** 

Organizations obtain security and privacy assurance by the actions taken by system developers, implementers, operators, maintainers, and assessors. Actions by individuals and/or groups during the development/operation of systems produce security and privacy evidence that contributes to the assurance, or measures of confidence, in the security and privacy functionality needed to deliver the security and privacy capability. The depth and coverage of these actions (as described in Appendix C) also contribute to the efficacy of the evidence and 

CHAPTER TWO 

PAGE 9 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

measures of confidence. The evidence produced by developers, implementers, operators, assessors, and maintainers during the system development life cycle (e.g., design/development artifacts and assessment results) contributes to the understanding of the effectiveness of security and privacy controls implemented by organizations. 

The strength of the security and privacy functionality<sup>19</sup> plays an important part in achieving the desired capabilities and subsequently satisfying the security and privacy requirements of organizations. System developers can increase the strength of security and privacy functionality by employing well-defined security and privacy policies and procedures, structured and rigorous design and development techniques, and sound system, security, and privacy engineering techniques as part of the system development process. The artifacts generated by development activities (e.g., functional specifications, system design documentation, and the results of testing and code analysis) can provide important evidence that systems and their components are more reliable and trustworthy. Security and privacy evidence can also be generated from testing conducted by independent, third-party assessment organizations and other assessment activities conducted by government and private sector organizations.<sup>20</sup> 

In addition to the evidence produced in the development environment, organizations can produce evidence from the operational environment that contributes to the assurance of functionality and security and privacy capabilities. Operational evidence includes records of remediation actions, the results of security incident reporting (including breaches involving personally identifiable information), and the results of organizational continuous monitoring activities. Such evidence helps determine the effectiveness of deployed security and privacy controls, changes to systems and environments of operation, and compliance with legislation, policies, directives, regulations, and standards. Security and privacy evidence – whether obtained from development or operational activities – helps organizations determine the extent to which their systems are implemented correctly, operating as intended, and producing the desired outcome with respect to meeting stated security and privacy requirements, thus providing greater assurance in the system’s security and privacy capabilities. 

The depth and coverage of security and privacy evidence can affect the level of assurance in the functionality implemented. Depth and coverage are attributes associated with assessment methods and the generation of security and privacy evidence.<sup>21</sup> Assessment methods can be applied to support developmental and operational assurance. For developmental assurance, depth is associated with the rigor, level of detail, and formality of the artifacts produced during system design and development. The level of detail available in development artifacts can affect the type of testing, evaluation, and analysis conducted during the system development life cycle (e.g., basic testing, comprehensive testing, and focused testing, static/dynamic analysis). For operational assurance, the depth attribute addresses the rigor and level of detail for the 

> 19 The security or privacy _strength_ of a system component (i.e., hardware, software, or firmware) is determined by the degree to which the security or privacy functionality implemented within that component is correct, complete, resistant to direct attacks (strength of mechanism), and resistant to bypass or tampering. 

> 20 For example, third-party assessment organizations assess cloud services and service providers in support of the Federal Risk and Authorization Management Program [FedRAMP]. Common Criteria Testing Laboratories test and evaluate information technology products using [ISO 15408]. Cryptographic/Security Testing Laboratories test cryptographic modules using the [FIPS 140-3] standard. 

> 21 For additional information about depth and coverage, see <u>Section 2.4 and Appendix C.</u> 

CHAPTER TWO 

PAGE 10 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

assessment. In contrast, the coverage attribute is associated with the assessment methods employed during development and operations, addressing the scope and breadth of assessment objects included in the assessments (e.g., number and types of tests conducted on source code). 

## **2.4 ASSESSMENT PROCEDURES: ASSESSMENT OBJECTS, METHODS AND OBJECTIVES** 

An assessment **_procedure_** consists of a set of assessment _objectives_ , each with an associated set of potential assessment _methods_ and assessment _objects_ . An assessment objective includes one or more _determination statements_ related to the [SP 800-53] control under review. The determination statements are linked to the content of the control (i.e., the security and privacy control functionality) to ensure the traceability of assessment results back to the fundamental control requirements. The application of an assessment procedure to a control produces assessment findings.<sup>22</sup> Assessment findings reflect or are subsequently used to help determine the overall effectiveness of the control and help the authorizing official make an informed, riskbased decision on whether to place the system into operation or continue its operation. 

##### **_2.4.1   ASSESSMENT OBJECTS_** 

Assessment **_objects_** identify the specific items being assessed as part of a given control and include _specifications_ , _mechanisms_ , _activities_ , and _individuals_ . Specifications are the documentbased artifacts (e.g., policies, procedures, plans, system security and privacy requirements, functional specifications, architectural designs) associated with a system or common control. Mechanisms are the specific hardware, software, or firmware safeguards and countermeasures employed within a system or common control.<sup>23</sup> Activities are the specific protection-related actions supporting a system or common control that involve people (e.g., conducting system backup operations, monitoring network traffic, exercising a contingency plan). Individuals or groups of individuals are people applying the specifications, mechanisms, or activities described above. 

##### **_2.4.2   ASSESSMENT METHODS_** 

Assessment **_methods_** define the nature of the assessor actions and include examine, interview, and test. 

- The _examine_ method is the process of reviewing, inspecting, observing, studying, or analyzing one or more assessment objects (i.e., specifications, mechanisms, or activities) to facilitate assessor understanding, achieve clarification, or obtain evidence. 

- The _interview_ method is the process of holding discussions with individuals or groups of individuals within an organization to facilitate assessor understanding, achieve clarification, or obtain evidence. 

- The _test_ method is the process of exercising one or more assessment objects (i.e., activities or mechanisms) under specified conditions to compare the actual state of the object to the desired state or expected behavior of the object. 

> 22 For more information about control assessment findings, see <u>Section 3.3.</u> 

> 23 Mechanisms also include physical protection devices associated with a system or common control (e.g., locks, keypads, security cameras, fire protection devices, fireproof safes, etc.). 

CHAPTER TWO 

PAGE 11 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

In all three assessment methods, the results are used to make specific determinations called for in the determination statements and thereby achieve the objectives for the assessment procedure. A complete description of assessment methods and assessment objects is provided in <u>Appendix C.</u> 

Assessment methods have a set of associated attributes – _depth_ and _coverage_ – which help define the level of effort for the assessment. The attributes are hierarchical in nature, providing the means to define the rigor and scope of the assessment for the increased assurances that may be needed for some systems. 

- The depth attribute addresses the rigor and level of detail in the examination, interview, and testing processes. Values for the depth attribute include _basic_ , _focused_ , and _comprehensive_ . 

- • The coverage attribute addresses the scope or breadth of the examination, interview, and testing processes, including the number and types of specifications, mechanisms, and activities to be examined or tested and individuals to be interviewed. Similar to the depth attribute, values for the coverage attribute include _basic_ , _focused_ , and _comprehensive_ . 

The appropriate depth and coverage attribute values for a particular assessment method are based on the assurance requirements specified by the organization and are an important component of protecting information commensurate with risk (i.e., risk management). As assurance requirements increase with regard to the development, implementation, and operation of controls within or inherited by the system, the rigor and scope of the assessment activities (as reflected in the selection of assessment methods and objects and the assignment of depth and coverage attribute values) tend to increase as well.<sup>24</sup> <u>Appendix C provides a</u> detailed description of assessment method attributes and attribute values. 

##### **_2.4.3   ASSESSMENT OBJECTIVES_** 

The assessment objectives are numbered sequentially, first in accordance with the numbering scheme in [SP 800-53] and, subsequently, where necessary to further granularize the security or privacy control requirements to facilitate assessment. Square bracketed sequential numbers, as opposed to parentheses, are used to indicate that the control from SP 800-53 has been further granularized (e.g., AC-17a.[01], AC-17a.[02], AC-17a.[03]). 

> 24 The level of effort for the assessment, including the depth and coverage, is primarily determined by the privacy risk assessment or security categorization of the system or common control being assessed. 

CHAPTER TWO 

PAGE 12 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

Figure 1 illustrates an example assessment procedure developed to assess the effectiveness of control AC-17. The assessment objective for AC-17 is derived from the base control statement described in [SP 800-53]. AC-17a.[01] is an example of a determination statement for a control item that is further granularized from SP 800-53. AC-17b. is an example of a determination statement for a control item that corresponds directly with the SP 800-53 control. Potential assessment methods and objects are added to each assessment procedure. Not all assessment procedures include all three potential assessment methods (i.e., examine, interview, test). The organization determines the assessment methods needed to provide the level of assurance required by the organization. 

|**AC-17**|**REMOTE ACCESS**||
|---|---|---|
||**ASSESSMENT OB**<br>_Determine if:_|**JECTIVE:**|
|Control further<br>granularized<br>from SP 800-53|**AC-17a.[01]**|usage restric�ons are established and documented for each type of remote<br>access allowed;<br>i|
||**AC-17a.[02]**|configura�on/connec�on requirements are established and documented<br>foreach type of remote access allowed;|
||**AC-17a.[03]**|implementa�on guidance is established and documented for each type of<br>remote access allowed;|
|Corresponds<br>directly with SP<br>800-53 control|**AC-17b.**|each type of remote access to the system is authorized prior to allowing such<br>connec�ons.|
||**POTENTIAL ASSE**|**SSMENT METHODS AND OBJECTS:**|
||**AC-17-Examine**|[SELECT FROM: Access control policy; procedures addressing remote access<br>implementa�on and usage (including restric�ons); configura�on management<br>plan; system configura�on se�ngs and associated documenta�on; remote<br>access authoriza�ons; system audit records; system security plan; other relevant<br>documents or records].|
||**AC-17-Interview**|[SELECT FROM: Organiza�onal personnel with responsibili�es for managing<br>remote access connec�ons; system/network administrators; organiza�onal<br>personnel with informa�on security responsibili�es].|
||**AC-17-Test**|[SELECT FROM: Remote access management capability for the system].|



**FIGURE 1: ASSESSMENT PROCEDURE FOR A CONTROL** 

CHAPTER TWO 

PAGE 13 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

Another example of granularization to support control assessments is the case of a privacy control requirement not being applicable to a particular system (e.g., the system does not process personally identifiable information); assessors can disregard such non-applicable requirements and still find that the control is satisfied. Figure 2 provides an example of control CM-04<sup>25</sup> , which is further granularized to address security impacts in CM-04[01] and privacy impacts in CM-04[02]. 

|**CM-04**<br>**I**<br> <br>|**MPACT ANALYSE**<br>**ASSESSMENT OB**<br>_Determine if:_<br>|**S**<br>**JECTIVE:**<br>|
|---|---|---|
|<br>|**CM-04[01]**<br>**CM-04[02]**<br>**POTENTIAL ASSE**<br>|changes to the system are analyzed to determine poten�al security impacts<br>prior to change implementa�on;<br>changes to the system are analyzed to determine poten�al privacy impacts prior<br>to change implementa�on.<br>**SSMENT METHODS AND OBJECTS:**<br>i|
||**CM-04-Examine**|[SELECT FROM: Configura�on management policy; procedures addressing<br>security impact analyses for changes to the system; procedures addressing<br>privacy impact analyses for changes to the system; configura�on management<br>plan; security impact analysis documenta�on; privacy impact analysis<br>documenta�on; privacy impact assessment; privacy risk assessment<br>documenta�on, system design documenta�on; analysis tools and associated<br>outputs; change control records; system audit records; system security plan;<br>privacy plan; other relevant documents or records].<br>**Granularized to address**<br>**privacy impacts separate**<br>**from security impacts**|
||**CM-04-Interview**|[SELECT FROM: Organiza�onal personnel with responsibility for conduc�ng<br>security impact analyses; organiza�onal personnel with responsibility for<br>conduc�ng privacy impact analyses; organiza�onal personnel with informa�on<br>security and privacy responsibili�es; system developer; system/network<br>administrators; members of change control board or similar].|
||**CM-04-Test**|[SELECT FROM: Organiza�onal processes for security impact analyses;<br>organiza�onal processes for privacy impact analyses].|



**FIGURE 2. ASSESSMENT PROCEDURE FOR A CONTROL FURTHER GRANULARIZED TO FACILITATE ASSESSMENT** 

Additionally, determination statements for organization-defined parameters (ODPs) are listed first and separately from the determination statements for each control item within each control or control enhancement to enable the assessor to quickly determine whether the ODPs are defined or selected by the organization. ODPs appear first in the determination statements, and each include a unique identifier associated with the control to facilitate a more efficient and streamlined assessment. ODPs include: 

- **Assignment operations** , where the organization defines a value (e.g., frequency, circumstances, personnel, or roles) 

- **Selection operations** , where the organization selects one or more of the options provided in the ODP 

The ODP numbering convention is “ **XX-nn_ODP”** , where XX is the two-character control family abbreviation, and nn is the control number (with a leading zero for single digits) followed by 

25 Note that the control identifiers (e.g., CM-4), as published in [SP 800-53], do not include a leading zero. Future revisions of SP 800-53 control identifiers will include a leading zero (e.g., CM-04). 

CHAPTER TWO 

PAGE 14 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

“_ODP”. If there is more than one ODP for the assessment procedure, “_ODP” is followed by square-bracketed sequential numbers starting from “01”. The ODP value is referenced in subsequent determination statements using the ODP unique identifier and a short phrase describing the ODP surrounded by < >. Similar to declaring a variable in computer programming, the ODP serves as a symbolic name to reference a stored value. In this scenario, the ODP unique identifier serves as the symbolic name, and the value assigned or selected by the organization is the stored value. 

Figure 3 provides an example of an assessment procedure for control CM-02 that includes two assignment operations: CM-02_ODP[01] and CM-02_ODP[02]. 

|**CM-02**|**BASELINE CONFI**<br>**ASSESSMENT OB**<br>_Determine if:_|**GURATION**<br>**JECTIVE:**<br>**_ii     i_**|
|---|---|---|
|**Organiza�on-**|**CM-02_ODP[01]**|**_the frequency of baseline configuration review and update is defined;_**<br>**_ii_**|
|**Defined**<br>**Parameter**<br>**id�fi**|**CM-02_ODP[02]**|**_the circumstances requiring baseline configuration review and update are_**<br>**_defined;_**|
|**(ODP) enier**|**CM-02a.[01]**|a current baseline configura�on of the system is developed and documented;|
||**CM-02a.[02]**|a current baseline configura�on of the system is maintained under configura�on<br>control;<br>**Assignment Statement**|
||**CM-02b.01**|the baseline configura�on of the system is reviewed and updated<br>**_<CM-02_ODP[01] frequency_**_>_;|
||**CM-02b.02**|the baseline configura�on of the system is reviewed and updated when required<br>due to**_<CM-02_ODP[02] circumstances>;_**<br>**Reference to**<br>**ODP in**<br>**determina�on**|
||**CM-02b.03**<br>**POTENTIAL ASSE**<br>|the baseline configura�on of the system is reviewed and updated when system<br>components are installed or upgraded.<br>**SSMENT METHODS AND OBJECTS:**<br>i<br>**statement**|
||**CM-02-Examine**|[SELECT FROM: Configura�on management policy; procedures addressing the<br>baseline configura�on of the system; configura�on management plan;<br>enterprise architecture documenta�on; system design documenta�on;<br>system<br>security plan; privacy plan; system architecture and configura�on<br>documenta�on; system configura�on se�ngs and associated documenta�on;<br>system component inventory; change control records; other relevant documents<br>or records].|
||**CM-02-Interview**|[SELECT FROM: Organiza�onal personnel with configura�on management<br>responsibili�es; organiza�onal personnel with informa�on security and privacy<br>responsibili�es; system/network administrators].|
||**CM-02-Test**|[SELECT FROM: Organiza�onal processes for managing baseline configura�ons;<br>automated mechanisms suppor�ng configura�on control of the baseline<br>configura�on].|



**FIGURE 3. ASSESSMENT PROCEDURE FOR CONTROL WITH ORGANIZATION-DEFINED PARAMETER: ASSIGNMENT OPERATIONS** 

CHAPTER TWO 

PAGE 15 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

Figure 4 provides an example of an assessment procedure for a control, MP-07, that includes assignment operations and a selection operation. Selection operations include a list of potential parameter values that the organization chooses from and instructions to select one or more parameters. The list of parameter values is identified using braces { }, with each potential parameter value separated with a semicolon. When the ODP for a selection operation is referenced in a subsequent determination statement, the ODP unique identifier and phrase “SELECTED PARAMETER VALUE(S)” is surrounded by < >. 

||**MP-07**|**MEDIA USE**||
|---|---|---|---|
|||**ASSESSMENT OB**<br>_Determine if:_|**JECTIVE:**|
|**Organ**|**iza�on-**|**MP-07_ODP[01]**|**_types of system media to be restricted or prohibited from use on systems or_**<br>**_system components are defined;_**<br>**_i_**|
|**Defi**<br>**Para**<br>**(ODP) ii**|**ined**<br>**meter**<br>**en�fier**|**MP-07_ODP[02]**|**_one of the following PARAMETER VALUES is selected to be applied on specific_**<br>**_types of system media: {restrict; prohibit};_**<br>**_i_**|
|**i**|**i**|**MP-07_ODP[03]**|**_systems or system components on which the use of specific types of system_**<br>**_media to be restricted or prohibited are defined;_**|
|||**MP-07_ODP[04]**|**_controls to restrict or prohibit the use of specific types of system media on_**<br>**_systems or system components are defined;_**<br>**~~Selec�on Statement~~**|
|||**MP-07a.**|the use of**_<MP-07_ODP[01] types of system media>_**is<br>**_<MP-07_ODP[02] SELECTED PARAMETER VALUE>_**on**_<MP-07_ODP[03] systems_**<br>**_or system components>_**using**_<MP-07_ODP[04] controls>_**;<br>**Reference to**<br>**ODP in**<br>**determina�on**<br>**statement**|
|||**MP-07b.**<br>**POTENTIAL ASSE**|the use of portable storage devices in organiza�onal systems is prohibited when<br>such devices have no iden�fiable owner.<br>**SSMENT METHODS AND OBJECTS:**|
|||**MP-07-Examine**|[SELECT FROM: System media protec�on policy; system use policy; procedures<br>addressing media usage restric�ons; rules of behavior; system design<br>documenta�on; system configura�on se�ngs and associated documenta�on;<br>audit records; system security plan; other relevant documents or records].|
|||**MP-07-Interview**|[SELECT FROM: Organiza�onal personnel with system media use responsibili�es;<br>organiza�onal personnel with informa�on security responsibili�es;<br>system/network administrators].|
|||**MP-07-Test**|[SELECT FROM: Organiza�onal processes for media use; automated mechanisms<br>restric�ng or prohibi�ng use of system media on systems or system<br>components].|



**FIGURE 4. ASSESSMENT PROCEDURE FOR CONTROL WITH ORGANIZATION-DEFINED PARAMETER: SELECTION OPERATION** 

CHAPTER TWO 

PAGE 16 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

Figure 5 provides an example of an assessment procedure for a control, CA-03, that includes an ODP that consists of a selection operation with an embedded assignment operation. The selection operation, CA-03(01)_ODP[01], identifies a list of parameters to choose from, including another ODP. The assignment operation for CA-03(01)_ODP[02] is only defined if the organization selects the ODP from the list of parameters. When the ODP for a selection operation is referenced in a subsequent determination statement, the ODP unique identifier and phrase “SELECTED PARAMETER VALUE(S)” is surrounded by < >. In this scenario, if the embedded assignment operation is selected, it becomes the “SELECTED PARAMETER VALUE(S)”. 



<!-- Start of picture text -->
Selec�on statement with<br>assignment statement as<br>CA-03 INFORMATION EXCHANGE poten�al parameter value<br>ASSESSMENT OBJECTIVE:<br>Determine if:<br>CA-03_ODP[01] one or more of the following PARAMETER VALUES is/are selected:<br>Organiza�on- {interconnection security agreements; information exchange security<br>Defined<br>Parameter  agreements; memoranda of understanding or agreement; service level<br>(ODP) iden�fier agreements; user agreements; non-disclosure agreements ;  <CA-03 _ ODP [ 02 ]<br>t yp e o f  a g reement> };<br>CA-03_ODP[02] the type of agreement used to approve and manage the exchange of<br>information is defined (if selected);<br>CA-03_ODP[03] the frequency at which to review and update agreements is defined;<br>CA-03a. the exchange of informa�on between system and other systems is approved and<br>Embedded Assignment  managed using  <CA-03_ODP[01] SELECTED PARAMETER VALUE(S)>;<br>Statement, def i ned<br>CA-03b.[01] only if the interface characteris�cs are documented as part of each exchange selected<br>agreement;<br>Reference to ODP with<br>CA-03b.[02] security requirements are documented as part of each exchange agreement; SELECTED PARAMETER<br>VALUE(S) in determina�on<br>CA-03b.[03] privacy requirements are documented as part of each exchange agreement; statement<br>CA-03b.[04] controls are documented as part of each exchange agreement;<br>CA-03b.[05] responsibili�es for each system are documented as part of each exchange<br>agreement;<br>CA-03b.[06] the impact level of the informa�on communicated is documented as part of<br>each exchange agreement;<br>CA-03c. agreements are reviewed and updated  <CA-03_ODP[03] frequency>.<br>POTENTIAL ASSESSMENT METHODS AND OBJECTS:<br>CA-03-Examine [SELECT FROM: Access control policy; procedures addressing system<br>connec�ons; system and communica�ons protec�on policy; system<br>interconnec�on security agreements; informa�on exchange security<br>agreements; memoranda of understanding or agreements; service level<br>agreements; non-disclosure agreements; system design documenta�on; system<br>configura�on se�ngs and associated documenta�on; system security plan;<br>privacy plan; other relevant documents or records].<br>CA-03-Interview [SELECT FROM: Organiza�onal personnel with responsibili�es for developing,<br>implemen�ng, or approving system interconnec�on agreements; organiza�onal<br>personnel with informa�on security and privacy responsibili�es; personnel<br>managing the system(s) to which the interconnec�on security agreement<br>applies].<br><!-- End of picture text -->

**FIGURE 5. ASSESSMENT PROCEDURE FOR CONTROL WITH ORGANIZATION-DEFINED PARAMETERS: SELECTION OPERATION WITH EMBEDDED ASSIGNMENT OPERATION** 

CHAPTER TWO 

PAGE 17 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

Although not explicitly noted with each assessment method in the assessment procedure, the attribute values of depth and coverage<sup>26</sup> are assigned by the organization and specified within the assessment plan (e.g., the level of rigor for documentation review, the number of similar assessment objects to test). The assessor/assessment team applies the depth and coverage attributes in the execution of the assessment method against an assessment object to provide the level of assurance required by the organization. 

If the control has any enhancements as designated by sequential parenthetical numbers (for example, AC-17(01) for the first enhancement for AC-17), assessment objectives are developed for each enhancement using the same process used for the base control. The resulting assessment objectives are numbered sequentially in the same way as the assessment procedure for the base control – first in accordance with the numbering scheme in [SP 800-53] and, subsequently, using bracketed sequential numbers to further apportion control enhancement requirements to facilitate assessments (e.g., AC-17(01), AC-17(02), AC-17(03)). 

Figure 6 illustrates an example of an assessment procedure developed to assess the effectiveness of the first enhancement to security control AC-17, AC-17(01). 

|**AC-17(01)**|**REMOTE ACCESS |**<br>**ASSESSMENT OBJE**<br>_Determine if:_|**MONITORING AND CONTROL**<br>**CTIVE:**|
|---|---|---|
||**AC-17(01)[01]**|automated mechanisms are employed to monitor remote access methods;|
||**AC-17(01)[02]**|automated mechanisms are employed to control remote access methods.|
||**POTENTIAL ASSESS**<br>|**MENT METHODS AND OBJECTS:**<br>|
||**AC-17(01)-Examine**|[SELECT FROM: Access control policy; procedures addressing remote access<br>to the system; system design documenta�on; system configura�on se�ngs<br>and associated documenta�on; system audit records; system monitoring<br>records; system security plan; other relevant documents or records].|
||**AC-17(01)-Interview**|[SELECT FROM: System/network administrators; organiza�onal personnel<br>with informa�on security responsibili�es; system developers].|
||**AC-17(01)-Test**|[SELECT FROM: Automated mechanisms monitoring and controlling remote<br>access methods].|



**FIGURE 6:  ASSESSMENT PROCEDURE FOR CONTROL ENHANCEMENT** 

> 26 Attribute values of depth and coverage are described in <u>Appendix C.</u> 

CHAPTER TWO 

PAGE 18 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

### **CHAPTER THREE** 

# **THE PROCESS** 

CONDUCTING EFFECTIVE SECURITY AND PRIVACY CONTROL ASSESSMENTS 

This chapter describes the process of assessing the security and privacy controls in organizational systems and environments of operation. The process to assess controls includes: 

- the activities carried out by organizations and assessors to prepare for security and privacy control assessments; 

- the development of security and privacy assessment plans; the conduct of control assessments and the analysis, documentation, and reporting of assessment results; and 

- post-assessment report analysis and follow-on activities. 

Additionally, this chapter describes assessing security and privacy _capabilities_ .<sup>27</sup> 



**FIGURE 7. OVERVIEW OF PROCESS TO CONDUCT EFFECTIVE SECURITY AND PRIVACY CONTROL ASSESSMENTS** 

## **3.1 PREPARE FOR SECURITY AND PRIVACY CONTROL ASSESSMENTS** 

Table 1 provides a summary of the purpose, roles, and expected outcomes of the Prepare for Security and Privacy Control Assessments Step. 

**TABLE 1. PREPARE FOR SECURITY AND PRIVACY CONTROL ASSESSMENTS SUMMARY** 

|**Purpose**|**Address a range of issues pertaining to the cost, schedule, scope, and performance of**<br>**the control assessment.**|
|---|---|
|**Primary**<br>**Roles**|Authorizing Official, Authorizing Official Designated Representative, system owner,<br>common controlprovider,control assessors|
|**Supporting**<br>**Roles**|System security officer, system privacy officer|
|**Outcomes**|•<br>The objective, scope, and timeframe of control assessment determined<br>•<br>Key organizational stakeholders notified and necessary resources allocated<br>•<br>Assessors/assessment teams identified<br>•<br>Artifacts collected and provided to assessors/assessment teams<br>•<br>Mechanism to minimize ambiguities and misunderstandings about control<br>implementation and identified control deficiencies or weaknesses established<br>•<br>Assessors/assessment teams understand the organization’s operations, structure,<br>objective,scope,and timeframe of control assessment|



> 27 A security and privacy _capabilit_ y is a combination of mutually reinforcing security and privacy controls (i.e., safeguards and countermeasures) implemented by technical means (i.e., functionality in hardware, software, and firmware), physical means (i.e., physical devices and protective measures), and procedural means (i.e., procedures performed by individuals). 

PAGE 19 

CHAPTER THREE 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

Conducting security and privacy control assessments can be difficult, challenging, and resource intensive. Security and privacy control assessments may be conducted by different organizational entities with distinct oversight responsibilities. However, success requires the cooperation and collaboration of all parties with a vested interest in the organization’s information security or privacy posture, including control assessors, system security and privacy officers, system owners, common control providers, authorizing officials, chief information officers, senior information security officers, senior agency officials for privacy/chief privacy officers, chief executive officers/heads of agencies, security and privacy staffs, Inspectors General, and OMB. Establishing an appropriate set of expectations before, during, and after an assessment is paramount to achieving an acceptable outcome (i.e., producing information necessary to help the authorizing official make a credible, risk-based decision on whether to place the system into operation or continue its operation). 

Thorough preparation by the organization and assessors is an important aspect of conducting effective security and privacy control assessments. Preparatory activities address a range of issues relating to the cost, schedule, and performance of the assessment. From an organizational perspective, preparing for a security and privacy control assessment includes the following key activities: 

- Ensuring that appropriate policies covering security and privacy control assessments are in place and understood by all affected organizational elements; 

- Ensuring that all steps in the RMF prior to the security or privacy control assessment step have been successfully completed and received appropriate management oversight;<sup>28</sup> 

- Establishing the objective and scope of assessments (i.e., the purpose of the assessments and what is being assessed); 

- Ensuring that security and privacy controls identified as common controls (and the common portion of hybrid controls) have been assigned to appropriate organizational entities (i.e., common control providers) for development and implementation;<sup>29</sup> 

- Notifying key organizational officials of impending assessments and allocating necessary resources to carry out the assessments; 

- Establishing appropriate communication channels among organizational officials with an interest in the assessments; 

- Establishing time frames for completing the assessments and key milestone decision points required by the organization; 

- Identifying and selecting appropriate assessors/assessment teams that will be responsible for conducting the assessments and considering issues of assessor independence; 

> 28 Conducting security and privacy control assessments in parallel with the development/acquisition and implementation phases of the life cycle allows for the early identification of weaknesses and deficiencies and provides the most cost-effective method for initiating corrective actions. Issues found during development assessments can be referred to authorizing officials for early resolution, as appropriate. The results of security and privacy control assessments carried out during system development and implementation can also be used (consistent with reuse criteria) during the authorization process to avoid system fielding delays or the costly repetition of assessments. 

> 29 Common control assessments and assessments of the common part of hybrid controls are the responsibility of the common control providers, not the system owner inheriting the controls. 

PAGE 20 

CHAPTER THREE 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

- Providing artifacts to the assessors/assessment teams (e.g., policies, procedures, plans, specifications, designs, records, administrator/operator manuals, system documentation, information exchange agreements, previous assessment results, legal requirements); and 

- Establishing a mechanism between the organization and the assessors and/or assessment teams to minimize ambiguities or misunderstandings about the implementation of security and privacy controls and related weaknesses or deficiencies identified during the assessments. 

Control assessors/assessment teams begin preparing for their respective assessments by: 

- Obtaining a general understanding of the organization’s operations (including mission, functions, and business processes) and how the system or common control that is the subject of the particular assessment supports those organizational operations, 

- Obtaining an understanding of the structure of the system (i.e., system architecture) and the security and privacy controls being assessed (including system-specific, hybrid, and common controls), 

- Identifying the organizational entities responsible for the development and implementation of the common controls (or the common portion of hybrid controls) supporting the system, 

- Meeting with appropriate organizational officials to ensure common understanding for assessment objectives and the proposed rigor and scope of the assessment, 

- Obtaining artifacts needed for the assessment (e.g., policies, procedures, plans, specifications, designs, records, administrator and operator manuals, system documentation, information exchange agreements, previous assessment results), 

- Establishing appropriate organizational points of contact to carry out the assessments, and 

- Obtaining previous assessment results that may be appropriately reused for the current assessment (e.g., Inspector General reports, audits, vulnerability scans, physical security inspections, developmental testing and evaluation, vendor flaw remediation activities, [ISO 15408] evaluations). 

In preparation for the assessment of security and privacy controls, the necessary background information is assembled and made available to the assessors or assessment team.<sup>30</sup> To the extent necessary to support the specific assessment, and depending upon whether security controls or privacy controls are being assessed, the organization identifies and arranges access to elements of the organization responsible for developing, documenting, disseminating, reviewing, and updating: 

- all policies and associated procedures for implementing policy-compliant controls; 

- • the policies for the system and any associated implementing procedures, individuals, or groups responsible for the development, implementation, operation, and maintenance of controls; 

30 System (or program) owners and organizational entities developing, implementing, and/or administering common controls (i.e., common control providers) are responsible for providing needed information to assessors. 

PAGE 21 

CHAPTER THREE 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

- any artifacts or materials (e.g., security or privacy plans, records, schedules, assessment reports, after-action reports, agreements, authorization packages) associated with the implementation and operation of the controls to be assessed; and 

- the specific objects to be assessed.<sup>31</sup> 

The availability of essential documentation as well as access to key organizational personnel and the system or common control being assessed are paramount to a successful assessment. 

Organizations consider both the technical expertise and level of independence required in selecting security and privacy control assessors.<sup>32</sup> Organizations ensure that assessors possess the required skills and technical expertise to successfully carry out assessments of systemspecific, hybrid, and common controls.<sup>33</sup> Skills and expertise includes knowledge of and experience with the specific hardware, software, and firmware components employed by the organization. An independent assessor is any individual capable of conducting an impartial assessment of security and privacy controls employed within or inherited by a system. Impartiality implies that security and privacy control assessors are free from any perceived or actual conflicts of interest with respect to the development, operation, and/or management of the system or the determination of security and privacy control effectiveness.<sup>34</sup> The authorizing official or designated representative determines the required level of independence for assessors based on the results of the security categorization process for the system (in the case of security control assessments) and the risk to organizational operations and assets, individuals, other organizations, and the Nation. The authorizing official determines whether the level of assessor independence is sufficient to provide confidence that the assessment results produced are sound and can be used to make a risk-based decision on whether to place the system or common control into operation or continue its operation. 

Independent security and privacy control assessment services can be obtained from other elements within the organization or be contracted to a public or private sector entity outside of the organization. In special situations (e.g., when the organization that owns the system or common control is small or the organizational structure requires that the security or privacy control assessment be accomplished by individuals who are in the developmental, operational, and/or management chain of the system owner), independence in the assessment process can be achieved by ensuring that the assessment results are carefully reviewed and analyzed by an 

> 31 In situations where there are multiple security and privacy assessments ongoing or planned within an organization, access to organizational elements, individuals, and artifacts supporting the assessments is centrally managed by the organization to ensure a cost-effective use of time and resources. 

32 In accordance with [OMB A-130], an independent evaluation of the privacy program and practices is not required. However, an organization may choose to employ independent privacy assessments at its discretion. 

> 33 NIST [SP 800-181] describes the Workforce Framework for Cybersecurity (National Initiative for Cybersecurity Education [NICE] Framework), a fundamental reference for describing and sharing information about cybersecurity work through Task statements, and Knowledge and Skills Statements. The NICE Framework is a reference source with which organizations or sectors can develop additional publications or tools that meet their needs to define or provide guidance on different aspects of cybersecurity education, training, and workforce development. 

34 Contracted assessment services are considered independent if the system (or program) owner is not directly involved in the contracting process or cannot unduly influence the independence of the assessor(s) conducting the assessment of the security or privacy controls. 

PAGE 22 

CHAPTER THREE 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

independent team of experts to validate the completeness, consistency, and veracity of the results.<sup>35</sup> 

## **3.2 DEVELOP SECURITY AND PRIVACY ASSESSMENT PLANS** 

Table 2 provides a summary of the purpose, roles, and expected outcomes of the Develop Security and Privacy Assessment Plans Step. 

**TABLE 2. DEVELOP SECURITY AND PRIVACY PLANS SUMMARY** 

|**Purpose**|**Provide the objectives for the security and privacy control assessments, as well as**<br>**a detailed roadmap of how to conduct such assessments based on the security**<br>**andprivacy plan(s). **|
|---|---|
|**Primary Roles**|Control assessors|
|**Supporting**<br>**Roles**|System security officers, system privacy officers, system owners|
|**Outcomes**|•<br>Controls and control enhancements to be included in assessments are<br>determined<br>•<br>Assessment procedures are selected and tailored; additional procedures for<br>security and privacy requirements/controls not covered by[SP 800-53]are<br>developed<br>•<br>Assessment procedures are optimized to reduce duplication of effort<br>•<br>Assessmentplan is finalized,and organizational approval is obtained|



The _security assessment plan_ and _privacy assessment plan_ provide the objectives for the security and privacy control assessments, respectively, as well as a detailed roadmap of how to conduct such assessments. The assessment plans may be developed as one integrated plan or as distinct plans, depending upon organizational needs. The following steps are considered by assessors when developing plans to assess the security and privacy controls in organizational systems or common controls available for inheritance: 

- Determine which security and privacy controls/control enhancements are to be included in assessments based on the contents of the security plan and privacy plan (or equivalent document if the controls to be assessed are non-system-based common controls)<sup>36</sup> and the purpose and scope of the assessments, 

- Select the appropriate assessment procedures to be used during assessments based on the security or privacy controls and control enhancements to be assessed, 

- Tailor the selected assessment procedures (e.g., select appropriate assessment methods and objects, and assign depth and coverage attribute values), 

- Develop additional assessment procedures to address any security requirements or controls that are not covered by [SP 800-53], 

> 35 The authorizing official consults with the Office of the Inspector General, the senior information security officer, senior agency officials for privacy/chief privacy officers, and the chief information officer, as appropriate, to discuss the implications of any decisions on assessor independence in the types of special circumstances described above. 

> 36 The approach to developing assessment plans and conducting control assessments also applies to information security program plans and privacy program plans. 

PAGE 23 

CHAPTER THREE 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

- Optimize the assessment procedures to reduce duplication of effort (e.g., sequencing and consolidating assessment procedures) and provide cost-effective assessment solutions, and 

- Finalize assessment plans and obtain the necessary approvals to execute the plans. 

#### **_3.2.1   DETERMINE WHICH SECURITY AND PRIVACY CONTROLS ARE TO BE ASSESSED_** 

The security plan and privacy plan provide an overview of the security and privacy requirements for the system and organization and describe the security controls and privacy controls in place or planned for meeting those requirements. For the assessment of common controls that are not implemented by a system, a document equivalent to the security or privacy plan may be used. The assessor starts with the security or privacy controls described in the security or privacy plan and considers the purpose of the assessment. A security or privacy control assessment can be a complete assessment of all controls in a system (e.g., during an initial system authorization process), a partial assessment of the controls in a system (e.g., during system development as part of a targeted assessment resulting from changes affecting specific controls or where controls were previously assessed and the results accepted in the reciprocity process), or a common control assessment. 

For partial assessments, system owners and common control providers collaborate with organizational officials with an interest in the assessment (e.g., senior information security officers, senior agency officials for privacy/chief privacy officers, mission/information owners, Inspectors General, and authorizing officials) to determine which controls are to be assessed. The determination of the controls to be assessed depends on the purpose of the assessment. For example, during the initial phases of the system development life cycle, specific controls may be selected for assessment to promote the early detection of weakness and deficiencies and a more cost-effective approach to risk response. After the initial authorization to operate has been granted, targeted assessments may be necessary when changes are made to the system, specific security or privacy controls, common controls, or the environment of operation. In such cases, the focus of the assessment is on the controls that may have been affected by the change. 

#### **_3.2.2   SELECT PROCEDURES TO ASSESS THE SECURITY AND PRIVACY CONTROLS_** 

SP 800-53A provides assessment procedures for each security and privacy control and control enhancement in [SP 800-53]. For each control in the security plan and privacy plan to be included in the assessment, assessors select the corresponding assessment procedure from <u>Chapter 4. The selected assessment procedures can vary from assessment to assessment based</u> on the current content of the security plans and privacy plans and the purpose of the assessment (e.g., complete assessment, partial assessment, common control assessment). 

#### **_3.2.3   TAILOR ASSESSMENT PROCEDURES_** 

In a manner similar to how the controls from [SP 800-53] are tailored for the organization’s mission, business functions, characteristics of the system, and operating environment, organizations tailor the assessment procedures in <u>Chapter 4 to meet specific organizational</u> needs. Organizations have the flexibility to perform the tailoring process at the organization level for all systems or common controls, at the individual system level, or using a combination of organization-level and system-specific approaches. Control assessors determine if the 

PAGE 24 

CHAPTER THREE 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

organization provides additional tailoring guidance prior to initiating the tailoring process. Assessment procedures are tailored by: 

- Selecting the appropriate assessment methods and objects needed to satisfy the stated assessment objectives, 

- Selecting the appropriate depth and coverage attribute values to define the rigor and scope of the assessment, 

- Identifying common controls and inherited portions of hybrid controls that have been assessed by a separately documented security assessment plan or privacy assessment plan and do not require the repeated execution of the assessment procedures,<sup>37</sup> 

- Developing system/platform-specific and organization-specific assessment procedures (which may be adaptations of those in Chapter 4), 

- Incorporating assessment results from previous assessments where the results are deemed applicable, and 

- Making appropriate adjustments in assessment procedures to obtain the requisite assessment evidence from external providers. 

#### **_3.2.3.1   ASSESSMENT METHOD- AND OBJECT-RELATED CONSIDERATIONS_** 

Organizations can specify, document, and configure their systems in a variety of ways, and the content and applicability of existing assessment evidence varies. This variety may result in the need to apply a mixture of assessment methods to assessment objects to generate the assessment evidence needed to determine whether the security and privacy controls are effective in their application. Additionally, as described in <u>Section 2.3</u> and Section 2.4, the number and type of assessment methods and assessment objects needed to provide the required assurance varies based on the depth and coverage needed for the assessment. Therefore, the assessment methods and objects provided with each assessment procedure are termed _potential_ to reflect the need to choose the specific methods and objects most appropriate for a specific assessment. The assessment methods and objects chosen are those deemed necessary to produce the evidence needed to make the determinations described in the determination statements in support of assurance requirements and the associated management of risk. The potential methods and objects in the assessment procedure are provided as a resource to assist in the selection of appropriate methods and objects and not with the intent of limiting the selection. Organizations use their judgment when selecting assessment methods and associated assessment objects. Organizations select those methods and objects that most cost-effectively manage risk and contribute to making the determinations associated with the assessment objective.<sup>38</sup> The quality of assessment results is based on the soundness of the rationale provided for selecting the methods and objects, not the specific set 

> 37 Common controls are not assessed as part of system control assessments unless the common controls are part of a system that provides the common control(s) for inheritance by other systems. The assessor simply verifies that the system being assessed has actually inherited the common control (i.e., that a given inherited common control is being used by the system being assessed to provide protection) and the control is not implemented at the level of the system being assessed. 

38 The selection of assessment methods and objects (including the number and type of assessment objects, i.e., coverage) can be a significant factor in cost-effectively managing risk while still meeting the assessment objectives. 

PAGE 25 

CHAPTER THREE 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

of methods and objects applied. It is not necessary, in most cases, to apply every assessment method to every assessment object to obtain the desired assurance. 

#### **_3.2.3.2   DEPTH- AND COVERAGE-RELATED CONSIDERATIONS_** 

In addition to selecting appropriate assessment methods and objects, each assessment method (i.e., examine, interview, and test) is associated with the depth and coverage attributes described in Appendix C. The attribute values identify the rigor (depth) and scope (coverage) of the assessment procedures executed by the assessor. The values selected by the organization are based on the characteristics of the system being assessed (including assurance requirements) and the specific determinations to be made. The depth and coverage attribute values are associated with the assurance requirements specified by the organization (i.e., the rigor and scope of the assessment increases in direct relationship with the assurance requirements, which in turn increase in direct relationship with the adverse impact of loss). 

#### **_3.2.3.3   COMMON CONTROL-RELATED CONSIDERATIONS_** 

Assessors note which security and privacy controls (or parts of such controls) in security plans or privacy plans are designated as _common controls_ .<sup>39</sup> Since the assessment of common controls is the responsibility of the organizational entity that developed and implemented the controls (i.e., common control provider), the assessment procedures in <u>Chapter 4 are also used to assess</u> common controls. The results from the common control assessment are made available to organizational systems and system owners that elect to inherit the common controls.<sup>40</sup> 

Another consideration in assessing common controls is awareness of system-specific aspects of a control that are not covered by the organizational entities responsible for the common aspects of the control. Such controls are referred to as _hybrid controls_ . For example, CP-02, the contingency planning security control, may be considered a hybrid control by the organization if there is a contingency plan developed by the organization for all organizational systems. System owners are expected to adjust or tailor the organization-developed contingency plan when there are specific aspects of the plan that need to be defined for the particular system where the control is employed. For each hybrid control, assessors include in security assessment plans or privacy assessment plans the portions of the assessment procedures from Chapter 4 related to the parts of the control that are system-specific to ensure that, along with the results from common control assessments, all aspects of the control are assessed. 

> 39 Common controls support multiple systems within the organization, and the protection measures provided by common controls are inherited by individual systems. Therefore, the organization determines the appropriate set of common controls to ensure that both the strength of the controls (i.e., security or privacy capability) and level of rigor and intensity of the control assessments are commensurate with the privacy risk assessment and categorization of the individual systems inheriting those controls. Weaknesses or deficiencies in common controls have the potential to adversely affect large portions of the organization and thus require significant attention. 

> 40 If assessment results are not currently available for the common controls, the assessment plans for the systems under assessment that depend on those controls are duly noted. The assessments cannot be considered complete until the assessment results for the common controls are made available to system owners. 

PAGE 26 

CHAPTER THREE 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

##### **ASSESSING COMMON CONTROLS AND PORTIONS OF HYBRID CONTROLS INHERITED** **<mark>FROM A COMMON CONTROL PROVIDER</mark>** 

<mark>In system security and privacy plans, common controls or portions of hybrid controls implemented and maintained by the common control provider are indicated as “inherited” with a reference to the common control provider. The system owner is not responsible for assessing common controls or the inherited portion of hybrid controls. Common controls are assessed separately and are not reassessed at the system level by each system that inherits them. However, the assessor verifies if the system does, in fact, inherit and utilize the common control as indicated in the system security plans and privacy plans. The assessment of common controls (for the common control provider) is carried out using the same process</mark> as a system control assessment. 

#### **_3.2.3.4   SYSTEM/PLATFORM- AND ORGANIZATION-RELATED CONSIDERATIONS_** 

The assessment procedures in SP 800-53A may be adapted to address system-, platform-, or organization-specific dependencies. For example, the assessment of a Linux implementation of control IA-02 for the identification and authentication of users might include an explicit examination of any key-based, “password-less” login capability and potential risks inherent from any deficiency in key management, account management, system and boundary protection, physical and environmental protection, and other safeguards to prevent identification and authentication bypass by unauthorized users or processes acting on behalf of users. 

#### **_3.2.3.5   REUSE OF ASSESSMENT EVIDENCE-RELATED CONSIDERATIONS_** 

Reuse of assessment results from previously accepted or approved assessments is considered in the body of evidence for determining overall security and privacy control effectiveness. Previously accepted or approved assessments include assessments of inherited common controls that are managed by the organization and support multiple systems, assessments of security or privacy controls that are reviewed as part of the control implementation (e.g., CP-02 requires a review of the contingency plan), or security-related information generated by the organization’s ISCM program. The acceptability of reusing assessment results in a security control assessment or privacy control assessment is coordinated with and approved by the users of the assessment results. It is essential that system owners and common control providers collaborate with authorizing officials and other appropriate organizational officials to determine the acceptability of using previous assessment results. When considering the reuse of assessment results and the value of those results to the current assessment, assessors determine the credibility of the assessment evidence, the appropriateness of previous analysis, and the applicability of the assessment evidence to current system operating conditions. If previous assessment results are reused, the date and type of the original assessment are documented in the assessment plan and assessment report. 

In certain situations, it may be necessary to supplement previous assessment results under consideration for reuse with additional assessment activities to fully address the current assessment objectives. For example, if an independent evaluation of an information technology product did not test a particular configuration setting that is employed by the organization in a system, then the assessor may need to supplement the original test results with additional testing to cover that configuration setting for the current system environment. The decision to reuse assessment results is documented in the security assessment plan or privacy assessment 

PAGE 27 

CHAPTER THREE 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

plan and the final security assessment report or privacy assessment report, and it is consistent with legislation, policies, directives, standards, and guidelines. 

The following items are considered when validating previous assessment results for reuse: 

- **Changing conditions associated with security controls and privacy controls over time.** Security and privacy controls that were deemed effective during previous assessments may have become ineffective due to changing conditions within the system or its environment of operation, including emergent threat information. Assessment results that were found to be previously acceptable may no longer provide credible evidence for the determination of security or privacy control effectiveness, and therefore, a reassessment may be required. Applying previous assessment results to a current assessment necessitates the identification of any changes that have occurred since the previous assessment and the impact of these changes on the previous results. For example, reusing previous assessment results from examining an organization’s security or privacy policies and procedures may be acceptable if it is determined that there have not been any significant changes to the identified policies and procedures. Reusing assessment results produced during the previous authorization of a system is a costeffective method for supporting continuous monitoring activities and annual FISMA reporting requirements when the related controls have not changed and there are adequate reasons for confidence in their continued application. 

- **Amount of time that has transpired since previous assessments.** In general, as the time between current and previous assessments increases, the credibility and utility of the previous assessment results decrease. This is primarily because the system or the environment in which the system operates is more likely to change with the passage of time, possibly invalidating the original conditions or assumptions on which the previous assessment was based. 

- **Degree of independence of previous assessments.** Assessor independence can be a critical factor in certain types of assessments. The degree of independence required from assessment to assessment should be consistent. For example, it is not appropriate to reuse results from a previous self-assessment where no assessor independence was required when a current assessment requires a greater degree of independence. 

#### **_3.2.3.6   EXTERNAL SYSTEM- RELATED CONSIDERATIONS_** 

The assessment procedures in <u>Chapter 4 need to be adjusted, as appropriate, to accommodate</u> the assessment of external systems.<sup>41</sup> Because the organization does not always have direct control over the security or privacy controls used in external systems or sufficient visibility into the development, implementation, and assessment of those controls, alternative assessment approaches may need to be applied, resulting in the need to tailor the assessment procedures described in Chapter 4. Where required assurances of agreed-upon security or privacy controls within a system are documented in contracts or service-level agreements, assessors review the contracts or agreements and tailor the assessment procedures as appropriate to assess the 

> 41 An external system is a system or component of a system that is outside of the authorization boundary established by the organization and for which the organization typically has no direct control over the application of required security and privacy controls or the assessment of control effectiveness. [SP 800-37] and [SP 800-53] provide additional guidance on external systems and the effect of employing security and privacy controls in external environments. 

PAGE 28 

CHAPTER THREE 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

security or privacy controls or the security and privacy control assessment results provided through contracts or agreements. In addition, assessors consider any other assessments that have been conducted or are in the process of being conducted for external systems that are relied upon with regard to protecting the system under assessment. Applicable information from these assessments, if deemed reliable, is incorporated into the security assessment report or privacy assessment report, as appropriate. 

#### **_3.2.4   DEVELOP ASSESSMENT PROCEDURES FOR ORGANIZATION-SPECIFIC CONTROLS_** 

Based on organizational policies, mission or business function requirements, and an assessment of risk, organizations may choose to develop and implement additional (organization-specific) controls or control enhancements for their systems that are beyond the scope of [SP 800-53]. Such controls are documented in the security plan and privacy plan as controls not found in SP 800-53. To assess the controls not found in SP 800-53, assessors use the guidelines in Chapter 2 to develop assessment procedures for those controls and control enhancements. The assessment procedures developed are subsequently integrated into the assessment plan, as appropriate. 

#### **_3.2.5   OPTIMIZE SELECTED ASSESSMENT PROCEDURES TO ENSURE MAXIMUM EFFICIENCY_** 

Assessors have flexibility in organizing assessment plans that meet the needs of the organization and that provide the best opportunity for obtaining the necessary evidence to determine security or privacy control effectiveness while reducing overall assessment costs. Combining and consolidating assessment procedures is one area where flexibility can be applied. During the assessment of a system, assessment methods are applied numerous times to a variety of assessment objects within a particular family of controls. To save time, reduce assessment costs, and maximize the usefulness of assessment results, assessors review the selected assessment procedures for the control families and combine or consolidate the procedures (or parts of procedures) whenever possible or practicable. For example, assessors may consolidate interviews with key organizational officials who deal with a variety of security- or privacy-related topics. Assessors may have other opportunities for significant consolidation and cost savings by examining all policies and procedures from the families of security controls and privacy controls at the same time or by organizing groups of related policies and procedures that could be examined as a unified entity. Obtaining and examining configuration settings from similar hardware and software components within the system is another example that can provide significant assessment efficiencies. 

An additional area for consideration in optimizing the assessment process is the sequence in which controls are assessed. The assessment of some controls before others may provide useful information that facilitates understanding and more efficient assessments of other controls. For example, controls such as CM-2 (Baseline Configuration), CM-8 (System Component Inventory), PL-2 (System Security and Privacy Plans), RA-2 (Security Categorization), and RA-3 (Risk Assessment) produce general descriptions of the system. Assessing related controls early in the assessment process may provide a basic understanding of the system that can aid in assessing other controls. In SP 800-53, the discussion section for each control identifies related controls that can provide useful information for organizing the assessment procedures. For example, AC19 (Access Control for Mobile Devices) lists controls MP-4 (Media Storage) and MP-5 (Media Transport) as being related to AC-19. Since AC-19 is related to MP-4 and MP-5, the sequence in 

PAGE 29 

CHAPTER THREE 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

which assessments are conducted for AC-19, MP-4, and MP-5 may facilitate the reuse of assessment information from one control in assessing other related controls. 

#### **_3.2.6   FINALIZE ASSESSMENT PLAN AND OBTAIN APPROVAL TO EXECUTE PLAN_** 

After selecting the assessment procedures (including developing necessary procedures not contained in the SP 800-53A catalog of procedures), tailoring the procedures for system/platform-specific and organization-specific conditions, optimizing the procedures for efficiency, and addressing the potential for unexpected events that may impact the assessment, the assessment plan is finalized and the schedule is established, including key milestones for the assessment process. Once the assessment plan is completed, the plan is reviewed and approved by appropriate organizational officials<sup>42</sup> to ensure that the plan is complete, consistent with the security and privacy objectives of the organization and the organization’s assessment of risk, and cost-effectively manages risk with regard assessment methods and objects, depth and coverage attributes, and to the resources allocated for the assessment. 

## **3.3 CONDUCT SECURITY AND PRIVACY CONTROL ASSESSMENTS** 

Table 3 provides a summary of the purpose, roles, and expected outcomes of the Conduct Security and Privacy Control Assessments Step. 

**TABLE 3. CONDUCT SECURITY AND PRIVACY CONTROL ASSESSMENTS SUMMARY** 

|**Purpose**|**Conduct the security and privacy control assessment in accordance with the**<br>**assessment plan, and document the results in security and privacy assessment**<br>**report(s).**|
|---|---|
|**Primary**<br>**Roles**|Control assessors|
|**Supporting**<br>**Roles**|System security and privacy officers, system owners, security and privacy engineers,<br>security and privacy architects, system administrators, system users|
|**Outcomes**|•<br>In-scope controls and control enhancements are assessed in accordance with the<br>security and privacy assessment plan(s)<br>•<br>Security and privacy assessment report(s) documenting the effectiveness of the<br>controls and identified weaknesses/deficiencies areproduced|



After the assessment plan is approved by the organization, the assessor(s) or assessment team executes the plan in accordance with the agreed-upon schedule. Determining the size and organizational makeup of the assessment team (i.e., skill sets, technical expertise, and assessment experience of the individuals composing the team) is one of the risk management decisions made by the organization requesting and initiating the assessment. The results of control assessments are documented in assessment reports, which are key inputs in the authorization package developed by system owners and common control providers for 

> 42 Organizations establish a security and privacy assessment plan approval process with the specific organizational officials (e.g., systems owners, common control providers, system security and privacy officers, senior information security officers, senior agency officials for privacy/chief privacy officers, authorizing officials) designated as approving authorities. 

PAGE 30 

CHAPTER THREE 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

authorizing officials.<sup>43</sup> Assessment reports include information from assessors (in the form of assessment findings) that is necessary to determine the effectiveness of the security and privacy controls employed within the system.<sup>44</sup> Assessment reports are an important factor in an authorizing official’s determination of risk. Organizations may choose to develop an assessment summary from the detailed findings that are generated by assessors during the security control assessments and privacy control assessments. An assessment summary can provide an authorizing official with an abbreviated version of an assessment report that focuses on the highlights of the assessment, synopsis of key findings, and recommendations for addressing weaknesses and deficiencies in the security or privacy controls assessed. Appendix E provides information on the recommended content of assessment reports. 

Assessment objectives are achieved by applying the designated assessment methods to selected assessment objects and compiling or producing the evidence necessary to make the determination associated with each assessment objective. Each determination statement<sup>45</sup> contained within an assessment procedure executed by an assessor produces one of the following findings: 

- _satisfied (S);_ or 

- _other than satisfied (O)._ 

A finding of “satisfied” indicates that – for the portion of the control addressed by the determination statement – the assessment objective for the control has been met and produces a fully acceptable result. 

A finding of “other than satisfied” indicates – for the portion of the control addressed by the determination statement – potential anomalies in the operation or implementation of the control that may need to be addressed by the organization. A finding of “other than satisfied” may also indicate that the assessor was unable to obtain sufficient information to make the determination called for in the determination statement for reasons specified in the assessment report. For assessment findings that are “other than satisfied”, organizations may choose to define subcategories of findings indicating the severity and/or criticality of the weaknesses or deficiencies discovered and the potential adverse effects on organizational operations (i.e., mission, functions, image, or reputation), organizational assets, individuals, other organizations, or the Nation. Defining such subcategories can help to establish priorities for needed risk mitigation actions. 

Assessor findings are an unbiased, factual reporting of what was found concerning the control assessed. For each finding of “other than satisfied”, assessors indicate which parts of the control are affected by the finding (i.e., aspects of the control that were deemed not satisfied or were not able to be assessed) and describe how the actual state of the control differs from the planned or expected/desired state. The potential for compromises to confidentiality, integrity, 

43 In accordance with [SP 800-37], the authorization package consists of the security plan, privacy plan, security assessment report, privacy assessment report, and plan of action and milestones (POA&M). 

> 44 See Section 3.2.3 for additional information about assessing common controls and portions of hybrid controls inherited from a common control provider. 

> 45 For additional information on determination statements and assessment findings, see <u>Appendix E.</u> 

PAGE 31 

CHAPTER THREE 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

and availability or privacy risks due to “other than satisfied” findings are also noted by the assessor in the assessment report. 

Risk determination and acceptance activities are conducted by the organization postassessment as part of the risk management strategy established by the organization. Postassessment risk management activities involve the senior leadership of the organization, such as heads of agencies, mission and business owners, information owners/stewards, risk executive (function), and authorizing officials in consultation with appropriate organizational support staff (e.g., senior information security officers, senior agency officials for privacy/chief privacy officers, chief information officers, system owners, common control providers, and assessors). Security control assessment and privacy control assessment results are documented at a level of detail appropriate for the assessment in accordance with the reporting format prescribed by organizational policy, NIST guidelines, and OMB policy. The reporting format is appropriate for the type of assessment conducted (e.g., self-assessments by system owners and common control providers, independent verification and validation, independent assessments supporting the authorization process, automated assessments, or independent audits or inspections). 

System owners and common control providers rely on the expertise and technical judgment of assessors to assess the security and privacy controls in the system and inherited by the system and provide recommendations on how to respond to the control assessment results (e.g., accept risk, reject risk, mitigate risk by correcting weaknesses or deficiencies in the controls and reducing or eliminating identified vulnerabilities). The assessment results produced by the assessor (i.e., findings of “satisfied” or “other than satisfied”, identification of the parts of the security or privacy control that did not produce a satisfactory result, and a description of resulting potential for compromises to the system or its environment of operation) are provided to system owners and common control providers in the initial security assessment reports and privacy assessment reports. System owners and common control providers may choose to act on selected recommendations of the assessor before the assessment reports are finalized if there are specific opportunities to correct weaknesses or deficiencies in the security or privacy controls or to correct and/or clarify misunderstandings or interpretations of assessment results.<sup>46</sup> Security or privacy controls that are modified, enhanced, or added during this process are reassessed by the assessor prior to the production of the final assessment reports. 

## **3.4 ANALYZE ASSESSMENT REPORT RESULTS** 

Table 4 provides a summary of the purpose, roles, and expected outcomes of the Analyze Assessment Report Results Step. 

> 46 The correction of weaknesses or deficiencies in security or privacy controls or carrying out recommendations during the review of the initial security assessment reports or privacy assessment reports by system owners or common control providers are not intended to replace the formal risk response process by the organization, which occurs after the delivery of the final reports. Rather, it provides the system owner or common control provider with an opportunity to address weaknesses or deficiencies that may be quickly corrected. However, in situations where limited resources exist for remediating weaknesses and deficiencies discovered during the security control assessments or privacy control assessments, organizations may decide without prejudice that waiting for the risk assessment to prioritize remediation efforts is the better course of action. 

PAGE 32 

CHAPTER THREE 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

**TABLE 4. ANALYZE ASSESSMENT REPORT RESULTS SUMMARY** 

|**Purpose**|**Analyze the risks resulting from identified weaknesses and deficiencies in controls**<br>**and determine an approach to respond to risk in accordance with organizational**<br>**priorities.**|
|---|---|
|**Primary**<br>**Roles**|System owners or common control providers, authorizing officials|
|**Supporting**<br>**Roles**|System security and privacy officers, security and privacy engineers, security and<br>privacyarchitects|
|**Outcomes**|•<br>Control assessment findings are reviewed<br>•<br>Subsequent risk responses are taken to manage risk<br>•<br>Authorization package artifacts (e.g., security and privacy plans, security and<br>privacy assessment reports, and plans of action and milestones) are updated to<br>reflect the as-implemented state of the system or common controls|



The results of control assessments ultimately influence control implementations, the content of security plans and privacy plans, and the respective plans of action and milestones. Accordingly, system owners and common control providers review the security assessment reports, privacy assessment reports, and updated risk assessment documentation and artifacts and – with the concurrence of designated organizational officials (e.g., authorizing officials, chief information officer, senior information security officer, senior agency officials for privacy/chief privacy officers, mission/information owners) – determine the appropriate steps required to respond to those weaknesses and deficiencies identified during the assessment. By using the labels of “satisfied” and “other than satisfied”, the reporting format for the assessment findings provides organizational officials with visibility into specific weaknesses and deficiencies in security or privacy controls within the system or inherited by the system and facilitates a disciplined and structured approach to responding to risks in accordance with organizational priorities. For example, system owners or common control providers in consultation with designated organizational officials may decide that certain assessment findings marked as “other than satisfied” present no significant risk to the organization and can be accepted. Conversely, system owners or common control providers may decide that certain findings marked as “other than satisfied” are significant and require remediation actions. In all cases, the organization reviews each assessment finding of “other than satisfied” and applies its judgment with regard to the severity of the finding and whether it is significant enough to warrant further investigation or remedial action.<sup>47</sup> 

Senior leadership involvement in the mitigation process may be necessary to ensure that the organization’s resources are effectively allocated in accordance with organizational priorities, provide resources first to the systems that support the most critical and sensitive missions for the organization, or correct the deficiencies that pose the greatest degree of risk. Ultimately, the assessment findings and any subsequent response actions (informed by the updated risk assessment) trigger updates to the key artifacts used by authorizing officials to determine the security and privacy risks of the system and its suitability for authorization to operate. The artifacts include security plans and privacy plans, security assessment reports and privacy assessment reports, and the respective plans of action and milestones. 

> 47 Potential risk response actions include risk acceptance, risk mitigation, risk rejection, and risk transfer/sharing. <u>[SP 800-39] provides guidance on risk response actions from a risk management perspective.</u> 

PAGE 33 

CHAPTER THREE 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

## **3.5 ASSESS SECURITY AND PRIVACY CAPABILITIES** 

In accordance with [SP 800-53], organizations may define a set of security and privacy capabilities as a precursor to the security and privacy control selection process. The concept of capability<sup>48</sup> recognizes that the protection of individuals’ privacy and information being processed by systems seldom derives from a single security or privacy safeguard or countermeasure. In most cases, such protection results from the selection and implementation of a set of mutually reinforcing security and privacy controls. Each control contributes to the overall organization-defined capability with some controls potentially contributing to a greater degree and other controls contributing to a lesser degree. For example, organizations may wish to define a capability for secure remote authentication. A secure remote authentication capability can be achieved by the implementation of a set of security controls from SP 800-53 (i.e., IA-02(01), IA-02(02), IA-02(08)], and SC-08(01)). 

Security and privacy capabilities can address a variety of areas, including technical means, physical means, procedural means, or any combination thereof. By employing the capability concept, organizations can obtain greater visibility into and a better understanding of the relationships (i.e., dependencies) among controls, the effects of specific control failures on organization-defined capabilities, and the potential severity of control weaknesses or deficiencies. However, when specific capabilities are affected by the failure of particular security and privacy controls, the capability approach may add complexity to assessments and necessitate root cause failure analysis to determine which control or controls are contributing to the failure. The greater the number of controls included in an organization-defined capability, the more difficult it may be to ascertain the root cause of failures. There may also be interactions among defined capabilities, which may contribute to the complexity of assessments. If it is found that a control is neither contributing to a defined capability nor to the overall security and privacy of the system, the organization revisits the RMF Select step, tailors the control set, and documents the rationale in the system security plan or privacy plan. 

Traditionally, assessments have been conducted on a control-by-control basis and produce results that are characterized as pass (i.e., control satisfied) or fail (i.e., control not satisfied). However, the failure of a single control or, in some cases, the failure of multiple controls may not affect the overall security and privacy capability required by an organization. This is not to say that such controls do not contribute to the security or privacy of the system and/or organization (as defined by the security requirements and privacy requirements during the initiation phase of the system development life cycle) but rather that such controls may not support the particular security or privacy capability. Furthermore, every implemented security and privacy control may not necessarily support or need to support an organization-defined capability. 

When organizations employ the concept of capabilities, automated and manual assessments account for all security and privacy controls that comprise the security and privacy capabilities. Assessors are aware of how the controls work together to provide such capabilities. In this way, 

> 48 A security capability or privacy capability is a combination of mutually reinforcing security controls or privacy controls (i.e., safeguards and countermeasures) implemented by technical means (i.e., functionality in hardware, software, and firmware), physical means (i.e., physical devices and protective measures), and procedural means (i.e., procedures performed by individuals). 

PAGE 34 

CHAPTER THREE 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

when assessments identify a failure in a capability, a root cause analysis can be conducted to determine the specific control or controls that are responsible for the failure based on the established relationships among controls. Moreover, employing the broader capability construct allows organizations to assess the severity of vulnerabilities discovered in their systems and organizations and determine if the failure of a particular security control or privacy control (associated with a vulnerability) or the decision not to deploy a certain control during the initial tailoring process (RMF Select step) affects the overall capability needed for mission and business protection. For example, the failure of a security control deemed critical for a particular security capability may be assigned a higher severity rating than a failed control of lesser importance to the capability. 

Ultimately, authorization decisions (i.e., risk acceptance decisions) are made based on the degree to which the desired security and privacy capabilities have been effectively achieved and are meeting the security and privacy requirements defined by an organization. Risk-based decisions are directly related to organizational risk tolerance that is defined as part of an organization’s risk management strategy. 

##### **CAPABILITY-BASED ASSESSMENTS** 

<mark>The grouping of controls into security and privacy capabilities necessitates root cause analyses to determine if the failure of a particular security or privacy capability can be traced to the failure of one or more security or privacy controls based on the established relationships among controls. The structure of the assessment procedures in this publication with the token-level decomposition and labelling of assessment objectives linked to the specific content of security and privacy controls supports such root cause analysis. Thus, assessments of security and privacy controls (defined as part of capabilities) can be tailored based on the guidance in Section 3.2.3 and [SP 800-137] to define the resource expenditures (e.g., frequency and level of effort) associated with such assessments. This additional precision in assessments is essential to supporting the continuous monitoring strategies developed by organizations</mark> and the ongoing authorization decisions of senior leaders. 

PAGE 35 

CHAPTER THREE 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

Figure 8 summarizes the security and privacy control assessment process, including the activities carried out before, during, and after the assessment. 



<!-- Start of picture text -->
Pre-Assessment Assessment Post-Assessment<br>Prepare for Security  Develop Security and  Conduct Security and<br>Analyze Assessment<br>and Privacy Control  Privacy Assessment  Privacy Control<br>Report Results<br>Assessments Plans Assessments<br>• Implement controls • Ensure assessment plan is  • Review assessor findings and<br>• No�fy key organiza�onal  appropriately tailored assess the risk of weaknesses and<br>officials of impending  • Involve senior leadership deficiencies<br>assessment • Balance schedule,  • Determine appropriate response<br>• Establish communica�ons  performance, and cost ac�ons<br>channels among stakeholders • Approve assessment plan • Develop/update Plans of Ac�on<br>• Iden�fy and allocate resources;  and Milestones<br>assemble assessment team • Update Security and Privacy<br>Approved  • Establish scope and key  Plans (and Risk Assessment)<br>Security and  milestones<br>Privacy Plans<br>• Assemble ar�facts for<br>assessment 1.Initial draft report Updated<br>Assessment  2.Final report with  Assessment  Plans of Ac�on  Security and<br>Plan(s) organizational  Report(s) and Milestones Privacy Plans<br>annotations<br>Authorization Package<br>• Establish organiza�onal points<br>of contact • Implement assessment plan(s) • Consult with organiza�onal<br>• Understand organiza�on’s  • Develop assessment plan based  • Execute assessment  officials regarding control<br>mission, func�ons, and  on security and privacy plans procedures to achieve  effec�veness<br>business processes • Select assessment methods  assessment objec�ves<br>• Understand system  and objects • Produce assessment findings<br>structure/architecture • Tailor procedures for  • Recommend specific<br>• Understand selected controls  organiza�on and system remedia�on ac�ons<br>for assessment and relevant  • Iden�fy schedule and milestones • Produce ini�al (dra�) and final<br>NIST standards and guidelines • Obtain ar�facts for assessment assessment report(s)<br>Organiza�on<br>Assessor /<br>Assessment Team<br><!-- End of picture text -->

**FIGURE 8:  SECURITY AND PRIVACY CONTROL ASSESSMENT PROCESS OVERVIEW** 

PAGE 36 

CHAPTER THREE 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

### **CHAPTER FOUR** 

# **SECURITY AND PRIVACY ASSESSMENT PROCEDURES** 

OBJECTIVES, METHODS, AND OBJECTS FOR ASSESSING SECURITY AND PRIVACY CONTROLS 

This chapter provides a catalog of procedures to assess the security and privacy controls and control enhancements in [SP 800-53].<sup>49</sup> Assessors select assessment procedures from the catalog in accordance with the guidance provided in Section 3.2. Since the contents of the security and privacy plan are the basis for the development of the security and privacy assessment plans and the assessments, there will likely be assessment procedures in the catalog not used by assessors because the associated security and privacy controls or control enhancements are not contained in the security and privacy plan for the system,<sup>50</sup> or the security and privacy controls or control enhancements are not being assessed at this time. 

##### **SP 800-53A REVISION 5, ASSESSMENT PROCEDURE SCHEMA** 

<u><mark>Section 2.4</mark></u> <mark>provides an overview of the assessment procedures, including the naming and numbering convention, assessment objectives, determination statements, potential assessment methods, and objects.</mark> 

<u><mark>Appendix C</mark></u> <mark>provides definitions of the assessment methods, applicable objects, and additional</mark> information on assessment attributes of depth and coverage. 

The same assessment object may appear in multiple assessment object lists in a variety of assessment procedures. The same object may be used in multiple contexts to obtain needed information or evidence for a particular aspect of an assessment. Assessors use the general references as appropriate to obtain the necessary information to make the specified determinations required by the assessment objective. For example, a reference to access control policy appears in the assessment procedures for AC-02 and AC-07. For assessment procedure AC-02, assessors use the access control policy to find information about that portion of the policy that addresses account management for the system. For assessment procedure AC07, assessors use the access control policy to find information about that portion of the policy that addresses unsuccessful login attempts for the system. 

Assessors are responsible for combining and consolidating the assessment procedures whenever possible or practical. Optimizing assessment procedures can save time, reduce assessment costs, and maximize the usefulness of assessment results. Assessors optimize assessment procedures by determining the best sequencing of the procedures. The assessment 

> 49 [SP 800-53] remains the definitive expression of the control or enhancement in the event of any differences between the assessment objectives identified for assessing the security and privacy controls and the underlying intent expressed by the security and privacy control statements defined in the most recent version of SP 800-53. 

> 50 The execution of the RMF includes the selection of an initial set of security and privacy controls employed within or inherited by an organizational system followed by a control tailoring process. The tailoring process often changes the set of security and privacy controls contained in the final security plan and privacy program plan. Therefore, the selection of assessment procedures from the catalog of available procedures is based solely on the content of the plan(s) after the tailoring activities are completed. 

CHAPTER FOUR 

PAGE 37 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

of some security and privacy controls before others may provide information that facilitates understanding and assessment of other controls.<sup>51</sup> 

The assessment procedures are published in multiple data formats, including comma-separated values (CSV), plain text, and Open Security Controls Assessment (OSCAL). The available data formats are accessible from on the NIST SP 800-53A Revision 5, publication details page at <u>https://csrc.nist.gov/publications/detail/sp/800-53A/rev-5. The OSCAL Content Git Repository is</u> available at <u>https://github.com/usnistgov/oscal-content.</u> 

##### **CAUTIONARY NOTE** 

<mark>Whereas a set of</mark> **_<mark>potential assessment methods</mark>_** <mark>are included in the following catalog of assessment procedures, the potential assessment methods are not intended to be mandatory or exclusive. Depending on the particular circumstances of the system or organization to be assessed, not all methods may be required, or other assessment methods may also be used. In addition, the set of</mark> **_<mark>potential assessment objects</mark>_** <mark>listed in the catalog are not intended to be mandatory but rather a set from which the necessary and sufficient set of objects for a given assessment can be selected to make the appropriate determinations. Organizational assurance requirements and other risk management-related factors (e.g., system categorization, organizational risk tolerance) are primary drivers for determining the appropriate</mark> assessment methods and objects for a given assessment. 

> 51 For additional information on optimizing assessment procedures, refer to <u>Section 3.2.5.</u> 

CHAPTER FOUR 

PAGE 38 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

##### **IMPLEMENTATION TIPS** 

**<mark>TIP #1:</mark>** <mark>Select only those assessment procedures from Chapter 4 that correspond to the controls and control enhancements in the approved system security plan and privacy plan to be included in the</mark> assessment. 

**<mark>TIP #2:</mark>** <mark>The assessment procedures selected from Chapter 4 are example procedures that serve as a starting point for organizations preparing for assessments. These assessment procedures are tailored as necessary by the assessors in accordance with the guidance in Section 3.2.3 to adapt to specific</mark> organizational requirements and operating environments. 

**<mark>TIP #3:</mark>** <mark>With respect to the assessment procedures in Chapter 4, assessors need only apply those procedures, methods, and objects necessary for making a final determination that a particular security</mark> control requirement is “satisfied” or “not satisfied” (see <u>Section 3.3).</u> 

**<mark>TIP #4:</mark>** <mark>To each assessment method, assessors apply values for depth and coverage (described in</mark> <u><mark>Appendix C) that are commensurate with the characteristics of the system (including assurance</mark></u> <mark>requirements) and the specific assessment activity that supports making a determination of the effectiveness of the security controls under review. The values selected for the depth and coverage attributes indicate the relative effort required in applying an assessment method to an assessment object (i.e., the rigor and scope of the activities associated with the assessment). The depth and coverage attributes, while not repeated in every assessment procedure in this appendix, can be represented as</mark> follows: 

**<mark>Interview:</mark>** <mark>[assign attribute values: <depth>, <coverage>]. [SELECT FROM: Organizational personnel with contingency planning and plan implementation</mark> responsibilities]. 

**<mark>TIP #5:</mark>** <mark>Assessors may find useful assessment-related information in the Discussion and Related Controls section of each control described in [SP 800-53]. Information from the discussion about related controls can be used to carry out more effective assessments with regard to the application of assessment</mark> procedures and the reuse of assessment artifacts. 

**<mark>TIP #6:</mark>** <mark>For controls with ODPs, the ODP values are defined during the RMF Select step and updated as necessary during the RMF Implement and Monitor steps. If ODP values are not defined and implemented,</mark> control effectiveness cannot be verified, resulting in an “other than satisfied” finding. 

**<mark>TIP #7:</mark>** <mark>Organizations may refer to this publication or the derivative data formats to easily identify all of the control parameters whose values to define. The ODP definitions are highlighted within the assessment procedure listing and can be filtered using keyword</mark> _<mark>“_ODP</mark>_ <mark>” or “</mark> _<mark>XX-nn_ODP</mark>_ <mark>” (where</mark> _<mark>XX</mark>_ <mark>is the two-</mark> character control family abbreviation, and _nn_ is the control number). 

**<mark>Note:</mark>** <mark>When assessing agency compliance with NIST guidance, auditors, Inspectors General, evaluators, and/or assessors consider the intent of the security and privacy concepts and principles articulated within the particular guidance document and how the agency applied the guidance in the context of its specific mission responsibilities,</mark> operational environments, and unique organizational conditions. 

CHAPTER FOUR 

PAGE 39 

NIST SP 800-53A, REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

## **4.1 ACCESS CONTROL** 

|**AC-01**<br>**POLICY AND PRO**|**CEDURES**|
|---|---|
|**ASSESSMENT OBJ**<br>_Determine if:_|**ECTIVE:**|
|**AC-01_ODP[01]**<br>**AC-01_ODP[02]**|**_personnel or roles to whom the access control policy is to be disseminated is/are_**<br>**_defined;_**<br>**_personnel or roles to whom the access control procedures are to be disseminated_**<br>**_is/are defined;_**|
|**AC-01_ODP[03]**|**_one or more of the following PARAMETER VALUES is/are selected: {organizaon-_**<br>**_level; mission/business process-level; system-level};_**|
|**AC-01_ODP[04]**|**_an official to manage the access control policy and procedures is defined;_**|
|**AC-01_ODP[05]**|**_the frequency at which the current access control policy is reviewed and updated_**<br>**_is defined;_**|
|**AC-01_ODP[06]**|**_events that would require the current access control policy to be reviewed and_**<br>**_updated are defined;_**|
|**AC-01_ODP[07]**|**_the frequency at which the current access control procedures are reviewed and_**<br>**_updated is defined;_**|
|**AC-01_ODP[08]**|**_events that would require procedures to be reviewed and updated are defined;_**|
|**AC-01a.[01]**|an access control policy is developed and documented;|
|**AC-01a.[02]**|the access control policy is disseminated to**_<AC-01_ODP[01] personnel or roles>_**;|
|**AC-01a.[03]**|access control procedures to facilitate the implementaon of the access control<br>policy and associated controls are developed and documented;|
|**AC-01a.[04]**|the access control procedures are disseminated to**_<AC-01_ODP[02] personnel or_**<br>**_roles>_**;|
|**AC-01a.01(a)[01]**|the**_<AC-01_ODP[03] SELECTED PARAMETER VALUE(S)>_**access control policy<br>addresses purpose;|
|**AC-01a.01(a)[02]**|the**_<AC-01_ODP[03] SELECTED PARAMETER VALUE(S)>_**access control policy<br>addresses scope;|
|**AC-01a.01(a)[03]**|the**_<AC-01_ODP[03] SELECTED PARAMETER VALUE(S)>_**access control policy<br>addresses roles;|
|**AC-01a.01(a)[04]**|the**_<AC-01_ODP[03] SELECTED PARAMETER VALUE(S)>_**access control policy<br>addresses responsibilies;|
|**AC-01a.01(a)[05]**|the**_<AC-01_ODP[03] SELECTED PARAMETER VALUE(S)>_**access control policy<br>addresses management commitment;|
|**AC-01a.01(a)[06]**|the**_<AC-01_ODP[03] SELECTED PARAMETER VALUE(S)>_**access control policy<br>addresses coordinaon among organizaonal enes;|
|**AC-01a.01(a)[07]**|the**_<AC-01_ODP[03] SELECTED PARAMETER VALUE(S)>_**access control policy<br>addresses compliance;|



_Reference produced from open data_ hps://github.com/usnistgov/oscal-content 

CHAPTER FOUR 

PAGE 40 

NIST SP 800-53A, REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

|**AC-01**<br>**POLICY AND PRO**|**CEDURES**|
|---|---|
|**AC-01a.01(b)**|the**_<AC-01_ODP[03] SELECTED PARAMETER VALUE(S)>_**access control policy is<br>consistent with applicable laws, Execuve Orders, direcves, regulaons, policies,<br>standards, and guidelines;|
|**AC-01b.**|the**_<AC-01_ODP[04] official>_**is designated to manage the development,<br>documentaon, and disseminaon of the access control policy and procedures;|
|**AC-01c.01[01]**|the current access control policy is reviewed and updated**_<AC-01_ODP[05]_**<br>**_frequency>_**;|
|**AC-01c.01[02]**|the current access control policy is reviewed and updated following<br>**_<AC-01_ODP[06] events>_**;|
|**AC-01c.02[01]**|the current access control procedures are reviewed and updated**_<AC-01_ODP[07]_**<br>**_frequency>_**;|
|**AC-01c.02[02]**|the current access control procedures are reviewed and updated following<br>**_<AC-01_ODP[08] events>_**.|
|**POTENTIAL ASSE**|**SSMENT METHODS AND OBJECTS:**|
|**AC-01-Examine**|[SELECT FROM: Access control policy and procedures; system security plan; privacy<br>plan; other relevant documents or records].|
|**AC-01-Interview**|[SELECT FROM: Organizaonal personnel with access control responsibilies;<br>organizaonal personnel with informaon security with informaon security and<br>privacy responsibilies].|



|**AC-02**|**ACCOUNT MANA**|**GEMENT**|
|---|---|---|
||**ASSESSMENT OB**<br>_Determine if:_|**JECTIVE:**|
||**AC-02_ODP[01]**|**_prerequisites and criteria for group and role membership are defined;_**|
||**AC-02_ODP[02]**|**_aributes (as required) for each account are defined;_**|
||**AC-02_ODP[03]**|**_personnel or roles required to approve requests to create accounts is/are defined;_**|
||**AC-02_ODP[04]**<br>**AC-02_ODP[05]**|**_policy, procedures, prerequisites, and criteria for account creaon, enabling,_**<br>**_modificaon, disabling, and removal are defined;_**<br>**_personnel or roles to be nofied is/are defined;_**|
||**AC-02_ODP[06]**<br>**AC-02_ODP[07]**|**_me period within which to nofy account managers when accounts are no_**<br>**_longer required is defined;_**<br>**_me period within which to nofy account managers when users are terminated_**<br>**_or transferred is defined;_**|
||**AC-02_ODP[08]**|**_me period within which to nofy account managers when system usage or the_**<br>**_need to know changes for an individual is defined;_**|
||**AC-02_ODP[09]**|**_aributes needed to authorize system access (as required) are defined;_**|
||**AC-02_ODP[10]**|**_the frequency of account review is defined;_**|
||**AC-02a.[01]**|account types allowed for use within the system are defined and documented;|



_Reference produced from open data_ hps://github.com/usnistgov/oscal-content 

CHAPTER FOUR 

PAGE 41 

NIST SP 800-53A, REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

|**AC-02**<br>**ACCOUNT MAN**|**AGEMENT**<br>i        i|
|---|---|
|**AC-02a.[02]**|account types specifically prohibited for use within the system are defined and<br>documented;|
|**AC-02b.**|account managers are assigned;|
|**AC-02c.**|**_<AC-02_ODP[01] prerequisites and criteria>_**for group and role membership are<br>required;|
|**AC-02d.01**|authorized users of the system are specified;|
|**AC-02d.02**|group and role membership are specified;|
|**AC-02d.03[01]**|access authorizaons (i.e., privileges) are specified for each account;|
|**AC-02d.03[02]**|**_<AC-02_ODP[02] aributes (as required)>_**are specified for each account;|
|**AC-02e.**|approvals are required by**_<AC-02_ODP[03] personnel or roles>_**for requests to<br>create accounts;|
|**AC-02f.[01]**|accounts are created in accordance with**_<AC-02_ODP[04] policy, procedures,_**<br>**_prerequisites, and criteria>_**;|
|**AC-02f.[02]**|accounts are enabled in accordance with**_<AC-02_ODP[04] policy, procedures,_**<br>**_prerequisites, and criteria>_**;|
|**AC-02f.[03]**|accounts are modified in accordance with**_<AC-02_ODP[04] policy, procedures,_**<br>**_prerequisites, and criteria>_**;|
|**AC-02f.[04]**|accounts are disabled in accordance with**_<AC-02_ODP[04] policy, procedures,_**<br>**_prerequisites, and criteria>_**;|
|**AC-02f.[05]**|accounts are removed in accordance with**_<AC-02_ODP[04] policy, procedures,_**<br>**_prerequisites, and criteria>_**;|
|**AC-02g.**|the use of accounts is monitored;|
|**AC-02h.01**|account managers and**_<AC-02_ODP[05] personnel or roles>_**are nofied within<br>**_<AC-02_ODP[06] me period>_**when accounts are no longer required;|
|**AC-02h.02**|account managers and**_<AC-02_ODP[05] personnel or roles>_**are nofied within<br>**_<AC-02_ODP[07] me period>_**when users are terminated or transferred;|
|**AC-02h.03**|account managers and**_<AC-02_ODP[05] personnel or roles>_**are nofied within<br>**_<AC-02_ODP[08] me period>_**when system usage or the need to know changes<br>for an individual;|
|**AC-02i.01**|access to the system is authorized based on a valid access authorizaon;|
|**AC-02i.02**|access to the system is authorized based on intended system usage;|
|**AC-02i.03**|access to the system is authorized based on**_<AC-02_ODP[09] aributes (as_**<br>**_required)>_**;|
|**AC-02j.**|accounts are reviewed for compliance with account management requirements<br>**_<AC-02_ODP[10] frequency>_**;|
|**AC-02k.[01]**|a process is established for changing shared or group account authencators (if<br>deployed) when individuals are removed from the group;|
|**AC-02k.[02]**|a process is implemented for changing shared or group account authencators (if<br>deployed) when individuals are removed from the group;|
|**AC-02l.[01]**|account management processes are aligned with personnel terminaon processes;|



_Reference produced from open data_ hps://github.com/usnistgov/oscal-content 

CHAPTER FOUR 

PAGE 42 

NIST SP 800-53A, REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

|**AC-02**|**ACCOUNT MANA**<br>|**GEMENT**<br>|
|---|---|---|
||**AC-02l.[02]**|account management processes are aligned with personnel transfer processes.|
||**POTENTIAL ASSES**<br>**AC-02-Examine**|**SMENT METHODS AND OBJECTS:**<br>[SELECT FROM: Access control policy; personnel terminaon policy and procedure;<br>personnel transfer policy and procedure; procedures for addressing account<br>management; system design documentaon; system configuraon sengs and<br>associated documentaon; list of acve system accounts along with the name<br>of the individual associated with each account; list of recently disabled system<br>accounts and the name of the individual associated with each account; list of<br>condions for group and role membership; noficaons of recent transfers,<br>separaons, or terminaons of employees; access authorizaon records; account<br>management compliance reviews; system monitoring records; system audit<br>records; system security plan; privacy plan; other relevant documents or records].|
||**AC-02-Interview**|[SELECT FROM: Organizaonal personnel with account management<br>responsibilies; system/network administrators; organizaonal personnel with<br>informaon security with informaon security and privacy responsibilies].|
||**AC-02-Test**|[SELECT FROM: Organizaonal processes for account management on the system;<br>mechanisms for implemenng account management].|



|**AC-02(01)**|**ACCOUNT MANAG**<br>**ASSESSMENT OBJE**<br>_Determine if:_<br>**AC-02(01)_ODP**|**EMENT | AUTOMATED SYSTEM ACCOUNT MANAGEMENT**<br>**CTIVE:**<br>**_automated mechanisms used to support the management of system accounts are_**<br>**_defined;_**|
|---|---|---|
||**AC-02(01)**<br>**POTENTIAL ASSESS**<br>**AC-02(01)-Examine**|the management of system accounts is supported using**_<AC-02(01)_ODP_**<br>**_automated mechanisms>_**.<br>**MENT METHODS AND OBJECTS:**<br>[SELECT FROM: Access control policy; procedures for addressing account<br>management; system design documentaon; system configuraon sengs and<br>associated documentaon; system audit records; system security plan; other<br>relevant documents or records].|
||**AC-02(01)-Interview**|[SELECT FROM: Organizaonal personnel with account management<br>responsibilies; system/network administrators; organizaonal personnel with<br>informaon security with informaon security responsibilies; system developers].|
||**AC-02(01)-Test**|[SELECT FROM: Automated mechanisms for implemenng account management<br>funcons].|



|**AC-02(02)**|**ACCOUNT MANAGEMENT | AUTOMATED TEMPORARY AND EMERGENCY ACCOUNT**<br>**MANAGEMENT**|
|---|---|
||**ASSESSMENT OBJECTIVE:**<br>_Determine if:_|
||**AC-02(02)_ODP[01]**<br>**_one of the following PARAMETER VALUES is selected: {remove; disable};_**|



_Reference produced from open data_ hps://github.com/usnistgov/oscal-content 

CHAPTER FOUR 

PAGE 43 

NIST SP 800-53A, REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

|**AC-02(02)**|**ACCOUNT MANAG**<br>**MANAGEMENT**|**EMENT | AUTOMATED TEMPORARY AND EMERGENCY ACCOUNT**|
|---|---|---|
||**AC-02(02)_ODP[02]**|**_the me period aer which to automacally remove or disable temporary or_**<br>**_emergency accounts is defined;_**|
||**AC-02(02)**<br>**POTENTIAL ASSESS**<br>**AC-02(02)-Examine**|temporary and emergency accounts are automacally**_<AC-02(02)_ODP[01]_**<br>**_SELECTED PARAMETER VALUE>_**aer**_<AC-02(02)_ODP[02] me period>_**.<br>**MENT METHODS AND OBJECTS:**<br>[SELECT FROM: Access control policy; procedures for addressing account<br>management; system design documentaon; system configuraon sengs and<br>associated documentaon; system-generated list of temporary accounts removed<br>and/or disabled; system-generated list of emergency accounts removed and/or<br>disabled; system audit records; system security plan; other relevant documents or<br>records].|
||**AC-02(02)-Interview**|[SELECT FROM: Organizaonal personnel with account management<br>responsibilies; system/network administrators; organizaonal personnel with<br>informaon security with informaon security responsibilies; system developers].|
||**AC-02(02)-Test**|[SELECT FROM: Automated mechanisms for implemenng account management<br>funcons].|



|**AC-02(03)**|**ACCOUNT MANAG**<br>**ASSESSMENT OBJE**<br>_Determine if:_<br>**AC-02(03)_ODP[01]**<br>**AC-02(03)_ODP[02]**|**EMENT | DISABLE ACCOUNTS**<br>**CTIVE:**<br>**_me period within which to disable accounts is defined;_**<br>**_me period for account inacvity before disabling is defined;_**|
|---|---|---|
||**AC-02(03)(a)**|accounts are disabled within**_<AC-02(03)_ODP[01] me period>_**when the accounts<br>have expired;|
||**AC-02(03)(b)**|accounts are disabled within**_<AC-02(03)_ODP[01] me period>_**when the accounts<br>are no longer associated with a user or individual;|
||**AC-02(03)(c)**|accounts are disabled within**_<AC-02(03)_ODP[01] me period>_**when the accounts<br>are in violaon of organizaonal policy;|
||**AC-02(03)(d)**<br>**POTENTIAL ASSESS**<br>|accounts are disabled within**_<AC-02(03)_ODP[01] me period>_**when the accounts<br>have been inacve for**_<AC-02(03)_ODP[02] me period>_**.<br>**MENT METHODS AND OBJECTS:**<br>|
||**AC-02(03)-Examine**|[SELECT FROM: Access control policy; procedures for addressing account<br>management; system security plan; system design documentaon; system<br>configuraon sengs and associated documentaon; system-generated list of<br>accounts removed; system-generated list of emergency accounts disabled; system<br>audit records; system security plan; other relevant documents or records].|
||**AC-02(03)-Interview**|[SELECT FROM: Organizaonal personnel with account management<br>responsibilies; system/network administrators; organizaonal personnel with<br>informaon security responsibilies; system developers].|
||**AC-02(03)-Test**|[SELECT FROM: Mechanisms for implemenng account management funcons].|



_Reference produced from open data_ hps://github.com/usnistgov/oscal-content 

CHAPTER FOUR 

PAGE 44 

NIST SP 800-53A, REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

|**AC-02(04)**|**ACCOUNT MANAG**<br>**ASSESSMENT OBJE**<br>_Determine if:_|**EMENT | AUTOMATED AUDIT ACTIONS**<br>**CTIVE:**|
|---|---|---|
||**AC-02(04)[01]**|account creaon is automacally audited;|
||**AC-02(04)[02]**|account modificaon is automacally audited;|
||**AC-02(04)[03]**|account enabling is automacally audited;|
||**AC-02(04)[04]**|account disabling is automacally audited;|
||**AC-02(04)[05]**|account removal acons are automacally audited.|
||**POTENTIAL ASSESS**|**MENT METHODS AND OBJECTS:**|
||**AC-02(04)-Examine**|[SELECT FROM: Access control policy; procedures addressing account management;<br>system design documentaon; system configuraon sengs and associated<br>documentaon; noficaons/alerts of account creaon, modificaon, enabling,<br>disabling, and removal acons; system audit records; system security plan; other<br>relevant documents or records].|
||**AC-02(04)-Interview**|[SELECT FROM: Organizaonal personnel with account management<br>responsibilies; system/network administrators; organizaonal personnel with<br>informaon security responsibilies].|
||**AC-02(04)-Test**|[SELECT FROM: Automated mechanisms implemenng account management<br>funcons].|



|**AC-02(05)**|**ACCOUNT MANAG**<br>**ASSESSMENT OBJE**<br>_Determine if:_|**EMENT | INACTIVITY LOGOUT**<br>**CTIVE:**|
|---|---|---|
||**AC-02(05)_ODP**|**_the me period of expected inacvity or descripon of when to log out is defined;_**|
||**AC-02(05)**|users are required to log out when**_<AC-02(05)_ODP me period of expected_**<br>**_inacvity or descripon of when to log out>_**.|
||**POTENTIAL ASSESS**|**MENT METHODS AND OBJECTS:**|
||**AC-02(05)-Examine**|[SELECT FROM: Access control policy; procedures addressing account management;<br>system design documentaon; system configuraon sengs and associated<br>documentaon; security violaon reports; system audit records; system security<br>plan; other relevant documents or records].|
||**AC-02(05)-Interview**|[SELECT FROM: Organizaonal personnel with account management<br>responsibilies; system/network administrators; organizaonal personnel with<br>informaon security responsibilies; users that must comply with inacvity logout<br>policy].|



_Reference produced from open data_ hps://github.com/usnistgov/oscal-content 

CHAPTER FOUR 

PAGE 45 

NIST SP 800-53A, REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

|**AC-02(06)**|**ACCOUNT MANAG**<br>**ASSESSMENT OBJE**<br>_Determine if:_<br>**AC-02(06)_ODP**|**EMENT | DYNAMIC PRIVILEGE MANAGEMENT**<br>**CTIVE:**<br>**_dynamic privilege management capabilies are defined;_**|
|---|---|---|
||**AC-02(06)**|**_<AC-02(06)_ODP dynamic privilege management capabilies>_**are implemented.|
||**POTENTIAL ASSESS**|**MENT METHODS AND OBJECTS:**|
||**AC-02(06)-Examine**|[SELECT FROM: Access control policy; procedures addressing account management;<br>system design documentaon; system configuraon sengs and associated<br>documentaon; system-generated list of dynamic privilege management<br>capabilies; system audit records; system security plan; other relevant documents<br>or records].|
||**AC-02(06)-Interview**|[SELECT FROM: Organizaonal personnel with account management<br>responsibilies; system/network administrators; organizaonal personnel with<br>informaon security responsibilies; system developers].|
||**AC-02(06)-Test**|[SELECT FROM: system or mechanisms implemenng dynamic privilege<br>management capabilies].|



|**AC-02(07)**|**ACCOUNT MANAG**<br>**ASSESSMENT OBJE**<br>_Determine if:_<br>**AC-02(07)_ODP**|**EMENT | PRIVILEGED USER ACCOUNTS**<br>**CTIVE:**<br>**_one of the following PARAMETER VALUES is selected: {a role-based access_**<br>**_scheme; an aribute-based access scheme};_**|
|---|---|---|
||**AC-02(07)(a)**|privileged user accounts are established and administered in accordance with<br>**_<AC-02(07)_ODP SELECTED PARAMETER VALUE>_**;|
||**AC-02(07)(b)**|privileged role or aribute assignments are monitored;|
||**AC-02(07)(c)**|changes to roles or aributes are monitored;|
||**AC-02(07)(d)**|access is revoked when privileged role or aribute assignments are no longer<br>appropriate.|
||**POTENTIAL ASSESS**<br>|**MENT METHODS AND OBJECTS:**<br>|
||**AC-02(07)-Examine**|[SELECT FROM: Access control policy; procedures addressing account management;<br>system design documentaon; system configuraon sengs and associated<br>documentaon; system-generated list of privileged user accounts and associated<br>roles; records of acons taken when privileged role assignments are no longer<br>appropriate; system audit records; audit tracking and monitoring reports; system<br>monitoring records; system security plan; other relevant documents or records].|
||**AC-02(07)-Interview**|[SELECT FROM: Organizaonal personnel with account management<br>responsibilies; system/network administrators; organizaonal personnel with<br>informaon security responsibilies].|
||**AC-02(07)-Test**|[SELECT FROM: Mechanisms implemenng account management funcons;<br>mechanisms monitoring privileged role assignments].|



_Reference produced from open data_ hps://github.com/usnistgov/oscal-content 

CHAPTER FOUR 

PAGE 46 

NIST SP 800-53A, REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

|**AC-02(08)**|**ACCOUNT MANAG**|**EMENT | DYNAMIC ACCOUNT MANAGEMENT**|
|---|---|---|
||**ASSESSMENT OBJE**<br>_Determine if:_|**CTIVE:**|
||**AC-02(08)_ODP**|**_system accounts that are dynamically created, acvated, managed, and_**<br>**_deacvated are defined;_**|
||**AC-02(08)[01]**|**_<AC-02(08)_ODP system accounts>_**are created dynamically;|
||**AC-02(08)[02]**|**_<AC-02(08)_ODP system accounts>_**are acvated dynamically;|
||**AC-02(08)[03]**|**_<AC-02(08)_ODP system accounts>_**are managed dynamically;|
||**AC-02(08)[04]**|**_<AC-02(08)_ODP system accounts>_**are deacvated dynamically.|
||**POTENTIAL ASSESS**|**MENT METHODS AND OBJECTS:**|
||**AC-02(08)-Examine**|[SELECT FROM: Access control policy; procedures addressing account management;<br>system design documentaon; system configuraon sengs and associated<br>documentaon; system-generated list of system accounts; system audit records;<br>system security plan; other relevant documents or records].|
||**AC-02(08)-Interview**|[SELECT FROM: Organizaonal personnel with account management<br>responsibilies; system/network administrators; organizaonal personnel with<br>informaon security responsibilies; system developers].|
||**AC-02(08)-Test**|[SELECT FROM: Automated mechanisms implemenng account management<br>funcons].|



|**AC-02(09)**|**ACCOUNT MANAG**|**EMENT | RESTRICTIONS ON USE OF SHARED AND GROUP ACCOUNTS**|
|---|---|---|
||**ASSESSMENT OBJE**<br>_Determine if:_|**CTIVE:**|
||**AC-02(09)_ODP**|**_condions for establishing shared and group accounts are defined;_**|
||**AC-02(09)**|the use of shared and group accounts is only permied if**_<AC-02(09)_ODP_**<br>**_condions>_**are met.|
||**POTENTIAL ASSESS**|**MENT METHODS AND OBJECTS:**|
||**AC-02(09)-Examine**|[SELECT FROM: Access control policy; procedures addressing account management;<br>system design documentaon; system configuraon sengs and associated<br>documentaon; system-generated list of shared/group accounts and associated<br>roles; system audit records; system security plan; other relevant documents or<br>records].|
||**AC-02(09)-Interview**|[SELECT FROM: Organizaonal personnel with account management<br>responsibilies; system/network administrators; organizaonal personnel with<br>informaon security responsibilies].|
||**AC-02(09)-Test**|[SELECT FROM: Mechanisms implemenng management of shared/group<br>accounts].|



_Reference produced from open data_ hps://github.com/usnistgov/oscal-content 

CHAPTER FOUR 

PAGE 47 

NIST SP 800-53A, REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

|**AC-02(10)**|**ACCOUNT MANAGEMENT | SHARED AND GROUP ACCOUNT CREDENTIAL CHANGE**|
|---|---|



[WITHDRAWN: Incorporated into AC-2k.] 

|**AC-02(11)**|**ACCOUNT MANAG**|**EMENT | USAGE CONDITIONS**|
|---|---|---|
||**ASSESSMENT OBJE**<br>_Determine if:_|**CTIVE:**|
||**AC-02(11)_ODP[01]**<br>**AC-02(11)_ODP[02]**|**_circumstances and/or usage condions to be enforced for system accounts are_**<br>**_defined;_**<br>**_system accounts subject to enforcement of circumstances and/or usage_**<br>**_condions are defined;_**|
||**AC-02(11)**|**_<AC-02(11)_ODP[01] circumstances and/or usage condions>_**for<br>**_<AC-02(11)_ODP[02] system accounts>_**are enforced.|
||**POTENTIAL ASSESS**|**MENT METHODS AND OBJECTS:**|
||**AC-02(11)-Examine**|[SELECT FROM: Access control policy; procedures addressing account management;<br>system design documentaon; system configuraon sengs and associated<br>documentaon; system-generated list of system accounts and associated<br>assignments of usage circumstances and/or usage condions; system audit records;<br>system security plan; other relevant documents or records].|
||**AC-02(11)-Interview**|[SELECT FROM: Organizaonal personnel with account management<br>responsibilies; system/network administrators; organizaonal personnel with<br>informaon security responsibilies; system developers].|
||**AC-02(11)-Test**|[SELECT FROM: Mechanisms implemenng account management funcons].|



|**AC-02(12)**|**ACCOUNT MANAG**<br>**ASSESSMENT OBJE**<br>_Determine if:_<br>**AC-02(12)_ODP[01]**<br>**AC-02(12)_ODP[02]**|**EMENT | ACCOUNT MONITORING FOR ATYPICAL USAGE**<br>**CTIVE:**<br>**_atypical usage for which to monitor system accounts is defined;_**<br>**_personnel or roles to report atypical usage is/are defined;_**|
|---|---|---|
||**AC-02(12)(a)**|system accounts are monitored for**_<AC-02(12)_ODP[01] atypical usage>_**;|
||**AC-02(12)(b)**<br>**POTENTIAL ASSESS**|atypical usage of system accounts is reported to**_<AC-02(12)_ODP[02] personnel or_**<br>**_roles>_**.<br>**MENT METHODS AND OBJECTS:**|
||**AC-02(12)-Examine**|[SELECT FROM: Access control policy; procedures addressing account management;<br>system design documentaon; system configuraon sengs and associated<br>documentaon; system monitoring records; system audit records; audit tracking<br>and monitoring reports; privacy impact assessment; system security plan; privacy<br>plan; other relevant documents or records].|
||**AC-02(12)-Interview**|[SELECT FROM: Organizaonal personnel with account management<br>responsibilies; system/network administrators; organizaonal personnel with<br>informaon security responsibilies].|



_Reference produced from open data_ hps://github.com/usnistgov/oscal-content 

CHAPTER FOUR 

PAGE 48 

NIST SP 800-53A, REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

|**AC-02(12)**|**ACCOUNT MANAGEMENT | ACCOUNT MONITORING FOR ATYPICAL USAGE**|
|---|---|
||**AC-02(12)-Test**<br>[SELECT FROM: Mechanisms implemenng account management funcons].|



|**AC-02(13)**|**ACCOUNT MANAG**|**EMENT | DISABLE ACCOUNTS FOR HIGH-RISK INDIVIDUALS**|
|---|---|---|
||**ASSESSMENT OBJE**<br>_Determine if:_|**CTIVE:**|
||**AC-02(13)_ODP[01]**|**_me period within which to disable accounts of individuals who are discovered to_**<br>**_pose significant risk is defined;_**|
||**AC-02(13)_ODP[02]**|**_significant risks leading to disabling accounts are defined;_**|
||**AC-02(13)**|accounts of individuals are disabled within**_<AC-02(13)_ODP[01] me period>_**of<br>discovery of**_<AC-02(13)_ODP[02] significant risks>_**.|
||**POTENTIAL ASSESS**|**MENT METHODS AND OBJECTS:**|
||**AC-02(13)-Examine**|[SELECT FROM: Access control policy; procedures addressing account management;<br>system design documentaon; system configuraon sengs and associated<br>documentaon; system-generated list of disabled accounts; list of user acvies<br>posing significant organizaonal risk; system audit records; system security plan;<br>other relevant documents or records].|
||**AC-02(13)-Interview**|[SELECT FROM: Organizaonal personnel with account management<br>responsibilies; system/network administrators; organizaonal personnel with<br>informaon security responsibilies].|
||**AC-02(13)-Test**|[SELECT FROM: Mechanisms implemenng account management funcons].|



|**AC-03**|**ACCESS ENFORCE**|**MENT**|
|---|---|---|
||**ASSESSMENT OB**<br>_Determine if:_<br>|**JECTIVE:**<br>|
||**AC-03**<br>**POTENTIAL ASSE**|approved authorizaons for logical access to informaon and system resources are<br>enforced in accordance with applicable access control policies.<br>**SSMENT METHODS AND OBJECTS:**|
||**AC-03-Examine**|[SELECT FROM: Access control policy; procedures addressing access enforcement;<br>system design documentaon; system configuraon sengs and associated<br>documentaon; list of approved authorizaons (user privileges); system audit<br>records; system security plan; privacy plan; other relevant documents or records].|
||**AC-03-Interview**|[SELECT FROM: Organizaonal personnel with access enforcement responsibilies;<br>system/network administrators; organizaonal personnel with informaon security<br>and privacy responsibilies; system developers].|
||**AC-03-Test**|[SELECT FROM: Mechanisms implemenng access control policy].|



_Reference produced from open data_ hps://github.com/usnistgov/oscal-content 

CHAPTER FOUR 

PAGE 49 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

### **APPENDIX C** 

# **ASSESSMENT METHOD DESCRIPTIONS** 

ASSESSMENT METHOD DEFINITIONS, APPLICABLE OBJECTS, AND ATTRIBUTES 

This appendix defines the three assessment methods that can be used by assessors during security and privacy control assessments: 

1. Examine 

2. Interview 

3. Test 

Included in the definition of each assessment method are types of objects to which the method can be applied. The application of each method is described in terms of the attributes of depth and coverage, progressing from basic to focused to comprehensive. The attribute values correlate to the assurance requirements specified by the organization. 

The depth attribute addresses the rigor and level of detail of the assessment. For the depth attribute, the focused attribute value includes and builds upon the assessment rigor and level of detail defined for the basic attribute value. The comprehensive attribute value includes and builds upon the assessment rigor and level of detail defined for the focused attribute value. 

The coverage attribute addresses the scope or breadth of the assessment. For the coverage attribute, the focused attribute value includes and builds upon the number and type of assessment objects defined for the basic attribute value. The comprehensive attribute value includes and builds upon the number and type of assessment objects defined for the focused attribute value. 

The use of bolded text in the assessment method description indicates content that was added and appears for the first time, signifying greater rigor and level of detail for the attribute value. 

PAGE 707 

APPENDIX C 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

**Assessment Method** Examine 

**Assessment Objects:** Specifications (e.g., policies, plans, procedures, system requirements, designs) Mechanisms (e.g., functionality implemented in hardware, software, firmware) 

Activities (e.g., system operations, administration, management, exercises) 

**Definition:** The process of checking, inspecting, reviewing, observing, studying, or analyzing one or more assessment objects to facilitate understanding, achieve clarification, or obtain evidence, the results of which are used to support the determination of security and privacy control existence, functionality, correctness, completeness, and potential for improvement over time. 

**Supplemental guidance:** Typical assessor actions may include reviewing information security and privacy policies, plans, and procedures; analyzing system design documentation and interface specifications; observing system backup operations; reviewing the results of contingency plan exercises; observing incident response activities; studying technical manuals and user/administrator guides; checking, studying, or observing the operation of an information technology mechanism in the system hardware and software; or checking, studying, or observing physical security or privacy measures related to the operation of a system. 

**Attributes:** Depth, Coverage 

- The depth attribute addresses the rigor of and level of detail in the examination process. There are three possible values for the depth attribute: _basic_ , _focused_ , and _comprehensive._ 

<u>Basic examination: Examination that consists of high-level reviews, checks,</u> observations, or inspections of the assessment object. The basic examination is conducted using a limited body of evidence or documentation (e.g., functionallevel descriptions for mechanisms; high-level process descriptions for activities; actual documents for specifications). Basic examinations provide a level of understanding of the security and privacy controls necessary for determining whether the controls are implemented and free of obvious errors. 

<u>Focused examination: Examination that consists of high-level reviews, checks,</u> observations, or inspections **and more in-depth studies/analyses** of the assessment object. The focused examination is conducted using a **substantial** body of evidence or documentation (e.g., functional-level descriptions **and, where appropriate and available, high-level design information** for 

mechanisms; high-level process descriptions **and implementation procedures** for activities; the actual documents **and related documents** for specifications). **Focused** examinations provide a level of understanding of the security and privacy controls necessary for determining whether the controls are implemented and free of obvious errors **and whether there are increased** 

PAGE 708 

APPENDIX C 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

**grounds for confidence that the controls are implemented correctly and operating as intended.** 

<u>Comprehensive examination: Examination that consists of high-level reviews,</u> checks, observations, or inspections and more in-depth, **detailed, and thorough** studies/analyses of the assessment object. The comprehensive examination is conducted using an **extensive** body of evidence or documentation (e.g., functional-level descriptions and, where appropriate and available, high-level design information, **low-level design information, and implementation information** for mechanisms; high-level process descriptions and **detailed** implementation procedures for activities; the actual documents and related documents for specifications<sup>53</sup> ). **Comprehensive** examinations provide a level of understanding of the security and privacy controls necessary for determining whether the controls are implemented and free of obvious errors, there are **further** increased grounds for confidence that the controls are implemented correctly and operating as intended **on an ongoing and consistent basis, and there is support for continuous improvement in the effectiveness of the controls.** 

- The _coverage_ attribute addresses the scope or breadth of the examination process and includes the types of assessment objects to be examined, the number of objects to be examined (by type), and specific objects to be examined.<sup>54</sup> There are three possible values for the coverage attribute: _basic_ , _focused_ , and _comprehensive_ . 

<u>Basic examination: Examination that uses a representative sample of</u> assessment objects (by type and number within type) to provide the level of coverage necessary for determining whether the security and privacy controls are implemented and free of obvious errors. 

<u>Focused examination: Examination that uses a representative sample of</u> assessment objects (by type and number within type) **and other specific assessment objects deemed particularly important to achieving the assessment objective** to provide the level of coverage necessary for determining whether the security and privacy controls are implemented and free of obvious errors **and whether there are increased grounds for confidence that the controls are implemented correctly and operating as intended.** 

<u>Comprehensive examination: Examination that uses a</u> **sufficiently large** sample of assessment objects (by type and number within type) and other specific assessment objects deemed particularly important to achieving the assessment objective to provide the level of coverage necessary for determining whether 

53 While additional documentation is likely needed for mechanisms when moving from basic to focused to comprehensive examinations, the documentation associated with specifications and activities may be the same or similar for focused and comprehensive examinations, with the rigor of the examinations of these documents being increased at the comprehensive level. 

54 The organization considers a variety of factors (e.g., available resources, importance of the assessment, the organization’s overall assessment goals and objectives), confers with assessors, and provides direction on the type, number, and specific objects to be examined for the particular attribute value described. 

PAGE 709 

APPENDIX C 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

the security and privacy controls are implemented and free of obvious errors, there are **further** increased grounds for confidence that the controls are implemented correctly and operating as intended **on an ongoing and consistent basis, and there is support for continuous improvement in the effectiveness of the controls.** 

PAGE 710 

APPENDIX C 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

**Assessment Method** Interview 

**Assessment Objects:** Individuals or groups of individuals 

**Definition:** The process of conducting discussions with individuals or groups within an organization to facilitate understanding, achieve clarification, or lead to the location of evidence, the results of which are used to support the determination of security and privacy control existence, functionality, correctness, completeness, and potential for improvement over time. 

Supplemental guidance: Typical assessor actions may include interviewing agency heads, chief information officers, senior agency information security officers, senior agency officials for privacy, authorizing officials, information owners, system and mission owners, system security and privacy officers, system security and privacy managers, personnel officers, human resource managers, legal, facilities managers, emergency management staff, training officers, system operators, network and system administrators, site managers, physical security officers, and users. 

**Attributes:** Depth, Coverage 

- The depth attribute addresses the rigor of and level of detail in the interview process. There are three possible values for the depth attribute: basic, focused, and comprehensive. 

<u>Basic interview: Interview that consists of broad-based, high-level discussions</u> with individuals or groups of individuals. The basic interview is conducted using a set of generalized, high-level questions. Basic interviews provide a level of understanding of the security and privacy controls necessary for determining whether the controls are implemented and free of obvious errors. 

<u>Focused interview: Interview that consists of broad-based, high-level discussions</u> **and more in-depth discussions in specific areas** with individuals or groups of individuals. The focused interview is conducted using a set of generalized, highlevel questions **and more in-depth questions where the need for greater assurance or where responses indicate a need for more in-depth investigation. Focused** interviews provide a level of understanding of the security and privacy controls necessary for determining whether the controls are implemented and free of obvious errors **and whether there are increased grounds for confidence that the controls are implemented correctly and operating as intended.** 

<u>Comprehensive interview</u> **:** Interview that consists of broad-based, high-level discussions and **more in-depth, probing discussions in specific areas with individuals or groups of individuals** . The comprehensive interview is conducted using a set of generalized, high-level questions **and more in-depth, probing questions where the need for greater assurance or where responses indicate a need for more in-depth investigation. Comprehensive** interviews provide a level of understanding of the security and privacy controls necessary for determining whether the controls are implemented and free of obvious errors, there are **further** increased grounds for confidence that the controls are 

PAGE 711 

APPENDIX C 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

implemented correctly and operating as intended **on an ongoing and consistent basis, and there is support for continuous improvement in the effectiveness of the controls.** 

- The _coverage_ attribute addresses the scope or breadth of the interview process and includes the types of individuals to be interviewed (by organizational role and associated responsibility), the number of individuals to be interviewed (by type), and specific individuals to be interviewed.<sup>55</sup> There are three possible values for the coverage attribute: _basic, focused, and comprehensive._ 

<u>Basic interview: Interview that uses a representative sample of individuals in key</u> organizational roles to provide the level of coverage necessary for determining whether the security and privacy controls are implemented and free of obvious errors. 

<u>Focused interview</u> **<u>:</u>** Interview that uses a representative sample of individuals in key organizational roles **and other specific individuals deemed particularly important to achieving the assessment objective** to provide the level of coverage necessary for determining whether the security and privacy controls are implemented and free of obvious errors **and whether there are increased grounds for confidence that the controls are implemented correctly and operating as intended.** 

<u>Comprehensive interview: Interview that uses a</u> **sufficiently large** sample of individuals in key organizational roles and other specific individuals deemed particularly important to achieving the assessment objective to provide the level of coverage necessary for determining whether the security and privacy controls are implemented and free of obvious errors, there are **further** increased grounds for confidence that the controls are implemented correctly and operating as intended **on an ongoing and consistent basis, and there is support for continuous improvement in the effectiveness of the controls.** 

> 55 The organization considers a variety of factors (e.g., available resources, importance of the assessment, the organization’s overall assessment goals and objectives), confers with assessors, and provides direction on the type, number, and specific individuals to be interviewed for the particular attribute value described. 

PAGE 712 

APPENDIX C 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

**Assessment Method** Test 

**Assessment Objects:** Mechanisms (e.g., hardware, software, firmware) 

Activities (e.g., system operations, administration, management, exercises) 

**Definition:** The process of exercising one or more assessment objects under specified conditions to compare actual with expected/desired behavior, the results of which are used to support the determination of security and privacy control existence, functionality, correctness, completeness, and potential for improvement over time.<sup>56</sup> 

**Supplemental guidance:** Typical assessor actions may include testing access control, identification and authentication, and audit mechanisms; testing security and privacy configuration settings; testing physical access control devices; conducting penetration testing of key system components; testing system backup operations; testing the incident response capability; and exercising the contingency planning capability. 

**Attributes:** Depth, Coverage 

- The _depth_ attribute addresses the types of testing to be conducted. There are three possible values for the depth attribute: _basic_ , _focused_ , and _comprehensive_ . 

<u>Basic testing: Test methodology that assumes no knowledge of the internal</u> structure and implementation detail of the assessment object. Basic testing is conducted using a functional specification for mechanisms and a high-level process description for activities. Basic testing provides a level of understanding of the security and privacy controls necessary for determining whether the controls are implemented and free of obvious errors. 

<u>Focused testing: Test methodology that assumes</u> **some** knowledge of the internal structure and implementation detail of the assessment object. Focused testing is conducted using a functional specification **and limited system architectural information (e.g., high-level design)** for mechanisms and a highlevel process description **and high-level description of integration into the operational environment** for activities. Focused testing provides a level of understanding of the security and privacy controls necessary for determining whether the controls are implemented and free of obvious errors **and whether there are increased grounds for confidence that the controls are implemented correctly and operating as intended.** 

<u>Comprehensive testing: Test methodology that assumes</u> **explicit and substantial** knowledge of the internal structure and implementation detail of the assessment object. Comprehensive testing is conducted using a functional 

> 56 Testing is typically used to determine if mechanisms or activities meet a set of predefined specifications. Testing can also be performed to determine characteristics of a security or privacy control that are not commonly associated with predefined specifications, such as penetration testing. Guidelines for conducting penetration testing are provided in Appendix D. 

PAGE 713 

APPENDIX C 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

specification, **extensive** system architectural information (e.g., high-level design, **low-level design** ), **implementation representation (e.g., source code, schematics)** for mechanisms, and a high-level process description and **detailed** description of integration into the operational environment for activities. Comprehensive testing provides a level of understanding of the security and privacy controls necessary for determining whether the controls are implemented and free of obvious errors, there are **further** increased grounds for confidence that the controls are implemented correctly and operating as intended **on an ongoing and consistent basis, and there is support for continuous improvement in the effectiveness of the controls.** 

- The coverage attribute addresses the scope or breadth of the testing process and includes the types of assessment objects to be tested, the number of objects to be tested (by type), and specific objects to be tested.<sup>57</sup> There are three possible values for the coverage attribute: _basic_ , _focused_ , and _comprehensive_ . 

<u>Basic testing: Testing that uses a representative sample of assessment objects</u> (by type and number within type) to provide the level of coverage necessary for determining whether the security and privacy controls are implemented and free of obvious errors. 

<u>Focused testing: Testing that uses a representative sample of assessment</u> objects (by type and number within type) **and other specific assessment objects deemed particularly important to achieving the assessment objective** to provide the level of coverage necessary for determining whether the security and privacy controls are implemented and free of obvious errors **and whether there are increased grounds for confidence that the controls are implemented correctly and operating as intended.** 

<u>Comprehensive testing: Testing that uses a</u> **sufficiently large** sample of assessment objects (by type and number within type) and other specific assessment objects deemed particularly important to achieving the assessment objective to provide the level of coverage necessary for determining whether the security and privacy controls are implemented and free of obvious errors, there are **further** increased grounds for confidence that the controls are implemented correctly and operating as intended **on an ongoing and consistent basis, and there is support for continuous improvement in the effectiveness of the controls.** 

> 57 The organization considers a variety of factors (e.g., available resources, importance of the assessment, the organization’s overall assessment goals and objectives), confers with assessors, and provides direction on the type, number, and specific objects to be tested for the particular attribute value described. For mechanism-related testing, the coverage attribute also addresses the extent of the testing conducted (e.g., for software, the number of test cases and modules tested; for hardware, the range of inputs, number of components tested, and range of environmental factors over which the testing is conducted). 

PAGE 714 

APPENDIX C 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

### **APPENDIX D** 

# **PENETRATION TESTING** 

##### ASSESSMENT TOOLS AND TECHNIQUES TO IDENTIFY SYSTEM WEAKNESSES 

Organizations may consider adding controlled penetration testing to their arsenal of tools and techniques used to assess the security and privacy controls in organizational systems. Penetration testing is a specific type of assessment in which assessors simulate the actions of a given class of attacker by using a defined set of documentation (i.e., documentation representative of what that class of attacker is likely to possess) and working under other specific constraints to attempt to circumvent the security or privacy features of a system. 

Penetration testing is conducted as a controlled attempt to breach the security and privacy controls employed within the system using the attacker’s techniques and appropriate hardware and software tools. Penetration testing represents the results of a specific assessor or group of assessors at a specific point in time using agreed-upon _rules of engagement_ . Considering the complexity of the information technologies commonly employed by organizations today, penetration testing can be viewed not as a means to verify the security and privacy features of a system but rather as a means to enhance the organization’s understanding of the system, uncover weaknesses or deficiencies in the system, and indicate the level of effort required on the part of adversaries to breach the system’s safeguards. 

Penetration testing exercises can be scheduled and/or random in accordance with organizational policy and organizational assessments of risk. Consideration can be given to performing penetration tests on any newly developed system (or legacy system undergoing a major upgrade) before the system is authorized for operation, after important changes are made to the environment in which the system operates, and when a new type of attack is discovered that may impact the system. Organizations actively monitor the system environment and threat landscape (e.g., new vulnerabilities, attack techniques, new technology deployments, user security, and privacy awareness and training) to identify changes that require out-of-cycle penetration testing. 

Organizations specify which components within the system are subject to penetration testing as well as the attacker’s profile to be adopted throughout the penetration testing exercises. Organizations train selected personnel in the use and maintenance of penetration testing tools and techniques. Effective penetration testing tools have the capability to readily update the list of attack techniques and exploitable vulnerabilities used during the exercises. Organizations update the list of attack techniques and exploitable vulnerabilities used in penetration testing based on an organizational assessment of risk or when significant new vulnerabilities or threats are identified and reported. Whenever possible, organizations employ tools and attack techniques that include the capability to perform penetration testing exercises on systems and security and privacy controls in an automated manner.<sup>58</sup> 

> 58 While automated penetration testing tools provide repeatable results and reduce the resources used, organizations should carefully consider the potential detrimental effects of automated exploits on system availability. Additionally, penetration testing based solely on automated tools may not provide the level of attempted system compromise that organizations might experience from an actual attacker. 

PAGE 715 

APPENDIX D 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

The information obtained from the penetration testing process can be shared with appropriate personnel throughout the organization to help prioritize the vulnerabilities in the system that are demonstrably subject to compromise by attackers of a profile equivalent to the ones used in the penetration testing exercises. The prioritization helps to determine effective strategies for eliminating the identified vulnerabilities and mitigating associated risks to the organization’s operations and assets, individuals, other organizations, and the Nation resulting from the operation and use of the system. Penetration testing can be integrated into the network security testing process and the patch and vulnerability management process.<sup>59</sup> 

#### **Penetration Testing Considerations** 

Organizations consider the following criteria when developing and implementing a controlled penetration testing program. An effective penetration test: 

- Goes beyond vulnerability scanning to provide explicit proof of mission risks and an indicator of the level of effort that an adversary would need to expend in order to cause harm to the organization’s operations and assets, individuals, other organizations, or the Nation 

- Approaches the system as the adversary would – considering vulnerabilities, incorrect system configurations, trust relationships between organizations, and architectural weaknesses in the environment being tested 

- Has a clearly defined scope and contains as a minimum: 

   - A definition of the environment subject to testing (e.g., facilities, users, organizational groups) 

   - A definition of the attack surface to be tested (e.g., servers, desktop systems, wireless networks, web applications, intrusion detection and prevention systems, firewalls, email accounts, user security and privacy awareness and training posture, and incident response posture, including breaches of personally identifiable information) 

   - A definition of the threat sources to simulate (e.g., an enumeration of attackers’ profiles to be used, such as an internal attacker, casual attacker, single or group of external targeted attackers, nation/state actor, or criminal organization) 

   - A definition of the objectives for the simulated attacker (e.g., gain domain administrator access on the organization’s LDAP [Lightweight Directory Access Protocol] structure and access and modify information in the organization’s financial system) 

   - A definition of level of effort (e.g., time and resources) to be expended 

> 59 <u>[SP 800-40] provides guidance on patch and vulnerability management. [SP 800-115] provides guidance on</u> information and network security testing. 

PAGE 716 

APPENDIX D 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

`o` A definition of the rules of engagement 

- Thoroughly documents all activities performed during the test, including all exploited vulnerabilities and how the vulnerabilities were combined into attacks 

- Produces results indicating a likelihood of occurrence for a given attack by using the level of effort that the team needed to expend to penetrate the system as an indicator of the penetration resistance of the system 

- Validates existing security and privacy controls (including risk mitigation mechanisms, such as firewalls and intrusion detection and prevention systems) 

- Provides a verifiable and reproducible log of all the activities performed during the test 

- Provides actionable results with information about possible remediation measures for the successful attacks performed. 

PAGE 717 

APPENDIX D 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

### **APPENDIX E** 

# **ASSESSMENT REPORTS** 

DOCUMENTING THE FINDINGS FROM SECURITY AND PRIVACY CONTROL ASSESSMENTS 

The primary purpose of the _security_ and _privacy assessment reports_ is to convey the results of the security and privacy control assessments to appropriate organizational officials. The security assessment report and privacy assessment report are included in the system authorization package along with the system security plan and privacy plan (or equivalent for common controls), plan of action and milestones, and an executive summary to provide authorizing officials with the information necessary to make risk-based decisions on whether to authorize a system to begin operating or continue its operation. As the assessment and authorization process becomes more dynamic in nature, relying to a greater degree on the continuous monitoring aspects of the process as an integrated and tightly coupled part of the system development life cycle, the ability to update the security and privacy assessment reports frequently becomes a critical aspect of information security and privacy programs. 

It is important to emphasize the relationship among the key artifacts in the authorization package, as described in [SP 800-37]. Artifacts in the authorization package provide a reliable indication of the overall security and privacy risk posture of the system and the ability of the system to protect the organization’s operations and assets, individuals, other organizations, and the Nation to the degree necessary. The key artifacts are updated on an ongoing basis in accordance with the continuous monitoring program established by the organization. 

The security and privacy assessment reports provide a disciplined and structured approach for documenting the findings of the assessor and the recommendations for correcting any weaknesses or deficiencies in the security and privacy controls.<sup>60</sup> This appendix provides a template for reporting the results from security and privacy control assessments. Organizations are not restricted to the specific template format. However, it is expected that the overall report of an assessment includes information similar to that detailed in the template for each security and privacy control assessed preceded by a summary that provides the list of all security and privacy controls assessed and the overall status of each control. 

#### **Key Elements for Assessment Reporting** 

The following elements are included in security and privacy assessment reports:<sup>61</sup> 

- System name 

- Security categorization 

- Site(s) assessed and assessment date(s) 

- Assessor’s name/identification 

- Previous assessment results (if reused) 

> 60 While the rationale for each determination made is a part of the formal security and privacy assessment reports, the complete set of records produced as part of the assessment is likely not included in the report. However, organizations retain the portion of the records necessary for maintaining an audit trail of assessment evidence, facilitating reuse of evidence, and promoting repeatability of assessor actions. 

> 61 Information available in other key organizational documents (e.g., security or privacy plans, risk assessments, plans of action and milestones, or security or privacy assessment plans) need not be duplicated in the security and privacy assessment reports. 

PAGE 718 

APPENDIX E 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

- Security/privacy control or control enhancement designator 

- Selected assessment methods and objects 

- Depth and coverage attributes values 

- Assessment finding summary (indicating “satisfied” or “other than satisfied”) 

- Assessor comments (weaknesses or deficiencies noted) 

- • Assessor recommendations (priorities, remediation, corrective actions, or improvements) 

#### **The Assessment Findings** 

Each determination statement executed by an assessor results in one of the following findings: satisfied (S) or other than satisfied (O). Figure 9 provides an example of an assessment finding for CP-03. 

During an actual security and privacy control assessment, the assessment findings, comments, and recommendations are documented using appropriate organization-defined reporting forms or platforms. Organizations are encouraged to develop standard templates for reporting that contain the key elements for assessment reporting described above. Whenever possible, automation is used to make assessment data collection and reporting cost-effective, timely, and efficient. 

PAGE 719 

APPENDIX E 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

|**CP-03**<br>**CONTINGENCY**<br>**ASSESSMENT O**|**TRAINING**<br>**BJECTIVE**|||
|---|---|---|---|
|_Determine if:_||**ASSESSMENT**<br>**FINDING**|**ASSESSOR COMMENTS AND RECOMMENDATIONS**|
|**CP-03_ODP[01]**|**_the time period within which to provide contingency training after_**<br>**_assuming a contingency role or responsibility is defined;_**|S|System ABC con�ngency planning policy iden�fies (organiza�on-defined) �me<br>period as 4 weeks.|
|**CP-03_ODP[02]**|**_frequency at which to provide training to system users with a_**<br>**_contingency role or responsibility is defined;_**|S|System ABC con�ngency planning policy iden�fies frequency as annually.|
|**CP-03_ODP[03]**|**_frequency at which to review and update contingency training_**<br>**_content is defined;_**|S|System ABC con�ngency planning policy iden�fies frequency as annually.|
|**CP-03_ODP[04]**|**_events necessitating review and update of contingency training are_**<br>**_defined;_**|O|No assessment ar�facts iden�fy events necessita�ng review and update of<br>con�ngency training.|
|**CP-03a.01**|_contingency training is provided to system users consistent with_<br>_assigned roles and responsibilities within <CP -03_ODP[01] time_<br>_period> of assuming a contingency role or responsibility;_|S||
|**CP-03a.02**|_contingency training is provided to system users consistent with_<br>_assigned roles and responsibilities when required by system changes;_|O|Marked as “other than sa�sfied.” Assessors could not find evidence that<br>con�ngency training to system ABC users was provided consistent with their<br>assigned roles and responsibili�es when there were significant changes to the<br>system.|
|**CP-03a.03**|_contingency training is provided to system users consistent with_<br>_assigned roles and responsibilities <CP -03_ODP[02] frequency>_<br>_thereafter;_|S||
|**CP-03b.[01]**|_the contingency plan training content is reviewed and updated_<br>_<CP-03_ODP[03] frequency>;_|S||
|**CP-03b.[02]**|_the contingency plan training content is reviewed and updated_<br>_following <CP-03_ODP[04] events>._|O|CP-03_ODP[04] is not defined; this objec�ve cannot be assessed.|



**FIGURE 9:  SECURITY AND PRIVACY CONTROL ASSESSMENT FINDINGS EXAMPLE** 

PAGE 720 

APPENDIX E 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

### **APPENDIX F** 

# **ONGOING ASSESSMENT AND AUTOMATION** 

USING AUTOMATED TECHNIQUES TO ACHIEVE MORE EFFICIENT ASSESSMENTS 

Ongoing security and privacy assessment is the continuous evaluation of the effectiveness of security and privacy control implementation. Ongoing assessment is an essential subset of _Information Security Continuous Monitoring (ISCM)_ activities.<sup>62</sup> Ongoing assessment encompasses ISCM Steps 3 and 4 and is initiated as part of ISCM Step 3, _Implement_ , when the collection of security-related information begins in accordance with organization-defined frequencies. Ongoing assessment continues as the security-related information generated as part of ISCM Step 3 is correlated, analyzed, and reported to senior leaders as part of ISCM Step 4. As noted in [SP 800-137], security-related information is generated, correlated, analyzed, and reported using automated tools to the extent that it is possible and practical to do so. When it is not possible and practical to use automated tools, security-related information is generated, correlated, analyzed, and reported using manual or procedural methods. In this way, senior leaders are provided with the security-related information necessary to make credible, riskbased decisions regarding information security risk to the mission and business.<sup>63</sup> 

Automating assessments is a fundamental element in helping organizations manage information security and privacy risks. Evolving threats and changes in PII processing create a challenge for organizations that design, implement, and operate complex systems compromised of many hardware, firmware, and software components. The ability to assess all implemented security and privacy controls as frequently as needed using manual or procedural methods has become impractical for most organizations due to the size, complexity, and scope of their information technology infrastructures. 

One strategy to increase the number of security and privacy controls for which assessment and monitoring can be automated depends on defining a _desired state specification_ and expressing the desired state in a form that can be compared automatically (i.e., in data) with the actual state. The desired state is a defined value or _specification_ to which the actual state value can be compared. A mismatch of the two values indicates that a defect is present in the effectiveness of one or more controls. For example, an organizational policy may state that user accounts will be locked after three unsuccessful logon attempts. The desired state specification would be that applicable devices are configured to lock accounts after three unsuccessful logon attempts. If, during automated assessment, the security-related information collected indicates that a specific device is configured such that accounts are locked only after _five_ unsuccessful logon attempts, a mismatch between the desired state (three attempts allowed before lockout) and the actual state (five attempts allowed before lockout) is identified. The mismatch may reflect a problem with the effectiveness of SP 800-53 control AC-7, Unsuccessful Logon Attempts; AC-2, Account Management; and/or CM-2, Baseline Configuration. When a desired state specification 

> 62 <u>[SP 800-137] provides guidance on Information Security Continuous Monitoring (ISCM). [SP 800-137A] provides</u> guidance on conducting assessments of ISCM Programs. 

> 63 Continuous monitoring can be effectively applied to privacy controls consistent with the concepts, techniques, and principles described in [SP 800-137]. Senior Agency Officials for Privacy (SAOPs)/Chief Privacy Officers (CPOs) provide guidance on the ongoing monitoring of privacy controls. 

PAGE 721 

APPENDIX F 

NIST SP 800-53A REV. 5 

ASSESSING SECURITY AND PRIVACY CONTROLS IN INFORMATION SYSTEMS AND ORGANIZATIONS 

strategy is employed, security-related information generated from ISCM activities is equivalent to security control assessment results. 

In order to effectively automate security and privacy control assessments using the desired state specification strategy, it is important to meet the following prerequisites: 

- Automated actual state and behavior specifications are defined; 

- Data-based desired state specifications (comparable to the actual state) are defined; and 

- A method to compute or identify defects (i.e., differences between desired and actual state and behavior) is defined. 

When the prerequisites are met, the assessment system can automatically compute where differences between the desired state and actual state (defects) occur, use that information to create security and privacy assessment reports, and deliver those reports to designated personnel via a security and privacy management console (dashboard). 

When automated tools are used to conduct assessments, the test assessment method is used.<sup>64</sup> The organization determines and documents the specific capabilities<sup>65</sup> and privacy controls that are being assessed by the automated tool, the frequency with which the tool will assess the capabilities or controls, and the analysis and reporting requirements for the capabilities or controls. 

To help automate ongoing assessment, NIST and the Department of Homeland Security Cybersecurity Infrastructure Security Agency (CISA) collaborated on the development of a process that leverages the _test_ assessment method and is consistent with the Risk Management Framework, as described in SP 800-37 and the ISCM guidance in SP 800-137. The automation process is described in NIST Interagency/Internal Report (NISTIR) 8011, _Automation Support for Security Control Assessments: Volume 1: Overview_ <u>[IR 8011-1]</u> which defines specific security capabilities and describes the overall automated assessment process. Specific methods to automate the assessment of each defined security capability is provided in subsequent NISTIR 8011 volumes. Automation of the test method for security assessments is facilitated by the CISA Continuous Diagnostics and Mitigation (CDM) program. 

> 64 If greater depth and coverage are needed to provide additional assurance, the automated test method may be supplemented by the use of manual or procedural assessment methods (i.e., interview, examine, or manual test). 

> 65 If a security or privacy capability is defined, a mapping of all individual controls that support the capability is documented. If organizations define multiple capabilities, a many-to-many relationship between security and privacy controls and capabilities is to be expected. See <u>Section 3.5</u> for additional information regarding security and privacy capability assessments. 

PAGE 722 

APPENDIX F 

