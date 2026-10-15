import runpy,pathlib,json
p=pathlib.Path(__file__).resolve().parent
g=runpy.run_path(str(p/'test_pow.py'));powhash=g['powhash'];libs=g['libs']
known=bytes.fromhex('0100fb8e8ac805899323371bb790db19218afd8db8e3755d8b90f39b3d5506a9abce4fa912244500000000ee8146d49fa93ee724deb57d12cbc6c6f3b924d946127c7a97418f9348828f0f02')
expected='38591572f820d4de253cf55a2192b622b0289e2e5c3616e61e787a8fe462ec5a'
rows=[]
for coin in libs:
 h=powhash(coin,known);rows.append({'coin':coin,'type':'published WRKZ CN_UPX known answer','pass':h==expected,'hash':h});assert h==expected,(coin,h)
for f in json.loads((p/'structure-results.json').read_text())['work_fixtures']:
 b=bytes.fromhex(f['blob']);hashes={coin:powhash(coin,b) for coin in libs}
 rows.append({'type':'modeled carrier work','transactions':f['transactions'],'pass':len(set(hashes.values()))==1,'hashes':hashes});assert rows[-1]['pass']
(p/'cross-work-results.json').write_text(json.dumps(rows,indent=2));print('PASS cross-work/known-answer',len(rows))
