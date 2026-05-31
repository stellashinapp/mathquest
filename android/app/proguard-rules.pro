# Add project specific ProGuard rules here.
# You can control the set of applied configuration files using the
# proguardFiles setting in build.gradle.
#
# For more details, see
#   http://developer.android.com/guide/developing/tools/proguard.html

# If your project uses WebView with JS, uncomment the following
# and specify the fully qualified class name to the JavaScript interface
# class:
#-keepclassmembers class fqcn.of.javascript.interface.for.webview {
#   public *;
#}

# Uncomment this to preserve the line number information for
# debugging stack traces.
#-keepattributes SourceFile,LineNumberTable

# If you keep the line number information, uncomment this to
# hide the original source file name.
#-renamesourcefileattribute SourceFile

# === Capacitor / 플러그인 보호 ===
# Capacitor 코어 및 플러그인 클래스 (리플렉션으로 호출되므로 제거 금지)
-keep class com.getcapacitor.** { *; }
-keep @com.getcapacitor.annotation.CapacitorPlugin class * { *; }
-keep class com.capacitorjs.** { *; }
-keep class com.getcapacitor.community.** { *; }

# Capacitor Cordova 브리지
-keep class org.apache.cordova.** { *; }

# 어노테이션 / 시그니처 (플러그인 메서드 매핑용)
-keepattributes *Annotation*, Signature, InnerClasses, EnclosingMethod

# WebView JavaScript 인터페이스 메서드 보호
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}

# Google AdMob — 광고 SDK 리플렉션 호출
-keep class com.google.android.gms.ads.** { *; }
-keep class com.google.android.gms.internal.** { *; }

# 스택 트레이스용 라인번호 유지 (R8 매핑은 별도)
-keepattributes SourceFile,LineNumberTable
-renamesourcefileattribute SourceFile
