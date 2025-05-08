# ebook2audiobook-ipa
ipa for ebook2audiobook fix for russian word stress

#tested on wndows
#assuming the user is C:\Users\admin\

1. pip install git+https://github.com/omogr/omogre.git
This will install Omogre, Russian accentuator and IPA transcriptor. https://github.com/omogr/omogre?tab=readme-ov-file
#will download C:\Users\admin\omogre_data sidefiles

2. https://huggingface.co/omogr/xtts-ru-ipa/tree/main
download russian ipa files and zip to xtts-ru-ipa.zip

3. convert audiobook from anyformat to epub
   <pre>C:\Users\admin\scoop\shims\ebook-convert.EXE C:\Users\admin\Downloads\XXX.fb2 C:\Users\admin\Downloads\XXX.epub</pre>

5. terminal
	<pre>pip install ebooklib bs4 num2words</pre>
	#run once, needed for transcribe_file_9_book.py
	<pre>python "C:\Users\admin\Downloads\transcribe_file_9_book.py" "C:\Users\admin\Downloads\Downloads\XXX.epub</pre>
	#this will make "C:\Users\admin\Downloads\XXX_processed.epub" file
	#transcribes russian for xtts_ru_ipa model using IPA installed in step 1, keeps english intact, converts numbers to words prior to transcribing, ignores html
	
5 GPU. 20000
docker run --pull always --rm --gpus all -p 7860:7860 athomasson2/ebook2audiobook 
	load xtts-ru-ipa.zip
	delete the zip and reload then you get an error:
Loading TTS xtts model, it takes a while, please be patient...
load_coqui_tts_checkpoint() error: [Errno 2] No such file or directory: '/app/models/__sessions/model-64efd217-6c2b-4a39-b850-5d4c4a68bb12/xtts/xtts-ru-ipa/config.json'
convert_chapters_to_audio() failed!

then in terminal 
docker cp C:\Users\admin\Downloads\xtts-ru-ipa\vocab.json interesting_hypatia:/app/models/__sessions/model-64efd217-6c2b-4a39-b850-5d4c4a68bb12/xtts/xtts-ru-ipa
docker cp C:\Users\admin\Downloads\xtts-ru-ipa\model.pth interesting_hypatia:/app/models/__sessions/model-64efd217-6c2b-4a39-b850-5d4c4a68bb12/xtts/xtts-ru-ipa
docker cp C:\Users\admin\Downloads\xtts-ru-ipa\ref.wav  interesting_hypatia:/app/models/__sessions/model-64efd217-6c2b-4a39-b850-5d4c4a68bb12/xtts/xtts-ru-ipa
docker cp C:\Users\admin\Downloads\xtts-ru-ipa\config.json  interesting_hypatia:/app/models/__sessions/model-64efd217-6c2b-4a39-b850-5d4c4a68bb12/xtts/xtts-ru-ipa
	
5 CPU. 54000sec
#delete docker image first 
ebook2audiobook.cmd
#load xtts-ru-ipa.zip
#Extracted files to C:\Users\admin\ebook2audiobook\models\__sessions\model-64efd217-6c2b-4a39-b850-5d4c4a68bb12\xtts\xtts-ru-ipa
# manually copy files again in to the model


6. http://localhost:7860/
	- select Downloads/XXX_processed.epub
	- select russian language
	- optional: change clone voice to Morgan Freeman
	- load custom model zip: xtts-ru-ipa
	
	
