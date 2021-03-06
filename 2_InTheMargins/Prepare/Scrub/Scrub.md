# Scrub

* [Overview](#overview)
* [Scrubbing Options](#features)
* [Additional Options](#addition)
* [Issues/Questions](#issues)

## <a name='overview'></a> Overview
On this page you can modify your active text files by selecting options to remove or alter different aspects of the text.


## <a name='features'></a> Scrubbing Options

### Project Gutenberg
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   Upon entering the scrub page if you have uploaded a file from the Project Gutenberg website without removing the boiler plates (text added by the Project Gutenberg site) you will receive a warning. If you choose to continue without removing this extra text on your own the text that is a part of every Project Gutenberg file will be removed, but there are inconsistencies from file to file because of additional text added by the contributors. For this reason we suggest you edit the file yourself to prevent extra unwanted text from being included in your word counts and other tests as you continue working with Lexos.
3. __Example:__  
   
4. __Issue/Questions:__  
   
### Preview Scrubbing
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   This button will allow you to see the changes you will be making to the text before the file is saved with the changes. If you have a Project Gutenberg file it will still show the boiler plates in the preview.
3. __Example:__  
   
4. __Issue/Questions:__  
   
### Apply Scrubbing
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   This button will save the changes you've selected to the active files. If you have a Project Gutenberg file the standard boiler plates will be removed at this point.
3. __Example:__  
   
4. __Issue/Questions:__  
   
### Download Scrubbed Files
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   This button allows you to download the files you have scrubbed to your computer.
3. __Example:__  
   
4. __Issue/Questions:__  
   
   
### Remove All Punctuation
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   This option will use a map containing all unicode punctuation characters to remove any character classified as punctuation from the selected files. If remove tags is not selected "<" and ">" will be removed as punctuation.
3. __Example:__  
   
4. __Issue/Questions:__  
   
#### Keep Hyphens:  
   1. __Tool Tip:__  
      none
   2. __Tool Tip Extended:__  
      Selecting this option within the remove punctuation menu will change all variatons of hyphens to a single type of hyphen and remove the one type of hyphen from the map of punctuation to be removed therefore keeping hyphens.
   3. __Example:__  
   
   4. __Issue/Questions:__  
   
#### Keep Word-Internal Apostrophes
   1. __Tool Tip:__  
      Retain apostrophes in contractions and possessives, but not those in plural possessives nor at the start of a word.
   2. __Tool Tip Extended:__  
   3. __Example:__  
   
   4. __Issue/Questions:__  
   
#### Keep Ampersands
   1. __Tool Tip:__  
      Leave all ampersands in the text. Note that HTML or XML entities such as <code>&amp;ae;</code> (ash) are handled separately. You can convert these entities to standard Unicode characters using the Special Characters function below.
   2. __Tool Tip Extended:__  
      
   3. __Example:__  
   
   4. __Issue/Questions:__  
   
   
### Make Lowercase
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   Selecting this option will change all uppercase characters in the active files into lowercase characters. In addition any files uploaded for Stop Words/Keep Words, Lemmas, Consolidations, or Special characters will also have all uppercase characters changed to lowercase. However if any of the previous options were manually entered they should be written in lowercase as they will not be changed.
3. __Example:__  
   
4. __Issue/Questions:__  
   

### Remove Digits
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   This option will use a map of all unicode characters classified as numbers to remove all digits from the selected documents.
3. __Example:__  
   
4. __Issue/Questions:__  
   

### Remove White Space
1. __Tool Tip:__  
   Remove whitespace characters. This may be useful in languages such as Chinese and/or desired when tokenizing with character n-grams.
2. __Tool Tip Extended:__  
   Selecting this option will remove all white spaces (space, tab, new line). Selecting this option automatically selects all sub options. If all the sub options are unchecked this button will do nothing.
3. __Example:__  
   
4. __Issue/Questions:__  
   
#### Remove Spaces:  
   1. __Tool Tip:__  
      none
   2. __Tool Tip Extended:__  
      While this option is selected all single spaces are removed from the text. This can only be selected if Remove White Space is selected.
   3. __Example:__  
   
   4. __Issue/Questions:__  
   
#### Remove Tabs
   1. __Tool Tip:__  
      none
   2. __Tool Tip Extended:__  
      While this option is selected all tabs (\t) are removed from the active documents.
   3. __Example:__  
   
   4. __Issue/Questions:__  
   
#### Remove New Lines
   1. __Tool Tip:__  
      none
   2. __Tool Tip Extended:__  
      While this option is selected all new line characters (\n) are removed. This will make the text one long line.
   3. __Example:__  
   
   4. __Issue/Questions:__  
   
### Scrub Tags
1. __Tool Tip:__  
   Handle tags such as those used in XML, HTML, or SGML. When this option is selected, a gear appears which will allow you to choose different options to handle each tag.
2. __Tool Tip Extended:__  
   
3. __Example:__  
   
4. __Issue/Questions:__  
   If this is selected and there are options selected in XML or DOE do those override this?  
   
#### Tag Options
   1. __Tool Tip:__  
      none
   2. __Tool Tip Extended:__  
      When you select this option a pop-up box with a list of all of the types of tags (Elements) is displayed with four different actions to be applied. The default option is Remove Tag Only. Other options:  Remove Element and All Its Contents, Replace Element's Contents with Attribute Value, Leave Tag Alone
   3. __Example:__  
   
   4. __Issue/Questions:__  
  

## <a name='addition'></a> Additional Options

### Stop Words/Keep Words
1. __Tool Tip:__  
    Upload or input a list of Stop Words (words to be removed) or Keep Words (words to keep).  
   * List format: a list of words separated by commas on one or more lines.
2. __Tool Tip Extended:__  
   By default this tool is off, but has the functionality to either select specific words to keep (keep words) or to remove (stop words). Stop words will remove all instances of the tokens listed, but will not remove that word within another word. Keep words will remove all tokens except for instances of the words listed. Either a file can be uploaded with these tokens or they can be manually entered in the box separated by commas.
3. __Example:__  
   * Stop Words: your stop word is "cat", your text is "The cat catches the caterpillar on the catwalk.", the text after scrubbing is "The catches the caterpillar on the catwalk."  
   * Keep Words: your keep words are "ball, cat", your text is "The cat chased the ball across the street, but got distracted by the balloon.", the text after scrubbing is "cat ball"
   
4. __Issue/Questions:__  
   * I don't believe this works with removed white space. Should this be mentioned and is it an issue?
  
   
### Lemmas
1. __Tool Tip:__  
   * Input a list of lemmas (word replacements).  
   * Lemma list format: one set of replacement words per line (each separated by commas) followed by a colon(:) then the lemma (e.g. *cyng,kyng:king* will replace every *cyng* and *kyng* in the document with *king*).
2. __Tool Tip Extended:__  
   Using this tool will replace a token or tokens with a different token (lemma). This can be used to replace words that have variations in spelling throughout the text with one spelling of the word.
3. __Example:__  
   Lemma: cyng,kyng:king  
   Text: The kyng ruled the cyngdom.  
   Scrubbed text: The king ruled the kingdom.  
4. __Issue/Questions:__  

   

   
### Consolidations
1. __Tool Tip:__  
   Input a list of consolidations (character replacements).  
   Consolidation list format: one set of replacement characters per line (each separated by commas) followed by a colon(:) then the replacement character (e.g. *a,b:c* will replace every *a* and *b* in the document with *c*).
2. __Tool Tip Extended:__  
   Selecting this tool allows you to replace any single character or characters with a different single character
3. __Example:__  
   Consolidation: a:o, Text: The cat sat on the rat., Scrubbed text: The cot sot on the rot.
4. __Issue/Questions:__  
   Like lemmas this is what it looks like to me, but not completely sure.
   
### Special Characters
1. __Tool Tip:__  
   * Select a pre-defined Rule Set or input a list of rules for handling character entities.  
   * Special Character list format: one set of replacement words or characters per line (each separated by commas) followed by a colon(:) then the replacement word or character (e.g. *æ,ae:æ* will replace *æ* and *ae* with *æ*).
2. __Tool Tip Extended:__  
   * Early English HTML: Transforms Early English HTML entities into their corresponding glyphs.
   * Dictionary of Old English SGML: Transforms DOE entities into their corresponding glyphs.
   * MUFI 3: Transforms the MUFI 3 entities into the MUFI 3 glyph (Junicode font required).
   * MUFI 4: Transforms the MUFI 4 entities into the MUFI 4 glyph (Junicode font required).
3. __Example:__  
   
4. __Issue/Questions:__  
   I don't know how to explain this better than it is in the tool tip.
   
## <a name='issues'></a> General Issues/Questions
I'm not sure where this should go, but there needs to be some mention of texts containing SGML/HTML/XML entities. Lexos does not recognise these entities automatically and will treat ampersands and semi-colons as punctuation. Users who think their texts might contain entities should use the Special Characters function to ensure that entities are converted to their Unicode equivalents.

