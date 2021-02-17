def apply_koch_rule(seq):
    return seq.replace("F", "F-F++F-F")

def apply_hilbert_rules(seq):
    ret_s = ""
    for elem in seq:
        if elem == "X":
            c1 = elem.replace("X", "-YF+XFX+FY-")
            ret_s = ret_s + c1
        elif elem == "Y":
            c2 = elem.replace("Y", "+XF-YFY-FX+")
            ret_s = ret_s + c2
        else:
            ret_s = ret_s + elem
    return ret_s





def test_apply_rules():
    s1 = apply_rules("AB", ["A->AB", "B->BA"])
    s2 = apply_rules("AB", ["A->XY", "B->XZ"])
    assert(s1 == "ABBA" and s2 == "XYXZ"), "{} {}: apply rules failed".format(s1, s2) #and s2 == "XYXZ"
    print(s1, s2, "pass apply rules\n")

def main():
    test_apply_rules()

if __name__ == "__main__":
    main()
