"""Gen ubee main."""
# pylint: disable=unused-import, wrong-import-position

import sys
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


def greet(text1, text2) -> pd.DataFrame:
    """Take inputs, return outputs.

    Args:
        text1: text
        text2: text
    Returns:
        pd.DataFrame
    """
    res1 = [elm.strip() for elm in text1.splitlines() if elm.strip()]
    res2 = [elm.strip() for elm in text2.splitlines() if elm.strip()]

    _ = pd.DataFrame(zip_longest(res1, res2), columns=["text1", "text2"])
    return _


def main():
    """Create main entry."""
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
    default1 = dedent(
        """
        test 1
        abc
        love you
        """
    )
    default2 = dedent(
        """
        爱你
        甲乙丙
        测试 1
        """
    )
    label1 = "text1"
    label2 = "text2"
    inputs = [
        gr.inputs.Textbox(
            lines=lines, placeholder=placeholder, default=default1, label=label1
        ),
        gr.inputs.Textbox(
            lines=lines, placeholder=placeholder, default=default2, label=label2
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
    outputs = [  # tot. 1
        out_df,
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
