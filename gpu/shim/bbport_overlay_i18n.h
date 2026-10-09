// SPDX-License-Identifier: GPL-2.0-or-later
#pragma once

#include "bbport_settings.h"

namespace BbI18n {

enum TextId {
    MenuTitle,
    FpsFormat,
    SectionUpscaler,
    ComboUpscaler,
    UpscalerOff,
    UpscalerFsr3,
    UpscalerFsr4,
    UpscalerFsr411,
    UpscalerTaa,
    UpscalerDlss,
    UpscalerXess,
    UnsupportedGpu,
    WorkInProgress,
    Fsr4Unavailable,
    Fsr4Fallback,
    HintFsr411,
    HintFsr4,
    CheckFsr4AutoExp,
    CheckFsr4InvertJitter,
    HintFsr4Jitter,
    ComboPreset,
    PresetFormat,
    PresetNativeAA,
    PresetQuality,
    PresetBalanced,
    PresetPerformance,
    PresetUltraPerformance,
    TextTaaDescription,
    ActiveRender,
    StartupPreset,
    HintFixedRenderAuto,
    HintFixedRenderCustom,
    HintDynamicRender,
    CheckSharpen,
    SliderSharpness,
    HintSharpen,
    CheckJitter,
    HintJitter,
    SectionReactive,
    CheckReactive,
    HintReactive,
    SliderReactiveScale,
    SliderReactiveThreshold,
    SliderReactiveMax,
    CheckShowReactiveMask,
    CheckObjectMotion,
    HintObjectMotion,
    CheckShowMotionVectors,
    HintMotionDebug,
    SectionOutputRes,
    ComboOutputRes,
    HintFixedOutputRes,
    HintDynamicOutputRes,
    ComboLiveRes,
    LiveResAuto,
    LiveResOff,
    LiveResOn,
    HintLiveRes,
    SectionGameEffects,
    ComboModelLod,
    LodMax,
    LodDefault,
    LodLower,
    LodMin,
    EffectChromatic,
    EffectDof,
    EffectMotionBlur,
    EffectSsao,
    EffectGameAa,
    EffectDynamicShadows,
    EffectSsr,
    EffectSkipIntro,
    EffectDebugCamera,
    EffectDebugMenu,
    HintEffectsPatches,
    HintControls,
    RestartNotice,
    BtnRestart,
    SectionMisc,
    CheckShowFps,
    ComboLanguage,
    BtnClose,
    SettingsSavedHint,
    PromptHint,
    TextIdCount
};

inline const char* const Strings[TextIdCount][BbSettings::LanguageCount] = {
    // MenuTitle
    {
        "Bloodborne — Ayarlar  (Insert / L3+R3)",
        "Bloodborne — Settings  (Insert / L3+R3)",
        "Bloodborne — настройки  (Insert / L3+R3)"
    },
    // FpsFormat
    {
        "%.0f FPS  (%.1f ms)",
        "%.0f FPS  (%.1f ms)",
        "%.0f FPS  (%.1f мс)"
    },
    // SectionUpscaler
    {
        "Zamansal Ölçekleyici (Upscaler)",
        "Temporal Upscaler",
        "Временной апскейлер"
    },
    // ComboUpscaler
    {
        "Ölçekleyici",
        "Upscaler",
        "Апскейлер"
    },
    // UpscalerOff
    {
        "Kapalı",
        "Off",
        "Выкл"
    },
    // UpscalerFsr3
    {
        "FSR 3.1",
        "FSR 3.1",
        "FSR 3.1"
    },
    // UpscalerFsr4
    {
        "FSR 4 (INT8)",
        "FSR 4 (INT8)",
        "FSR 4 (INT8)"
    },
    // UpscalerFsr411
    {
        "FSR 4.1.1 (INT8)",
        "FSR 4.1.1 (INT8)",
        "FSR 4.1.1 (INT8)"
    },
    // UpscalerTaa
    {
        "TAA (Doğal Kenar Yumuşatma)",
        "TAA (Native Anti-Aliasing)",
        "TAA (нативное сглаживание)"
    },
    // UpscalerDlss
    {
        "DLSS (NVIDIA RTX)",
        "DLSS (NVIDIA RTX)",
        "DLSS (NVIDIA RTX)"
    },
    // UpscalerXess
    {
        "XeSS",
        "XeSS",
        "XeSS"
    },
    // UnsupportedGpu
    {
        "— Ekran kartı tarafından desteklenmiyor",
        "— Not supported by GPU",
        "— не поддерживается видеокартой"
    },
    // WorkInProgress
    {
        "— Geliştirilme aşamasında",
        "— In progress",
        "— в работе"
    },
    // Fsr4Unavailable
    {
        "FSR 4 kullanılamıyor: %s",
        "FSR 4 unavailable: %s",
        "FSR 4 недоступен: %s"
    },
    // Fsr4Fallback
    {
        "Yukarıda seçilen mod devrede. FSR 4 tekrar seçilebilir.",
        "Active mode selected above. FSR 4 can be selected again.",
        "Активен режим, выбранный выше. FSR 4 можно выбрать снова."
    },
    // HintFsr411
    {
        "FSR 4.1.1 INT8 modu: AMD 4.1.1 DLL modeli Vulkan üzerinde çalıştırılır (sonuç DLL ile birebir aynıdır). Native..Performance için tek model, Ultra Performance için özel model.",
        "FSR 4.1.1 in INT8 mode: model from AMD 4.1.1 DLL reproduced in Vulkan (matches DLL). One model for Native..Performance and dedicated model for Ultra Performance.",
        "FSR 4.1.1 в режиме INT8: модель из DLL AMD 4.1.1, воспроизведённая в Vulkan (результат совпадает с DLL). Одна модель для Native..Performance и отдельная для Ultra Performance."
    },
    // HintFsr4
    {
        "FSR 4 INT8 modu (AMD FidelityFX SDK v07 modeli). FSR 3.1'e kıyasla daha yüksek görüntü kalitesi sunar. Profil değişimi modeli yeniden oluşturur (kısa duraklama).",
        "FSR 4 in INT8 mode (v07 model from AMD FidelityFX SDK). Higher quality than FSR 3.1, but heavier pass. Preset change rebuilds model (brief pause).",
        "FSR 4 в режиме INT8 (модель v07 из исходников AMD FidelityFX SDK). Качество выше, чем у FSR 3.1, но проход тяжелее. Смена пресета пересобирает модель (короткая пауза)."
    },
    // CheckFsr4AutoExp
    {
        "FSR 4: Otomatik Pozlama (Auto-Exposure)",
        "FSR 4: Auto-exposure",
        "FSR 4: авто-экспозиция"
    },
    // CheckFsr4InvertJitter
    {
        "FSR 4: Ters Jitter İşareti (Invert Jitter)",
        "FSR 4: Invert jitter sign",
        "FSR 4: обратный знак jitter"
    },
    // HintFsr4Jitter
    {
        "Ghosting önleme ayarı: FSR 4 ağı renkleri pozlamaya göre normalize eder ve geçmiş kareleri ne zaman bırakacağına karar verir. Yeniden başlatma gerektirmez.",
        "Ghosting check: FSR 4 network normalizes color by exposure and decides when to drop past frames. Changes immediately without restart.",
        "Проверка при гостинге: сеть FSR 4 нормирует цвет по экспозиции и по ней решает, когда отбросить прошлые кадры. Меняются сразу, без перезапуска."
    },
    // ComboPreset
    {
        "Ölçekleme Kalitesi",
        "Preset",
        "Пресет"
    },
    // PresetFormat
    {
        "%s (x%.1f, render %dx%d)",
        "%s (x%.1f, render %dx%d)",
        "%s (x%.1f, рендер %dx%d)"
    },
    // PresetNativeAA
    {
        "Doğal (Native AA)",
        "Native AA",
        "Native AA"
    },
    // PresetQuality
    {
        "Kalite",
        "Quality",
        "Качество"
    },
    // PresetBalanced
    {
        "Dengeli",
        "Balanced",
        "Баланс"
    },
    // PresetPerformance
    {
        "Performans",
        "Performance",
        "Производительность"
    },
    // PresetUltraPerformance
    {
        "Ultra Performans",
        "Ultra Performance",
        "Ультра-производительность"
    },
    // TextTaaDescription
    {
        "TAA, sahneyi çıkış çözünürlüğünde FSR modeli veya ölçekleme olmadan yumuşatır. Kayıtlı FSR profili FSR seçildiğinde geri yüklenir.",
        "TAA antialiases the scene at output resolution without FSR model or upscaling. Saved FSR preset will restore upon selecting FSR.",
        "TAA сглаживает сцену в разрешении вывода, без модели FSR и апскейлинга. Сохранённый пресет FSR восстановится при выборе FSR."
    },
    // ActiveRender
    {
        "Aktif Sahne Çözünürlüğü: %d x %d",
        "Active scene render: %d x %d",
        "Активный рендер сцены: %d x %d"
    },
    // StartupPreset
    {
        "Başlangıç Profili: %s",
        "Startup preset: %s",
        "Пресет при запуске: %s"
    },
    // HintFixedRenderAuto
    {
        "1080p harici çıkışta tüm oyun profil çözünürlüğünde işlenir (başlangıç yaması): Zayıf GPU'lar ve Steam Deck için en hızlı yoldur. Değişiklikler yeniden başlatma gerektirir.",
        "When output is not 1080p, the game renders at preset resolution (startup patch): fastest on Steam Deck and weak GPUs. Changes require restart.",
        "При выводе не 1080p вся игра рисуется в разрешении пресета (патч при запуске): это быстрее всего на Steam Deck и слабых GPU. Смена пресета или разрешения вывода — после перезапуска."
    },
    // HintFixedRenderCustom
    {
        "BB_RENDER_RES başlangıçta sahne boyutunu sabitler. Dinamik değişim için bu ortam değişkenini kaldırın.",
        "BB_RENDER_RES fixes scene size at startup. Remove this explicit variable to change resolution/presets dynamically.",
        "BB_RENDER_RES фиксирует размер сцены при запуске. Уберите эту явную переменную для смены разрешения и пресетов без перезапуска игры."
    },
    // HintDynamicRender
    {
        "Native AA: FSR doğal kenar yumuşatma olarak çalışır. Diğer profiller sahne çizim çözünürlüğünü düşürerek FPS artırır. Kullanıcı arayüzü daima tam çıkış çözünürlüğünde net çizilir. Yeniden başlatma gerektirmez.",
        "Native AA: FSR acts as anti-aliasing. Other presets reduce scene render resolution relative to output. UI renders at output resolution. Applies on the next frame without restart.",
        "Native AA: FSR работает как сглаживание. Остальные пресеты уменьшают разрешение отрисовки сцены относительно вывода. Интерфейс рисуется в разрешении вывода. Пресет применяется со следующего кадра без перезапуска игры."
    },
    // CheckSharpen
    {
        "Keskinleştirme (RCAS)",
        "Sharpening (RCAS)",
        "Резкость (RCAS)"
    },
    // SliderSharpness
    {
        "Keskinlik Oranı",
        "Sharpness",
        "Сила резкости"
    },
    // HintSharpen
    {
        "1.0'a kadar ölçekleyicinin kendi RCAS keskinliği devrededir. 1.0 üzeri ek bir RCAS geçişi ekler. Ctrl+tık ile tam değer yazabilirsiniz.",
        "Up to 1 is native upscaler RCAS. Above 1 adds an extra RCAS pass. Ctrl+click on slider to enter exact value.",
        "До 1 — резкость самого апскейлера (RCAS). Выше 1 добавляется ещё один проход RCAS. Ctrl+клик по ползунку — ввести точное значение."
    },
    // CheckJitter
    {
        "Alt-Piksel Titreşimi (Jitter)",
        "Subpixel Jitter",
        "Субпиксельный сдвиг (jitter)"
    },
    // HintJitter
    {
        "Her kare sahne bir pikselin kesri kadar kaydırılır ve ölçekleyici geçmiş karelerden daha fazla detay üretir. Kapatılırsa yalnızca basit zamansal yumuşatma kalır.",
        "Each frame the scene shifts by a fraction of a pixel, and the upscaler reconstructs more detail across frames. Without it, only history smoothing remains.",
        "Каждый кадр сцена сдвигается на долю пикселя, и апскейлер собирает из нескольких кадров больше деталей. Без него получается только сглаживание по истории."
    },
    // SectionReactive
    {
        "Tepkisellik Maskesi (Reactive Mask)",
        "Reactive Mask",
        "Маска реактивности"
    },
    // CheckReactive
    {
        "Maskeyi Etkinleştir",
        "Enable mask",
        "Включить маску"
    },
    // HintReactive
    {
        "Şeffaf parçacık ve sis efektlerini işaretleyerek ölçekleyicinin geçmiş karelere daha az bağımlı olmasını sağlar. Efekt arkasındaki gölgelenmeyi (ghosting) azaltır.",
        "Marks transparent effects (particles, smoke) so the upscaler relies less on past frames. Reduces ghosting behind effects.",
        "Помечает прозрачные эффекты (частицы, дымку), чтобы апскейлер меньше опирался на прошлые кадры. Меньше шлейфов за эффектами."
    },
    // SliderReactiveScale
    {
        "Ölçek",
        "Scale",
        "Масштаб"
    },
    // SliderReactiveThreshold
    {
        "Eşik",
        "Threshold",
        "Порог"
    },
    // SliderReactiveMax
    {
        "Maksimum",
        "Maximum",
        "Максимум"
    },
    // CheckShowReactiveMask
    {
        "Maskeyi Göster (Hata Ayıklama)",
        "Show mask (Debug)",
        "Показать маску (отладка)"
    },
    // CheckObjectMotion
    {
        "Karakter Hareket Vektörleri",
        "Object Motion Vectors",
        "Векторы движения персонажей"
    },
    // HintObjectMotion
    {
        "Animasyonlu nesneler için hassas hareket vektörleri: Karakter hareket ederken pelerin ve silah kenarlarındaki parçalanmayı önler. Yeniden başlatma gerektirir.",
        "Accurate motion vectors for animated objects: clothes and weapons break up less during motion. Applied after restart.",
        "Точные векторы для анимированных объектов: одежда и оружие меньше рассыпаются при движении. Изменение применяется после перезапуска игры."
    },
    // CheckShowMotionVectors
    {
        "Hareket Vektörlerini Göster (Hata Ayıklama)",
        "Show motion vectors (Debug)",
        "Показать векторы движения (отладка)"
    },
    // HintMotionDebug
    {
        "Kırmızı/Yeşil: Yatay/dikey hareket (8 piksel = tam parlaklık). Mavi: Piksel kamera harici nesne hareket vektörü içeriyor.",
        "Red/Green: Horizontal/vertical movement (8 pixels = full brightness). Blue: Pixel received exact object vector.",
        "Красный/зелёный: движение по горизонтали/вертикали (8 пикселей = полная яркость). Синий: пиксель получил точный вектор объекта."
    },
    // SectionOutputRes
    {
        "Çıkış Çözünürlüğü",
        "Output Resolution",
        "Разрешение вывода"
    },
    // ComboOutputRes
    {
        "Çıkış Çözünürlüğü",
        "Output Resolution",
        "Разрешение вывода"
    },
    // HintFixedOutputRes
    {
        "Nihai kare ve kullanıcı arayüzü boyutu. Seçilen profil sahne çözünürlüğünü çıkışa göre oranlar: 4K Performans = 1920x1080 render. Yeniden başlatma gerektirir.",
        "Final frame and UI size. Preset defines scene size relative to output: 4K Performance = 1920x1080 render. Applies after restart.",
        "Размер готового кадра и интерфейса. Пресет задаёт размер сцены относительно вывода: 4K Performance = 1920x1080. Применяется после перезапуска игры."
    },
    // HintDynamicOutputRes
    {
        "Nihai kare ve kullanıcı arayüzü boyutu bir sonraki karede anında değişir. Seçilen profil sahne çözünürlüğünü oranlar.",
        "Final frame and UI size changes on the next frame. Preset defines scene size relative to output.",
        "Размер готового кадра и интерфейса меняется на границе следующего кадра. Пресет задаёт размер сцены относительно вывода."
    },
    // ComboLiveRes
    {
        "Anında Çözünürlük Değişimi",
        "Live Resolution Switching",
        "Смена разрешения на лету"
    },
    // LiveResAuto
    {
        "Otomatik (Ekran kartına göre)",
        "Auto (GPU-based)",
        "Авто (по видеокарте)"
    },
    // LiveResOff
    {
        "Kapalı (Daha hızlı)",
        "Disabled (Faster)",
        "Выключена (быстрее)"
    },
    // LiveResOn
    {
        "Açık",
        "Enabled",
        "Включена"
    },
    // HintLiveRes
    {
        "Açık: Çıkış çözünürlüğü ve profil oyunu yeniden başlatmadan anında değişir ancak son işleme 1080p kalır. Kapalı: En yüksek performans için başlangıç yaması kullanılır. Yeniden başlatma gerektirir.",
        "Enabled: Output resolution and preset change without restart, post-processing remains at 1080p. Disabled: Entire game renders at preset resolution, faster on Steam Deck. Applies after restart.",
        "Включена: разрешение вывода и пресет меняются без перезапуска, но постобработка игры остаётся в 1080p. Выключена: всё рисуется в разрешении пресета. Применяется после перезапуска игры."
    },
    // SectionGameEffects
    {
        "Oyun Efektleri (Yeniden Başlatma Gerekir)",
        "Game Effects (After Restart)",
        "Эффекты игры (после перезапуска)"
    },
    // ComboModelLod
    {
        "Model Detay Seviyesi (LoD)",
        "Model Detail (LoD)",
        "Детализация моделей"
    },
    // LodMax
    {
        "Maksimum Detay (-2)",
        "Maximum (-2)",
        "Максимальная (-2)"
    },
    // LodDefault
    {
        "Varsayılan (0)",
        "Default (0)",
        "Как в игре"
    },
    // LodLower
    {
        "Düşük (1)",
        "Lower (1)",
        "Ниже (1)"
    },
    // LodMin
    {
        "En Düşük (2)",
        "Minimum (2)",
        "Минимальная (2)"
    },
    // EffectChromatic
    {
        "Kromatik Sapma (Chromatic Aberration)",
        "Chromatic Aberration",
        "Хроматическая аберрация"
    },
    // EffectDof
    {
        "Alan Derinliği (DoF)",
        "Depth of Field (DoF)",
        "Глубина резкости (DoF)"
    },
    // EffectMotionBlur
    {
        "Hareket Bulanıklığı (Motion Blur)",
        "Motion Blur",
        "Размытие в движении"
    },
    // EffectSsao
    {
        "Ortam Kapatma (SSAO)",
        "Ambient Occlusion (SSAO)",
        "Затенение SSAO"
    },
    // EffectGameAa
    {
        "Oyunun Yerel FXAA Kenar Yumuşatması",
        "Game Native FXAA",
        "Собственное сглаживание игры"
    },
    // EffectDynamicShadows
    {
        "Dinamik Işık Gölgeleri",
        "Dynamic Light Shadows",
        "Тени от динамических источников"
    },
    // EffectSsr
    {
        "SSR Yansımaları (Deneysel)",
        "SSR Reflections (Experimental)",
        "Отражения SSR (не было в игре)"
    },
    // EffectSkipIntro
    {
        "Açılış İntrolarını Atla",
        "Skip Intro Cutscenes",
        "Пропуск заставок при запуске"
    },
    // EffectDebugCamera
    {
        "Serbest Kamera (Cross + L3)",
        "Free Camera (Cross + L3)",
        "Свободная камера (Cross + L3)"
    },
    // EffectDebugMenu
    {
        "Geliştirici / Debug Menüsü (Font gerekir)",
        "Debug Menu (Requires fonts)",
        "Debug menu (нужны файлы шрифтов)"
    },
    // HintEffectsPatches
    {
        "Efektler başlangıçta oyun ikili dosyasına yamalanır (patches/Bloodborne.xml). Hareket bulanıklığı ve dinamik gölgeler GPU'yu hissedilir derecede yükler.",
        "Effects are toggled via game patches at startup (patches/Bloodborne.xml). Motion blur and dynamic shadows noticeably load the GPU.",
        "Эффекты включаются и выключаются патчами игры при запуске (patches/Bloodborne.xml). Размытие в движении и тени от динамических источников заметно нагружают GPU."
    },
    // HintControls
    {
        "Serbest kamera: Cross basılı tutup L3'e basın (Klavyede: Space + Z). Debug menü: Sol Touchpad / Tab (Nexus #253 fontları gerekir). Sağ Touchpad: Backspace.",
        "Free camera: Hold Cross and press L3 (Keyboard: Space + Z). Debug menu: Left Touchpad / Tab (requires Nexus #253 fonts). Right Touchpad: Backspace.",
        "Свободная камера: удерживайте Cross и нажимайте L3 (клавиатура: Space + Z). Debug menu: левый touchpad / Tab. Нужны DbgFont14h.ccm и DbgFont14h.tpf в dvdroot_ps4/font из мода Nexus #253. Правый touchpad: Backspace."
    },
    // RestartNotice
    {
        "Değişikliklerin geçerli olması için oyunu yeniden başlatın",
        "Changes will apply after restarting the game",
        "Изменения применятся после перезапуска игры"
    },
    // BtnRestart
    {
        "Kaydet ve Oyunu Yeniden Başlat",
        "Save & Restart Game",
        "Применить и перезапустить игру"
    },
    // SectionMisc
    {
        "Diğer Seçenekler",
        "Miscellaneous",
        "Прочее"
    },
    // CheckShowFps
    {
        "Ekran Köşesinde Canlı FPS Göstergesi",
        "FPS counter in corner",
        "Счётчик FPS в углу"
    },
    // ComboLanguage
    {
        "Arayüz Dili / Language",
        "Interface Language",
        "Язык интерфейса"
    },
    // BtnClose
    {
        "Kapat",
        "Close",
        "Закрыть"
    },
    // SettingsSavedHint
    {
        "Ayarlar bbport.ini dosyasına kaydedilir",
        "Settings are saved to bbport.ini",
        "Настройки сохраняются в bbport.ini"
    },
    // PromptHint
    {
        "Klavye: Enter = Onayla, Esc = İptal  |  Oyun Kolu: Çarpı (A) = Onayla, Daire (B) = İptal",
        "Keyboard: Enter = OK, Esc = Cancel  |  Gamepad: Cross (A) = OK, Circle (B) = Cancel",
        "Keyboard: Enter = OK, Esc = Cancel  |  Gamepad: Cross (A) = OK, Circle (B) = Cancel"
    }
};

inline const char* Tr(TextId id, int lang = -1) {
    if (lang < 0 || lang >= BbSettings::LanguageCount) {
        lang = BbSettings::Get().language.load();
    }
    if (lang < 0 || lang >= BbSettings::LanguageCount) {
        lang = BbSettings::LangTr;
    }
    return Strings[id][lang];
}

inline const char* PresetName(int preset, int lang = -1) {
    switch (preset) {
    case BbSettings::NativeAA: return Tr(PresetNativeAA, lang);
    case BbSettings::Quality: return Tr(PresetQuality, lang);
    case BbSettings::Balanced: return Tr(PresetBalanced, lang);
    case BbSettings::Performance: return Tr(PresetPerformance, lang);
    case BbSettings::UltraPerformance: return Tr(PresetUltraPerformance, lang);
    default: return "";
    }
}

inline const char* EffectLabel(int effect_index, int lang = -1) {
    static constexpr TextId effect_ids[BbSettings::EffectCount] = {
        EffectChromatic,
        EffectDof,
        EffectMotionBlur,
        EffectSsao,
        EffectGameAa,
        EffectDynamicShadows,
        EffectSsr,
        EffectSkipIntro,
        EffectDebugCamera,
        EffectDebugMenu
    };
    if (effect_index >= 0 && effect_index < BbSettings::EffectCount) {
        return Tr(effect_ids[effect_index], lang);
    }
    return "";
}

} // namespace BbI18n
