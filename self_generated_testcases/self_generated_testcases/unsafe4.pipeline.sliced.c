
extern void __assert_fail(const char *, const char *,
                          unsigned int, const char *)
  __attribute__ ((__nothrow__ , __leaf__))
  __attribute__ ((__noreturn__));

extern unsigned int __VERIFIER_nondet_uint(void);
extern int __VERIFIER_nondet_int(void);
extern _Bool __VERIFIER_nondet_bool(void);
extern char __VERIFIER_nondet_char(void);

void reach_error() {
    __assert_fail("0", "generated.c", 1, "reach_error");
}
int main() {
    unsigned int critical_gate_1 = __VERIFIER_nondet_uint();
    if ((critical_gate_1 & 1u) != 0u) {
    }
    for (int step_1=0; step_1<6; ++step_1) {
        if ((step_1 & 1u) == 0u) {
            continue;
        }
        if (step_1 + 1 == 6) {
            break;
        }
    }
    unsigned int related_gate_1 = __VERIFIER_nondet_uint();
    unsigned int related_tracker_1 = related_gate_1;
    for (int tick_1=0; tick_1<7; ++tick_1) {
        unsigned int __tmp_1 = related_gate_1;
        related_gate_1 = __tmp_1;
        if (tick_1 + 1 == 7) {
            break;
        }
    }
    if (related_gate_1 != related_tracker_1) {
    }
    unsigned int unrelated_lane_1 = (unsigned int)(8);
    for (int idx_1=0; idx_1<5; ++idx_1) {
        if (((unrelated_lane_1 + idx_1) & 1u) == 0u) {
            continue;
        }
        if (idx_1 + 2 == 5) {
            break;
        }
    }
    unsigned int related_switch_1 = __VERIFIER_nondet_uint();
    unsigned int related_marker_1 = related_switch_1;
    if (related_switch_1 != related_marker_1) {
    }
    unsigned int do_state_1 = __VERIFIER_nondet_uint();
    unsigned int backup_do_1 = do_state_1;
    int dw_1 = 0;
    do {
        do_state_1 ^= dw_1;
        dw_1++;
    } while(dw_1 < 11);
    if (do_state_1 != (backup_do_1 ^ 11)) {
    }
    for (int loop_45278=0; loop_45278<14; loop_45278++) {
    }
    int while_cnt = 11;
    while (while_cnt > 0) {
        while_cnt--;
    }
    unsigned int fake_state_1 = __VERIFIER_nondet_uint();
    unsigned int backup_fakecont_1 = fake_state_1;
    for (int i_1=0; i_1<17; i_1++) {
        continue;
        fake_state_1 += i_1;
    }
    if (fake_state_1 != backup_fakecont_1) {
    }
    unsigned int break_state_1 = __VERIFIER_nondet_uint();
    unsigned int original_1 = break_state_1;
    while (break_state_1 < break_state_1 + 1000) {
        break;
        break_state_1 += 99999;
    }
    if (break_state_1 != original_1) {
    }
    unsigned int overwrite_state_1 = __VERIFIER_nondet_uint();
    unsigned int saved_1 = overwrite_state_1;
    for (int i_1=0; i_1<16; i_1++) {
    }
    overwrite_state_1 = saved_1;
    if (overwrite_state_1 != saved_1) {
    }
    unsigned int cont_state_1 = __VERIFIER_nondet_uint();
    unsigned int backup_cont_1 = cont_state_1;
    for (int i_1=0; i_1<15; i_1++) {
        if (i_1 >= 0)
            continue;
        cont_state_1 += i_1;
    }
    if (cont_state_1 != backup_cont_1) {
    }
    unsigned int carry_state_1 = __VERIFIER_nondet_uint();
    unsigned int orig_1 = carry_state_1;
    for (int i_1=0; i_1<12; i_1++) {
        carry_state_1 ^= i_1;
        carry_state_1 ^= i_1;
    }
    if (carry_state_1 != orig_1) {
    }
    unsigned int nested_state_1 = __VERIFIER_nondet_uint();
    unsigned int backup_nested_1 = nested_state_1;
    for (int i=0;i<20;i++) {
        while (1) {
            break;
            nested_state_1 += i;
        }
    }
    if (nested_state_1 != backup_nested_1) {
    }
    unsigned int input_0 = __VERIFIER_nondet_uint();
    if ((input_0 ^ 86) == 15) {
        input_0 = input_0 ^ 9126;
    }
    unsigned int input_1 = __VERIFIER_nondet_uint();
    if ((input_1 ^ 26) == 6) {
        input_1 = input_1 ^ 1788;
    }
    unsigned int input_2 = __VERIFIER_nondet_uint();
    if ((input_2 ^ 173) == 81) {
        input_2 = input_2 ^ 8563;
    }
    unsigned int input_3 = __VERIFIER_nondet_uint();
    if ((input_3 ^ 222) == 123) {
        input_3 = input_3 ^ 1091;
    }
    unsigned int input_4 = __VERIFIER_nondet_uint();
    if ((input_4 ^ 93) == 81) {
        input_4 = input_4 ^ 4583;
    }
    unsigned int input_5 = __VERIFIER_nondet_uint();
    if ((input_5 ^ 239) == 150) {
        input_5 = input_5 ^ 3881;
    }
    unsigned int input_6 = __VERIFIER_nondet_uint();
    if ((input_6 ^ 85) == 41) {
        input_6 = input_6 ^ 1538;
    }
    unsigned int input_7 = __VERIFIER_nondet_uint();
    if ((input_7 ^ 63) == 9) {
        input_7 = input_7 ^ 7563;
    }
    unsigned int input_8 = __VERIFIER_nondet_uint();
    if ((input_8 ^ 241) == 194) {
        input_8 = input_8 ^ 123;
    }
    unsigned int input_9 = __VERIFIER_nondet_uint();
    if ((input_9 ^ 142) == 116) {
        input_9 = input_9 ^ 998;
    }
    unsigned int input_10 = __VERIFIER_nondet_uint();
    if ((input_10 ^ 147) == 56) {
        input_10 = input_10 ^ 273;
    }
    unsigned int input_11 = __VERIFIER_nondet_uint();
    if ((input_11 ^ 220) == 9) {
        input_11 = input_11 ^ 1335;
    }
    unsigned int input_12 = __VERIFIER_nondet_uint();
    if ((input_12 ^ 53) == 46) {
        input_12 = input_12 ^ 929;
    }
    unsigned int input_13 = __VERIFIER_nondet_uint();
    if ((input_13 ^ 157) == 6) {
        input_13 = input_13 ^ 224;
    }
    unsigned int input_14 = __VERIFIER_nondet_uint();
    if ((input_14 ^ 68) == 13) {
        input_14 = input_14 ^ 7871;
    }
    unsigned int input_15 = __VERIFIER_nondet_uint();
    if ((input_15 ^ 37) == 8) {
        input_15 = input_15 ^ 1946;
    }
    unsigned int input_16 = __VERIFIER_nondet_uint();
    if ((input_16 ^ 56) == 48) {
        input_16 = input_16 ^ 5921;
    }
    unsigned int input_17 = __VERIFIER_nondet_uint();
    if ((input_17 ^ 16) == 12) {
        input_17 = input_17 ^ 9875;
    }
    unsigned int input_18 = __VERIFIER_nondet_uint();
    if ((input_18 ^ 67) == 7) {
        input_18 = input_18 ^ 2315;
    }
    unsigned int input_19 = __VERIFIER_nondet_uint();
    if ((input_19 ^ 35) == 22) {
        input_19 = input_19 ^ 7606;
    }
    reach_error();
}
