---
doc_id: GGD-URS-001
title: GrainGuard user requirements
project: GrainGuard
doc_type: User requirements
version: "0.1"
status: Draft
date: 2026-10-24
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-10-24
    author: Amish Chadha
    change: First issue (kit 1.8 upgrade), drawn from the users, constraints and decisions in GGD-PRB-001 and GGD-DDR-001
---

# GrainGuard user requirements

What the people who store grain, fit the kit and live with it need, written from their side. Seventeen needs, twelve of them High. The product requirements that meet them are in GGD-PRS-001 (`03-requirements.md`) and the links are in the traceability matrix GGD-RTM-001 (`03b-traceability.md`). The needs come from the users and stakeholders in GGD-PRB-001 (Tables 1 and 2) and from Amish's decisions in GGD-DDR-001; none has yet been checked with a farmer, so all are proposals for the first co-design visit (GGD-DEC-001, item 4 of 2026-10-02). Method: STANDARDS section 22.

Table 1. User requirements.

| ID | Category | Title | Need | Priority | Source |
| --- | --- | --- | --- | --- | --- |
| UR-001 | Performance | Grain temperature through the depth | I want to know the temperature of my grain from the floor to the top without climbing the bin or entering it | High | Small or mid-size grain farmer (PRB Table 1) |
| UR-002 | Performance | Drying or rewetting | I want to know whether my grain is drying or taking on water while it is stored | High | Small or mid-size grain farmer |
| UR-003 | Performance | Outside air at the bin | I want the controller to judge the air the fan actually pulls in, at my bin, not a forecast | Medium | Small or mid-size grain farmer; extension specialist (PRB Table 2) |
| UR-004 | Performance | Fans run only when they help | I want the fan to run when the air will cool or dry the grain, and to stay off when it would rewet or rewarm it | High | Small or mid-size grain farmer; extension specialist |
| UR-005 | Safety | Safe when the controller fails | If the controller dies or loses its readings, the fan must stop, and I must still be able to run it by hand | High | Farm electrician; small or mid-size grain farmer |
| UR-006 | Performance | Warning of heating | I want to be warned early when part of the grain starts to heat, before it spoils | High | Small or mid-size grain farmer |
| UR-007 | Usability | Status from the farmhouse | I want to see how the bin is doing and be alarmed in the house, without walking out to the bin | Medium | Farm worker or family member |
| UR-008 | Environment and durability | No mains, all winter | It must keep working at a bin with no outlet nearby, through short winter days and cloudy weeks | High | Small or mid-size grain farmer |
| UR-009 | Environment and durability | Survives the bin's conditions | It must survive a northern winter, a hot dusty summer and a fumigation of the bin | High | Small or mid-size grain farmer; licensed fumigator (PRB Table 2) |
| UR-010 | Safety | No damage to the roof | Whatever hangs in the bin must not overload the roof or break when the grain is unloaded | High | Bin maker (PRB Table 2); small or mid-size grain farmer |
| UR-011 | Safety | No entry into a bin holding grain | Nobody should ever have to enter a bin holding grain to fit, check or service it | High | Farm worker or family member |
| UR-012 | Safety | Mains work kept small | The only mains work should be a small, clearly isolated job an electrician can do at the starter | High | Farm electrician |
| UR-013 | Cost | Affordable per bin | It must cost far less per bin than the commercial monitoring and fan control systems | High | Small or mid-size grain farmer; cooperative or storage manager |
| UR-014 | Regulatory | Data stays on the farm | My readings stay on my farm and need no cloud account | Medium | Small or mid-size grain farmer |
| UR-015 | Deployment and assembly | Retrofit, workshop built | It must fit my existing bin and fan with no welding or cutting of bin sheets, and be buildable in a farm workshop | Medium | Small or mid-size grain farmer; open hardware community (PRB Table 1) |
| UR-016 | Maintenance | Repairable | I want to repair it with bought parts and the documents, without the maker | Low | Open hardware community; cooperative or storage manager |
| UR-017 | Regulatory | Legal radio | The radio must be legal to use where the farm is | Medium | Radio regulator (PRB Table 2) |

Categories: deployment and assembly, performance, usability, safety, environment and durability, logistics, maintenance, cost, regulatory. Priorities: High, Medium, Low.
