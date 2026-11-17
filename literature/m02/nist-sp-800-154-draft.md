---
title: "NIST SP 800-154 (Initial Public Draft), Guide to Data-Centric System Threat Modeling"
publisher: "NIST (March 2016 draft; never finalized)"
source_url: https://csrc.nist.gov/files/pubs/sp/800/154/ipd/docs/sp800_154_draft.pdf
retrieved: 2026-11-17
sha256: 53fc49939603cffe116b0dc6d07cc81b46c072411dc1c2d2ed5c41a6b3933286
converter: pymupdf4llm 2.1
source_format: pdf
licence: "US government work (NIST)"
module: 2
verified: true
---
1 

## **Draft NIST Special Publication 800-154** 

2 

3 

4 

# **Guide to Data-Centric System Threat Modeling** 

5 

6 

7 

8 

9 

Murugiah Souppaya Karen Scarfone 

10 

11 

12 

13 

14 

15 

16 

17 

C  O  M  P  U  T  E  R      S  E  C  U  R  I  T  Y 

18 

19 



20 

21 

24 

28 

29 

30 31 32 33 34 35 

36 37 38 39 40 41 42 43 

44 45 46 47 48 49 50 51 

22 

23 

# **Draft NIST Special Publication 800-154 Guide to Data-Centric System Threat Modeling** 

25 

26 

27 

Murugiah Souppaya _Computer Security Division Information Technology Laboratory_ 

Karen Scarfone _Scarfone Cybersecurity Clifton, VA_ 

March 2016 



U.S. Department of Commerce _Penny Pritzker, Secretary_ 

National Institute of Standards and Technology _Willie May, Under Secretary of Commerce for Standards and Technology and Director_ 

52 

85 86 87 88 

#### **Authority** 

53 This publication has been developed by NIST in accordance with its statutory responsibilities under the 54 Federal Information Security Modernization Act (FISMA) of 2014, 44 U.S.C. § 3541 _et seq._ , Public Law 55 (P.L.) 113-283. NIST is responsible for developing information security standards and guidelines, 56 including minimum requirements for federal information systems, but such standards and guidelines shall 57 not apply to national security systems without the express approval of appropriate federal officials 58 exercising policy authority over such systems. This guideline is consistent with the requirements of the 59 Office of Management and Budget (OMB) Circular A-130. 

58 59 

60 Nothing in this publication should be taken to contradict the standards and guidelines made mandatory 61 and binding on federal agencies by the Secretary of Commerce under statutory authority. Nor should 62 these guidelines be interpreted as altering or superseding the existing authorities of the Secretary of 63 Commerce, Director of the OMB, or any other federal official.  This publication may be used by 64 nongovernmental organizations on a voluntary basis and is not subject to copyright in the United States. 65 Attribution would, however, be appreciated by NIST. 

66 67 68 

National Institute of Standards and Technology Special Publication 800-154 Natl. Inst. Stand. Technol. Spec. Publ. 800-154, 25 pages (March 2016) CODEN: NSPUE2 

69 70 71 72 73 74 75 76 77 78 79 80 81 

Certain commercial entities, equipment, or materials may be identified in this document in order to describe an <mark>experimental procedure or concept adequately. Such identification is not intended to imply recommendation or endorsement by NIST, nor is it intended to imply that the entities, materials, or equipment are necessarily the best</mark> available for the purpose. 

<mark>There may be references in this publication to other publications currently under development by NIST in accordance with its assigned statutory responsibilities. The information in this publication, including concepts and methodologies, may be used by federal agencies even before the completion of such companion publications. Thus, until each publication is completed, current requirements, guidelines, and procedures, where they exist, remain operative. For planning and transition purposes, federal agencies may wish to closely follow the development of</mark> these new publications by NIST. 

<mark>Organizations are encouraged to review all draft publications during public comment periods and provide feedback to NIST. Many NIST cybersecurity publications, other than the ones noted above, are available at</mark> <u>http://csrc.nist.gov/publications.</u> 

82 

83 

#### **Public comment period:** **_March 14, 2016_ through** **_April 15, 2016_** 

84 

All comments are subject to release under the Freedom of Information Act (FOIA). 

National Institute of Standards and Technology Attn: Computer Security Division, Information Technology Laboratory 100 Bureau Drive (Mail Stop 8930) Gaithersburg, MD 20899-8930 Email: 800-154comments@nist.gov 

89 

i 

90 

#### **Reports on Computer Systems Technology** 

91 The Information Technology Laboratory (ITL) at the National Institute of Standards and Technology 92 (NIST) promotes the U.S. economy and public welfare by providing technical leadership for the Nation’s 93 measurement and standards infrastructure. ITL develops tests, test methods, reference data, proof of 94 concept implementations, and technical analyses to advance the development and productive use of 95 information technology. ITL’s responsibilities include the development of management, administrative, 96 technical, and physical standards and guidelines for the cost-effective security and privacy of other than 97 national security-related information in federal information systems. The Special Publication 800-series 98 reports on ITL’s research, guidelines, and outreach efforts in information system security, and its 99 collaborative activities with industry, government, and academic organizations. 

97 98 99 

100 

101 

#### **Abstract** 

102 Threat modeling is a form of risk assessment that models aspects of the attack and defense sides of a 103 particular logical entity, such as a piece of data, an application, a host, a system, or an environment. This 104 publication examines data-centric system threat modeling, which is threat modeling that is focused on 105 protecting particular types of data within systems. The publication provides information on the basics of 106 data-centric system threat modeling so that organizations can successfully use it as part of their risk 107 management processes. The general methodology provided by the publication is not intended to replace 108 existing methodologies, but rather to define fundamental principles that should be part of any sound data109 centric system threat modeling methodology. 

110 

111 

#### **Keywords** 

112 data security; information security; risk assessment; risk management; threat modeling; threats; 113 vulnerabilities 

114 

115 

#### **Trademark Information** 

116 

All trademarks or registered trademarks belong to their respective organizations. 

117 

118 

#### **Acknowledgments** 

- 119 The authors, Murugiah Souppaya of the National Institute of Standards and Technology (NIST) and 120 Karen Scarfone of Scarfone Cybersecurity, wish to thank their colleagues who reviewed drafts of this 121 document and contributed to its technical content. 

122 

ii 

123 

125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 

149 150 151 

### Table of Contents 

124 

|**Exe**<br>|**cutive**<br>|**Summary ................................................................................................................. 1**<br>|
|---|---|---|
|**1.**|**Intro**|**duction ...................................................................................................................... 2**|
||1.1<br>|Purpose and Scope ................................................................................................... 2<br>|
||1.2|Audience ................................................................................................................... 2|
||1.3|Document Structure .................................................................................................. 2|
|**2.**|**Attac**|**k and Defense Basics .............................................................................................. 3**|
||2.1|The Attack Side ......................................................................................................... 3|
|||2.1.1<br>Vulnerability .................................................................................................. 3|
|||2.1.2<br>Exploit and Attack ......................................................................................... 4|
|||2.1.3<br>Attack Vector ................................................................................................. 5|
|||2.1.4<br>Threat ........................................................................................................... 6|
||2.2|The Defense Side ...................................................................................................... 7|
|||2.2.1<br>Risk ............................................................................................................... 7|
|||2.2.2<br>Security Controls ........................................................................................... 7|
|||2.2.3<br>Security Objectives ....................................................................................... 7|
|**3.**|**Intro**|**duction to System and Data-Centric System Threat Modeling ............................. 9**|
|**4.**|**Basi**|**cs of Data-Centric System Threat Modeling ..........................................................11**|
||4.1|Step 1: Identify and Characterize the System and Data of Interest .......................... 11|
||4.2|Step 2: Identify and Select the Attack Vectors to Be Included in the Model ............. 13|
||4.3|Step 3: Characterize the Security Controls for Mitigating the Attack Vectors ........... 14|
||4.4|Step 4: Analyze the Threat Model ........................................................................... 16|
||4.5|Customizing the Data-Centric System Threat Modeling Approach .......................... 17|



|147|List of Appendices|
|---|---|
|148|**Appendix A— Acronyms and Other Abbreviations ..............................................................19**|
|149|**Appendix B— References ......................................................................................................20**|



iii 

NIST SP 800-154 (DRAFT) 

GUIDE TO DATA-CENTRIC SYSTEM THREAT MODELING 

#### 152 

### **<mark>Executive Summary</mark>** 

153 Threat modeling is a form of risk assessment that models aspects of the attack and defense sides of a 154 particular logical entity, such as a piece of data, an application, a host, a system, or an environment. The 155 fundamental principle underlying threat modeling is that there are always limited resources for security 156 and it is necessary to determine how to use those limited resources effectively. There are many types of 157 threat modeling; for example, system threat modeling is threat modeling performed for operational 158 systems to improve their overall security. This publication focuses on one type of system threat modeling: 159 data-centric system threat modeling. Data-centric system threat modeling is threat modeling that is 160 focused on protecting particular types of data within systems. 

161 Threat modeling is needed because of the dynamic nature of security. The attack and defense sides of 162 security are constantly changing. As part of handling this change, organizations should continually 163 reassess and evolve their defenses. This includes adopting continuous monitoring practices, security 164 automation technologies, and threat intelligence feeds to detect new vulnerabilities and attacks in near165 real-time, allowing rapid risk mitigation. Another key component of handling the constant change in 166 security is having security metrics; these can be used for more informed decision making, again often 167 relating to risk management in general and risk mitigation in particular. 

168 Increasingly, simply following general “best practices” for security is insufficient for safeguarding high169 value data. Best practices are largely based on conventional wisdom intended to mitigate common threats 170 and vulnerabilities. By their very nature, such best practices are generalized, especially for ubiquitous 171 products (web browsers, server and desktop operating systems, etc.) They do not take into account the 172 unique characteristics of each system. Also, most best practices are geared toward preventing host 173 compromise and do not take into account the security needs for particular data (again, a more generalized 174 goal versus a specific one). So, for a particular situation, best practices may not include security controls 175 that are necessary to effectively reduce risk. 

176 Data-centric system threat modeling allows organizations to consider the security needs of each case of 177 interest, instead of relying solely on generalized “best practice” recommendations. Organizations with 178 strong capabilities in continuous monitoring, security automation, and security metrics should consider 179 adding data-centric system threat modeling based on the principles presented in this publication to 180 supplement these capabilities and achieve demonstrably better security for data of particular importance. 

181 

1 

NIST SP 800-154 (DRAFT) 

GUIDE TO DATA-CENTRIC SYSTEM THREAT MODELING 

### 182 **<mark>1. Introduction</mark>** 

#### 183 

#### **1.1 Purpose and Scope** 

184 Organizations often plan, implement, maintain, and assess the security controls for their systems without 185 performing a methodical analysis of risk involving system threat modeling. The purpose of this 186 publication is to provide information on the basics of system threat modeling so that organizations can 187 successfully use it as part of their risk management processes. 

188 There are many forms of threat modeling. This publication’s scope is limited to data-centric system threat 189 modeling, which involves focusing on the security of particular instances of data (such as client 190 information stored on a field agent’s laptop) instead of focusing on the security of particular hosts, 191 operating systems (OS), applications, etc. 

192 This publication provides a general methodology that organizations can use. The intent is not to replace 193 existing methodologies, but rather to define fundamental principles that should be part of any sound data194 centric system threat modeling methodology. 

195 

#### **1.2 Audience** 

196 This document is intended for security managers, security engineers/architects, system administrators, and 197 others who are responsible for planning, implementing, and maintaining data and system security 198 controls. Auditors and others who need to assess the security of data and systems may also find this 199 publication useful. 

200 

#### **1.3 Document Structure** 

201 

The remainder of this document is organized into the following major sections and appendices: 

- 202 • Section 2 discusses attack and defense basics. The terminology and concepts defined in this 203 section are fundamental to understanding the rest of the publication. 

204 

- Section 3 provides an introduction to general system threat modeling. 

205 

- 205 • Section 4 presents a basic methodology for data-centric system threat modeling, with simplified 206 examples illustrating the use of the methodology. 

207 

   - Appendix A contains an acronym and abbreviation list. 

- 208 • Appendix B lists the references for the document. 

209 

2 

NIST SP 800-154 (DRAFT) 

GUIDE TO DATA-CENTRIC SYSTEM THREAT MODELING 

227 228 229 230 231 232 

233 234 235 236 237 238 239 240 

#### 210 

### **<mark>2. Attack and Defense Basics</mark>** 

211 212 213 214 215 216 

This section establishes a foundation for the rest of the document by covering the basic concepts of security relevant to threat modeling. It defines fundamental terminology, such as what vulnerabilities and attack vectors are, because of the lack of consensus in the security community as to what such terms mean. It also explains how these concepts work in practice. The discussion is divided into two parts: the attack side (Section 2.1) and the defense side (Section 2.2). This section can be thought of as explaining the problem that threat modeling is trying to solve. The term “threat modeling” is defined in Section 3. 

217 

#### **2.1 The Attack Side** 

218 219 220 221 222 

This section defines the basic concepts related to the attack side of threat modeling, grouped by core terms: _vulnerability_ , _exploit and attack_ , _attack vector_ , and _threat_ . Where applicable, it enumerates the major categories of each entity (such as major categories of vulnerabilities). These enumerations are not intended to be comprehensive or authoritative, but instead to help illustrate the potential scope of threat modeling activities. 

223 

#### **2.1.1 Vulnerability** 

224 The term “vulnerability” has been defined in many ways over years. This document proposes that a 225 _vulnerability_ is any trust assumption involving people, processes, or technology that can be violated in 226 order to exploit a system. Types of vulnerabilities include the following: 

   - A _software flaw vulnerability_ is caused by an error in the design or coding of software. One example is an input validation error, such as user-provided input being trusted, and thus not being properly evaluated for malicious character strings and overly long values associated with known attacks. Another example is a race condition error that allows the attacker to perform a specific action with elevated privileges. A race condition is possible because the software does not expect certain patterns of activity to occur, in effect trusting that users will not cause such patterns. 

   - A _security configuration issue vulnerability_ involves the use of security configuration settings that negatively affect the security of the software if taken advantage of by users. A security configuration setting is an element of a software’s security that can be altered through the software itself. Examples of settings are an operating system offering access control lists that set user privileges for files, and an application offering a setting to enable or disable the encryption of sensitive data stored by the application. Many configuration settings increase security at the expense of reducing functionality, so using the most secure settings could make the software useless or unusable. 

- 241 • A software feature is a functional capability provided by software. A _software feature misuse_ 242 _vulnerability_ is a vulnerability in which the feature also provides an avenue to compromise the 243 security of a system. These vulnerabilities are caused by the software designer making trust 244 assumptions that permit the software to provide beneficial features, while also introducing the 245 possibility of someone violating the trust assumptions to compromise security. For example, 246 email client software may contain a feature that renders HTML content in email messages. An 247 attacker could craft a fraudulent email message that contains hyperlinks that, when rendered in 248 HTML, appear to the recipient to be benign, but actually take the recipient to a malicious web site 249 when they are clicked on. One of the trust assumptions in the design of the HTML content 250 rendering feature was that users would not receive malicious hyperlinks and click on them. 251 Another example of a software feature misuse vulnerability is an attacker stealing a user’s 252 credentials and reusing them to impersonate the user; the trust assumption was that only the 253 legitimate user would use those credentials. Misuse vulnerabilities are inherent in software 

3 

NIST SP 800-154 (DRAFT) 

GUIDE TO DATA-CENTRIC SYSTEM THREAT MODELING 

254 255 

256 257 258 259 260 261 262 

263 

264 265 266 267 268 269 270 271 

272 273 274 275 276 277 

278 

279 280 281 282 283 284 

285 286 287 288 289 290 291 292 

features because each feature is based on trust assumptions—and those assumptions can be broken, albeit involving significant cost and effort in some cases. [1] 

No system is 100 percent secure: every system has vulnerabilities. At any given time, a system may not have any known software flaws, but security configuration issues and software feature misuse vulnerabilities are always present and cannot even be readily enumerated at this time. A system’s vulnerabilities are likely to have a wide variety of characteristics. Some will be very easy to exploit, while others will only be exploitable under a combination of highly unlikely conditions. One vulnerability might provide root-level access to a system, while another vulnerability might only permit read access to an insignificant file. 

#### **2.1.2 Exploit and Attack** 

To _exploit_ a vulnerability is to use it to violate security objectives, such as confidentiality, integrity, and availability (see Section 2.2.3 for more information on security objectives). The program code or other commands used to exploit a vulnerability are generically referred to as an _exploit_ or an _attack_ . These meanings, which are specific to the commands, are not to be confused with the verb forms of “exploit” and “attack”, which have different meanings; “to exploit” implies a successful security violation, while “to attack” implies an attempted security violation but not its success or failure. Noun forms of these verbs, referring to the actions, have the same distinction in meanings; an attack (action) that succeeds can also be called an exploit. 

This document uses the term _attacker_ to refer to a party who attacks a host, network, or other IT resource. However, not all attacks are intentional. Some attacks are performed by users who accidentally or otherwise unintentionally violate security policies, requirements, etc., to the point of compromising 

security. Because intent often has no relation to the impact of a compromise, this document uses the term “attack” to refer to both intentional and inadvertent compromises. Sections 2.1.2.1 and 2.1.2.2 discuss the individuals who perform attacks in both categories. 

#### **2.1.2.1 Intentional** 

Attackers who intend to exploit vulnerabilities are motivated by various reasons, ranging from the desire to make political or social statements to financial gain and cyberwarfare. Some attackers are focused on a short-term action, such as a financial transaction, but many attackers, especially those interested in gaining access to sensitive information, may be more interested in long-term infiltration and data gathering. These attacks are often targeted, such as focusing on exploiting a high-value system or individual. 

The skill sets of attackers vary as widely as their motivations. At one extreme are unskilled individuals who purchase attack toolkits that make basic exploitation almost trivial to perform. At the other extreme are highly skilled individuals who are capable of discovering new vulnerabilities on their own and figuring out how to exploit them. Another important group of attackers to consider is malicious insiders; even though they may not be particularly skilled in exploitation, their level of access and detailed knowledge of the organization’s systems makes them particularly effective at data theft and manipulation. A malicious insider may also work in conjunction with an external attacker, such as insiders selling their usernames and passwords to third parties. 

293 Another category of intentional attacks is not directly associated with a particular person or group—for 294 example, malware may have been propagating from system to system for some time and is not being 295 directed or otherwise controlled by anyone. This is not meant to imply that no one is responsible for the 296 malware, but rather that there is not a person specifically launching each instance of the malware. 

4 

NIST SP 800-154 (DRAFT) 

GUIDE TO DATA-CENTRIC SYSTEM THREAT MODELING 

310 

311 312 313 

318 319 

320 321 322 

323 324 325 326 327 

297 Because the malware is designed to exploit vulnerabilities, this publication considers all malware-based 298 attacks to be intentional attacks. 

#### 299 

#### **2.1.2.2 Inadvertent** 

300 Attackers who inadvertently exploit vulnerabilities are acting either by accident or through a lack of 301 understanding, such as performing actions that they do not know are security violations or do not consider 302 a “real” security problem. 

#### 303 

#### **2.1.3 Attack Vector** 

304 An _attack vector_ is a segment of the entire pathway that an attack uses to access a vulnerability. Each 305 attack vector can be thought of as comprising a _source_ of malicious content, a potentially vulnerable 306 _processor_ of that malicious content, and the nature of the malicious _content_ itself. Examples of attack 307 vectors are: 

308 309 

- Malicious web page content (content) downloaded from a web site (source) by a vulnerable web browser (processor); 

- A malicious email attachment (content) in an email client (source) rendered by a vulnerable helper application (processor); 

- A malicious email attachment (content) downloaded from an email server (source) to a vulnerable email client (processor); 

314 315 

- A network service with inherent vulnerabilities (processor) used maliciously (content) by an external endpoint (source); 

316 

317 

- Social engineering-based conversation (content) performed by phone from a human attacker (source) to get a username and password from a vulnerable user (processor); 

- Stolen user credentials (content) typed in by an attacker (source) to a web interface for an enterprise authentication system (processor); and 

- Personal information about a user harvested from social media (content) entered into a password reset website by an attacker (source) to reset a password by taking advantage of weak password reset processes (processor). 

The characteristics of attacks vary widely. Some involve exploitation of a single vulnerability using a single attack vector, while others involve multiple vulnerabilities and multiple attack vectors, or even a single vulnerability and multiple attack vectors. And the vulnerabilities and attack vectors may be spread across multiple hosts, compromising one host in order to compromise another, further complicating the composition of an attack. 

328 Here is an example of a single possible attack involving one vulnerability, decomposed into its attack 329 vectors: 

330 331 

1. Malicious email attachment (content) sent from a host (source) to the organization’s primary mail server (processor); 

5 

NIST SP 800-154 (DRAFT) 

GUIDE TO DATA-CENTRIC SYSTEM THREAT MODELING 

338 339 

- 332 2. Malicious email attachment (content) sent from the organization’s primary mail server (source) to 333 antivirus server (processor); 

334 

335 

3. Malicious email attachment (content) sent from the antivirus server (source) to the organization’s internal mail server (processor); 

336 337 

4. Malicious email attachment (content) sent from the organization’s internal mail server (source) to the user’s email client (processor); and 

5. Malicious email attachment (content) rendered (processor) by the vulnerable email client (source). 

340 Note that although there are five attack vectors, the actual exploitation only occurs during the last of the 341 five (when the malicious attachment is rendered by a vulnerable email client). However, each attack 342 vector affords an opportunity to detect and stop the attack before it goes any farther. 

343 Although this example focuses on vulnerabilities in technologies, many attacks include non-technological 344 attack vectors. For example, attackers often use social engineering methods to trick users into revealing 345 their passwords, performing actions that unknowingly grant attackers remote access to systems, and 346 otherwise enabling security to be compromised. Similar attacks may be performed on IT personnel, such 347 as an attacker impersonating a legitimate user and convincing a help desk agent to reset the user’s 348 password to a password selected by the attacker. 

349 Because the focus of this publication is modeling threats against a targeted (vulnerable) system, the 350 compromises of greatest interest are those against the ultimate target itself. There are often intermediate 351 hosts used as jumping off points for attacks—in botnets, for example. Analyzing how those intermediate 352 hosts become compromised would fall within the scope of performing an analysis of those individual 353 intermediate hosts themselves as targets, and is outside the scope of analyzing the ultimate target. So, in 354 the previous example with five attack vectors, with the ultimate target being the host with the vulnerable 355 email client, it would be irrelevant to the target how the host in step 1 that originally sent the malicious 356 email attachment was compromised. 

357 Other terms are useful when discussing attack vectors. For example, an _attack model_ comprises a scenario 358 that may occur and a single path (one or more attack vectors in sequence) that could be taken for that 359 scenario. The attack models for a scenario and the security controls attempting to disrupt those attack 360 models collectively constitute a threat model.<sup>1</sup> Another way to analyze attack vectors is to analyze all of 361 the attack vectors directly against a particular system; this is known as the system’s _attack surface_ . 

362 

#### **2.1.4 Threat** 

363 A _threat_ is defined in NIST Special Publication (SP) 800-30 as “any circumstance or event with the 364 potential to adversely impact organizational operations and assets, individuals, other organizations, or the 365 Nation through an information system via unauthorized access, destruction, disclosure, or modification of 366 information, and/or denial of service.” [2, p. B-13] Threats may be intentional or unintentional. A _threat_ 367 _source_ is the cause of a threat, such as a hostile cyber or physical attack, a human error of omission or 368 commission, a failure of organization-controlled hardware or software, or other failure beyond the control 369 of the organization. 

> 1 Section 3 contains a more formal definition of the term “threat modeling.” 

6 

NIST SP 800-154 (DRAFT) 

GUIDE TO DATA-CENTRIC SYSTEM THREAT MODELING 

370 A _threat event_ is defined in NIST SP 800-30 as “an event or situation initiated or caused by a threat 371 source that has the potential for causing adverse impact.” [2, p. B-13] The distinction between a threat and 372 a threat event is subtle, but basically a threat event is caused by a particular threat source, while a threat is 373 more generic (not caused by a particular threat source). 

374 

#### **2.2 The Defense Side** 

375 This section explains the basic concepts related to the defense side of threat modeling, grouped by core 376 terms: _risk_ , _security controls_ , and _security objectives_ . 

377 

#### **2.2.1 Risk** 

378 Committee on National Security Systems Instruction (CNSSI) 4009, _National Information Assurance (IA)_ 379 _Glossary_ , defines _risk_ in general as “a measure of the extent to which an entity is threatened by a potential 380 circumstance or event, and typically a function of: (i) the adverse impacts that would arise if the 381 circumstance or event occurs; and (ii) the likelihood of occurrence” [3, p. 104] and _information security_ 382 _risks_ specifically as “those risks that arise from the loss of confidentiality, integrity, or availability of 383 information or information systems and reflect the potential adverse impacts to organizational operations 384 (including mission, functions, image, or reputation), organizational assets, individuals, other 385 organizations, and the Nation” [3, p. 65]. 

386 _Risk management_ is defined in CNSSI 4009  as “the program and supporting processes to manage 387 information security risk to organizational operations….” [3, p. 104]. Part of risk management is _risk_ 388 _assessment_ , which is defined in NIST SP 800-30 as “the process of identifying, prioritizing, and 389 estimating risks to organizational operations (including mission, functions, image, reputation), 390 organizational assets, individuals, other organizations, and the Nation, resulting from the operation of an 391 information system” [2, p. B-9]. Risk assessment considers the possible threats and vulnerabilities, and 392 determines what security controls (see Section 2.2.2) should be used to _mitigate_ them, which means to 393 reduce their risk to an acceptable level. 

#### 394 

#### **2.2.2 Security Controls** 

395 CNSSI 4009 defines _security controls_ as “the management, operational, and technical controls (i.e., 396 safeguards or countermeasures) prescribed for an information system to protect the confidentiality, 397 integrity, and availability of the system and its information” [3, p. 110]. Although technical controls can 398 be fully automated, which makes them an obvious choice for stopping attacks, management and 399 operational controls also play important roles. For example, users must be trained on their security 400 responsibilities so that they are less likely to violate security policies, be tricked by phishing attacks, and 401 otherwise decrease the organization’s security posture. Ultimately an organization’s security relies on a 402 combination of people, processes, and technology. 

#### 403 

#### **2.2.3 Security Objectives** 

404 Organizations usually think of their security objectives for data in terms of protecting its confidentiality<sup>2</sup> , 405 integrity, and/or availability.<sup>3</sup> In many cases, the security objectives for an instance of data should not all 406 have equal importance, and in some cases, an organization may want to focus its threat modeling efforts 

> 2 For the purposes of this publication, privacy objectives will be considered a subset of confidentiality objectives. 

> 3 Some organizations may choose to replace the security objectives with one or more security requirements for threat modeling purposes. Security requirements are more specific and granular than security objectives, and they often come directly from the organization’s policies or from regulations or security compliance initiatives that the organization is subject to. 

7 

NIST SP 800-154 (DRAFT) 

GUIDE TO DATA-CENTRIC SYSTEM THREAT MODELING 

- 407 on a single objective. For example, if a risk assessment shows that the risk of a breach of confidentiality is 408 unacceptably high, then performing threat modeling for confidentiality only may be most helpful for 409 mitigating the confidentiality breach risk to an acceptable level. Similarly, information that has already 410 been released to the public may still need its integrity and availability protected, but not its 411 confidentiality. 

- 412 Because this publication is addressing data-centric system threat modeling, only security objectives for 413 data—not systems—are pertinent. This means that operational unavailability of systems caused by attacks 414 is out of scope, for example, while operational unavailability of data caused by attacks is in scope. 

- 415 The security objectives relate directly to the risk management, assessment, mitigation, and security 416 control concepts discussed in Sections 2.2.1 and 2.2.2. For example, if the results of risk assessment show 

- 417 that the risk of a breach of confidentiality is unacceptably high, then additional security controls or 

- 418 changes to existing security controls may be needed to mitigate the confidentiality breach risk to an 419 acceptable level. The same is true for integrity and availability. 

- 420 

8 

NIST SP 800-154 (DRAFT) 

GUIDE TO DATA-CENTRIC SYSTEM THREAT MODELING 

#### 421 

### **<mark>3. Introduction to System and Data-Centric System Threat Modeling</mark>** 

422 This section provides an overview of threat modeling in general, with an emphasis on system and data423 centric system threat modeling. _Threat modeling_ is a form of risk assessment that models aspects of the 424 attack and defense sides of a particular logical entity, such as a piece of data, an application, a host, a 425 system, or an environment. The fundamental principle underlying threat modeling is that there are always 426 limited resources for security and it is necessary to determine how to use those limited resources 427 effectively. 

423 424 425 426 

428 There are many types of threat modeling, and they can be distinguished based on three related 429 characteristics: 

430 

1. The _logical entity_ being modeled (data, software, system, etc.); 

431 

432 433 

2. The _phase_ of the system lifecycle (for example, modeling security for software during its initial design versus modeling security for already-implemented off-the-shelf software, for example); and 

434 435 

3. The _goal_ of the threat modeling (to reduce software vulnerabilities, to thwart particular classes of attackers, to improve overall system security, to protect particular types of data, etc.). 

436 A common form of threat modeling is _software threat modeling_ , which is threat modeling performed 437 during software design to reduce software vulnerabilities. There are many established methodologies for 438 performing software threat modeling. 

439 Another common form of threat modeling is known as _system threat modeling_ , which is threat modeling 440 performed for operational systems to improve their overall security. Compared to software threat 441 modeling, system threat modeling tends to be largely informal and ad hoc. 

441 

442 _Data-centric system threat modeling_ is a particular type of system threat modeling, and its basics are 443 described in Section 4. This type of threat modeling is focused on protecting particular types of data 444 within systems. 

445 Threat modeling is needed because of the dynamic nature of security. Security would be difficult enough 446 to tackle if it was a one-time endeavor. Unfortunately, the attack side is constantly changing; new 447 vulnerabilities are discovered, new attacks are created, and new threats arise. Long-term changes happen, 448 too—new classes of vulnerabilities are discovered, attacker motivations change, and other 449 transformations occur over years. The defense side of security is also constantly changing—security 450 controls are improved and enhanced, new types of security controls are developed, etc. Change is 451 inevitable; as a particular class of vulnerabilities becomes well mitigated, for example, attackers simply 452 identify another class of vulnerabilities that are not as well mitigated to exploit, and defenders adjust 453 security controls accordingly. 

447 448 449 450 451 452 453 

454 

454 As part of handling this constant change, organizations should continually reassess and evolve their 455 defenses. This includes adopting continuous monitoring practices [4], security automation technologies 456 [5], and threat intelligence feeds to detect new vulnerabilities and attack attempts in near-real-time, 457 allowing rapid risk mitigation. Another key component of handling the constant change in security is 458 having security metrics; these can be used for more informed decision making, again often relating to risk 459 management in general and risk mitigation in particular. 

9 

NIST SP 800-154 (DRAFT) 

GUIDE TO DATA-CENTRIC SYSTEM THREAT MODELING 

460 Organizations with strong capabilities in continuous monitoring, security automation, and security metrics 461 should consider adding data-centric system threat modeling as described in Section 4 to supplement these 462 capabilities and achieve demonstrably better security for data of particular interest. Quantitative security 463 metrics are more accurate than qualitative ones, but quantitative metrics are presently very difficult for 464 most organizations to collect. Using high-quality qualitative metrics is far better than using no metrics at 465 all. 

466 Increasingly, simply following general “best practices” for security is insufficient for safeguarding high467 value data. Best practices are largely based on conventional wisdom intended to mitigate common threats 468 and vulnerabilities. By their very nature, such best practices are generalized, especially for ubiquitous 469 products (web browsers, server and desktop operating systems, etc.) They do not take into account the 470 unique characteristics of each system. Also, most best practices are geared toward preventing host 471 compromise and do not take into account the security needs for particular data (again, a more generalized 472 goal versus a specific one). So, for a particular situation, best practices may omit security controls that are 473 necessary to effectively reduce risk. 

474 Data-centric system threat modeling allows organizations to consider the security needs of each case of 475 interest, instead of relying solely on “best practice” generalized recommendations. Organizations are 476 already very familiar with applying best practices to operating systems and individual applications, such 477 as securing a web server (host) or web server software. What is considerably more challenging for 478 organizations to tackle is determining how to secure a particular chunk of data. It is not that securing a 479 piece of data is so difficult, but that traditionally security professionals, system administrators, and others 480 responsible for securing operational systems have focused on securing systems, not data. The rest of this 481 publication focuses on data security. 

482 This differentiation between system and data security has parallels to existing NIST publications. A 483 system security approach starts with a FIPS 199 [6] low/moderate/high impact rating for a system, and 484 then selects the corresponding security controls from NIST SP 800-53 [7]. In contrast, a data security 485 approach starts with a publication such as NIST SP 800-60 [8] for categorizing the type of information. 

486 

10 

NIST SP 800-154 (DRAFT) 

GUIDE TO DATA-CENTRIC SYSTEM THREAT MODELING 

### 487 **<mark>4. Basics of Data-Centric System Threat Modeling</mark>** 

488 Data-centric system threat modeling brings together the attack and defense side information for data of 489 interest in a standardized model that facilitates security analysis, decision making, and change planning. 490 This section provides information on the fundamentals of data-centric system threat modeling. This 491 publication is not trying to define a new threat modeling methodology, but rather to educate organizations 492 on the fundamentals of data-centric system threat modeling and to make recommendations related to the 493 use of this type of modeling. 

494 

- The data-centric system threat modeling approach presented in this publication has four major steps: 

495 

1. Identify and characterize the system and data of interest; 

496 

2. Identify and select the attack vectors to be included in the model; 

497 

3. Characterize the security controls for mitigating the attack vectors; and 

498 

4. Analyze the threat model. 

499 Sections 4.1 through 4.4 provide more information on performing each of these steps. Each step is also 500 illustrated by examples, which are denoted by a border around the text. The same example is continued 501 throughout all of the steps. Note that the data presented in the example is hypothetical and meant solely 502 for providing a simplified illustration of the steps. 

503 Section 4.5 explains in detail that this approach to data-centric system threat modeling is intended to be 504 customized to meet the needs of each organization, and it shows how easily this customization can occur. 

505 

#### **4.1 Step 1: Identify and Characterize the System and Data of Interest** 

506 The first step is to identify and characterize the system and data of interest. The system and data should be 507 defined narrowly, pertaining to a particular logical set of data on a particular host or small group of 508 closely related hosts and devices. 

509 Once the system and data are defined, they need to be characterized, which refers to understanding the 510 system’s operation and usage to the extent needed for the organization’s data-centric system threat 511 modeling approach. **At an absolute minimum, characterization should include the following:** 

512 513 

514 

- **The authorized locations for the data within the system.**<sup>4</sup> This will include some or all of the following: 

   - _Storage_ : all places where data may be at rest within the system boundaries; 

515 516 

- _Transmission_ : all ways in which data may transit over networks between system components and across the system’s boundaries; 

517 518 

- _Execution environment_ : e.g., data held in local memory during runtime, data processed by virtual CPUs, etc.; 

519 

- _Input_ : e.g., data typed in using the keyboard; and 

> 4 The methodology identifies just the authorized locations because someone with access to the data could store, transmit, output, or otherwise place the data in any accessible location, authorized or not, including locations outside the system boundaries. 

11 

NIST SP 800-154 (DRAFT) 

GUIDE TO DATA-CENTRIC SYSTEM THREAT MODELING 

521 

529 530 

- 520 `o` _Output_ : e.g., data printed to a physically attached printer, data displayed on the laptop screen, 521 etc. 

522 

523 

- 524 

525 

526 

527 

528 

531 532 533 534 

535 536 537 538 

539 540 

541 542 

543 

544 545 

546 547 

- **A basic understanding of how the data moves within the system between authorized locations.** For example, a file might be held in memory while it is being created and is only written out to storage when the user directs the system to do so. Depending on the complexity of the system, gaining this understanding may require first understanding the system’s functions and processes, users and usage scenarios, workflows, trust assumptions, and other aspects of people, processes, and technology related to the system. 

- **The security objectives (e.g., confidentiality, integrity, availability) for the data.** In many cases, some objectives are more important than others; in other cases, an organization may want to focus on a single objective for a particular threat model.<sup>5</sup> 

- **The people and processes who are authorized to access the data in a way that could affect the security objectives.** For example, if an organization has selected confidentiality as its sole objective for a particular threat model, the authorized people and processes should include all users, administrators, applications, services, etc. who are allowed to read the data. 

#### **Example Scenario** 

**Summary:** The data of interest is a spreadsheet containing personally identifiable information (PII) for employees who have received workers’ compensation. 

The system of interest comprises: 

- a human resource specialist’s laptop (spreadsheet is stored on and used from the laptop); 

- a USB flash drive (spreadsheet is backed up onto the USB flash drive); and 

- a printer (spreadsheet can be printed from the laptop to the printer). 

The authorized locations for the data of interest are as follows: 

- Storage: Spreadsheet kept on a laptop hard drive, backup of spreadsheet kept on a USB flash drive; 

- Transmission: Sent to a printer over a wireless network; 

- Execution environment: Local laptop memory and processors; 

- Input: Typed in using the laptop keyboard; and 

- Output: Displayed to the screen. 

548 549 **Description:** Data is input through the keyboard into the spreadsheet, which is temporarily held in the 550 execution environment. As the user updates the spreadsheet, the data is displayed to the screen. When the 551 user has completed editing the spreadsheet, the user directs the system to save the spreadsheet to the 552 laptop hard drive. The user may also load the spreadsheet into the execution environment and print the 553 spreadsheet to a nearby printer through a wireless network connection. Finally, the user occasionally 554 copies the latest version of the spreadsheet from the laptop hard drive to a USB flash drive as a backup. 

> 5 Some organizations may choose to replace the security objectives with one or more security requirements. Security requirements are more specific and granular than security objectives, and they often come directly from the organization’s policies or from regulations or security compliance initiatives that the organization is subject to. 

12 

NIST SP 800-154 (DRAFT) 

GUIDE TO DATA-CENTRIC SYSTEM THREAT MODELING 

- 555 Although confidentiality, integrity, and availability all matter for the data of interest, confidentiality is 556 considered so much more important that the organization has decided to perform its trust modeling in 557 terms of confidentiality only. 

- 558 In this highly simplified example, the human resource specialist is the only person who is authorized to 559 access the data. 

#### 560 **4.2 Step 2: Identify and Select the Attack Vectors to Be Included in the Model** 

561 The second step involves identifying the potential attack vectors, as discussed in Section 2.1.3, that could 562 be used to negatively impact one or more of the identified security objectives for one of the authorized 563 locations for the data. Once the attack vectors are identified, it may be necessary to select only a subset of 564 those attack vectors to be included in the threat model. Although it is generally preferable to include all 565 the attack vectors, there are often too many to be addressed with limited resources. Possible criteria to 566 consider include the relative likelihood of the attack vector being used and the most likely impact of a 567 successful attack. See Section 4.5 below for more information on the selection process. 

- **Location 1** : Stored in a spreadsheet on the local hard drive. 

568 

569 570 

- _Vector 1a_ : Attacker gains unauthorized physical access to the laptop, uses forensic tools or other utilities to copy the file (without authenticating to the OS). 

571 572 

- _Vector 1b_ : Attacker gains unauthorized physical access to the laptop, exploits vulnerabilities to gain OS access (impersonating user/admin). 

573 

- _Vector 1c_ : Attacker steals and reuses user/admin/service credentials. 

574 

- _Vector 1d_ : Attacker gains access to/control over user’s session/device. 

575 

- 575 • _Vector 1e_ : User forwards the file to an unauthorized recipient (user was tricked via social 576 engineering, user is malicious, user made a mistake, etc.). 

577 578 

   - _Vector 1f_ : Attacker accesses unsecured network service (e.g., connects to unsecured file share) and gains access to the file. 

- 579 580 

- **Location 2** : Stored in a spreadsheet on a flash drive backup. 

581 582 

- _Vector 2a_ : Attacker gains unauthorized physical access to the flash drive, mounts the drive and copies the file. 

583 584 

- _Vector 2b_ : Attacker steals and reuses user/admin/service credentials for laptop while flash drive is mounted. 

585 

   - _Vector 2c_ : Attacker gains access to/control over user’s session/device while flash drive is mounted. 

- 586 

- _Vector 2d_ : User forwards the file to an unauthorized recipient. 

587 

- 588 

   - **Location 3** : Printed to a nearby printer over a wireless network connection. 

- 589 • _Vector 3a_ : Attacker monitors unencrypted or weakly encrypted wireless network communications 590 and captures the data being sent to the printer. 

- 591 • _Vector 3b_ : Attacker views a printout of the spreadsheet. 

13 

NIST SP 800-154 (DRAFT) 

GUIDE TO DATA-CENTRIC SYSTEM THREAT MODELING 

- 592 593 **Location 4** : Processed locally. 594 • _Vector 4a_ : Attacker gains access to/control over user’s session/device. 595 596 **Location 5** : Input locally. 597 • _Vector 5a_ : Attacker watches the information being typed in to the laptop. 598 • _Vector 5b_ : Attacker uses keystroke logger on laptop to monitor keystrokes. 599 600 **Location 6** : Output locally. 601 • _Vector 6a_ : Attacker views the information on the laptop screen. 602 • _Vector 6b_ : Attacker uses malware on laptop to take screen shots. 603 604 **Selected attack vectors** (based on the possibility and the likelihood of each attack vector being used to 605 completely compromise confidentiality): 606 `o` _Vector 1c_ : Data is stored in a spreadsheet on the local hard drive; attacker steals and reuses 607 user/admin/service credentials. 608 `o` _Vector 1d_ : Data is stored in a spreadsheet on the local hard drive; attacker gains access to/control 609 over user’s session/device. 610 `o` _Vector 2b_ : Data is stored in a spreadsheet on a flash drive backup; attacker steals and reuses 611 user/admin/service credentials for laptop while flash drive is mounted. 612 `o` _Vector 2c_ : Data is stored in a spreadsheet on a flash drive backup; attacker gains access to/control 613 over user’s session/device while flash drive is mounted. 614 `o` _Vector 4a_ : Data is processed locally; attacker gains access to/control over user’s session/device. 

615 

616 

#### **4.3 Step 3: Characterize the Security Controls for Mitigating the Attack Vectors** 

617 The third step of the methodology is, for each attack vector selected in Step 2, to identify and document 618 security control alterations (additions to existing security controls, reconfigurations of existing security 619 controls, etc.) that would help mitigate the risk associated with the attack vector and that are reasonably 620 feasible to accomplish. Note that it is not necessarily to enumerate every single applicable control, such as 621 having a security program and policies, because these controls should already be in place for the entire 622 enterprise and are not normally customized to take a particular attack vector into consideration. 

- 623 Next, for each selected security control alteration, estimate how effectively it would address exploitation 624 of each applicable attack vector. This could be as simple as ranking effectiveness as low, medium, or 625 high, or as complex as estimating the percentage of attacks against the attack vector that would be stopped 626 by this mitigation. Whatever method is selected, it should be comparable across mitigations and attack 627 vectors. 

- 628 The counterpart to estimating the effectiveness of each security control alteration is estimating the 629 negative implications. Factors to consider may include cost (perhaps the order of magnitude or the range 630 of costs for acquisition and implementation, and for annual management/maintenance) and reductions in 631 functionality, usability, and performance. These can be particularly hard to determine accurately for 

14 

NIST SP 800-154 (DRAFT) 

GUIDE TO DATA-CENTRIC SYSTEM THREAT MODELING 

- 632 future mitigations, so it may be necessary to develop very rough estimates for them using a simple 633 low/medium/high type scale that is particular to the organization. 

- 634 **Feasible security control alterations** : 

- 635 

- 636 

- 637 

- 638 

- 639 

- 640 

- 641 

   1. Require strong password with strongly encrypted password hash (vectors _1c_ and _2b_ ). 

   - Effectiveness: Low 

   - Acquisition and implementation costs: Low 

   - Annual management/maintenance costs: Low 

   - Impact on functionality: Low 

   - Impact on usability: Low 

   - Impact on performance: Low 

- 642 

- 643 

- 644 

- 645 646 647 648 649 650 

   2. Require multifactor authentication (vectors _1c_ and _2b_ ) 

   - Effectiveness: High 

   - Acquisition and implementation costs: Moderate 

   - Annual management/maintenance costs: Moderate 

   - Impact on functionality: Low 

   - Impact on usability: Moderate 

   - Impact on performance: Low 

- 651 3. Use antivirus software, spam filtering, real-time blacklists, user awareness, web reputation software, 652 etc. (vectors _1c_ , _1d_ , _2b_ , _2c_ , and _4a_ ) 

- 653 • Effectiveness: Moderate 654 • Acquisition and implementation costs: Moderate 655 • Annual management/maintenance costs: Moderate 656 • Impact on functionality: Moderate 657 • Impact on usability: Moderate 658 • Impact on performance: Moderate 659 660 4. Patch vulnerabilities (vectors _1c_ , _1d_ , _2b_ , _2c_ , and _4a_ ) 661 • Effectiveness: Low 662 • Acquisition and implementation costs: Moderate 663 • Annual management/maintenance costs: Moderate 664 • Impact on functionality: Moderate 665 • Impact on usability: Low 666 • Impact on performance: Moderate 

15 

NIST SP 800-154 (DRAFT) 

GUIDE TO DATA-CENTRIC SYSTEM THREAT MODELING 

667 

668 

#### **4.4 Step 4: Analyze the Threat Model** 

669 The final step of the methodology is to analyze all the characteristics documented during the previous 670 steps, which collectively comprise the threat model, to assist in evaluating the effectiveness and efficiency 671 of each security control option against the selected attack vectors. It is far too simplistic to say that a 672 control should be applied because it lowers risk. In addition to their financial costs in terms of acquisition, 673 implementation, and management/maintenance, security controls can negatively impact functionality, 674 usability, and performance, among other factors. Any assessment of security controls should include 675 considerations of all significant relevant factors. 

676 The most challenging part of threat model analysis is determining how to consider all of these 677 characteristics together. It is straightforward to compare an individual characteristic, such as the annual 678 management/maintenance costs, across attack vectors and mitigations. However, it is not straightforward 679 at all to compare the entire set of characteristics for an attack vector against the entire set of 680 characteristics for another attack vector. Yet such comparisons are absolutely critical to determining how 681 risk can best be reduced across all the attack vectors, in a cost-effective manner that has an acceptable 682 negative impact on the organization’s operations. Each organization needs to determine how to compare 683 the characteristics for each attack vector/security control pair, as a basis for comparing attack vector 684 characteristics and security control characteristics. 

685 One approach to facilitating these comparisons is to assign scores and weightings to each characteristic. 686 For example, the narrative descriptions of threat consequence could be converted to numerical values on a 687 three-point scale. Three-point scales could also be used for other characteristics in place of low, medium, 688 and high ratings. Even complex characteristics, such as cost, could be mapped to a simple scale. 

689 In addition to assigning scores to each characteristic’s possible values or value ranges, the organization 690 also needs to consider the relative weights of each characteristic. Perhaps the effectiveness against attacks 691 is considered much more important than other characteristics; if so, this could be conveyed by doubling or 692 tripling its score. Similarly, all other characteristics could be assigned a multiplier that would increase or 693 decrease their scores or keep them the same. Then after applying the multipliers, the organization would 694 add up the results and have a relative score for each attack vector/security control pair. 

695 Another scoring approach that could be followed in addition to the previously described approach is to set 696 thresholds or rules for certain criteria and eliminate from further consideration any attack vector/security 697 control pairs that do not meet these. A simple example is eliminating all pairs that have a cost of $100,000 698 or more over a period of three years. A more complex example is eliminating all pairs that have a cost of 699 $50,000 or more over a period of three years AND a high impact on usability AND low or medium 700 effectiveness against attacks. 

- 701 After much debate, the organization decides to set the following scores for the characteristics and weigh 702 them all evenly: 

- 703 • No security control effectiveness = 0 

704 

   - Security control effectiveness of low = 1 

- 705 • Security control effectiveness of moderate = 2 

- 706 

   - Security control effectiveness of high = 3 

- 707 • Negative implication of high = 1 

16 

NIST SP 800-154 (DRAFT) 

GUIDE TO DATA-CENTRIC SYSTEM THREAT MODELING 

717 

718 

719 

- 708 • Negative implication of moderate = 2 

- 709 

   - Negative implication of low = 3 

- 710 The organization calculates the total of the negative implication scores for each security control (see first 711 table below), then multiplies these totals by the score of the security control effectiveness per attack 712 vector (see second table below) to reach a score for each attack vector/security control pair (see shaded 713 area of the second table below). The higher the score, the more “bang for the buck” the security control 714 will provide against the corresponding attack vector. This information is now ready for use in decision 715 making. 

- 716 

|**Possible Secur**|**ity C**|**ontrol**|**s**|||**Acquisition and**<br>**Implementation Costs**|**Annual Management/**<br>**Maintenance Costs**|**Impact on**<br>**Functionality**|**Impact on Usability**|**Impact on**<br>**Performance**|**Total for Security**<br>**Control**|
|---|---|---|---|---|---|---|---|---|---|---|---|
|Require strong password with str<br>hash|ongly|encryp|ted p|asswo|rd|3|3|3|3|3|**15**|
|Require multifactor authentication||||||2|2|3|2|3|**12**|
|Use antivirus software, spam filte<br>awareness, web reputation softwa|ring,<br>re, e|real-tim<br>tc.|e bla|cklists|, user|2|2|2|2|2|**10**|
|Patch vulnerabilities||||||2|2|2|3|2|**11**|
|**Possible Security Controls**||**Secur**<br>**Effecti**<br>**Atta**|**ity C**<br>**vene**<br>**ck Ve**|**ontrol**<br>**ss Per**<br>**ctor**|<br>|**Negative**<br>**Implication**<br>|<br>**Sec**<br>**Time**|**urity Co**<br>**s Negati**<br>**Per A**|**ntrol Ef**<br>**ve Imp**<br>**ttack V**|**fectiven**<br>**lication**<br>**ector**|**ess**<br>**Total**|
|||||||**Total**||||||
||**1c**|**1d**|**2b**|**2c**|**4a**||**1c**|**1d**|**2b**|**2c**|**4a**|
|Require strong password with<br>strongly encrypted password<br>hash|1|0|1|0|0|15|15|0|15|0|0|
|Require multifactor<br>authentication|3|0|3|0|0|12|36|0|36|0|0|
|Use antivirus software, spam<br>filtering, real-time blacklists,<br>user awareness, web<br>reputation software, etc.|2|2|2|2|2|10|20|20|20|20|20|
|Patch vulnerabilities|1|1|1|1|1|11|11|11|11|11|11|



#### **4.5 Customizing the Data-Centric System Threat Modeling Approach** 

720 This publication presents a primarily qualitative approach to data-centric system threat modeling. A 721 quantitative approach would lead to more precise and accurate results than a qualitative approach, but 722 quantitative approaches would also be much more resource-intensive and would not scale well for 723 modeling large and complex systems unless the metrics and methodologies are mostly automated. 724 Because such automation is not yet widely available, if at all, this publication focuses on qualitative 

724 

17 

NIST SP 800-154 (DRAFT) 

GUIDE TO DATA-CENTRIC SYSTEM THREAT MODELING 

725 modeling, which is still quite beneficial. In the future, as more automated quantitative metrics and 726 methodologies become available, organizations should reconsider the feasibility of using quantitative 727 modeling. 

728 Most of the actions within the methodology can be addressed in a wide variety of ways in terms of both 729 content (what information is captured) and format/structure (how that information is captured). There is 730 no “right” method, and the examples are purely illustrative. What is important is recording sufficient 731 information to provide the necessary input for subsequent steps and a basis for making actionable 732 recommendations. 

733 A prime example of the flexibility of the methodology is Step 2. Step 2 uses the list from Step 1 of 734 authorized locations for the data of interest. In the example, each attack vector is defined in a narrative 735 way, such as “Attacker gains unauthorized physical access to the laptop, uses forensic tools or other 736 utilities to copy the file (without authenticating to the OS).” This single statement actually conveys three 737 pieces of data: 1) a source of malicious content, 2) a potentially vulnerable processor of that malicious 738 content, and 3) the nature of the malicious content itself. 

739 Some organizations may prefer a more narrative approach to defining attack vectors because it is easier 740 for others to understand, while other organizations may want a more thorough or technically-based 741 approach and therefore want to go through the threat consequences and actions as a taxonomy for 742 identifying the attack vectors. And, of course, there are many other ways of defining attack vectors that 743 individual organizations may prefer to use because of existing processes and tools or for other reasons. 744 Another factor to consider is the granularity of the attack vectors; one organization may only have the 745 resources to consider the attack vectors at a truly high level, while another organization may want to do a 746 deep dive and make the attack vectors as narrow as possible. 

747 Organizations may also want to scope their threat modeling so it takes less effort. Using Step 2 as an 748 example, an organization may decide to eliminate any attack vectors that do not merit further 749 consideration. For example, an organization may decide that attack vectors with the lowest relative 750 likelihood should be ignored because there are far too many other attack vectors to be considered. 751 Similarly, an organization may only be interested (at least initially) in attack vectors that are likely to lead 752 to a complete compromise of confidentiality, integrity, and availability. Another possibility is to eliminate 753 attack vectors that do not have any feasible mitigations. Ideally an organization should analyze all attack 754 vectors before winnowing out any—for example, an unlikely attack vector may turn out to be incredibly 755 easy and inexpensive to mitigate, or a single mitigation may address multiple attack vectors—but 756 realistically this may not be feasible in some cases. 

757 Of course, an organization can skip any of the elements of the methodology that are not relevant for a 758 particular situation or environment, and likewise an organization can add characteristics if other factors 759 are also important to the organization. 

760 

18 

NIST SP 800-154 (DRAFT) 

GUIDE TO DATA-CENTRIC SYSTEM THREAT MODELING 

#### 761 

#### **<mark>Appendix A—Acronyms and Other Abbreviations</mark>** 

762 Selected acronyms and other abbreviations used in the guide are defined below. 

|**CMSS**|Common Misuse Scoring System|
|---|---|
|**CNSSI**|Committee on National Security Systems Instruction|
|**FIPS**|Federal Information Processing Standard|
|**FISMA**|Federal Information Security Modernization Act|
|**FOIA**|Freedom of Information Act|
|**HTML**|Hypertext Markup Language|
|**IA**|Information Assurance|
|**IR**|Interagency Report|
|**IT**|Information Technology|
|**ITL**|Information Technology Laboratory|
|**NIST**|National Institute of Standards and Technology|
|**OMB**|Office of Management and Budget|
|**OS**|Operating System|
|**PII**|Personally Identifiable Information|
|**RFC**|Request for Comments|
|**SCAP**|Security Content Automation Protocol|
|**SP**|Special Publication|
|**USB**|Universal Serial Bus|



763 

764 

19 

NIST SP 800-154 (DRAFT) 

GUIDE TO DATA-CENTRIC SYSTEM THREAT MODELING 

765 

#### **<mark>Appendix B—References</mark>** 

- 766 This appendix lists the references for the document. 

   - [1] E. LeMay, K. Scarfone, and P. Mell, National Institute of Standards and Technology (NIST) Interagency Report (IR) 7864, _The Common Misuse Scoring System (CMSS): Metrics for Software Feature Misuse Vulnerabilities_ , July 2012. <u>http://dx.doi.org/10.6028/NIST.IR.7864</u> 

   - [2] Joint Task Force Transformation Initiative, National Institute of Standards and Technology (NIST) Special Publication (SP) 800-30 Revision 1, _Guide for Conducting Risk Assessments_ , September 2012. <u>http://dx.doi.org/10.6028/NIST.SP.800-30r1</u> 

   - [3] Committee on National Security Systems (CNSS), CNSS Instruction No. 4009, _National Information Assurance (IA) Glossary_ , April 6, 2015. <u>https://www.cnss.gov/CNSS/issuances/Instructions.cfm</u> 

   - [4] K. Dempsey, N. Chawla, A. Johnson, R. Johnston, A. Jones, A. Orebaugh, M. Scholl, and K. Stine, National Institute of Standards and Technology (NIST) Special Publication (SP) 800137, _Information Security Continuous Monitoring (ISCM) for Federal Information Systems and Organizations_ , September 2011. <u>http://dx.doi.org/10.6028/NIST.SP.800-137</u> 

   - [5] S. Quinn, K. Scarfone, and D. Waltermire, National Institute of Standards and Technology (NIST) Special Publication (SP) 800-117 Revision 1 (Draft), _Guide to Adopting and Using the Security Content Automation Protocol (SCAP) Version 1.2_ , January 2012. <u>http://csrc.nist.gov/publications/PubsSPs.html#800-117-R1</u> 

   - [6] National Institute of Standards and Technology (NIST) Federal Information Processing Standard (FIPS) Publication (PUB) 199, _Standards for Security Categorization of Federal Information and Information Systems_ , February 2004. <u>http://csrc.nist.gov/publications/fips/fips199/FIPS-PUB-199-final.pdf</u> 

   - [7] Joint Task Force Transformation Initiative, National Institute of Standards and Technology (NIST) Special Publication (SP) 800-53 Revision 4, _Security and Privacy Controls for Federal Information Systems and Organizations_ , April 2013 (including updates as of January 22, 2015). <u>http://dx.doi.org/10.6028/NIST.SP.800-53r4</u> 

   - [8] K. Stine, R. Kissel, W. Barker, J. Fahlsing, and J. Gulick, National Institute of Standards and Technology (NIST) Special Publication (SP) 800-60 Revision 1, _Volume 1: Guide for Mapping Types of Information and Information Systems to Security Categories_ , August 2008. <u>http://dx.doi.org/10.6028/NIST.SP.800-60v1r1</u> 

767 

20 

