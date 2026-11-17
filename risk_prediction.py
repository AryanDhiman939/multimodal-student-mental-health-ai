def combine(q,t=None):
 s=float(q) if t is None else .65*float(q)+.35*float(t)
 s=round(max(0,min(100,s)),1)
 return s,("Lower frequency of reported signals" if s<35 else ("Some reported signals" if s<65 else "More frequent reported signals"))
def guidance(label):
 return ["Try to maintain regular sleep, meals and study breaks.","Stay connected with someone you trust."]+(
 ["If these experiences persist or affect daily life, consider speaking with a college counsellor or trusted person."]
 if label!="Lower frequency of reported signals" else ["Continue habits and relationships that support your wellbeing."])
