# Lisp Interpreter

This is a simple Lisp interpreter written in Python. It can run Lisp files made with a basic subset
of Common Lisp.

## Usage

To run a Lisp file, use the following command in this projects root directory:

```bash
python3 -m lisp <filename> [--debug]
```

The `--debug` flag will print each step of the evaluation process so you can see
how Lisp code is evaluated.

## Example Usage

You can run the example file in the `test` directory as follows:

```bash
python3 -m lisp test/example.lsp
```
