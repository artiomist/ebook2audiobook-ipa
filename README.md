# ebook2audiobook-ipa
ipa for ebook2audiobook fix for russian word stress

There is a great tool https://github.com/DrewThomasson/ebook2audiobook made by Drew Thomasson to convert an e-book to audiobook. For russian language there is a bug with word stresses: https://github.com/DrewThomasson/ebook2audiobook/discussions/597

This script is a workaround that uses IPA transcriptor and xtts-ru-ipa model.

- after a few testes, it seems that tha _intonation_ is a bit better with the original model, and _word stresses_ are better with ipa model
- tested on wndows
- assuming the user path is C:\Users\admin\
- on my pc GPU option (step 5) is twice as fast as CPU (~20000sec GPU, 54000sec CPU)

1. <pre>pip install git+https://github.com/omogr/omogre.git
<div class="zeroclipboard-container position-absolute right-0 top-0">
    <clipboard-copy aria-label="Copy" class="ClipboardButton btn js-clipboard-copy m-2 p-0" data-copy-feedback="Copied!" data-tooltip-direction="w" value="git checkout v25
git pull" tabindex="0" role="button" style="display: inherit;">
      <svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon m-2">
    <path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path>
</svg>
      <svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-check js-clipboard-check-icon color-fg-success d-none m-2">
    <path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"></path>
</svg>
    </clipboard-copy>
  </div>
  </pre>

This will install Omogre, Russian accentuator and IPA transcriptor. https://github.com/omogr/omogre

2. Download russian ipa files from https://huggingface.co/omogr/xtts-ru-ipa/tree/main
 and zip to "xtts-ru-ipa.zip". This is an IPA model that uses this corpus https://ruslan-corpus.github.io/

3. convert audiobook from anyformat to epub
   <pre>C:\Users\admin\scoop\shims\ebook-convert.EXE C:\Users\admin\Downloads\XXX.fb2 C:\Users\admin\Downloads\XXX.epub</pre>

4. 
	<pre>pip install ebooklib bs4 num2words</pre>
	#run once, needed for transcribe_epub_book_file.py
	<pre>python "C:\Users\admin\Downloads\transcribe_epub_book_file.py" "C:\Users\admin\Downloads\Downloads\XXX.epub"</pre>
	- this will make "C:\Users\admin\Downloads\XXX_processed.epub" file
	- transcribes russian for xtts_ru_ipa model using IPA installed in step 1, processes only index_split_XXX.xhtml files
 	- keeps english intact
  	- converts numbers to words prior to transcribing
   	- should ignore html (keep intact)
	
5. run with GPU, go to step 6 if you use CPU
- Use https://github.com/DrewThomasson/ebook2audiobook code
<pre>docker run --pull always --rm --gpus all -p 7860:7860 athomasson2/ebook2audiobook </pre>
- load xtts-ru-ipa.zip into custom model zip (it must be a zip without folder inside but 4 files: ref.wav, model.pth, config.json, vocab.json).
	
6. run with CPU, go to step 5 if you use GPU
-run ebook2audiobook/ebook2audiobook.cmd
- load xtts-ru-ipa.zip into custom model zip (it must be a zip without folder inside but 4 files: ref.wav, model.pth, config.json, vocab.json).

7. - open http://localhost:7860/
- select C:\Users\admin\Downloads\XXX_processed.epub
- select russian language
- optional: change clone voice to Morgan Freeman, I like the voice
- load custom model zip: xtts-ru-ipa
- process audiobook
	
	
