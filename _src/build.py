import os,re,json,html,glob
REG=json.load(open('site.json',encoding='utf-8'))
HEAD='''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="canonical" href="https://petlusnews.com/{path}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website"><meta property="og:url" content="https://petlusnews.com/{path}"><meta property="og:site_name" content="펫러스뉴스"><meta property="og:image" content="https://petlusnews.com/img/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:locale" content="ko_KR"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="https://petlusnews.com/img/og.png">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" type="image/png" href="/img/icon-512.png"><link rel="apple-touch-icon" href="/img/apple-touch-icon.png"><meta name="theme-color" content="#15233D"><meta name="naver-site-verification" content="a41504f54d8ca8a9d811a2c747599f601df6ccf3"><meta name="google-site-verification" content="UarPQjnbLLQOrz9SbC_ddajic1QH1zQVwLeKBuEro7o">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=IBM+Plex+Sans+KR:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css"><link rel="alternate" type="application/rss+xml" title="펫러스뉴스" href="feed.xml">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"NewsMediaOrganization","name":"펫러스뉴스","alternateName":"PETLUS NEWS","url":"https://petlusnews.com/","email":"tothemoon_park@naver.com","logo":{{"@type":"ImageObject","url":"https://petlusnews.com/img/logo.png","width":600,"height":60}},"image":"https://petlusnews.com/img/og.png","founder":{{"@type":"Person","name":"박근필","jobTitle":"수의사"}}}}</script>
</head><body>
<header><div class="wrap">
<div class="dateline"><span id="today">반려동물과 함께 사는 날들, 그리고 이별 이후까지</span><span>제보·문의 <a href="mailto:tothemoon_park@naver.com">tothemoon_park@naver.com</a></span></div>
<div class="mast"><a href="./"><p class="name">펫러스뉴스</p><p class="en">PETLUS NEWS</p></a><p class="motto">수의사가 만드는 반려동물·펫로스 전문 인터넷신문</p></div>
<nav class="sec" aria-label="분야"><a class="c-health" href="./health.html">건강</a><a class="c-behavior" href="./behavior.html">행동</a><a class="c-life" href="./life.html">생활</a><a class="c-loss" href="./loss.html">펫로스</a><a href="about.html">매체 소개</a><a href="publisher.html">발행인</a></nav>
</div></header>
<aside class="xband" aria-label="함께 보기"><div class="wrap"><p><b>펫로스로 마음이 힘드신가요?</b> 이름 없이 편지를 남기고 이야기를 나누는 <a href="https://tothemoonpark-cpu.github.io/pilacademy/petlus-shelter.html" target="_blank" rel="noopener">펫러스(PETLUS) 쉼터</a>가 있습니다. 발행인 박근필의 강연·집필은 <a href="https://tothemoonpark-cpu.github.io/pilacademy/" target="_blank" rel="noopener">박근필성장연구소</a>에서 만나실 수 있습니다.</p></div></aside>
<main><div class="wrap">'''
FOOT_T='''</div></main>
<footer><div class="wrap">
<p class="fn">펫러스뉴스</p>
<div class="links"><a href="about.html">매체 소개</a><a href="publisher.html">발행인 소개</a><a href="youth.html">청소년보호정책</a><a href="privacy.html">개인정보처리방침</a></div>
<dl>
<div><dt>제호</dt><dd>펫러스뉴스(PETLUS NEWS)</dd></div>
<div><dt>등록번호</dt><dd>{reg_no}</dd></div>
<div><dt>등록연월일</dt><dd>{reg_date}</dd></div>
<div><dt>발행연월일</dt><dd>{pub_date}</dd></div>
<div><dt>발행인·편집인</dt><dd>박근필</dd></div>
<div><dt>청소년보호책임자</dt><dd>박근필</dd></div>
<div><dt>발행소</dt><dd>부산광역시 동래구 금강로131번길 41</dd></div>
<div><dt>전화번호</dt><dd>070-8064-6639</dd></div>
<div><dt>이메일</dt><dd>tothemoon_park@naver.com</dd></div>
</dl>
<p class="copy">펫러스뉴스의 모든 콘텐츠는 저작권법의 보호를 받으며, 무단 전재·복사·배포를 금합니다. © 2026 펫러스뉴스</p>
</div></footer>
<script>try{const d=new Date(),w="일월화수목금토"[d.getDay()];document.getElementById("today").textContent=d.getFullYear()+"년 "+(d.getMonth()+1)+"월 "+d.getDate()+"일 "+w+"요일"}catch(e){}</script>
</body></html>'''
FOOT=FOOT_T.replace('{reg_no}',REG['reg_no']).replace('{reg_date}',REG['reg_date']).replace('{pub_date}',REG['pub_date'])
pages={}
pages['index.html']=('펫러스뉴스 PETLUS NEWS — 수의사가 만드는 반려동물·펫로스 전문 인터넷신문','반려동물의 건강·행동·생활과 펫로스를 다루는 인터넷신문. 20년 가까이 동물병원에서 일해 온 수의사가 발행합니다.','','''
<div class="front">
<article class="lead">
<span class="label">창간을 준비하며</span>
<h2>반려동물과 사는 날들, 그리고 그 이후까지 쓰겠습니다</h2>
<p class="byline"><a href="publisher.html">발행인 박근필(수의사)</a></p>
<p class="first">진료실에서 가장 자주 듣는 질문은 병의 이름보다 「제가 무엇을 해 줄 수 있을까요」였다.</p>
<p>반려동물과 사는 사람은 많아졌지만, 믿고 읽을 정보는 여전히 흩어져 있다. 광고와 정보가 섞인 글, 출처 없는 건강 상식, 겁을 주거나 지나치게 안심시키는 글 사이에서 보호자는 혼자 판단해야 한다.</p>
<p>펫러스뉴스는 그 판단을 돕기 위해 만든다. 반려동물의 건강과 행동, 함께 사는 생활과 제도를 수의학 근거와 출처를 밝혀 전한다.</p>
<p>그리고 지금까지 잘 다루지 않던 이야기, 반려동물을 떠나보낸 뒤의 시간까지 쓴다. 펫로스 증후군(펫로스 신드롬)은 유난이 아니라 많은 보호자가 겪는 슬픔이다.</p>
<p>현재 「신문 등의 진흥에 관한 법률」에 따른 인터넷신문 등록 절차를 밟고 있다. 등록이 끝나면 첫 기사를 싣는다.</p>
</article>
<aside class="side">
<div class="box status"><strong>창간 준비 중</strong>부산광역시에 인터넷신문 등록을 신청하고 있습니다. 등록번호가 나오면 이 화면 아래에 적고 기사를 싣습니다.</div>
<div class="box"><h3>편집 원칙</h3><ol>
<li>건강 정보는 수의학 근거와 출처를 함께 적는다.</li>
<li>진단과 치료를 대신하지 않는다. 아픈 반려동물은 동물병원 진료가 먼저다.</li>
<li>광고와 기사를 섞지 않는다.</li>
<li>틀린 내용은 바로 고치고, 고친 사실을 밝힌다.</li>
</ol></div>
<div class="box"><h3>제보·문의</h3><p>취재가 필요한 일, 바로잡을 내용, 함께 다뤘으면 하는 주제를 보내 주세요.</p><p><a href="mailto:tothemoon_park@naver.com">tothemoon_park@naver.com</a></p></div>
</aside>
</div>
<section class="desks" aria-labelledby="desks-h">
<h3 id="desks-h">펫러스뉴스가 다루는 분야</h3>
<div class="desk-grid">
<div class="desk d-health" id="d-health"><h4>건강</h4><p>몸이 보내는 신호를 읽는 법과 언제 병원에 가야 하는지를 수의학 근거로 전합니다.</p><ul><li>질병의 초기 신호</li><li>예방접종과 영양</li><li>나이 든 반려동물 돌보기</li></ul></div>
<div class="desk d-behavior" id="d-behavior"><h4>행동</h4><p>짖음, 숨기, 물기 같은 행동 뒤의 이유를 풀어 씁니다.</p><ul><li>몸짓과 소리의 뜻</li><li>문제 행동 이해하기</li><li>함께 지내는 법</li></ul></div>
<div class="desk d-life" id="d-life"><h4>생활</h4><p>입양부터 여행, 계절 안전, 바뀌는 제도까지 보호자에게 필요한 소식을 정리합니다.</p><ul><li>입양과 등록</li><li>계절별 안전</li><li>관련 제도와 산업 소식</li></ul></div>
<div class="desk d-loss" id="d-loss"><h4>펫로스</h4><p>이별을 준비하는 법, 떠나보낸 뒤의 슬픔, 장례와 추모, 곁에 있는 사람이 할 수 있는 일을 다룹니다.</p><ul><li>이별 준비와 결정</li><li>슬픔과 회복</li><li>장례와 추모</li></ul></div>
</div>
</section>''')
pages['about.html']=('매체 소개 — 펫러스뉴스','펫러스뉴스의 발행 목적과 편집 원칙.','about.html','''
<article class="doc"><h2>매체 소개</h2>
<p>펫러스뉴스(PETLUS NEWS)는 반려동물 전반과 펫로스를 다루는 인터넷신문입니다.</p>
<p>제호 「펫러스(PETLUS)」는 「펫 러브 어스(PET Love US)」를 줄인 이름입니다.</p>
<p>반려동물(PET)과 사랑(Love), 우리(US)를 한데 이었습니다.</p>
<p>반려동물을 사랑하는 우리 모두를 위한 신문이라는 뜻을 담았습니다.</p>
<h3>다루는 분야</h3>
<p>반려동물의 건강·행동·생활 정보와 관련 제도·산업 소식, 그리고 반려동물을 떠나보낸 보호자의 슬픔과 회복을 다룹니다.</p>
<h3>편집 원칙</h3>
<p>1. 건강 정보는 수의학 근거와 출처를 밝혀 씁니다.</p>
<p>2. 진단과 치료를 대신하지 않습니다. 아픈 반려동물은 동물병원 진료가 먼저입니다.</p>
<p>3. 광고와 기사를 구분합니다.</p>
<p>4. 잘못이 확인되면 바로 고치고, 고친 사실을 밝힙니다.</p>
<h3>발행인·편집인</h3>
<p>박근필 — 20년 가까이 동물병원 임상 현장에서 일해 온 수의사이자 작가입니다.</p>
<h3>연락처</h3>
<p>제보·정정 요청·문의: tothemoon_park@naver.com</p>
</article>''')
pages['publisher.html']=('발행인 박근필 — 펫러스뉴스','펫러스뉴스 발행인 박근필. 20년 가까이 동물병원에서 일해 온 수의사이자 저서 5권의 작가. 두산 두피디아 동물 백과 집필, ONN TV 〈신비한 동물 사전〉 고정 출연, 펫로스 치유 글쓰기 강좌를 이끈다.','publisher.html','''
<article class="doc pub">
<h2>발행인 박근필</h2>
<p class="pub-lead">20년 가까이 동물병원에서 아픈 동물과 보호자를 만나 온 수의사입니다. 진료실 밖에서는 책과 칼럼, 강연과 방송으로 반려동물과 사람 이야기를 전합니다.</p>

<h3>수의사</h3>
<ul>
<li>경북대학교 수의학과 졸업(2010), 수의사 면허 취득(2010)</li>
<li>한국예술인복지재단 예술활동증명(2025)</li>
<li>임상 수의사로 20년 가까이 근무, 동물병원 약 10년 직접 운영</li>
<li>두산 두피디아 동물 백과 항목 집필(네이버 지식백과 동물 분야)</li>
</ul>

<h3>펫로스</h3>
<ul>
<li>펫로스 치유 글쓰기 「펫러스(PETLUS)」 강좌 진행(김해율하도서관 2026년 7월, 4회)</li>
<li>전북대학교 수의과대학 「반려동물 한마당」 강연 「지금 함께하는 시간을 더 잘 사랑하는 법과 건강한 이별 준비」(2026년 9월, 약 1,600명 참여 행사) — <a href="https://youtu.be/qxMwZeOjdik">강연 영상</a> · <a href="https://www.dailyvet.co.kr/news/college/298148">데일리벳 보도</a></li>
<li>세계일보 「펫 상실학 개론」 칼럼 연재(2026년 9월~) — <a href="https://www.segye.com/newsView/20260903510324">「그날 진료실에 있던 또 한 사람」</a> 외</li>
<li>반려동물을 떠나보낸 보호자가 이름 없이 편지와 이야기를 나누는 펫러스(PETLUS) 쉼터 운영</li>
<li>각당복지재단 애도상담전문가 기본교육 수강 중(2026.9~12), 건국대학교 「독서치유론」(K-MOOC) 수강 중</li>
</ul>

<h3>방송</h3>
<ul>
<li>ONN TV 〈신비한 동물 사전〉 고정 출연</li>
<li>ONN닥터TV 〈이 책을 쓴 사람〉, 한국시니어TV 〈생각을 바꾸는 시간, S클래스〉 출연</li>
</ul>

<h3>저서</h3>
<ul>
<li>『할퀴고 물려도 나는 수의사니까』(씽크스마트, 2023)</li>
<li>『나는 매일 두 번 출근합니다』(미다스북스, 2024)</li>
<li>『마흔 더 늦기 전에 생각의 틀을 리셋하라』(알토북스, 2025) — 교보문고·예스24 자기계발 온라인 일간 베스트셀러 1위</li>
<li>『방구석에서 혼자 읽는 직업 토크쇼』(공저, 미다스북스, 2025)</li>
<li>『당신의 원고는 왜 계약되지 않는가』(미다스북스, 2026)</li>
<li>여섯 번째 책 집필 중(파지트)</li>
</ul>

<h3>칼럼과 강연</h3>
<ul>
<li>수의 전문지 데일리벳·데일리개원을 비롯해 30개 매체에 칼럼 기고, 지금도 20여 개 매체에 연재 중</li>
<li>전국 초·중·고 38개교 진로·직업 특강, 부산시청 저자 특강</li>
<li>부산대학교 미래시민교육원·부경대학교 미래교육원 강좌 선정(2026), 부산시교육청영재교육진흥원 교사 직무연수 강사</li>
<li>매일경제 MK Speaker 연사 등록</li>
<li>직업인 60여 명 인터뷰 「박근필의 피플인사이트」 진행</li>
</ul>

<h3>언론 인터뷰</h3>
<ul class="press">
<li>2026.8 한국강사신문 — <a href="https://www.lecturernews.com/news/articleView.html?idxno=207862">“AI 시대 대체되지 않는 경쟁력은 읽고 쓰는 힘에서 나온다”</a></li>
<li>2026.7 경향신문 — <a href="https://www.khan.co.kr/article/202607271437001">“누구든 책 두 권은 쓸 수 있어요” 평범한 사람이 작가가 되는 법</a></li>
<li>2026.6 투데이신문 — <a href="https://www.ntoday.co.kr/news/articleView.html?idxno=127775">“AI 시대, 글쓰기가 ‘나다움’이라는 무기를 만든다”</a></li>
<li>2026.4 ONN닥터TV — <a href="https://www.youtube.com/watch?v=2fe0JvvrvbU">수의사가 말하는 직업의 현실과 글쓰기가 인생에 가져온 변화</a></li>
<li>2026.3 커리어온뉴스 — <a href="https://www.careeronnews.kr/news/473344">“좋은 직업보다 중요한 것은 판단 기준”</a></li>
<li>2026.3 뉴스앤잡 — <a href="https://www.newsnjob.com/news/articleView.html?idxno=32467">전문직도 N잡러 시대! 박근필 성장연구소 소장</a></li>
<li>2026.2 뉴스클레임 — <a href="https://www.newsclaim.co.kr/news/articleView.html?idxno=3056718">수의사로 살다 마흔에 인생을 리셋하다</a></li>
<li>2026.2 미디어파인 — <a href="https://www.mediafine.co.kr/news/articleView.html?idxno=75486">읽고 쓰고 말하는 삶… 박근필 작가 인터뷰</a></li>
<li>2026.2 대한민국교육신문 — <a href="https://www.kedupress.com/news/article.html?no=390683">「꿈보다 중요한 것은 기준이다」</a></li>
<li>2025.9 Book News — <a href="https://booknews.or.kr/?p=3034">‘마흔, 더 늦기 전에 생각의 틀을 리셋하라’의 박근필 작가</a></li>
<li>2025.7 SLICE — <a href="https://blog.myslice.is/interview_11th_tothemoon/">수의사로서 위축될 땐 작가로 자존감을 챙겨요</a></li>
<li>2024.11 월간 리더스 — <a href="https://blog.naver.com/kleadersforum/223643797678">읽고 쓰고 말하는 삶 - 박근필 수의사</a></li>
<li>2023.10 CEO저널 — <a href="https://www.ceojhn.com/news/articleView.html?idxno=2717">글쓰는 수의사 투더문, 박근필 수의사</a></li>
</ul>
<p class="more"><a href="https://tothemoonpark-cpu.github.io/pilacademy/author.html">인터뷰 전체 목록 보기</a></p>

<h3>칼럼 연재 매체</h3>
<p class="outlets">세계일보 · 한국강사신문 · 한국독서교육신문 · 대한민국교육신문 · 교육플러스 · 미디어파인 · 뉴스클레임 · 코스미안뉴스 · PPSS · 뉴스프리존 · 이모작뉴스 · 캐어유뉴스 · 아웃소싱타임즈 · 더에듀 · 데일리벳 · 데일리개원 · 학생과청소년 · 이로운넷 · 뉴스앤잡 · 키즈맘 · 경인미래교육신문 · 독서신문 · 뉴스테이션 · 경인열린신문 · 호남교육신문 · 한국인공지능신문 · 뉴스후플러스 · 에듀진 · 출판교육문화뉴스 · 커리어온뉴스</p>
<p class="more"><a href="https://tothemoonpark-cpu.github.io/pilacademy/columns.html">칼럼 아카이브(전체 글) 보기</a></p>

<h3>자주 묻는 질문</h3>
<dl class="faq">
<dt>박근필은 누구인가요?</dt>
<dd>20년 가까이 임상에서 일해 온 수의사이자 저서 5권의 작가입니다. 펫러스뉴스를 발행하고, 박근필성장연구소를 운영합니다.</dd>
<dt>지금도 수의사로 일하나요?</dt>
<dd>그렇습니다. 약 10년간 운영하던 병원은 정리했지만, 지금도 동물병원에서 일합니다.</dd>
<dt>펫로스 강연이나 강좌를 요청할 수 있나요?</dt>
<dd>네. 도서관 펫로스 치유 글쓰기 강좌와 대학 행사 강연을 해 왔고, 기관 강연 요청도 받습니다. tothemoon_park@naver.com 으로 문의해 주십시오.</dd>
<dt>펫러스뉴스는 어떤 매체인가요?</dt>
<dd>수의사 박근필이 발행하는 반려동물·펫로스 전문 인터넷신문입니다. 반려동물의 건강·행동·생활과 펫로스를 수의학 근거와 출처를 밝혀 다룹니다.</dd>
</dl>

<h3>더 알아보기</h3>
<ul class="links-out">
<li><a href="https://tothemoonpark-cpu.github.io/pilacademy/author.html">박근필성장연구소 소장 소개</a></li>
<li><a href="https://tothemoonpark-cpu.github.io/pilacademy/books.html">저서 전체</a></li>
<li><a href="https://blog.naver.com/tothemoon_park">네이버 블로그</a> · <a href="https://brunch.co.kr/@tothemoonpark">브런치</a> · <a href="https://www.youtube.com/@tothemoonpark">유튜브</a></li>
<li><a href="https://www.instagram.com/tothemoon_park/">인스타그램</a> · <a href="https://www.threads.com/@tothemoon_park">스레드</a> · <a href="https://x.com/Tothemoon_Park">X</a> · <a href="https://litt.ly/tothemoonpark">리틀리</a></li>
</ul>
<p class="contact">취재·강연·집필 문의: <a href="mailto:tothemoon_park@naver.com">tothemoon_park@naver.com</a></p>
</article>''')
pages['youth.html']=('청소년보호정책 — 펫러스뉴스','펫러스뉴스 청소년보호정책.','youth.html','''
<article class="doc"><h2>청소년보호정책</h2>
<p>펫러스뉴스는 청소년이 유해한 정보에 노출되지 않도록 「청소년 보호법」과 「신문 등의 진흥에 관한 법률」에 따라 다음과 같이 청소년보호정책을 운영합니다.</p>
<h3>1. 유해정보 차단</h3>
<p>청소년에게 유해한 기사, 광고, 이미지를 게재하지 않습니다.</p>
<p>외부에서 받은 광고와 자료도 게재 전에 확인합니다.</p>
<h3>2. 유해정보 신고</h3>
<p>청소년에게 유해하다고 판단되는 내용을 발견하시면 아래 청소년보호책임자에게 알려 주십시오.</p>
<p>확인 즉시 조치하겠습니다.</p>
<h3>3. 청소년보호책임자</h3>
<p>성명: 박근필 (발행인)</p>
<p>이메일: tothemoon_park@naver.com</p>
<p>시행일: 2026년 10월 9일</p>
</article>''')
pages['privacy.html']=('개인정보처리방침 — 펫러스뉴스','펫러스뉴스 개인정보처리방침.','privacy.html','''
<article class="doc"><h2>개인정보처리방침</h2>
<p>펫러스뉴스는 「개인정보 보호법」에 따라 이용자의 개인정보를 보호합니다.</p>
<h3>1. 수집하는 개인정보</h3>
<p>펫러스뉴스는 회원가입 기능이 없으며, 기사를 읽는 데 개인정보를 받지 않습니다.</p>
<p>이용자가 이메일로 제보·문의를 보낼 때, 보낸 사람의 이메일 주소와 이용자가 직접 적은 내용만 처리합니다.</p>
<h3>2. 이용 목적과 보유 기간</h3>
<p>제보·문의에 답하고 사실을 확인하는 데에만 쓰며, 처리가 끝나면 지체 없이 파기합니다.</p>
<p>법령에 따라 보관해야 하는 경우에는 그 기간 동안 보관합니다.</p>
<h3>3. 제3자 제공</h3>
<p>법령에 근거가 있는 경우를 제외하고 개인정보를 다른 곳에 제공하지 않습니다.</p>
<h3>4. 제보자 보호</h3>
<p>제보자의 신원은 본인의 동의 없이 공개하지 않습니다.</p>
<h3>5. 이용자의 권리</h3>
<p>이용자는 자신의 개인정보에 대해 열람, 정정, 삭제, 처리 정지를 요청할 수 있습니다.</p>
<h3>6. 개인정보 보호책임자</h3>
<p>성명: 박근필 / 이메일: tothemoon_park@naver.com</p>
<p>시행일: 2026년 10월 9일</p>
</article>''')
PERSON={"@context":"https://schema.org","@type":"Person","name":"박근필","alternateName":"PARK KEUNPIL","jobTitle":["수의사","작가","펫러스뉴스 발행인"],"url":"https://petlusnews.com/publisher.html","email":"tothemoon_park@naver.com","alumniOf":{"@type":"CollegeOrUniversity","name":"경북대학교 수의학과"},"knowsAbout":["수의학","반려동물 건강","반려동물 행동","펫로스","펫로스 증후군","애도","글쓰기","진로"],"worksFor":{"@type":"NewsMediaOrganization","name":"펫러스뉴스","url":"https://petlusnews.com/"},"sameAs":["https://tothemoonpark-cpu.github.io/pilacademy/author.html","https://litt.ly/tothemoonpark","https://blog.naver.com/tothemoon_park","https://brunch.co.kr/@tothemoonpark","https://www.youtube.com/@tothemoonpark","https://www.instagram.com/tothemoon_park/","https://www.threads.com/@tothemoon_park","https://x.com/Tothemoon_Park","http://www.mkspeaker.co.kr/speaker_view.php?no=424"]}
for f,(t,d,p,body) in pages.items():
    h=HEAD.format(title=t,desc=d,path=p)
    if f=='publisher.html':
        import re as _re
        qa=_re.findall(r'<dt>(.*?)</dt>\s*<dd>(.*?)</dd>',body,_re.S)
        FAQ={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":_re.sub('<[^>]+>','',a)}} for q,a in qa]}
        h=h.replace('</head>','<script type="application/ld+json">'+json.dumps(PERSON,ensure_ascii=False)+'</script><script type="application/ld+json">'+json.dumps(FAQ,ensure_ascii=False)+'</script></head>',1)
    if f=='publisher.html': h=h.replace('<meta property="og:type" content="website">','<meta property="og:type" content="profile">')
    open(f,'w',encoding='utf-8').write(h+body+FOOT)
open('robots.txt','w').write('User-agent: *\nAllow: /\nSitemap: https://petlusnews.com/sitemap.xml\n')
open('sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>https://petlusnews.com/{p}</loc></url>' for p in ['','about.html','publisher.html','youth.html','privacy.html'])+'</urlset>\n')

# ---------------- 기사 (articles/*.md) ----------------
SECTIONS=['건강','행동','생활','펫로스']
def parse(fp):
    t=open(fp,encoding='utf-8').read()
    m=re.match(r'---\n(.*?)\n---\n(.*)',t,re.S); meta={}; key=None
    for line in m.group(1).split('\n'):
        if re.match(r'^\w+:',line): key,v=line.split(':',1); meta[key.strip()]=v.strip()
        elif key: meta[key]+='\n'+line
    for k in list(meta):
        v=meta[k].strip()
        if len(v)>1 and v[0]==v[-1]=='"': meta[k]=v[1:-1]
    meta['body']=m.group(2).strip(); return meta
def body_html(b):
    out=[]
    for blk in re.split(r'\n\s*\n',b):
        blk=blk.strip()
        if not blk: continue
        if blk.startswith('## '): out.append('<h3>'+html.escape(blk[3:])+'</h3>')
        else: out.append('<p>'+'<br>'.join(html.escape(l) for l in blk.split('\n'))+'</p>')
    return '\n'.join(out)
arts=[]
if REG.get('registered'):
    for fp in sorted(glob.glob('articles/*.md')):
        a=parse(fp)
        if a.get('publish','').lower()!='yes': continue
        arts.append(a)
arts.sort(key=lambda a:a['date'],reverse=True)
os.makedirs('news',exist_ok=True)
def VETNOTE(a):
    n=(a.get('note') or '').strip()
    if not n: return ''
    return '\n<aside class="vetnote" style="margin:1.6em 0;padding:1em 1.2em;border-left:4px solid #2f6f6b;background:#f3f8f7;border-radius:4px"><p style="margin:0 0 .4em;font-weight:700;font-size:.9em;color:#2f6f6b">박근필 수의사의 한 줄</p><p style="margin:0">'+html.escape(n)+'</p></aside>'
CARE='<p class="care">마음이 많이 힘드실 때는 혼자 견디지 않으셔도 됩니다. 사랑의전화복지재단 상담센터 1566-2525(펫로스 상담), 자살예방상담전화 109, 정신건강위기상담 1577-0199(야간·공휴일에는 광역정신건강복지센터로 연결)에 전화하실 수 있습니다.</p>'
for a in arts:
    slug=a['slug']; url=f'https://petlusnews.com/news/{slug}.html'
    src=''.join(f'<li><a href="{html.escape(u.strip())}" rel="nofollow noopener">{html.escape(n.strip())}</a></li>' if u.strip() else f'<li>{html.escape(n.strip())}</li>' for n,_,u in (l.partition('|') for l in a.get('sources','').split('\n') if l.strip()))
    ld={"@context":"https://schema.org","@type":"NewsArticle","headline":a['title'],"datePublished":a['date'],"dateModified":a.get('updated',a['date']),"author":{"@type":"Person","name":"박근필","jobTitle":"수의사","url":"https://tothemoonpark-cpu.github.io/pilacademy/author.html","sameAs":["https://litt.ly/tothemoonpark","https://tothemoonpark-cpu.github.io/pilacademy/"]},"publisher":{"@type":"NewsMediaOrganization","name":"펫러스뉴스","url":"https://petlusnews.com/","logo":{"@type":"ImageObject","url":"https://petlusnews.com/img/logo.png","width":600,"height":60},"publishingPrinciples":"https://petlusnews.com/about.html"},"image":"https://petlusnews.com/img/og.png","inLanguage":"ko-KR","keywords":a.get('keywords',''),"mainEntityOfPage":url,"articleSection":a['section'],"description":a['summary']}
    page=HEAD.format(title=a['title']+' — 펫러스뉴스',desc=a['summary'],path='news/'+slug+'.html').replace('href="style.css"','href="../style.css"').replace('href="./','href="../').replace('href="about.html"','href="../about.html"').replace('href="publisher.html"','href="../publisher.html"')
    faqs=[(q.strip(),an.strip()) for q,_,an in (l.partition('|') for l in a.get('faq','').split('\n') if l.strip())]
    lds=[ld,{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"펫러스뉴스","item":"https://petlusnews.com/"},{"@type":"ListItem","position":2,"name":a['section'],"item":"https://petlusnews.com/"+{'건강':'health','행동':'behavior','생활':'life','펫로스':'loss'}[a['section']]+".html"},{"@type":"ListItem","position":3,"name":a['title'],"item":url}]}]
    if faqs: lds.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":an}} for q,an in faqs]})
    page=page.replace('<meta property="og:type" content="website">','<meta property="og:type" content="article"><meta property="article:published_time" content="'+a['date']+'"><meta property="article:section" content="'+a['section']+'"><meta name="keywords" content="'+html.escape(a.get('keywords',''))+'">')
    page=page.replace('</head>',''.join('<script type="application/ld+json">'+json.dumps(x,ensure_ascii=False)+'</script>' for x in lds)+'</head>',1)
    body=f'''<article class="doc news"><p class="kicker s-{a["section"]}">{html.escape(a["section"])}</p><h2>{html.escape(a['title'])}</h2>
<p class="byline"><a href="../publisher.html">박근필 발행인(수의사)</a> · {a['date']}{(' · 수정 '+a['updated']) if a.get('updated') else ''}</p>
<p class="lead-sum">{html.escape(a["summary"])}</p>
{body_html(a['body'])}{VETNOTE(a)}
{('<h3>자주 묻는 질문</h3>'+''.join('<p><strong>'+html.escape(q)+'</strong><br>'+html.escape(an)+'</p>' for q,an in faqs)) if faqs else ''}
{CARE if a['section']=='펫로스' else ''}
{('<h3>참고 자료</h3><ul class="src">'+src+'</ul>') if src else ''}
<p class="fix">기사에 잘못된 내용이 있으면 tothemoon_park@naver.com 으로 알려 주세요. 확인 즉시 고치고 고친 사실을 밝힙니다.</p></article>'''
    foot=FOOT.replace('href="publisher.html"','href="../publisher.html"').replace('href="about.html"','href="../about.html"').replace('href="publisher.html"','href="../publisher.html"').replace('href="youth.html"','href="../youth.html"').replace('href="privacy.html"','href="../privacy.html"')
    open(f'news/{slug}.html','w',encoding='utf-8').write(page+body+foot)
if arts:
    lst=''.join(f'<li class="item"><span class="sec s-{a["section"]}">{html.escape(a["section"])}</span><a href="news/{a["slug"]}.html">{html.escape(a["title"])}</a><p>{html.escape(a["summary"])}</p><time>{a["date"]}</time></li>' for a in arts)
    secs=''.join(f'<section class="card" id="s-{s}"><h3>{s}</h3><ul>'+''.join(f'<li><a href="news/{a["slug"]}.html">{html.escape(a["title"])}</a></li>' for a in arts if a['section']==s)+'</ul></section>' for s in SECTIONS)
    idx=HEAD.format(title='펫러스뉴스 PETLUS NEWS — 반려동물·펫로스 전문 인터넷신문',desc='반려동물의 건강·행동·생활과 펫로스를 다루는 인터넷신문. 현직 수의사가 발행합니다.',path='')
    idx=idx.replace('href="./#sections">건강','href="#s-건강">건강').replace('href="./#sections">행동','href="#s-행동">행동').replace('href="./#sections">생활','href="#s-생활">생활').replace('href="./#sections">펫로스','href="#s-펫로스">펫로스')
    open('index.html','w',encoding='utf-8').write(idx+'<h2 class="latest">최신 기사</h2><ul class="list">'+lst+'</ul><div class="grid">'+secs+'</div>'+FOOT)
    CATS=[('건강','health','몸이 보내는 신호를 읽는 법과 언제 병원에 가야 하는지를 수의학 근거로 전합니다.'),('행동','behavior','짖음, 숨기, 물기 같은 행동 뒤의 이유를 풀어 씁니다.'),('생활','life','입양부터 여행, 계절 안전, 바뀌는 제도까지 보호자에게 필요한 소식을 정리합니다.'),('펫로스','loss','이별을 준비하는 법, 떠나보낸 뒤의 슬픔, 장례와 추모, 곁에 있는 사람이 할 수 있는 일을 다룹니다.')]
    for sec,fn,desc in CATS:
        sa=[a for a in arts if a['section']==sec]
        lst2=''.join(f'<li class="item"><span class="sec s-{a["section"]}">{html.escape(a["section"])}</span><a href="news/{a["slug"]}.html">{html.escape(a["title"])}</a><p>{html.escape(a["summary"])}</p><time>{a["date"]}</time></li>' for a in sa)
        if not lst2: lst2='<li class="item"><p>이 분야의 첫 기사를 준비하고 있습니다. 사실 대조를 마친 기사만 게재합니다.</p></li>'
        extra=CARE if sec=='펫로스' else ''
        pg=HEAD.format(title=sec+' 기사 — 펫러스뉴스',desc=desc,path=fn+'.html')
        pg=pg.replace('class="c-%s"'%fn,'class="c-%s" aria-current="page"'%fn,1)
        open(fn+'.html','w',encoding='utf-8').write(pg+'<h2 class="latest">'+sec+' <span style="font-weight:400;font-size:.7em">기사 '+str(len(sa))+'편</span></h2><p class="lead">'+desc+'</p><ul class="list">'+lst2+'</ul>'+extra+'<p><a href="./">전체 기사 보기</a></p>'+FOOT)
    items=''.join(f'<item><title>{html.escape(a["title"])}</title><link>https://petlusnews.com/news/{a["slug"]}.html</link><description>{html.escape(a["summary"])}</description><pubDate>{a["date"]}</pubDate></item>' for a in arts[:30])
    open('feed.xml','w',encoding='utf-8').write(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>펫러스뉴스</title><link>https://petlusnews.com/</link><description>반려동물·펫로스 전문 인터넷신문</description>{items}</channel></rss>')
    urls=['','health.html','behavior.html','life.html','loss.html','about.html','publisher.html','youth.html','privacy.html']+['news/'+a['slug']+'.html' for a in arts]
    open('sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>https://petlusnews.com/{p}</loc></url>' for p in urls)+'</urlset>\n')
llm=["# 펫러스뉴스 (PETLUS NEWS)","","> 수의사 박근필이 발행하는 반려동물·펫로스 전문 인터넷신문. 반려동물의 건강·행동·생활과 펫로스(반려동물 상실 뒤의 슬픔)를 수의학 근거와 출처를 밝혀 다룬다.","","- 발행인·편집인: 박근필(수의사, 20년 가까이 동물병원 임상) — https://tothemoonpark-cpu.github.io/pilacademy/author.html","- 발행인 소개: https://petlusnews.com/publisher.html","- 편집 원칙: https://petlusnews.com/about.html","- 문의: tothemoon_park@naver.com",""]
if arts: llm+=["## 기사",""]+[f"- [{a['title']}](https://petlusnews.com/news/{a['slug']}.html): {a['summary']}" for a in arts]
open('llms.txt','w',encoding='utf-8').write('\n'.join(llm)+'\n')
print('articles published:',len(arts))
