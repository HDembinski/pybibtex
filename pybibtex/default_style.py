def author(bibentry):
  words = bibentry["author"]
  if len(words) > 2 or (len(words) == 2 and words[1] == "others"):
    return words[0] + " \\textit{et al.}"
  else:
    return ", ".join(words)

def article(bibentry):
  s = author(bibentry)
  s += ", %(journal)s {\\bf %(volume)s}, %(pages)s (%(year)s)" % bibentry
  if "note" in bibentry: s += ", %(note)s" % bibentry
  return s + "."

def misc(bibentry):
  s = []
  if "author" in bibentry:
    s.append(author(bibentry))
  if "title" in bibentry:
    s.append("{\em %(title)s}"%bibentry)
  if "howpublished" in bibentry:
    s.append("%(howpublished)s"%bibentry)
  if "note" in bibentry:
    s.append("%(note)s"%bibentry)
  s = ", ".join(s)
  if "year" in bibentry:
    s += " (%(year)s)" % bibentry
  return s + "."

def electronic(bibentry):
  s = author(bibentry)
  s += ", %(howpublished)s (%(year)s)" % bibentry
  return s + "."

def inproceedings(bibentry):
  s = author(bibentry)
  s += ", %(booktitle)s, %(address)s, (%(year)s)" % bibentry
  if "note" in bibentry: s+= ", %(note)s" % bibentry
  return s + "."

def phdthesis(bibentry):
  return "%(author)s, Ph.D. thesis, %(school)s, %(address)s (%(year)s)." % bibentry

def book(bibentry):
  if "edition" in bibentry:
    return "%(author)s, {\em %(title)s, %(edition)s}, %(publisher)s, %(address)s (%(year)s)." % bibentry
  else:
    return "%(author)s, {\em %(title)s}, %(publisher)s, %(address)s (%(year)s)." % bibentry
