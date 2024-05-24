from os import environ
from pathlib import Path
from dataclasses import dataclass

from fontTools.ttLib import TTCollection

YAHEI_PATH = Path(environ.get("YAHEI_PATH", "C:\\Windows\\Fonts"))


@dataclass
class Task:
    input: str
    output: str
    template: str


def convert(main, temp):
    main["name"] = temp["name"]
    main["gasp"] = temp["gasp"]

    main["OS/2"].usWinAscent = temp["OS/2"].usWinAscent
    main["OS/2"].usWinDescent = temp["OS/2"].usWinDescent

    if main["OS/2"].usWeightClass == 300:
        main["OS/2"].usWeightClass = 290

    main["GSUB"].table.ScriptList.ScriptRecord = [
        R for R in main["GSUB"].table.ScriptList.ScriptRecord if R.ScriptTag != "hani"
    ]  # Remove LangSys `hani` to avoid slow rendering

    def calcu(tota, diff):
        a, b, c, d = 1, 1, 1, -1
        determinant = a * d - c * b
        x = (tota * d - diff * b) / determinant
        y = (a * diff - c * tota) / determinant
        return int(x), int(y)

    tota = main["OS/2"].sTypoAscender + main["OS/2"].sTypoDescender
    diff = 2180
    main["OS/2"].sTypoAscender, main["OS/2"].sTypoDescender = calcu(tota, diff)
    main["OS/2"].fsSelection = temp["OS/2"].fsSelection

    main["hhea"].ascent = temp["hhea"].ascent
    main["hhea"].descent = temp["hhea"].descent


for task in [
    Task(
        input="out/TTC/Sarasa-Light.ttc",
        output="msyhl.ttc",
        template=YAHEI_PATH / "msyhl.ttc",
    ),
    Task(
        input="out/TTC/Sarasa-Regular.ttc",
        output="msyh.ttc",
        template=YAHEI_PATH / "msyh.ttc",
    ),
    Task(
        input="out/TTC/Sarasa-Bold.ttc",
        output="msyhbd.ttc",
        template=YAHEI_PATH / "msyhbd.ttc",
    ),
]:
    sara = TTCollection(task.input)
    msyh = TTCollection(task.template)

    for m in [0, 1]:
        convert(sara.fonts[m], msyh.fonts[m])

    sara.save(task.output)
