REM Envia a data para o arquivos txt
date /T > C:\hp\verifyarray\array.txt
REM Acessa o gerenciado do raid e envia
cd "C:\Program Files\hp\hpssacli\bin"
REM Envia a saída do comando para o arquivo txt abaixo da data
hpssacli.exe ctrl all show config >> C:\hp\verifyarray\array.txt
REM Chama o script python
python C:\hp\verifyarray\read_hpacucli_raid.py
