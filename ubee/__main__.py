"""Gen ubee main."""
# pylint: disable=unused-import, wrong-import-position, wrong-import-order, too-many-locals, broad-except

from typing import Tuple, Optional

from pathlib import Path
import sys
from random import shuffle

from itertools import zip_longest
from textwrap import dedent

import gradio as gr

import pandas as pd
from icecream import install as ic_install, ic
import logzero
from logzero import logger

# for embeddable python
if "." not in sys.path:
    sys.path.insert(0, ".")

from ubee.ubee import ubee

# logzero.loglevel(10)
ic_install()
ic.configureOutput(
    includeContext=True,
    outputFunction=logger.info,
)
ic.enable()
# ic.disenable()  # to turn off


def greet1(name):
    """Dummy."""
    return "Hello " + name + "!!"


def greet(
    text1,
    text2,
    thresh: float
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Take inputs, return outputs.

    Args:
        text1: text
        text2: text
    Returns:
        pd.DataFrame
    """
    res1 = [elm.strip() for elm in text1.splitlines() if elm.strip()]
    res2 = [elm.strip() for elm in text2.splitlines() if elm.strip()]

    ic(res1)
    ic(res2)

    # _ = pd.DataFrame(zip_longest(res1, res2), columns=["text1", "text2"])
    # return _

    res1_, res2_ = ubee(res1, res2, thresh)

    out_df = pd.DataFrame(
        zip_longest(res1, res2),
        columns=["text1", "text2"],
    )

    if res2_:
        _ = pd.DataFrame(res2_, columns=["text1", "text2"])
    else:
        _ = None

    return out_df, pd.DataFrame(res1_, columns=["text1", "text2", "likelihood"]), _


def main():
    """Create main entry."""
    text_zh = Path("data/test_zh.txt").read_text(encoding="utf8")
    text_zh = [elm.strip() for elm in text_zh.splitlines() if elm.strip()][:10]
    text_zh = "\n\n".join(text_zh)

    text_en = [
        elm.strip()
        for elm in Path("data/test_en.txt").read_text(encoding="utf8").splitlines()
        if elm.strip()
    ]
    _ = text_en[:9]
    shuffle(_)
    text_en = "\n\n".join(_)

    title = "Ultimatumbee Aligner"
    theme = "dark-grass"
    theme = "grass"
    description = """WIP showcasing a novel aligner"""
    article = dedent("""
        ## NB

        *   The ultimatumbee aligner (``ubee`` for short) is intended for aligning text blocks (be it paragraphs, sentences or words). Since it is rather slow (30 para pairs (Wuthering Height ch1. for example) can take 10 to 20 mniutes), anything more than 50 blocks should probably be avaoided. Nevertheless, you are welcome to try. No big brother is watching.

        *   ``thresh``: longer text blocks justify a larger value; `.5` appears to be just right for paragraphs for Wuthering Height ch1.

        Stay tuned for more details coming soon...
        """).strip()
    examples = [
        ["yo\nme", "你\n我", .5],
        ["me\nshe", "你\n她", .5],
    ]

    lines = 15
    placeholder = "Type or paste text here"
    default1 = text_zh
    default2 = text_en
    label1 = "text1"
    label2 = "text2"
    inputs = [
        gr.inputs.Textbox(
            lines=lines, placeholder=placeholder, default=default1, label=label1
        ),
        gr.inputs.Textbox(
            lines=lines, placeholder=placeholder, default=default2, label=label2
        ),
        gr.inputs.Slider(
            minimum=0.0,
            maximum=1.0,
            step=0.1,
            default=0.5,
        ),
    ]

    out_df = gr.outputs.Dataframe(
        headers=None,
        max_rows=lines,  # 20
        max_cols=None,
        overflow_row_behaviour="paginate",
        type="auto",
        label="To be aligned",
    )
    aligned = gr.outputs.Dataframe(
        headers=None,
        max_rows=lines,  # 20
        max_cols=None,
        overflow_row_behaviour="paginate",
        type="auto",
        label="Aligned",
    )
    leftover = gr.outputs.Dataframe(
        headers=None,
        max_rows=lines,  # 20
        max_cols=None,
        overflow_row_behaviour="paginate",
        type="auto",
        label="Leftover",
    )
    outputs = [  # tot. 3
        out_df,
        aligned,
        leftover,
    ]

    iface = gr.Interface(
        fn=greet,
        # fn=ubee,
        title=title,
        theme=theme,
        layout="vertical",  # horizontal unaligned
        description=description,
        article=article,
        # inputs="text",
        # outputs="text",
        inputs=inputs,
        outputs=outputs,
        examples=examples,
        # enable_queue=True,
    )
    iface.launch(
        enable_queue=True,
        share=True,
    )


if __name__ == "__main__":
    main()
