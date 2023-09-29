# Fannish Utilities

Scripts I use for tasks like fanwork archival and conversion.  (Well, currently script _singular_, but more may come soon.)

## Installation

There isn't much, assuming you have a command line and a working python 3 install.  You'll need to install the Python dependencies with `pip3 install -r requirements.txt`.

I use [pandoc](https://pandoc.org/installing.html) for many conversion tasks (for example, converting HTML to LaTeX as step one of typesetting for ficbinding); it's not strictly required, but you may find that installing it makes your life easier.  And it's dead easy to use if you have any familiarity with the command line: the syntax for nearly all pandoc commands is `pandoc -i [name of input file] -o [name of output file]`; pandoc is smart enough to figure out that if your input file ends in `.html` and your output ends in `.tex`, you probably want html -> tex conversion.

## Usage 

### AO3 Styled Epub Downloader

It works like this:

```
python3 ao3_download_styled_epub.py [url of work on AO3]
```

This will output a file, in whatever directory you run it in, named `[work_id].epub` (the "work id" is the number you see in the URL, `archiveofourown.org/works/[work id]`; it makes a good filename because every fic on AO3 gets a unique one).  It uses the built-in AO3 epub downloader for structure (and, uh, will probably break if the AO3 epub downloader changes too much), but downloads and adds the workskin CSS and replaces all the chapter contents so the formatting matches what you get by looking at the fic in a browser.  (None of AO3's built-in downloaders download the workskin, and all of them strip any custom CSS classes defined in the workskin from the downloaded file, for portability reasons.)

There are no command-line options, config, etc.

## Other Useful Links for Fan Archivists

* archive.org archives of [AO3](https://archive.org/details/AO3_final_location) and [ffnet](https://archive.org/download/fanfictiondotnet_repack)
* FicHub's [ffnet exporter](https://fichub.net/)
* My [Tumblr tag](https://gender-trash.tumblr.com/tagged/datahoarding%20tag) for posts on archiving/datahoarding
* [Guide to finding danmei epubs](https://www.tumblr.com/mu-qingfang-stan-account/726745605416894464/btw-if-you-ever-cant-find-an?source=share), from my danmei sideblog
