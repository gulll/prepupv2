import json
import cgi
import HTMLParser
import os
from pre_storage import PreLocal

dir_path = os.path.dirname(os.path.realpath(__file__))

def unicodeToHTMLEntities(text):
    """Converts unicode to HTML entities.  For example '&' becomes '&amp;'."""
    text = cgi.escape(text).decode('utf-8').encode('ascii', 'xmlcharrefreplace')
    text = text.replace('\n', '<br/>')
    text = text.replace(' ','&nbsp;')
    return text

def main():
    qn_text = ''
    qn_flag = False
    opt1 = ''
    opt2 = ''
    opt3 = ''
    opt4 = ''
    cnt = 0
    ans = ''
    tags = ''
    expl = ''
    pre_local = PreLocal()
    with open(dir_path+'/../data/raw_questions_java', 'r') as raw_file:
        for line in raw_file:
            #print line
            if line[0]=='Q' and line[1]=='.':
                qn_text = line.split(' ',1)[1]
                qn_flag = True
            elif len(line) >= 4 and line[1]=='(' and line[3] == ')':
            	qn_flag = False
            	if line[2] == 'A':
            		opt1 = line[4:]
            	elif line[2] == 'B':
                	opt2 = line[4:]
            	elif line[2] == 'C':
                	opt3 = line[4:]
            	elif line[2] == 'D':
                	opt4 = line[4:]
            elif len(line) >= 5 and line[1]=='A' and line[2] == 'n' and line[3]=='s' and line[4] == ':':
                ans = line[5]
            elif len(line) >= 6 and line[1]=='T' and line[2] == 'a' and line[3]=='g' and line[4] == 's' and line[5] == ':':
                tags = line.split(':',1)[1].strip()
                # print line
            elif len(line) >= 6 and line[1]=='E' and line[2] == 'x' and line[3]=='p' and line[4] == 'l' and line[5] == ':':
                print line
                expl = line.split(':',1)[1]
            elif qn_flag:
            	qn_text+=line
            else:
                try:
                	#fout.write(unicodeToHTMLEntities(qn_text) +'\t'+unicodeToHTMLEntities(opt1)+'\t'
                	#	+unicodeToHTMLEntities(opt2)+'\t'+unicodeToHTMLEntities(opt3)+'\t'
                	#	+unicodeToHTMLEntities(opt4)+'\t'+unicodeToHTMLEntities(ans)+'\t'
                	#	+unicodeToHTMLEntities(tags))
                	#fout.write('\n')
                        db, cur = pre_local.connect()
                        
                        _sql = """
                                INSERT INTO %s (cat_id, qnType, qn_text, opt1, opt2, opt3, opt4, ans, explanation, tags)
                                VALUES (%d,'%s','%s','%s','%s','%s','%s','%s', '%s', '%s');
                               """ % ('question_mcq',2, 'MCQ', db.escape_string(str(unicodeToHTMLEntities(qn_text))),db.escape_string(str(unicodeToHTMLEntities(opt1))),
                                      db.escape_string(str(unicodeToHTMLEntities(opt2))),db.escape_string(str(unicodeToHTMLEntities(opt3))),
                                      db.escape_string(str(unicodeToHTMLEntities(opt4))),db.escape_string(str(unicodeToHTMLEntities(ans))),
                                      db.escape_string(str(unicodeToHTMLEntities(expl))),db.escape_string(str(unicodeToHTMLEntities(tags))))
                        results = cur.execute(_sql)
                        db.commit()
                        db.close()
                        print results
                except Exception as e:
                	print str(unicodeToHTMLEntities(qn_text))
                	#print opt1
                	#print opt2
                	#print opt3
                	#print opt4
                	#print tags
                        print str(unicodeToHTMLEntities(expl)) 
                	print e
                        _sql = """
                                INSERT INTO %s (cat_id, qnType, qn_text, opt1, opt2, opt3, opt4, ans, explanation, tags)
                                VALUES (%d,'%s','%s','%s','%s','%s','%s','%s', %s, %s);
                               """ % ('question_mcq',2, 'MCQ', db.escape_string(str(unicodeToHTMLEntities(qn_text))),db.escape_string(str(unicodeToHTMLEntities(opt1))),
                                      db.escape_string(str(unicodeToHTMLEntities(opt2))),db.escape_string(str(unicodeToHTMLEntities(opt3))),
                                      db.escape_string(str(unicodeToHTMLEntities(opt4))),db.escape_string(str(unicodeToHTMLEntities(ans))),
                                      db.escape_string(str(unicodeToHTMLEntities(expl))),db.escape_string(str(unicodeToHTMLEntities(tags))))
                        print _sql

if __name__ == '__main__':
    main()
