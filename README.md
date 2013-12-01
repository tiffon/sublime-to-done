# Sublime Text package for to do list

## About

This package is a simple tool for creating to do lists. To do lists are just text files with the extension "todo". The functionality of this package is based entirely on a language syntax.

![](https://raw.github.com/tiffon/sublime-to-done/master/img/example.png)

## Content

### Tasks

The format for a task item is generally a hyphen then a hard-tab then the task title:

![](https://raw.github.com/tiffon/sublime-to-done/master/img/basic-task.png)

```
-       Some title
```

The number of hyphens indicates the importance of the task: 5 hyphens for the most important, 1 hyphen for the least important.

![](https://raw.github.com/tiffon/sublime-to-done/master/img/task-importance.png)

```
-       Not that important
-----   Very important
```

### Sub tasks

Sub tasks are the same as any other task, they are just indented.

![](https://raw.github.com/tiffon/sublime-to-done/master/img/sub-tasks.png)

```
-       A top level task
        -       First sub task
        -       Second sub task
```

### Notes

A task can have notes associated with it. There are three formats for notes:

**Same line** - All text after a colon `:`

![](https://raw.github.com/tiffon/sublime-to-done/master/img/note-same-line.png)

```
-       Some title: This is a note
```

**New line** - Lines of text with a greater indentation than the task's first hyphen

![](https://raw.github.com/tiffon/sublime-to-done/master/img/note-new-line.png)

```
-       Some title
        This is a note
```

**Note block** - Blocks of text starting and ending with three forward slashes `///`

![](https://raw.github.com/tiffon/sublime-to-done/master/img/note-block.png)

```
-       Some title ///
        This is a note
        - this is still the note
        - and so is this
        ///
```

Text within a note can be emphasized by wrapping it with back quotes: `` ` ``

![](https://raw.github.com/tiffon/sublime-to-done/master/img/note-emphasis.png)

```
-       Some title: This has a `special` note
```

## Task states

### Completed tasks

Completed tasks have a plus sign `+` in front of the first hyphen. Any sub-tasks are automatically considered completed.

![](https://raw.github.com/tiffon/sublime-to-done/master/img/task-state-completed.png)

```
+-      This is completed
        -       This sub task is considered completed, too
```

### Emergency tasks

Tasks can be emphasized by putting an exclamation mark `!` in front of the tasks first hyphen. This state is applied to any sub tasks.

![](https://raw.github.com/tiffon/sublime-to-done/master/img/task-state-emergency.png)

```
!-      This task is now considered dire
        -       So is this one, by association
```

### Cancelled tasks

Tasks can be dimmed to make them easier to ignore by putting a period `.` in front of the tasks first hyphen. A note about the cancellation can be defined by enclosing text in parentheses at the beginning of the title of the task. This state is applied to any sub tasks.

![](https://raw.github.com/tiffon/sublime-to-done/master/img/task-state-cancelled.png)

```
.-      (reason cancelled) Some title
        -       This is cancelled, too
```

## Goto

The goto menu (`super+r` on Mac) is set up to show only current tasks. Completed tasks and cancelled tasks are filtered out.

![](https://raw.github.com/tiffon/sublime-to-done/master/img/example-goto.png)
