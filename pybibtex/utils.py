import re,os

def Uniquify(seq): # Dave Kirby
  # Order preserving
  seen = set()
  return [x for x in seq if x not in seen and not seen.add(x)]

def GetCites(fileName):
  cites = [ x.split(",") for x in re.findall(r"\\citation(?:\[.+\])?\{(.*?)\}",file(fileName).read()) ]
  return [ x.strip() for x in Uniquify(sum(cites,[])) ] # flatten list, remove duplicates while preserving order

def GetBibOptions(fileName):
  txt = file(fileName).read()

  dbBases = []
  for x in re.findall(r"\\bibdata\{(.*?)\}",txt):
    if x is None: continue
    if "," in x:
      dbBases += x.split(",")
    else:
      dbBases.append(x)

  databases = []
  for d in dbBases:
    if "." not in d: d += ".bib"
    for dbPath in ["."] + os.path.expandvars("$BIBINPUTS").split(":"):
      dd = os.path.join(dbPath,d)
      if os.path.exists(dd):
        databases.append(dd)
        break
    else:
      print "Warning: database %s not found" % d

  styleFile = None
  s = re.search(r"\\bibstyle\{(.*?)\}",txt)
  if s:
    s = s.group(1)
    if not s.endswith(".py"):
      s += ".py"
    if os.path.exists(s):
      styleFile = s
    else:
      raise SystemExit("bibstyle %s not found" % s)

  return databases, styleFile
