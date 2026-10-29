#!/usr/bin/env python3
"""펫러스뉴스 매일 자동 게재 (GitHub Actions에서 한국 시각 00:05 전후 실행).
규칙: ① _queue/*.md 중 publish_date<=오늘 이고 reviewed: yes + review_note + sources 가 있는 기사만 게재
      ② 검수 표시가 없으면 절대 올리지 않고 실패로 끝낸다(알림)
      ③ 오늘 날짜 기사가 하나도 없으면 실패로 끝낸다(누락 알림)
      ④ 빌드 후 feed.xml 에 오늘 날짜가 들어갔는지 스스로 검사한다
사용: python3 _src/publish.py [--today YYYY-MM-DD] [--root 저장소폴더] [--dry]"""
import os,sys,re,glob,shutil,subprocess,tempfile,datetime
args=sys.argv[1:]
def opt(n,d=None):
    return args[args.index(n)+1] if n in args else d
ROOT=os.path.abspath(opt('--root','.'))
DRY='--dry' in args
now_kst=datetime.datetime.utcnow()+datetime.timedelta(hours=9)
TODAY=opt('--today') or os.environ.get('PN_TODAY') or now_kst.strftime('%Y-%m-%d')
SRC=os.path.join(ROOT,'_src'); QUEUE=os.path.join(ROOT,'_queue'); ARTS=os.path.join(SRC,'articles')
problems=[]; warns=[]; log=[]
def say(m): print(m); log.append(m)
def fm(path):
    t=open(path,encoding='utf-8').read()
    m=re.match(r'---\n(.*?)\n---\n(.*)',t,re.S)
    if not m: return None,None,t
    meta={}; key=None
    for line in m.group(1).split('\n'):
        if re.match(r'^\w+:',line): key,v=line.split(':',1); meta[key.strip()]=v.strip()
        elif key: meta[key]+='\n'+line
    return meta,m.group(1),m.group(2)
def set_field(head,key,val):
    if re.search(r'^%s:.*$'%key,head,re.M): return re.sub(r'^%s:.*$'%key,'%s: %s'%(key,val),head,count=1,flags=re.M)
    return head+'\n%s: %s'%(key,val)
say('오늘(한국) %s · 저장소 %s%s'%(TODAY,ROOT,' · 시험(--dry)' if DRY else ''))
published_now=[]
for fp in sorted(glob.glob(os.path.join(QUEUE,'*.md'))):
    name=os.path.basename(fp); meta,head,body=fm(fp)
    if meta is None: warns.append('%s: 머리말 형식 오류 → 올리지 않음'%name); continue
    pd=meta.get('publish_date','')
    if not re.match(r'^\d{4}-\d{2}-\d{2}$',pd): warns.append('%s: publish_date 없음/형식 오류 → 올리지 않음'%name); continue
    if pd>TODAY: say('대기 %s → %s 게재 예정'%(name,pd)); continue
    ok=(meta.get('reviewed','').lower()=='yes' and len(meta.get('review_note','').strip())>=10 and len(meta.get('sources','').strip())>=10 and meta.get('slug') and meta.get('title') and meta.get('summary') and meta.get('section'))
    if not ok:
        warns.append('%s: 게재일 %s 도래했지만 검수 표시(reviewed: yes·review_note·sources) 또는 필수 항목 부족 → 올리지 않음'%(name,pd)); continue
    head=set_field(head,'date',TODAY); head=set_field(head,'publish','yes')
    out=os.path.join(ARTS,name)
    say('게재 확정 %s (예정 %s, 실제 %s)'%(name,pd,TODAY))
    if not DRY:
        open(out,'w',encoding='utf-8').write('---\n'+head+'\n---\n'+body); os.remove(fp)
    else:
        os.makedirs(tempfile.gettempdir(),exist_ok=True)
        open(out,'w',encoding='utf-8').write('---\n'+head+'\n---\n'+body)  # dry 도 빌드 시험을 위해 쓰되 큐 파일은 둔다
    published_now.append(name)
# 오늘 날짜 기사가 있는지
have_today=[]
for fp in glob.glob(os.path.join(ARTS,'*.md')):
    meta,_,_=fm(fp)
    if meta and meta.get('date')==TODAY and meta.get('publish','').lower()=='yes': have_today.append(os.path.basename(fp))
if not have_today: problems.append('오늘(%s) 날짜 기사가 없음 — 큐(_queue)에 검수 통과 기사가 없거나 게재일이 맞지 않음'%TODAY)
left=len(glob.glob(os.path.join(QUEUE,'*.md')))
say('오늘 기사 %d건 %s · 큐 남은 기사 %d건'%(len(have_today),have_today,left))
if left<2: say('⚠ 큐가 %d건 남음 — 곧 바닥(다음 기사 검수·큐 보충 필요)'%left)
# 빌드
tmp=tempfile.mkdtemp(); work=os.path.join(tmp,'w'); out=os.path.join(tmp,'o'); os.makedirs(work)
for f in ('build.py','site.json'): shutil.copy(os.path.join(SRC,f),work)
shutil.copytree(ARTS,os.path.join(work,'articles'))
r=subprocess.run([sys.executable,'build.py'],cwd=work,capture_output=True,text=True); say('build: '+r.stdout.strip()[-120:])
if r.returncode: problems.append('build.py 실패: '+r.stderr[-300:])
else:
    r=subprocess.run([sys.executable,os.path.join(SRC,'postbuild.py'),work,out],capture_output=True,text=True)
    if r.returncode: problems.append('postbuild 실패: '+r.stderr[-300:])
if not problems or all('오늘' not in p for p in problems):
    pass
# 결과 복사(생성되는 것만, 고정 파일(CNAME·style.css·img)은 건드리지 않음)
if os.path.isdir(out) and not [p for p in problems if '실패' in p]:
    tgt=ROOT if not DRY else os.path.join(tmp,'root_preview')
    os.makedirs(tgt,exist_ok=True)
    n=0
    for base,pats in ((out,('*.html','news/*.html','sitemap.xml','llms.txt')),(work,('feed.xml','robots.txt'))):
        for pat in pats:
            for fp in glob.glob(os.path.join(base,pat)):
                rel=os.path.relpath(fp,base); dst=os.path.join(tgt,rel); os.makedirs(os.path.dirname(dst),exist_ok=True)
                shutil.copyfile(fp,dst); n+=1
    say('복사 %d개 → %s'%(n,'(미리보기) '+tgt if DRY else '저장소 루트'))
    feed=open(os.path.join(tgt,'feed.xml'),encoding='utf-8').read()
    if '<pubDate>%s<'%TODAY not in feed: problems.append('빌드된 feed.xml 에 오늘(%s) pubDate 없음'%TODAY)
    sm=open(os.path.join(tgt,'sitemap.xml'),encoding='utf-8').read()
    for a in have_today:
        meta,_,_=fm(os.path.join(ARTS,a)); u='news/%s.html'%meta['slug']
        if u not in sm: problems.append('sitemap 에 %s 없음'%u)
        if not os.path.exists(os.path.join(tgt,u)): problems.append('%s 페이지 파일 없음'%u)
open(os.path.join(tmp,'_log.txt'),'w',encoding='utf-8').write('\n'.join(log))
sumf=os.environ.get('GITHUB_STEP_SUMMARY')
if sumf:
    with open(sumf,'a',encoding='utf-8') as f:
        f.write('## 펫러스뉴스 자동 게재 %s\n'%TODAY+'\n'.join('- '+l for l in log)+'\n')
        if problems: f.write('\n### ❌ 치명적 문제\n'+'\n'.join('- '+p for p in problems)+'\n')
        if warns: f.write('\n### ⚠ 올리지 않은 큐 기사\n'+'\n'.join('- '+p for p in warns)+'\n')
if problems:
    print('\n❌ 치명적 문제 %d건 (아무것도 올리지 않음)'%len(problems)); [print(' -',p) for p in problems+warns]; sys.exit(1)
if warns:
    print('\n⚠ 오늘 기사는 준비됐지만 큐에 올리지 않은 기사가 있음(검수 표시 확인 필요)'); [print(' -',p) for p in warns]; sys.exit(10)
print('\n✅ 게재 준비 완료 — 오늘 기사:',have_today)
