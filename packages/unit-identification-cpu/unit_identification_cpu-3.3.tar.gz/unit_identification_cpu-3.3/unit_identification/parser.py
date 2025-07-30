import re
def preprocess(_,text):
	text_procesed = text
	text_procesed = text_procesed.lower() 
	text_procesed = re.sub(r'\n', '', text_procesed) 
	text_procesed = text_procesed.replace('.','').replace("-","")
	text_procesed = re.sub(r'[,:;{}?!/_\$@<>()\\#%+=\[\]\']','', text_procesed)
	text_procesed = re.sub(r'[^a-z0-9]', '', text_procesed)
	text_procesed = ' '.join([t for t in text_procesed.split()])
	return text 
def parse(text):	
	return []