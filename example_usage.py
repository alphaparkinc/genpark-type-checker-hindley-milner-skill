from client import HMTypeInference, TypeVar, TypeOperator

def main():
    hm = HMTypeInference()
    int_t = TypeOperator("Int", [])
    str_t = TypeOperator("String", [])
    var_a = TypeVar("alpha")
    fn_a = TypeOperator("->", [var_a, int_t])
    fn_b = TypeOperator("->", [str_t, int_t])
    hm.unify(fn_a, fn_b)
    print("Hindley-Milner Type Inference Verification:")
    print(f"Unification successful!")
    print(f"Inferred alpha: {hm.prune(var_a)}")

if __name__ == "__main__":
    main()
