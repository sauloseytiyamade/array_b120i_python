# Monitoramento de RAID e envio de email para servidores
# Modelo da placa: Dynamic Smart Array B120i RAID
#

# Importação das bibliotecas:
# re (para utilizar expressão regulares na consulta de palavras)
# smtplib para envio de e-mails
import re
import smtplib


# Criação de uma função para comparação de uma comparacao_string
# Retorna TRUE caso existe alguma string que foi passada com parâmetro

def comparacao_string(comparacao,string):
	re.compile(comparacao)
	if (re.search(comparacao,string)):
		return True
	else:
		return False

# Função que envia e-mail
def envia_email(assunto,texto_email):
	smtp = smtplib.SMTP_SSL('mail.xtpo.com.br',465) #servidor smtp
	smtp.login('user@xtpo.com.br','password') #usuário e senha do e-mail
	smtp.ehlo_or_helo_if_needed()
	from_email = 'From: user@xpto.com.br\n' #remetente do email
	to_email = 'To: rotinas@xpto.com.br\n' #destinatario do email
	subject_email = 'Subject: '+assunto+'\n' #assunto
	body_email = texto_email+'\n' #corpo do email
	msg = from_email+to_email+subject_email+body_email
	msg = msg.encode('ascii','ignore').decode('utf-8')
	smtp.sendmail('user@xpto.com.br',['rotinas@xpto.com.br'],msg)
	smtp.quit()

# Abre o arquivo array.txt e armazena ele em uma variavel
# Esta variavel sera o corpo do email
file_mail = open('array.txt','r')
text_body_mail = file_mail.read()
file_mail.close()

# Lê novamente o arquivo array.txt só que desta vez armazena cada linha em um array para que possa ser analisado
file = open('array.txt','r')
text_array = []
for line in file:
	text_array.append(line)

cont_lines_text_array = len(text_array)
cont_while = 0
cont_errors = 0

while cont_while < cont_lines_text_array:
	line_peer_line = (text_array[cont_while])
	date_line = (text_array[0])
	#verifica se existe em alguma linha a palavra pysicaldrive (São os HDS do RAID)
	verify_physicaldrive = comparacao_string('physicaldrive',line_peer_line)
	if verify_physicaldrive:
		physicaldrive = line_peer_line
		#verifica se na mesma linha do physicaldrive exite a palavra OK.
		status_physicaldrive = comparacao_string('OK',physicaldrive)
		if status_physicaldrive:
			# Se existir OK os discos estão funcionando
			print ('Status OK')
		else:
			# Se não exisitir OK algum dos discos está com problema
			print ('Status Error')
			cont_errors += 1
	cont_while += 1

#envia email informando se o raid está com problema ou não
if cont_errors > 0:
	envia_email('HP Raid Error'+' - '+date_line,text_body_mail)
else:
	envia_email('HP Raid OK'+' - '+date_line,text_body_mail)

file.close()
