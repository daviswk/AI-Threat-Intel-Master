# SEALED ANSWER KEY: Module 1 (m01-risk-controls-independence)

Written by `first-line-engineer` from the generator's own output (`assurance-harness/generators/m01_iam.py`, SEED 20260930). Format: `spec/SCHEMAS.md` section 4.
Not to be shown to the learner before the gate's artifact check. `red-team` does not read it.

Datasets: `assurance-harness/data/m01/planted.duckdb` (all planted flaws below) and `assurance-harness/data/m01/clean.duckdb` (none of them; expected exceptions on every control = 0).
Observation period 2026-04-01 00:00:00 to 2026-09-30 23:59:59. Review campaigns 2026Q2 (population as at 2026-06-01 00:00:00, window to 2026-06-21) and 2026Q3 (as at 2026-09-01 00:00:00, window to 2026-09-21).

Identifier note (realistic constraint, present in BOTH datasets): `hr_identities.hr_id` holds the raw HR export identifier. Rows with `record_source = 'hris_legacy_import'` use legacy formats (`E-012345`, `e012345`, `E12345`, `012345`). `iam_accounts.hr_id`, `owner_hr_id`, `manager_hr_id` and all reviewer/approver columns use the canonical form: prefix letter plus 6 digits. Normalise with: strip, upper-case, drop '-', take the digits as an integer and match on the number (numbers are unique across E and C).
Legacy-format identities in planted/clean: 112.

---

## PF-01
- **id:** PF-01
- **type:** incomplete_population
- **where:** `access_reviews` (planted), both campaigns. The review list was built by an inner join of `iam_accounts.owner_hr_id` to `hr_identities.hr_id` on the exact string. Accounts whose owner's HR record carries a legacy-format identifier fall out of the join silently, so they were never put in front of a reviewer. The campaign still shows 100% completion because completion is measured against the list.
- **expected exceptions, 2026Q2:** 597 active accounts not reviewed (192 human, 405 service); list size 9156, population 9753.
  - ids (2026Q2):
    LDA100023, LDA100057, LDA102363, LDA103706, LDA103853, LDA104897, LDA107308, LDA107383
    LDA109147, LDA109444, LDA109493, LDA110560, LDA112269, LDA112306, LDA112348, LDA113637
    LDA115984, LDA117648, LDA118848, LDA119120, LDA119198, LDA121535, LDA121919, LDA121969
    LDA125329, LDA129029, LDA131347, LDA131543, LDA132253, LDA133094, LDA134206, LDA136249
    LDA140468, LDA143207, LDA144389, LDA145307, LDA146444, LDA146958, LDA147656, LDA148173
    LDA148586, LDA148596, LDA151830, LDA153672, LDA153800, LDA154326, LDA157088, LDA157878
    LDA158691, LDA160413, LDA162331, LDA162407, LDA162872, LDA164400, LDA166678, LDA168610
    LDA172543, LDA173178, LDA173620, LDA174056, LDA174151, LDA174221, LDA179479, LDA179739
    LDA180918, LDA183185, LDA183508, LDA184990, LDA192645, LDA199962, LDA203353, LDA205411
    LDA206132, LDA207181, LDA207259, LDA208457, LDA209917, LDA215590, LDA216324, LDA216695
    LDA217102, LDA221769, LDA224055, LDA226968, LDA227960, LDA231196, LDA231740, LDA233377
    LDA235417, LDA236834, LDA240058, LDA240610, LDA247626, LDA248202, LDA248718, LDA249128
    LDA251017, LDA251535, LDA251559, LDA252117, LDA252195, LDA252420, LDA256053, LDA258206
    LDA259391, LDA259681, LDA260935, LDA262431, LDA268147, LDA271248, LDA273679, LDA274602
    LDA277088, LDA277924, LDA281510, LDA283097, LDA283125, LDA283188, LDA285519, LDA286161
    LDA287265, LDA289975, LDA290082, LDA291596, LDA292400, LDA292899, LDA293006, LDA293802
    LDA294806, LDA296964, LDA297840, LDA298840, LDA299263, LDA302537, LDA304131, LDA305019
    LDA309419, LDA310218, LDA310277, LDA310602, LDA311279, LDA311400, LDA311795, LDA314033
    LDA315196, LDA319303, LDA320425, LDA322203, LDA326111, LDA326619, LDA332196, LDA332518
    LDA334965, LDA339171, LDA339819, LDA341598, LDA343797, LDA345422, LDA345454, LDA345620
    LDA346134, LDA348645, LDA349615, LDA351590, LDA352482, LDA355178, LDA355831, LDA356390
    LDA359051, LDA359249, LDA361187, LDA361363, LDA362254, LDA364537, LDA370637, LDA370769
    LDA371706, LDA374398, LDA375247, LDA379105, LDA382401, LDA384947, LDA386282, LDA386436
    LDA387833, LDA388246, LDA389217, LDA390145, LDA390187, LDA390226, LDA390385, LDA390554
    LDA391007, LDA394289, LDA395854, LDA396185, LDA399283, LDA399453, LDA400426, LDA402349
    LDA402553, LDA404605, LDA405529, LDA405748, LDA407669, LDA410081, LDA412595, LDA415807
    LDA416451, LDA416736, LDA417078, LDA417531, LDA421400, LDA421649, LDA422027, LDA423574
    LDA426055, LDA426421, LDA427872, LDA429417, LDA430125, LDA430157, LDA431468, LDA435134
    LDA435310, LDA438940, LDA440311, LDA441124, LDA441149, LDA441566, LDA443054, LDA448945
    LDA451737, LDA455645, LDA456457, LDA460241, LDA466883, LDA467494, LDA468494, LDA470050
    LDA470750, LDA471119, LDA471447, LDA472085, LDA472542, LDA473423, LDA475388, LDA475590
    LDA475907, LDA476035, LDA476412, LDA477626, LDA483883, LDA485502, LDA486504, LDA488435
    LDA491717, LDA492546, LDA493972, LDA494924, LDA498554, LDA505242, LDA505291, LDA505769
    LDA505855, LDA506912, LDA507488, LDA510526, LDA510653, LDA515427, LDA516122, LDA517268
    LDA519101, LDA521588, LDA525404, LDA527327, LDA528943, LDA529031, LDA533459, LDA534154
    LDA539872, LDA542490, LDA545200, LDA546126, LDA549028, LDA549104, LDA549219, LDA549587
    LDA550444, LDA550822, LDA551383, LDA552096, LDA553441, LDA556647, LDA557242, LDA559876
    LDA559969, LDA560420, LDA560614, LDA561305, LDA563022, LDA563453, LDA564225, LDA565459
    LDA566671, LDA568137, LDA571470, LDA573224, LDA574335, LDA575746, LDA587619, LDA589456
    LDA591105, LDA593169, LDA594020, LDA595115, LDA598433, LDA603142, LDA605811, LDA606261
    LDA608023, LDA611053, LDA613334, LDA618292, LDA618306, LDA618425, LDA619289, LDA619383
    LDA619727, LDA620947, LDA622273, LDA624367, LDA625245, LDA627541, LDA628878, LDA628894
    LDA630154, LDA630704, LDA632137, LDA632249, LDA632379, LDA632473, LDA632800, LDA632842
    LDA633848, LDA635233, LDA639262, LDA641973, LDA645257, LDA645632, LDA646849, LDA649004
    LDA649504, LDA649509, LDA650918, LDA651966, LDA652600, LDA656060, LDA656104, LDA656164
    LDA657421, LDA658068, LDA660898, LDA661173, LDA662281, LDA662533, LDA662896, LDA666817
    LDA666924, LDA670387, LDA673147, LDA673458, LDA673641, LDA676390, LDA677136, LDA680404
    LDA682235, LDA688573, LDA689961, LDA690609, LDA691387, LDA692347, LDA693234, LDA694161
    LDA695167, LDA695665, LDA697598, LDA700480, LDA701014, LDA701687, LDA702176, LDA702219
    LDA702990, LDA704451, LDA708296, LDA710706, LDA711071, LDA711167, LDA711588, LDA712627
    LDA713731, LDA714374, LDA715766, LDA717481, LDA717890, LDA718979, LDA720492, LDA721399
    LDA723999, LDA727238, LDA729916, LDA734968, LDA736398, LDA736672, LDA737711, LDA738032
    LDA738415, LDA738743, LDA738860, LDA742162, LDA743136, LDA743507, LDA745033, LDA746896
    LDA751402, LDA751458, LDA753085, LDA753315, LDA753562, LDA754552, LDA758456, LDA761483
    LDA764168, LDA766937, LDA767235, LDA769033, LDA769278, LDA771107, LDA774396, LDA775229
    LDA775512, LDA776718, LDA778040, LDA778193, LDA778341, LDA778372, LDA778601, LDA779348
    LDA780388, LDA781076, LDA782866, LDA783944, LDA785042, LDA786462, LDA786717, LDA786961
    LDA788846, LDA789776, LDA791387, LDA792531, LDA793418, LDA793517, LDA794024, LDA794078
    LDA802635, LDA804021, LDA809011, LDA811612, LDA812529, LDA816178, LDA819181, LDA819653
    LDA822726, LDA822844, LDA823959, LDA824486, LDA824652, LDA826469, LDA827311, LDA835541
    LDA836105, LDA838475, LDA840645, LDA844797, LDA846264, LDA848594, LDA849801, LDA854435
    LDA855467, LDA856118, LDA857404, LDA857883, LDA861275, LDA861414, LDA864554, LDA864671
    LDA867617, LDA867618, LDA869123, LDA869640, LDA871471, LDA876706, LDA877053, LDA880142
    LDA880513, LDA880533, LDA881042, LDA881235, LDA881948, LDA884784, LDA885529, LDA885949
    LDA886663, LDA888050, LDA889517, LDA890691, LDA892166, LDA893225, LDA893375, LDA894158
    LDA894651, LDA894758, LDA894896, LDA895023, LDA896646, LDA900137, LDA900144, LDA901858
    LDA905267, LDA908624, LDA909610, LDA910759, LDA911337, LDA912578, LDA912656, LDA913011
    LDA914070, LDA914258, LDA914387, LDA914662, LDA915765, LDA919678, LDA920710, LDA922304
    LDA924177, LDA926341, LDA927478, LDA928760, LDA935992, LDA937354, LDA939483, LDA939804
    LDA940751, LDA943094, LDA944819, LDA945167, LDA949909, LDA950035, LDA954397, LDA956922
    LDA957690, LDA958601, LDA959454, LDA959765, LDA960704, LDA961429, LDA962542, LDA963809
    LDA965978, LDA970145, LDA970673, LDA970774, LDA971015, LDA972095, LDA973649, LDA974076
    LDA978906, LDA979955, LDA980340, LDA982338, LDA983121, LDA983928, LDA984598, LDA985181
    LDA986110, LDA987264, LDA987875, LDA988632, LDA988923, LDA988984, LDA990754, LDA991041
    LDA993387, LDA994252, LDA998915, LDA999184, LDA999614
- **expected exceptions, 2026Q3:** 624 active accounts not reviewed (187 human, 437 service); list size 9831, population 10455.
  - ids (2026Q3):
    LDA100023, LDA100057, LDA102363, LDA103706, LDA103853, LDA104897, LDA107291, LDA107308
    LDA107383, LDA109147, LDA109444, LDA109493, LDA110560, LDA112269, LDA112306, LDA112348
    LDA113637, LDA115984, LDA117648, LDA118848, LDA119120, LDA119198, LDA121535, LDA121919
    LDA121969, LDA125329, LDA129029, LDA131347, LDA131543, LDA132253, LDA133094, LDA134206
    LDA136249, LDA143207, LDA144389, LDA145307, LDA146444, LDA146958, LDA147656, LDA148173
    LDA148586, LDA148596, LDA151830, LDA153672, LDA153800, LDA154326, LDA157088, LDA157878
    LDA158691, LDA160413, LDA162331, LDA162407, LDA162872, LDA164400, LDA166678, LDA168610
    LDA171333, LDA172543, LDA173620, LDA174056, LDA174151, LDA174221, LDA179479, LDA179739
    LDA180918, LDA183185, LDA183508, LDA184990, LDA192028, LDA192645, LDA199962, LDA203353
    LDA204322, LDA205377, LDA205411, LDA206132, LDA207181, LDA207259, LDA208457, LDA208796
    LDA209917, LDA215394, LDA215590, LDA216324, LDA216695, LDA217102, LDA221769, LDA224055
    LDA226968, LDA227960, LDA231196, LDA231740, LDA233377, LDA235417, LDA236834, LDA240058
    LDA240610, LDA247626, LDA248202, LDA248718, LDA249128, LDA251017, LDA251535, LDA251559
    LDA252117, LDA252195, LDA252420, LDA256053, LDA258206, LDA259391, LDA259681, LDA260935
    LDA262431, LDA268147, LDA269109, LDA271248, LDA273679, LDA274602, LDA277088, LDA277924
    LDA281510, LDA282796, LDA283097, LDA283125, LDA283188, LDA285519, LDA286161, LDA287265
    LDA289975, LDA290082, LDA291596, LDA292400, LDA292899, LDA292973, LDA293006, LDA293802
    LDA294806, LDA295381, LDA296964, LDA297840, LDA298840, LDA299263, LDA302537, LDA304131
    LDA305019, LDA309419, LDA310218, LDA310277, LDA310602, LDA311279, LDA311400, LDA311795
    LDA314033, LDA315196, LDA319303, LDA320425, LDA322203, LDA326111, LDA326619, LDA332196
    LDA332518, LDA334965, LDA339171, LDA339819, LDA341598, LDA343797, LDA345422, LDA345454
    LDA345620, LDA346134, LDA348645, LDA349615, LDA351590, LDA352482, LDA355831, LDA356390
    LDA359051, LDA359249, LDA361187, LDA361363, LDA362254, LDA364537, LDA370637, LDA370769
    LDA371706, LDA374398, LDA375247, LDA379105, LDA379792, LDA382401, LDA384947, LDA386282
    LDA386436, LDA387833, LDA388246, LDA389217, LDA390145, LDA390187, LDA390226, LDA390385
    LDA390554, LDA391007, LDA394289, LDA395854, LDA396185, LDA399283, LDA399453, LDA400426
    LDA402349, LDA402553, LDA404605, LDA405529, LDA405748, LDA406589, LDA407669, LDA410081
    LDA412595, LDA415807, LDA416451, LDA416736, LDA417078, LDA417531, LDA421400, LDA421649
    LDA422027, LDA423574, LDA426055, LDA426421, LDA429417, LDA430125, LDA430157, LDA431468
    LDA433882, LDA435134, LDA435310, LDA438940, LDA440311, LDA441124, LDA441149, LDA441566
    LDA443054, LDA448945, LDA451737, LDA455645, LDA456457, LDA460241, LDA467494, LDA468494
    LDA470050, LDA470750, LDA471119, LDA471447, LDA472085, LDA472542, LDA473423, LDA474857
    LDA475388, LDA475590, LDA475906, LDA475907, LDA476035, LDA476412, LDA476415, LDA477626
    LDA480493, LDA483883, LDA485502, LDA486504, LDA488435, LDA491717, LDA492546, LDA493972
    LDA494924, LDA498554, LDA505242, LDA505291, LDA505769, LDA505855, LDA506912, LDA507488
    LDA510526, LDA510653, LDA514525, LDA515427, LDA516122, LDA517268, LDA519101, LDA521588
    LDA525404, LDA527327, LDA528943, LDA529031, LDA533459, LDA534154, LDA539872, LDA542490
    LDA545200, LDA546126, LDA549028, LDA549104, LDA549219, LDA549587, LDA550444, LDA550822
    LDA551383, LDA552096, LDA553441, LDA556647, LDA557242, LDA559197, LDA559876, LDA559969
    LDA560420, LDA560614, LDA561305, LDA563022, LDA563453, LDA564225, LDA565459, LDA566671
    LDA568137, LDA569487, LDA571470, LDA573224, LDA574335, LDA575746, LDA587619, LDA589456
    LDA591105, LDA593169, LDA594020, LDA595115, LDA597807, LDA598433, LDA605811, LDA606261
    LDA608023, LDA611053, LDA612334, LDA613334, LDA618292, LDA618306, LDA618425, LDA619289
    LDA619383, LDA619727, LDA620947, LDA622273, LDA624367, LDA625245, LDA627541, LDA628878
    LDA628894, LDA630154, LDA630704, LDA632137, LDA632249, LDA632379, LDA632473, LDA632800
    LDA632842, LDA633848, LDA635233, LDA639262, LDA641973, LDA645257, LDA645632, LDA646849
    LDA649004, LDA649504, LDA649509, LDA650918, LDA651966, LDA652600, LDA656060, LDA656104
    LDA656164, LDA657421, LDA658068, LDA660898, LDA661173, LDA662281, LDA662533, LDA662896
    LDA666817, LDA666924, LDA670387, LDA673147, LDA673458, LDA673641, LDA676390, LDA677136
    LDA680404, LDA682235, LDA684251, LDA688573, LDA689961, LDA690609, LDA691387, LDA692347
    LDA693234, LDA694161, LDA695167, LDA695665, LDA697598, LDA700480, LDA701014, LDA702176
    LDA702219, LDA702990, LDA704451, LDA708296, LDA710706, LDA711071, LDA711167, LDA711588
    LDA712627, LDA713731, LDA714374, LDA714839, LDA715766, LDA717481, LDA717890, LDA718979
    LDA720492, LDA721399, LDA723999, LDA727238, LDA729916, LDA734968, LDA736398, LDA736672
    LDA738032, LDA738415, LDA738743, LDA738860, LDA742162, LDA743136, LDA743507, LDA745033
    LDA745613, LDA746896, LDA751402, LDA751458, LDA753085, LDA753315, LDA753562, LDA754552
    LDA758456, LDA761483, LDA763893, LDA764168, LDA766937, LDA767235, LDA769033, LDA771107
    LDA774396, LDA775229, LDA775512, LDA776718, LDA778040, LDA778193, LDA778341, LDA778372
    LDA778601, LDA779348, LDA780388, LDA781076, LDA782866, LDA783944, LDA786462, LDA786717
    LDA786961, LDA788452, LDA788846, LDA789776, LDA791387, LDA792531, LDA793418, LDA793517
    LDA794024, LDA794078, LDA802635, LDA804021, LDA809011, LDA811612, LDA812529, LDA816178
    LDA819181, LDA819653, LDA822726, LDA822844, LDA823959, LDA824486, LDA824652, LDA826469
    LDA827311, LDA835541, LDA836105, LDA838475, LDA840645, LDA844797, LDA846264, LDA848594
    LDA849801, LDA849914, LDA854435, LDA855467, LDA856118, LDA857404, LDA857883, LDA858361
    LDA859240, LDA861275, LDA861414, LDA864554, LDA864671, LDA867617, LDA867618, LDA869123
    LDA869640, LDA871471, LDA876706, LDA876913, LDA877053, LDA880142, LDA880513, LDA881042
    LDA881235, LDA881948, LDA884784, LDA885529, LDA885949, LDA885974, LDA886663, LDA888050
    LDA889517, LDA890691, LDA892166, LDA893225, LDA893375, LDA894158, LDA894651, LDA894758
    LDA894896, LDA895023, LDA896646, LDA900020, LDA900137, LDA900144, LDA901858, LDA905267
    LDA908624, LDA909610, LDA910759, LDA911337, LDA912578, LDA912656, LDA913011, LDA914070
    LDA914258, LDA914387, LDA914662, LDA915765, LDA919678, LDA920710, LDA922304, LDA924177
    LDA926341, LDA927262, LDA927478, LDA928425, LDA928760, LDA934227, LDA937354, LDA939483
    LDA939804, LDA940751, LDA942345, LDA943094, LDA944819, LDA945167, LDA949909, LDA950035
    LDA954397, LDA956922, LDA957690, LDA958601, LDA959454, LDA959765, LDA960704, LDA961429
    LDA962542, LDA963407, LDA963809, LDA965978, LDA970145, LDA970673, LDA970774, LDA971015
    LDA972095, LDA973649, LDA974076, LDA978906, LDA979955, LDA980340, LDA982338, LDA983121
    LDA983928, LDA984598, LDA985181, LDA986110, LDA987264, LDA987875, LDA988632, LDA988923
    LDA988984, LDA990754, LDA991041, LDA993387, LDA994252, LDA998915, LDA999184, LDA999614
- **which control it defeats:** LD-AC-03 (AC-2, CA-7).
- **detection:** reconcile each campaign's reviewed accounts to `iam_accounts` active at the population date (created_at < as-at and (disabled_at is null or disabled_at >= as-at)). Clean: 0 unreviewed.

---

## PF-02
- **id:** PF-02
- **type:** drift
- **where:** `iam_accounts.disabled_at` against `hr_identities.termination_ts` for leavers in the period (planted). The share of leavers disabled more than 24 hours after termination rises month by month (target rates Apr..Sep: 2%, 4%, 8%, 15%, 25%, 38%), and the lag of on-time disables creeps up too (about +36 minutes per month). Some September leavers are still active at period end.
- **PF-02 exception leavers / all leavers in the period, by termination month:** Apr 0/32; May 0/36; Jun 3/34; Jul 4/39; Aug 9/31; Sep 22/52. Denominators are the literal population: every `hr_identities` row in `planted.duckdb` with `termination_ts` from 2026-04-01 00:00:00 up to (not including) 2026-10-01 00:00:00, 224 in total. 3 of those leavers are accounted for under PF-03 (their accounts were never disabled) and are therefore not counted as PF-02 exceptions; the numerators count PF-02 exception leavers only and use the same exception rows as the totals below.
- **expected exceptions:** 67 human accounts belonging to 38 leavers: 62 disabled more than 24h after termination, 5 still active at period end with termination more than 24h before it.
  - an exact-string join of `iam_accounts.hr_id` to `hr_identities.hr_id` finds only 64 of these (the rest belong to legacy-format HR records).
  - late (account_id, hours after termination):
    LDA145755 (158.1h), LDA165653 (157.6h), LDA168727 (149.8h), LDA188463 (116.4h), LDA192205 (61.9h)
    LDA214875 (105.4h), LDA299577 (29.4h), LDA306450 (64.8h), LDA308618 (136.3h), LDA316885 (145.2h)
    LDA319355 (75.8h), LDA319478 (95.0h), LDA326607 (89.9h), LDA326770 (76.1h), LDA347959 (171.9h)
    LDA348786 (59.1h), LDA362588 (66.2h), LDA383602 (29.0h), LDA390589 (92.9h), LDA399679 (66.0h)
    LDA405274 (152.3h), LDA436040 (94.9h), LDA438494 (145.0h), LDA459875 (29.2h), LDA506803 (173.7h)
    LDA508992 (42.6h), LDA526486 (88.1h), LDA534580 (121.1h), LDA576470 (90.8h), LDA587892 (30.2h)
    LDA590435 (173.7h), LDA608027 (27.4h), LDA617783 (91.1h), LDA626756 (157.9h), LDA642340 (61.7h)
    LDA651245 (118.8h), LDA652318 (30.5h), LDA653865 (136.8h), LDA662150 (114.4h), LDA673641 (155.1h)
    LDA682843 (116.4h), LDA692846 (37.7h), LDA701697 (42.7h), LDA702219 (155.4h), LDA703653 (61.9h)
    LDA712627 (155.2h), LDA749823 (67.1h), LDA783134 (89.5h), LDA790346 (64.9h), LDA793117 (88.3h)
    LDA801145 (78.7h), LDA814557 (29.3h), LDA838935 (97.3h), LDA840968 (150.0h), LDA852206 (171.7h)
    LDA865175 (105.8h), LDA874291 (37.8h), LDA914775 (64.8h), LDA925753 (66.2h), LDA929353 (88.1h)
    LDA980746 (42.3h), LDA988100 (29.7h)
  - not disabled:
    LDA127053, LDA331817, LDA462992, LDA477480, LDA860386
  - leavers (canonical hr_id): C025554, C028885, C032509, C033307, C036702, C037144, C045404, C048348, C052420, C052590, C053795, C076053, C089594, E010922, E013812, E016861, E018908, E019402, E024055, E026571, E027274, E028152, E030382, E036417, E037378, E040435, E045017, E052389, E053099, E060775, E062101, E070289, E072642, E074361, E082297, E089446, E089816, E093436
- **which control it defeats:** LD-AC-02 (AC-2).
- **detection:** full population of leavers (normalised identifiers) against disable timestamps; trend by month. Clean: every leaver's human accounts disabled within 24h (max lag about 20.5h).

---

## PF-03
- **id:** PF-03
- **type:** planted_exception
- **where:** three contractors terminated in April-May 2026 in `hr_identities` (planted) whose accounts were never disabled and kept authenticating after termination (`auth_events`). This is the dilemma's 'contractor who left in the spring'. Two of the three have legacy-format HR identifiers, so an exact join misses them, and the access review (PF-01) never listed their accounts. The third is canonical; its account was certified by the line manager in the review(s) after the person left.
  - C067668 (HR export id `C67668`), terminated 2026-04-12 16:28:33; accounts LDA251535, LDA660898; 26 successful logins after termination, last 2026-09-23 09:31:19; certified in campaigns: none (not on list).
  - C089779 (HR export id `089779`), terminated 2026-05-24 16:46:38; accounts LDA618306, LDA619727; 24 successful logins after termination, last 2026-09-27 14:07:36; certified in campaigns: none (not on list).
  - C043480 (HR export id `C043480`), terminated 2026-05-22 16:00:05; accounts LDA632068, LDA918645; 23 successful logins after termination, last 2026-09-30 17:09:37; certified in campaigns: 2026Q2, 2026Q3.
- **expected exceptions:** 6 accounts not disabled (ids: LDA251535, LDA618306, LDA619727, LDA632068, LDA660898, LDA918645); 4 `access_reviews` rows with decision 'certify' dated after the holder's HR termination (ids: RV-2026Q2-005411, RV-2026Q2-008365, RV-2026Q3-005816, RV-2026Q3-008985). These are the only certify-after-termination rows in planted; clean has none.
- **which control it defeats:** LD-AC-02 (AC-2); also LD-AC-03 (a departed person's account certified, or not reviewed at all).

---

## PF-04
- **id:** PF-04
- **type:** missing_inventory
- **where:** 16 accounts that exist in `entitlements` and `auth_events` (planted) but have no row in `iam_accounts` and no `access_requests`. Backstory: created directly in the directory backend during an integration cut-over and never registered in IAM. Their entitlements carry `approval_ref` NULL and `granted_by` = `LDA861191` (an IAM admin account). Account ids are random, so there is no sequence gap in `iam_accounts`; `access_requests` ids have gaps where their requests were removed.
  - LDA115457 (human, reporting, username `ezamora.rpt`): 1 entitlements, 5 auth events
  - LDA122153 (service, integration, username `svc-int-01310`): 2 entitlements, 8 auth events
  - LDA145689 (service, integration, username `svc-int-04070`): 2 entitlements, 7 auth events
  - LDA205680 (service, integration, username `svc-sync-00599`): 4 entitlements, 9 auth events
  - LDA208946 (service, integration, username `svc-bot-03115`): 3 entitlements, 7 auth events
  - LDA268355 (human, reporting, username `clockwood2.rpt`): 1 entitlements, 3 auth events
  - LDA279463 (human, reporting, username `vthistlewood.rpt`): 3 entitlements, 6 auth events
  - LDA413676 (service, integration, username `svc-int-05724`): 3 entitlements, 9 auth events
  - LDA422590 (service, integration, username `svc-int-03251`): 4 entitlements, 11 auth events
  - LDA490838 (service, integration, username `svc-mailer-05757`): 3 entitlements, 10 auth events
  - LDA493845 (service, integration, username `svc-int-03052`): 4 entitlements, 14 auth events
  - LDA560975 (human, reporting, username `ddelacroix2.rpt`): 1 entitlements, 3 auth events
  - LDA670252 (service, integration, username `svc-int-06340`): 4 entitlements, 9 auth events
  - LDA853610 (human, sandbox, username `fjuniper5.sbx`): 3 entitlements, 5 auth events
  - LDA869952 (service, integration, username `svc-int-00414`): 2 entitlements, 10 auth events
  - LDA973671 (service, integration, username `svc-sync-00040`): 2 entitlements, 7 auth events
- **expected exceptions:** 16 account ids (above); 42 entitlement rows with no approval reference; 123 auth events from accounts outside the inventory.
- **which control it defeats:** LD-AC-03 (population: never reviewed because not in the system of record); also LD-AC-01 (grants with no approval).
- **detection:** reconcile distinct `account_id` in `entitlements` and `auth_events` to `iam_accounts`. Clean: every account id in every table exists in `iam_accounts`.

---

## PF-05
- **id:** PF-05
- **type:** planted_exception
- **where:** `access_requests` rows of type `sod_exception` and `privileged_nomination` (planted) whose `expires_at` fell inside the period, while the covered entitlements stayed active to period end. In clean every exception expires 2026-12-31 and every nomination 2027-03-31.
  - REQ0025917 sod_exception `refund.issue+refund.approve` for E045322 (account LDA253688), expired 2026-05-31 23:59:59
  - REQ0026326 sod_exception `refund.issue+refund.approve` for E027610 (account LDA133396), expired 2026-06-30 23:59:59
  - REQ0026476 sod_exception `refund.issue+refund.approve` for E053071 (account LDA533760), expired 2026-07-31 23:59:59
  - REQ0027422 sod_exception `refund.issue+refund.approve` for E052217 (account LDA431988), expired 2026-08-31 23:59:59
  - REQ0026533 sod_exception `iam.admin+auditlog.admin` for E031776 (account LDA907585), expired 2026-09-15 23:59:59
  - REQ0028317 privileged_nomination `iam.admin` for E041979 (account LDA169876), expired 2026-06-30 23:59:59
  - REQ0028330 privileged_nomination `tenant.config` for E037285 (account LDA331989), expired 2026-07-31 23:59:59
  - REQ0028350 privileged_nomination `iam.admin` for E059824 (account LDA947561), expired 2026-08-31 23:59:59
- **expected exceptions:** 5 identities holding a toxic pair under a lapsed exception (LD-AC-04); 3 privileged holdings whose named-owner nomination lapsed (LD-AC-05).
- **which control it defeats:** LD-AC-04 (AC-5) and LD-AC-05 (AC-6).

---

## PF-06
- **id:** PF-06
- **type:** survivorship
- **where:** `auth_events` (planted). The telemetry export only carries events for accounts that are not disabled at export time; when an account is disabled its history drops out. Every disabled account has zero events, including accounts that were active for months of the period, and the late-disabled leavers in PF-02. The only post-termination activity that survives is from accounts that were never disabled (PF-03). `event_id` is assigned before the export filter, so the sequence has gaps.
- **expected:** 4716 events removed across 785 accounts; 785 accounts disabled during the period, of which 785 have zero auth events. Clean: every account disabled during the period has at least one event before its disable time, and `event_id` is contiguous (7000001 upward).
- **which control it defeats:** the evidence for LD-AC-02 (any test of whether late-disabled accounts were used after termination returns a false 'no use') and the CA-7 monitoring claim under LD-AC-03.

---

## PF-07 (stage 1 contrastive pair)
- **id:** PF-07
- **type:** incomplete_population
- **flawed package:** `evidence/q3_access_review/package_B/` (system of record `data/q3_review_snapshot_B.duckdb`). Reconciling package: `package_A/`.
- **where:** the package's `review_decisions.csv` and that snapshot's `access_reviews` for 2026Q3. List size 9855; active accounts in `iam_accounts` at 2026-09-01 00:00:00: 10367. Package A: list size 9908 = its active population (reconciles exactly).
- **expected exceptions:** 512 active accounts omitted from the Q3 list (206 human, 306 service). The same query also omitted 499 accounts in 2026Q2.
  - omitted account ids (2026Q3):
    LDA100905, LDA101110, LDA104090, LDA104336, LDA106432, LDA115071, LDA115275, LDA115618
    LDA117649, LDA120103, LDA121819, LDA121990, LDA123029, LDA124789, LDA127914, LDA131035
    LDA133359, LDA133420, LDA133500, LDA134192, LDA134268, LDA137451, LDA141208, LDA145368
    LDA146117, LDA147310, LDA147599, LDA149771, LDA149788, LDA150760, LDA152111, LDA153219
    LDA153307, LDA158943, LDA161350, LDA164133, LDA165265, LDA166951, LDA167721, LDA171231
    LDA172631, LDA173694, LDA174231, LDA176208, LDA176798, LDA182099, LDA182972, LDA184835
    LDA185490, LDA185912, LDA189060, LDA190658, LDA198798, LDA198926, LDA202386, LDA203687
    LDA205863, LDA205893, LDA206152, LDA207827, LDA210052, LDA212367, LDA212947, LDA213943
    LDA214323, LDA214346, LDA218150, LDA223021, LDA223283, LDA225527, LDA228710, LDA229394
    LDA230435, LDA232246, LDA233228, LDA233927, LDA237874, LDA240438, LDA242467, LDA246382
    LDA246677, LDA246821, LDA248355, LDA248885, LDA248976, LDA252050, LDA253357, LDA254872
    LDA255925, LDA262823, LDA264269, LDA266811, LDA268949, LDA276739, LDA277186, LDA279662
    LDA280148, LDA280223, LDA280841, LDA281030, LDA286798, LDA290355, LDA290691, LDA292717
    LDA295914, LDA299696, LDA300914, LDA303695, LDA304421, LDA308737, LDA309638, LDA311171
    LDA313132, LDA314367, LDA318190, LDA322611, LDA323555, LDA325109, LDA326401, LDA329664
    LDA331697, LDA332794, LDA335131, LDA335335, LDA341288, LDA341591, LDA343508, LDA346151
    LDA348478, LDA355643, LDA356433, LDA356877, LDA360842, LDA365140, LDA365265, LDA366070
    LDA366690, LDA367344, LDA367845, LDA367938, LDA368472, LDA369543, LDA372208, LDA373835
    LDA376022, LDA376506, LDA381634, LDA383125, LDA384771, LDA387556, LDA388728, LDA389951
    LDA391837, LDA392615, LDA393079, LDA393610, LDA394304, LDA394499, LDA394933, LDA399268
    LDA399479, LDA403204, LDA404419, LDA404423, LDA405069, LDA407698, LDA407751, LDA409223
    LDA412541, LDA413839, LDA414132, LDA416025, LDA418088, LDA420313, LDA422107, LDA423819
    LDA425459, LDA426846, LDA428844, LDA429866, LDA431706, LDA431768, LDA432794, LDA433100
    LDA433755, LDA437536, LDA439727, LDA440609, LDA441460, LDA442465, LDA443003, LDA443040
    LDA445436, LDA446310, LDA448268, LDA448404, LDA452019, LDA453146, LDA455837, LDA457001
    LDA457954, LDA459036, LDA461369, LDA461412, LDA461704, LDA463122, LDA464839, LDA468139
    LDA468662, LDA469936, LDA471945, LDA473342, LDA477343, LDA481711, LDA486482, LDA486926
    LDA487746, LDA487966, LDA488150, LDA489957, LDA491593, LDA493520, LDA495531, LDA496594
    LDA498200, LDA501247, LDA501680, LDA503970, LDA506582, LDA507577, LDA507782, LDA509529
    LDA510076, LDA510480, LDA511957, LDA513405, LDA513685, LDA514055, LDA515836, LDA515842
    LDA522566, LDA522836, LDA527863, LDA528055, LDA532863, LDA533362, LDA534306, LDA535267
    LDA536428, LDA541346, LDA541559, LDA545985, LDA548124, LDA553535, LDA554157, LDA556813
    LDA557221, LDA557980, LDA558195, LDA562979, LDA564261, LDA564729, LDA566651, LDA568144
    LDA569335, LDA571098, LDA571272, LDA571376, LDA575825, LDA577382, LDA577692, LDA577895
    LDA578752, LDA579639, LDA579723, LDA580268, LDA580726, LDA581306, LDA581822, LDA587871
    LDA589844, LDA590360, LDA590664, LDA593020, LDA593098, LDA593491, LDA593594, LDA597679
    LDA598830, LDA600180, LDA600362, LDA601080, LDA601882, LDA602482, LDA605807, LDA607447
    LDA610972, LDA611905, LDA612470, LDA613352, LDA616605, LDA619192, LDA623525, LDA625876
    LDA627496, LDA630352, LDA630836, LDA632859, LDA634743, LDA636412, LDA637708, LDA640271
    LDA640437, LDA641696, LDA645820, LDA646469, LDA647446, LDA647451, LDA647535, LDA647618
    LDA649550, LDA650386, LDA652992, LDA654318, LDA654991, LDA657537, LDA657702, LDA660314
    LDA663545, LDA665149, LDA665259, LDA666623, LDA671988, LDA673547, LDA674125, LDA676028
    LDA678636, LDA679814, LDA680203, LDA680911, LDA683733, LDA691451, LDA696420, LDA701275
    LDA702843, LDA704427, LDA708189, LDA710143, LDA714592, LDA715982, LDA716266, LDA717002
    LDA717762, LDA722704, LDA723660, LDA724021, LDA727028, LDA727458, LDA731221, LDA733380
    LDA735028, LDA741878, LDA742725, LDA746029, LDA750577, LDA751896, LDA754590, LDA754896
    LDA756824, LDA758541, LDA759160, LDA761124, LDA765260, LDA765737, LDA767540, LDA768105
    LDA769801, LDA770643, LDA772234, LDA774292, LDA774366, LDA778128, LDA778398, LDA784495
    LDA786524, LDA786750, LDA786874, LDA790498, LDA790886, LDA791133, LDA794777, LDA796192
    LDA796497, LDA802367, LDA802754, LDA803526, LDA805880, LDA806255, LDA806715, LDA808309
    LDA808835, LDA809999, LDA812408, LDA814391, LDA818027, LDA820193, LDA821484, LDA821946
    LDA824129, LDA824620, LDA825014, LDA828561, LDA830078, LDA832850, LDA832939, LDA835455
    LDA835752, LDA835887, LDA837770, LDA838042, LDA838794, LDA841346, LDA841633, LDA843697
    LDA844636, LDA845748, LDA848388, LDA850682, LDA851148, LDA851785, LDA851876, LDA856554
    LDA856687, LDA859529, LDA860991, LDA862815, LDA864029, LDA864541, LDA868263, LDA871889
    LDA872969, LDA872971, LDA875039, LDA875570, LDA877177, LDA884459, LDA885597, LDA887693
    LDA889478, LDA892219, LDA892509, LDA892754, LDA894875, LDA895782, LDA901680, LDA902663
    LDA902713, LDA903036, LDA903273, LDA903355, LDA904040, LDA905973, LDA906660, LDA908847
    LDA909877, LDA910597, LDA910702, LDA911207, LDA914083, LDA914122, LDA914597, LDA918023
    LDA919177, LDA919606, LDA919755, LDA920922, LDA925152, LDA930008, LDA930657, LDA932679
    LDA932798, LDA933002, LDA943843, LDA944109, LDA944785, LDA945842, LDA946987, LDA952807
    LDA953714, LDA958908, LDA962789, LDA965681, LDA970367, LDA971370, LDA971805, LDA971856
    LDA972837, LDA973090, LDA973788, LDA975459, LDA979286, LDA980401, LDA983959, LDA984533
    LDA986942, LDA988230, LDA990177, LDA991974, LDA993137, LDA997210, LDA998416, LDA999432
- **why the omission is plausible:** the list query joins accounts to the HR export to route each account to a reviewer (manager or service owner), and does it as an inner join on the raw `hr_id` string. Owners whose HR records came from the previous HRIS keep legacy-format identifiers, so their accounts (human accounts of those people and service accounts they own) drop out without an error. Every account that does reach the list is reviewed, signed off and actioned, so completion is genuinely 100% of the list. Nothing in the package shows the gap: account ids are random, the human/service mix is unchanged, and the snapshot world was sized so the headline count matches the other package.
- **which control it defeats:** LD-AC-03.

---

## Simulator gaps (labs/m01-risk-controls-independence/larkspur/), for the red-team step

What 'expected' means for the B entries: the count of rows **produced through the simulator** in the generated datasets is 0 for every B entry (no simulator command was used to build them). That is not the same as 'no row looks like it'. Rows with the literal B-02 signature (`entitlements.approval_ref` NULL) do exist in planted: exactly 42, and they are exactly the entitlement rows of the PF-04 accounts (all of them, and no other rows). Rows with the literal B-01 signature (approval_ref present but not resolving to an approved request for the same account and permission decided before the grant): 0 in planted. Clean, q3_review_snapshot_A and q3_review_snapshot_B: 0 rows with either signature. The key writer asserts all of this against the data when it writes this file.

### B-01
- **id:** B-01
- **type:** bypass
- **where:** `larkspur_cli.py grant --actor ADMIN --account ID --permission P --approval-ref X`.
- **expected (observable behaviour):** succeeds for any value of X, including an id that does not exist in `access_requests`, one that is pending or rejected, one for another account or permission, or one decided after the grant. X is not stored verbatim: leading and trailing whitespace is stripped before storage, and a whitespace-only X is stored as NULL (which is then the B-02 case). Per invocation it writes exactly 1 row to `entitlements` (approval_ref = stripped X, granted_by = actor) and 1 row to `auth_events` (actor, method sso, collector admin-console, result success); 0 rows to `access_requests`. Exception population for a tester: entitlements whose approval_ref does not resolve to an approved request for the same account (and permission) decided before granted_at.
- **which control it defeats:** LD-AC-01 (the grant looks approved if `entitlements` is inspected alone).

### B-02
- **id:** B-02
- **type:** bypass
- **where:** `larkspur_cli.py grant` without `--approval-ref` (or with a whitespace-only value).
- **expected (observable behaviour):** succeeds. Per invocation: 1 row in `entitlements` with approval_ref NULL and granted_by = actor, 1 row in `auth_events` (the actor's admin-console sso success, which does not name the permission or target account), 0 rows in `access_requests`. Nothing blocks or alerts.
- **which control it defeats:** LD-AC-01 as a preventive control (detectable only after the fact, as approval_ref NULL).

### B-03
- **id:** B-03
- **type:** bypass
- **where:** `larkspur_cli.py create-account` (T1136).
- **expected (observable behaviour):** succeeds with no provisioning request; `--request-ref` is optional and is stored unvalidated. Per invocation: 1 row in `iam_accounts` (status active, provisioning_request_id NULL or the unvalidated value; no column of the row names the actor), 1 row in `auth_events` (actor admin-console sso success), 0 rows in `access_requests`, 0 rows in `entitlements`. The account is in the inventory, so the next complete review population includes it.
- **which control it defeats:** depends on how LD-AC-01 is read; a grader should accept either attribution if the reasoning matches. (a) Reading LD-AC-01 by its control statement ('every entitlement grant has an owner-approved request dated before the grant'): create-account grants no entitlement, so none of LD-AC-01 to LD-AC-05 is defeated; it is a design gap against AC-2 account management, and any entitlement later granted to the account falls under B-01 or B-02. (b) Reading LD-AC-01 by its 'How it operates' paragraph in SYSTEM.md, which says new accounts are created from an approved `new_account` request and that admin-console changes record the approved request reference: account creation is inside LD-AC-01's operation, and B-03 defeats LD-AC-01 (an account exists with no approved `new_account` request).

### B-04
- **id:** B-04
- **type:** bypass
- **where:** `larkspur_cli.py authenticate ACCOUNT --method api_token` on an account with status disabled (T1078).
- **expected (observable behaviour):** succeeds. Per invocation: 1 row in `auth_events` with result success, method api_token, collector api-gw-1, for the disabled account. The same call with method sso or password writes 1 row with result failure, reason account_disabled.
- **which control it defeats:** LD-AC-02 (disabling the account does not stop token use, so the control's objective is not met even when the disable is on time).

### B-05
- **id:** B-05
- **type:** survivorship
- **where:** simulator telemetry (T1087).
- **expected (observable behaviour):** `info`, `list-*`, `describe-*` and `sql` write 0 rows to any table. `authenticate` against an account id that is not in `iam_accounts` prints 'authentication failed' and writes 0 rows to any table. `grant`, `create-account` and `disable-account`: if the actor id is not in `iam_accounts`, 0 rows; if the actor is disabled or lacks iam.admin, exactly 1 `auth_events` row (actor, sso, admin-console, failure, reason account_disabled or not_authorized) and nothing else; if the actor is accepted, exactly 1 `auth_events` row (actor, sso, admin-console, success) plus the change itself (`grant`: 1 `entitlements` insert; `create-account`: 1 `iam_accounts` insert; `disable-account`: 1 `iam_accounts` row updated in status, disabled_at, disable_reason), or only the actor row if the target check then fails. Where the actor is recorded, per command: `grant` records the actor on the changed row itself (`entitlements.granted_by`) as well as in the sign-in row; `create-account` and `disable-account` record the actor only in the sign-in row (no column of the inserted or updated `iam_accounts` row names the actor). No row anywhere records which command ran or its parameters, and there is no separate admin audit table.
- **which control it defeats:** none of LD-AC-01 to LD-AC-05 directly. It is a telemetry gap: discovery and failed attempts against non-existent accounts leave no record; a `grant` can be attributed directly from `entitlements.granted_by`, but a `create-account` or `disable-account` can be attributed only by joining the changed row's timestamp to the actor's sign-in row.

