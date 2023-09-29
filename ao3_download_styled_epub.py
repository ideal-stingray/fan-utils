# Python STL
import argparse
import requests

# Third-party
import AO3 as ao3
from ebooklib import epub
from bs4 import BeautifulSoup


def get_workskin(url):
    html = requests.get(url).content
    soup = BeautifulSoup(html, features="lxml")
    style = soup.find("style")
    return style.get_text()


def get_chapter_body(chapter_url, chapter_idx):
    html = requests.get(chapter_url).content
    soup = BeautifulSoup(html, features="lxml")
    for elm in soup.div.find_all(class_ = "chapter preface group"):
        elm.decompose()  # remove beginning and end notes

    chapter_body = soup.div.find(role="article")
    chapter_body["id"] = "workskin"
    del chapter_body["role"]
    del chapter_body["class"]
    chapter_body.find("h3").decompose()
    return chapter_body


def download_work(url):
    work_id = ao3.utils.workid_from_url(url)
    work = ao3.Work(work_id)

    filename = f"{work_id}.epub"
    with open(filename, "wb") as f:
        f.write(work.download(filetype="EPUB"))

    chapter_bodies = [
        get_chapter_body(chapter.url, i + 1) for i, chapter in enumerate(work.chapters)
    ]

    return filename, chapter_bodies


def modify_epub(filename, workskin, chapter_bodies):
    book = epub.read_epub(filename)

    workskin = epub.EpubItem(
        uid="workskin",
        file_name="style/workskin.css",
        media_type="text/css",
        content=workskin,
    )
    book.add_item(workskin)

    # chapter content in epub is all in <div class="userstuff2"> and chapters start
    # at [title]_split_002 (000 is metadata, 001 is summary/beginning notes)
    for item in book.items:
        if not isinstance(item, epub.EpubHtml):
            continue

        chapter_number = int(item.file_name.split(".")[0].split("_")[-1]) - 2
        if chapter_number < 0 or chapter_number >= len(chapter_bodies):
            continue

        try:
            epub_chapter_soup = BeautifulSoup(item.get_content(), features="lxml")
            epub_chapter_soup.div.find(class_ = "userstuff2").replace_with(
                chapter_bodies[chapter_number]
            )
            item.set_content(epub_chapter_soup.encode())
            item.add_item(workskin)
        except Exception as e:
            print(e)
            continue

    epub.write_epub(filename, book)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="AO3 Styled Epub Downloader")
    parser.add_argument("url", type=str)
    args = parser.parse_args()

    workskin = get_workskin(args.url)
    filename, chapter_bodies = download_work(args.url)
    modify_epub(filename, workskin, chapter_bodies)
