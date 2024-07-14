import os


def scan_dir(path):
  content: list = os.listdir(path)

  for inner_content in content:
    inner_content_path = "/".join([path, inner_content])

    if os.path.isdir(inner_content_path):
      level += 1
      scan_dir(inner_content_path)
    elif os.path.isfile(inner_content_path):
      if str(inner_content)[-4:] == "html":
        with open(inner_content_path, "r", encoding="utf-8") as file:
          code = file.read()
          print(inner_content_path)
          try:
            before_header = code.split("<header>")[0]
            after_header = code.split("</header>")[1]
          except:
            continue

          print(code)
          print(f"""{before_header}<header>
    <div class="row">
      <div class="main-link">
        <a href="#section-cover">
          <img src="{"../" * level}static/imgs/logo-wo-bg.png" class="icon">
        </a>
      </div>
  
      <div class="links">
        <a href="{"../" * level}about/people/" class="link margin-left">Состав</a>
        <a href="{"../" * level}blog/" class="link margin-left">Блог</a>
        <a href="{"../" * level}top/" class="link margin-left">Топы</a>
      </div>
    </div>

    <div class="row">
      <div class="socials">
        <a href="https://t.me/BeJIuka9IuMnEpu9II22I" class="link social margin-left" target="_blank"><i class="fi fi-brands-telegram"></i></a>
        <a href="https://discord.gg/47fRgMfKC4" class="link social margin-left" target="_blank"><i class="fi fi-brands-discord"></i></a>

        <div class="button">Вступить</div>
      </div>
    </div>
  </header>{after_header}""")


if __name__ == "__main__":
  level = 0
  scan_dir("..")
