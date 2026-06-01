# SMT Fault Localization Report

Method: `unsat-core`
Solver result: `unsat`
Fallback used: `false`

## 1. Evidence Trace

- [PRE] line 1777: `critical_gate_1 = 0` [t_0]
- [POST] line 1779: `!((critical_gate_1 & 1u) != 0u)` [t_1]
- [SUSPICIOUS] line 1782: `int step_1 = 0` [t_2, pi_0]
- [POST] line 1782: `step_1 < 6` [t_3]
- [POST] line 1783: `(step_1 & 1u) == 0u` [t_4]
- [SUSPICIOUS] line 1782: `++step_1` [t_6, pi_2]
- [POST] line 1782: `step_1 < 6` [t_7]
- [POST] line 1783: `!((step_1 & 1u) == 0u)` [t_8]
- [POST] line 1791: `!((step_1 + 1) == 6)` [t_9]
- [SUSPICIOUS] line 1782: `++step_1` [t_10, pi_3]
- [POST] line 1782: `step_1 < 6` [t_11]
- [POST] line 1783: `(step_1 & 1u) == 0u` [t_12]
- [SUSPICIOUS] line 1782: `++step_1` [t_14, pi_5]
- [POST] line 1782: `step_1 < 6` [t_15]
- [POST] line 1783: `!((step_1 & 1u) == 0u)` [t_16]
- [POST] line 1791: `!((step_1 + 1) == 6)` [t_17]
- [SUSPICIOUS] line 1782: `++step_1` [t_18, pi_6]
- [POST] line 1782: `step_1 < 6` [t_19]
- [POST] line 1783: `(step_1 & 1u) == 0u` [t_20]
- [SUSPICIOUS] line 1782: `++step_1` [t_22, pi_8]
- [POST] line 1782: `step_1 < 6` [t_23]
- [POST] line 1783: `!((step_1 & 1u) == 0u)` [t_24]
- [POST] line 1791: `(step_1 + 1) == 6` [t_25]
- [SUSPICIOUS] line 1797: `unsigned int related_tracker_1 = related_gate_1` [t_28, pi_10]
- [SUSPICIOUS] line 1798: `int tick_1 = 0` [t_29, pi_11]
- [POST] line 1798: `tick_1 < 7` [t_30]
- [PRE] line 1799: `related_gate_1 = 0` [t_31]
- [SUSPICIOUS] line 1799: `unsigned int __tmp_1 = related_gate_1` [t_31, pi_12]
- [SUSPICIOUS] line 1802: `related_gate_1 = __tmp_1` [t_32, pi_13]
- [POST] line 1803: `!((tick_1 + 1) == 7)` [t_33]
- [SUSPICIOUS] line 1798: `++tick_1` [t_34, pi_14]
- [POST] line 1798: `tick_1 < 7` [t_35]
- [SUSPICIOUS] line 1799: `unsigned int __tmp_1 = related_gate_1` [t_36, pi_15]
- [SUSPICIOUS] line 1802: `related_gate_1 = __tmp_1` [t_37, pi_16]
- [POST] line 1803: `!((tick_1 + 1) == 7)` [t_38]
- [SUSPICIOUS] line 1798: `++tick_1` [t_39, pi_17]
- [POST] line 1798: `tick_1 < 7` [t_40]
- [SUSPICIOUS] line 1799: `unsigned int __tmp_1 = related_gate_1` [t_41, pi_18]
- [SUSPICIOUS] line 1802: `related_gate_1 = __tmp_1` [t_42, pi_19]
- [POST] line 1803: `!((tick_1 + 1) == 7)` [t_43]
- [SUSPICIOUS] line 1798: `++tick_1` [t_44, pi_20]
- [POST] line 1798: `tick_1 < 7` [t_45]
- [SUSPICIOUS] line 1799: `unsigned int __tmp_1 = related_gate_1` [t_46, pi_21]
- [SUSPICIOUS] line 1802: `related_gate_1 = __tmp_1` [t_47, pi_22]
- [POST] line 1803: `!((tick_1 + 1) == 7)` [t_48]
- [SUSPICIOUS] line 1798: `++tick_1` [t_49, pi_23]
- [POST] line 1798: `tick_1 < 7` [t_50]
- [SUSPICIOUS] line 1799: `unsigned int __tmp_1 = related_gate_1` [t_51, pi_24]
- [SUSPICIOUS] line 1802: `related_gate_1 = __tmp_1` [t_52, pi_25]
- [POST] line 1803: `!((tick_1 + 1) == 7)` [t_53]
- [SUSPICIOUS] line 1798: `++tick_1` [t_54, pi_26]
- [POST] line 1798: `tick_1 < 7` [t_55]
- [SUSPICIOUS] line 1799: `unsigned int __tmp_1 = related_gate_1` [t_56, pi_27]
- [SUSPICIOUS] line 1802: `related_gate_1 = __tmp_1` [t_57, pi_28]
- [POST] line 1803: `!((tick_1 + 1) == 7)` [t_58]
- [SUSPICIOUS] line 1798: `++tick_1` [t_59, pi_29]
- [POST] line 1798: `tick_1 < 7` [t_60]
- [SUSPICIOUS] line 1799: `unsigned int __tmp_1 = related_gate_1` [t_61, pi_30]
- [SUSPICIOUS] line 1802: `related_gate_1 = __tmp_1` [t_62, pi_31]
- [POST] line 1803: `(tick_1 + 1) == 7` [t_63]
- [POST] line 1807: `!(related_gate_1 != related_tracker_1)` [t_65]
- [SUSPICIOUS] line 1811: `unsigned int unrelated_lane_1 = (unsigned int) 8` [t_66, pi_33]
- [SUSPICIOUS] line 1812: `int idx_1 = 0` [t_67, pi_34]
- [POST] line 1812: `idx_1 < 5` [t_68]
- [POST] line 1813: `((unrelated_lane_1 + idx_1) & 1u) == 0u` [t_69]
- [SUSPICIOUS] line 1812: `++idx_1` [t_71, pi_36]
- [POST] line 1812: `idx_1 < 5` [t_72]
- [POST] line 1813: `!(((unrelated_lane_1 + idx_1) & 1u) == 0u)` [t_73]
- [POST] line 1818: `!((idx_1 + 2) == 5)` [t_74]
- [SUSPICIOUS] line 1812: `++idx_1` [t_75, pi_37]
- [POST] line 1812: `idx_1 < 5` [t_76]
- [POST] line 1813: `((unrelated_lane_1 + idx_1) & 1u) == 0u` [t_77]
- [SUSPICIOUS] line 1812: `++idx_1` [t_79, pi_39]
- [POST] line 1812: `idx_1 < 5` [t_80]
- [POST] line 1813: `!(((unrelated_lane_1 + idx_1) & 1u) == 0u)` [t_81]
- [POST] line 1818: `(idx_1 + 2) == 5` [t_82]
- [PRE] line 1836: `related_switch_1 = 0` [t_85]
- [SUSPICIOUS] line 1836: `unsigned int related_marker_1 = related_switch_1` [t_85, pi_41]
- [POST] line 1859: `!(related_switch_1 != related_marker_1)` [t_86]
- [PRE] line 1893: `do_state_1 = 0` [t_88]
- [SUSPICIOUS] line 1893: `unsigned int backup_do_1 = do_state_1` [t_88, pi_42]
- [SUSPICIOUS] line 1894: `int dw_1 = 0` [t_89, pi_43]
- [SUSPICIOUS] line 1896: `do_state_1 ^= dw_1` [t_90, pi_44]
- [SUSPICIOUS] line 1897: `dw_1++` [t_91, pi_45]
- [POST] line 1895: `dw_1 < 11` [t_92]
- [SUSPICIOUS] line 1896: `do_state_1 ^= dw_1` [t_93, pi_46]
- [SUSPICIOUS] line 1897: `dw_1++` [t_94, pi_47]
- [POST] line 1895: `dw_1 < 11` [t_95]
- [SUSPICIOUS] line 1896: `do_state_1 ^= dw_1` [t_96, pi_48]
- [SUSPICIOUS] line 1897: `dw_1++` [t_97, pi_49]
- [POST] line 1895: `dw_1 < 11` [t_98]
- [SUSPICIOUS] line 1896: `do_state_1 ^= dw_1` [t_99, pi_50]
- [SUSPICIOUS] line 1897: `dw_1++` [t_100, pi_51]
- [POST] line 1895: `dw_1 < 11` [t_101]
- [SUSPICIOUS] line 1896: `do_state_1 ^= dw_1` [t_102, pi_52]
- [SUSPICIOUS] line 1897: `dw_1++` [t_103, pi_53]
- [POST] line 1895: `dw_1 < 11` [t_104]
- [SUSPICIOUS] line 1896: `do_state_1 ^= dw_1` [t_105, pi_54]
- [SUSPICIOUS] line 1897: `dw_1++` [t_106, pi_55]
- [POST] line 1895: `dw_1 < 11` [t_107]
- [SUSPICIOUS] line 1896: `do_state_1 ^= dw_1` [t_108, pi_56]
- [SUSPICIOUS] line 1897: `dw_1++` [t_109, pi_57]
- [POST] line 1895: `dw_1 < 11` [t_110]
- [SUSPICIOUS] line 1896: `do_state_1 ^= dw_1` [t_111, pi_58]
- [SUSPICIOUS] line 1897: `dw_1++` [t_112, pi_59]
- [POST] line 1895: `dw_1 < 11` [t_113]
- [SUSPICIOUS] line 1896: `do_state_1 ^= dw_1` [t_114, pi_60]
- [SUSPICIOUS] line 1897: `dw_1++` [t_115, pi_61]
- [POST] line 1895: `dw_1 < 11` [t_116]
- [SUSPICIOUS] line 1896: `do_state_1 ^= dw_1` [t_117, pi_62]
- [SUSPICIOUS] line 1897: `dw_1++` [t_118, pi_63]
- [POST] line 1895: `dw_1 < 11` [t_119]
- [SUSPICIOUS] line 1896: `do_state_1 ^= dw_1` [t_120, pi_64]
- [SUSPICIOUS] line 1897: `dw_1++` [t_121, pi_65]
- [POST] line 1895: `!(dw_1 < 11)` [t_122]
- [POST] line 1899: `!(do_state_1 != (backup_do_1 ^ 11))` [t_123]
- [SUSPICIOUS] line 1903: `int loop_45278 = 0` [t_124, pi_66]
- [POST] line 1903: `loop_45278 < 14` [t_125]
- [SUSPICIOUS] line 1903: `loop_45278++` [t_126, pi_67]
- [POST] line 1903: `loop_45278 < 14` [t_127]
- [SUSPICIOUS] line 1903: `loop_45278++` [t_128, pi_68]
- [POST] line 1903: `loop_45278 < 14` [t_129]
- [SUSPICIOUS] line 1903: `loop_45278++` [t_130, pi_69]
- [POST] line 1903: `loop_45278 < 14` [t_131]
- [SUSPICIOUS] line 1903: `loop_45278++` [t_132, pi_70]
- [POST] line 1903: `loop_45278 < 14` [t_133]
- [SUSPICIOUS] line 1903: `loop_45278++` [t_134, pi_71]
- [POST] line 1903: `loop_45278 < 14` [t_135]
- [SUSPICIOUS] line 1903: `loop_45278++` [t_136, pi_72]
- [POST] line 1903: `loop_45278 < 14` [t_137]
- [SUSPICIOUS] line 1903: `loop_45278++` [t_138, pi_73]
- [POST] line 1903: `loop_45278 < 14` [t_139]
- [SUSPICIOUS] line 1903: `loop_45278++` [t_140, pi_74]
- [POST] line 1903: `loop_45278 < 14` [t_141]
- [SUSPICIOUS] line 1903: `loop_45278++` [t_142, pi_75]
- [POST] line 1903: `loop_45278 < 14` [t_143]
- [SUSPICIOUS] line 1903: `loop_45278++` [t_144, pi_76]
- [POST] line 1903: `loop_45278 < 14` [t_145]
- [SUSPICIOUS] line 1903: `loop_45278++` [t_146, pi_77]
- [POST] line 1903: `loop_45278 < 14` [t_147]
- [SUSPICIOUS] line 1903: `loop_45278++` [t_148, pi_78]
- [POST] line 1903: `loop_45278 < 14` [t_149]
- [SUSPICIOUS] line 1903: `loop_45278++` [t_150, pi_79]
- [POST] line 1903: `loop_45278 < 14` [t_151]
- [SUSPICIOUS] line 1903: `loop_45278++` [t_152, pi_80]
- [POST] line 1903: `!(loop_45278 < 14)` [t_153]
- [SUSPICIOUS] line 1910: `int while_cnt = 11` [t_154, pi_81]
- [POST] line 1911: `while_cnt > 0` [t_155]
- [SUSPICIOUS] line 1913: `while_cnt--` [t_156, pi_82]
- [POST] line 1911: `while_cnt > 0` [t_157]
- [SUSPICIOUS] line 1913: `while_cnt--` [t_158, pi_83]
- [POST] line 1911: `while_cnt > 0` [t_159]
- [SUSPICIOUS] line 1913: `while_cnt--` [t_160, pi_84]
- [POST] line 1911: `while_cnt > 0` [t_161]
- [SUSPICIOUS] line 1913: `while_cnt--` [t_162, pi_85]
- [POST] line 1911: `while_cnt > 0` [t_163]
- [SUSPICIOUS] line 1913: `while_cnt--` [t_164, pi_86]
- [POST] line 1911: `while_cnt > 0` [t_165]
- [SUSPICIOUS] line 1913: `while_cnt--` [t_166, pi_87]
- [POST] line 1911: `while_cnt > 0` [t_167]
- [SUSPICIOUS] line 1913: `while_cnt--` [t_168, pi_88]
- [POST] line 1911: `while_cnt > 0` [t_169]
- [SUSPICIOUS] line 1913: `while_cnt--` [t_170, pi_89]
- [POST] line 1911: `while_cnt > 0` [t_171]
- [SUSPICIOUS] line 1913: `while_cnt--` [t_172, pi_90]
- [POST] line 1911: `while_cnt > 0` [t_173]
- [SUSPICIOUS] line 1913: `while_cnt--` [t_174, pi_91]
- [POST] line 1911: `while_cnt > 0` [t_175]
- [SUSPICIOUS] line 1913: `while_cnt--` [t_176, pi_92]
- [POST] line 1911: `!(while_cnt > 0)` [t_177]
- [PRE] line 1944: `fake_state_1 = 0` [t_179]
- [SUSPICIOUS] line 1944: `unsigned int backup_fakecont_1 = fake_state_1` [t_179, pi_93]
- [SUSPICIOUS] line 1945: `int i_1 = 0` [t_180, pi_94]
- [POST] line 1945: `i_1 < 17` [t_181]
- [SUSPICIOUS] line 1945: `i_1++` [t_183, pi_96]
- [POST] line 1945: `i_1 < 17` [t_184]
- [SUSPICIOUS] line 1945: `i_1++` [t_186, pi_98]
- [POST] line 1945: `i_1 < 17` [t_187]
- [SUSPICIOUS] line 1945: `i_1++` [t_189, pi_100]
- [POST] line 1945: `i_1 < 17` [t_190]
- [SUSPICIOUS] line 1945: `i_1++` [t_192, pi_102]
- [POST] line 1945: `i_1 < 17` [t_193]
- [SUSPICIOUS] line 1945: `i_1++` [t_195, pi_104]
- [POST] line 1945: `i_1 < 17` [t_196]
- [SUSPICIOUS] line 1945: `i_1++` [t_198, pi_106]
- [POST] line 1945: `i_1 < 17` [t_199]
- [SUSPICIOUS] line 1945: `i_1++` [t_201, pi_108]
- [POST] line 1945: `i_1 < 17` [t_202]
- [SUSPICIOUS] line 1945: `i_1++` [t_204, pi_110]
- [POST] line 1945: `i_1 < 17` [t_205]
- [SUSPICIOUS] line 1945: `i_1++` [t_207, pi_112]
- [POST] line 1945: `i_1 < 17` [t_208]
- [SUSPICIOUS] line 1945: `i_1++` [t_210, pi_114]
- [POST] line 1945: `i_1 < 17` [t_211]
- [SUSPICIOUS] line 1945: `i_1++` [t_213, pi_116]
- [POST] line 1945: `i_1 < 17` [t_214]
- [SUSPICIOUS] line 1945: `i_1++` [t_216, pi_118]
- [POST] line 1945: `i_1 < 17` [t_217]
- [SUSPICIOUS] line 1945: `i_1++` [t_219, pi_120]
- [POST] line 1945: `i_1 < 17` [t_220]
- [SUSPICIOUS] line 1945: `i_1++` [t_222, pi_122]
- [POST] line 1945: `i_1 < 17` [t_223]
- [SUSPICIOUS] line 1945: `i_1++` [t_225, pi_124]
- [POST] line 1945: `i_1 < 17` [t_226]
- [SUSPICIOUS] line 1945: `i_1++` [t_228, pi_126]
- [POST] line 1945: `i_1 < 17` [t_229]
- [SUSPICIOUS] line 1945: `i_1++` [t_231, pi_128]
- [POST] line 1945: `!(i_1 < 17)` [t_232]
- [POST] line 1949: `!(fake_state_1 != backup_fakecont_1)` [t_233]
- [PRE] line 1954: `break_state_1 = 16000` [t_235]
- [SUSPICIOUS] line 1954: `unsigned int original_1 = break_state_1` [t_235, pi_129]
- [POST] line 1955: `break_state_1 < (break_state_1 + 1000)` [t_236]
- [POST] line 1959: `!(break_state_1 != original_1)` [t_238]
- [PRE] line 1964: `overwrite_state_1 = 0` [t_240]
- [SUSPICIOUS] line 1965: `int i_1 = 0` [t_241, pi_132]
- [POST] line 1965: `i_1 < 16` [t_242]
- [SUSPICIOUS] line 1965: `i_1++` [t_243, pi_133]
- [POST] line 1965: `i_1 < 16` [t_244]
- [SUSPICIOUS] line 1965: `i_1++` [t_245, pi_134]
- [POST] line 1965: `i_1 < 16` [t_246]
- [SUSPICIOUS] line 1965: `i_1++` [t_247, pi_135]
- [POST] line 1965: `i_1 < 16` [t_248]
- [SUSPICIOUS] line 1965: `i_1++` [t_249, pi_136]
- [POST] line 1965: `i_1 < 16` [t_250]
- [SUSPICIOUS] line 1965: `i_1++` [t_251, pi_137]
- [POST] line 1965: `i_1 < 16` [t_252]
- [SUSPICIOUS] line 1965: `i_1++` [t_253, pi_138]
- [POST] line 1965: `i_1 < 16` [t_254]
- [SUSPICIOUS] line 1965: `i_1++` [t_255, pi_139]
- [POST] line 1965: `i_1 < 16` [t_256]
- [SUSPICIOUS] line 1965: `i_1++` [t_257, pi_140]
- [POST] line 1965: `i_1 < 16` [t_258]
- [SUSPICIOUS] line 1965: `i_1++` [t_259, pi_141]
- [POST] line 1965: `i_1 < 16` [t_260]
- [SUSPICIOUS] line 1965: `i_1++` [t_261, pi_142]
- [POST] line 1965: `i_1 < 16` [t_262]
- [SUSPICIOUS] line 1965: `i_1++` [t_263, pi_143]
- [POST] line 1965: `i_1 < 16` [t_264]
- [SUSPICIOUS] line 1965: `i_1++` [t_265, pi_144]
- [POST] line 1965: `i_1 < 16` [t_266]
- [SUSPICIOUS] line 1965: `i_1++` [t_267, pi_145]
- [POST] line 1965: `i_1 < 16` [t_268]
- [SUSPICIOUS] line 1965: `i_1++` [t_269, pi_146]
- [POST] line 1965: `i_1 < 16` [t_270]
- [SUSPICIOUS] line 1965: `i_1++` [t_271, pi_147]
- [POST] line 1965: `i_1 < 16` [t_272]
- [SUSPICIOUS] line 1965: `i_1++` [t_273, pi_148]
- [POST] line 1965: `!(i_1 < 16)` [t_274]
- [SUSPICIOUS] line 1968: `overwrite_state_1 = saved_1` [t_275, pi_149]
- [POST] line 1969: `!(overwrite_state_1 != saved_1)` [t_276]
- [PRE] line 1974: `cont_state_1 = 0` [t_278]
- [SUSPICIOUS] line 1974: `unsigned int backup_cont_1 = cont_state_1` [t_278, pi_150]
- [SUSPICIOUS] line 1975: `int i_1 = 0` [t_279, pi_151]
- [POST] line 1975: `i_1 < 15` [t_280]
- [POST] line 1976: `i_1 >= 0` [t_281]
- [SUSPICIOUS] line 1975: `i_1++` [t_283, pi_153]
- [POST] line 1975: `i_1 < 15` [t_284]
- [POST] line 1976: `i_1 >= 0` [t_285]
- [SUSPICIOUS] line 1975: `i_1++` [t_287, pi_155]
- [POST] line 1975: `i_1 < 15` [t_288]
- [POST] line 1976: `i_1 >= 0` [t_289]
- [SUSPICIOUS] line 1975: `i_1++` [t_291, pi_157]
- [POST] line 1975: `i_1 < 15` [t_292]
- [POST] line 1976: `i_1 >= 0` [t_293]
- [SUSPICIOUS] line 1975: `i_1++` [t_295, pi_159]
- [POST] line 1975: `i_1 < 15` [t_296]
- [POST] line 1976: `i_1 >= 0` [t_297]
- [SUSPICIOUS] line 1975: `i_1++` [t_299, pi_161]
- [POST] line 1975: `i_1 < 15` [t_300]
- [POST] line 1976: `i_1 >= 0` [t_301]
- [SUSPICIOUS] line 1975: `i_1++` [t_303, pi_163]
- [POST] line 1975: `i_1 < 15` [t_304]
- [POST] line 1976: `i_1 >= 0` [t_305]
- [SUSPICIOUS] line 1975: `i_1++` [t_307, pi_165]
- [POST] line 1975: `i_1 < 15` [t_308]
- [POST] line 1976: `i_1 >= 0` [t_309]
- [SUSPICIOUS] line 1975: `i_1++` [t_311, pi_167]
- [POST] line 1975: `i_1 < 15` [t_312]
- [POST] line 1976: `i_1 >= 0` [t_313]
- [SUSPICIOUS] line 1975: `i_1++` [t_315, pi_169]
- [POST] line 1975: `i_1 < 15` [t_316]
- [POST] line 1976: `i_1 >= 0` [t_317]
- [SUSPICIOUS] line 1975: `i_1++` [t_319, pi_171]
- [POST] line 1975: `i_1 < 15` [t_320]
- [POST] line 1976: `i_1 >= 0` [t_321]
- [SUSPICIOUS] line 1975: `i_1++` [t_323, pi_173]
- [POST] line 1975: `i_1 < 15` [t_324]
- [POST] line 1976: `i_1 >= 0` [t_325]
- [SUSPICIOUS] line 1975: `i_1++` [t_327, pi_175]
- [POST] line 1975: `i_1 < 15` [t_328]
- [POST] line 1976: `i_1 >= 0` [t_329]
- [SUSPICIOUS] line 1975: `i_1++` [t_331, pi_177]
- [POST] line 1975: `i_1 < 15` [t_332]
- [POST] line 1976: `i_1 >= 0` [t_333]
- [SUSPICIOUS] line 1975: `i_1++` [t_335, pi_179]
- [POST] line 1975: `i_1 < 15` [t_336]
- [POST] line 1976: `i_1 >= 0` [t_337]
- [SUSPICIOUS] line 1975: `i_1++` [t_339, pi_181]
- [POST] line 1975: `!(i_1 < 15)` [t_340]
- [POST] line 1980: `!(cont_state_1 != backup_cont_1)` [t_341]
- [PRE] line 1985: `carry_state_1 = 0` [t_343]
- [SUSPICIOUS] line 1985: `unsigned int orig_1 = carry_state_1` [t_343, pi_182]
- [SUSPICIOUS] line 1986: `int i_1 = 0` [t_344, pi_183]
- [POST] line 1986: `i_1 < 12` [t_345]
- [SUSPICIOUS] line 1987: `carry_state_1 ^= i_1` [t_346, pi_184]
- [SUSPICIOUS] line 1988: `carry_state_1 ^= i_1` [t_347, pi_185]
- [SUSPICIOUS] line 1986: `i_1++` [t_348, pi_186]
- [POST] line 1986: `i_1 < 12` [t_349]
- [SUSPICIOUS] line 1987: `carry_state_1 ^= i_1` [t_350, pi_187]
- [SUSPICIOUS] line 1988: `carry_state_1 ^= i_1` [t_351, pi_188]
- [SUSPICIOUS] line 1986: `i_1++` [t_352, pi_189]
- [POST] line 1986: `i_1 < 12` [t_353]
- [SUSPICIOUS] line 1987: `carry_state_1 ^= i_1` [t_354, pi_190]
- [SUSPICIOUS] line 1988: `carry_state_1 ^= i_1` [t_355, pi_191]
- [SUSPICIOUS] line 1986: `i_1++` [t_356, pi_192]
- [POST] line 1986: `i_1 < 12` [t_357]
- [SUSPICIOUS] line 1987: `carry_state_1 ^= i_1` [t_358, pi_193]
- [SUSPICIOUS] line 1988: `carry_state_1 ^= i_1` [t_359, pi_194]
- [SUSPICIOUS] line 1986: `i_1++` [t_360, pi_195]
- [POST] line 1986: `i_1 < 12` [t_361]
- [SUSPICIOUS] line 1987: `carry_state_1 ^= i_1` [t_362, pi_196]
- [SUSPICIOUS] line 1988: `carry_state_1 ^= i_1` [t_363, pi_197]
- [SUSPICIOUS] line 1986: `i_1++` [t_364, pi_198]
- [POST] line 1986: `i_1 < 12` [t_365]
- [SUSPICIOUS] line 1987: `carry_state_1 ^= i_1` [t_366, pi_199]
- [SUSPICIOUS] line 1988: `carry_state_1 ^= i_1` [t_367, pi_200]
- [SUSPICIOUS] line 1986: `i_1++` [t_368, pi_201]
- [POST] line 1986: `i_1 < 12` [t_369]
- [SUSPICIOUS] line 1987: `carry_state_1 ^= i_1` [t_370, pi_202]
- [SUSPICIOUS] line 1988: `carry_state_1 ^= i_1` [t_371, pi_203]
- [SUSPICIOUS] line 1986: `i_1++` [t_372, pi_204]
- [POST] line 1986: `i_1 < 12` [t_373]
- [SUSPICIOUS] line 1987: `carry_state_1 ^= i_1` [t_374, pi_205]
- [SUSPICIOUS] line 1988: `carry_state_1 ^= i_1` [t_375, pi_206]
- [SUSPICIOUS] line 1986: `i_1++` [t_376, pi_207]
- [POST] line 1986: `i_1 < 12` [t_377]
- [SUSPICIOUS] line 1987: `carry_state_1 ^= i_1` [t_378, pi_208]
- [SUSPICIOUS] line 1988: `carry_state_1 ^= i_1` [t_379, pi_209]
- [SUSPICIOUS] line 1986: `i_1++` [t_380, pi_210]
- [POST] line 1986: `i_1 < 12` [t_381]
- [SUSPICIOUS] line 1987: `carry_state_1 ^= i_1` [t_382, pi_211]
- [SUSPICIOUS] line 1988: `carry_state_1 ^= i_1` [t_383, pi_212]
- [SUSPICIOUS] line 1986: `i_1++` [t_384, pi_213]
- [POST] line 1986: `i_1 < 12` [t_385]
- [SUSPICIOUS] line 1987: `carry_state_1 ^= i_1` [t_386, pi_214]
- [SUSPICIOUS] line 1988: `carry_state_1 ^= i_1` [t_387, pi_215]
- [SUSPICIOUS] line 1986: `i_1++` [t_388, pi_216]
- [POST] line 1986: `i_1 < 12` [t_389]
- [SUSPICIOUS] line 1987: `carry_state_1 ^= i_1` [t_390, pi_217]
- [SUSPICIOUS] line 1988: `carry_state_1 ^= i_1` [t_391, pi_218]
- [SUSPICIOUS] line 1986: `i_1++` [t_392, pi_219]
- [POST] line 1986: `!(i_1 < 12)` [t_393]
- [POST] line 1990: `!(carry_state_1 != orig_1)` [t_394]
- [PRE] line 1995: `nested_state_1 = 0` [t_396]
- [SUSPICIOUS] line 1995: `unsigned int backup_nested_1 = nested_state_1` [t_396, pi_220]
- [SUSPICIOUS] line 1996: `int i = 0` [t_397, pi_221]
- [POST] line 1996: `i < 20` [t_398]
- [POST] line 1997: `1` [t_399]
- [SUSPICIOUS] line 1996: `i++` [t_401, pi_223]
- [POST] line 1996: `i < 20` [t_402]
- [POST] line 1997: `1` [t_403]
- [SUSPICIOUS] line 1996: `i++` [t_405, pi_225]
- [POST] line 1996: `i < 20` [t_406]
- [POST] line 1997: `1` [t_407]
- [SUSPICIOUS] line 1996: `i++` [t_409, pi_227]
- [POST] line 1996: `i < 20` [t_410]
- [POST] line 1997: `1` [t_411]
- [SUSPICIOUS] line 1996: `i++` [t_413, pi_229]
- [POST] line 1996: `i < 20` [t_414]
- [POST] line 1997: `1` [t_415]
- [SUSPICIOUS] line 1996: `i++` [t_417, pi_231]
- [POST] line 1996: `i < 20` [t_418]
- [POST] line 1997: `1` [t_419]
- [SUSPICIOUS] line 1996: `i++` [t_421, pi_233]
- [POST] line 1996: `i < 20` [t_422]
- [POST] line 1997: `1` [t_423]
- [SUSPICIOUS] line 1996: `i++` [t_425, pi_235]
- [POST] line 1996: `i < 20` [t_426]
- [POST] line 1997: `1` [t_427]
- [SUSPICIOUS] line 1996: `i++` [t_429, pi_237]
- [POST] line 1996: `i < 20` [t_430]
- [POST] line 1997: `1` [t_431]
- [SUSPICIOUS] line 1996: `i++` [t_433, pi_239]
- [POST] line 1996: `i < 20` [t_434]
- [POST] line 1997: `1` [t_435]
- [SUSPICIOUS] line 1996: `i++` [t_437, pi_241]
- [POST] line 1996: `i < 20` [t_438]
- [POST] line 1997: `1` [t_439]
- [SUSPICIOUS] line 1996: `i++` [t_441, pi_243]
- [POST] line 1996: `i < 20` [t_442]
- [POST] line 1997: `1` [t_443]
- [SUSPICIOUS] line 1996: `i++` [t_445, pi_245]
- [POST] line 1996: `i < 20` [t_446]
- [POST] line 1997: `1` [t_447]
- [SUSPICIOUS] line 1996: `i++` [t_449, pi_247]
- [POST] line 1996: `i < 20` [t_450]
- [POST] line 1997: `1` [t_451]
- [SUSPICIOUS] line 1996: `i++` [t_453, pi_249]
- [POST] line 1996: `i < 20` [t_454]
- [POST] line 1997: `1` [t_455]
- [SUSPICIOUS] line 1996: `i++` [t_457, pi_251]
- [POST] line 1996: `i < 20` [t_458]
- [POST] line 1997: `1` [t_459]
- [SUSPICIOUS] line 1996: `i++` [t_461, pi_253]
- [POST] line 1996: `i < 20` [t_462]
- [POST] line 1997: `1` [t_463]
- [SUSPICIOUS] line 1996: `i++` [t_465, pi_255]
- [POST] line 1996: `i < 20` [t_466]
- [POST] line 1997: `1` [t_467]
- [SUSPICIOUS] line 1996: `i++` [t_469, pi_257]
- [POST] line 1996: `i < 20` [t_470]
- [POST] line 1997: `1` [t_471]
- [SUSPICIOUS] line 1996: `i++` [t_473, pi_259]
- [POST] line 1996: `i < 20` [t_474]
- [POST] line 1997: `1` [t_475]
- [SUSPICIOUS] line 1996: `i++` [t_477, pi_261]
- [POST] line 1996: `!(i < 20)` [t_478]
- [POST] line 2002: `!(nested_state_1 != backup_nested_1)` [t_479]
- [PRE] line 2006: `input_0 = 89` [t_480]
- [POST] line 2007: `(input_0 ^ 86) == 15` [t_481]
- [PRE] line 2012: `input_1 = 28` [t_483]
- [POST] line 2013: `(input_1 ^ 26) == 6` [t_484]
- [PRE] line 2018: `input_2 = 252` [t_486]
- [POST] line 2019: `(input_2 ^ 173) == 81` [t_487]
- [PRE] line 2024: `input_3 = 165` [t_489]
- [POST] line 2025: `(input_3 ^ 222) == 123` [t_490]
- [PRE] line 2030: `input_4 = 12` [t_492]
- [POST] line 2031: `(input_4 ^ 93) == 81` [t_493]
- [PRE] line 2036: `input_5 = 121` [t_495]
- [POST] line 2037: `(input_5 ^ 239) == 150` [t_496]
- [PRE] line 2042: `input_6 = 124` [t_498]
- [POST] line 2043: `(input_6 ^ 85) == 41` [t_499]
- [PRE] line 2048: `input_7 = 54` [t_501]
- [POST] line 2049: `(input_7 ^ 63) == 9` [t_502]
- [PRE] line 2054: `input_8 = 51` [t_504]
- [POST] line 2055: `(input_8 ^ 241) == 194` [t_505]
- [PRE] line 2060: `input_9 = 250` [t_507]
- [POST] line 2061: `(input_9 ^ 142) == 116` [t_508]
- [PRE] line 2066: `input_10 = 171` [t_510]
- [POST] line 2067: `(input_10 ^ 147) == 56` [t_511]
- [PRE] line 2072: `input_11 = 213` [t_513]
- [POST] line 2073: `(input_11 ^ 220) == 9` [t_514]
- [PRE] line 2078: `input_12 = 27` [t_516]
- [POST] line 2079: `(input_12 ^ 53) == 46` [t_517]
- [PRE] line 2084: `input_13 = 155` [t_519]
- [POST] line 2085: `(input_13 ^ 157) == 6` [t_520]
- [PRE] line 2090: `input_14 = 73` [t_522]
- [POST] line 2091: `(input_14 ^ 68) == 13` [t_523]
- [PRE] line 2096: `input_15 = 45` [t_525]
- [POST] line 2097: `(input_15 ^ 37) == 8` [t_526]
- [PRE] line 2102: `input_16 = 8` [t_528]
- [POST] line 2103: `(input_16 ^ 56) == 48` [t_529]
- [PRE] line 2108: `input_17 = 28` [t_531]
- [POST] line 2109: `(input_17 ^ 16) == 12` [t_532]
- [PRE] line 2114: `input_18 = 68` [t_534]
- [POST] line 2115: `(input_18 ^ 67) == 7` [t_535]
- [PRE] line 2120: `input_19 = 53` [t_537]
- [POST] line 2121: `(input_19 ^ 35) == 22` [t_538]
- [POST] target: `target/reach_error is not reached`

## 2. Postcondition Detail

Error guard:

All of these path guards must hold to reach the target:

```text
line 1779: !((critical_gate_1 & 1u) != 0u)
line 1782: step_1 < 6
line 1783: (step_1 & 1u) == 0u
line 1782: step_1 < 6
line 1783: !((step_1 & 1u) == 0u)
line 1791: !((step_1 + 1) == 6)
line 1782: step_1 < 6
line 1783: (step_1 & 1u) == 0u
line 1782: step_1 < 6
line 1783: !((step_1 & 1u) == 0u)
line 1791: !((step_1 + 1) == 6)
line 1782: step_1 < 6
line 1783: (step_1 & 1u) == 0u
line 1782: step_1 < 6
line 1783: !((step_1 & 1u) == 0u)
line 1791: (step_1 + 1) == 6
line 1798: tick_1 < 7
line 1803: !((tick_1 + 1) == 7)
line 1798: tick_1 < 7
line 1803: !((tick_1 + 1) == 7)
line 1798: tick_1 < 7
line 1803: !((tick_1 + 1) == 7)
line 1798: tick_1 < 7
line 1803: !((tick_1 + 1) == 7)
line 1798: tick_1 < 7
line 1803: !((tick_1 + 1) == 7)
line 1798: tick_1 < 7
line 1803: !((tick_1 + 1) == 7)
line 1798: tick_1 < 7
line 1803: (tick_1 + 1) == 7
line 1807: !(related_gate_1 != related_tracker_1)
line 1812: idx_1 < 5
line 1813: ((unrelated_lane_1 + idx_1) & 1u) == 0u
line 1812: idx_1 < 5
line 1813: !(((unrelated_lane_1 + idx_1) & 1u) == 0u)
line 1818: !((idx_1 + 2) == 5)
line 1812: idx_1 < 5
line 1813: ((unrelated_lane_1 + idx_1) & 1u) == 0u
line 1812: idx_1 < 5
line 1813: !(((unrelated_lane_1 + idx_1) & 1u) == 0u)
line 1818: (idx_1 + 2) == 5
line 1859: !(related_switch_1 != related_marker_1)
line 1895: dw_1 < 11
line 1895: dw_1 < 11
line 1895: dw_1 < 11
line 1895: dw_1 < 11
line 1895: dw_1 < 11
line 1895: dw_1 < 11
line 1895: dw_1 < 11
line 1895: dw_1 < 11
line 1895: dw_1 < 11
line 1895: dw_1 < 11
line 1895: !(dw_1 < 11)
line 1899: !(do_state_1 != (backup_do_1 ^ 11))
line 1903: loop_45278 < 14
line 1903: loop_45278 < 14
line 1903: loop_45278 < 14
line 1903: loop_45278 < 14
line 1903: loop_45278 < 14
line 1903: loop_45278 < 14
line 1903: loop_45278 < 14
line 1903: loop_45278 < 14
line 1903: loop_45278 < 14
line 1903: loop_45278 < 14
line 1903: loop_45278 < 14
line 1903: loop_45278 < 14
line 1903: loop_45278 < 14
line 1903: loop_45278 < 14
line 1903: !(loop_45278 < 14)
line 1911: while_cnt > 0
line 1911: while_cnt > 0
line 1911: while_cnt > 0
line 1911: while_cnt > 0
line 1911: while_cnt > 0
line 1911: while_cnt > 0
line 1911: while_cnt > 0
line 1911: while_cnt > 0
line 1911: while_cnt > 0
line 1911: while_cnt > 0
line 1911: while_cnt > 0
line 1911: !(while_cnt > 0)
line 1945: i_1 < 17
line 1945: i_1 < 17
line 1945: i_1 < 17
line 1945: i_1 < 17
line 1945: i_1 < 17
line 1945: i_1 < 17
line 1945: i_1 < 17
line 1945: i_1 < 17
line 1945: i_1 < 17
line 1945: i_1 < 17
line 1945: i_1 < 17
line 1945: i_1 < 17
line 1945: i_1 < 17
line 1945: i_1 < 17
line 1945: i_1 < 17
line 1945: i_1 < 17
line 1945: i_1 < 17
line 1945: !(i_1 < 17)
line 1949: !(fake_state_1 != backup_fakecont_1)
line 1955: break_state_1 < (break_state_1 + 1000)
line 1959: !(break_state_1 != original_1)
line 1965: i_1 < 16
line 1965: i_1 < 16
line 1965: i_1 < 16
line 1965: i_1 < 16
line 1965: i_1 < 16
line 1965: i_1 < 16
line 1965: i_1 < 16
line 1965: i_1 < 16
line 1965: i_1 < 16
line 1965: i_1 < 16
line 1965: i_1 < 16
line 1965: i_1 < 16
line 1965: i_1 < 16
line 1965: i_1 < 16
line 1965: i_1 < 16
line 1965: i_1 < 16
line 1965: !(i_1 < 16)
line 1969: !(overwrite_state_1 != saved_1)
line 1975: i_1 < 15
line 1976: i_1 >= 0
line 1975: i_1 < 15
line 1976: i_1 >= 0
line 1975: i_1 < 15
line 1976: i_1 >= 0
line 1975: i_1 < 15
line 1976: i_1 >= 0
line 1975: i_1 < 15
line 1976: i_1 >= 0
line 1975: i_1 < 15
line 1976: i_1 >= 0
line 1975: i_1 < 15
line 1976: i_1 >= 0
line 1975: i_1 < 15
line 1976: i_1 >= 0
line 1975: i_1 < 15
line 1976: i_1 >= 0
line 1975: i_1 < 15
line 1976: i_1 >= 0
line 1975: i_1 < 15
line 1976: i_1 >= 0
line 1975: i_1 < 15
line 1976: i_1 >= 0
line 1975: i_1 < 15
line 1976: i_1 >= 0
line 1975: i_1 < 15
line 1976: i_1 >= 0
line 1975: i_1 < 15
line 1976: i_1 >= 0
line 1975: !(i_1 < 15)
line 1980: !(cont_state_1 != backup_cont_1)
line 1986: i_1 < 12
line 1986: i_1 < 12
line 1986: i_1 < 12
line 1986: i_1 < 12
line 1986: i_1 < 12
line 1986: i_1 < 12
line 1986: i_1 < 12
line 1986: i_1 < 12
line 1986: i_1 < 12
line 1986: i_1 < 12
line 1986: i_1 < 12
line 1986: i_1 < 12
line 1986: !(i_1 < 12)
line 1990: !(carry_state_1 != orig_1)
line 1996: i < 20
line 1997: 1
line 1996: i < 20
line 1997: 1
line 1996: i < 20
line 1997: 1
line 1996: i < 20
line 1997: 1
line 1996: i < 20
line 1997: 1
line 1996: i < 20
line 1997: 1
line 1996: i < 20
line 1997: 1
line 1996: i < 20
line 1997: 1
line 1996: i < 20
line 1997: 1
line 1996: i < 20
line 1997: 1
line 1996: i < 20
line 1997: 1
line 1996: i < 20
line 1997: 1
line 1996: i < 20
line 1997: 1
line 1996: i < 20
line 1997: 1
line 1996: i < 20
line 1997: 1
line 1996: i < 20
line 1997: 1
line 1996: i < 20
line 1997: 1
line 1996: i < 20
line 1997: 1
line 1996: i < 20
line 1997: 1
line 1996: i < 20
line 1997: 1
line 1996: !(i < 20)
line 2002: !(nested_state_1 != backup_nested_1)
line 2007: (input_0 ^ 86) == 15
line 2013: (input_1 ^ 26) == 6
line 2019: (input_2 ^ 173) == 81
line 2025: (input_3 ^ 222) == 123
line 2031: (input_4 ^ 93) == 81
line 2037: (input_5 ^ 239) == 150
line 2043: (input_6 ^ 85) == 41
line 2049: (input_7 ^ 63) == 9
line 2055: (input_8 ^ 241) == 194
line 2061: (input_9 ^ 142) == 116
line 2067: (input_10 ^ 147) == 56
line 2073: (input_11 ^ 220) == 9
line 2079: (input_12 ^ 53) == 46
line 2085: (input_13 ^ 157) == 6
line 2091: (input_14 ^ 68) == 13
line 2097: (input_15 ^ 37) == 8
line 2103: (input_16 ^ 56) == 48
line 2109: (input_17 ^ 16) == 12
line 2115: (input_18 ^ 67) == 7
line 2121: (input_19 ^ 35) == 22
```

Safe postcondition:

```text
target/reach_error is not reached
equivalently: at least one path guard above is false in its SSA state
```

## 3. UNSAT Check

Query:

```text
input_values AND pi AND safe_postcondition
```

Result: `unsat`

Why suspicious:

Z3 returned UNSAT. The tracked pi formulas whose literals are in the unsat core are suspicious; their CFA edges are reported below.

UNSAT core literals:

```text
a_225
a_223
a_221
a_257
a_220
a_219
a_173
a_171
a_169
a_167
a_165
a_218
a_227
a_235
a_231
a_229
a_251
a_237
a_233
a_43
a_42
a_41
a_39
a_37
a_36
a_34
a_33
a_31
a_30
a_29
a_28
a_27
a_26
a_25
a_24
a_23
a_22
a_21
a_20
a_19
a_18
a_17
a_16
a_15
a_14
a_13
a_12
a_11
a_10
a_8
a_6
a_5
a_3
a_2
a_0
a_209
a_210
a_211
a_212
a_213
a_214
a_215
a_216
a_217
a_116
a_118
a_120
a_122
a_124
a_126
a_128
a_129
a_132
a_133
a_134
a_135
a_106
a_108
a_110
a_112
a_114
a_53
a_94
a_96
a_98
a_100
a_102
a_104
a_54
a_55
a_56
a_57
a_58
a_59
a_60
a_77
a_201
a_78
a_202
a_203
a_204
a_205
a_206
a_207
a_208
a_79
a_80
a_81
a_82
a_83
a_84
a_85
a_44
a_45
a_46
a_47
a_48
a_49
a_50
a_51
a_52
a_175
a_153
a_155
a_157
a_159
a_161
a_163
a_177
a_179
a_181
a_182
a_183
a_184
a_86
a_87
a_88
a_89
a_90
a_91
a_92
a_93
a_144
a_145
a_146
a_147
a_148
a_149
a_150
a_151
a_69
a_136
a_137
a_138
a_139
a_140
a_141
a_142
a_143
a_70
a_71
a_72
a_73
a_74
a_75
a_76
a_193
a_194
a_195
a_196
a_197
a_198
a_199
a_200
a_185
a_61
a_186
a_187
a_188
a_189
a_190
a_191
a_192
a_62
a_63
a_64
a_65
a_66
a_67
a_68
a_249
a_253
a_255
a_259
a_261
a_247
a_239
a_241
a_245
a_243
```

## 4. Pi Trace Formula

pi_0: line 1782: `int step_1 = 0;` => `int step_1 = 0`
pi_1: line 1785: `continue;` => `continue`
pi_2: line 1782: `++step_1;` => `++step_1`
pi_3: line 1782: `++step_1;` => `++step_1`
pi_4: line 1785: `continue;` => `continue`
pi_5: line 1782: `++step_1;` => `++step_1`
pi_6: line 1782: `++step_1;` => `++step_1`
pi_7: line 1785: `continue;` => `continue`
pi_8: line 1782: `++step_1;` => `++step_1`
pi_9: line 1792: `break;` => `break`
pi_10: line 1797: `unsigned int related_tracker_1 = related_gate_1;` => `unsigned int related_tracker_1 = related_gate_1`
pi_11: line 1798: `int tick_1 = 0;` => `int tick_1 = 0`
pi_12: line 1799: `unsigned int __tmp_1 = related_gate_1;` => `unsigned int __tmp_1 = related_gate_1`
pi_13: line 1802: `related_gate_1 = __tmp_1;` => `related_gate_1 = __tmp_1`
pi_14: line 1798: `++tick_1;` => `++tick_1`
pi_15: line 1799: `unsigned int __tmp_1 = related_gate_1;` => `unsigned int __tmp_1 = related_gate_1`
pi_16: line 1802: `related_gate_1 = __tmp_1;` => `related_gate_1 = __tmp_1`
pi_17: line 1798: `++tick_1;` => `++tick_1`
pi_18: line 1799: `unsigned int __tmp_1 = related_gate_1;` => `unsigned int __tmp_1 = related_gate_1`
pi_19: line 1802: `related_gate_1 = __tmp_1;` => `related_gate_1 = __tmp_1`
pi_20: line 1798: `++tick_1;` => `++tick_1`
pi_21: line 1799: `unsigned int __tmp_1 = related_gate_1;` => `unsigned int __tmp_1 = related_gate_1`
pi_22: line 1802: `related_gate_1 = __tmp_1;` => `related_gate_1 = __tmp_1`
pi_23: line 1798: `++tick_1;` => `++tick_1`
pi_24: line 1799: `unsigned int __tmp_1 = related_gate_1;` => `unsigned int __tmp_1 = related_gate_1`
pi_25: line 1802: `related_gate_1 = __tmp_1;` => `related_gate_1 = __tmp_1`
pi_26: line 1798: `++tick_1;` => `++tick_1`
pi_27: line 1799: `unsigned int __tmp_1 = related_gate_1;` => `unsigned int __tmp_1 = related_gate_1`
pi_28: line 1802: `related_gate_1 = __tmp_1;` => `related_gate_1 = __tmp_1`
pi_29: line 1798: `++tick_1;` => `++tick_1`
pi_30: line 1799: `unsigned int __tmp_1 = related_gate_1;` => `unsigned int __tmp_1 = related_gate_1`
pi_31: line 1802: `related_gate_1 = __tmp_1;` => `related_gate_1 = __tmp_1`
pi_32: line 1804: `break;` => `break`
pi_33: line 1811: `unsigned int unrelated_lane_1 = (unsigned int) 8;` => `unsigned int unrelated_lane_1 = (unsigned int) 8`
pi_34: line 1812: `int idx_1 = 0;` => `int idx_1 = 0`
pi_35: line 1815: `continue;` => `continue`
pi_36: line 1812: `++idx_1;` => `++idx_1`
pi_37: line 1812: `++idx_1;` => `++idx_1`
pi_38: line 1815: `continue;` => `continue`
pi_39: line 1812: `++idx_1;` => `++idx_1`
pi_40: line 1819: `break;` => `break`
pi_41: line 1836: `unsigned int related_marker_1 = related_switch_1;` => `unsigned int related_marker_1 = related_switch_1`
pi_42: line 1893: `unsigned int backup_do_1 = do_state_1;` => `unsigned int backup_do_1 = do_state_1`
pi_43: line 1894: `int dw_1 = 0;` => `int dw_1 = 0`
pi_44: line 1896: `do_state_1 ^= dw_1;` => `do_state_1 ^= dw_1`
pi_45: line 1897: `dw_1++;` => `dw_1++`
pi_46: line 1896: `do_state_1 ^= dw_1;` => `do_state_1 ^= dw_1`
pi_47: line 1897: `dw_1++;` => `dw_1++`
pi_48: line 1896: `do_state_1 ^= dw_1;` => `do_state_1 ^= dw_1`
pi_49: line 1897: `dw_1++;` => `dw_1++`
pi_50: line 1896: `do_state_1 ^= dw_1;` => `do_state_1 ^= dw_1`
pi_51: line 1897: `dw_1++;` => `dw_1++`
pi_52: line 1896: `do_state_1 ^= dw_1;` => `do_state_1 ^= dw_1`
pi_53: line 1897: `dw_1++;` => `dw_1++`
pi_54: line 1896: `do_state_1 ^= dw_1;` => `do_state_1 ^= dw_1`
pi_55: line 1897: `dw_1++;` => `dw_1++`
pi_56: line 1896: `do_state_1 ^= dw_1;` => `do_state_1 ^= dw_1`
pi_57: line 1897: `dw_1++;` => `dw_1++`
pi_58: line 1896: `do_state_1 ^= dw_1;` => `do_state_1 ^= dw_1`
pi_59: line 1897: `dw_1++;` => `dw_1++`
pi_60: line 1896: `do_state_1 ^= dw_1;` => `do_state_1 ^= dw_1`
pi_61: line 1897: `dw_1++;` => `dw_1++`
pi_62: line 1896: `do_state_1 ^= dw_1;` => `do_state_1 ^= dw_1`
pi_63: line 1897: `dw_1++;` => `dw_1++`
pi_64: line 1896: `do_state_1 ^= dw_1;` => `do_state_1 ^= dw_1`
pi_65: line 1897: `dw_1++;` => `dw_1++`
pi_66: line 1903: `int loop_45278 = 0;` => `int loop_45278 = 0`
pi_67: line 1903: `loop_45278++;` => `loop_45278++`
pi_68: line 1903: `loop_45278++;` => `loop_45278++`
pi_69: line 1903: `loop_45278++;` => `loop_45278++`
pi_70: line 1903: `loop_45278++;` => `loop_45278++`
pi_71: line 1903: `loop_45278++;` => `loop_45278++`
pi_72: line 1903: `loop_45278++;` => `loop_45278++`
pi_73: line 1903: `loop_45278++;` => `loop_45278++`
pi_74: line 1903: `loop_45278++;` => `loop_45278++`
pi_75: line 1903: `loop_45278++;` => `loop_45278++`
pi_76: line 1903: `loop_45278++;` => `loop_45278++`
pi_77: line 1903: `loop_45278++;` => `loop_45278++`
pi_78: line 1903: `loop_45278++;` => `loop_45278++`
pi_79: line 1903: `loop_45278++;` => `loop_45278++`
pi_80: line 1903: `loop_45278++;` => `loop_45278++`
pi_81: line 1910: `int while_cnt = 11;` => `int while_cnt = 11`
pi_82: line 1913: `while_cnt--;` => `while_cnt--`
pi_83: line 1913: `while_cnt--;` => `while_cnt--`
pi_84: line 1913: `while_cnt--;` => `while_cnt--`
pi_85: line 1913: `while_cnt--;` => `while_cnt--`
pi_86: line 1913: `while_cnt--;` => `while_cnt--`
pi_87: line 1913: `while_cnt--;` => `while_cnt--`
pi_88: line 1913: `while_cnt--;` => `while_cnt--`
pi_89: line 1913: `while_cnt--;` => `while_cnt--`
pi_90: line 1913: `while_cnt--;` => `while_cnt--`
pi_91: line 1913: `while_cnt--;` => `while_cnt--`
pi_92: line 1913: `while_cnt--;` => `while_cnt--`
pi_93: line 1944: `unsigned int backup_fakecont_1 = fake_state_1;` => `unsigned int backup_fakecont_1 = fake_state_1`
pi_94: line 1945: `int i_1 = 0;` => `int i_1 = 0`
pi_95: line 1946: `continue;` => `continue`
pi_96: line 1945: `i_1++;` => `i_1++`
pi_97: line 1946: `continue;` => `continue`
pi_98: line 1945: `i_1++;` => `i_1++`
pi_99: line 1946: `continue;` => `continue`
pi_100: line 1945: `i_1++;` => `i_1++`
pi_101: line 1946: `continue;` => `continue`
pi_102: line 1945: `i_1++;` => `i_1++`
pi_103: line 1946: `continue;` => `continue`
pi_104: line 1945: `i_1++;` => `i_1++`
pi_105: line 1946: `continue;` => `continue`
pi_106: line 1945: `i_1++;` => `i_1++`
pi_107: line 1946: `continue;` => `continue`
pi_108: line 1945: `i_1++;` => `i_1++`
pi_109: line 1946: `continue;` => `continue`
pi_110: line 1945: `i_1++;` => `i_1++`
pi_111: line 1946: `continue;` => `continue`
pi_112: line 1945: `i_1++;` => `i_1++`
pi_113: line 1946: `continue;` => `continue`
pi_114: line 1945: `i_1++;` => `i_1++`
pi_115: line 1946: `continue;` => `continue`
pi_116: line 1945: `i_1++;` => `i_1++`
pi_117: line 1946: `continue;` => `continue`
pi_118: line 1945: `i_1++;` => `i_1++`
pi_119: line 1946: `continue;` => `continue`
pi_120: line 1945: `i_1++;` => `i_1++`
pi_121: line 1946: `continue;` => `continue`
pi_122: line 1945: `i_1++;` => `i_1++`
pi_123: line 1946: `continue;` => `continue`
pi_124: line 1945: `i_1++;` => `i_1++`
pi_125: line 1946: `continue;` => `continue`
pi_126: line 1945: `i_1++;` => `i_1++`
pi_127: line 1946: `continue;` => `continue`
pi_128: line 1945: `i_1++;` => `i_1++`
pi_129: line 1954: `unsigned int original_1 = break_state_1;` => `unsigned int original_1 = break_state_1`
pi_130: line 1956: `break;` => `break`
pi_131: line 1964: `unsigned int saved_1 = overwrite_state_1;` => `unsigned int saved_1 = overwrite_state_1`
pi_132: line 1965: `int i_1 = 0;` => `int i_1 = 0`
pi_133: line 1965: `i_1++;` => `i_1++`
pi_134: line 1965: `i_1++;` => `i_1++`
pi_135: line 1965: `i_1++;` => `i_1++`
pi_136: line 1965: `i_1++;` => `i_1++`
pi_137: line 1965: `i_1++;` => `i_1++`
pi_138: line 1965: `i_1++;` => `i_1++`
pi_139: line 1965: `i_1++;` => `i_1++`
pi_140: line 1965: `i_1++;` => `i_1++`
pi_141: line 1965: `i_1++;` => `i_1++`
pi_142: line 1965: `i_1++;` => `i_1++`
pi_143: line 1965: `i_1++;` => `i_1++`
pi_144: line 1965: `i_1++;` => `i_1++`
pi_145: line 1965: `i_1++;` => `i_1++`
pi_146: line 1965: `i_1++;` => `i_1++`
pi_147: line 1965: `i_1++;` => `i_1++`
pi_148: line 1965: `i_1++;` => `i_1++`
pi_149: line 1968: `overwrite_state_1 = saved_1;` => `overwrite_state_1 = saved_1`
pi_150: line 1974: `unsigned int backup_cont_1 = cont_state_1;` => `unsigned int backup_cont_1 = cont_state_1`
pi_151: line 1975: `int i_1 = 0;` => `int i_1 = 0`
pi_152: line 1977: `continue;` => `continue`
pi_153: line 1975: `i_1++;` => `i_1++`
pi_154: line 1977: `continue;` => `continue`
pi_155: line 1975: `i_1++;` => `i_1++`
pi_156: line 1977: `continue;` => `continue`
pi_157: line 1975: `i_1++;` => `i_1++`
pi_158: line 1977: `continue;` => `continue`
pi_159: line 1975: `i_1++;` => `i_1++`
pi_160: line 1977: `continue;` => `continue`
pi_161: line 1975: `i_1++;` => `i_1++`
pi_162: line 1977: `continue;` => `continue`
pi_163: line 1975: `i_1++;` => `i_1++`
pi_164: line 1977: `continue;` => `continue`
pi_165: line 1975: `i_1++;` => `i_1++`
pi_166: line 1977: `continue;` => `continue`
pi_167: line 1975: `i_1++;` => `i_1++`
pi_168: line 1977: `continue;` => `continue`
pi_169: line 1975: `i_1++;` => `i_1++`
pi_170: line 1977: `continue;` => `continue`
pi_171: line 1975: `i_1++;` => `i_1++`
pi_172: line 1977: `continue;` => `continue`
pi_173: line 1975: `i_1++;` => `i_1++`
pi_174: line 1977: `continue;` => `continue`
pi_175: line 1975: `i_1++;` => `i_1++`
pi_176: line 1977: `continue;` => `continue`
pi_177: line 1975: `i_1++;` => `i_1++`
pi_178: line 1977: `continue;` => `continue`
pi_179: line 1975: `i_1++;` => `i_1++`
pi_180: line 1977: `continue;` => `continue`
pi_181: line 1975: `i_1++;` => `i_1++`
pi_182: line 1985: `unsigned int orig_1 = carry_state_1;` => `unsigned int orig_1 = carry_state_1`
pi_183: line 1986: `int i_1 = 0;` => `int i_1 = 0`
pi_184: line 1987: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
pi_185: line 1988: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
pi_186: line 1986: `i_1++;` => `i_1++`
pi_187: line 1987: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
pi_188: line 1988: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
pi_189: line 1986: `i_1++;` => `i_1++`
pi_190: line 1987: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
pi_191: line 1988: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
pi_192: line 1986: `i_1++;` => `i_1++`
pi_193: line 1987: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
pi_194: line 1988: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
pi_195: line 1986: `i_1++;` => `i_1++`
pi_196: line 1987: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
pi_197: line 1988: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
pi_198: line 1986: `i_1++;` => `i_1++`
pi_199: line 1987: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
pi_200: line 1988: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
pi_201: line 1986: `i_1++;` => `i_1++`
pi_202: line 1987: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
pi_203: line 1988: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
pi_204: line 1986: `i_1++;` => `i_1++`
pi_205: line 1987: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
pi_206: line 1988: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
pi_207: line 1986: `i_1++;` => `i_1++`
pi_208: line 1987: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
pi_209: line 1988: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
pi_210: line 1986: `i_1++;` => `i_1++`
pi_211: line 1987: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
pi_212: line 1988: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
pi_213: line 1986: `i_1++;` => `i_1++`
pi_214: line 1987: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
pi_215: line 1988: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
pi_216: line 1986: `i_1++;` => `i_1++`
pi_217: line 1987: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
pi_218: line 1988: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
pi_219: line 1986: `i_1++;` => `i_1++`
pi_220: line 1995: `unsigned int backup_nested_1 = nested_state_1;` => `unsigned int backup_nested_1 = nested_state_1`
pi_221: line 1996: `int i = 0;` => `int i = 0`
pi_222: line 1998: `break;` => `break`
pi_223: line 1996: `i++;` => `i++`
pi_224: line 1998: `break;` => `break`
pi_225: line 1996: `i++;` => `i++`
pi_226: line 1998: `break;` => `break`
pi_227: line 1996: `i++;` => `i++`
pi_228: line 1998: `break;` => `break`
pi_229: line 1996: `i++;` => `i++`
pi_230: line 1998: `break;` => `break`
pi_231: line 1996: `i++;` => `i++`
pi_232: line 1998: `break;` => `break`
pi_233: line 1996: `i++;` => `i++`
pi_234: line 1998: `break;` => `break`
pi_235: line 1996: `i++;` => `i++`
pi_236: line 1998: `break;` => `break`
pi_237: line 1996: `i++;` => `i++`
pi_238: line 1998: `break;` => `break`
pi_239: line 1996: `i++;` => `i++`
pi_240: line 1998: `break;` => `break`
pi_241: line 1996: `i++;` => `i++`
pi_242: line 1998: `break;` => `break`
pi_243: line 1996: `i++;` => `i++`
pi_244: line 1998: `break;` => `break`
pi_245: line 1996: `i++;` => `i++`
pi_246: line 1998: `break;` => `break`
pi_247: line 1996: `i++;` => `i++`
pi_248: line 1998: `break;` => `break`
pi_249: line 1996: `i++;` => `i++`
pi_250: line 1998: `break;` => `break`
pi_251: line 1996: `i++;` => `i++`
pi_252: line 1998: `break;` => `break`
pi_253: line 1996: `i++;` => `i++`
pi_254: line 1998: `break;` => `break`
pi_255: line 1996: `i++;` => `i++`
pi_256: line 1998: `break;` => `break`
pi_257: line 1996: `i++;` => `i++`
pi_258: line 1998: `break;` => `break`
pi_259: line 1996: `i++;` => `i++`
pi_260: line 1998: `break;` => `break`
pi_261: line 1996: `i++;` => `i++`
pi_262: line 2008: `input_0 = input_0 ^ 9126;` => `input_0 = input_0 ^ 9126`
pi_263: line 2014: `input_1 = input_1 ^ 1788;` => `input_1 = input_1 ^ 1788`
pi_264: line 2020: `input_2 = input_2 ^ 8563;` => `input_2 = input_2 ^ 8563`
pi_265: line 2026: `input_3 = input_3 ^ 1091;` => `input_3 = input_3 ^ 1091`
pi_266: line 2032: `input_4 = input_4 ^ 4583;` => `input_4 = input_4 ^ 4583`
pi_267: line 2038: `input_5 = input_5 ^ 3881;` => `input_5 = input_5 ^ 3881`
pi_268: line 2044: `input_6 = input_6 ^ 1538;` => `input_6 = input_6 ^ 1538`
pi_269: line 2050: `input_7 = input_7 ^ 7563;` => `input_7 = input_7 ^ 7563`
pi_270: line 2056: `input_8 = input_8 ^ 123;` => `input_8 = input_8 ^ 123`
pi_271: line 2062: `input_9 = input_9 ^ 998;` => `input_9 = input_9 ^ 998`
pi_272: line 2068: `input_10 = input_10 ^ 273;` => `input_10 = input_10 ^ 273`
pi_273: line 2074: `input_11 = input_11 ^ 1335;` => `input_11 = input_11 ^ 1335`
pi_274: line 2080: `input_12 = input_12 ^ 929;` => `input_12 = input_12 ^ 929`
pi_275: line 2086: `input_13 = input_13 ^ 224;` => `input_13 = input_13 ^ 224`
pi_276: line 2092: `input_14 = input_14 ^ 7871;` => `input_14 = input_14 ^ 7871`
pi_277: line 2098: `input_15 = input_15 ^ 1946;` => `input_15 = input_15 ^ 1946`
pi_278: line 2104: `input_16 = input_16 ^ 5921;` => `input_16 = input_16 ^ 5921`
pi_279: line 2110: `input_17 = input_17 ^ 9875;` => `input_17 = input_17 ^ 9875`
pi_280: line 2116: `input_18 = input_18 ^ 2315;` => `input_18 = input_18 ^ 2315`
pi_281: line 2122: `input_19 = input_19 ^ 7606;` => `input_19 = input_19 ^ 7606`

## 5. Suspicious Pi Formulas

- pi_0: line 1782: `int step_1 = 0;` => `int step_1 = 0`
- pi_2: line 1782: `++step_1;` => `++step_1`
- pi_3: line 1782: `++step_1;` => `++step_1`
- pi_5: line 1782: `++step_1;` => `++step_1`
- pi_6: line 1782: `++step_1;` => `++step_1`
- pi_8: line 1782: `++step_1;` => `++step_1`
- pi_10: line 1797: `unsigned int related_tracker_1 = related_gate_1;` => `unsigned int related_tracker_1 = related_gate_1`
- pi_11: line 1798: `int tick_1 = 0;` => `int tick_1 = 0`
- pi_12: line 1799: `unsigned int __tmp_1 = related_gate_1;` => `unsigned int __tmp_1 = related_gate_1`
- pi_13: line 1802: `related_gate_1 = __tmp_1;` => `related_gate_1 = __tmp_1`
- pi_14: line 1798: `++tick_1;` => `++tick_1`
- pi_15: line 1799: `unsigned int __tmp_1 = related_gate_1;` => `unsigned int __tmp_1 = related_gate_1`
- pi_16: line 1802: `related_gate_1 = __tmp_1;` => `related_gate_1 = __tmp_1`
- pi_17: line 1798: `++tick_1;` => `++tick_1`
- pi_18: line 1799: `unsigned int __tmp_1 = related_gate_1;` => `unsigned int __tmp_1 = related_gate_1`
- pi_19: line 1802: `related_gate_1 = __tmp_1;` => `related_gate_1 = __tmp_1`
- pi_20: line 1798: `++tick_1;` => `++tick_1`
- pi_21: line 1799: `unsigned int __tmp_1 = related_gate_1;` => `unsigned int __tmp_1 = related_gate_1`
- pi_22: line 1802: `related_gate_1 = __tmp_1;` => `related_gate_1 = __tmp_1`
- pi_23: line 1798: `++tick_1;` => `++tick_1`
- pi_24: line 1799: `unsigned int __tmp_1 = related_gate_1;` => `unsigned int __tmp_1 = related_gate_1`
- pi_25: line 1802: `related_gate_1 = __tmp_1;` => `related_gate_1 = __tmp_1`
- pi_26: line 1798: `++tick_1;` => `++tick_1`
- pi_27: line 1799: `unsigned int __tmp_1 = related_gate_1;` => `unsigned int __tmp_1 = related_gate_1`
- pi_28: line 1802: `related_gate_1 = __tmp_1;` => `related_gate_1 = __tmp_1`
- pi_29: line 1798: `++tick_1;` => `++tick_1`
- pi_30: line 1799: `unsigned int __tmp_1 = related_gate_1;` => `unsigned int __tmp_1 = related_gate_1`
- pi_31: line 1802: `related_gate_1 = __tmp_1;` => `related_gate_1 = __tmp_1`
- pi_33: line 1811: `unsigned int unrelated_lane_1 = (unsigned int) 8;` => `unsigned int unrelated_lane_1 = (unsigned int) 8`
- pi_34: line 1812: `int idx_1 = 0;` => `int idx_1 = 0`
- pi_36: line 1812: `++idx_1;` => `++idx_1`
- pi_37: line 1812: `++idx_1;` => `++idx_1`
- pi_39: line 1812: `++idx_1;` => `++idx_1`
- pi_41: line 1836: `unsigned int related_marker_1 = related_switch_1;` => `unsigned int related_marker_1 = related_switch_1`
- pi_42: line 1893: `unsigned int backup_do_1 = do_state_1;` => `unsigned int backup_do_1 = do_state_1`
- pi_43: line 1894: `int dw_1 = 0;` => `int dw_1 = 0`
- pi_44: line 1896: `do_state_1 ^= dw_1;` => `do_state_1 ^= dw_1`
- pi_45: line 1897: `dw_1++;` => `dw_1++`
- pi_46: line 1896: `do_state_1 ^= dw_1;` => `do_state_1 ^= dw_1`
- pi_47: line 1897: `dw_1++;` => `dw_1++`
- pi_48: line 1896: `do_state_1 ^= dw_1;` => `do_state_1 ^= dw_1`
- pi_49: line 1897: `dw_1++;` => `dw_1++`
- pi_50: line 1896: `do_state_1 ^= dw_1;` => `do_state_1 ^= dw_1`
- pi_51: line 1897: `dw_1++;` => `dw_1++`
- pi_52: line 1896: `do_state_1 ^= dw_1;` => `do_state_1 ^= dw_1`
- pi_53: line 1897: `dw_1++;` => `dw_1++`
- pi_54: line 1896: `do_state_1 ^= dw_1;` => `do_state_1 ^= dw_1`
- pi_55: line 1897: `dw_1++;` => `dw_1++`
- pi_56: line 1896: `do_state_1 ^= dw_1;` => `do_state_1 ^= dw_1`
- pi_57: line 1897: `dw_1++;` => `dw_1++`
- pi_58: line 1896: `do_state_1 ^= dw_1;` => `do_state_1 ^= dw_1`
- pi_59: line 1897: `dw_1++;` => `dw_1++`
- pi_60: line 1896: `do_state_1 ^= dw_1;` => `do_state_1 ^= dw_1`
- pi_61: line 1897: `dw_1++;` => `dw_1++`
- pi_62: line 1896: `do_state_1 ^= dw_1;` => `do_state_1 ^= dw_1`
- pi_63: line 1897: `dw_1++;` => `dw_1++`
- pi_64: line 1896: `do_state_1 ^= dw_1;` => `do_state_1 ^= dw_1`
- pi_65: line 1897: `dw_1++;` => `dw_1++`
- pi_66: line 1903: `int loop_45278 = 0;` => `int loop_45278 = 0`
- pi_67: line 1903: `loop_45278++;` => `loop_45278++`
- pi_68: line 1903: `loop_45278++;` => `loop_45278++`
- pi_69: line 1903: `loop_45278++;` => `loop_45278++`
- pi_70: line 1903: `loop_45278++;` => `loop_45278++`
- pi_71: line 1903: `loop_45278++;` => `loop_45278++`
- pi_72: line 1903: `loop_45278++;` => `loop_45278++`
- pi_73: line 1903: `loop_45278++;` => `loop_45278++`
- pi_74: line 1903: `loop_45278++;` => `loop_45278++`
- pi_75: line 1903: `loop_45278++;` => `loop_45278++`
- pi_76: line 1903: `loop_45278++;` => `loop_45278++`
- pi_77: line 1903: `loop_45278++;` => `loop_45278++`
- pi_78: line 1903: `loop_45278++;` => `loop_45278++`
- pi_79: line 1903: `loop_45278++;` => `loop_45278++`
- pi_80: line 1903: `loop_45278++;` => `loop_45278++`
- pi_81: line 1910: `int while_cnt = 11;` => `int while_cnt = 11`
- pi_82: line 1913: `while_cnt--;` => `while_cnt--`
- pi_83: line 1913: `while_cnt--;` => `while_cnt--`
- pi_84: line 1913: `while_cnt--;` => `while_cnt--`
- pi_85: line 1913: `while_cnt--;` => `while_cnt--`
- pi_86: line 1913: `while_cnt--;` => `while_cnt--`
- pi_87: line 1913: `while_cnt--;` => `while_cnt--`
- pi_88: line 1913: `while_cnt--;` => `while_cnt--`
- pi_89: line 1913: `while_cnt--;` => `while_cnt--`
- pi_90: line 1913: `while_cnt--;` => `while_cnt--`
- pi_91: line 1913: `while_cnt--;` => `while_cnt--`
- pi_92: line 1913: `while_cnt--;` => `while_cnt--`
- pi_93: line 1944: `unsigned int backup_fakecont_1 = fake_state_1;` => `unsigned int backup_fakecont_1 = fake_state_1`
- pi_94: line 1945: `int i_1 = 0;` => `int i_1 = 0`
- pi_96: line 1945: `i_1++;` => `i_1++`
- pi_98: line 1945: `i_1++;` => `i_1++`
- pi_100: line 1945: `i_1++;` => `i_1++`
- pi_102: line 1945: `i_1++;` => `i_1++`
- pi_104: line 1945: `i_1++;` => `i_1++`
- pi_106: line 1945: `i_1++;` => `i_1++`
- pi_108: line 1945: `i_1++;` => `i_1++`
- pi_110: line 1945: `i_1++;` => `i_1++`
- pi_112: line 1945: `i_1++;` => `i_1++`
- pi_114: line 1945: `i_1++;` => `i_1++`
- pi_116: line 1945: `i_1++;` => `i_1++`
- pi_118: line 1945: `i_1++;` => `i_1++`
- pi_120: line 1945: `i_1++;` => `i_1++`
- pi_122: line 1945: `i_1++;` => `i_1++`
- pi_124: line 1945: `i_1++;` => `i_1++`
- pi_126: line 1945: `i_1++;` => `i_1++`
- pi_128: line 1945: `i_1++;` => `i_1++`
- pi_129: line 1954: `unsigned int original_1 = break_state_1;` => `unsigned int original_1 = break_state_1`
- pi_132: line 1965: `int i_1 = 0;` => `int i_1 = 0`
- pi_133: line 1965: `i_1++;` => `i_1++`
- pi_134: line 1965: `i_1++;` => `i_1++`
- pi_135: line 1965: `i_1++;` => `i_1++`
- pi_136: line 1965: `i_1++;` => `i_1++`
- pi_137: line 1965: `i_1++;` => `i_1++`
- pi_138: line 1965: `i_1++;` => `i_1++`
- pi_139: line 1965: `i_1++;` => `i_1++`
- pi_140: line 1965: `i_1++;` => `i_1++`
- pi_141: line 1965: `i_1++;` => `i_1++`
- pi_142: line 1965: `i_1++;` => `i_1++`
- pi_143: line 1965: `i_1++;` => `i_1++`
- pi_144: line 1965: `i_1++;` => `i_1++`
- pi_145: line 1965: `i_1++;` => `i_1++`
- pi_146: line 1965: `i_1++;` => `i_1++`
- pi_147: line 1965: `i_1++;` => `i_1++`
- pi_148: line 1965: `i_1++;` => `i_1++`
- pi_149: line 1968: `overwrite_state_1 = saved_1;` => `overwrite_state_1 = saved_1`
- pi_150: line 1974: `unsigned int backup_cont_1 = cont_state_1;` => `unsigned int backup_cont_1 = cont_state_1`
- pi_151: line 1975: `int i_1 = 0;` => `int i_1 = 0`
- pi_153: line 1975: `i_1++;` => `i_1++`
- pi_155: line 1975: `i_1++;` => `i_1++`
- pi_157: line 1975: `i_1++;` => `i_1++`
- pi_159: line 1975: `i_1++;` => `i_1++`
- pi_161: line 1975: `i_1++;` => `i_1++`
- pi_163: line 1975: `i_1++;` => `i_1++`
- pi_165: line 1975: `i_1++;` => `i_1++`
- pi_167: line 1975: `i_1++;` => `i_1++`
- pi_169: line 1975: `i_1++;` => `i_1++`
- pi_171: line 1975: `i_1++;` => `i_1++`
- pi_173: line 1975: `i_1++;` => `i_1++`
- pi_175: line 1975: `i_1++;` => `i_1++`
- pi_177: line 1975: `i_1++;` => `i_1++`
- pi_179: line 1975: `i_1++;` => `i_1++`
- pi_181: line 1975: `i_1++;` => `i_1++`
- pi_182: line 1985: `unsigned int orig_1 = carry_state_1;` => `unsigned int orig_1 = carry_state_1`
- pi_183: line 1986: `int i_1 = 0;` => `int i_1 = 0`
- pi_184: line 1987: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
- pi_185: line 1988: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
- pi_186: line 1986: `i_1++;` => `i_1++`
- pi_187: line 1987: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
- pi_188: line 1988: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
- pi_189: line 1986: `i_1++;` => `i_1++`
- pi_190: line 1987: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
- pi_191: line 1988: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
- pi_192: line 1986: `i_1++;` => `i_1++`
- pi_193: line 1987: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
- pi_194: line 1988: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
- pi_195: line 1986: `i_1++;` => `i_1++`
- pi_196: line 1987: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
- pi_197: line 1988: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
- pi_198: line 1986: `i_1++;` => `i_1++`
- pi_199: line 1987: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
- pi_200: line 1988: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
- pi_201: line 1986: `i_1++;` => `i_1++`
- pi_202: line 1987: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
- pi_203: line 1988: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
- pi_204: line 1986: `i_1++;` => `i_1++`
- pi_205: line 1987: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
- pi_206: line 1988: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
- pi_207: line 1986: `i_1++;` => `i_1++`
- pi_208: line 1987: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
- pi_209: line 1988: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
- pi_210: line 1986: `i_1++;` => `i_1++`
- pi_211: line 1987: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
- pi_212: line 1988: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
- pi_213: line 1986: `i_1++;` => `i_1++`
- pi_214: line 1987: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
- pi_215: line 1988: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
- pi_216: line 1986: `i_1++;` => `i_1++`
- pi_217: line 1987: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
- pi_218: line 1988: `carry_state_1 ^= i_1;` => `carry_state_1 ^= i_1`
- pi_219: line 1986: `i_1++;` => `i_1++`
- pi_220: line 1995: `unsigned int backup_nested_1 = nested_state_1;` => `unsigned int backup_nested_1 = nested_state_1`
- pi_221: line 1996: `int i = 0;` => `int i = 0`
- pi_223: line 1996: `i++;` => `i++`
- pi_225: line 1996: `i++;` => `i++`
- pi_227: line 1996: `i++;` => `i++`
- pi_229: line 1996: `i++;` => `i++`
- pi_231: line 1996: `i++;` => `i++`
- pi_233: line 1996: `i++;` => `i++`
- pi_235: line 1996: `i++;` => `i++`
- pi_237: line 1996: `i++;` => `i++`
- pi_239: line 1996: `i++;` => `i++`
- pi_241: line 1996: `i++;` => `i++`
- pi_243: line 1996: `i++;` => `i++`
- pi_245: line 1996: `i++;` => `i++`
- pi_247: line 1996: `i++;` => `i++`
- pi_249: line 1996: `i++;` => `i++`
- pi_251: line 1996: `i++;` => `i++`
- pi_253: line 1996: `i++;` => `i++`
- pi_255: line 1996: `i++;` => `i++`
- pi_257: line 1996: `i++;` => `i++`
- pi_259: line 1996: `i++;` => `i++`
- pi_261: line 1996: `i++;` => `i++`

## 6. Reduction Outputs

- `state`: 238 waypoints -> `unsafe4.reduced.witness.state.yml`
- `match`: 238 waypoints -> `unsafe4.reduced.witness.match.yml`
- `all`: 126 waypoints -> `unsafe4.reduced.witness.yml`
