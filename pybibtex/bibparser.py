import re
import codecs

def ParseBib(filenames):
  database = {}
  for fn in filenames:
    content = GetFilteredContent(fn)

    for match in re.finditer(r"@([a-zA-Z]+)\{([^,\s]+)\s*,(.*?[\}\"]),?\s*\}\s*(?=@|$)", content, re.DOTALL):
      key = match.group(2)
      database[key] = entry = DefaultDict()
      entry["type"] = match.group(1).lower()

      raw = match.group(3)+","
      for match in re.finditer(r"\s*([a-zA-Z]+)\s*=\s*[\{\"](.*?)[\}\"]\s*,", raw, re.DOTALL):
        key = match.group(1)
        value = match.group(2)
        entry[key] = value

      PostProcessing(entry)
      database[key] = entry
  return database

class DefaultDict(dict):
  def __getitem__(self, key):
    if not key in self:
      return "MISSING"
    else:
      return dict.__getitem__(self, key)

def GetFilteredContent(fileName):
  content = []
  with codecs.open(fileName) as f:
    for line in f:
      if line and line[0] != "%":
        content.append(line)
  return "".join(content)

def PostProcessing(entry):
  for key in entry:
    if key == "type": continue
    value = entry[key]
    value = re.sub("[ \t\n]+", " ", value)
    if len(value) > 2 and value[0] == '{' and value[-1] == '}':
      value = value[1:-1] # no other processing
    else:
      if key == "author":
        value = ParseAuthor(value)
    entry[key] = value

def ParseAuthor(s):
  authors = []
  for ra in s.split(" and "):
    first, last = ParseAuthorName(ra)
    if first is None:
      word = last
    elif first[-1] == ".":
      word = first+" "+last
    else:
      word = first[0]+". "+last
    authors.append(word)
  return authors

def ParseAuthorName(s):
  s = s.strip()
  words = []
  n = len(s)
  i = 0
  braceLvl = 0
  currentWord = ""
  while i < n:
    char = s[i]

    if char == "{" and s[i-1] != "\\":
      braceLvl += 1
    elif char == "}" and s[i-1] != "\\":
      braceLvl -= 1

    if braceLvl == 0:
      if char == " ":
        if currentWord:
          words.append(currentWord)
        currentWord = ""
        i+=1
        continue

    currentWord += char
    i+=1
  if currentWord:
    words.append(currentWord)

  n = len(words)
  iComma = None
  for i in xrange(n):
    if words[i][-1] == ",":
      iComma = i
      words[i] = words[i][:-1]

    if words[i][0] == "{" and words[i][-1] == "}":
      words[i] = words[i][1:-1]

  if iComma is not None:
    last = " ".join(words[:iComma+1])
    first = " ".join(words[iComma+1:])
  else:
    if len(words) != 2:
      return None, " ".join(words)

    first = words[0]
    last = words[1]

  return first, last
