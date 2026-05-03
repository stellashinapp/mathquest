# 🎮 Math Quest — 초등 수학 게임 앱

초등학교 1~6학년 게임형 수학 학습 앱. **브라우저 웹앱** + **안드로이드 네이티브 앱**(Capacitor) 두 가지 방식으로 실행할 수 있습니다.

## 🌏 적용 범위

이 앱은 **대한민국 초등학교 교육과정** 기준. UI와 문제 모두 한국어, 한국 교과서 단원 구성을 따릅니다. 다국어/타국 커리큘럼은 별도 작업 필요.

## ✨ 핵심 특징

- **매번 새 문제 자동 생성** (절차적 생성기, 고정 목록 아님)
- **스테이지 게임 방식** — 5문제 풀면 클리어, 스테이지마다 난이도 상승
- **목숨·별·코인 시스템** — 하트 3개, 정답률에 따라 ⭐~⭐⭐⭐
- **진행도 자동 저장** (localStorage)
- **사고력·도형·규칙 문제** — 단순 계산 + 수열/각도/쌓기나무/각기둥 등 포함
- **네이티브 앱 빌드 지원** — Capacitor로 안드로이드 앱으로 포장 가능
- **AdMob 광고 연동** — 스테이지 클리어 후 전면 광고 표시 (네이티브 앱에서만)

## 📚 학년별 단원 (총 49개)

| 학년 | 단원 |
|-----|-----|
| 1학년 | 10까지 덧셈/뺄셈, 20까지 덧셈/뺄셈, 50까지의 수, 덧뺄 혼합, 규칙 찾기, 모양 알아보기 |
| 2학년 | 두 자리 덧뺄, 세 자리 수, 곱셈구구, 길이 재기, 시각과 시간, 규칙 찾기, 평면도형 |
| 3학년 | 세 자리 덧뺄, 곱셈, 나눗셈, 분수·소수 기초, 도형의 둘레, 사고력 문장제, 각과 도형 성질 |
| 4학년 | 큰 수, 곱셈/나눗셈, 각도, 분수 덧뺄(동분모), 소수 덧뺄, 수 배열 규칙, 다각형 |
| 5학년 | 약수·배수, 분수 덧뺄(이분모), 분수 곱셈, 소수 곱셈, 다각형 넓이, 평균, 합동·대칭, 직육면체 |
| 6학년 | 분수/소수 나눗셈, 비와 비율, 원의 넓이·둘레, 직육면체 부피, 비례식, 각기둥·각뿔, 쌓기나무, 수열 심화 |

## 🚀 실행 방법 (가장 빠름 — 브라우저)

```bash
cd "e:/개발/math"
python -m http.server 8765 -d www
```

브라우저에서 `http://localhost:8765/index.html` 접속.

같은 Wi-Fi의 휴대폰에서도 `http://<PC IP>:8765/index.html`로 바로 사용 가능.

## 📱 Android 앱으로 빌드하기

### 사전 준비 (한 번만)

1. **Android Studio 설치** — <https://developer.android.com/studio> (약 10GB, SDK + JDK 자동 설치)
2. **환경변수 설정**: `ANDROID_HOME`이 자동으로 잡히지 않으면 수동 설정
   ```
   ANDROID_HOME = C:\Users\<사용자>\AppData\Local\Android\Sdk
   ```
3. **Java 17+ 확인**: `java -version` (Android Studio 설치 시 함께 들어감)

### 빌드 절차

프로젝트 루트에서:

```bash
# 1) 의존성 설치 (이미 완료됨)
npm install

# 2) Android 플랫폼 추가 (최초 1회)
npx cap add android

# 3) www/ 변경사항 네이티브 프로젝트로 동기화
npx cap sync

# 4) Android Studio로 열기
npx cap open android
```

Android Studio가 열리면 **Gradle 동기화** 완료 대기 → 상단의 "Run" 버튼 클릭:

- **폰 USB 연결** + 개발자 모드·USB 디버깅 ON → 바로 설치됨
- **에뮬레이터** 사용 가능
- **APK 빌드**: `Build > Build Bundle(s) / APK(s) > Build APK(s)` → `android/app/build/outputs/apk/` 에 APK 생성

APK 파일을 카톡이나 구글 드라이브로 폰에 보내고 설치하면 앱으로 작동합니다.

### 코드 수정 후 재빌드

```bash
npx cap sync   # www/index.html 수정했을 때
# Android Studio에서 Run 다시 누르기
```

## 📢 AdMob 광고 설정

현재 **Google 공식 테스트 광고 ID**로 설정되어 있어서 빌드하면 바로 테스트 광고가 보입니다. 실제 광고로 바꾸려면:

### 1. AdMob 계정 만들기

<https://admob.google.com> → 앱 등록 → **전면 광고(Interstitial)** 단위 생성 → 광고 단위 ID 복사 (`ca-app-pub-XXXXXXXXXX/YYYYYYYYY` 형태)

### 2. 코드 수정

`www/index.html` 에서 아래 두 값만 교체:

```js
const AD_INTERSTITIAL_ID = 'ca-app-pub-실제값/광고단위ID'; // 실제 ID
const AD_TESTING = false; // 배포 시 false
```

광고 빈도도 조절 가능:

```js
const AD_SHOW_EVERY_N_CLEARS = 1; // 매 N번째 스테이지 클리어마다 광고
// 1 = 매번, 2 = 두 번에 한 번, 3 = 세 번에 한 번
```

### 3. AndroidManifest에 AdMob App ID 추가

`android/app/src/main/AndroidManifest.xml` 의 `<application>` 태그 안에 추가:

```xml
<meta-data
    android:name="com.google.android.gms.ads.APPLICATION_ID"
    android:value="ca-app-pub-XXXXXXXXXX~YYYYYYYYY"/>
```

(AdMob 대시보드 > 앱 > 앱 설정 > 앱 ID 복사)

## ⚠️ 아동용 앱 관련 유의사항

Play Store에 **"만 13세 미만 대상"** 으로 등록하면 광고가 제한됩니다:

- **Google Play Families Policy** 준수 필수
- **AdMob for Families** 설정 (행동 기반 광고 불가, 콘텐츠 기반 광고만)
- **개인정보 처리방침** 필수
- **COPPA** (미국) / **GDPR-K** (EU) 설정

해당 설정은 AdMob 대시보드 → 앱 → "이 앱은 아동을 대상으로 함" 토글.

## 📁 파일 구성

| 파일/폴더 | 설명 |
|---------|-----|
| `www/index.html` | 메인 앱 (브라우저 + Capacitor 공용) |
| `capacitor.config.json` | Capacitor 설정 (앱 ID, 앱 이름) |
| `package.json` | 의존성 및 빌드 스크립트 |
| `android/` | `npx cap add android` 실행 시 자동 생성 (네이티브 프로젝트) |
| `math_problems.py` | Python CLI 초기 버전 (참고용) |
| `test_generators.mjs` | 문제 생성기 자동 검증 (`node test_generators.mjs`) |

## 🎯 난이도 설계

각 단원의 `generate(stage)` 함수는 스테이지 번호를 받아 난이도 조절:

- 1학년 10까지 덧셈: 스테이지 1은 `3+2`, 스테이지 5는 `7+2`
- 4학년 수 배열 규칙: 스테이지 올라갈수록 공차 확대, 등비/피보나치/제곱수까지
- 6학년 쌓기나무: 정육면체·직육면체 크기 점진 확장

5문제 중 **3문제 이상 정답 → 스테이지 통과**. 5문제 올정답 + 하트 다 남음 → **3별**. 무한 반복 가능.

## ⌨️ 입력 방법

- **숫자 키패드** (큰 버튼, 아이 친화적)
- **분수**: `1/2` 형식 (기약 아니어도 동등값이면 정답)
- **소수**: `.` 키
- **음수**: `±` 버튼

## 🔧 문제 생성기 확장

`www/index.html` 의 `GRADES` 객체에 새 단원 추가:

```js
{
  id: "g3-new-unit",
  name: "새 단원",
  icon: "🆕",
  color: "#ffcccc",
  generate(stage) {
    const a = rand(1, 5 + stage);
    const b = rand(1, 5 + stage);
    return { q: `${a} + ${b} = ?`, a: a + b };
  }
}
```

`stage`를 활용해 숫자 범위·복잡도 확장 → 자동 난이도 상승.

## ✅ 현재 규모

- **49개 단원**, 약 200여 개 문제 템플릿 → 사실상 무한 생성
- 7,350개 샘플 자동 검증 통과 (`npm run test:gen`)
