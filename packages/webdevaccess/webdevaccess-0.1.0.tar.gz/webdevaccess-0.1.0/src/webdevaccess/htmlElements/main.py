""" src/webdevaccess/htmlElements/main.py """

import logging
import jsonloggeriso8601datetime as jlidt

jlidt.setConfig()
logger = logging.getLogger(__name__)

from domible.elements import Html, Head, Body, Title, Base
from domible.elements import Heading, Anchor, Paragraph
from domible.builders.tableBuilder import TableBuilder
from domible.starterDocuments import basic_head_empty_body
from domible.tools import open_html_document_in_browser

from webdevaccess.htmlElements import mdnElements

import argparse 
parser = argparse.ArgumentParser(
    prog="htmlElements",
    description="scrape MDN to summarize all HTML elements in accessible tables",
    formatter_class=argparse.RawTextHelpFormatter,
    epilog="Cheers!",
)

parser.add_argument("-u", "--url_mdn", default="https://developer.mozilla.org")
parser.add_argument("-l", "--lang", default="en-US")
parser.add_argument("-o", "--outfile")
args = parser.parse_args()


def run():
    """
    elements is used to test, and provide an example of, Table and the tableBuilder
    it will scrape HTML element reference info from MDN and present it in a table in your default browser
    The HTML is also saved to a passed in file, not saved if no file specified.
    """
    mdn_base_url: str = args.url_mdn
    lang: str = args.lang
    outputfile: str = args.outfile

    if outputfile:
        print(f"saving html output to file: {outputfile}")
    title = "Tables of HTML Elements Scraped from MDN "
    htmlDoc = basic_head_empty_body(title, lang)
    head = htmlDoc.get_head_element()
    head.add_content(Base(href=mdn_base_url))
    body = htmlDoc.get_body_element()
    (currentElementsTable, deprecatedElementsTable) = mdnElements.getElementsTables(
        mdn_base_url, lang
    )
    if not currentElementsTable or not deprecatedElementsTable:
        body.add_content(
            Heading(1, f"failed to scrape elements from {mdnElements.MdnAnchor}")
        )
    else:
        # building up the body of the html document
        currentTable, _, _ = currentElementsTable.get_table()
        deprecatedTable, _, _ = deprecatedElementsTable.get_table()
        body.add_content(
            [
                Heading(1, title),
                Paragraph(
                    f"Information in the below tables was scraped from {mdnElements.MdnAnchor}."
                ),
                Heading(2, "Currently Supported HTML Elements"),
                currentTable,
                Heading(2, "Deprecated HTML Elements"),
                deprecatedTable,
            ]
        )
    open_html_document_in_browser(htmlDoc)


if __name__ == "__main__":
    run()

## end of file
