# main.py의 점수 규칙(점수_계산)과 미끄러지기 법칙(한_걸음)을 보통 파이썬으로 시험해요.
# VPyLab에서는 쓰지 않는 파일이에요. 실행: python3 test_score.py
import ast
import pathlib

소스 = (pathlib.Path(__file__).parent / 'main.py').read_text(encoding='utf-8')
함수들 = [n for n in ast.parse(소스).body if isinstance(n, ast.FunctionDef) and n.name in ('점수_계산', '한_걸음')]


class 벡터:                                          # 시험용으로 아주 작게 만든 벡터 (x, z만)
    def __init__(self, x, z):
        self.x, self.z = x, z
    def __add__(self, o):
        return 벡터(self.x + o.x, self.z + o.z)
    def __mul__(self, k):
        return 벡터(self.x * k, self.z * k)
    __rmul__ = __mul__


def mag(v):
    return (v.x ** 2 + v.z ** 2) ** 0.5


def hat(v):
    m = mag(v)
    return 벡터(0, 0) if m == 0 else 벡터(v.x / m, v.z / m)


공간 = {'mag': mag, 'hat': hat, '시간간격': 1 / 600}
exec(compile(ast.Module(body=함수들, type_ignores=[]), 'main.py', 'exec'), 공간)
점수_계산, 한_걸음 = 공간['점수_계산'], 공간['한_걸음']
닿음 = 1.83 + 0.4                                    # 과녁 반지름 + 스톤 반지름

# 1) 점수: 과녁에 닿은 스톤만, 가장 가까운 팀이 상대의 가장 가까운 스톤보다 가까운 수만큼
assert 점수_계산([], [], 닿음) == ('', 0)                                        # 스톤이 없어요
assert 점수_계산(['빨강', '노랑'], [3.0, 2.5], 닿음) == ('', 0)                  # 둘 다 과녁 밖
assert 점수_계산(['빨강'], [0.5], 닿음) == ('빨강', 1)
assert 점수_계산(['빨강', '빨강', '노랑'], [0.3, 0.9, 0.6], 닿음) == ('빨강', 1)  # 노랑(0.6)보다 가까운 빨강은 1개
assert 점수_계산(['빨강', '빨강', '빨강', '노랑'], [0.3, 0.5, 2.0, 1.0], 닿음) == ('빨강', 2)
assert 점수_계산(['노랑', '노랑', '빨강'], [0.2, 2.1, 2.5], 닿음) == ('노랑', 2)  # 빨강은 과녁 밖이라 노랑 둘 다 1점
assert 점수_계산(['빨강', '노랑'], [1.0, 1.0], 닿음) == ('', 0)                  # 똑같이 가까우면 0점
assert 점수_계산(['노랑', '빨강', '노랑'], [2.23, 2.24, 5.0], 닿음) == ('노랑', 1)  # 테두리에 걸친 스톤도 세요

# 2) 법칙: 얼음(1초에 1 m/s씩 줄어듦)에서 4 m/s로 놓으면 v²/(2a) = 8 m쯤에서 멈춰요
def 멈춘_거리(빠르기, 줄어드는_빠르기):
    속도, 위치 = 벡터(빠르기, 0), 벡터(0, 0)
    while mag(속도) > 0:
        속도, 위치 = 한_걸음(속도, 위치, 줄어드는_빠르기)
    return 위치.x

assert abs(멈춘_거리(4, 1) - 8) < 0.01
assert abs(멈춘_거리(6.6, 1) - 6.6 ** 2 / 2) < 0.01          # 과녁 한가운데(21.5 m) 근처
assert abs(멈춘_거리(4, 0.5) - 16) < 0.01                    # 비질하면 두 배
print('모든 시험 통과: 4 m/s → %.4f m, 6.6 m/s → %.3f m' % (멈춘_거리(4, 1), 멈춘_거리(6.6, 1)))
