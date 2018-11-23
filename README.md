# *viu*

A small *less*-like Python code viewer with responsive formatting and styling

![Demo](res/demo.gif)

## Installation

Install via pip (tested on *Linux* and *Windows Subsystem for Linux (WSL)*, but should work on OSX too):

```
pip install viu
```

Usage:

```
viu <your_file.py>
```

## About

Code style is important. Having consistently formatted code can make your programs easier to read and understand. But as with anything related to style, it's a matter of taste. There have been decade-long debates on line length, line wrapping, whitespace, single- vs. double quoted strings etc. and it's unlikely that all programmers will agree on one style in the future. And even if they would, the optimal style also depends on the environment in which you're viewing your code. Using a 79 character line lenght limit is a waste of space on a 4K screen, might fit well when viewing two editors side-by-side on a FullHD screen and be toally unreadable in a presentation or when doing a three-way merge on your laptop.

But does it have to be this way? What if you could ignore the messy style your colleague wrote and render code optimized to your personal preferences and your current environment.

This project is a small (< 200 LOC) experiment that demonstrates some of the advantages of separating the *meaning of code* from it's *style*. It's a command line code viewer that basically works like the linux `less` command. It uses [Black](https://github.com/ambv/black) for formatting code and [pygments](http://pygments.org/) for syntax highlighting. When resizing the console window, the code gets reformatted to fill the available space.

The original styling of the code doesn't matter as long as it's valid Python. In the future, tools like this could allow users to specify their preferred style and then render all code accordingly. By making code style a per-user decision instead of having to agree on a coding style in a team / project, this could finally bring an end to the pointless debates on *"right"* way to format your code.

### The bigger picture

Code is written, stored and read as a bunch of characters. We've done it this way for so long that most people don't even realize how limiting it can be. Forcing everyone working on the same code to use the same style doesn't work. In fact, one single style might not even work for you all the time.

This project might not be that useful after all, but I'd like you to imagine what source code "renderers" that aren't tied to the exact characters used in the source file might look like. I've shown that such a renderer can format code according to a style guide and adapt to the current window width, but you could do more. You could use parametric fonts and word wrapping for things like documentation and comments, render markdown to make it even more readable or display syntax you don't like in a different way (just imagine something like braceless-java for a moment :P). You could even use non-textual elements to display code (e.g. real lists / tables instead of a bunch of `[]` characters.

Should you do this? Well, honestly ... I don't know. Most of us are so used to how code looks that going crazy with formatting may subjectively reduce readability initially. I think that there might be better ways to represent code than the current staticly formatted lines of monospace characters. Maybe we just need to start experimenting. We are used to rich and responsive formatting of web content and even though some sites are barely readable, we wouldn't want to go back to the web of the 90s. Presenting code might not be that different.

## Feedback

I'd love to hear your feedback. Feel free to open an issue, send an [e-mail](mailto:felix.kohlgrueber@gmail.com) or reach out on twitter [@fkohlgrueber](https://twitter.com/fkohlgrueber).
