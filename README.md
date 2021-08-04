Executable example
===================

This is a Z3 Python 2.7 implementation of the application example of the chapter "Reasoning with First-Order Logic"


Documentation
-------------

```bash
pip install z3-solver
```
```bash
python model.py
```
output should be

```console
STEP 1: Check if the pre conditions of the required task are fulfilled by the available skill 'M_Capping'.
I.e. if the skill 'M_Capping' can be executed, are all the preconditions of the required production task fulfilled?
  unsat
  saving model to model_pre_conditions.smt2 ...
  Done.

STEP 2: Check if the restrictions on process execution are fulfilled if the skill 'M_Capping' is executed.
If the skill 'M_capping' is executed, are all restriction on process execution fulfilled?
  unsat
  saving model to model_conditions_exec.smt2 ...
  Done.

STEP 3: Check if the restrictions on post-material are fulfilled if the skill 'M_Capping' is executed.
If the skill 'M_capping' is executed, are all restrictions on post-material fulfilled?
  unsat
  saving model to model_post_conditions.smt2 ...
  Done.


Process finished with exit code 0
```

<!-- CONTRIBUTING -->
## Contributing

Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->
## License

See `LICENSE` for more information.

<!-- CONTACT -->
## Contact

Jupiter Bakakeu - [@JBakakeu](https://twitter.com/JBakakeu) - jupiter.bakakeu@gmail.com
