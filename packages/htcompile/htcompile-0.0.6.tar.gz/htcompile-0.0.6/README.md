# HTCompile

<a href="#about" class="btn">About</a>
<a href="#install" class="btn">Install</a>
<a href="#manual" class="btn">Manual</a>
<a href="https://github.com/KittKat7/htcompile" class="btn">Github</a>
<a href="https://pypi.org/project/htcompile/" class="btn">PyPi</a>

## About

HTCompile has compile-time imports to prevent the need to rewrite a page
header every on every single page. Instead, just import it at
compile-time! For an example, look at the source code for this website.

## Install

### Requirements

-   Python 3.9+

### Manual

-   Make sure python 3.9+ is installed by running `python --version`
-   Clone the GitHub repo to a location on your system
    `git clone https://github.com/KittKat7/htcompile.git`
-   The program can now be run by using
    `python PATH/TO/htcompile/main.py SOURCE DESTINATION`
-   (Optional) Add an alias in your shell rc file (IE ~/.bashrc).
    `alias 'htcompile'='python PATH/TO/htcompile/main.py` This will
    allow simply running `htcompile SOURCE DESTINATION`

### PIP - Recommended

-   Make sure python3 pip is installed for your system.
-   Run `pip install htcompile`
-   Make sure htcompile is installed by running `htcompile --help`

## User Manual

### Basics

Once the program is installed, the program can be run with
`htcompile SOURCER DESTINATION` to compile your website. `SOURCE` is the
source folder of the HTML and `DESTINATION` is the folder to output the
compiled HTML.  
The recommended file structure is:

    |--projectdir/
    |  |--src/
    |  |  |--index.html
    |  |  |--page-a/
    |  |  |  |--index.html
    |  |  |  |--another.html
    |  |  |--page-b/
    |  |     |--index.html
    |  |--dst/
    |  |  |--(this is where the compiled files will go)
                    

Then running the the program inside `projectdir` would look like this:  
`$ htcompile ./src ./dst`  
The generated files will be placed in `./dst`  
To utilize htcompile in your HTML, add a
`<htcompile src="/PATH/TO/FILE/>` Make note that starting the path with
"/" starts at the path provided as SOURCE to `htcompile`. IE in the file
structure above using `htcompile ./src ./dst` "/" would represent
"src/". To import `page-b` into `page-a` you would use
`<htcompile src="/page-b/index.html">`. On the other hand, "./" is
treated as relative to the files location, so to import `another.html`
into `page-a/index.html` you could either use
`<htcompile src="/page-a/another.html">` or
`<htcompile src="./another.html">` If you wanted to inport
`another.html` into `page-b/index.html` you would use
`<htcompile src="/page-a/another.html">`
