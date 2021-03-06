"""Gen ubee main.

private
url = 'https://hf.space/embed/mikeee/zero-shot/+/api/predict'
resp = httpx.post(
    url,
    json={"data": ["love", ",".join(["liebe", "this is test", "hate you"]), False]},
    timeout=httpx.Timeout(None, connect=3),
)
resp.json()
{'data': [{'label': 'liebe',
   'confidences': [{'label': 'liebe', 'confidence': 0.8688847422599792},
    {'label': 'this is test', 'confidence': 0.12558135390281677},
    {'label': 'hate you', 'confidence': 0.005533925257623196}]}],
 'duration': 0.265749454498291,
 'average_duration': 4.639325571060181}

"""
# pylint: disable=unused-import, wrong-import-position, wrong-import-order, too-many-locals, broad-except, line-too-long

import sys
from itertools import zip_longest
from pathlib import Path
from random import shuffle
from textwrap import dedent
from typing import Optional, Tuple

import gradio as gr
import logzero
import pandas as pd
from icecream import ic
from icecream import install as ic_install
from logzero import logger
from set_loglevel import set_loglevel
logzero.loglevel(set_loglevel())

# for embeddable python
# if "." not in sys.path: sys.path.insert(0, ".")

from ubee import __version__
from ubee.ubee import ubee

# logzero.loglevel(10)
logger.debug(" debug on ")

ic_install()
ic.configureOutput(
    includeContext=True,
    outputFunction=logger.info,
)
ic.enable()
# ic.disenable()  # to turn off

ic(" ic.enabled ")

_ = """
ic("Testing...")
import model_pool
from model_pool import fetch_check_aux
print("model-pool version", model_pool.__version__)
print("gradio version", gr.__version__)

try:
    fetch_check_aux.fetch_check_aux()
except Exception as _:
    ic(["fetch_check_aux.fetch_check_aux", _])

from model_pool.load_model import load_model
try:
    clas = load_model("clas-l-user")
except Exception as _:
    ic(["load_model(\"clas-l-user\")", _])
# """

# _ = clas("love", ["liebe", "hate you", "test"])
# print(_)
# raise SystemExit("Exit by intention")
# {'sequence': 'love', 'labels': ['liebe', 'test', 'hate you'],
# 'scores': [0.8885253667831421, 0.10581762343645096, 0.005657028406858444]}
# Runs OK

# text1 = ""
# text2 = ""
# thresh: float = 0.4


# segment: str
def ifn(
    text1,
    text2,
    thresh
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
    # res1_, res2_ = res1, res2

    out_df = pd.DataFrame(
        zip_longest(res1, res2),
        columns=["text1", "text2"],
    )

    if res2_:
        _ = pd.DataFrame(res2_, columns=["text1", "text2"])
    else:
        _ = None

    # return out_df, pd.DataFrame(res1_, columns=["text1", "text2", "likelihood"]), _
    return pd.DataFrame(res1_, columns=["text1", "text2", "likelihood"]), _


def main():
    """Create main entry."""
    # global text1, text2, threash

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

    title = "Ultimatumbee"
    theme = "dark-grass"
    theme = "grass"
    description = """WIP showcasing a novel aligner"""
    article = dedent("""
        ## NB

        *   The ultimatumbee aligner (``ubee`` for short) is intended for aligning text blocks (be it paragraphs, sentences or words). Since it is rather slow (30 para pairs (Wuthering Height ch1. for example) can take 10 to 20 mniutes), anything more than 50 blocks should probably be avaoided. Nevertheless, you are welcome to try. No big brother is watching.

        *   ``thresh``: longer text blocks justify a larger value; `.5` appears to be just right for paragraphs for Wuthering Height ch1.

        Stay tuned for more details coming soon...
        """).strip()

    ex1_zh = [
        '?????????????????????',
        '??????????????????????????????',
        '??????????????????????????????????????????????????????????????????????????????????????????', '???????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????',
        '????????????????????????????????????????????????????????????????????????????????????', '?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????',
        '?????????????????????????????????????????????',
        '???????????????????????????????????????????????????????????????'
    ]
    ex1_en = [
        'The snow began to drive thickly.',
        'I seized the handle to essay another trial; when a young man without coat, and shouldering a pitchfork, appeared in the yard behind.',
        'He hailed me to follow him, and, after marching through a wash-house, and a paved area containing a coal shed, pump, and pigeon cot, we at length arrived in the huge, warm, cheerful apartment, where I was formerly received.',
        "It glowed delightfully in the radiance of an immense fire, compounded of coal, peat, and wood; and near the table, laid for a plentiful evening meal, I was pleased to observe the `missis', an individual whose existence I had never previously suspected.",
        'I bowed and waited, thinking she would bid me take a seat.',
        'She looked at me, leaning back in her chair, and remained motionless and mute.'
    ]
    shuffle(ex1_en)
    ex1_zh = "\n".join(ex1_zh)
    ex1_en = "\n".join(ex1_en)

    ex2_zh = "???\n??????\n???\n???\n??????\n??????\n??????\n???\n???\n???\n???\n??????"
    ex2_en = "She looked at me leaning back in her chair and remained motionless and mute".split()
    shuffle(ex2_en)
    ex2_en = "\n".join(ex2_en)

    examples = [
        [ex2_zh, ex2_en, .3],
        [text_zh, text_en, .5],
    ]
    lines = 15
    placeholder = "Type or paste text here"

    blocks = gr.Blocks()

    with blocks:
        gr.Markdown(
            dedent(f"""
            ## Ultimatumbee {__version__}

            Align non-sequential dualtexts.

            ????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????? threshold ????????? -- ?????? 0.3?????????0.5??? ?????? 0.7??????????????? leftover?????????????????? threshold??? ??????????????????????????????????????? threshold???

            """).strip()
        )
        with gr.Column():
            with gr.Row():
                text1 = gr.Textbox(
                    lines=lines,
                    placeholder=placeholder,
                    value=ex2_zh,
                    label="text1"
                )
                text2 = gr.Textbox(
                    lines=lines,
                    placeholder=placeholder,
                    value=ex2_en,
                    label="text2"
                )
            with gr.Row():
                thresh = gr.Slider(
                    minimum=0.0,
                    maximum=1.0,
                    step=0.1,
                    value=0.4,
                    label="threshold",
                )
                btn = gr.Button("Run")

            _ = """
            out_df = gr.Dataframe(
                headers=None,
                max_rows=lines,  # 20
                max_cols=None,
                overflow_row_behaviour="paginate",
                type="auto",
                label="To be aligned",
            )
            # """

            # with gr.Row():
            aligned = gr.Dataframe(
                headers=None,
                max_rows=lines,  # 20
                max_cols=None,
                overflow_row_behaviour="paginate",
                type="auto",
                label="Aligned",
            )

            leftover = gr.Dataframe(
                headers=None,
                max_rows=lines,  # 20
                max_cols=None,
                overflow_row_behaviour="paginate",
                type="auto",
                label="Leftover",
            )

            logger.debug("text1: %s", text1)
            logger.debug("text2: %s", text2)

            btn.click(
                fn=ifn,
                inputs=[
                    text1,
                    text2,
                    thresh,
                ],
                outputs=[
                    # out_df,
                    aligned,
                    leftover,
                ]
            )

    # blocks.launch()
    blocks.launch(debug=True, enable_queue=True)


if __name__ == "__main__":
    logger.info(" Start main()")
    main()

_ = """

        gr.inputs.Radio(
            ["para", "sent", "word"],
            default="para",
            label="segment"
        )
# """
