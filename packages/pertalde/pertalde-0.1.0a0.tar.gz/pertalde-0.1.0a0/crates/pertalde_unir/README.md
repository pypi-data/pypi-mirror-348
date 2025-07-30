
# pertalde

pertalde is a set of tools to manipulate traces. 

## pertalde separar

When you have a big trace that you want to analyse its common practice
to filter it. This tool has a preset of filters that you can use without
having to rely on a configuration generated from Paraver. Furthermore,
it allows to run multiple filters on a single execution. Which results
in generating the filters faster. Right now we have event filters for neSmiK,
MPI, OpenMP, Counters, and Flushing. And we have a useful filter with a
minimum duration threshold.

### How to use it.

```bash
pertalde separar --compress --useful 100 --profile=mpi,counters trace.prv
```

This will generate a directory names `test.partials`, which will contain
3 different traces with names
`trace.{useful,mpi,counters}.{prv.gz,pcf,row}`. Notice that this tool
can also leverage processing the trace to compress it with the flag
`--compress` which is available for all subcommands that produce output
traces.

## pertalde unir

When you a trace with sparse semantic values, and/or with inconsistent
value per semantic across traces you can use `pertalde unir`. This will
use the values from the `pcf` files to unify the values based on their
semantic, and translate the `prv` files accordingly. You can also group
different event types together to unify their semantics.

### How to use it.

**If you had a trace with different event** that share semantics but differ
in values. For a more specific example, lets say we have a `trace.prv`
with events `1000`, `1001`, `2000`, `2001`. Where events `1000` and
`1001` share meaning between them, and `2000` and `2001` between them.

```bash
pertalde unir --types=1000,1001 --types=2000,2001 trace.prv
```

This would result in a `trace.unir.prv` file where now all values that
have the same name for `1000` and `1001` have also the same value. And
all the same for values `2000` and `2001`.

**If you have multiple traces with the same event** but this event has
inconsistent values for the same semantic across traces, you can also
use `pertalde unir`. By running the same command on different traces,
the resulting event values will be common across traces also.

```bash
pertalde unir --types=1000,1001 trace1.prv trace2.prv
```

**In the case you get a new trace** and you want it to have common
values with a trace you have already processed earlier you can make use
of the option `--base-pcf`.

```bash
# This produces trace1.unir.prv trace1.unir.pcf and trace1.unir.row
pertalde unir --types=1000,1001 trace1.prv

# Now you get a new trace: trace2.prv
pertalde unir --types=1000,1001 --base-pcf=trace1.unir.pcf trace2.prv
```

This will make event values from types `1000` and `1001`, form
`trace2.prv`, consistent with those in `trace1.prv`.

**This tool has preset gorups** for specific tools. As this tool was
initially implemented to solve a common problem with `neSmiK` and
`nsys2prv` we have presets for this tools. For example, for nesmik you
could use:

```bash
pertalde unir --profile=nesmik trace.prv
```

## pertalde comprovar

This tool basically will test a trace to check if its well formatted. If
you are having problems with a trace, or are generating trace files,
this tool can tell you where the trace has format issues.

```bash
pertalde comprovar trace.prv
```

## pertalde sincronitzar

If you get a trace that is not synchronized, you can use this tool to
synchronize it based on an event. This is helpful when the merging
process is very long, or you no longer have the unmerged files. This
tool can only syncronize the MPI tasks.

```bash
# By default it will use the MPI init event.
pertalde syncronitzar trace.prv
```

