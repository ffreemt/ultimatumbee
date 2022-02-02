"""Gen ubee main."""
# pylint: disable=unused-import, wrong-import-position

from typing import Tuple

from pathlib import Path
import sys
from random import shuffle

# from itertools import zip_longest
# from textwrap import dedent

import gradio as gr

import pandas as pd
from icecream import install as ic_install, ic
import logzero
from logzero import logger

# for embeddable python
if "." not in sys.path:
    sys.path.insert(0, ".")

from ubee.ubee import ubee

logzero.loglevel(10)
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
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Take inputs, return outputs.

    Args:
        text1: text
        text2: text
    Returns:
        pd.DataFrame
    """
    res1 = [elm.strip() for elm in text1.splitlines() if elm.strip()]
    res2 = [elm.strip() for elm in text2.splitlines() if elm.strip()]

    # _ = pd.DataFrame(zip_longest(res1, res2), columns=["text1", "text2"])
    # return _

    res1_, res2_ = ubee(res1, res2, thresh)

    return pd.DataFrame(res1_, columns=["text1", "text2", "likelihood"]), pd.DataFrame(res2_, columns=["text1", "text2"])


def main():
    """Create main entry."""
    text_zh = Path("data/test_zh.txt").read_text("utf8")
    text_en = [
        elm.strip()
        for elm in Path("data/test_en.txt").read_text("utf8").splitlines()
        if elm.strip()
    ]
    shuffle(text_en)
    text_en = "\n\n".join(text_en)

    title = "Ultimatumbee Aligner"
    theme = "dark-grass"
    description = """WIP showcasing a novel aligner"""
    article = """Stay tuned for more details coming soon...
        """
    examples = [
        ["yo\nme", "你\n我"],
        ["me\nshe", "你\n她", ],
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
    )
    iface.launch(enable_queue=False)


if __name__ == "__main__":
    main()
