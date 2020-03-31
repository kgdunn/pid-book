# Process Improvement using Data

All the reStructuredText (RST) source files for the book with this title.

## Book website (HTML and PDF)

https://learnche.org/pid

## How to compile the book yourself

You will need:

* Clone this repository, which we call `pid-book`, somewhere on your computer. The location is referred to `/location/of/pid-book/` in the example below.
* All the figures for the book, in a separate repository: https://github.com/kgdunn/figures. We call this `figures` in the text below.
* Python, [Sphinx](https://www.sphinx-doc.org/en/master/) and a working copy of LaTeX, if you wish to generate  the PDF version of the book. If you are interested only in making HTML, you only need Sphinx then.
* Around 2Gb (yes!) space for files, compiled documents and illustrations.
* A good text editor, with syntax highlighting for RST files. I use Visual Studio Code at the moment, but many IDE environments support syntax highlighting for RST source documents.

1. Clone the `figures` repository, preferably somewhere outside or next-to this repository.
2. Softlink the `figures` repo so that it is visible as the directory of the same name, but within `pid-book`. You could also just move the `figures` repo into this one, but that is hackish.

   `ln -s /location/of/figures /location/of/pid-book/figures`

3. `make clean`
4. `make html`   
5. `make latexpdf`

Step 4 is quick and is a good check if you have all the settings correct. Step 5 can take around 5 to 10 minutes to completely compile the PDF document. You can compare your PDF to the one of the website, https://learnche.org/pid/PID.pdf, to see if you successfully managed to reproduce it.


## Why would you want to compile it yourself?

Perhaps you would like to improve a section, customize the book for a course you are teaching, delete topics you don't want. Whatever the reason, you are allowed to do so. Everything provided to you is licensed as [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) license](https://creativecommons.org/licenses/by-sa/4.0/).

But that means, I still hold the copyright on the parts I've writted. Your adaptations are allowed, and in fact encouraged, but your changes must be distributed under the same, or similar, conditions as this license.

Surprise me! 