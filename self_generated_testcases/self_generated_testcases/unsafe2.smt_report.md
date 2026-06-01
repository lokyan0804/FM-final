# SMT Fault Localization Report

Method: `unsat-core`
Solver result: `unsat`
Fallback used: `false`

## 1. Input Values


## 2. Postcondition

Error guard:

All of these path guards must hold to reach the target:

```text
line 1747: important_state == 35939
line 1754: important_state == 89007
line 1761: important_state == 134531
line 1768: important_state == 201761
line 1775: important_state == 217213
line 1782: important_state == 279338
line 1789: important_state == 307356
line 1796: important_state == 344806
line 1803: important_state == 347584
line 1810: important_state == 437608
line 1817: important_state == 519216
line 1824: important_state == 572871
line 1831: important_state == 619203
line 1838: important_state == 641468
line 1845: important_state == 685125
line 1852: important_state == 685731
line 1859: important_state == 709150
line 1866: important_state == 750771
line 1873: important_state == 829242
line 1880: important_state == 853948
```

Safe postcondition:

```text
target/reach_error is not reached
equivalently: at least one path guard above is false in its SSA state
```

## 3. Pi Trace Formula

pi_0: line 1745: `int important_state = 0;` => `int important_state = 0`
pi_1: line 1746: `important_state += 35939;` => `important_state += 35939`
pi_2: line 1748: `important_state ^= 62963;` => `important_state ^= 62963`
pi_3: line 1749: `important_state ^= 62963;` => `important_state ^= 62963`
pi_4: line 1753: `important_state += 53068;` => `important_state += 53068`
pi_5: line 1755: `important_state ^= 81952;` => `important_state ^= 81952`
pi_6: line 1756: `important_state ^= 81952;` => `important_state ^= 81952`
pi_7: line 1760: `important_state += 45524;` => `important_state += 45524`
pi_8: line 1762: `important_state ^= 25091;` => `important_state ^= 25091`
pi_9: line 1763: `important_state ^= 25091;` => `important_state ^= 25091`
pi_10: line 1767: `important_state += 67230;` => `important_state += 67230`
pi_11: line 1769: `important_state ^= 96361;` => `important_state ^= 96361`
pi_12: line 1770: `important_state ^= 96361;` => `important_state ^= 96361`
pi_13: line 1774: `important_state += 15452;` => `important_state += 15452`
pi_14: line 1776: `important_state ^= 81143;` => `important_state ^= 81143`
pi_15: line 1777: `important_state ^= 81143;` => `important_state ^= 81143`
pi_16: line 1781: `important_state += 62125;` => `important_state += 62125`
pi_17: line 1783: `important_state ^= 13012;` => `important_state ^= 13012`
pi_18: line 1784: `important_state ^= 13012;` => `important_state ^= 13012`
pi_19: line 1788: `important_state += 28018;` => `important_state += 28018`
pi_20: line 1790: `important_state ^= 16199;` => `important_state ^= 16199`
pi_21: line 1791: `important_state ^= 16199;` => `important_state ^= 16199`
pi_22: line 1795: `important_state += 37450;` => `important_state += 37450`
pi_23: line 1797: `important_state ^= 57807;` => `important_state ^= 57807`
pi_24: line 1798: `important_state ^= 57807;` => `important_state ^= 57807`
pi_25: line 1802: `important_state += 2778;` => `important_state += 2778`
pi_26: line 1804: `important_state ^= 1396;` => `important_state ^= 1396`
pi_27: line 1805: `important_state ^= 1396;` => `important_state ^= 1396`
pi_28: line 1809: `important_state += 90024;` => `important_state += 90024`
pi_29: line 1811: `important_state ^= 60919;` => `important_state ^= 60919`
pi_30: line 1812: `important_state ^= 60919;` => `important_state ^= 60919`
pi_31: line 1816: `important_state += 81608;` => `important_state += 81608`
pi_32: line 1818: `important_state ^= 31823;` => `important_state ^= 31823`
pi_33: line 1819: `important_state ^= 31823;` => `important_state ^= 31823`
pi_34: line 1823: `important_state += 53655;` => `important_state += 53655`
pi_35: line 1825: `important_state ^= 50846;` => `important_state ^= 50846`
pi_36: line 1826: `important_state ^= 50846;` => `important_state ^= 50846`
pi_37: line 1830: `important_state += 46332;` => `important_state += 46332`
pi_38: line 1832: `important_state ^= 99901;` => `important_state ^= 99901`
pi_39: line 1833: `important_state ^= 99901;` => `important_state ^= 99901`
pi_40: line 1837: `important_state += 22265;` => `important_state += 22265`
pi_41: line 1839: `important_state ^= 26207;` => `important_state ^= 26207`
pi_42: line 1840: `important_state ^= 26207;` => `important_state ^= 26207`
pi_43: line 1844: `important_state += 43657;` => `important_state += 43657`
pi_44: line 1846: `important_state ^= 27964;` => `important_state ^= 27964`
pi_45: line 1847: `important_state ^= 27964;` => `important_state ^= 27964`
pi_46: line 1851: `important_state += 606;` => `important_state += 606`
pi_47: line 1853: `important_state ^= 6266;` => `important_state ^= 6266`
pi_48: line 1854: `important_state ^= 6266;` => `important_state ^= 6266`
pi_49: line 1858: `important_state += 23419;` => `important_state += 23419`
pi_50: line 1860: `important_state ^= 65821;` => `important_state ^= 65821`
pi_51: line 1861: `important_state ^= 65821;` => `important_state ^= 65821`
pi_52: line 1865: `important_state += 41621;` => `important_state += 41621`
pi_53: line 1867: `important_state ^= 93186;` => `important_state ^= 93186`
pi_54: line 1868: `important_state ^= 93186;` => `important_state ^= 93186`
pi_55: line 1872: `important_state += 78471;` => `important_state += 78471`
pi_56: line 1874: `important_state ^= 43032;` => `important_state ^= 43032`
pi_57: line 1875: `important_state ^= 43032;` => `important_state ^= 43032`
pi_58: line 1879: `important_state += 24706;` => `important_state += 24706`
pi_59: line 1881: `important_state ^= 46141;` => `important_state ^= 46141`
pi_60: line 1882: `important_state ^= 46141;` => `important_state ^= 46141`

## 4. UNSAT Check

Query:

```text
input_values AND pi AND safe_postcondition
```

Result: `unsat`

Why suspicious:

Z3 returned UNSAT. The tracked pi formulas whose literals are in the unsat core are suspicious; their CFA edges are reported below.

UNSAT core literals:

```text
a_13
a_11
a_8
a_21
a_10
a_7
a_16
a_19
a_6
a_18
a_20
a_5
a_14
a_17
a_4
a_23
a_3
a_9
a_12
a_22
a_2
a_1
a_15
a_0
a_24
a_25
a_26
a_27
a_28
a_29
a_30
a_31
a_32
a_33
a_34
a_35
a_36
a_37
a_38
a_39
a_40
a_41
a_42
a_43
a_44
a_45
a_46
a_47
a_48
a_49
a_50
a_51
a_52
a_53
a_54
a_55
a_56
a_57
a_58
```

## 5. Suspicious Pi Formulas

- pi_0: line 1745: `int important_state = 0;` => `int important_state = 0`
- pi_1: line 1746: `important_state += 35939;` => `important_state += 35939`
- pi_2: line 1748: `important_state ^= 62963;` => `important_state ^= 62963`
- pi_3: line 1749: `important_state ^= 62963;` => `important_state ^= 62963`
- pi_4: line 1753: `important_state += 53068;` => `important_state += 53068`
- pi_5: line 1755: `important_state ^= 81952;` => `important_state ^= 81952`
- pi_6: line 1756: `important_state ^= 81952;` => `important_state ^= 81952`
- pi_7: line 1760: `important_state += 45524;` => `important_state += 45524`
- pi_8: line 1762: `important_state ^= 25091;` => `important_state ^= 25091`
- pi_9: line 1763: `important_state ^= 25091;` => `important_state ^= 25091`
- pi_10: line 1767: `important_state += 67230;` => `important_state += 67230`
- pi_11: line 1769: `important_state ^= 96361;` => `important_state ^= 96361`
- pi_12: line 1770: `important_state ^= 96361;` => `important_state ^= 96361`
- pi_13: line 1774: `important_state += 15452;` => `important_state += 15452`
- pi_14: line 1776: `important_state ^= 81143;` => `important_state ^= 81143`
- pi_15: line 1777: `important_state ^= 81143;` => `important_state ^= 81143`
- pi_16: line 1781: `important_state += 62125;` => `important_state += 62125`
- pi_17: line 1783: `important_state ^= 13012;` => `important_state ^= 13012`
- pi_18: line 1784: `important_state ^= 13012;` => `important_state ^= 13012`
- pi_19: line 1788: `important_state += 28018;` => `important_state += 28018`
- pi_20: line 1790: `important_state ^= 16199;` => `important_state ^= 16199`
- pi_21: line 1791: `important_state ^= 16199;` => `important_state ^= 16199`
- pi_22: line 1795: `important_state += 37450;` => `important_state += 37450`
- pi_23: line 1797: `important_state ^= 57807;` => `important_state ^= 57807`
- pi_24: line 1798: `important_state ^= 57807;` => `important_state ^= 57807`
- pi_25: line 1802: `important_state += 2778;` => `important_state += 2778`
- pi_26: line 1804: `important_state ^= 1396;` => `important_state ^= 1396`
- pi_27: line 1805: `important_state ^= 1396;` => `important_state ^= 1396`
- pi_28: line 1809: `important_state += 90024;` => `important_state += 90024`
- pi_29: line 1811: `important_state ^= 60919;` => `important_state ^= 60919`
- pi_30: line 1812: `important_state ^= 60919;` => `important_state ^= 60919`
- pi_31: line 1816: `important_state += 81608;` => `important_state += 81608`
- pi_32: line 1818: `important_state ^= 31823;` => `important_state ^= 31823`
- pi_33: line 1819: `important_state ^= 31823;` => `important_state ^= 31823`
- pi_34: line 1823: `important_state += 53655;` => `important_state += 53655`
- pi_35: line 1825: `important_state ^= 50846;` => `important_state ^= 50846`
- pi_36: line 1826: `important_state ^= 50846;` => `important_state ^= 50846`
- pi_37: line 1830: `important_state += 46332;` => `important_state += 46332`
- pi_38: line 1832: `important_state ^= 99901;` => `important_state ^= 99901`
- pi_39: line 1833: `important_state ^= 99901;` => `important_state ^= 99901`
- pi_40: line 1837: `important_state += 22265;` => `important_state += 22265`
- pi_41: line 1839: `important_state ^= 26207;` => `important_state ^= 26207`
- pi_42: line 1840: `important_state ^= 26207;` => `important_state ^= 26207`
- pi_43: line 1844: `important_state += 43657;` => `important_state += 43657`
- pi_44: line 1846: `important_state ^= 27964;` => `important_state ^= 27964`
- pi_45: line 1847: `important_state ^= 27964;` => `important_state ^= 27964`
- pi_46: line 1851: `important_state += 606;` => `important_state += 606`
- pi_47: line 1853: `important_state ^= 6266;` => `important_state ^= 6266`
- pi_48: line 1854: `important_state ^= 6266;` => `important_state ^= 6266`
- pi_49: line 1858: `important_state += 23419;` => `important_state += 23419`
- pi_50: line 1860: `important_state ^= 65821;` => `important_state ^= 65821`
- pi_51: line 1861: `important_state ^= 65821;` => `important_state ^= 65821`
- pi_52: line 1865: `important_state += 41621;` => `important_state += 41621`
- pi_53: line 1867: `important_state ^= 93186;` => `important_state ^= 93186`
- pi_54: line 1868: `important_state ^= 93186;` => `important_state ^= 93186`
- pi_55: line 1872: `important_state += 78471;` => `important_state += 78471`
- pi_56: line 1874: `important_state ^= 43032;` => `important_state ^= 43032`
- pi_57: line 1875: `important_state ^= 43032;` => `important_state ^= 43032`
- pi_58: line 1879: `important_state += 24706;` => `important_state += 24706`
## 6. Suspicious CFA Edges

- line 1745: `int important_state = 0;`
- line 1746: `important_state += 35939;`
- line 1748: `important_state ^= 62963;`
- line 1749: `important_state ^= 62963;`
- line 1753: `important_state += 53068;`
- line 1755: `important_state ^= 81952;`
- line 1756: `important_state ^= 81952;`
- line 1760: `important_state += 45524;`
- line 1762: `important_state ^= 25091;`
- line 1763: `important_state ^= 25091;`
- line 1767: `important_state += 67230;`
- line 1769: `important_state ^= 96361;`
- line 1770: `important_state ^= 96361;`
- line 1774: `important_state += 15452;`
- line 1776: `important_state ^= 81143;`
- line 1777: `important_state ^= 81143;`
- line 1781: `important_state += 62125;`
- line 1783: `important_state ^= 13012;`
- line 1784: `important_state ^= 13012;`
- line 1788: `important_state += 28018;`
- line 1790: `important_state ^= 16199;`
- line 1791: `important_state ^= 16199;`
- line 1795: `important_state += 37450;`
- line 1797: `important_state ^= 57807;`
- line 1798: `important_state ^= 57807;`
- line 1802: `important_state += 2778;`
- line 1804: `important_state ^= 1396;`
- line 1805: `important_state ^= 1396;`
- line 1809: `important_state += 90024;`
- line 1811: `important_state ^= 60919;`
- line 1812: `important_state ^= 60919;`
- line 1816: `important_state += 81608;`
- line 1818: `important_state ^= 31823;`
- line 1819: `important_state ^= 31823;`
- line 1823: `important_state += 53655;`
- line 1825: `important_state ^= 50846;`
- line 1826: `important_state ^= 50846;`
- line 1830: `important_state += 46332;`
- line 1832: `important_state ^= 99901;`
- line 1833: `important_state ^= 99901;`
- line 1837: `important_state += 22265;`
- line 1839: `important_state ^= 26207;`
- line 1840: `important_state ^= 26207;`
- line 1844: `important_state += 43657;`
- line 1846: `important_state ^= 27964;`
- line 1847: `important_state ^= 27964;`
- line 1851: `important_state += 606;`
- line 1853: `important_state ^= 6266;`
- line 1854: `important_state ^= 6266;`
- line 1858: `important_state += 23419;`
- line 1860: `important_state ^= 65821;`
- line 1861: `important_state ^= 65821;`
- line 1865: `important_state += 41621;`
- line 1867: `important_state ^= 93186;`
- line 1868: `important_state ^= 93186;`
- line 1872: `important_state += 78471;`
- line 1874: `important_state ^= 43032;`
- line 1875: `important_state ^= 43032;`
- line 1879: `important_state += 24706;`

## 7. Reduction Outputs

- `state`: 21 waypoints -> `unsafe2.reduced.witness.state.yml`
- `match`: 21 waypoints -> `unsafe2.reduced.witness.match.yml`
- `all`: 1 waypoints -> `unsafe2.reduced.witness.yml`
