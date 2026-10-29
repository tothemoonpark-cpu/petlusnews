import re,os,glob,shutil
import sys
SRC=sys.argv[1] if len(sys.argv)>1 else '/home/claude/jj/site'; OUT=sys.argv[2] if len(sys.argv)>2 else '/home/claude/jj/site_out'
tpl=open(f'{SRC}/about.html',encoding='utf-8').read()
tpl=tpl.replace('<a href="editorial.html">편집규약</a><a href="corrections.html">정정·반론보도</a><a href="contact.html">제보·광고·제휴</a><a href="terms.html">이용약관·저작권</a>','')
head,rest=tpl.split('<article class="doc">',1)
_,foot=rest.split('</article>',1)
PAGES={
'editorial.html':('편집규약','펫러스뉴스가 기사를 쓰고 고치는 원칙.','''<h2>편집규약</h2>
<p>펫러스뉴스는 반려동물의 건강·행동·생활과 펫로스를 다루는 인터넷신문입니다. 아래 원칙으로 기사를 쓰고 고칩니다.</p>
<h3>1. 출처와 사실 확인</h3>
<p>건강·행동 기사는 학술지 논문, 학회 지침, 공공기관 자료 같은 1차 출처를 밝힙니다.</p>
<p>연구를 소개할 때는 연구 대상과 나라, 발표 연도, 숫자의 분모를 함께 적고, 연구가 말하지 않은 것을 덧붙이지 않습니다.</p>
<p>개와 고양이처럼 종이 다른 동물의 사실은 섞어 쓰지 않습니다.</p>
<h3>2. 의료 정보의 한계</h3>
<p>기사는 진단과 치료를 대신하지 않습니다. 약 이름과 용량을 권하지 않습니다.</p>
<p>아픈 반려동물은 동물병원 진료가 먼저입니다. 응급일 수 있는 증상은 기사 안에서 병원에 가야 한다고 분명히 적습니다.</p>
<h3>3. 펫로스 기사</h3>
<p>떠난 반려동물을 둔 보호자의 슬픔을 병으로 단정하거나 축소하지 않습니다.</p>
<p>죽음과 자해를 다룰 때는 방법과 수단을 자세히 쓰지 않고, 도움을 받을 수 있는 상담 창구를 기사 끝에 안내합니다.</p>
<h3>4. 광고와 기사의 구분</h3>
<p>광고와 협찬은 기사와 분명히 구분해 「광고」 또는 「협찬」으로 표시합니다. 광고주나 협찬 사실이 기사 내용에 영향을 주지 않도록 합니다.</p>
<h3>5. 이해관계 공개</h3>
<p>발행인이 쓴 책, 강연, 칼럼, 운영하는 활동을 기사에서 다룰 때는 발행인과의 관계를 밝힙니다.</p>
<h3>6. 오류의 정정</h3>
<p>사실 오류가 확인되면 지체 없이 고치고, 고친 내용과 날짜를 기사 안에 밝힙니다. 정정·반론 보도 청구는 <a href="corrections.html">정정·반론보도 안내</a>를 따릅니다.</p>
<h3>7. 이미지</h3>
<p>기사에 쓰는 이미지는 직접 만들었거나 사용 허락을 받은 것만 씁니다.</p>
<p class="small">시행일: 2026년 10월 26일</p>'''),
'corrections.html':('정정·반론보도 안내','펫러스뉴스 기사의 오류 신고와 정정·반론보도 청구 방법.','''<h2>정정·반론보도 안내</h2>
<p>펫러스뉴스 기사에 사실과 다른 내용이 있거나 보도로 권리를 침해받았다고 생각하시면 아래 방법으로 알려 주십시오.</p>
<h3>1. 오류 신고</h3>
<p>기사의 사실 오류, 숫자·출처의 착오는 이메일 tothemoon_park@naver.com 으로 알려 주십시오. 기사 제목과 주소, 어느 부분이 어떻게 다른지 근거와 함께 적어 주시면 빠르게 확인합니다.</p>
<p>확인되면 기사를 고치고, 고친 내용과 날짜를 기사 안에 밝힙니다.</p>
<h3>2. 정정·반론보도 청구</h3>
<p>「언론중재 및 피해구제 등에 관한 법률」에 따른 정정보도·반론보도 청구는 발행인에게 서면으로 하며, 다음 내용을 적어 주십시오.</p>
<p>1. 청구인의 성명, 주소, 전화번호</p>
<p>2. 정정 또는 반론을 청구하는 보도의 내용(기사 제목과 주소)</p>
<p>3. 청구하는 이유</p>
<p>4. 청구하는 정정보도문 또는 반론보도문</p>
<p>보낼 곳: 부산광역시 동래구 금강로131번길 41 펫러스뉴스 발행인 앞, 또는 tothemoon_park@naver.com</p>
<h3>3. 처리 절차</h3>
<p>청구를 받은 날부터 3일 이내에 수용 여부를 알려 드립니다.</p>
<p>수용하면 청구를 받은 날부터 7일 이내에 정정보도문을 게재하고, 내용과 크기는 청구인과 협의합니다.</p>
<p>수용하지 못하는 경우에는 그 사유를 함께 알려 드립니다. 이견이 있으시면 언론중재위원회(<a href="https://www.pac.or.kr" rel="noopener">pac.or.kr</a>)에 조정을 신청하실 수 있습니다.</p>
<p class="small">이 안내는 법 조문을 쉽게 옮긴 것으로, 구체적인 요건과 기간은 법령이 정한 대로 적용합니다.</p>
<p class="small">시행일: 2026년 10월 26일</p>'''),
'contact.html':('제보·광고·제휴 문의','펫러스뉴스 제보, 보도자료, 광고·제휴 문의 방법.','''<h2>제보·광고·제휴 문의</h2>
<h3>기사 제보</h3>
<p>반려동물의 건강, 행동, 생활, 펫로스와 관련해 알리고 싶은 이야기나 확인이 필요한 소식이 있으면 이메일 tothemoon_park@naver.com 으로 보내 주십시오.</p>
<p>제보하실 때 확인할 수 있는 근거(자료, 출처, 날짜)를 함께 보내 주시면 도움이 됩니다.</p>
<p>제보자의 신원은 본인의 동의 없이 공개하지 않습니다. 자세한 내용은 <a href="privacy.html">개인정보처리방침</a>을 보십시오.</p>
<h3>보도자료</h3>
<p>동물병원, 학회, 연구기관, 지자체, 기업의 보도자료도 같은 주소로 받습니다. 기사 게재 여부와 내용은 편집 원칙에 따라 발행인이 정하며, 보도자료를 받았다고 해서 게재가 보장되지는 않습니다.</p>
<h3>광고·협찬</h3>
<p>광고와 협찬은 기사와 구분해 「광고」 또는 「협찬」으로 표시합니다. 청소년에게 유해한 광고와 의학적 효능을 과장하거나 진료를 대신하는 것처럼 보이게 하는 광고는 싣지 않습니다.</p>
<h3>콘텐츠 제휴</h3>
<p>기사 인용과 재게재, 공동 기획에 관한 문의도 받습니다. 출처 표시 조건은 <a href="terms.html">이용약관·저작권</a>을 보십시오.</p>
<h3>연락처</h3>
<p>이메일 tothemoon_park@naver.com · 전화 070-8064-6639</p>
<p>주소 부산광역시 동래구 금강로131번길 41</p>'''),
'terms.html':('이용약관·저작권','펫러스뉴스 이용 조건과 기사 저작권, 인용 기준.','''<h2>이용약관·저작권</h2>
<h3>1. 이용 조건</h3>
<p>펫러스뉴스는 회원가입 없이 누구나 기사를 읽을 수 있습니다. 이용자는 기사를 개인적으로 읽고 공유할 수 있습니다.</p>
<h3>2. 저작권</h3>
<p>펫러스뉴스가 쓴 기사와 이미지의 저작권은 펫러스뉴스에 있습니다. 허락 없는 전재, 복사, 배포, 편집은 금지됩니다.</p>
<h3>3. 인용과 링크</h3>
<p>기사의 일부를 인용할 때는 출처(펫러스뉴스)와 기사 주소를 분명히 밝히고, 인용하는 분량은 정당한 범위로 제한해 주십시오.</p>
<p>기사 주소로 거는 링크는 자유롭게 하셔도 됩니다.</p>
<h3>4. 건강 정보 안내</h3>
<p>기사의 건강 정보는 일반 정보이며 진단과 치료를 대신하지 않습니다. 아픈 반려동물은 동물병원 진료가 먼저입니다. 기사 정보를 따르다 생긴 결과는 수의사의 진료를 대신하지 않습니다.</p>
<h3>5. 외부 링크</h3>
<p>기사에 연결한 외부 사이트의 내용과 운영은 해당 사이트의 책임이며, 펫러스뉴스는 그 내용을 보증하지 않습니다.</p>
<h3>6. 문의</h3>
<p>이용 약관에 관한 문의는 tothemoon_park@naver.com 으로 보내 주십시오.</p>
<p class="small">시행일: 2026년 10월 26일</p>'''),
}
def mk(fn,title,desc,body):
    h=head
    h=re.sub(r'<title>.*?</title>',f'<title>{title} — 펫러스뉴스</title>',h)
    h=re.sub(r'<meta name="description" content="[^"]*">',f'<meta name="description" content="{desc}">',h)
    h=h.replace('https://petlusnews.com/about.html',f'https://petlusnews.com/{fn}')
    h=re.sub(r'<meta property="og:title" content="[^"]*">',f'<meta property="og:title" content="{title} — 펫러스뉴스">',h)
    h=re.sub(r'<meta property="og:description" content="[^"]*">',f'<meta property="og:description" content="{desc}">',h)
    return h+'<article class="doc">'+body+'</article>'+foot
os.makedirs(OUT,exist_ok=True)
for fn,(t,d,b) in PAGES.items():
    open(f'{OUT}/{fn}','w',encoding='utf-8').write(mk(fn,t,d,b))
# 404
body404='<h2>페이지를 찾을 수 없습니다</h2><p>주소가 바뀌었거나 없어진 페이지입니다.</p><p><a href="/">펫러스뉴스 첫 화면으로 가기</a></p>'
h404=mk('404.html','페이지를 찾을 수 없습니다','요청한 페이지를 찾을 수 없습니다.',body404)
h404=h404.replace('href="style.css"','href="/style.css"').replace('href="./"','href="/"')
h404=h404.replace('<link rel="canonical" href="https://petlusnews.com/404.html">','<meta name="robots" content="noindex">')
open(f'{OUT}/404.html','w',encoding='utf-8').write(h404)
# patch footers & about contact
NEWLINKS=[('editorial.html','편집규약'),('corrections.html','정정·반론보도'),('contact.html','제보·광고·제휴'),('terms.html','이용약관·저작권')]
def patch(path,rel):
    s=open(path,encoding='utf-8').read()
    pre='../' if rel.startswith('news/') else ''
    pat=f'<a href="{pre}privacy.html">개인정보처리방침</a></div>'
    if 'editorial.html' in s and f'{pre}editorial.html">편집규약' in s: return s
    assert pat in s,(path)
    add=''.join(f'<a href="{pre}{u}">{n}</a>' for u,n in NEWLINKS)
    s=s.replace(pat,f'<a href="{pre}privacy.html">개인정보처리방침</a>{add}</div>')
    return s
files=[os.path.relpath(p,SRC) for p in glob.glob(f'{SRC}/*.html')+glob.glob(f'{SRC}/news/*.html')]
for rel in files:
    s=patch(f'{SRC}/{rel}',rel)
    if rel=='about.html' and '편집규약</a>, <a href="corrections.html">' not in s:
        s=s.replace('<p>제보·정정 요청·문의: tothemoon_park@naver.com</p>','<p>제보·정정 요청·문의: tothemoon_park@naver.com</p>\n<p>자세한 원칙과 절차는 <a href="editorial.html">편집규약</a>, <a href="corrections.html">정정·반론보도 안내</a>, <a href="contact.html">제보·광고·제휴 문의</a>, <a href="terms.html">이용약관·저작권</a>에 있습니다.</p>')
    os.makedirs(os.path.dirname(f'{OUT}/{rel}') or OUT,exist_ok=True)
    open(f'{OUT}/{rel}','w',encoding='utf-8').write(s)
for fn in list(PAGES)+['404.html']:
    p=f'{OUT}/{fn}'
    _n=patch(p,fn)
    open(p,'w',encoding='utf-8').write(_n)
# sitemap + llms
sm=open(f'{SRC}/sitemap.xml',encoding='utf-8').read()
new=''.join(f'<url><loc>https://petlusnews.com/{u}</loc></url>' for u,_ in NEWLINKS)
sm=sm if 'editorial.html' in sm else (sm.replace('</urlset>',new+'</urlset>') if '</urlset>' in sm else sm)
open(f'{OUT}/sitemap.xml','w',encoding='utf-8').write(sm)
ll=open(f'{SRC}/llms.txt',encoding='utf-8').read()
ll=ll if 'editorial.html' in ll else ll.replace('- 문의: tothemoon_park@naver.com','- 편집규약: https://petlusnews.com/editorial.html\n- 정정·반론보도: https://petlusnews.com/corrections.html\n- 제보·광고·제휴: https://petlusnews.com/contact.html\n- 이용약관·저작권: https://petlusnews.com/terms.html\n- 문의: tothemoon_park@naver.com')
open(f'{OUT}/llms.txt','w',encoding='utf-8').write(ll)
print(sorted(os.listdir(OUT)))
