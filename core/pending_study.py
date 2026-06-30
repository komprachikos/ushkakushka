import json


FILE = "memory/pending_study.json"


def load_pending():

    with open(
        FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def save_pending(data):

    with open(
        FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )


def set_pending(
    topic,
    summary,
    opinion,
    related=None
):

    save_pending(
        {
            "topic": topic,
            "summary": summary,
            "opinion": opinion,
            "related": related or []
        }
    )


def clear_pending():

    save_pending({})