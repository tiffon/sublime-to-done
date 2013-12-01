# Sublime Text package for Rust

## About

This package is a simple tool for creating to do lists. To do lists are just text files with the extension "todo". The functionality of this package is based entirely on syntax highlighting.

![](https://raw.github.com/tiffon/sublime-to-done/master/img/example.png)

## Syntax

### Tasks

The format for a task item is generally a hyphen then a hard-tab then the task title:

```
-       Some title
```

The number of hyphens indicates the importance of the task: 5 hyphens for the most important, 1 hyphen for the least important.

```
-       Not that important
-----   Very important
```

### Sub tasks

Sub tasks are the same as any other task, they are just indented.
```
-       A top level task
        -       First sub task
        -       Second sub task
```

### Completed tasks

Completed tasks have a plus sign `+` in front of the first hyphen. Any sub-tasks are automatically considered completed.

```
+-      This is completed
        -       This task is considered completed, too
```

### Notes

A task can have notes associated with it. There are three formats for notes:

* Same line - all text after a colon `:`
```
-       Some title: This is a note
```

* New line - Lines of text with a greater indentation than the task's first hyphen
```
-       Some title
        This is a note
```

* Note block - Blocks of text starting and ending with three forward slashes `///`
```
-       Some title ///
        This is a note
        - this is still the note
        - and so is this
        ///
```

Text within a note can be emphasized by wrapping it with back quotes: `` ` ``
```
-       Some title: This has a `special` note
```
