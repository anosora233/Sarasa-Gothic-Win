from pathlib import Path
from dataclasses import dataclass

from fontTools.ttLib import TTCollection


@dataclass
class Task:
    input: str
    output: str
    template: str


def convert(main, temp):
    main["name"] = temp["name"]

    if main["OS/2"].usWeightClass == 300:
        main["OS/2"].usWeightClass = 290

    main["GSUB"].table.ScriptList.ScriptRecord = [
        r
        for r in main["GSUB"].table.ScriptList.ScriptRecord
        if r.ScriptTag in ["grek", "cyrl", "latn", "DFLT"]
    ]  # Simplify GSUB


msyh = Path("./.msyh")

for task in [
    Task(
        input="out/TTC/Sarasa-Light.ttc",
        output="msyhl.ttc",
        template=msyh / "msyhl.ttc",
    ),
    Task(
        input="out/TTC/Sarasa-Regular.ttc",
        output="msyh.ttc",
        template=msyh / "msyh.ttc",
    ),
    Task(
        input="out/TTC/Sarasa-Bold.ttc",
        output="msyhbd.ttc",
        template=msyh / "msyhbd.ttc",
    ),
]:
    sara = TTCollection(task.input)
    msyh = TTCollection(task.template)

    for m in [0, 1]:
        convert(sara.fonts[m], msyh.fonts[m])

    sara.save(task.output)
