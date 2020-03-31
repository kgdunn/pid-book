# Process Improvement using Data

All the reStructuredText (RST) source files for the book with this title.

## Book website (HTML and PDF)

https://learnche.org/pid

## How to compile the book yourself

You will need:

* All the figures for the book, in a separate repository: https://github.com/kgdunn/figures
* Python and Sphinx: https://www.sphinx-doc.org/en/master/
* Around 2Gb (yes!) space for files, compiled documents and illustrations

1. Clone the `figures` repository, preferable outside/next-to this repository.
2. Softlink the `figures` repo so that it is visible as the directory of the same name, but within in this repo. You could also just move the `figures` repo into this one, but that is hackish.

   `ln -s ../figures figures`

3. `make clean`
4. `make html`   
5. `make latexpdf`

Step 4 is quick and is a good check if you have all the settings correct. Step 5 can take around 5 to 10 minutes to completely compile the PDF document. You can compare your PDF to the one of the website, https://learnche.org/pid/PID.pdf, to see if you successfully managed to reproduce it.


## Why would you want to compile it yourself?

Perhaps you would like to improve a section, customize the book for a course you are teaching, delete topics you don't want. Whatever the reason, you are allowed to do so. Everything provided to you is licensed as [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) license](https://creativecommons.org/licenses/by-sa/4.0/).

But that means, I still hold the copyright on the parts I've writted. Your adaptations are allowed, and in fact encouraged, but your changes must be distributed under the same, or similar, conditions as this license.

Surprise me! 