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
 and zip to "xtts-ru-ipa.zip"

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
- load xtts-ru-ipa.zip into custom model zip
- Then there is a strange bug. My workaround was to delete the zip and reload it, maybe multiple times, till you get an error:
"Loading TTS xtts model, it takes a while, please be patient...
load_coqui_tts_checkpoint() error: [Errno 2] No such file or directory: '/app/models/__sessions/model-64efd217-6c2b-4a39-b850-5d4c4a68bb12/xtts/xtts-ru-ipa/config.json'
convert_chapters_to_audio() failed!"

then manually add files to docker image in terminal 
<pre>docker cp C:\Users\admin\Downloads\xtts-ru-ipa\vocab.json interesting_hypatia:/app/models/__sessions/model-64efd217-6c2b-4a39-b850-5d4c4a68bb12/xtts/xtts-ru-ipa</br>
docker cp C:\Users\admin\Downloads\xtts-ru-ipa\model.pth interesting_hypatia:/app/models/__sessions/model-64efd217-6c2b-4a39-b850-5d4c4a68bb12/xtts/xtts-ru-ipa</br>
docker cp C:\Users\admin\Downloads\xtts-ru-ipa\ref.wav  interesting_hypatia:/app/models/__sessions/model-64efd217-6c2b-4a39-b850-5d4c4a68bb12/xtts/xtts-ru-ipa</br>
docker cp C:\Users\admin\Downloads\xtts-ru-ipa\config.json  interesting_hypatia:/app/models/__sessions/model-64efd217-6c2b-4a39-b850-5d4c4a68bb12/xtts/xtts-ru-ipa</pre>
	
6. run with CPU, go to step 5 if you use GPU
-run ebook2audiobook/ebook2audiobook.cmd
- load xtts-ru-ipa.zip into custom model zip
- Then there is a strange bug. My workaround was to delete the zip and reload it, maybe multiple times, till you get an error:
"Loading TTS xtts model, it takes a while, please be patient...
load_coqui_tts_checkpoint() error: [Errno 2] No such file or directory: 'C:\Users\admin\ebook2audiobook\models\__sessions\model-64efd217-6c2b-4a39-b850-5d4c4a68bb12\xtts\xtts-ru-ipa'
convert_chapters_to_audio() failed!"
- then manually copy files to "C:\Users\admin\ebook2audiobook\models\__sessions\model-64efd217-6c2b-4a39-b850-5d4c4a68bb12\xtts\xtts-ru-ipa"


7. - open http://localhost:7860/
- select C:\Users\admin\Downloads\XXX_processed.epub
- select russian language
- optional: change clone voice to Morgan Freeman, I like the voice
- load custom model zip: xtts-ru-ipa
- process audiobook
	
	
