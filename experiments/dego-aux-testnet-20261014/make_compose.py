import json
from pathlib import Path
root=Path(__file__).resolve().parent
services={}
for n in range(1,4):
 cmd=['/research/build/src/DeroGoldd','--no-console','--allow-local-ip','--data-dir','/data','--log-file','/data/daemon.log','--log-level','3','--p2p-bind-ip','0.0.0.0','--p2p-bind-port',str(43070+n),'--rpc-bind-ip','0.0.0.0','--rpc-bind-port',str(43170+n)]
 for peer in range(1,4):
  if peer!=n:cmd+=['--add-exclusive-node',f'172.30.247.{10+peer}:{43070+peer}']
 services[f'node{n}']={'image':'dego-research-build:20261014','container_name':f'dego-aux-testnet-node{n}','command':cmd,'volumes':['.:/research:ro',f'./data/node{n}:/data'],'ports':[f'127.0.0.1:{43170+n}:{43170+n}'],'networks':{'lab':{'ipv4_address':f'172.30.247.{10+n}'}},'cpus':1,'mem_limit':'2g','restart':'no','stop_grace_period':'30s'}
d={'name':'dego-aux-testnet','services':services,'networks':{'lab':{'name':'dego-aux-testnet-lab','internal':True,'ipam':{'config':[{'subnet':'172.30.247.0/24'}]}}}}
(root/'compose.json').write_text(json.dumps(d,indent=2)+'\n')
