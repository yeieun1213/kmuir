with KLT2000
  > kma.exe ../../ko_wiki_text_EUCKR.txt ../../kmaoutput.txt
with Komoran at files

with iconv to change encoding language from cp949 to utf-8
  > iconv -c -f cp949 -t utf-8 < kmaoutput.txt > kmaoutput_utf8.txt
