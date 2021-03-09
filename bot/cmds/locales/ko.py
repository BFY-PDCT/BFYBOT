"""
    Copyright (C) 2021 BFY Entertainment
    All right reserved

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

if __name__ == "__main__":
    import sys

    print("Please execute bot.py")
    sys.exit(0)

locale_ko = {
    "dictcmd_error_notadmin": "관리자 아니면 안해줄건뎅",
    "dictcmd_error_err": "오류가 있었어요.. :( 자동으로 리포트가 생성되었어요",
    "dictcmd_checka_delete": "지워",
    "dictcmd_checkb_yes": "어",
    "dictcmd_checkb_no": "아니",
    "dictcmd_checkd_report": "신고",
    "dictcmd_checkd_change": "바꿔",
    "dictcmd_general_deleted": "지웠읍니다",
    "dictcmd_general_reqedit": "바꿔",
    "dictcmd_general_rejedit": "이건 못바꿔줘",
    "dictcmd_general_cfmedit": "100000포인트를 사용해서 대답을 바꿔줄래?",
    "dictcmd_general_yes": "어",
    "dictcmd_general_no": "아니",
    "dictcmd_general_editing": "누군가 수정중인것 같아요 ;)",
    "dictcmd_general_using": "이미 사용중이에요 ;)",
    "dictcmd_general_question": "머라고할건데",
    "dictcmd_general_emptyerr": "빈 메시지는 등록할 수 없어요 ^^",
    "dictcmd_general_limiterr": "100자까지만 등록할 수 있어요 ^^",
    "dictcmd_general_acpedit": "ㅇㅋ `💰-100000`",
    "dictcmd_general_cancel": "ㅇㅋ 싫음말고",
    "dictcmd_general_npntedit": "100000포인트 벌고와",
    "dictcmd_report_title": "새 신고",
    "dictcmd_report_cmd": "질문",
    "dictcmd_report_reply": "답변",
    "dictcmd_report_reason": "사유",
    "dictcmd_report_author": "작성자",
    "dictcmd_report_reported": "해당 답변을 신고하였습니다. 신고된 답변은 관리자가 검토 후 조치할 예정입니다.",
    "dictcmd_general_ownercfmnew": "주인님 새 명령어가 필요하십니까",
    "dictcmd_general_cfmnew": "50000포인트를 사용해서 대답을 알려줄래?",
    "dictcmd_general_cancel": "뭐래 ㅋ",
    "dictcmd_general_ownerquestion": "주인님 무엇을 원하십니까.",
    "dictcmd_general_owneracpnew": "주인님 등록하였읍니다.",
    "dictcmd_general_ownercancel": "알겠습니다 주인님",
    "dictcmd_general_acpnew": "ㅇㅋ `💰-50000`",
    "economy_seemoney_0": "{0} 니가 가진 돈은 이만큼이다 알았나 `💰 {1}`",
    "economy_getmoney_1": " 형님",
    "economy_getmoney_2": "어휴 불쌍한넘 내가 특별히 1000포인트 준다 `💰+1000`",
    "economy_getmoney_3": "싫은뒈~~에베ㅔㅔ",
    "economy_getmoney_4": "뭐래 ㅋㅋ",
    "economy_getmoney_5": "가져가서 어디 써보시던가 ㅋㅋ `💰+100`",
    "economy_getmoney_6": " 형님 해봐",
    "economy_getmoney_7": "자존심만 높아서는 ㅉㅉ",
    "economy_getmoney_8": "옳지 잘한다 옛다 선물 `💰+2500`",
    "economy_getmoney_9": "내가 니한테 돈을 왜주냐?",
    "economy_getmoney_10": "ㄲㅈ",
    "economy_seeothermoney_0": "죄송합니다 대상자를 멘션해주세요.",
    "economy_seeothermoney_1": "죄송합니다 1명의 대상자만을 멘션해주세요.",
    "economy_seeothermoney_2": "{} 이 친구가 가진 돈은 이만큼이다 알았나 `💰 {1}`",
    "economy_seestk_0": "{0} 니가 가진 주식은 이만큼이다 A: {1}주 / B: {2}주 / C: {3}주",
    "economy_seeotherstk_0": "죄송합니다 대상자를 멘션해주세요.",
    "economy_seeotherstk_1": "죄송합니다 1명의 대상자만을 멘션해주세요.",
    "economy_seeotherstk_2": "{0} 이 친구가 가진 주식은 이만큼이다 A: {1}주 / B: {2}주 / C: {3}주",
    "economy_sendmoney_0": "선물할 수 없는 금액입니다.",
    "economy_sendmoney_1": "대상자를 멘션해주세요.",
    "economy_sendmoney_2": "1명의 대상자만을 멘션해주세요.",
    "economy_sendmoney_3": "{0}님에게 `💰 {1}`을(를) 선물했습니다.",
    "economy_sendmoneyerror_0": "금액을 올바르게 입력해주세요.",
    "economy_sendmoneyerror_1": "뭔가 잘못 입력하신것 같아요,,",
    "economy_sendmoneyerror_2": "오류가 있었어요.. :( 자동으로 리포트가 생성되었어요",
    "game_gamble_0": "돈도없으면서 도박같은 소리하네",
    "game_gamble_1": "얼마걸건데? 잔액: `💰 {0}`",
    "game_gamble_2": "안할거면 ㄲㅈ",
    "game_gamble_3": "{0}포인트로 게임을 시작하지",
    "game_gamble_4": "돈도없으면서 도박같은 소리하네",
    "game_gamble_5": "제대로 된 숫자를 좀 주시죠?",
    "game_gamble_6": "꿀--꺼억 `💰-{0}`",
    "game_gamble_7": "0.5배 다먹기엔 배불러 ㅋㅋ `💰-{0}`",
    "game_gamble_8": "꿀--꺼억하려다 참았다... 후... `💰+0`",
    "game_gamble_9": "2배... 나쁘지 않지? `💰+{0}`",
    "game_gamble_10": "올 4배 ㅊㅊ `💰+{0}`",
    "game_gamble_11": "이야 이걸 6배로 가져가네 `💰+{0}`",
    "game_gamble_12": "8배면 와... `💰+{0}`",
    "game_gamble_13": "10배라니 너 운 좀 좋다? `💰+{0}`",
    "game_gamble_14": "뭔 나 거지되겠네 50배는 너무한거아니냐 `💰+{0}`",
    "game_stock_0": "`{0} 주식 (그래프|매수|매도|통계) (A|B|C|ENT|CORP|AT7)` 이 올바른 사용법이에요 ^^",
    "game_stock_1": "현재 가격: {0}",
    "game_stock_2": "{0}의 그래프입니다.",
    "game_stock_3": "돈도없으면서 주식같은 소리하네",
    "game_stock_4": "얼마나 구매하시겠어요? 잔액: `💰 {0}`, 현재가격: {1}, 구매가능수량: {2}주",
    "game_stock_5": "안살거면 가세요",
    "game_stock_6": "정확한 수량을 입력하십쇼",
    "game_stock_7": "주식 최대 보유량은 10만주입니다.",
    "game_stock_8": "{0}주를 구매하셨습니다. `💰-{1}`",
    "game_stock_9": "주식도 없으면서 매도같은 소리하네",
    "game_stock_10": "얼마나 판매하시겠어요? 현재가격: {0}, 판매가능수량: {1}주",
    "game_stock_11": "안팔거면 가세요",
    "game_stock_12": "{0}주를 판매하셨습니다. `💰+{1}`",
    "game_stock_13": "거래내역을 못찾았어요 ㅎㅎ;",
    "game_stock_14": "매수",
    "game_stock_15": "매도",
    "game_stock_16": "{0} - {1}포인트 - {2}주 - 총 {3}포인트",
    "game_stock_17": "{0} 주식 거래내역입니다.",
    "general_version_0": "{0} 버전",
    "general_version_1": "현재 버전",
    "general_version_2": "discord.py 버전",
    "general_version_3": "제작자",
    "general_version_4": "서버 상태 확인",
    "general_version_5": "{0}의 음악 기능",
    "general_version_6": "{0} 버전 정보입니다",
    "general_help_0": "{0} 사용 방법",
    "general_help_1": "도움말 (온라인)",
    "general_help_2": "음악 도움말",
    "general_help_3": "문의",
    "general_help_4": "봇에게 DM을 보내주시면 메시지가 운영자에게 전달됩니다.\n홈페이지: https://www.bfy.kr/ 개발자이메일: jhlee@bfy.kr\n개발자 디스코드: KRMSS#9279",
    "general_help_5": "점검 안내 수신하기",
    "general_help_6": "{0}의 관리자이시군요! `{1} 구독 #채널` 명령어를 통해 점검 등의 공지사항을 받으시는 것을 추천드립니다!",
    "general_help_7": "{0}한테 명령하는 방법입니다",
    "general_help_8": "도움말 전송에 실패했어요 :( DM이 차단된건 아닌지 확인해주세요!",
    "general_docalculate_0": "계산 결과는 {0}입니다! (이상하면 너가 이상한식 넣은거임)",
    "general_docalculateerror_0": "계산할 식을 입력해주세요.",
    "manage_error_0": "모든 항목을 입력해주세요.",
    "manage_error_1": "관리자가 아니면 못써요 흥",
    "manage_error_2": "뭔가 잘못 입력하신것 같아요,,",
    "manage_error_3": "오류가 있었어요.. :( 자동으로 리포트가 생성되었어요",
    "manage_error_4": "죄송합니다 {0}을(를) 멘션해주세요",
    "manage_error_5": "구독 설정에 오류가 있습니다. 수정해주세요.",
    "manage_error_6": "권한도 없으면서 나대긴 ㅋ",
    "manage_cfrm": "넵^^7",
    "manage_delwelcome_0": "일단 설정하고 말씀하시죠?",
    "manage_delwelcome_1": "환영인사는 이제 없습니다.",
    "manage_delbye_0": "일단 설정하고 말씀하시죠?",
    "manage_delbye_1": "작별인사는 이제 없습니다.",
    "manage_unsubscribe_0": "구독하지도 않아놓고는 ㅋㅋ",
    "manage_unsubscribe_1": "구독해제되었어요 힝 ㅠㅠ",
    "manage_deldefaultrole_0": "기본 역할이 설정되지 않았습니다.",
    "manage_cleanchat_0": "권한도 없으면서 나대긴 ㅋ",
    "manage_cleanchat_1": "얼마나 치울지를 알려줘야 치우던가하지",
    "manage_cleanchat_2": "숫자가 아닌걸 주시면 어쩌자는겁니까?",
    "manage_cleanchat_3": "정상적인 숫자를 좀 주시죠?",
    "manage_cleanchat_4": "너무 많어 200개이상은 안치움 ㅅㄱ",
    "manage_cleanchat_5": "{0}개 치웠어용 히히 칭찬해조",
    "manage_setpunish_0": "경고는 최대 10개까지에요.",
    "manage_setpunish_1": "경고는 최소 1개부터에요.",
    "manage_setpunish_2": "뮤트",
    "manage_setpunish_3": "킥",
    "manage_setpunish_4": "밴",
    "manage_setpunish_5": "삭제",
    "manage_setpunish_6": "뮤트, 킥, 밴, 삭제 중에서만 선택 가능해요.",
    "manage_setpunish_7": "설정이 되어있지 않습니다.",
    "manage_setpunish_8": "모든 항목을 입력해주세요.",
    "manage_delguildadmin_0": "{0} 넌이제 내 주인이 아니다 ㅋㅋㅋㅋㅋㅋㅋㅋ",
    "manage_delguildadmin_1": "누구세요?",
    "manage_delguildadmin_2": "이게 서버주인을 건드리네?",
    "manage_delguildadmin_3": "이게 아버지를 건드리네?",
    "manage_addguildadmin_4": "작업완료 ^^7 환영합니다 {0} 주인님!",
    "manage_addguildadmin_5": "이미 주인님이십니다.",
    "manage_execmute_0": "죄송합니다 역할을 지정해주세요.",
    "manage_execmute_1": "죄송합니다 역할이 잘못 지정되어 있습니다.",
    "manage_execmute_2": "죄송합니다 권한이 부족합니다.",
    "manage_execmute_3": "이미 뮤트처리된 사용자입니다.",
    "manage_execmute_4": "처리 완료되었습니다 - 뮤트 {0} / 이유: {1} / 처리자: {2}",
    "manage_execkick_0": "문제가 있었어요,, 관리자한테 문의해주세요 ㅠㅠ",
    "manage_execkick_1": "문제가 있었어요,, 아마 뮤트를 한적이 없는거 아닐까요..?",
    "manage_execkick_2": "처리 완료되었습니다 - 킥 {0} / 이유: {1} / 처리자: {2}",
    "manage_execban_0": "문제가 있었어요,, 관리자한테 문의해주세요 ㅠㅠ",
    "manage_execban_1": "문제가 있었어요,, 아마 뮤트를 한적이 없는거 아닐까요..?",
    "manage_execban_2": "처리 완료되었습니다 - 밴 {0} / 이유: {1} / 처리자: {2}",
    "manage_delwarning_0": "경고가 없습니다.",
    "manage_delwarning_1": "넵^^7 (누적 경고수: {0})",
    "manage_getpunishlist_0": "경고 {0}회시 뮤트 {1}초",
    "manage_getpunishlist_1": "경고 {0}회시 킥",
    "manage_getpunishlist_2": "경고 {0}회시 밴",
    "manage_getpunishlist_3": "처벌 정책이 없습니다",
    "manage_getpunishlist_4": "서버의 처벌 정책입니다.",
    "manage_seewarning_0": "{0} 님의 현재 누적 경고 수는 {1}회 입니다.",
    "privatecmd_": "",
    "update_0": "처리 종료되었습니다 - 뮤트 {0} / 처리자: {1}",
    "update_1": "처리 종료되었습니다 - 뮤트 {0}",
    "update_2": "구독 설정에 오류가 있습니다. 수정해주세요.",
    "events_0": "{0}님이 참가했어요",
    "events_1": "새 멤버 역할이 잘못 지정되어 있습니다.",
    "events_2": "새 멤버 역할 변경 권한이 부족합니다.",
    "events_3": "{0}님이 떠났어요",
    "private_": "",
}
