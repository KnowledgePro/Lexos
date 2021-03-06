Preprocessing your texts, what we refer to as "scrubbing", is a critical step in the Lexos workflow. In order to facilitate a conscious consideration of the many small decisions required, scrubbing options are isolated into individual choices. If for no other reason, your careful deliberation and choice of the many options facilitates a replication of your analyses in the future, both by you and others who wish to verify your experiment.

The Scrubber tool interface allows you to select and combine options on the left side of the screen. Click the **Preview Scrubbing** button to see the results in the preview windows below. At this point, only the beginning and ending of each document is displayed, separated by an ellipsis (…). When you are satisfied that you have achieved the desired effect, click the **Apply Scrubbing** button. Your documents will be scrubbed, and the scrubbed versions will be used by all the other Lexos tools.

Scrubbing affects all active documents and cannot be undone. So make sure to de-activate any documents you do not wish to scrub using the **Manage** tool. If you apply scrubbing and later wish to revert to the unscrubbed version, you will have to upload another copy to Lexos.

Scrubbing is an algorithm: a series of steps applied in a specific order. If you wish to change that order, you will need to de-select some options, scrub, re-select them, and then scrub again. The order of operations is provided in **The Lexos Scrubber Algorithm** section below.

### Scrubbing Options

1.  **Remove [Project Gutenberg](https://www.gutenberg.org) boilerplate material**: Upon entering the Scrubber page, if you have uploaded a file from the Project Gutenberg website without removing the boilerplate material (i.e., text added by the Project Gutenberg site at the top and license material at the end of the text), you will receive the following warning:

    > One or more files you uploaded contain Project Gutenberg licensure material. You should remove the beginning and ending material, save, and re-upload the edited version. If you Apply Scrubbing with a text with Gutenberg boilerplate, Lexos will attempt to remove the majority of the Project Gutenberg Licensure, however there may still be some unwanted material left over.

    Note that if you select the ‘Apply Scrubbing’ button without removing this extra text, Lexos will attempt to remove the Project Gutenberg boilerplate material at the top and end of the file. However, since Project Gutenberg texts do not have a consistent boilerplate format, we suggest you remove the boilerplate material using a text editor before uploading it to Lexos in order to prevent unwanted text from being included in subsequent analyses, e.g., including Project Gutenberg licensure material in your word counts. Lexos’ attempt to remove start and ending boilerplate material only applies to files from the Project Gutenberg website. When choosing a file from this website, we recommend the “Plain Text UTF-8” version. It is smaller, so it will upload faster, and you will not have to remove any HTML markup.

1.  **Remove All Punctuation**: Lexos assumes that uploaded files may be in any language and automatically converts them to [Unicode](https://en.wikipedia.org/wiki/Unicode) using [UTF-8 character encoding](https://en.wikipedia.org/wiki/UTF-8). This requires that Lexos recognize punctuation marks from a wide variety of languages. All Unicode characters have an associated set of metadata for classifying its “type”, e.g. as a letter, punctuation, or symbol. If the **Remove All Punctuation** option is selected, any Unicode character in each of the active texts with a “Punctuation Character Property” (that character’s property begins with a ‘P’) or a Symbol Character Property (begins with ‘S’) is removed. A guide to Unicode Character Categories can be found on [fileformat.info](http://www.fileformat.info/info/unicode/category/index.htm).

    If **Remove All Punctuation** is selected, three additional sub-options are available:

    1.  **Keep Hyphens**: Selecting this option will change all variations of Unicode hyphens to a single type of hyphen ("-") and this will be left in the text. Hyphenated words (e.g., “computer-aided”) will be subsequently treated as a single token. Further discussion of the limitations can be found [here](link to scrubbing-topic/keep-hyphen).
    2.  **Keep Word-Internal Apostrophes**: If this option is selected, apostrophes will be retained in contractions (e.g., _can’t_) and possessives (_Scott’s_), but not those in plural possessives (_students’_ becomes the term _students_) nor those that appear at the start of a token (_'bout_ becomes the term _bout_). Further discussion of the limitations can be found [here](link to scrubbing-topic/keep-word-internal-apostrophes).
    3.  **Keep Ampersands**: This option will not treat ampersands as punctuation marks and will retain them in the text. Note that HTML, XML, and SGML entities such as `&aelig;` (_æ_) are handled separately and prior to the **Keep Ampersands** option. You can choose how to convert these entities to standard Unicode characters using the **Special Characters** option.
    4.  **Make Lowercase**: Converts all uppercase characters to lowercase characters so that the tokens _The_ and _the_ will be considered as the same term. In addition, all contents (whether in uploaded files or entered manually) for the **Stop Words/Keep Words**, **Lemmas**, **Consolidations**, or **Special Characters** options will also have all uppercase characters changed to lowercase. Lowercase is not applied inside any HTML, XML, or SGML markup tags remaining in the text.
    5.  **Remove Digits**: Removes all number characters from the text. Similar to the handling of punctuation marks, any Unicode character in each of the active texts with a “Number Character Property” is removed. For example, this option will remove a Chinese three (㈢) and Eastern Arabic six (۶) from the text. Note: at present, Lexos does not match Real numbers as a unit. For example, for _3.14_, Lexos will remove (only) the 3, 1, and 4 and the decimal point will be removed only if the **Remove All Punctuation** option is selected. **Remove Digits** is not applied inside any HTML, XML, or SGML markup tags remaining in the text.
    6.  **Remove Whitespace**: Removes all whitespace characters (blank spaces, tabs, and line breaks), except in HTML, XML, and SGML markup tags. Removing whitespace characters may be useful when you are working with non-Western languages such as Chinese that do not use whitespace for word boundaries. In addition, this option may be desired when tokenizing by character n-grams if you do not want spaces to be part of your n-grams. See the section on [Tokenization](link%20to%20tokenize%20page) for further discussion on tokenizing by character n-grams. If **Remove Whitespace** is selected the following sub-options are available to allow you to fine-tune the handling of whitespace:
        1.  **Remove Spaces**: each _blank-space_ will be removed.
        2.  **Remove Tabs**: each tab character ( `\t` ) will be removed.
        3.  **Remove Line Break**: each newline character ( `\n` ) and carriage return character ( `\r` ) will be removed.
    7.  **Scrub Tags**: Handles markup tags in angular brackets, such as those used in XML, HTML, and SGML. In markup languages like these, start and end tags like `<p>...</p>` are used to designate an “element”. Elements may be modified by “attributes” specified inside the start tag. For instance, a text using the the [Text Encoding Initiative (TEI)](http://www.tei-c.org/index.xml) specification for XML might contain the markup `<p rend="italic">...</p>` for a paragraph in italics. When this option is selected, a gear icon will appear. Click the icon to open the tag scrubbing dialog. This will allow you to choose one of four options to handle each type of tag or to handle all the tags at once:
        1.  **Remove Tag Only (default)**: Removes the start and end tags but keeps the content in between. For instance, `<p>Some text</p>` will be replaced by `Some text` .
        2.  **Remove Element and All Its Contents**: Removes the start and end tags and all the content in between. For instance, `<p>Some text</p>` will be removed entirely.
        3.  **Replace Element’s Contents with Attribute Value**: Replaces the element with the value of one of its attributes. Since elements may have multiple attributes, Lexos allows you to enter the name of the attribute you wish to use. For instance, if you have some markup like `<stage type="setting"> Scene <view>Morning-room in Algernon's flat in Half-Moon Street.</view></stage>` , you could use this option to replace the entire scene description with `setting` if you entered `type` as the attribute name.
        4.  **Leave Tag Alone**: This option will leave the specified element untouched in the text. This is especially useful if you want to scrub only certain markup tags.
        
        **Troubleshooting**: Lexos compiles a list of the tags in your documents by first attempting to parse the documents as XML. If the markup is not well-formed XML, it next tries to parse the documents as HTML using Python's BeautifulSoup library. This will generally work with the proviso that BeautifulSoup automatically converts all tags to lowercase. As a result, the Lexos scrubbing function will miss HTML (and SGML) tags contain uppercase letters. In this case, you may have to check each of the tags Lexos finds to make sure it does not have uppercase letters in your original document. If you find that Lexos is not scrubbing tags containing capital letters, you will have to change these in an editor before uploading the files. This issue does not affect valid XML files since XML parsers are case sensitive. If Lexos is unable to compile an accurate list of the tags in your XML file, we recommend testing the file with an [XML Validator](http://www.w3schools.com/xml/xml_validator.asp).

    #### Additional Options

    1.  **Stop Words/Keep Words**: “Stop Words” represents a list of words or terms to _remove_ from your documents, and “Keep Words” represents a list of words or terms that should remain in your documents with all other words removed. In both cases, words must be entered as comma-separated or line-separated lists like the following:

            a, some, that, the, which
            a
            some
            that
            the
            which

        You may enter these lists manually in the provided form area or upload a file (e.g. `stopWords.txt` ). Note that the <b>Make Lowercase</b> option will be applied to your list of stop/keep words if that option is also selected.
    2.  **Lemmas**: Replaces a list of tokens with a common replacement term called a “lemma”. Lemmas might be conceived of as dictionary headwords. Using the lemmas option will allow you to count a lemma and all of its variants (such grammatically inflected forms) as a single term. For instance, in Old English, the word for “king”, _cyning_ may occur as _cyninges_ (possessive) or _cyningas_ (plural), amongst other variants. If each of these forms occurs one time in a text, the **Lemmas** function will instruct Lexos to treat this as three occurrences of the term _cyning_. Lemmas are specified by providing a comma-separated list of variants followed by a colon and then the lemma. Multiple lemmas can be specified in separate lines as shown below:

            cyninges, cyningas: cyning
            Beowulfes, Beowulfe: Beowulf

        The list may be entered manually in the form provided or uploaded from a file. Note that the **Make Lowercase** option will be applied to your list of tokens and lemmas if that option is also selected. To replace individual characters with other characters, you should use the **Consolidation** option.
    3.  **Consolidations**: Replaces a list of characters with a different character. This is typically to consolidate symbols considered equivalent. For instance, in Old English the character common character “eth” _ð_ is interchangeable with the character “thorn” _þ_. The **Consolidations** option allows you to choose to merge the two using a single character. Consolidations should be entered in the format `ð: þ` , where you wish to change all occurrences of `ð` to `þ` . Multiple consolidations can be separated by commas or line breaks. Consolidations can be entered manually in the provided form field or uploaded from a file. Note that the **Make Lowercase** option will be applied to your list of characters if that option is also selected. To replace entire words (terms) with other words, you should use the **Lemma** option.
    4.  **Special Characters**: Replaces character entities with their glyph equivalents. A [character entity](https://en.wikipedia.org/wiki/List_of_XML_and_HTML_character_entity_references) is a symbolic representation for an actual character symbol (glyph). Entities are used by markup languages like HTML, XML, and SGML when the symbol itself cannot be entered in the editor used to produce the text or when the method of rendering the character is left to independent software like a web browser. For instance, in HTML, the Old English character “aesc” (_æ_) is represented with the entity `&aelig;` . Since Lexos works entirely with Unicode characters you will most likely want to replace character entities with their Unicode equivalents prior to further analysis. The **Special Characters** option can be used to replace entities like `&aelig;` with its corresponding Unicode glyph _æ_. Lexos provides four rule sets of pre-defined entities and their corresponding glyphs:
        1.  **Early English HTML**: Transforms a variety of HTML entities used to encode Old English, Middle English, and Early Modern English into their corresponding glyphs.
        2.  **Dictionary of Old English SGML**: Transforms SGML entities used by the _Dictionary of Old English_ into their corresponding glyphs.
        3.  **MUFI 3**: Transforms entities specified in version 3.0 of the Medieval Unicode Font Initiative (MUFI 3) to their corresponding glyphs.
        4.  **MUFI 4**: Transforms entities specified in version 4.0 of the Medieval Unicode Font Initiative (MUFI 4) to their corresponding glyphs.

        Note: Selecting MUFI 3 or MUFI 4 will convert entities specified by the Medieval Unicode Font Initiative (MUFI) to their Unicode equivalents. In this case, the Preview window will be changed to use the [Junicode](http://junicode.sourceforge.net/) font, which correctly displays most MUFI characters. However, if you downloaded your files after scrubbing, these characters may not display correctly on your computer if you do not have a MUFI-compatible font installed. Information about MUFI and other MUFI-compatible fonts can be found on the [MUFI website](http://folk.uib.no/hnooh/mufi/).

        Note: Any special characters that appear inside tags _will_ be modified.

        You may also design your own rule set if you are not using a language covered by one of the pre-defined rule sets. To do this, enter your transformation rules in the provided form field. The entity should be separated from its replacement glyph by a comma (e.g. `&aelig;, æ` ). Multiple transformation rules should be listed on separate lines. The Lexomics Project welcomes submission of the new rule sets. Please use the **Feedback and Support** button in Lexos or [click here](https://urldefense.proofpoint.com/v2/url?u=https-3A__docs.google.com_a_wheatoncollege.edu_forms_d_e_1FAIpQLSddEsRE2PcserYwcjtNpBAMF-2DYRKVrL4H4LtWDxHeNKoVVxcA_viewform&d=CwMCaQ&c=Oo8bPJf7k7r_cPTz1JF7vEiFxvFRfQtp-j14fFwh71U&r=fkkkcAta9tNbJT0GbA-b8fBT5Vx0day25Z1KcBOKxKQ&m=pvw58nUgCb4t3z5cj9Zj2XFIXgBppHEM8aQoOb5vqpA&s=ZxoSL8vQIBP526hKabavc3SaECtb_M8nMnjGHo6MiSk&e=)[](http://junicode.sourceforge.net/) to contact us about a adding pre-defined rule set to Lexos.

### The Lexos Scrubber Algorithm

Lexos scrubs documents by applying rules in the following order:

#### <u>When the **Preview Scrubbing** button is clicked</u>

Markup tags in angular brackets are not affected by the rules below except rule 4. The actual text is not permanently modified at this point, but of course the Preview window shows a sample of what will be changed if you select **Apply Scrubbing**.

1.  Remove Project Gutenberg boilerplate, if present
2.  Convert stopwords, keepwords, lemmas, consolidations, and special characters to lowercase (the actual text is converted to lowercase later, see step #5 below).
3.  Apply special character transformations.
4.  Apply markup tag scrubbing rules.
5.  Convert text to lowercase.
6.  Apply consolidation rules.
7.  Apply lemmatization rules.
8.  Apply stopword/keepword lists.
9.  Remove punctuation (hyphens, apostrophes, ampersands).
10.  Remove digits.
11.  Remove whitespace.

#### <u>When the **Apply Scrubbing** button is clicked</u>

Markup tags in angular brackets are not affected by the rules below except rule 4.

1.  Remove Project Gutenberg boilerplate, if present
2.  Convert stopwords, keepwords, lemmas, consolidations, and special characters to lowercase (the actual text is converted to lowercase later, see step #5 below).
3.  Apply special character transformations.
4.  Apply markup tag scrubbing rules.
5.  Convert text to lowercase.
6.  Apply consolidation rules.
7.  Apply lemmatization rules.
8.  Apply stopword/keepword lists.
9.  Remove punctuation (hyphens, apostrophes, ampersands).
10.  Remove digits.
11.  Remove whitespace.
