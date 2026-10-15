import pathlib,subprocess,re
out=pathlib.Path(__file__).resolve().parent
for coin in ['dego','xkr']:
 root=pathlib.Path('/tmp/dego-xkr-research-'+coin);s=root/'src';d=coin=='dego'
 ns,cr,co=('CryptoNote','Crypto','Common') if d else ('cryptonote','crypto','common')
 core='cryptonotecore' if d else 'cryptonote_core'
 cached=core+('/CachedBlock' if d else '/cached_block');tools='common/CryptoNoteTools' if d else core+'/cryptonote_tools';extra='common/TransactionExtra' if d else core+'/transaction_extra';diff='common/CheckDifficulty' if d else core+'/check_difficulty'
 currency=(s/core/('Currency.cpp' if d else 'currency.cpp')).read_text();start=currency.index('    bool Currency::checkProofOfWorkV2');start=currency.index('{',start)+1;end=currency.index('\n    bool Currency::checkProofOfWork(',start);body=currency[start:end].rstrip();body=body[:body.rfind('}')];body=re.sub(r'logger\([^;]+;', '(void)0;',body)
 code=(out/'native.cpp.in').read_text()
 for k,v in {'CACHED':cached+'.h','TOOLS':tools+'.h','EXTRA':extra+'.h','DIFF':diff+'.h','NS':ns,'CRYPTO':cr,'COMMON':co,'VERSION':'7' if d else '5','PROOF':body}.items():code=code.replace('@'+k+'@',v)
 (out/(coin+'-native.cpp')).write_text(code)
 files=[cached,tools,extra,diff]
 files+=['serialization/'+x for x in (['CryptoNoteSerialization','BinaryInputStreamSerializer','BinaryOutputStreamSerializer','SerializationOverloads'] if d else ['binary_input_stream_serializer','binary_output_stream_serializer','serialization_overloads'])]
 if not d:files +=[core+'/cryptonote_serialization']
 files+=['common/'+x for x in (['MemoryInputStream','VectorOutputStream','StringOutputStream','StreamTools','StringTools','StringView','IInputStream','IOutputStream'] if d else ['memory_input_stream','vector_output_stream','string_output_stream','stream_tools','string_tools','string_view','iinput_stream','ioutput_stream'])]
 sources=[str(s/(f+'.cpp')) for f in files if (s/(f+'.cpp')).exists()]
 cmd=['g++','-std=c++17','-DRAPIDJSON_HAS_STDSTRING=1','-I/tmp/dego-xkr-research-xkr/external','-O2','-ffunction-sections','-fdata-sections','-Wl,--gc-sections','-I'+str(s),'-I'+str(s/'platform/posix'),'-I'+str(s/'platform/linux'),'-I'+str(root/'external/nlohmann-json'),'-I/usr/include/nlohmann','-I'+str(root/'include'),'-I'+str(root/'external'),'-I'+str(root/'external/rapidjson/include'),'-I'+str(root/'external/rapidjson'),str(out/(coin+'-native.cpp'))]+sources+['/tmp/dego-xkr-probe/'+coin+'-full.so','-o',str(out/(coin+'-native'))]
 r=subprocess.run(cmd,capture_output=True,text=True);(out/(coin+'-native-build.log')).write_text(r.stdout+r.stderr);print(coin,r.returncode,r.stderr[-3500:],flush=True)

 assert r.returncode==0, coin+" native build failed"
