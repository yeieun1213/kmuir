from konlpy.tag import Komoran
komoran = Komoran()

# output 파일 읽기
f = open('./kmaoutput_utf8.txt', 'r', encoding='utf8')

# list에 저장
chaeonheadList = set()      # 체언
josatailList = set()        # 조사
eomitailList = set()        # 어미
jeopmisatailList = set()    # 접미사

# komoran의 명사/접미사 list
chaeonList = ['NN', 'NNG', 'NNP', 'NNB']
jeopmisaList = ['XS', 'XSN', 'XSV', 'XSA']

while(1):
    s = f.readline()    # 한 줄씩 파일 읽기
    if not s:   # 종료
        print("break")
        break
    s = s.strip()       # 좌우 공백지우기

    if s.find('(') != 0:
        pass
    else:
        while(True):
            num = s.find('(')
            if num == -1:
                break
            n = s[num+1:num+2]  # 형태소
            s = s[num+4:]   # s indexing
            if n == 'N':    # 명사
                num = s.find("\"")
                chaeonheadList.add(s[:num])
            elif n == 'Z':      # 부사
                num = s.find("\"")
                chaeonheadList.add(s[:num])
            elif n == 'j':      # 조사
                num = s.find("\"")
                josatailList.add(s[:num])
            elif n == 'e':      # 어미
                num = s.find("\"")
                eomitailList.add(s[:num])
            elif (n == 'c') or (n == 't'):     # 접미사
                num = s.find("\"")
                jeopmisatailList.add(s[:num])

test = ['먹고는', '갔었다', '아름다운', '했다', '노력했다', '생각한다면',
        '안녕하세요', '너는', '즐겁다', '행복한', '배고프다']

for i in range(len(test)):
    sen = test[i]
    print("%d. %s" %(i+1, sen))
    sum = 0     # 조사/어미를 나눌 수 없을 경우를 판단하기 위해
    case1 = 0   # 전미사로 나눠야 하는 경우를 판단하기 위해

    # 해당 어절이 명사 + 접미사로 나눠지는 경우
    headNN = ''     # head 명사
    tailNum = 0     # suffix 위치
    sList = komoran.pos(sen)    # komoran 사용
    for k in range(len(sList)):
        sl = sList[k][1]
        if sl in chaeonList:    # 형태소가 명사일 경우
            headNN = sList[k][0]
        if sl in jeopmisaList:  # 형태소가 접미사일 경우
            tailNum += len(headNN)  # 접미사 위치
            case1 += 1
            print("case1: %s/head + %s/tail_suffix" % (headNN, sen[tailNum:]))

    # 해당 어절이 명사 + 접미사로 나눠지지 않는 경우
    if case1 == 0:
        for j in range(len(sen)):
            head = sen[:j+1]
            tail = sen[j+1:]
            if tail in eomitailList:    # 어미
                sum += 1
                print("case2: %s/head + %s/tail_Eomi" % (head, tail))
            if tail in josatailList:    # 조사
                sum += 1
                print("case3: %s/head + %s/tail_Josa" % (head, tail))

        # 어미/조사로 나눠지지 않는 경우
        if sum == 0:
            print("case4: %s/head" % (sen))
    print("\n")
