# 🚀 fastlane supply 자동 배포 셋업 가이드

`fastlane`은 설치되어 있고 `Fastfile`도 작성됐어요. 이제 **Google Play 측 셋업** (사용자님이 직접 하셔야 하는 부분) 만 끝내면 한 줄 명령으로 자동 업로드됩니다.

---

## 사전 준비 (1회만, ~30분)

### 1. Google Play Developer 가입 ($25)

<https://play.google.com/console/signup>

이미 가입되어 있으면 다음 단계로.

### 2. Play Console에 앱 만들기 (첫 업로드는 수동)

⚠️ **fastlane은 기존 앱에만 업로드**할 수 있습니다. 첫 AAB는 수동 업로드 필요:

1. Play Console → "앱 만들기"
2. 앱 이름: `Math Quest`
3. 기본 언어: 한국어
4. 무료/유료, 광고 포함 여부, 콘텐츠 정책 설문 응답
5. **테스트 → 내부 테스트 → 새 릴리스 만들기**
6. `MathQuest-release.aab` 업로드 → 저장 → 검토 → 출시
7. 테스터 이메일 추가 → 옵트인 링크로 폰에 설치

이 과정이 끝나면 fastlane으로 **두 번째 릴리스부터 자동 업로드** 가능.

### 3. Google Cloud 서비스 계정 만들기

1. <https://console.cloud.google.com/iam-admin/serviceaccounts>
2. 프로젝트 선택 또는 새 프로젝트 만들기 (예: `mathquest-publishing`)
3. **+ 서비스 계정 만들기**
   - 이름: `play-publishing`
   - 설명: Fastlane Play Console publishing
   - 만들기
4. 권한 부여 단계: 일단 **건너뛰기** (Play Console에서 따로 부여)
5. 만든 서비스 계정 클릭 → **키** 탭 → **키 추가 → 새 키 만들기 → JSON**
6. 다운로드된 JSON 파일을 **`play-store-key.json`** 으로 이름 변경
7. 이 파일을 프로젝트 루트(`e:/개발/math/`)에 저장

### 4. Google Play Android Developer API 활성화

1. <https://console.cloud.google.com/apis/library/androidpublisher.googleapis.com>
2. 만든 프로젝트 선택 → **사용 설정**

### 5. Play Console에서 서비스 계정 권한 부여

1. <https://play.google.com/console/u/0/developers/api-access>
2. 방금 만든 서비스 계정이 목록에 보임 (안 보이면 잠시 기다린 후 새로고침)
3. **앱 권한 부여** 클릭
4. Math Quest 앱 선택 → 다음
5. 권한 체크:
   - ☑ **앱 정보 보기**
   - ☑ **프로덕션 외 트랙에 출시** (internal/alpha/beta)
   - ☑ **프로덕션 트랙에 출시** (선택, 처음엔 비추천)
6. 적용

---

## 사용법 (셋업 완료 후, 매번 5초)

### 내부 테스트 트랙 업로드 (제일 안전)

```bash
cd "e:/개발/math/android"
PATH="/c/Ruby33-x64/bin:$PATH" fastlane internal
```

자동으로:
1. `gradle clean bundleRelease` 실행
2. AAB 빌드
3. Play Console internal track에 업로드
4. 끝

### 다른 트랙

```bash
fastlane alpha       # 비공개 알파
fastlane beta        # 공개 베타
fastlane production  # 실제 프로덕션 출시 (신중!)
fastlane build       # 업로드 없이 빌드만
fastlane bump_version  # versionCode 자동 +1
```

### 자주 만나는 에러

**`Version code X has already been used`**: 이미 같은 versionCode의 AAB가 업로드됨. 해결:
```bash
fastlane bump_version  # versionCode +1
fastlane internal
```

**`The Android App Bundle is signed with the wrong key`**: 키스토어가 다름. `android/app/build.gradle`의 `signingConfigs.release.storeFile`이 정확한지 확인.

---

## 다른 앱에 재사용

다른 앱 (예: 영어 패턴 마스터) 출시할 때:

1. **이미 있는 것 재사용**:
   - Ruby + fastlane (시스템 전역 ✅)
   - `play-store-key.json` (같은 Google Play 계정이면 그대로 ✅)

2. **새로 해야 할 것**:
   - 새 앱의 `Fastfile`, `Appfile` (이 파일 그대로 복사 + `package_name`만 수정)
   - Play Console에서 새 앱 만들고 첫 AAB 수동 업로드 (한 번만)
   - Play Console > API access 에서 같은 서비스 계정에 새 앱 권한 부여 (체크 한 번)

→ 두 번째 앱부터는 **5분이면 자동 배포 라인 셋업 완료**.

---

## 보안 주의

`play-store-key.json` 은 절대 공개 저장소에 커밋하면 안 됩니다.
이미 `.gitignore`에 추가되어 있는지 확인하고, 없으면:

```
play-store-key.json
*.p12
android/play-store-key.json
```

USB·1Password 등 안전한 곳에 별도 백업 필수.
