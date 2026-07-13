"""Lightweight UI translation layer.

Usage:
    from i18n import t, set_language
    set_language("en")
    label = t("spray.generate")
    msg = t("spray.done", name="foo", w=512, h=512, fmt="DXT1", kb=170, path="...")

Language is chosen once at startup (from config / system locale); changing it
saves to config and the app relaunches, so strings are resolved at widget
construction time. Emoji/✅/❌ prefixes live in the calling code — values here
are plain text.
"""

from __future__ import annotations

# (code, native display name) — order shown in the language dropdown.
LANGUAGES = [
    ("tr", "Türkçe"),
    ("en", "English"),
    ("ru", "Русский"),
    ("es", "Español"),
    ("de", "Deutsch"),
    ("fr", "Français"),
    ("ko", "한국어"),
    ("pt", "Português"),
    ("zh", "中文"),
]
_CODES = {c for c, _ in LANGUAGES}
_current = "en"

_STRINGS = {
    # ---- common -------------------------------------------------------
    "common.browse": {
        "tr": "Göz At...", "en": "Browse...", "ru": "Обзор...",
        "es": "Examinar...", "de": "Durchsuchen...", "fr": "Parcourir...",
        "ko": "찾아보기...", "pt": "Procurar...", "zh": "浏览...",
    },
    "common.pick_image": {
        "tr": "Görsel Seç", "en": "Choose Image", "ru": "Выбрать изображение",
        "es": "Elegir imagen", "de": "Bild wählen", "fr": "Choisir une image",
        "ko": "이미지 선택", "pt": "Escolher imagem", "zh": "选择图片",
    },
    "common.pick_image_dialog": {
        "tr": "Görsel seç", "en": "Choose image", "ru": "Выберите изображение",
        "es": "Elegir imagen", "de": "Bild wählen", "fr": "Choisir une image",
        "ko": "이미지 선택", "pt": "Escolher imagem", "zh": "选择图片",
    },
    "common.images_filter": {
        "tr": "Görseller", "en": "Images", "ru": "Изображения",
        "es": "Imágenes", "de": "Bilder", "fr": "Images",
        "ko": "이미지", "pt": "Imagens", "zh": "图片",
    },
    "common.audio_filter": {
        "tr": "Ses dosyaları", "en": "Audio files", "ru": "Аудиофайлы",
        "es": "Archivos de audio", "de": "Audiodateien", "fr": "Fichiers audio",
        "ko": "오디오 파일", "pt": "Arquivos de áudio", "zh": "音频文件",
    },
    "common.all_files": {
        "tr": "Tümü", "en": "All files", "ru": "Все файлы",
        "es": "Todos", "de": "Alle", "fr": "Tous", "ko": "모든 파일",
        "pt": "Todos", "zh": "所有文件",
    },
    "common.pick_dir_dialog": {
        "tr": "Kayıt dizini seç", "en": "Choose export folder",
        "ru": "Выберите папку сохранения", "es": "Elegir carpeta de guardado",
        "de": "Zielordner wählen", "fr": "Choisir le dossier de sortie",
        "ko": "저장 폴더 선택", "pt": "Escolher pasta de saída",
        "zh": "选择保存文件夹",
    },
    "common.export_dir": {
        "tr": "Kayıt Dizini:", "en": "Export folder:", "ru": "Папка сохранения:",
        "es": "Carpeta de guardado:", "de": "Zielordner:",
        "fr": "Dossier de sortie :", "ko": "저장 폴더:",
        "pt": "Pasta de saída:", "zh": "保存文件夹：",
    },
    "common.export_dir_custom": {
        "tr": "Kayıt Dizini (custom klasörü):",
        "en": "Export folder (custom folder):",
        "ru": "Папка сохранения (папка custom):",
        "es": "Carpeta de guardado (carpeta custom):",
        "de": "Zielordner (custom-Ordner):",
        "fr": "Dossier de sortie (dossier custom) :",
        "ko": "저장 폴더 (custom 폴더):",
        "pt": "Pasta de saída (pasta custom):",
        "zh": "保存文件夹（custom 文件夹）：",
    },
    "common.select_image_first": {
        "tr": "Önce bir görsel seçin.", "en": "Choose an image first.",
        "ru": "Сначала выберите изображение.", "es": "Elige una imagen primero.",
        "de": "Zuerst ein Bild wählen.", "fr": "Choisissez d'abord une image.",
        "ko": "먼저 이미지를 선택하세요.", "pt": "Escolha uma imagem primeiro.",
        "zh": "请先选择图片。",
    },
    "common.select_export": {
        "tr": "Kayıt dizini seçin.", "en": "Choose an export folder.",
        "ru": "Выберите папку сохранения.", "es": "Elige una carpeta de guardado.",
        "de": "Zielordner wählen.", "fr": "Choisissez un dossier de sortie.",
        "ko": "저장 폴더를 선택하세요.", "pt": "Escolha uma pasta de saída.",
        "zh": "请选择保存文件夹。",
    },
    "common.select_export_custom": {
        "tr": "Kayıt dizini seçin (örn: ...\\tf\\custom\\ModKlasorum).",
        "en": "Choose an export folder (e.g. ...\\tf\\custom\\MyMod).",
        "ru": "Выберите папку сохранения (напр. ...\\tf\\custom\\MyMod).",
        "es": "Elige una carpeta (ej. ...\\tf\\custom\\MyMod).",
        "de": "Zielordner wählen (z. B. ...\\tf\\custom\\MyMod).",
        "fr": "Choisissez un dossier (ex. ...\\tf\\custom\\MyMod).",
        "ko": "저장 폴더를 선택하세요 (예: ...\\tf\\custom\\MyMod).",
        "pt": "Escolha uma pasta (ex.: ...\\tf\\custom\\MyMod).",
        "zh": "请选择文件夹（例如 ...\\tf\\custom\\MyMod）。",
    },
    "common.image_open_error": {
        "tr": "Görsel açılamadı: {exc}", "en": "Could not open image: {exc}",
        "ru": "Не удалось открыть изображение: {exc}",
        "es": "No se pudo abrir la imagen: {exc}",
        "de": "Bild konnte nicht geöffnet werden: {exc}",
        "fr": "Impossible d'ouvrir l'image : {exc}",
        "ko": "이미지를 열 수 없습니다: {exc}",
        "pt": "Não foi possível abrir a imagem: {exc}",
        "zh": "无法打开图片：{exc}",
    },
    "common.preview_error": {
        "tr": "Önizleme hatası: {exc}", "en": "Preview error: {exc}",
        "ru": "Ошибка предпросмотра: {exc}", "es": "Error de vista previa: {exc}",
        "de": "Vorschaufehler: {exc}", "fr": "Erreur d'aperçu : {exc}",
        "ko": "미리보기 오류: {exc}", "pt": "Erro de pré-visualização: {exc}",
        "zh": "预览错误：{exc}",
    },

    # ---- app / top bar ------------------------------------------------
    "app.rescan": {
        "tr": "Yeniden Tara", "en": "Rescan", "ru": "Пересканировать",
        "es": "Reescanear", "de": "Neu suchen", "fr": "Rescanner",
        "ko": "다시 검색", "pt": "Verificar de novo", "zh": "重新扫描",
    },
    "app.manual": {
        "tr": "El ile Seç", "en": "Choose Manually", "ru": "Выбрать вручную",
        "es": "Elegir manual", "de": "Manuell wählen", "fr": "Choisir manuel",
        "ko": "직접 선택", "pt": "Escolher manual", "zh": "手动选择",
    },
    "app.searching": {
        "tr": "TF2 aranıyor...", "en": "Looking for TF2...",
        "ru": "Поиск TF2...", "es": "Buscando TF2...", "de": "Suche TF2...",
        "fr": "Recherche de TF2...", "ko": "TF2 찾는 중...",
        "pt": "Procurando TF2...", "zh": "正在查找 TF2...",
    },
    "app.tf2_not_found": {
        "tr": "TF2 bulunamadı — dizinleri el ile seçin",
        "en": "TF2 not found — choose folders manually",
        "ru": "TF2 не найдена — выберите папки вручную",
        "es": "TF2 no encontrado — elige las carpetas manualmente",
        "de": "TF2 nicht gefunden — Ordner manuell wählen",
        "fr": "TF2 introuvable — choisissez les dossiers manuellement",
        "ko": "TF2를 찾을 수 없음 — 폴더를 직접 선택하세요",
        "pt": "TF2 não encontrado — escolha as pastas manualmente",
        "zh": "未找到 TF2 — 请手动选择文件夹",
    },
    "app.pick_tf2_dialog": {
        "tr": "Team Fortress 2\\tf klasörünü seç",
        "en": "Choose the Team Fortress 2\\tf folder",
        "ru": "Выберите папку Team Fortress 2\\tf",
        "es": "Elige la carpeta Team Fortress 2\\tf",
        "de": "Team Fortress 2\\tf-Ordner wählen",
        "fr": "Choisir le dossier Team Fortress 2\\tf",
        "ko": "Team Fortress 2\\tf 폴더 선택",
        "pt": "Escolha a pasta Team Fortress 2\\tf",
        "zh": "选择 Team Fortress 2\\tf 文件夹",
    },
    "app.language": {
        "tr": "Dil:", "en": "Language:", "ru": "Язык:", "es": "Idioma:",
        "de": "Sprache:", "fr": "Langue :", "ko": "언어:", "pt": "Idioma:",
        "zh": "语言：",
    },

    # ---- tab names ----------------------------------------------------
    "tab.spray": {
        "tr": "Sprey Oluşturucu", "en": "Spray Maker", "ru": "Спрей-мейкер",
        "es": "Creador de sprays", "de": "Spray-Ersteller",
        "fr": "Créateur de spray", "ko": "스프레이 제작", "pt": "Criador de spray",
        "zh": "喷漆制作",
    },
    "tab.objector": {
        "tr": "Objector Yapıcı", "en": "Objector Maker",
        "ru": "Objector-мейкер", "es": "Creador Objector",
        "de": "Objector-Ersteller", "fr": "Créateur Objector",
        "ko": "Objector 제작", "pt": "Criador Objector", "zh": "Objector 制作",
    },
    "tab.sound": {
        "tr": "Hitsound Kesici", "en": "Hitsound Trimmer",
        "ru": "Хитсаунд-триммер", "es": "Recortador de hitsound",
        "de": "Hitsound-Schneider", "fr": "Découpeur de hitsound",
        "ko": "히트사운드 자르기", "pt": "Cortador de hitsound", "zh": "命中音裁剪",
    },

    # ---- spray tab ----------------------------------------------------
    "spray.header": {
        "tr": "Görselleri (.png/.jpg/.gif) TF2 sprey formatına (.vtf + .vmt) "
              "dönüştürür. Çıktı 512 KB sınırına göre otomatik optimize edilir.",
        "en": "Turns images (.png/.jpg/.gif) into TF2 spray format (.vtf + .vmt). "
              "Output is auto-optimized to stay under the 512 KB limit.",
        "ru": "Превращает изображения (.png/.jpg/.gif) в формат спрея TF2 "
              "(.vtf + .vmt). Результат авто-оптимизируется под лимит 512 КБ.",
        "es": "Convierte imágenes (.png/.jpg/.gif) al formato de spray de TF2 "
              "(.vtf + .vmt). Se optimiza para no superar los 512 KB.",
        "de": "Wandelt Bilder (.png/.jpg/.gif) ins TF2-Spray-Format (.vtf + .vmt) "
              "um. Die Ausgabe wird automatisch unter 512 KB gehalten.",
        "fr": "Convertit les images (.png/.jpg/.gif) au format spray TF2 "
              "(.vtf + .vmt). La sortie est optimisée sous la limite de 512 Ko.",
        "ko": "이미지(.png/.jpg/.gif)를 TF2 스프레이 형식(.vtf + .vmt)으로 "
              "변환합니다. 출력은 512 KB 제한에 맞춰 자동 최적화됩니다.",
        "pt": "Converte imagens (.png/.jpg/.gif) para o formato de spray do TF2 "
              "(.vtf + .vmt). A saída é otimizada para ficar abaixo de 512 KB.",
        "zh": "将图片（.png/.jpg/.gif）转换为 TF2 喷漆格式（.vtf + .vmt）。"
              "输出会自动优化以保持在 512 KB 限制内。",
    },
    "spray.view_original": {
        "tr": "Orijinal", "en": "Original", "ru": "Оригинал", "es": "Original",
        "de": "Original", "fr": "Original", "ko": "원본", "pt": "Original",
        "zh": "原图",
    },
    "spray.view_game": {
        "tr": "Oyun İçi (VTF)", "en": "In-Game (VTF)", "ru": "В игре (VTF)",
        "es": "En el juego (VTF)", "de": "Im Spiel (VTF)", "fr": "En jeu (VTF)",
        "ko": "게임 내 (VTF)", "pt": "No jogo (VTF)", "zh": "游戏内 (VTF)",
    },
    "spray.example": {
        "tr": "Örnek", "en": "Example", "ru": "Пример", "es": "Ejemplo",
        "de": "Beispiel", "fr": "Exemple", "ko": "예제", "pt": "Exemplo",
        "zh": "示例",
    },
    "spray.no_preview": {
        "tr": "Önizleme yok", "en": "No preview", "ru": "Нет предпросмотра",
        "es": "Sin vista previa", "de": "Keine Vorschau", "fr": "Aucun aperçu",
        "ko": "미리보기 없음", "pt": "Sem pré-visualização", "zh": "无预览",
    },
    "spray.name_label": {
        "tr": "Sprey adı:", "en": "Spray name:", "ru": "Имя спрея:",
        "es": "Nombre del spray:", "de": "Spray-Name:", "fr": "Nom du spray :",
        "ko": "스프레이 이름:", "pt": "Nome do spray:", "zh": "喷漆名称：",
    },
    "spray.name_placeholder": {
        "tr": "dosya adı", "en": "file name", "ru": "имя файла",
        "es": "nombre de archivo", "de": "Dateiname", "fr": "nom de fichier",
        "ko": "파일 이름", "pt": "nome do arquivo", "zh": "文件名",
    },
    "spray.max_res": {
        "tr": "Maks. çözünürlük:", "en": "Max resolution:",
        "ru": "Макс. разрешение:", "es": "Resolución máx.:",
        "de": "Max. Auflösung:", "fr": "Résolution max :",
        "ko": "최대 해상도:", "pt": "Resolução máx.:", "zh": "最大分辨率：",
    },
    "spray.generate": {
        "tr": "Sprey Oluştur", "en": "Create Spray", "ru": "Создать спрей",
        "es": "Crear spray", "de": "Spray erstellen", "fr": "Créer le spray",
        "ko": "스프레이 생성", "pt": "Criar spray", "zh": "生成喷漆",
    },
    "spray.generating_btn": {
        "tr": "Oluşturuluyor...", "en": "Creating...", "ru": "Создание...",
        "es": "Creando...", "de": "Wird erstellt...", "fr": "Création...",
        "ko": "생성 중...", "pt": "Criando...", "zh": "生成中...",
    },
    "spray.encoding": {
        "tr": "VTF kodlanıyor, lütfen bekleyin...",
        "en": "Encoding VTF, please wait...",
        "ru": "Кодирование VTF, подождите...",
        "es": "Codificando VTF, espera...",
        "de": "VTF wird kodiert, bitte warten...",
        "fr": "Encodage VTF, veuillez patienter...",
        "ko": "VTF 인코딩 중, 잠시만 기다리세요...",
        "pt": "Codificando VTF, aguarde...", "zh": "正在编码 VTF，请稍候...",
    },
    "spray.computing_preview": {
        "tr": "VTF önizlemesi hesaplanıyor...",
        "en": "Computing VTF preview...",
        "ru": "Расчёт предпросмотра VTF...",
        "es": "Calculando vista previa VTF...",
        "de": "VTF-Vorschau wird berechnet...",
        "fr": "Calcul de l'aperçu VTF...",
        "ko": "VTF 미리보기 계산 중...",
        "pt": "Calculando pré-visualização VTF...", "zh": "正在计算 VTF 预览...",
    },
    "spray.hint": {
        "tr": "İpucu: \"Oyun İçi (VTF)\" görünümü spreyi gerçek DXT\n"
              "sıkıştırmasından geçirip duvar üzerinde gösterir.\n\n"
              "Spreyin oyunda görünmesi için çıktıyı\n"
              "tf\\materials\\vgui\\logos klasörüne kaydedin ve\n"
              "oyun ayarlarından spreyi seçin.",
        "en": "Tip: the \"In-Game (VTF)\" view runs the spray through real\n"
              "DXT compression and shows it on a wall.\n\n"
              "For the spray to appear in game, save the output to\n"
              "tf\\materials\\vgui\\logos and select it in the\n"
              "game settings.",
        "ru": "Совет: режим «В игре (VTF)» пропускает спрей через реальное\n"
              "DXT-сжатие и показывает его на стене.\n\n"
              "Чтобы спрей появился в игре, сохраните результат в\n"
              "tf\\materials\\vgui\\logos и выберите его в\n"
              "настройках игры.",
        "es": "Consejo: la vista \"En el juego (VTF)\" pasa el spray por\n"
              "compresión DXT real y lo muestra en una pared.\n\n"
              "Para que aparezca en el juego, guarda la salida en\n"
              "tf\\materials\\vgui\\logos y selecciónalo en los\n"
              "ajustes del juego.",
        "de": "Tipp: Die \"Im Spiel (VTF)\"-Ansicht schickt das Spray durch\n"
              "echte DXT-Kompression und zeigt es an einer Wand.\n\n"
              "Damit das Spray im Spiel erscheint, speichere die Ausgabe in\n"
              "tf\\materials\\vgui\\logos und wähle es in den\n"
              "Spieleinstellungen aus.",
        "fr": "Astuce : la vue \"En jeu (VTF)\" applique une vraie\n"
              "compression DXT au spray et l'affiche sur un mur.\n\n"
              "Pour qu'il apparaisse en jeu, enregistrez la sortie dans\n"
              "tf\\materials\\vgui\\logos et sélectionnez-le dans les\n"
              "paramètres du jeu.",
        "ko": "팁: \"게임 내 (VTF)\" 보기는 스프레이를 실제 DXT\n"
              "압축으로 처리해 벽에 보여줍니다.\n\n"
              "게임에서 보이려면 출력을\n"
              "tf\\materials\\vgui\\logos 에 저장하고\n"
              "게임 설정에서 선택하세요.",
        "pt": "Dica: a visão \"No jogo (VTF)\" passa o spray por\n"
              "compressão DXT real e o mostra numa parede.\n\n"
              "Para aparecer no jogo, salve a saída em\n"
              "tf\\materials\\vgui\\logos e selecione-o nas\n"
              "configurações do jogo.",
        "zh": "提示：“游戏内 (VTF)”视图会用真实的 DXT\n"
              "压缩处理喷漆并显示在墙上。\n\n"
              "要在游戏中显示，请把输出保存到\n"
              "tf\\materials\\vgui\\logos 并在\n"
              "游戏设置中选择它。",
    },
    "spray.kind_static": {
        "tr": "statik görsel", "en": "static image", "ru": "статичное изображение",
        "es": "imagen estática", "de": "statisches Bild", "fr": "image statique",
        "ko": "정적 이미지", "pt": "imagem estática", "zh": "静态图片",
    },
    "spray.kind_animated": {
        "tr": "{n} kare (animasyonlu GIF)", "en": "{n} frames (animated GIF)",
        "ru": "{n} кадров (анимированный GIF)", "es": "{n} fotogramas (GIF animado)",
        "de": "{n} Frames (animiertes GIF)", "fr": "{n} images (GIF animé)",
        "ko": "{n} 프레임 (움직이는 GIF)", "pt": "{n} quadros (GIF animado)",
        "zh": "{n} 帧（动态 GIF）",
    },
    "spray.game_info": {
        "tr": "Oyun içi: {w}x{h} {fmt}{note} · ~{kb} KB",
        "en": "In-game: {w}x{h} {fmt}{note} · ~{kb} KB",
        "ru": "В игре: {w}x{h} {fmt}{note} · ~{kb} КБ",
        "es": "En el juego: {w}x{h} {fmt}{note} · ~{kb} KB",
        "de": "Im Spiel: {w}x{h} {fmt}{note} · ~{kb} KB",
        "fr": "En jeu : {w}x{h} {fmt}{note} · ~{kb} Ko",
        "ko": "게임 내: {w}x{h} {fmt}{note} · ~{kb} KB",
        "pt": "No jogo: {w}x{h} {fmt}{note} · ~{kb} KB",
        "zh": "游戏内：{w}x{h} {fmt}{note} · ~{kb} KB",
    },
    "spray.frame_note": {
        "tr": " · {n} kare", "en": " · {n} frames", "ru": " · {n} кадров",
        "es": " · {n} fotogramas", "de": " · {n} Frames", "fr": " · {n} images",
        "ko": " · {n} 프레임", "pt": " · {n} quadros", "zh": " · {n} 帧",
    },
    "spray.done": {
        "tr": "Tamamlandı: {name}.vtf + .vmt\n{w}x{h} {fmt}{note} — {kb} KB\n{path}",
        "en": "Done: {name}.vtf + .vmt\n{w}x{h} {fmt}{note} — {kb} KB\n{path}",
        "ru": "Готово: {name}.vtf + .vmt\n{w}x{h} {fmt}{note} — {kb} КБ\n{path}",
        "es": "Listo: {name}.vtf + .vmt\n{w}x{h} {fmt}{note} — {kb} KB\n{path}",
        "de": "Fertig: {name}.vtf + .vmt\n{w}x{h} {fmt}{note} — {kb} KB\n{path}",
        "fr": "Terminé : {name}.vtf + .vmt\n{w}x{h} {fmt}{note} — {kb} Ko\n{path}",
        "ko": "완료: {name}.vtf + .vmt\n{w}x{h} {fmt}{note} — {kb} KB\n{path}",
        "pt": "Concluído: {name}.vtf + .vmt\n{w}x{h} {fmt}{note} — {kb} KB\n{path}",
        "zh": "完成：{name}.vtf + .vmt\n{w}x{h} {fmt}{note} — {kb} KB\n{path}",
    },
    "spray.done_note": {
        "tr": ", {n} kare", "en": ", {n} frames", "ru": ", {n} кадров",
        "es": ", {n} fotogramas", "de": ", {n} Frames", "fr": ", {n} images",
        "ko": ", {n} 프레임", "pt": ", {n} quadros", "zh": "，{n} 帧",
    },
    "spray.example_not_found": {
        "tr": "Örnek görsel bulunamadı.", "en": "Example image not found.",
        "ru": "Пример не найден.", "es": "Imagen de ejemplo no encontrada.",
        "de": "Beispielbild nicht gefunden.", "fr": "Image d'exemple introuvable.",
        "ko": "예제 이미지를 찾을 수 없습니다.", "pt": "Imagem de exemplo não encontrada.",
        "zh": "未找到示例图片。",
    },

    # ---- objector tab -------------------------------------------------
    "objector.header": {
        "tr": "Conscientious Objector için tam renkli paper_overlay.png üretir. "
              "Dosya, custom klasörünün içine doğru yola "
              "(scripts\\items\\custom_texture_blend_layers) yazılır. Kare alanı "
              "sürükleyerek taşıyın, sağ alt köşeden boyutlandırın — önizleme "
              "anında güncellenir.",
        "en": "Creates a full-color paper_overlay.png for the Conscientious "
              "Objector. The file is written to the correct path inside your "
              "custom folder (scripts\\items\\custom_texture_blend_layers). Drag "
              "the square to move it, resize from the bottom-right corner — the "
              "preview updates instantly.",
        "ru": "Создаёт полноцветный paper_overlay.png для Conscientious "
              "Objector. Файл записывается по верному пути в вашу папку custom "
              "(scripts\\items\\custom_texture_blend_layers). Перетаскивайте "
              "квадрат, меняйте размер за правый нижний угол — предпросмотр "
              "обновляется мгновенно.",
        "es": "Crea un paper_overlay.png a todo color para el Conscientious "
              "Objector. El archivo se guarda en la ruta correcta dentro de tu "
              "carpeta custom (scripts\\items\\custom_texture_blend_layers). "
              "Arrastra el cuadro para moverlo y ajústalo desde la esquina "
              "inferior derecha — la vista previa se actualiza al instante.",
        "de": "Erstellt ein vollfarbiges paper_overlay.png für den Conscientious "
              "Objector. Die Datei wird in den richtigen Pfad in deinem "
              "custom-Ordner geschrieben "
              "(scripts\\items\\custom_texture_blend_layers). Ziehe das Quadrat "
              "zum Verschieben, ändere die Größe an der unteren rechten Ecke — "
              "die Vorschau aktualisiert sofort.",
        "fr": "Crée un paper_overlay.png en couleur pour le Conscientious "
              "Objector. Le fichier est écrit au bon endroit dans votre dossier "
              "custom (scripts\\items\\custom_texture_blend_layers). Déplacez le "
              "carré, redimensionnez depuis le coin inférieur droit — l'aperçu "
              "se met à jour instantanément.",
        "ko": "Conscientious Objector용 풀컬러 paper_overlay.png를 만듭니다. "
              "파일은 custom 폴더 안의 올바른 경로 "
              "(scripts\\items\\custom_texture_blend_layers)에 저장됩니다. "
              "사각형을 드래그해 옮기고 오른쪽 아래 모서리로 크기를 조절하세요 — "
              "미리보기가 즉시 갱신됩니다.",
        "pt": "Cria um paper_overlay.png em cores para o Conscientious Objector. "
              "O arquivo é gravado no caminho correto dentro da sua pasta custom "
              "(scripts\\items\\custom_texture_blend_layers). Arraste o quadrado "
              "para mover e redimensione pelo canto inferior direito — a "
              "pré-visualização atualiza na hora.",
        "zh": "为 Conscientious Objector 生成全彩 paper_overlay.png。文件会写入 "
              "custom 文件夹内的正确路径"
              "（scripts\\items\\custom_texture_blend_layers）。拖动方框移动，"
              "从右下角调整大小 — 预览会即时更新。",
    },
    "objector.reset_crop": {
        "tr": "Kırpmayı Sıfırla", "en": "Reset Crop", "ru": "Сброс обрезки",
        "es": "Restablecer recorte", "de": "Zuschnitt zurücksetzen",
        "fr": "Réinitialiser le recadrage", "ko": "자르기 초기화",
        "pt": "Redefinir recorte", "zh": "重置裁剪",
    },
    "objector.resolution": {
        "tr": "Çözünürlük:", "en": "Resolution:", "ru": "Разрешение:",
        "es": "Resolución:", "de": "Auflösung:", "fr": "Résolution :",
        "ko": "해상도:", "pt": "Resolução:", "zh": "分辨率：",
    },
    "objector.size_256": {
        "tr": "256 (önerilen)", "en": "256 (recommended)", "ru": "256 (рекоменд.)",
        "es": "256 (recomendado)", "de": "256 (empfohlen)", "fr": "256 (recommandé)",
        "ko": "256 (권장)", "pt": "256 (recomendado)", "zh": "256（推荐）",
    },
    "objector.size_128": {
        "tr": "128 (en uyumlu)", "en": "128 (most compatible)",
        "ru": "128 (совместимо)", "es": "128 (más compatible)",
        "de": "128 (kompatibel)", "fr": "128 (compatible)", "ko": "128 (호환성)",
        "pt": "128 (mais compatível)", "zh": "128（最兼容）",
    },
    "objector.size_512": {
        "tr": "512 (en keskin)", "en": "512 (sharpest)", "ru": "512 (чётче)",
        "es": "512 (más nítido)", "de": "512 (schärfste)", "fr": "512 (net)",
        "ko": "512 (가장 선명)", "pt": "512 (mais nítido)", "zh": "512（最清晰）",
    },
    "objector.output": {
        "tr": "Çıktı ({size}px)", "en": "Output ({size}px)",
        "ru": "Результат ({size}px)", "es": "Salida ({size}px)",
        "de": "Ausgabe ({size}px)", "fr": "Sortie ({size}px)",
        "ko": "출력 ({size}px)", "pt": "Saída ({size}px)", "zh": "输出（{size}px）",
    },
    "objector.ingame_view": {
        "tr": "Oyun içi görünüm", "en": "In-game look", "ru": "Вид в игре",
        "es": "Aspecto en el juego", "de": "Ansicht im Spiel", "fr": "Aperçu en jeu",
        "ko": "게임 내 모습", "pt": "Aparência no jogo", "zh": "游戏内效果",
    },
    "objector.save_btn": {
        "tr": "paper_overlay.png Olarak Kaydet", "en": "Save as paper_overlay.png",
        "ru": "Сохранить как paper_overlay.png",
        "es": "Guardar como paper_overlay.png",
        "de": "Als paper_overlay.png speichern",
        "fr": "Enregistrer en paper_overlay.png",
        "ko": "paper_overlay.png로 저장", "pt": "Salvar como paper_overlay.png",
        "zh": "保存为 paper_overlay.png",
    },
    "objector.res_note": {
        "tr": "\nOyunda görünmezse Çözünürlük'ü 128'e alıp tekrar deneyin.",
        "en": "\nIf it doesn't show in game, set Resolution to 128 and retry.",
        "ru": "\nЕсли не видно в игре, поставьте разрешение 128 и повторите.",
        "es": "\nSi no aparece en el juego, pon la resolución en 128 y reintenta.",
        "de": "\nErscheint es nicht im Spiel, Auflösung auf 128 setzen und erneut.",
        "fr": "\nS'il n'apparaît pas en jeu, mettez la résolution à 128 et réessayez.",
        "ko": "\n게임에서 안 보이면 해상도를 128로 바꾸고 다시 시도하세요.",
        "pt": "\nSe não aparecer no jogo, use resolução 128 e tente de novo.",
        "zh": "\n如果游戏中不显示，请将分辨率设为 128 再试一次。",
    },
    "objector.saved": {
        "tr": "Kaydedildi ({w}x{h}):\n{path}{note}",
        "en": "Saved ({w}x{h}):\n{path}{note}",
        "ru": "Сохранено ({w}x{h}):\n{path}{note}",
        "es": "Guardado ({w}x{h}):\n{path}{note}",
        "de": "Gespeichert ({w}x{h}):\n{path}{note}",
        "fr": "Enregistré ({w}x{h}) :\n{path}{note}",
        "ko": "저장됨 ({w}x{h}):\n{path}{note}",
        "pt": "Salvo ({w}x{h}):\n{path}{note}",
        "zh": "已保存（{w}x{h}）：\n{path}{note}",
    },

    # ---- sound tab ----------------------------------------------------
    "sound.header": {
        "tr": "Ses dosyasını (.mp3/.wav/.ogg) kırpar ve TF2 standardında "
              "(44100 Hz, 16-bit PCM) hitsound/killsound olarak kaydeder. "
              "Turuncu tutamaçları sürükleyin.",
        "en": "Trims an audio file (.mp3/.wav/.ogg) and saves it as a "
              "TF2-standard (44100 Hz, 16-bit PCM) hitsound/killsound. "
              "Drag the orange handles.",
        "ru": "Обрезает аудиофайл (.mp3/.wav/.ogg) и сохраняет как хитсаунд/"
              "килсаунд стандарта TF2 (44100 Гц, 16-бит PCM). "
              "Тяните оранжевые маркеры.",
        "es": "Recorta un archivo de audio (.mp3/.wav/.ogg) y lo guarda como "
              "hitsound/killsound estándar de TF2 (44100 Hz, 16-bit PCM). "
              "Arrastra los tiradores naranjas.",
        "de": "Schneidet eine Audiodatei (.mp3/.wav/.ogg) zu und speichert sie "
              "als TF2-Standard (44100 Hz, 16-bit PCM) Hitsound/Killsound. "
              "Ziehe die orangefarbenen Griffe.",
        "fr": "Découpe un fichier audio (.mp3/.wav/.ogg) et l'enregistre en "
              "hitsound/killsound standard TF2 (44100 Hz, 16-bit PCM). "
              "Faites glisser les poignées orange.",
        "ko": "오디오 파일(.mp3/.wav/.ogg)을 잘라 TF2 표준(44100 Hz, 16-bit "
              "PCM) 히트사운드/킬사운드로 저장합니다. 주황색 핸들을 드래그하세요.",
        "pt": "Corta um arquivo de áudio (.mp3/.wav/.ogg) e o salva como "
              "hitsound/killsound padrão do TF2 (44100 Hz, 16-bit PCM). "
              "Arraste as alças laranja.",
        "zh": "裁剪音频文件（.mp3/.wav/.ogg）并保存为 TF2 标准"
              "（44100 Hz, 16-bit PCM）命中音/击杀音。拖动橙色手柄。",
    },
    "sound.pick_file": {
        "tr": "Ses Dosyası Seç", "en": "Choose Audio File",
        "ru": "Выбрать аудиофайл", "es": "Elegir archivo de audio",
        "de": "Audiodatei wählen", "fr": "Choisir un fichier audio",
        "ko": "오디오 파일 선택", "pt": "Escolher arquivo de áudio",
        "zh": "选择音频文件",
    },
    "sound.pick_dialog": {
        "tr": "Ses dosyası seç", "en": "Choose audio file",
        "ru": "Выберите аудиофайл", "es": "Elegir archivo de audio",
        "de": "Audiodatei wählen", "fr": "Choisir un fichier audio",
        "ko": "오디오 파일 선택", "pt": "Escolher arquivo de áudio",
        "zh": "选择音频文件",
    },
    "sound.start": {
        "tr": "Başlangıç (sn):", "en": "Start (s):", "ru": "Начало (с):",
        "es": "Inicio (s):", "de": "Start (s):", "fr": "Début (s) :",
        "ko": "시작 (초):", "pt": "Início (s):", "zh": "开始（秒）：",
    },
    "sound.end": {
        "tr": "Bitiş (sn):", "en": "End (s):", "ru": "Конец (с):",
        "es": "Fin (s):", "de": "Ende (s):", "fr": "Fin (s) :",
        "ko": "끝 (초):", "pt": "Fim (s):", "zh": "结束（秒）：",
    },
    "sound.selection": {
        "tr": "Seçim: {x} sn", "en": "Selection: {x} s", "ru": "Выбор: {x} с",
        "es": "Selección: {x} s", "de": "Auswahl: {x} s", "fr": "Sélection : {x} s",
        "ko": "선택: {x} 초", "pt": "Seleção: {x} s", "zh": "选中：{x} 秒",
    },
    "sound.stop": {
        "tr": "Durdur", "en": "Stop", "ru": "Стоп", "es": "Detener",
        "de": "Stopp", "fr": "Arrêter", "ko": "정지", "pt": "Parar", "zh": "停止",
    },
    "sound.preview_btn": {
        "tr": "Önizle", "en": "Preview", "ru": "Прослушать", "es": "Escuchar",
        "de": "Vorhören", "fr": "Écouter", "ko": "미리듣기", "pt": "Ouvir",
        "zh": "试听",
    },
    "sound.export_hit": {
        "tr": "Hitsound Olarak Aktar", "en": "Export as Hitsound",
        "ru": "Экспорт как хитсаунд", "es": "Exportar como hitsound",
        "de": "Als Hitsound exportieren", "fr": "Exporter en hitsound",
        "ko": "히트사운드로 내보내기", "pt": "Exportar como hitsound",
        "zh": "导出为命中音",
    },
    "sound.export_kill": {
        "tr": "Killsound Olarak Aktar", "en": "Export as Killsound",
        "ru": "Экспорт как килсаунд", "es": "Exportar como killsound",
        "de": "Als Killsound exportieren", "fr": "Exporter en killsound",
        "ko": "킬사운드로 내보내기", "pt": "Exportar como killsound",
        "zh": "导出为击杀音",
    },
    "sound.loading": {
        "tr": "Yükleniyor...", "en": "Loading...", "ru": "Загрузка...",
        "es": "Cargando...", "de": "Wird geladen...", "fr": "Chargement...",
        "ko": "불러오는 중...", "pt": "Carregando...", "zh": "加载中...",
    },
    "sound.exporting": {
        "tr": "Dışa aktarılıyor...", "en": "Exporting...", "ru": "Экспорт...",
        "es": "Exportando...", "de": "Wird exportiert...", "fr": "Exportation...",
        "ko": "내보내는 중...", "pt": "Exportando...", "zh": "导出中...",
    },
    "sound.channels": {
        "tr": "{n} kanal", "en": "{n} channels", "ru": "{n} канала",
        "es": "{n} canales", "de": "{n} Kanäle", "fr": "{n} canaux",
        "ko": "{n} 채널", "pt": "{n} canais", "zh": "{n} 声道",
    },
    "sound.file_info": {
        "tr": "{name} — {dur} sn, {rate} Hz, {ch}",
        "en": "{name} — {dur} s, {rate} Hz, {ch}",
        "ru": "{name} — {dur} с, {rate} Гц, {ch}",
        "es": "{name} — {dur} s, {rate} Hz, {ch}",
        "de": "{name} — {dur} s, {rate} Hz, {ch}",
        "fr": "{name} — {dur} s, {rate} Hz, {ch}",
        "ko": "{name} — {dur} 초, {rate} Hz, {ch}",
        "pt": "{name} — {dur} s, {rate} Hz, {ch}",
        "zh": "{name} — {dur} 秒, {rate} Hz, {ch}",
    },
    "sound.load_first": {
        "tr": "Önce bir ses dosyası yükleyin.", "en": "Load an audio file first.",
        "ru": "Сначала загрузите аудиофайл.", "es": "Carga un archivo de audio primero.",
        "de": "Zuerst eine Audiodatei laden.", "fr": "Chargez d'abord un fichier audio.",
        "ko": "먼저 오디오 파일을 불러오세요.", "pt": "Carregue um arquivo de áudio primeiro.",
        "zh": "请先加载音频文件。",
    },
    "sound.load_prompt": {
        "tr": "Ses dosyası yükleyin", "en": "Load an audio file",
        "ru": "Загрузите аудиофайл", "es": "Carga un archivo de audio",
        "de": "Audiodatei laden", "fr": "Chargez un fichier audio",
        "ko": "오디오 파일을 불러오세요", "pt": "Carregue um arquivo de áudio",
        "zh": "加载音频文件",
    },
    "sound.saved": {
        "tr": "Kaydedildi: {dur} sn, 44100 Hz 16-bit {ch}\n{path}",
        "en": "Saved: {dur} s, 44100 Hz 16-bit {ch}\n{path}",
        "ru": "Сохранено: {dur} с, 44100 Гц 16-бит {ch}\n{path}",
        "es": "Guardado: {dur} s, 44100 Hz 16-bit {ch}\n{path}",
        "de": "Gespeichert: {dur} s, 44100 Hz 16-bit {ch}\n{path}",
        "fr": "Enregistré : {dur} s, 44100 Hz 16-bit {ch}\n{path}",
        "ko": "저장됨: {dur} 초, 44100 Hz 16-bit {ch}\n{path}",
        "pt": "Salvo: {dur} s, 44100 Hz 16-bit {ch}\n{path}",
        "zh": "已保存：{dur} 秒, 44100 Hz 16-bit {ch}\n{path}",
    },
}


def available_languages():
    return list(LANGUAGES)


def get_language() -> str:
    return _current


def set_language(code: str) -> None:
    global _current
    if code in _CODES:
        _current = code


def detect_default() -> str:
    try:
        import locale
        code = (locale.getdefaultlocale()[0] or "en")[:2].lower()
    except Exception:
        code = "en"
    return code if code in _CODES else "en"


def t(key: str, **kwargs) -> str:
    entry = _STRINGS.get(key)
    if entry is None:
        return key
    text = entry.get(_current) or entry.get("en") or next(iter(entry.values()))
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text
    return text
