from vpython import *
# 두근두근 물리 1편 관성 — 응용 실습 「컬링 대결」 (숫자는 모두 설명용이에요)
# 스톤을 마우스로 끌다가 놓으면 놓는 순간의 속도로 출발해요. 손을 떠난 뒤에는 아무도 밀지 않아요.

# ===== 1. 바꿔 볼 숫자: 고친 뒤 다시 실행해 보세요 =====
줄어드는_빠르기 = 1      # 얼음에서 1초 동안 줄어드는 빠르기 (m/s): 기본 실습의 얼음과 같아요
비질한_빠르기 = 0.5      # 비질하는 동안 1초에 줄어드는 빠르기 (m/s): 닦은 얼음은 더 매끄러워요
손_배율 = 3              # 놓는 빠르기(m/s) = 마우스 빠르기(1초에 화면 높이의 몇 배) × 손_배율
최대_빠르기 = 9          # 놓는 빠르기는 이보다 빠를 수 없어요 (m/s)
팀마다_스톤 = 4          # 팀마다 던지는 스톤 수 (1~8): 화면 오른쪽 위 메뉴로도 바꿀 수 있어요
시간간격 = 1 / 600       # 한 걸음에 걸리는 시간 (초): 1초를 600걸음으로 잘게 나눠요

# ===== 2. 법칙: 미끄러지기는 기본 실습과 같아요. 다만 속도에는 방향이 있어요 =====
def 한_걸음(속도, 위치, 줄어드는_빠르기):
    빠르기 = mag(속도) - 줄어드는_빠르기 * 시간간격   # 방해가 있는 만큼만 빠르기가 줄어들어요
    if 빠르기 < 0:
        빠르기 = 0                                   # 방해는 멈추게 할 뿐, 뒤로 밀지는 않아요
    속도 = 빠르기 * hat(속도)                       # 방향은 그대로 두고 빠르기만 바꿔요
    위치 = 위치 + 속도 * 시간간격                    # 지금 속도로 한 걸음만큼 가요
    return 속도, 위치

def 부딪히기(i, j):                                  # 무게가 같은 두 스톤 i, j가 맞닿으면
    사이 = 위치들[j] - 위치들[i]
    if mag(사이) >= 2 * 스톤_반지름:
        return                                       # 아직 닿지 않았어요
    방향 = hat(사이)                                 # i에서 j로 향하는 방향
    다가옴 = dot(속도들[i] - 속도들[j], 방향)       # 그 방향으로 서로 다가오는 빠르기
    if 다가옴 > 0:
        속도들[i] = 속도들[i] - 다가옴 * 방향        # 맞닿은 방향의 속도를 서로 주고받아요
        속도들[j] = 속도들[j] + 다가옴 * 방향
        play_sound(330, 0.06, 'triangle', 0.4)

def 점수_계산(팀들, 거리들, 닿는_거리):              # 거리들: 스톤마다 과녁 한가운데까지의 거리 (m)
    빨강_최고, 노랑_최고 = 99, 99                    # 팀마다 과녁 한가운데에 가장 가까운 거리
    for i in range(len(팀들)):
        if 거리들[i] <= 닿는_거리 and 팀들[i] == '빨강':      # 과녁에 닿은 스톤만 세요
            빨강_최고 = min(빨강_최고, 거리들[i])
        if 거리들[i] <= 닿는_거리 and 팀들[i] == '노랑':
            노랑_최고 = min(노랑_최고, 거리들[i])
    if 빨강_최고 == 노랑_최고:
        return '', 0                                 # 과녁에 스톤이 없거나 똑같이 가까우면 0점
    이긴_팀 = '빨강' if 빨강_최고 < 노랑_최고 else '노랑'
    상대_최고 = max(빨강_최고, 노랑_최고)
    점수 = 0
    for i in range(len(팀들)):                       # 상대 팀의 가장 가까운 스톤보다 가까운 스톤마다 1점
        if 팀들[i] == 이긴_팀 and 거리들[i] < 상대_최고 and 거리들[i] <= 닿는_거리:
            점수 = 점수 + 1
    return 이긴_팀, 점수

# ===== 3. 아래는 경기장 · 스톤 · 마우스 · 화면 코드예요 (읽지 않아도 돼요) =====
과녁 = vector(21.5, 0, 0)            # 과녁 한가운데: 손 떼는 선에서 21.5 m (기본 실습과 같아요)
과녁_반지름, 옆벽 = 1.83, 2.2        # 과녁 반지름, 가운데 선에서 옆 벽까지 (m)
넘을_선 = 과녁.x - 6.4               # 멈췄을 때 이 선을 넘지 못한 스톤은 빠져요
뒷선 = 과녁.x + 과녁_반지름          # 이 선을 완전히 넘어간 스톤은 빠져요
스톤_반지름 = 0.4                    # 잘 보이게 실제(0.145 m)보다 크게 그렸어요
출발_위치 = vector(0, 0, 0)          # 스톤은 손 떼는 선 위에서 출발해요
흰색, 얼음색 = vector(0.97, 0.98, 1), vector(0.93, 0.97, 1)
빨강색, 노랑색 = vector(0.9, 0.12, 0.15), vector(1, 0.78, 0.05)

scene.background = vector(0.78, 0.85, 0.93)
scene.ambient = color.gray(0.5)
scene.userspin, scene.userzoom, scene.userpan = False, False, False   # 마우스로 끌어도 화면이 돌지 않게
distant_light(direction=vector(0.3, -1, -0.5), color=color.gray(0.35))
for x in range(-4, 29, 8):                           # 천장 조명과 등
    local_light(pos=vector(x, 6, 0), color=vector(1, 0.96, 0.88), intensity=0.9)
    box(pos=vector(x, 8, 0), size=vector(2, 0.12, 0.6), color=vector(1, 0.97, 0.85), emissive=True)
local_light(pos=vector(과녁.x, 2.5, 0), color=vector(0.8, 0.88, 1), intensity=0.7)   # 과녁 위 조명

앞끝, 뒤끝 = -6, 뒷선 + 3.5                         # 얼음판의 앞과 뒤 (x)
가운데, 길이 = (앞끝 + 뒤끝) / 2, 뒤끝 - 앞끝
box(pos=vector(가운데, -0.2, 0), size=vector(90, 0.3, 40), color=vector(0.5, 0.56, 0.66))     # 경기장 바닥
box(pos=vector(뒤끝 + 4, 2.8, 0), size=vector(0.4, 6, 30), color=vector(0.2, 0.28, 0.5))      # 뒤쪽 벽
box(pos=vector(뒤끝 + 3.75, 1.6, 0), size=vector(0.1, 0.4, 30), color=vector(0.95, 0.3, 0.35))
box(pos=vector(뒤끝 + 50, 40, 0), size=vector(1, 120, 300), opacity=0)   # 보이지 않는 큰 벽: 손가락이 하늘이나 화면 밖을 가리켜도 위치를 알 수 있게
for z0 in (-6, 0):                                   # 우리 경기장과, 분위기를 내는 옆 경기장
    box(pos=vector(가운데, -0.1, z0), size=vector(길이, 0.2, 2 * 옆벽), texture=textures.ice, color=얼음색, shininess=1)
    for z in (z0 - 옆벽 - 0.1, z0 + 옆벽 + 0.1):
        box(pos=vector(가운데, 0.05, z), size=vector(길이, 0.3, 0.2), color=흰색)            # 옆 벽
    box(pos=vector(뒤끝 + 0.1, 0.05, z0), size=vector(0.2, 0.3, 2 * 옆벽 + 0.4), color=흰색)
    for 층, 반지름, 색 in ((0, 1.83, vector(0.2, 0.45, 0.9)), (1, 1.22, color.white), (2, 0.61, vector(0.9, 0.2, 0.25)), (3, 0.15, color.white)):
        cylinder(pos=vector(과녁.x, 0.002 + 0.003 * 층, z0), axis=vector(0, 0.003, 0), radius=반지름, color=색)
box(pos=vector(가운데, 0.001, 0), size=vector(길이, 0.002, 0.03), color=vector(0.2, 0.2, 0.25))
box(pos=vector(과녁.x, 0.015, 0), size=vector(0.03, 0.004, 2 * 옆벽), color=vector(0.2, 0.2, 0.25))
for z in (-0.25, 0.25):                              # 발판
    box(pos=vector(-1.2, 0.03, z), size=vector(0.3, 0.06, 0.25), color=color.gray(0.15))
옆_글자들 = []                                       # 옆에서 볼 때만 보이는 글자 (선수 시점에서는 숨겨요)
for x, 색, 이름 in ((0, color.red, '손 떼는 선'), (넘을_선, vector(0.85, 0.4, 0.05), '넘어야 하는 선'), (과녁.x, vector(0.2, 0.3, 0.75), '과녁'), (뒷선, vector(0.3, 0.3, 0.35), '뒷선')):
    if 이름 != '과녁':
        box(pos=vector(x, 0.006, 0), size=vector(0.1, 0.012, 2 * 옆벽), color=색)
    옆_글자들.append(label(pos=vector(x, -1.1, 옆벽 + 0.6), text=이름, color=색, height=15, background=color.white))
for m in range(0, 25, 2):                            # 2 m마다 눈금, 4 m마다 숫자
    box(pos=vector(m, 0.01, 옆벽 - 0.15), size=vector(0.04, 0.02, 0.25), color=color.black)
    if m % 4 == 0:
        옆_글자들.append(label(pos=vector(m, -0.5, 옆벽 + 0.6), text=f'{m} m', color=color.black, height=13))

def 스톤_만들기(손잡이색):                           # 화강암 몸통 + 손잡이 (기본 실습과 같은 모양)
    몸통 = cylinder(pos=vector(0, 0.02, 0), axis=vector(0, 0.22, 0), radius=스톤_반지름, texture=textures.granite, color=vector(0.85, 0.85, 0.88))
    띠 = cylinder(pos=vector(0, 0.1, 0), axis=vector(0, 0.04, 0), radius=스톤_반지름 + 0.005, color=vector(0.35, 0.35, 0.4))
    뚜껑 = cylinder(pos=vector(0, 0.24, 0), axis=vector(0, 0.025, 0), radius=스톤_반지름 * 0.84, color=vector(0.55, 0.55, 0.6))
    기둥 = box(pos=vector(0, 0.3, 0), size=vector(0.08, 0.1, 0.08), color=손잡이색)
    손잡이 = box(pos=vector(0, 0.37, 0), size=vector(0.56, 0.07, 0.12), color=손잡이색)
    return compound([몸통, 띠, 뚜껑, 기둥, 손잡이])

팀들 = ['빨강' if i % 2 == 0 else '노랑' for i in range(16)]          # 빨강 · 노랑을 번갈아 8개씩 만들어 둬요
스톤들 = [스톤_만들기(빨강색 if 팀 == '빨강' else 노랑색) for 팀 in 팀들]
위치들, 속도들, 상태들 = [vector(0, 0, 0)] * 16, [vector(0, 0, 0)] * 16, ['대기'] * 16   # 스톤마다 한 칸 (상태: '대기' · '경기' · '빠짐')
스톤_높이 = 스톤들[0].pos.y
화살표 = arrow(pos=vector(0, 0.6, 0), axis=vector(0.01, 0, 0), shaftwidth=0.12, color=vector(1, 0.5, 0.1), visible=False)
빠르기_글자 = label(pos=vector(0, 1.2, 0), text='', color=color.black, height=17, background=color.white, visible=False)
빗자루 = compound([box(pos=vector(0, 0.05, 0), size=vector(0.22, 0.1, 0.95), color=vector(0.1, 0.35, 0.95)),
                   cylinder(pos=vector(0, 0.1, 0), axis=vector(-0.7, 1.4, 0), radius=0.04, color=vector(0.95, 0.75, 0.2))], visible=False)
빗자루_차이 = 빗자루.pos - vector(0, 0.05, 0)        # 솔 가운데에서 빗자루 중심까지
자국들, 점들, 점수_글자들, 자취_시각, 자취_위치, 문지름 = [], [], [], [], [], []
차례, 단계, 시점, 카메라_x, 알림, 빠진_글 = 0, '준비', '옆', 4, '', ''
눈_방향 = (vector(1, 0, 0), vector(0, 0, -1))         # 화면 오른쪽 · 위쪽이 얼음에서 가리키는 방향
잡은_손 = vector(0, 0, 0)
놓은_위치, 놓은_빠르기, 걸음, 비질_시간, 자국_수, 지난_자국, 멈춘_시각 = vector(0, 0, 0), 0, 0, 0, 0, vector(0, 0, 0), 0

def 지금_점수():
    팀, 거리 = [], []
    for i in range(16):
        if 상태들[i] == '경기':
            팀.append(팀들[i])
            거리.append(mag(위치들[i] - 과녁))
    return 점수_계산(팀, 거리, 과녁_반지름 + 스톤_반지름)

def 판_쓰기():                                       # 화면 왼쪽 위 점수판
    팀, 점 = 지금_점수()
    if 단계 == '끝':
        첫줄 = f'경기 끝! {팀} 팀이 {점}점을 얻었어요' if 점 > 0 else '경기 끝! 0 : 0 (점수 없음)'
    else:
        첫줄 = f'차례: {팀들[차례]} 팀 ({차례 // 2 + 1}번째 스톤)'
    남음 = f'남은 스톤: 빨강 {상태들[0:2 * 팀마다_스톤:2].count("대기")} · 노랑 {상태들[1:2 * 팀마다_스톤:2].count("대기")}'
    scene.title = f'{첫줄}\n{남음}\n지금 과녁: ' + (f'{팀} {점}점' if 점 > 0 else '0 : 0') + f'\n{알림}{빠진_글}'

def 카메라_두기():
    if 시점 == '옆':
        scene.center = vector(카메라_x, 0, 0)
    else:
        높이 = 3.2 + 2.8 * max(0, min(1, (카메라_x - 4) / (과녁.x - 4)))   # 과녁에 다가갈수록 높이 올라가요
        눈 = vector(카메라_x - 13, 높이, 0)          # 스톤 뒤에서 과녁 쪽을 봐요
        scene.camera.pos = 눈
        scene.camera.axis = 과녁 + vector(1, 0, 0) - 눈

def 시점_맞추기():
    if 시점 == '옆':
        scene.fov, scene.forward, scene.range = pi / 3, vector(0, -0.6, -1), 6
    else:
        scene.fov = pi / 4.5                         # 선수 시점은 망원 렌즈처럼 좁게 봐요
    카메라_두기()

def 시점_바꾸기(b):
    global 시점
    시점 = '선수' if 시점 == '옆' else '옆'
    b.text = '옆에서 보기' if 시점 == '선수' else '선수 시점으로 보기'
    for 글자 in 옆_글자들:
        글자.visible = 시점 == '옆'
    시점_맞추기()

def 준비():                                          # 다음 스톤을 손 떼는 선 위에 놓아요
    global 단계, 카메라_x
    위치들[차례], 단계, 카메라_x = 출발_위치, '준비', 4
    빠르기_글자.pos, 빠르기_글자.visible = 출발_위치 + vector(0, 1.2, 0), 차례 < 2   # 팀마다 첫 스톤에는 안내를 띄워요
    빠르기_글자.text = '스톤을 잡고 과녁 쪽으로\n끌다가 놓아요'
    시점_맞추기()
    판_쓰기()

def 새_경기(b=None):
    global 팀마다_스톤, 차례, 알림, 빠진_글, 자국_수
    팀마다_스톤 = 스톤_수_메뉴.index + 1
    for i in range(16):                              # 아직 안 던진 스톤은 경기장 옆에 줄 세워요
        위치들[i] = vector(-2 - (i // 2) * 0.95, -0.05, (옆벽 + 0.8) * (1 if i % 2 == 0 else -1))
        속도들[i], 상태들[i] = vector(0, 0, 0), '대기'
        스톤들[i].visible = i < 2 * 팀마다_스톤
    for 것 in 점들 + 점수_글자들 + 자국들:
        것.visible = False
    점들.clear()
    점수_글자들.clear()
    차례, 알림, 빠진_글, 자국_수 = 0, '', '', 0
    준비()

def 스톤_수_바꾸기(s):
    global 알림
    if 차례 == 0 and 단계 == '준비':
        새_경기()
    else:
        알림 = f'팀마다 스톤 {s.index + 1}개는 [새 경기]부터예요'
        판_쓰기()

def 화면_방향():                                     # 카메라가 보는 방향, 화면의 오른쪽과 위쪽 방향
    앞 = hat(scene.camera.axis)
    오른쪽 = hat(cross(앞, vector(0, 1, 0)))
    return 앞, 오른쪽, cross(오른쪽, 앞)

def 화면_좌표(점):                                   # 3D 점이 화면 어디에 보이는지 (화면 높이를 1로 잰 값)
    앞, 오른쪽, 위 = 화면_방향()
    d = 점 - scene.camera.pos
    높이 = 2 * tan(scene.fov / 2) * dot(d, 앞)       # 그 점의 깊이에서 화면 높이
    return vector(dot(d, 오른쪽) / 높이, dot(d, 위) / 높이, 0)

def 던질_속도():                                     # 마지막 0.1초 동안 손이 간 거리 ÷ 걸린 시간
    if len(자취_시각) < 2 or clock() - 자취_시각[-1] > 0.08:
        return vector(0, 0, 0)                       # 손(손가락)이 멈춰 있어요
    처음 = len(자취_시각) - 2
    while 처음 > 0 and 자취_시각[-1] - 자취_시각[처음] < 0.1:
        처음 = 처음 - 1
    화면_속도 = (자취_위치[-1] - 자취_위치[처음]) / (자취_시각[-1] - 자취_시각[처음])
    속도 = 손_배율 * (화면_속도.x * 눈_방향[0] + 화면_속도.y * 눈_방향[1])   # 화면 방향을 얼음 방향으로
    if mag(속도) > 최대_빠르기:
        속도 = 최대_빠르기 * hat(속도)
    return 속도

def 누름(e):                                         # 스톤 가까이를 누르면 잡아요 (손가락도 잡기 쉽게 넉넉히)
    global 단계, 눈_방향, 잡은_손
    if 단계 == '준비' and mag(vector(e.pos.x, 0, e.pos.z) - 위치들[차례]) < 1.8:
        앞, 오른쪽, 위 = 화면_방향()
        단계, 눈_방향 = '잡는 중', (오른쪽, hat(vector(위.x, 0, 위.z)))   # 화면 오른쪽·위쪽 = 얼음의 이 방향
        잡은_손 = scene.mouse.pos                     # 손가락은 누르기 전 위치가 남아 있으니, 바뀔 때까지 쓰지 않아요
        자취_시각[:] = [clock()]
        자취_위치[:] = [화면_좌표(e.pos)]               # 누른 곳에서 자취를 시작해요

def 뗌(e):
    if 단계 == '잡는 중':
        스톤_놓기()

def 스톤_놓기():                                     # 손을 떼는 순간: 그때의 손 속도로 출발해요
    global 단계, 알림, 빠진_글, 놓은_위치, 놓은_빠르기, 걸음, 비질_시간, 자국_수, 지난_자국
    속도 = 던질_속도()
    화살표.visible = False
    if 속도.x < 0.3:
        알림 = '과녁 쪽으로 끌다가 놓아 보세요'
        빠르기_글자.visible = False
        준비()
        return
    for 것 in 점들 + 자국들:
        것.visible = False
    점들.clear()
    문지름.clear()
    속도들[차례], 상태들[차례], 단계 = 속도, '경기', '달리는 중'
    놓은_위치, 놓은_빠르기, 걸음, 비질_시간, 자국_수, 지난_자국 = 위치들[차례], mag(속도), 0, 0, 0, vector(-99, 0, 0)
    알림, 빠진_글 = f'놓은 빠르기 {mag(속도):.1f} m/s', ''
    play_sound(520, 0.08, 'sine', 0.2)
    판_쓰기()

def 빼기(i, 까닭):                                   # 경기에서 빠진 스톤은 치워요
    global 빠진_글
    상태들[i], 속도들[i] = '빠짐', vector(0, 0, 0)
    스톤들[i].visible = False
    빠진_글 = 빠진_글 + f'\n{팀들[i]} 스톤이 {까닭} 빠졌어요'
    print(f'  {팀들[i]} 스톤이 {까닭} 빠졌어요')
    play_sound(140, 0.25, 'sawtooth', 0.15)
    판_쓰기()

def 앞_스톤():                                       # 움직이는 스톤 가운데 가장 앞에 있는 것 (없으면 -1)
    앞 = -1
    for i in range(16):
        if 상태들[i] == '경기' and mag(속도들[i]) > 0 and (앞 < 0 or 위치들[i].x > 위치들[앞].x):
            앞 = i
    return 앞

def 문지르는_중(앞):                                 # 최근 0.3초 동안 스톤 앞에서 손이 화면 위를 오간 길이로 알아봐요
    if 앞 < 0:
        return False
    스톤 = 화면_좌표(위치들[앞])
    문지름.append(화면_좌표(scene.mouse.pos) - 스톤)     # 화면에서 스톤을 기준으로 본 손의 위치
    if len(문지름) > 18:
        문지름.pop(0)
    길 = 0
    for k in range(1, len(문지름)):
        길 = 길 + mag(문지름[k] - 문지름[k - 1])
    오간_길 = 길 - mag(문지름[-1] - 문지름[0])        # 한쪽으로 쭉 움직인 만큼은 빼요
    앞쪽 = 화면_좌표(위치들[앞] + hat(속도들[앞])) - 스톤   # 화면에서 스톤 1 m 앞
    return 오간_길 > 0.12 and mag(문지름[-1] - 앞쪽) < 0.22   # 스톤 앞에서 화면 높이의 0.12배 넘게 오갔나요?

def 자국_놓기(위치):                                 # 비질로 닦인 자국 (쓴 자국은 다시 써요)
    global 자국_수
    if 자국_수 == len(자국들):
        자국들.append(box(size=vector(0.34, 0.003, 0.8), color=vector(0.5, 0.78, 1), opacity=0.7))
    자국들[자국_수].pos, 자국들[자국_수].visible = 위치 + vector(0, 0.02, 0), True
    자국_수 = 자국_수 + 1

def 멈춤():                                          # 모든 스톤이 멈추면
    global 단계, 멈춘_시각, 알림
    빠르기_글자.visible = 빗자루.visible = False
    if 상태들[차례] == '경기' and 위치들[차례].x < 넘을_선:
        빼기(차례, '넘어야 하는 선을 못 넘어')
    거리 = mag(위치들[차례] - 놓은_위치)
    print(f'{차례 + 1}번째 스톤({팀들[차례]}): 놓은 빠르기 {놓은_빠르기:.2f} m/s, 미끄러진 거리 {거리:.2f} m, 비질 {비질_시간:.1f}초')
    알림 = f'놓은 빠르기 {놓은_빠르기:.1f} m/s → {거리:.1f} m 미끄러졌어요'
    단계, 멈춘_시각 = '보는 중', clock()
    판_쓰기()

def 경기_끝():
    global 단계
    단계 = '끝'
    팀, 점 = 지금_점수()
    순서 = sorted([i for i in range(16) if 상태들[i] == '경기' and 팀들[i] == 팀], key=lambda i: mag(위치들[i] - 과녁))
    for i in 순서[:점]:                              # 점수가 된 스톤 위에 표시해요
        점수_글자들.append(label(pos=위치들[i] + vector(0, 1, 0), text='1점', color=color.black, height=16, background=color.white))
    판_쓰기()
    play_sound(784, 0.3, 'sine', 0.3)

button(text='새 경기', bind=새_경기)
button(text='선수 시점으로 보기', bind=시점_바꾸기)
스톤_수_메뉴 = menu(choices=[f'팀마다 스톤 {k}개' for k in range(1, 9)], selected=f'팀마다 스톤 {팀마다_스톤}개', bind=스톤_수_바꾸기)
scene.caption = '끌다가 놓으면 던지기 · 달리는 스톤 앞을 문지르면 비질 (Space 키도 돼요)'
scene.bind('mousedown', 누름)
scene.bind('mouseup', 뗌)
새_경기()

초당_걸음 = round(1 / 시간간격)                      # 1초에 몇 걸음인지 (지금은 600)
while True:
    rate(240 if 단계 == '잡는 중' else 60)           # 스톤을 잡고 있는 동안은 손을 더 자주 살펴요
    목표_x = 4
    if 단계 == '잡는 중':
        손 = 화면_좌표(scene.mouse.pos)
        if scene.mouse.pos != 잡은_손 and 손 != 자취_위치[-1]:
            자취_시각.append(clock())
            자취_위치.append(손)
        if len(자취_위치) > 40:
            자취_시각.pop(0)
            자취_위치.pop(0)
        속도 = 던질_속도()
        화살표.pos, 화살표.axis, 화살표.visible = 출발_위치 + vector(0, 0.6, 0), 0.8 * 속도 + vector(0.01, 0, 0), True
        새_글 = f'{mag(속도):.1f} m/s'
        if 빠르기_글자.text != 새_글:
            빠르기_글자.pos, 빠르기_글자.text, 빠르기_글자.visible = 출발_위치 + vector(0, 1.2, 0), 새_글, True
    elif 단계 == '달리는 중':
        앞 = 앞_스톤()
        손 = scene.mouse.project(normal=vector(0, 1, 0))   # 마우스가 가리키는 얼음 위의 점 (빗자루를 그릴 곳)
        문지름_중 = 문지르는_중(앞)
        비질_중 = 문지름_중 or ' ' in keysdown()     # 마우스로 문지르거나 Space 키를 누르고 있으면 비질
        for k in range(초당_걸음 // 60):             # 화면을 다시 그리는 사이(1/60초)의 걸음
            for i in range(16):
                if 상태들[i] == '경기' and mag(속도들[i]) > 0:
                    방해 = 비질한_빠르기 if 비질_중 and i == 앞 else 줄어드는_빠르기   # 비질은 가장 앞 스톤 앞만 닦아요
                    속도들[i], 위치들[i] = 한_걸음(속도들[i], 위치들[i], 방해)
                    for j in range(16):
                        if j != i and 상태들[j] == '경기':
                            부딪히기(i, j)
                    if abs(위치들[i].z) + 스톤_반지름 > 옆벽:
                        빼기(i, '옆 벽에 닿아')
                    elif 위치들[i].x - 스톤_반지름 > 뒷선:
                        빼기(i, '뒷선을 넘어가')
            걸음 = 걸음 + 1
            if 걸음 % 초당_걸음 == 0 and 상태들[차례] == '경기' and mag(속도들[차례]) > 0:   # 1초마다 점 하나
                점들.append(sphere(pos=위치들[차례] + vector(0, 0.03, 0), radius=0.09, color=color.blue))
                play_sound(660, 0.06, 'sine', 0.15)
        앞 = 앞_스톤()
        if 앞 >= 0:
            if 비질_중:
                비질_시간 = 비질_시간 + 1 / 60
                솔_위치 = 위치들[앞] + (스톤_반지름 + 0.35) * hat(속도들[앞])   # 스톤 바로 앞
                빗자루.pos = (손 if 문지름_중 and 손 is not None else 솔_위치 + vector(0, 0, 0.3 * sin(clock() * 30))) + 빗자루_차이
                if mag(솔_위치 - 지난_자국) > 0.3:
                    자국_놓기(솔_위치)
                    지난_자국 = 솔_위치
            빗자루.visible = 비질_중
            목표_x = max(4, min(위치들[앞].x + 2, 과녁.x))
            빠르기_글자.pos = 위치들[앞] + vector(0, 1.2, 0)
            빠르기_글자.text = f'{mag(속도들[앞]):.1f} m/s' + ('  비질 중!' if 비질_중 else '\n앞을 문지르면 비질' if 차례 < 2 else '')
        else:
            멈춤()
    elif 단계 == '보는 중' and clock() - 멈춘_시각 > 2:
        차례 = 차례 + 1
        if 차례 < 2 * 팀마다_스톤:
            준비()
        else:
            경기_끝()
    if 단계 in ('보는 중', '끝'):
        목표_x = 과녁.x
    if abs(목표_x - 카메라_x) > 0.01:                # 화면이 스톤을 부드럽게 따라가요
        카메라_x = 카메라_x + (목표_x - 카메라_x) * 0.08
        카메라_두기()
    for i in range(16):                              # 계산한 위치로 스톤을 옮겨요 (미끄러지며 천천히 돌아요)
        새 = 위치들[i] + vector(0, 스톤_높이, 0)
        if 스톤들[i].pos != 새:
            스톤들[i].rotate(angle=-0.3 * mag(새 - 스톤들[i].pos), axis=vector(0, 1, 0))
            스톤들[i].pos = 새
