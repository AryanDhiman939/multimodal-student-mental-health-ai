QUESTIONS=[
{"key":"stress","question":"I have felt stressed or under pressure."},
{"key":"sleep","question":"I have had difficulty sleeping or keeping a regular sleep routine."},
{"key":"focus","question":"I have found it difficult to concentrate on studies or daily tasks."},
{"key":"energy","question":"I have felt low on energy or unusually tired."},
{"key":"motivation","question":"I have found it difficult to feel motivated."},
{"key":"worry","question":"I have found myself worrying more than usual."},
{"key":"connection","question":"I have felt disconnected from friends, family, or classmates."},
{"key":"enjoyment","question":"I have had less enjoyment in activities I usually like."},
{"key":"overload","question":"My academic or personal workload has felt difficult to manage."},
{"key":"calm","question":"I have found it difficult to relax or switch off."},
{"key":"confidence","question":"I have doubted my ability to handle everyday challenges."},
{"key":"routine","question":"My daily routine, meals, or self-care have been disrupted."}]
def score_answers(a): return round(sum(a.values())/(len(QUESTIONS)*3)*100,1)
def band(s): return "Lower frequency" if s<35 else ("Some signals" if s<65 else "More frequent signals")
