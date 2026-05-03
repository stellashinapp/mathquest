# 초등학교 수학문제 어플리케이션
# Elementary School Math Problems Application

import random
from typing import List, Dict, Tuple

class GameState:
    """게임 상태 관리"""
    
    def __init__(self):
        self.total_points = 0
        self.total_correct = 0
        self.total_problems = 0
        self.current_combo = 0
        self.max_combo = 0
        self.badges = []
        self.level = 1
    
    def add_points(self, points: int, combo_bonus: int = 1):
        """포인트 추가"""
        total_points = points * combo_bonus
        self.total_points += total_points
        return total_points
    
    def add_combo(self):
        """콤보 증가"""
        self.current_combo += 1
        if self.current_combo > self.max_combo:
            self.max_combo = self.current_combo
    
    def reset_combo(self):
        """콤보 리셋"""
        self.current_combo = 0
    
    def update_level(self):
        """레벨 업데이트"""
        self.level = (self.total_correct // 10) + 1
    
    def add_badge(self, badge_name: str):
        """뱃지 추가"""
        if badge_name not in self.badges:
            self.badges.append(badge_name)
    
    def get_level_name(self) -> str:
        """레벨 이름 반환"""
        if self.level <= 2:
            return "🌱 초보자"
        elif self.level <= 4:
            return "🌿 성장 중"
        elif self.level <= 6:
            return "🌳 전문가"
        elif self.level <= 8:
            return "🏆 마스터"
        else:
            return "👑 전설의 수학자"


class MathProblems:
    """초등학교 1-6학년 수학문제"""
    
    def __init__(self):
        self.problems = {
            1: self.grade_1_problems(),
            2: self.grade_2_problems(),
            3: self.grade_3_problems(),
            4: self.grade_4_problems(),
            5: self.grade_5_problems(),
            6: self.grade_6_problems(),
        }
        self.units_config = {
            1: ["덧셈", "뺄셈", "혼합"],
            2: ["덧셈", "뺄셈", "곱셈", "시간"],
            3: ["덧셈/뺄셈", "곱셈/나눗셈", "도형"],
            4: ["큰수", "분수", "소수"],
            5: ["소수", "분수", "도형"],
            6: ["분수계산", "소수/비율", "도형"],
        }
    
    def grade_1_problems(self):
        """1학년: 기초 덧셈과 뺄셈"""
        all_problems = {
            "덧셈": [
                {"problem": "2 + 1 = ?", "answer": 3, "type": "수식"},
                {"problem": "3 + 2 = ?", "answer": 5, "type": "수식"},
                {"problem": "1 + 4 = ?", "answer": 5, "type": "수식"},
                {"problem": "4 + 1 = ?", "answer": 5, "type": "수식"},
                {"problem": "2 + 3 = ?", "answer": 5, "type": "수식"},
                {"problem": "사과 3개, 사과 2개 더 → 모두?", "answer": 5, "type": "문제"},
                {"problem": "공이 1개 있었는데, 2개 받았어요. 모두?", "answer": 3, "type": "문제"},
                {"problem": "별이 4개, 별 1개 더 → 모두?", "answer": 5, "type": "문제"},
            ],
            "뺄셈": [
                {"problem": "5 - 2 = ?", "answer": 3, "type": "수식"},
                {"problem": "4 - 1 = ?", "answer": 3, "type": "수식"},
                {"problem": "5 - 3 = ?", "answer": 2, "type": "수식"},
                {"problem": "3 - 1 = ?", "answer": 2, "type": "수식"},
                {"problem": "6 - 2 = ?", "answer": 4, "type": "수식"},
                {"problem": "연필 5개 중 2개를 잃었어요. 남은 연필?", "answer": 3, "type": "문제"},
                {"problem": "풍선 4개 중 1개가 터졌어요. 남은 풍선?", "answer": 3, "type": "문제"},
                {"problem": "사탕 6개 중 2개를 줬어요. 남은 사탕?", "answer": 4, "type": "문제"},
            ],
            "혼합": [
                {"problem": "3 + 2 - 1 = ?", "answer": 4, "type": "수식"},
                {"problem": "5 - 2 + 1 = ?", "answer": 4, "type": "수식"},
                {"problem": "2 + 3 - 2 = ?", "answer": 3, "type": "수식"},
                {"problem": "4 - 1 + 2 = ?", "answer": 5, "type": "수식"},
            ]
        }
        return all_problems
    
    def grade_2_problems(self):
        """2학년: 두 자리 수, 곱셈 기초"""
        all_problems = {
            "덧셈": [
                {"problem": "10 + 5 = ?", "answer": 15, "type": "수식"},
                {"problem": "12 + 8 = ?", "answer": 20, "type": "수식"},
                {"problem": "15 + 10 = ?", "answer": 25, "type": "수식"},
                {"problem": "23 + 17 = ?", "answer": 40, "type": "수식"},
                {"problem": "30 + 20 = ?", "answer": 50, "type": "수식"},
            ],
            "뺄셈": [
                {"problem": "15 - 5 = ?", "answer": 10, "type": "수식"},
                {"problem": "20 - 8 = ?", "answer": 12, "type": "수식"},
                {"problem": "25 - 10 = ?", "answer": 15, "type": "수식"},
                {"problem": "40 - 23 = ?", "answer": 17, "type": "수식"},
                {"problem": "50 - 20 = ?", "answer": 30, "type": "수식"},
            ],
            "곱셈": [
                {"problem": "2 × 2 = ?", "answer": 4, "type": "수식"},
                {"problem": "3 × 3 = ?", "answer": 9, "type": "수식"},
                {"problem": "2 × 5 = ?", "answer": 10, "type": "수식"},
                {"problem": "4 × 2 = ?", "answer": 8, "type": "수식"},
                {"problem": "5 × 3 = ?", "answer": 15, "type": "수식"},
            ],
            "시간": [
                {"problem": "1시간은 몇 분?", "answer": 60, "type": "개념"},
                {"problem": "2시간은 몇 분?", "answer": 120, "type": "개념"},
                {"problem": "오후 3시 + 2시간 = ?", "answer": "5시", "type": "개념"},
                {"problem": "오전 10시 + 1시간 = ?", "answer": "11시", "type": "개념"},
            ]
        }
        return all_problems
    
    def grade_3_problems(self):
        """3학년: 세 자리 수, 곱셈, 나눗셈"""
        all_problems = {
            "덧셈/뺄셈": [
                {"problem": "100 + 200 = ?", "answer": 300, "type": "수식"},
                {"problem": "234 + 156 = ?", "answer": 390, "type": "수식"},
                {"problem": "500 - 200 = ?", "answer": 300, "type": "수식"},
                {"problem": "456 - 123 = ?", "answer": 333, "type": "수식"},
            ],
            "곱셈/나눗셈": [
                {"problem": "5 × 4 = ?", "answer": 20, "type": "수식"},
                {"problem": "6 × 7 = ?", "answer": 42, "type": "수식"},
                {"problem": "8 × 3 = ?", "answer": 24, "type": "수식"},
                {"problem": "20 ÷ 4 = ?", "answer": 5, "type": "수식"},
                {"problem": "35 ÷ 7 = ?", "answer": 5, "type": "수식"},
            ],
            "도형": [
                {"problem": "정사각형의 한 변이 5cm일 때, 둘레는?", "answer": 20, "type": "개념"},
                {"problem": "직사각형 (가로 6cm, 세로 4cm)의 둘레는?", "answer": 20, "type": "개념"},
                {"problem": "정삼각형의 한 변이 4cm일 때, 둘레는?", "answer": 12, "type": "개념"},
            ]
        }
        return all_problems
    
    def grade_4_problems(self):
        """4학년: 큰 수, 분수, 소수"""
        all_problems = {
            "큰수": [
                {"problem": "1000 + 2000 = ?", "answer": 3000, "type": "수식"},
                {"problem": "5000 - 1500 = ?", "answer": 3500, "type": "수식"},
                {"problem": "123 × 4 = ?", "answer": 492, "type": "수식"},
            ],
            "분수": [
                {"problem": "1/2 + 1/2 = ?", "answer": "1", "type": "개념"},
                {"problem": "1/4 × 2 = ?", "answer": "1/2", "type": "개념"},
                {"problem": "3/4 - 1/4 = ?", "answer": "1/2", "type": "개념"},
            ],
            "소수": [
                {"problem": "0.5 + 0.5 = ?", "answer": 1.0, "type": "수식"},
                {"problem": "1.5 + 2.5 = ?", "answer": 4.0, "type": "수식"},
                {"problem": "3.0 - 1.5 = ?", "answer": 1.5, "type": "수식"},
            ]
        }
        return all_problems
    
    def grade_5_problems(self):
        """5학년: 소수, 분수 계산, 도형"""
        all_problems = {
            "소수": [
                {"problem": "2.5 + 3.5 = ?", "answer": 6.0, "type": "수식"},
                {"problem": "5.0 - 2.3 = ?", "answer": 2.7, "type": "수식"},
                {"problem": "1.5 × 2 = ?", "answer": 3.0, "type": "수식"},
            ],
            "분수": [
                {"problem": "2/3 + 1/3 = ?", "answer": "1", "type": "개념"},
                {"problem": "3/4 - 1/4 = ?", "answer": "1/2", "type": "개념"},
                {"problem": "1/2 × 2/3 = ?", "answer": "1/3", "type": "개념"},
            ],
            "도형": [
                {"problem": "정사각형 (한 변 5cm)의 넓이는?", "answer": 25, "type": "개념"},
                {"problem": "직사각형 (8cm × 6cm)의 넓이는?", "answer": 48, "type": "개념"},
                {"problem": "삼각형의 내각의 합은?", "answer": 180, "type": "개념"},
            ]
        }
        return all_problems
    
    def grade_6_problems(self):
        """6학년: 고급 분수/소수, 비율, 도형의 넓이"""
        all_problems = {
            "분수계산": [
                {"problem": "2/3 × 3/4 = ?", "answer": "1/2", "type": "개념"},
                {"problem": "5/6 - 1/3 = ?", "answer": "1/2", "type": "개념"},
                {"problem": "3/5 ÷ 2/5 = ?", "answer": "3/2", "type": "개념"},
            ],
            "소수/비율": [
                {"problem": "2.5 × 4 = ?", "answer": 10.0, "type": "수식"},
                {"problem": "10 ÷ 2.5 = ?", "answer": 4.0, "type": "수식"},
                {"problem": "비율 2:3 = 4:?", "answer": 6, "type": "개념"},
            ],
            "도형": [
                {"problem": "반지름 5cm인 원의 넓이는? (π=3.14)", "answer": 78.5, "type": "개념"},
                {"problem": "원의 둘레 공식은?", "answer": "2πr", "type": "개념"},
                {"problem": "정육면체의 면의 개수는?", "answer": 6, "type": "개념"},
            ]
        }
        return all_problems
    
    def get_random_problems(self, grade: int, unit: str, count: int = 3) -> List[Dict]:
        """특정 단원에서 랜덤하게 문제를 가져옴"""
        if grade not in self.problems:
            return []
        
        problems_dict = self.problems[grade]
        if unit not in problems_dict:
            return []
        
        unit_problems = problems_dict[unit]
        return random.sample(unit_problems, min(count, len(unit_problems)))
    
    def get_units_by_grade(self, grade: int) -> List[str]:
        """특정 학년의 모든 단원 반환"""
        return self.units_config.get(grade, [])


class GradeTheme:
    """학년별 테마 및 디자인"""
    
    themes = {
        1: {
            "emoji": "👶",
            "title_color": "🌈",
            "problem_marker": "⭐",
            "correct": "✅ 우와! 맞았어요!",
            "incorrect": "❌ 아, 틀렸어요!",
            "divider": "=" * 40,
            "progress_bar": "🌟",
            "decoration": "🎈🎀🎉"
        },
        2: {
            "emoji": "🧒",
            "title_color": "🔵",
            "problem_marker": "📌",
            "correct": "✅ 잘했어요!",
            "incorrect": "❌ 다시 한번!",
            "divider": "=" * 45,
            "progress_bar": "💫",
            "decoration": "🎯🎲🎪"
        },
        3: {
            "emoji": "👦",
            "title_color": "🟢",
            "problem_marker": "📍",
            "correct": "✅ 훌륭해요!",
            "incorrect": "❌ 한번 더!",
            "divider": "=" * 50,
            "progress_bar": "🌱",
            "decoration": "🎬🎭🎨"
        },
        4: {
            "emoji": "👧",
            "title_color": "🟣",
            "problem_marker": "🔹",
            "correct": "✅ 완벽합니다!",
            "incorrect": "❌ 다시 풀어봐!",
            "divider": "=" * 50,
            "progress_bar": "✨",
            "decoration": "🎻🎸🎺"
        },
        5: {
            "emoji": "👨",
            "title_color": "🔴",
            "problem_marker": "🔸",
            "correct": "✅ 뛰어난 성적!",
            "incorrect": "❌ 재도전하세요!",
            "divider": "=" * 50,
            "progress_bar": "🌟",
            "decoration": "🏆🎖️⚡"
        },
        6: {
            "emoji": "👩",
            "title_color": "💛",
            "problem_marker": "◆",
            "correct": "✅ 최고의 성적!",
            "incorrect": "❌ 다시 시도!",
            "divider": "=" * 50,
            "progress_bar": "💎",
            "decoration": "🏅🎯🚀"
        }
    }
    
    unit_themes = {
        "덧셈": {"background": "➕", "points": 10, "icon": "🔢"},
        "뺄셈": {"background": "➖", "points": 10, "icon": "🔢"},
        "혼합": {"background": "🔀", "points": 15, "icon": "⚡"},
        "곱셈": {"background": "✖️", "points": 15, "icon": "💥"},
        "시간": {"background": "🕐", "points": 15, "icon": "⏰"},
        "덧셈/뺄셈": {"background": "➕➖", "points": 12, "icon": "🔢"},
        "곱셈/나눗셈": {"background": "✖️➗", "points": 15, "icon": "💫"},
        "도형": {"background": "📐", "points": 20, "icon": "🔺"},
        "큰수": {"background": "🔢", "points": 15, "icon": "📈"},
        "분수": {"background": "🥧", "points": 20, "icon": "📊"},
        "소수": {"background": "🎯", "points": 20, "icon": "🎲"},
        "분수계산": {"background": "🧮", "points": 25, "icon": "🔧"},
        "소수/비율": {"background": "📐", "points": 25, "icon": "⚖️"},
    }
    
    @classmethod
    def get_theme(cls, grade: int) -> Dict:
        """특정 학년의 테마 반환"""
        return cls.themes.get(grade, cls.themes[1])
    
    @classmethod
    def get_unit_theme(cls, unit: str) -> Dict:
        """단원별 테마 반환"""
        return cls.unit_themes.get(unit, {"background": "📚", "points": 10, "icon": "✨"})


class MathQuiz:
    """수학 퀴즈 실행 클래스 (게임 버전)"""
    
    def __init__(self):
        self.math_problems = MathProblems()
        self.game_state = GameState()
        self.score = 0
        self.total = 0
        self.correct_answers = []
        self.incorrect_answers = []
        self.current_combo = 0
    
    def show_game_header(self, grade: int):
        """게임 헤더 표시"""
        theme = GradeTheme.get_theme(grade)
        print(f"\n{theme['divider']}")
        print(f"{theme['emoji']} 레벨 {self.game_state.level} - {self.game_state.get_level_name()} {theme['emoji']}")
        print(f"{'🎮 누적 포인트':^30} {self.game_state.total_points}P")
        print(f"{theme['divider']}")
    
    def show_progress_bar(self, current: int, total: int, grade: int) -> str:
        """진행률 표시 바"""
        theme = GradeTheme.get_theme(grade)
        filled = int((current / total) * 10)
        bar = theme["progress_bar"] * filled + "⬜" * (10 - filled)
        return f"진행: [{bar}] {current}/{total}"
    
    def show_combo_display(self) -> str:
        """콤보 표시"""
        if self.current_combo == 0:
            return ""
        elif self.current_combo < 3:
            return f"🔥 콤보: {self.current_combo}"
        elif self.current_combo < 5:
            return f"🔥🔥 콤보: {self.current_combo}"
        else:
            return f"🔥🔥🔥 슈퍼 콤보: {self.current_combo}!"
    
    def select_unit(self, grade: int) -> str:
        """단원 선택"""
        theme = GradeTheme.get_theme(grade)
        units = self.math_problems.get_units_by_grade(grade)
        
        print(f"\n{theme['divider']}")
        print(f"{theme['title_color']} {grade}학년 - 단원 선택 {theme['title_color']}")
        print(f"{theme['divider']}")
        
        for i, unit in enumerate(units, 1):
            unit_theme = GradeTheme.get_unit_theme(unit)
            points = unit_theme['points']
            print(f"{i}) {unit_theme['background']} {unit} (기본점수: {points}P)")
        
        while True:
            try:
                choice = int(input("\n단원을 선택하세요: "))
                if 1 <= choice <= len(units):
                    return units[choice - 1]
                else:
                    print(f"1~{len(units)} 사이의 숫자를 입력하세요.")
            except ValueError:
                print("숫자를 입력하세요.")
    
    def run_unit_quiz(self, grade: int, unit: str, num_problems: int = 3):
        """단원별 퀴즈 실행"""
        theme = GradeTheme.get_theme(grade)
        unit_theme = GradeTheme.get_unit_theme(unit)
        problems = self.math_problems.get_random_problems(grade, unit, num_problems)
        
        if not problems:
            print(f"❌ 문제를 찾을 수 없습니다.")
            return False
        
        self.show_game_header(grade)
        print(f"\n{unit_theme['background']} {grade}학년 - {unit} {unit_theme['background']}")
        print(f"{'기본 점수': ^30} {unit_theme['points']}P")
        print(f"{theme['divider']}\n")
        
        self.score = 0
        self.total = len(problems)
        self.current_combo = 0
        self.correct_answers = []
        self.incorrect_answers = []
        
        for idx, problem in enumerate(problems, 1):
            print(f"{theme['problem_marker']} 문제 {idx}/{self.total}")
            self.ask_question(problem, theme, unit_theme)
            print(f"{self.show_progress_bar(idx, self.total, grade)}")
            combo_msg = self.show_combo_display()
            if combo_msg:
                print(f"{combo_msg}")
            print()
        
        return self.show_unit_result(grade, unit, theme, unit_theme)
    
    def ask_question(self, problem: Dict, theme: Dict, unit_theme: Dict):
        """문제 제시 및 답 받기 (게임 버전)"""
        print(f"📝 {problem['problem']}")
        user_answer = input("답: ").strip()
        
        # 정답과 사용자 입력을 비교
        if isinstance(problem['answer'], float):
            try:
                user_float = float(user_answer)
                expected_float = float(problem['answer'])
                is_correct = abs(user_float - expected_float) < 0.0001
            except ValueError:
                is_correct = user_answer == str(problem['answer'])
        else:
            is_correct = user_answer == str(problem['answer'])
        
        if is_correct:
            self.current_combo += 1
            combo_bonus = 1 + (self.current_combo // 3) * 0.5  # 3콤보마다 보너스
            points = self.game_state.add_points(unit_theme['points'], int(combo_bonus * 10) // 10)
            
            print(f"{theme['correct']}")
            print(f"💰 +{points}P", end="")
            if self.current_combo > 1:
                print(f" (×{combo_bonus:.1f} 콤보보너스)", end="")
            print()
            
            self.score += 1
            self.correct_answers.append(problem['problem'])
        else:
            print(f"{theme['incorrect']} (정답: {problem['answer']})")
            self.current_combo = 0  # 콤보 리셋
            self.incorrect_answers.append((problem['problem'], problem['answer']))
        
        print()
    
    def show_unit_result(self, grade: int, unit: str, theme: Dict, unit_theme: Dict) -> bool:
        """단원 결과 표시 (게임 버전)"""
        percentage = (self.score / self.total) * 100
        unit_base_points = unit_theme['points'] * self.total
        
        self.game_state.update_level()
        
        print(f"{theme['divider']}")
        print(f"📊 {unit_theme['background']} {unit} 게임 결과")
        print(f"{theme['divider']}")
        print(f"정답: {self.score}/{self.total} ({percentage:.0f}%)")
        print(f"최고 콤보: {self.current_combo}연속")
        print(f"획득 포인트: {self.game_state.total_points}P")
        print(f"레벨: {self.game_state.get_level_name()}\n")
        
        # 성과 평가
        if percentage == 100:
            feedback = f"🏆 퍼펙트! 모든 문제를 맞혔어요!"
            self.game_state.add_badge(f"⭐ {unit} 마스터")
        elif percentage >= 80:
            feedback = f"🌟 훌륭해요! {unit} 능력이 뛰어나네요!"
            self.game_state.add_badge(f"💫 {unit} 전문가")
        elif percentage >= 60:
            feedback = f"👍 좋아요! 계속 도전해봐요!"
        else:
            feedback = f"💪 다시 한번! 화이팅!"
        
        print(feedback)
        
        # 뱃지 표시
        if self.game_state.badges:
            print(f"\n🎖️ 획득한 뱃지: {', '.join(self.game_state.badges)}")
        
        print(f"{theme['divider']}\n")
        
        return percentage >= 60
    
    def run_full_grade_quiz(self, grade: int):
        """전체 학년 퀴즈 (모든 단원)"""
        theme = GradeTheme.get_theme(grade)
        units = self.math_problems.get_units_by_grade(grade)
        
        self.show_game_header(grade)
        print(f"{theme['emoji']} {grade}학년 완전 정복 모드 시작! {theme['emoji']}")
        print(f"{theme['divider']}\n")
        
        total_score = 0
        total_problems = 0
        passed_units = 0
        unit_results = []
        
        for unit in units:
            problems = self.math_problems.get_random_problems(grade, unit, 4)
            unit_theme = GradeTheme.get_unit_theme(unit)
            self.score = 0
            self.total = len(problems)
            self.current_combo = 0
            
            print(f"{unit_theme['background']} {unit} 도전!")
            print(f"기본점수: {unit_theme['points']}P x {len(problems)} = {unit_theme['points'] * len(problems)}P\n")
            
            for idx, problem in enumerate(problems, 1):
                print(f"【{idx}/{len(problems)}】 {problem['problem']}")
                user_answer = input("답: ").strip()
                
                if isinstance(problem['answer'], float):
                    try:
                        is_correct = abs(float(user_answer) - float(problem['answer'])) < 0.0001
                    except ValueError:
                        is_correct = user_answer == str(problem['answer'])
                else:
                    is_correct = user_answer == str(problem['answer'])
                
                if is_correct:
                    combo_bonus = 1 + (self.current_combo // 2) * 0.5
                    points = self.game_state.add_points(unit_theme['points'], int(combo_bonus * 10) // 10)
                    print(f"{theme['correct']} +{points}P\n")
                    self.current_combo += 1
                    self.score += 1
                else:
                    print(f"{theme['incorrect']} (정답: {problem['answer']})\n")
                    self.current_combo = 0
            
            unit_percentage = (self.score / self.total) * 100
            total_score += self.score
            total_problems += self.total
            
            self.game_state.update_level()
            
            if unit_percentage >= 60:
                passed_units += 1
                result = f"✅ {unit}: {self.score}/{self.total} ({unit_percentage:.0f}%)"
                self.game_state.add_badge(f"🏅 {unit} 완료")
            else:
                result = f"⚠️  {unit}: {self.score}/{self.total} ({unit_percentage:.0f}%)"
            
            unit_results.append(result)
            print(result)
            print()
        
        self.show_full_result(grade, total_score, total_problems, passed_units, len(units), theme, unit_results)
    
    def show_full_result(self, grade: int, score: int, total: int, passed: int, total_units: int, theme: Dict, unit_results: List[str]):
        """전체 결과 표시 (게임 버전)"""
        percentage = (score / total) * 100
        
        print(f"\n{theme['divider']}")
        print(f"🎮 {grade}학년 완전 정복 - 최종 결과")
        print(f"{theme['divider']}")
        print(f"전체 정답: {score}/{total} ({percentage:.0f}%)")
        print(f"통과 단원: {passed}/{total_units}개")
        print(f"최종 레벨: {self.game_state.get_level_name()}")
        print(f"총 획득 포인트: {self.game_state.total_points}P\n")
        
        # 단원별 결과
        print("📋 단원별 성적:")
        for result in unit_results:
            print(f"  {result}")
        
        print()
        
        if percentage == 100 and passed == total_units:
            final_result = "🏆🏆🏆 완벽한 성적! 당신은 수학 천재입니다! 🏆🏆🏆"
        elif percentage >= 80:
            final_result = "🥇 탁월한 성적! 당신은 진정한 마스터입니다!"
        elif percentage >= 60:
            final_result = "🥈 양호한 성적! 계속 연습하면 더 잘할 수 있어요!"
        else:
            final_result = "🥉 더 노력이 필요합니다. 다시 도전해봐요!"
        
        print(final_result)
        
        # 획득한 뱃지
        if self.game_state.badges:
            print(f"\n🎖️ 획득한 뱃지:")
            for badge in self.game_state.badges:
                print(f"  {badge}")
        
        print(f"{theme['divider']}\n")
    
    def show_main_menu(self):
        """메인 메뉴"""
        while True:
            print(f"\n{'=' * 50}")
            print("🎮 초등학교 수학 게임")
            print(f"{'=' * 50}")
            print(f"현재 레벨: {self.game_state.get_level_name()}")
            print(f"누적 포인트: {self.game_state.total_points}P")
            print(f"{"=" * 50}")
            print("1) 단원별 퀴즈 (3문제)")
            print("2) 학년 도전 (전체 단원)")
            print("0) 종료")
            print(f"{'=' * 50}")
            
            choice = input("메뉴를 선택하세요 (0-2): ").strip()
            
            if choice == '0':
                self.show_game_over()
                break
            elif choice == '1':
                self.select_grade_and_unit()
            elif choice == '2':
                self.select_grade_for_full()
            else:
                print("❌ 잘못된 선택입니다.")
    
    def select_grade_and_unit(self):
        """학년 선택 후 단원 선택"""
        print(f"\n{'=' * 50}")
        print("📚 학년을 선택하세요:")
        print(f"{'=' * 50}")
        print("1) 1학년  2) 2학년  3) 3학년")
        print("4) 4학년  5) 5학년  6) 6학년")
        print(f"{'=' * 50}")
        
        try:
            grade = int(input("선택 (1-6): "))
            if 1 <= grade <= 6:
                unit = self.select_unit(grade)
                self.run_unit_quiz(grade, unit)
            else:
                print("❌ 1-6 사이의 숫자를 입력하세요.")
        except ValueError:
            print("❌ 숫자를 입력하세요.")
    
    def select_grade_for_full(self):
        """전체 풀이용 학년 선택"""
        print(f"\n{'=' * 50}")
        print("📚 학년을 선택하세요:")
        print(f"{'=' * 50}")
        print("1) 1학년  2) 2학년  3) 3학년")
        print("4) 4학년  5) 5학년  6) 6학년")
        print(f"{'=' * 50}")
        
        try:
            grade = int(input("선택 (1-6): "))
            if 1 <= grade <= 6:
                self.run_full_grade_quiz(grade)
            else:
                print("❌ 1-6 사이의 숫자를 입력하세요.")
        except ValueError:
            print("❌ 숫자를 입력하세요.")
    
    def show_game_over(self):
        """게임 종료 화면"""
        print(f"\n{'=' * 50}")
        print("🎮 게임 종료")
        print(f"{'=' * 50}")
        print(f"최종 레벨: {self.game_state.get_level_name()}")
        print(f"총 정답: {self.game_state.total_correct}개")
        print(f"총 포인트: {self.game_state.total_points}P")
        
        if self.game_state.badges:
            print(f"\n🎖️ 획득한 뱃지 ({len(self.game_state.badges)}개):")
            for badge in self.game_state.badges:
                print(f"  {badge}")
        
        print(f"\n👋 다음에 또 만나요!")
        print(f"{'=' * 50}\n")



def main():
    """메인 함수"""
    quiz = MathQuiz()
    quiz.show_main_menu()


if __name__ == "__main__":
    main()
