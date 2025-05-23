# ebook2audiobook-ipa
ipa for ebook2audiobook fix for russian word stress

There is a great tool https://github.com/DrewThomasson/ebook2audiobook made by Drew Thomasson to convert an e-book to audiobook. For russian language there is a bug with word stresses: https://github.com/DrewThomasson/ebook2audiobook/discussions/597

This script is a workaround that uses IPA transcriptor and xtts-ru-ipa model.

- after a few testes, it seems that tha _intonation_ is a bit better with the original model, and _word stresses_ are better with ipa model
- tested on wndows
- assuming the user path is C:\Users\admin\
- on my pc GPU option (step 5) is twice as fast as CPU (~20000sec GPU, 54000sec CPU)

1. pip install git+https://github.com/omogr/omogre.git

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
	
	
