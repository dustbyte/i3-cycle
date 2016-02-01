# i3-cycle
i3 WM focus-like tool with cycling in mind

## Presentation
`i3-cycle` is a small python tool written for the [i3 Window Manager](http://i3wm.org/) that allows to cycle the focus across windows and monitors.

Given the following example:

```
        a                   b
+---------------+   +---------------+
|       |       |   |       |       |
|       |       |   |       |       |
|       |       |   |       |       |
|   1   |   2   |   |   3   |   4   |
|       |       |   |       |       |
|       |       |   |       |       |
|       |       |   |       |       |
+---------------+   +---------------+
```

Where `a` and `b` are different screens/monitors/outputs and `1`, `2`, `3` and `4` four different windows spread amongst the two screens.

If the focus if set on `2` and we want to set the focus to the right, with traditional `i3` focus, the target will be `3`.
With `i3-cycle`, the new focus recipient will be 1.

`i3-cycle` also works vertically, and allows to cycle directely through the different screens without requiring to move the focus through multiple windows before reaching it.

## Installation

`i3-cycle` is developed in [Python](https://www.python.org/) and requires [i3-py](https://github.com/ziberna/i3-py)

### Source Setup

```
$ git clone https://github.com/mota/i3-cycle.git
$ cd i3-cycle
$ python setup.py install
```

### Pypi Setup

```
$ pip install i3-cycle
```

or

```
$ easy_install i3-cycle
```

### Usage

#### As is

```
$ i3-cycle -h
usage: i3-cycle [-h] {up,down,left,right,next,prev}

positional arguments:
  {up,down,left,right,next,prev}
                        Direction to put the focus on

optional arguments:
  -h, --help            show this help message and exit
```

`up`, `down`, `left` and `right` allow to move through windows of the current workspace in a cycling fashion.
`next` and `prev` cycle through the screens.

#### With i3

Example i3 configuration

```
$ cat ~/.i3/config
...
bindsym $mod+} exec i3-cycle right
bindsym $mod+{ exec i3-cycle left
bindsym $mod+Shift+{ exec i3-cycle up
bindsym $mod+Shift+} exec i3-cycle down
bind $mod+49 exec i3-cycle next
bind $mod+Shift+49 exec i3-cycle prev
...
```
